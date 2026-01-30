"""An mdformat plugin for parsing/validating footnotes"""

__version__ = "0.1.3"
__plugin_name__ = "footnote"

from .plugin import RENDERERS, add_cli_argument_group, update_mdit  # noqa: F401
