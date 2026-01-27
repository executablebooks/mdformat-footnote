"""Footnote ID and subId normalization logic."""

from __future__ import annotations

from markdown_it.rules_core import StateCore


def reorder_footnotes_by_definition(state: StateCore) -> None:
    """Reorder footnotes to match definition order and normalize subIds.

    The mdit-py-plugins footnote plugin assigns IDs and subIds based on the
    order the references are encountered during inline parsing. This causes
    HTML to differ when footnote definitions are reordered by the formatter

    This rule:
    1. Preserves orphan footnotes (defined but never referenced)
    2. Reorders the footnote list to match definition order
    3. Updates all token IDs to match the new ordering
    4. Reassigns subIds based on output order (body first, then definitions)

    This ensures consistent HTML output regardless of definition position.
    """
    if "footnotes" not in state.env:
        return

    footnote_data = state.env["footnotes"]
    refs = footnote_data.get("refs", {})
    old_list = footnote_data.get("list", {})

    if not refs:
        return

    new_list: dict[int, dict] = {}
    old_to_new_id: dict[int, int] = {}

    for new_id, label_key in enumerate(refs.keys()):
        label = label_key[1:]
        old_id = refs[label_key]

        if old_id >= 0 and old_id in old_list:
            new_list[new_id] = old_list[old_id].copy()
        else:
            new_list[new_id] = {"label": label, "count": 0}

        if old_id >= 0:
            old_to_new_id[old_id] = new_id
        refs[label_key] = new_id

    footnote_data["list"] = new_list

    _update_token_ids(state.tokens, old_to_new_id)
    _reassign_subids(state.tokens, refs, new_list)


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


def _partition_refs_by_context(
    tokens: list,
) -> tuple[list, dict[str, list]]:
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

    for label_key in refs.keys():
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
    if hasattr(token, "children") and token.children:
        for child in token.children:
            _collect_refs(child, ref_list)
