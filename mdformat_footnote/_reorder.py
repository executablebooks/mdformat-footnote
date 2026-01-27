"""Footnote ID and subId normalization logic."""

from __future__ import annotations

from dataclasses import dataclass, field

from markdown_it.rules_core import StateCore


@dataclass
class _ReorderState:
    """Mutable state for footnote reordering."""

    old_list: dict
    refs: dict
    new_list: dict = field(default_factory=dict)
    old_to_new_id: dict[int, int] = field(default_factory=dict)
    processed: set[str] = field(default_factory=set)
    new_id: int = 0

    def get_or_create_def(self, label: str) -> dict:
        """Get footnote definition by label, or create a default."""
        for fn_data in self.old_list.values():
            if fn_data.get("label") == label:
                return fn_data.copy()
        return {"label": label, "count": 0}

    def find_old_id_by_label(self, label: str) -> int | None:
        """Find the old ID for a label in old_list."""
        for old_id, fn_data in self.old_list.items():
            if fn_data.get("label") == label:
                return old_id
        return None

    def add_footnote(
        self, label: str, label_key: str, old_id: int | None = None
    ) -> None:
        """Add a footnote to the new list and update mappings."""
        self.new_list[self.new_id] = self.get_or_create_def(label)

        if old_id is not None:
            self.old_to_new_id[old_id] = self.new_id
        elif (found_id := self.find_old_id_by_label(label)) is not None:
            self.old_to_new_id[found_id] = self.new_id

        self.refs[label_key] = self.new_id
        self.processed.add(label)
        self.new_id += 1


def _categorize_footnotes(
    refs: dict,
    footnote_deps: dict[str, set[str]],
) -> tuple[list[tuple[int, str, str]], set[str], list[str]]:
    """Categorize footnotes into body-referenced, nested-only, and orphans.

    Returns:
        Tuple of (body_referenced, nested_only, true_orphans) where:
        - body_referenced: list of (old_id, label_key, label) sorted by old_id
        - nested_only: set of labels only referenced from other footnotes
        - true_orphans: list of label_keys never referenced anywhere
    """
    referenced_by_footnotes: set[str] = set()
    for refs_set in footnote_deps.values():
        referenced_by_footnotes.update(refs_set)

    body_referenced: list[tuple[int, str, str]] = []
    nested_only: set[str] = set()
    true_orphans: list[str] = []

    for label_key, old_id in refs.items():
        label = label_key[1:]
        if old_id >= 0:
            body_referenced.append((old_id, label_key, label))
        elif label in referenced_by_footnotes:
            nested_only.add(label)
        else:
            true_orphans.append(label_key)

    body_referenced.sort(key=lambda x: x[0])
    return body_referenced, nested_only, true_orphans


def _should_skip_nested(
    label: str,
    state: _ReorderState,
    body_referenced_labels: set[str],
    true_orphans: list[str],
) -> bool:
    """Check if a nested footnote should be skipped."""
    if label in state.processed:
        return True
    if label in body_referenced_labels:
        return True
    if f":{label}" in true_orphans:
        return True
    return False


def _process_nested_footnotes(
    parent_label: str,
    footnote_deps: dict[str, set[str]],
    state: _ReorderState,
    body_referenced_labels: set[str],
    true_orphans: list[str],
) -> None:
    """Process nested footnotes referenced by a parent footnote."""
    if parent_label not in footnote_deps:
        return

    for nested_label in footnote_deps[parent_label]:
        if _should_skip_nested(
            nested_label, state, body_referenced_labels, true_orphans
        ):
            continue
        state.add_footnote(nested_label, f":{nested_label}")


