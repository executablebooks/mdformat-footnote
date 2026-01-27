from pathlib import Path
import re

from markdown_it.utils import read_fixture_file
import mdformat
import pytest

FIXTURE_PATH = Path(__file__).parent / "fixtures_wrap.md"
fixtures = read_fixture_file(FIXTURE_PATH)


def _extract_wrap_length(title):
    if match := re.search(r"wrap at (\d+)", title):
        return int(match.group(1))
    return 40


@pytest.mark.parametrize(
    "line,title,text,expected",
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_word_wrap(line, title, text, expected):
    wrap_length = _extract_wrap_length(title)
    output = mdformat.text(text, options={"wrap": wrap_length}, extensions={"footnote"})
    assert output.rstrip() == expected.rstrip(), output
