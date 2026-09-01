"""Orphan handling for footnotes kept at their source position."""

from __future__ import annotations

from markdown_it.rules_core import StateCore

from ._reorder import (
    build_dependency_graph,
    categorize_footnotes,
    collect_refs_in_fences,
)


def _drop_footnote_spans(tokens: list, labels: set[str]) -> list:
    """Remove footnote_reference_open/close spans for the given labels."""
    kept = []
    skip = False
    for token in tokens:
        if token.type == "footnote_reference_open":
            skip = token.meta.get("label") in labels
            if skip:
                continue
        elif token.type == "footnote_reference_close" and skip:
            skip = False
            continue
        if not skip:
            kept.append(token)
    return kept


def strip_orphan_footnotes(state: StateCore, keep_orphans: bool = False) -> None:
    """Remove footnote definitions that are never referenced, in place."""
    if keep_orphans:
        return

    footnote_data = state.env.get("footnotes", {})
    refs = footnote_data.get("refs", {})
    if not refs:
        return

    footnote_deps = build_dependency_graph(state.tokens)
    refs_in_fences = collect_refs_in_fences(state.tokens)
    categories = categorize_footnotes(refs, footnote_deps, refs_in_fences)
    if not categories.true_orphans:
        return

    for label_key in categories.true_orphans:
        del refs[label_key]

    orphan_labels = {label_key[1:] for label_key in categories.true_orphans}
    state.tokens = _drop_footnote_spans(state.tokens, orphan_labels)
