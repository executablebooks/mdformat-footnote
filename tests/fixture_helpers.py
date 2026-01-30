"""Helper utilities for loading test fixtures."""

from pathlib import Path

from markdown_it.utils import read_fixture_file


def load_fixtures(filename: str) -> list[tuple[int, str, str, str]]:
    """Load fixtures from a file in tests/fixtures/ directory."""
    fixture_path = Path(__file__).parent / "fixtures" / filename
    return read_fixture_file(fixture_path)


def get_fixture(filename: str, title: str) -> tuple[str, str]:
    """Get a specific fixture by title from a file."""
    fixtures = load_fixtures(filename)
    for _, fixture_title, input_text, expected_output in fixtures:
        if fixture_title == title:
            return input_text, expected_output
    available = [f[1] for f in fixtures]
    raise ValueError(
        f"Fixture '{title}' not found in {filename}. Available: {available}"
    )
