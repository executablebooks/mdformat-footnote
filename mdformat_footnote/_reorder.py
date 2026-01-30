"""Footnote ID and subId normalization logic."""

from __future__ import annotations

from dataclasses import dataclass, field
import re

from markdown_it.rules_core import StateCore

_FOOTNOTE_REF_PATTERN = re.compile(r"\[\^([^\]]+)\]")


@dataclass
class _FootnoteCategories:
    """Categorized footnotes for reordering."""

    body_referenced: list[tuple[int, str, str]]
    nested_only: set[str]
    fence_only: list[str]
    true_orphans: list[str]

    @property
    def body_labels(self) -> set[str]:
        return {label for _, _, label in self.body_referenced}


@dataclass
class _ReorderState:
    """Mutable state for footnote reordering."""

    old_list: dict
    refs: dict
    new_list: dict = field(default_factory=dict)
    old_to_new_id: dict[int, int] = field(default_factory=dict)
    processed: set[str] = field(default_factory=set)
    new_id: int = 0

    def _find_def_by_label(self, label: str) -> dict:
        for fn_data in self.old_list.values():
            if fn_data.get("label") == label:
                return fn_data.copy()
        return {"label": label, "count": 0}

    def _find_old_id_by_label(self, label: str) -> int | None:
        for old_id, fn_data in self.old_list.items():
            if fn_data.get("label") == label:
                return old_id
        return None

    def add_footnote(
        self, label: str, label_key: str, old_id: int | None = None
    ) -> None:
        """Add a footnote to the new list and update mappings."""
        if label in self.processed:
            return

        self.new_list[self.new_id] = self._find_def_by_label(label)

        effective_old_id = old_id or self._find_old_id_by_label(label)
        if effective_old_id is not None:
            self.old_to_new_id[effective_old_id] = self.new_id

        self.refs[label_key] = self.new_id
        self.processed.add(label)
        self.new_id += 1


def _collect_refs_in_fences(tokens: list) -> list[str]:
    """Collect footnote labels referenced in fence tokens, preserving order."""
    refs: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        if token.type != "fence" or not token.content:
            continue
        for match in _FOOTNOTE_REF_PATTERN.finditer(token.content):
            label = match.group(1)
            if label not in seen:
                refs.append(label)
                seen.add(label)
    return refs


def _build_dependency_graph(tokens: list) -> dict[str, set[str]]:
    """Build a graph of which footnotes reference which others."""
    graph: dict[str, set[str]] = {}
    current_def_label: str | None = None

    for token in tokens:
        match token.type:
            case "footnote_reference_open":
                current_def_label = token.meta.get("label")
                if current_def_label:
                    graph.setdefault(current_def_label, set())
            case "footnote_reference_close":
                current_def_label = None
            case _ if current_def_label is not None:
                _collect_nested_refs(token, graph[current_def_label])

    return graph


def _collect_nested_refs(token, ref_set: set[str]) -> None:
    """Collect footnote labels referenced from a token and its children."""
    if token.type == "footnote_ref" and token.meta:
        ref_set.add(token.meta["label"])
    for child in token.children or []:
        _collect_nested_refs(child, ref_set)


def _categorize_footnotes(
    refs: dict,
    footnote_deps: dict[str, set[str]],
    refs_in_fences: list[str],
) -> _FootnoteCategories:
    """Categorize footnotes."""
    referenced_by_footnotes: set[str] = set()
    for refs_set in footnote_deps.values():
        referenced_by_footnotes.update(refs_set)

    refs_in_fences_set = set(refs_in_fences)

    body_referenced: list[tuple[int, str, str]] = []
    nested_only: set[str] = set()
    fence_only_set: set[str] = set()
    true_orphans: list[str] = []

    for label_key, old_id in refs.items():
        label = label_key[1:]
        match (
            old_id >= 0,
            label in referenced_by_footnotes,
            label in refs_in_fences_set,
        ):
            case (True, _, _):
                body_referenced.append((old_id, label_key, label))
            case (False, True, _):
                nested_only.add(label)
            case (False, False, True):
                fence_only_set.add(label)
            case _:
                true_orphans.append(label_key)

    body_referenced.sort(key=lambda x: x[0])
    fence_only = [label for label in refs_in_fences if label in fence_only_set]

    return _FootnoteCategories(body_referenced, nested_only, fence_only, true_orphans)


