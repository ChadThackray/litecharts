"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

# Type alias matching what the library functions expect
DataMapping = Mapping[str, int | float | str | datetime]

HASHES_FILE = Path(__file__).parent / "expected_hashes.json"
HTML_OUTPUT_DIR = Path(__file__).parent / "html_output"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--update-hashes",
        action="store_true",
        default=False,
        help="Update expected hashes file with current values",
    )


@pytest.fixture
def update_hashes(request: pytest.FixtureRequest) -> bool:
    """Return whether to update hashes."""
    result = request.config.getoption("--update-hashes")
    if isinstance(result, bool):
        return result
    return False


def _load_expected_hashes() -> dict[str, str]:
    """Load expected hashes from file."""
    if HASHES_FILE.exists():
        return dict(json.loads(HASHES_FILE.read_text()))
    return {}


def _save_expected_hashes(hashes: dict[str, str]) -> None:
    """Save expected hashes to file."""
    HASHES_FILE.write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n")


@pytest.fixture
def hash_checker(update_hashes: bool) -> Callable[[str, str], None]:
    """Fixture for checking/updating content hashes.

    Also saves HTML files to tests/html_output/ for manual inspection.

    Usage:
        def test_something(hash_checker):
            html = generate_html()
            hash_checker("test_name", html)
    """
    expected_hashes = _load_expected_hashes()
    updated_hashes = expected_hashes.copy()

    # Ensure output directory exists
    HTML_OUTPUT_DIR.mkdir(exist_ok=True)

    def check_hash(name: str, content: str) -> None:
        actual_hash = hashlib.sha256(content.encode()).hexdigest()[:16]

        # Always save HTML for manual inspection
        html_file = HTML_OUTPUT_DIR / f"{name}.html"
        html_file.write_text(content, encoding="utf-8")

        if update_hashes:
            updated_hashes[name] = actual_hash
            _save_expected_hashes(updated_hashes)
        else:
            expected = expected_hashes.get(name)
            if expected is None:
                pytest.fail(
                    f"No expected hash for '{name}'. "
                    f"Run with --update-hashes to generate."
                )
            assert actual_hash == expected, (
                f"Hash mismatch for '{name}'.\n"
                f"Expected: {expected}\n"
                f"Actual:   {actual_hash}\n"
                f"Run with --update-hashes to update."
            )

    return check_hash


# Sample data fixtures for tests


@pytest.fixture
def sample_ohlc_dicts() -> list[DataMapping]:
    """Sample OHLC data as list of dicts."""
    return [
        {"time": 1609459200, "open": 100.0, "high": 110.0, "low": 95.0, "close": 105.0},
        {
            "time": 1609545600,
            "open": 105.0,
            "high": 115.0,
            "low": 100.0,
            "close": 110.0,
        },
        {
            "time": 1609632000,
            "open": 110.0,
            "high": 120.0,
            "low": 105.0,
            "close": 115.0,
        },
    ]


@pytest.fixture
def sample_single_value_dicts() -> list[DataMapping]:
    """Sample single-value data as list of dicts."""
    return [
        {"time": 1609459200, "value": 100.0},
        {"time": 1609545600, "value": 110.0},
        {"time": 1609632000, "value": 115.0},
    ]
