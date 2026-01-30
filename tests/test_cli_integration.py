"""Integration tests for CLI arguments."""

from pathlib import Path
import subprocess
import tempfile

from fixture_helpers import get_fixture


def test_cli_keep_orphans_flag():
    """Test --keep-footnote-orphans flag from command line."""
    text, expected_keep = get_fixture(
        "cli_integration.md", "CLI keep orphans flag test"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "test.md"
        input_file.write_text(text)

        # Default behavior: remove orphans
        result = subprocess.run(
            ["python", "-m", "mdformat", str(input_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        output_default = input_file.read_text()
        assert "[^orphan]" not in output_default
        assert "[^used]" in output_default

        # With --keep-footnote-orphans: preserve orphans
        input_file.write_text(text)  # Reset file
        result = subprocess.run(
            ["python", "-m", "mdformat", "--keep-footnote-orphans", str(input_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        output_keep = input_file.read_text()
        assert output_keep.strip() == expected_keep.strip()


def test_cli_help_shows_option():
    """Test that --keep-footnote-orphans appears in help."""
    result = subprocess.run(
        ["python", "-m", "mdformat", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--keep-footnote-orphans" in result.stdout
