"""HTML rendering for litecharts."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, cast

from ._js import get_lwc_js
from .convert import convert_options_to_js, convert_options_to_js_list

if TYPE_CHECKING:
    from .chart import Chart
    from .pane import Pane
    from .series import BaseSeries


def _render_series_js(series: BaseSeries[Any], chart_var: str) -> str:
    """Generate JS code for a series.

    Args:
        series: The series to render.
        chart_var: The JS variable name of the parent chart.

    Returns:
        JavaScript code string.
    """
    series_var = series.id
    series_type = series.series_type
    options_js = json.dumps(convert_options_to_js(series.options))
    data_js = json.dumps(series.data)

    lines = [
        f"const {series_var} = {chart_var}.add{series_type}Series({options_js});",
        f"{series_var}.setData({data_js});",
    ]

    if series.markers:
        markers_js = json.dumps(convert_options_to_js_list(series.markers))
        lines.append(f"{series_var}.setMarkers({markers_js});")

    return "\n    ".join(lines)


def _calculate_pane_heights(panes: list[Pane], total_height: int) -> list[int]:
    """Calculate pixel heights for each pane based on ratios.

    Args:
        panes: List of panes.
        total_height: Total available height.

    Returns:
        List of pixel heights for each pane.
    """
    total_ratio = sum(p.height_ratio for p in panes)
    heights = []

    remaining = total_height
    for i, pane in enumerate(panes):
        if i == len(panes) - 1:
            # Last pane gets remaining height to avoid rounding issues
            heights.append(remaining)
        else:
            height = int(total_height * pane.height_ratio / total_ratio)
            heights.append(height)
            remaining -= height

    return heights


def _render_time_sync_js(chart_vars: list[str]) -> str:
    """Generate JS code to sync time scales across charts.

    Args:
        chart_vars: List of chart variable names.

    Returns:
        JavaScript code string.
    """
    if len(chart_vars) < 2:
        return ""

    lines = []
    for i, chart_var in enumerate(chart_vars):
        other_vars = [v for j, v in enumerate(chart_vars) if j != i]
        listeners = ", ".join(
            f"{v}.timeScale().setVisibleLogicalRange(range)" for v in other_vars
        )
        lines.append(
            f"{chart_var}.timeScale().subscribeVisibleLogicalRangeChange("
            f"range => {{ if (range) {{ {listeners}; }} }});"
        )

    return "\n    ".join(lines)


def render_chart(chart: Chart) -> str:
    """Render a chart to self-contained HTML.

    Args:
        chart: The chart to render.

    Returns:
        HTML string.
    """
    container_id = f"container_{chart.id}"
    lwc_js = get_lwc_js()

    panes = chart.panes
    if not panes:
        # No panes, no chart to render
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Chart</title>
</head>
<body>
    <div id="{container_id}" style="width: {chart.width}px; height: {chart.height}px;">
        <p>No data to display</p>
    </div>
</body>
</html>"""

    # Calculate heights
    heights = _calculate_pane_heights(panes, chart.height)

    # Build container HTML
    pane_divs = []
    for i, height in enumerate(heights):
        pane_id = f"{container_id}_pane_{i}"
        style = f"width: {chart.width}px; height: {height}px;"
        pane_divs.append(f'<div id="{pane_id}" style="{style}"></div>')
    pane_html = "\n        ".join(pane_divs)

    # Build chart JS
    chart_vars = []
    chart_js_parts = []

    for i, pane in enumerate(panes):
        # Build options for this pane
        pane_options = dict(chart.options)
        pane_options["width"] = chart.width
        pane_options["height"] = heights[i]

        # Hide time scale on all but last pane for cleaner stacking
        if i < len(panes) - 1:
            existing_ts = pane_options.get("time_scale")
            if existing_ts:
                time_scale = {**cast(dict[str, Any], existing_ts), "visible": False}
            else:
                time_scale = {"visible": False}
            pane_options["time_scale"] = time_scale

        chart_var = f"chart_{pane.id}"
        chart_vars.append(chart_var)
        pane_container = f"{container_id}_pane_{i}"

        options_js = json.dumps(convert_options_to_js(pane_options))

        js_lines = [
            f"const {chart_var} = LightweightCharts.createChart(",
            f"      document.getElementById('{pane_container}'),",
            f"      {options_js}",
            "    );",
        ]

        # Add series
        for series in pane.series:
            js_lines.append(_render_series_js(series, chart_var))

        chart_js_parts.append("\n    ".join(js_lines))

    # Time sync
    sync_js = _render_time_sync_js(chart_vars)

    # Combine all JS
    all_chart_js = "\n\n    ".join(chart_js_parts)
    if sync_js:
        all_chart_js += f"\n\n    // Sync time scales\n    {sync_js}"

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Chart</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: #1e1e1e;
        }}
        #{container_id} {{
            display: flex;
            flex-direction: column;
        }}
    </style>
</head>
<body>
    <div id="{container_id}">
        {pane_html}
    </div>
    <script>{lwc_js}</script>
    <script>
    {all_chart_js}
    </script>
</body>
</html>"""
