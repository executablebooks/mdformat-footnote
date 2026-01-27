from __future__ import annotations

from collections.abc import Mapping
import textwrap

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.footnote import footnote_plugin

from ._reorder import reorder_footnotes_by_definition


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, adding the footnote plugin."""
    mdit.use(footnote_plugin)
    # Disable inline footnotes for now, since we don't have rendering
    # support for them yet.
    mdit.disable("footnote_inline")
    # Reorder footnotes to match definition order and preserve orphans.
    # Must run before footnote_tail.
    mdit.core.ruler.before(
        "footnote_tail", "reorder_footnotes", reorder_footnotes_by_definition
    )


def _footnote_ref_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"[^{node.meta['label']}]"


def _footnote_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    first_line = f"[^{node.meta['label']}]:"
    indent = " " * 4
    elements = []

    first_child_idx = 0
    while (
        first_child_idx < len(node.children)
        and node.children[first_child_idx].type == "footnote_anchor"
    ):
        first_child_idx += 1

    if (
        first_child_idx < len(node.children)
        and node.children[first_child_idx].type == "paragraph"
    ):
        with context.indented(len(first_line) + 1):
            first_element = node.children[first_child_idx].render(context)

        first_element_lines = first_element.split("\n")
        first_para_first_line = first_element_lines[0]
        first_para_rest_lines = first_element_lines[1:]

        with context.indented(len(indent)):
            for child in node.children[first_child_idx + 1 :]:
                if child.type == "footnote_anchor":
                    continue
                elements.append(child.render(context))

        result = first_line + " " + first_para_first_line
        if first_para_rest_lines:
            indented_rest = textwrap.indent("\n".join(first_para_rest_lines), indent)
            result += "\n" + indented_rest
        if elements:
            result += "\n\n" + textwrap.indent("\n\n".join(elements), indent)
        return result

    with context.indented(len(indent)):
        for child in node.children:
            if child.type == "footnote_anchor":
                continue
            elements.append(child.render(context))
    body = textwrap.indent("\n\n".join(elements), indent)
    if body:
        body = "\n" + body
    return first_line + body


def _render_children(node: RenderTreeNode, context: RenderContext) -> str:
    return "\n\n".join(child.render(context) for child in node.children)


RENDERERS: Mapping[str, Render] = {
    "footnote": _footnote_renderer,
    "footnote_ref": _footnote_ref_renderer,
    "footnote_block": _render_children,
}
