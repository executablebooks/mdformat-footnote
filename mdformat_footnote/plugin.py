from typing import List, Optional, Tuple

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MARKERS, MDRenderer
from mdit_py_plugins.footnote import footnote_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    mdit.use(footnote_plugin)


def render_token(
    renderer: MDRenderer,
    tokens: List[Token],
    index: int,
    options: dict,
    env: dict,
) -> Optional[Tuple[str, int]]:
    """Convert token(s) to a string, or return None if no render method available.

    :returns: (text, index) where index is of the final "consumed" token
    """
    token = tokens[index]
    if token.type == "footnote_anchor":
        # skip as this is just the jump-back
        return None
    elif token.type == "footnote_ref":
        content = f"[^{token.meta['label']}]" + token.content
        print(token)
    elif token.type == "footnote_block_open":
        # skip as we're not doing anything special
        # maybe check for empty line before later
        return None
    elif token.type == "footnote_block_close":
        content = MARKERS.BLOCK_SEPARATOR
        return None
    elif token.type == "footnote_open":
        print(token)
        index += 1
        inner_tokens = []
        while index < len(tokens) and tokens[index].type != "footnote_close":
            inner_tokens.append(tokens[index])
            index += 1
        content = f"[^{token.meta['label']}]: " + renderer.render(
            inner_tokens, options, env, finalize=False
        )
        token = tokens[index]
        print(token)
    elif token.type == "footnote_close":
        # make sure we have a line at the end
        return None
    else:
        return None
    #        mdformat.renderer.LOGGER.warning("Invalid YAML in a front matter block")

    return content, index
