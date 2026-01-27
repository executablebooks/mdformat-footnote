from __future__ import annotations

from collections.abc import Mapping
import textwrap

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.footnote import footnote_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, adding the footnote plugin."""
    mdit.use(footnote_plugin)
    # Disable inline footnotes for now, since we don't have rendering
    # support for them yet.
    mdit.disable("footnote_inline")


def _footnote_ref_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"[^{node.meta['label']}]"


def _footnote_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    first_line = f"[^{node.meta['label']}]:"
    indent = " " * 4

    children = [c for c in node.children if c.type != "footnote_anchor"]

    if children and children[0].type == "paragraph":
        with context.indented(len(first_line) + 1):
            first_element = children[0].render(context)

        first_para_first_line, *first_para_rest_lines = first_element.split("\n")

        with context.indented(len(indent)):
            elements = [child.render(context) for child in children[1:]]

        result = first_line + " " + first_para_first_line
        if first_para_rest_lines:
            result += "\n" + textwrap.indent("\n".join(first_para_rest_lines), indent)
        if elements:
            result += "\n\n" + textwrap.indent("\n\n".join(elements), indent)
        return result

    with context.indented(len(indent)):
        elements = [child.render(context) for child in children]
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
