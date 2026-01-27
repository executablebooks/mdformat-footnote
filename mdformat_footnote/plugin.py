from __future__ import annotations

import argparse
from collections.abc import Mapping
from functools import partial
import textwrap

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.footnote import footnote_plugin

from ._helpers import ContextOptions, get_conf
from ._reorder import reorder_footnotes_by_definition


def _keep_orphans(options: ContextOptions) -> bool:
    """Check if orphan footnotes should be preserved."""
    return bool(get_conf(options, "keep_orphans")) or False


def add_cli_argument_group(group: argparse._ArgumentGroup) -> None:
    """Add options to the mdformat CLI.

    Stored in `mdit.options["mdformat"]["plugin"]["footnote"]`
    """
    group.add_argument(
        "--keep-footnote-orphans",
        action="store_const",
        const=True,
        dest="keep_orphans",
        help=(
            "Keep footnote definitions that are never referenced "
            "(default: remove them)"
        ),
    )


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, adding the footnote plugin."""
    mdit.use(footnote_plugin)
    # Disable inline footnotes for now, since we don't have rendering
    # support for them yet.
    mdit.disable("footnote_inline")
    # Reorder footnotes by reference order, fix IDs, and handle orphans.
    # Must run before footnote_tail.
    keep_orphans = _keep_orphans(mdit.options)
    reorder_fn = partial(reorder_footnotes_by_definition, keep_orphans=keep_orphans)
    mdit.core.ruler.before("footnote_tail", "reorder_footnotes", reorder_fn)


def _footnote_ref_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"[^{node.meta['label']}]"


def _footnote_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    first_line = f"[^{node.meta['label']}]:"
    indent = " " * 4
    elements = []
    with context.indented(len(indent)):
        for child in node.children:
            if child.type == "footnote_anchor":
                continue
            elements.append(child.render(context))
    body = textwrap.indent("\n\n".join(elements), indent)
    # if the first body element is a paragraph, we can start on the first line,
    # otherwise we start on the second line
    if body and node.children and node.children[0].type != "paragraph":
        body = "\n" + body
    else:
        body = " " + body.lstrip()
    return first_line + body


def _render_children(node: RenderTreeNode, context: RenderContext) -> str:
    return "\n\n".join(child.render(context) for child in node.children)


RENDERERS: Mapping[str, Render] = {
    "footnote": _footnote_renderer,
    "footnote_ref": _footnote_ref_renderer,
    "footnote_block": _render_children,
}
