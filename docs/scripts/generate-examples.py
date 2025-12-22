#!/usr/bin/env python3
"""Generate example HTML files for documentation.

This script imports and executes the example files from the examples/ directory,
capturing their chart output as HTML files.
"""

import importlib.util
import sys
from pathlib import Path

# Add the src directory to the path so we can import litecharts
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

EXAMPLES_DIR = Path(__file__).parent / "examples"
OUTPUT_DIR = Path(__file__).parent.parent / "public" / "examples"


def load_and_run_example(example_path: Path) -> str:
    """Load an example file and return its chart HTML.

    Args:
        example_path: Path to the example Python file.

    Returns:
        HTML string from the chart.
    """
    # Load the module
    spec = importlib.util.spec_from_file_location(example_path.stem, example_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {example_path}")

    module = importlib.util.module_from_spec(spec)

    # Patch chart.show() to capture the chart instead of displaying it
    captured_chart = None

    def capture_show(self: object) -> None:
        nonlocal captured_chart
        captured_chart = self

    # Import litecharts and patch the show method
    from litecharts.chart import Chart

    original_show = Chart.show
    Chart.show = capture_show

    try:
        spec.loader.exec_module(module)
    finally:
        Chart.show = original_show

    if captured_chart is None:
        raise RuntimeError(f"No chart was created in {example_path}")

    return captured_chart.toHtml()  # type: ignore[union-attr]


def main() -> None:
    """Generate all example HTML files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find all example files
    example_files = sorted(EXAMPLES_DIR.glob("*.py"))

    for example_path in example_files:
        html = load_and_run_example(example_path)
        output_path = OUTPUT_DIR / f"{example_path.stem}.html"
        output_path.write_text(html)
        print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