def reorder_footnotes_by_definition(
    state: StateCore, keep_orphans: bool = False
) -> None:
    """Reorder footnotes by reference order, fix IDs, and handle orphans.

    The mdit-py-plugins footnote plugin assigns IDs based on the order
    references are encountered during inline parsing. This function:
    1. Sorts footnotes by reference order (order they appear in body text)
    2. Keeps nested footnotes (referenced from other footnotes) with their parents
    3. Removes true orphans (never referenced) unless keep_orphans=True
    4. Reassigns IDs to ensure consistent HTML output

    Args:
        state: markdown-it state
        keep_orphans: If True, preserve footnotes that are never referenced
    """
    if "footnotes" not in state.env:
        return

    footnote_data = state.env["footnotes"]
    refs = footnote_data.get("refs", {})
    old_list = footnote_data.get("list", {})

    if not refs:
        return

    footnote_deps = _build_dependency_graph(state.tokens)
    body_referenced, nested_only, true_orphans = _categorize_footnotes(
        refs, footnote_deps
    )

    if not keep_orphans:
        for orphan_key in true_orphans:
            del refs[orphan_key]

    body_referenced_labels = {label for _, _, label in body_referenced}
    reorder_state = _ReorderState(old_list=old_list, refs=refs)

    for old_id, label_key, label in body_referenced:
        reorder_state.add_footnote(label, label_key, old_id)
        _process_nested_footnotes(
            label, footnote_deps, reorder_state, body_referenced_labels, true_orphans
        )

    for nested_label in nested_only - reorder_state.processed:
        reorder_state.add_footnote(nested_label, f":{nested_label}")

    if keep_orphans:
        for orphan_key in true_orphans:
            reorder_state.add_footnote(orphan_key[1:], orphan_key)

    footnote_data["list"] = reorder_state.new_list

    _update_token_ids(state.tokens, reorder_state.old_to_new_id)
    _reassign_subids(state.tokens, refs, reorder_state.new_list)


def _build_dependency_graph(tokens: list) -> dict[str, set[str]]:
    """Build a graph of which footnotes reference which others.

    Returns:
        Dict mapping footnote label to set of labels it references
    """
    graph: dict[str, set[str]] = {}
    current_def_label: str | None = None

    for token in tokens:
        if token.type == "footnote_reference_open":
            current_def_label = token.meta.get("label")
            if current_def_label:
                graph.setdefault(current_def_label, set())
        elif token.type == "footnote_reference_close":
            current_def_label = None
        elif current_def_label is not None:
            _collect_nested_refs(token, graph[current_def_label])

    return graph


def _collect_nested_refs(token, ref_set: set[str]) -> None:
    """Collect footnote labels referenced from a token and its children."""
    if token.type == "footnote_ref" and token.meta:
        ref_set.add(token.meta["label"])
    if token.children:
        for child in token.children:
            _collect_nested_refs(child, ref_set)


def _update_token_ids(tokens: list, old_to_new_id: dict[int, int]) -> None:
    """Recursively update footnote IDs in tokens."""
    for token in tokens:
        if token.type in ("footnote_ref", "footnote_anchor"):
            if token.meta and "id" in token.meta:
                old_id = token.meta["id"]
                if old_id in old_to_new_id:
                    token.meta["id"] = old_to_new_id[old_id]
        if token.children:
            _update_token_ids(token.children, old_to_new_id)


def _partition_refs_by_context(tokens: list) -> tuple[list, dict[str, list]]:
    """Partition footnote refs into body refs and definition refs."""
    body_refs: list = []
    def_refs: dict[str, list] = {}
    current_def_label: str | None = None

    for token in tokens:
        if token.type == "footnote_reference_open":
            current_def_label = token.meta.get("label")
            if current_def_label:
                def_refs.setdefault(current_def_label, [])
        elif token.type == "footnote_reference_close":
            current_def_label = None
        elif current_def_label is None:
            _collect_refs(token, body_refs)
        else:
            _collect_refs(token, def_refs.setdefault(current_def_label, []))

    return body_refs, def_refs


def _assign_subids_to_refs(ref_tokens: list, counters: dict[int, int]) -> None:
    """Assign sequential subIds to a list of ref tokens."""
    for ref_token in ref_tokens:
        fn_id = ref_token.meta["id"]
        ref_token.meta["subId"] = counters.get(fn_id, 0)
        counters[fn_id] = counters.get(fn_id, 0) + 1


def _reassign_subids(tokens: list, refs: dict, footnote_list: dict) -> None:
    """Reassign subIds based on output order: body refs first, then definition refs."""
    body_refs, def_refs = _partition_refs_by_context(tokens)
    subid_counters: dict[int, int] = {}

    _assign_subids_to_refs(body_refs, subid_counters)

    for label_key in refs:
        label = label_key[1:]
        if label in def_refs:
            _assign_subids_to_refs(def_refs[label], subid_counters)

    for fn_id, count in subid_counters.items():
        if fn_id in footnote_list:
            footnote_list[fn_id]["count"] = count


def _collect_refs(token, ref_list: list) -> None:
    """Collect footnote_ref tokens from a token and its children."""
    if token.type == "footnote_ref" and token.meta:
        ref_list.append(token)
    if token.children:
        for child in token.children:
            _collect_refs(child, ref_list)
