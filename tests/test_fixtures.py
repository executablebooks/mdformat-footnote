"""All fixture-based tests for mdformat-footnote."""

from pathlib import Path
import re

from fixture_helpers import load_fixtures
import mdformat
import pytest


def _get_options(filename: str, title: str) -> dict:
    """Determine mdformat options based on fixture file and title."""
    if filename == "word_wrap.md":
        if match := re.search(r"wrap at (\d+)", title):
            return {"wrap": int(match.group(1))}
        return {"wrap": 40}
    lowered = title.lower()
    options: dict = {}
    if "keep orphans" in lowered:
        options["keep_orphans"] = True
    if "keep position" in lowered or filename == "keep_position.md":
        options["keep_position"] = True
    return options


# Load all fixture files
TEST_CASES: list[tuple[str, str, str, str, str, dict]] = []
for pth in (Path(__file__).parent / "fixtures").glob("*.md"):
    filename = pth.name
    for line, title, text, expected in load_fixtures(filename):
        options = _get_options(filename, title)
        TEST_CASES.append((filename, line, title, text, expected, options))


@pytest.mark.parametrize(
    "filename,line,title,text,expected,options",
    TEST_CASES,
    ids=[f"{tc[0].replace('.md', '')}::{tc[2]}" for tc in TEST_CASES],
)
def test_fixtures(
    filename: str,
    line: int,
    title: str,
    text: str,
    expected: str,
    options: dict,
):
    output = mdformat.text(text, extensions={"footnote"}, options=options)
    assert output.rstrip() == expected.rstrip(), output
