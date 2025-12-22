"""HTML rendering for litecharts."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, cast

from ._js import getLwcJs
from .plugins.draw_rectangle import (
    RECTANGLE_PRIMITIVE_JS,
    extractRectangles,
    renderRectangleJs,
)
from .plugins.marker_tooltips import extractMarkerTooltips, renderTooltipJs

if TYPE_CHECKING:
    from .chart import Chart
    from .pane import Pane
    from .series import BaseSeries
    from .types import OhlcInput, SingleValueInput


def _stripTooltipFromMarkers(
    markers: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Strip tooltip field from markers before sending to LWC.

    Args:
        markers: List of marker dicts that may contain tooltip field.

    Returns:
        List of marker dicts without tooltip field.
    """
    return [{k: v for k, v in marker.items() if k != "tooltip"} for marker in markers]


def _renderSeriesJs(
    series: BaseSeries[SingleValueInput] | BaseSeries[OhlcInput], chartVar: str
) -> str:
    """Generate JS code for a series.

    Args:
        series: The series to render.
        chartVar: The JS variable name of the parent chart.

    Returns:
        JavaScript code string.
    """
    seriesVar = series.id
    seriesType = series.seriesType
    optionsJs = json.dumps(series.options)
    dataJs = json.dumps(series.data)

    lines = [
        f"const {seriesVar} = {chartVar}.addSeries("
        f"LightweightCharts.{seriesType}Series, {optionsJs});",
        f"{seriesVar}.setData({dataJs});",
    ]

    if series.markers:
        # Strip tooltip field before sending to LWC (it's handled separately)
        markersForLwc = _stripTooltipFromMarkers(
            cast(list[dict[str, object]], series.markers)
        )
        markersJs = json.dumps(markersForLwc)
        lines.append(
            f"LightweightCharts.createSeriesMarkers({seriesVar}, {markersJs});"
        )

    # Render price lines
    for priceLine in series.priceLines:
        plJs = json.dumps(priceLine)
        lines.append(f"{seriesVar}.createPriceLine({plJs});")

    return "\n    ".join(lines)


def _calculatePaneHeights(panes: list[Pane], totalHeight: int) -> list[int]:
    """Calculate pixel heights for each pane based on ratios.

    Args:
        panes: List of panes.
        totalHeight: Total available height.

    Returns:
        List of pixel heights for each pane.
    """
    totalRatio = sum(p.heightRatio for p in panes)
    heights = []

    remaining = totalHeight
    for i, pane in enumerate(panes):
        if i == len(panes) - 1:
            # Last pane gets remaining height to avoid rounding issues
            heights.append(remaining)
        else:
            height = int(totalHeight * pane.heightRatio / totalRatio)
            heights.append(height)
            remaining -= height

    return heights


def _renderTimeSyncJs(chartVars: list[str]) -> str:
    """Generate JS code to sync time scales across charts.

    Args:
        chartVars: List of chart variable names.

    Returns:
        JavaScript code string.
    """
    if len(chartVars) < 2:
        return ""

    lines = []
    for i, chartVar in enumerate(chartVars):
        otherVars = [v for j, v in enumerate(chartVars) if j != i]
        listeners = ", ".join(
            f"{v}.timeScale().setVisibleLogicalRange(range)" for v in otherVars
        )
        lines.append(
            f"{chartVar}.timeScale().subscribeVisibleLogicalRangeChange("
            f"range => {{ if (range) {{ {listeners}; }} }});"
        )

    return "\n    ".join(lines)


def renderChart(chart: Chart) -> str:
    """Render a chart to self-contained HTML.

    Args:
        chart: The chart to render.

    Returns:
        HTML string.
    """
    containerId = f"container_{chart.id}"
    lwcJs = getLwcJs()

    panes = chart.panes
    if not panes:
        # No panes, no chart to render
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Chart</title>
</head>
<body>
    <div id="{containerId}" style="width: {chart.width}px; height: {chart.height}px;">
        <p>No data to display</p>
    </div>
</body>
</html>"""

    # Calculate heights
    heights = _calculatePaneHeights(panes, chart.height)

    # Build container HTML
    paneDivs = []
    for i, height in enumerate(heights):
        paneId = f"{containerId}_pane_{i}"
        style = f"width: {chart.width}px; height: {height}px;"
        paneDivs.append(f'<div id="{paneId}" style="{style}"></div>')
    paneHtml = "\n        ".join(paneDivs)

    # Build chart JS
    chartVars = []
    chartJsParts = []

    for i, pane in enumerate(panes):
        # Build options for this pane
        paneOptions = dict(chart.options)
        paneOptions["width"] = chart.width
        paneOptions["height"] = heights[i]

        # Hide time scale on all but last pane for cleaner stacking
        if i < len(panes) - 1:
            existingTs = paneOptions.get("timeScale")
            if existingTs:
                timeScale = {**cast(dict[str, object], existingTs), "visible": False}
            else:
                timeScale = {"visible": False}
            paneOptions["timeScale"] = timeScale

        chartVar = f"chart_{pane.id}"
        chartVars.append(chartVar)
        paneContainer = f"{containerId}_pane_{i}"

        optionsJs = json.dumps(paneOptions)

        jsLines = [
            f"const {chartVar} = LightweightCharts.createChart(",
            f"      document.getElementById('{paneContainer}'),",
            f"      {optionsJs}",
            "    );",
        ]

        # Add series
        for series in pane.series:
            jsLines.append(_renderSeriesJs(series, chartVar))

            # Add rectangles if any (plugin)
            rectangles = extractRectangles(series)
            if rectangles:
                jsLines.append(renderRectangleJs(chartVar, series.id, rectangles))

        # Add marker tooltips if any markers have tooltip data (plugin)
        tooltips = extractMarkerTooltips(pane)
        if tooltips:
            jsLines.append(renderTooltipJs(chartVar, paneContainer, tooltips))

        chartJsParts.append("\n    ".join(jsLines))

    # Time sync
    syncJs = _renderTimeSyncJs(chartVars)

    # Check if any series has rectangles (to include primitive class)
    hasRectangles = any(series.rectangles for pane in panes for series in pane.series)
    rectangleScript = (
        f"\n    <script>{RECTANGLE_PRIMITIVE_JS}</script>" if hasRectangles else ""
    )

    # Combine all JS
    allChartJs = "\n\n    ".join(chartJsParts)
    if syncJs:
        allChartJs += f"\n\n    // Sync time scales\n    {syncJs}"

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
        #{containerId} {{
            display: flex;
            flex-direction: column;
        }}
    </style>
</head>
<body>
    <div id="{containerId}">
        {paneHtml}
    </div>
    <script>{lwcJs}</script>{rectangleScript}
    <script>
    {allChartJs}
    </script>
</body>
</html>"""
