from typing import Mapping, MutableMapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderTreeNode
from mdformat.renderer.typing import RendererFunc
from mdit_py_plugins.footnote import footnote_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, adding the footnote plugin."""
    mdit.use(footnote_plugin)


def _footnote_ref_renderer(
    node: RenderTreeNode,
    renderer_funcs: Mapping[str, RendererFunc],
    options: Mapping,
    env: MutableMapping,
) -> str:
    return f"[^{node.meta['label']}]"


def _footnote_renderer(
    node: RenderTreeNode,
    renderer_funcs: Mapping[str, RendererFunc],
    options: Mapping,
    env: MutableMapping,
) -> str:
    return f"[^{node.meta['label']}]: " + _render_children(
        node, renderer_funcs, options, env, separator=""
    )


def _render_children(
    node: RenderTreeNode,
    renderer_funcs: Mapping[str, RendererFunc],
    options: Mapping,
    env: MutableMapping,
    *,
    separator: str = "\n\n",
) -> str:
    return separator.join(
        child.render(renderer_funcs, options, env) for child in node.children
    )


RENDERER_FUNCS: Mapping[str, RendererFunc] = {
    "footnote": _footnote_renderer,
    "footnote_ref": _footnote_ref_renderer,
    "footnote_block": _render_children,
}