def _process_nested_for_parent(
    parent_label: str,
    footnote_deps: dict[str, set[str]],
    state: _ReorderState,
    skip_labels: set[str],
) -> None:
    """Process nested footnotes referenced by a parent footnote."""
    for nested_label in footnote_deps.get(parent_label, []):
        if nested_label not in skip_labels:
            state.add_footnote(nested_label, f":{nested_label}")


def _build_reordered_list(
    categories: _FootnoteCategories,
    footnote_deps: dict[str, set[str]],
    old_list: dict,
    refs: dict,
    keep_orphans: bool,
) -> _ReorderState:
    """Build the reordered footnote list from categorized footnotes."""
    state = _ReorderState(old_list=old_list, refs=refs)
    skip_labels = categories.body_labels | set(categories.true_orphans)

    for old_id, label_key, label in categories.body_referenced:
        state.add_footnote(label, label_key, old_id)
        _process_nested_for_parent(label, footnote_deps, state, skip_labels)

    for nested_label in categories.nested_only:
        state.add_footnote(nested_label, f":{nested_label}")

    for fence_label in categories.fence_only:
        state.add_footnote(fence_label, f":{fence_label}")

    if keep_orphans:
        for orphan_key in categories.true_orphans:
            state.add_footnote(orphan_key[1:], orphan_key)

    return state


def _update_token_ids(tokens: list, old_to_new_id: dict[int, int]) -> None:
    """Recursively update footnote IDs in tokens."""
    for token in tokens:
        if token.type in ("footnote_ref", "footnote_anchor"):
            if token.meta and (old_id := token.meta.get("id")) in old_to_new_id:
                token.meta["id"] = old_to_new_id[old_id]
        for child in token.children or []:
            _update_token_ids([child], old_to_new_id)


def _partition_refs_by_context(tokens: list) -> tuple[list, dict[str, list]]:
    """Partition footnote refs into body refs and definition refs."""
    body_refs: list = []
    def_refs: dict[str, list] = {}
    current_def_label: str | None = None

    for token in tokens:
        match token.type:
            case "footnote_reference_open":
                current_def_label = token.meta.get("label")
                if current_def_label:
                    def_refs.setdefault(current_def_label, [])
            case "footnote_reference_close":
                current_def_label = None
            case _ if current_def_label is None:
                _collect_refs(token, body_refs)
            case _:
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
    for child in token.children or []:
        _collect_refs(child, ref_list)


def _get_footnote_data(state: StateCore) -> tuple[dict, dict] | None:
    """Extract footnote refs and list from state, or None if missing."""
    footnote_data = state.env.get("footnotes", {})
    refs = footnote_data.get("refs", {})
    if not refs:
        return None
    return refs, footnote_data.get("list", {})


def reorder_footnotes_by_definition(
    state: StateCore, keep_orphans: bool = False
) -> None:
    """Reorder footnotes by reference order, fix IDs, and handle orphans."""
    if (data := _get_footnote_data(state)) is None:
        return

    refs, old_list = data
    footnote_deps = _build_dependency_graph(state.tokens)
    refs_in_fences = _collect_refs_in_fences(state.tokens)
    categories = _categorize_footnotes(refs, footnote_deps, refs_in_fences)

    if not keep_orphans:
        for orphan_key in categories.true_orphans:
            del refs[orphan_key]

    reorder_state = _build_reordered_list(
        categories, footnote_deps, old_list, refs, keep_orphans
    )

    state.env["footnotes"]["list"] = reorder_state.new_list
    _update_token_ids(state.tokens, reorder_state.old_to_new_id)
    _reassign_subids(state.tokens, refs, reorder_state.new_list)
