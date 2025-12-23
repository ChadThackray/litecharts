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
    series: BaseSeries[SingleValueInput] | BaseSeries[OhlcInput], paneVar: str
) -> str:
    """Generate JS code for a series.

    Args:
        series: The series to render.
        paneVar: The JS variable name of the parent pane.

    Returns:
        JavaScript code string.
    """
    seriesVar = series.id
    seriesType = series.seriesType
    optionsJs = json.dumps(series.options)
    dataJs = json.dumps(series.data)

    lines = [
        f"const {seriesVar} = {paneVar}.addSeries("
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


def _renderContainerHtml(chart: Chart) -> str:
    """Generate container HTML div for the chart.

    Args:
        chart: The chart to render container for.

    Returns:
        HTML string with container div.
    """
    containerId = f"container_{chart.id}"
    style = f"width: {chart.width}px; height: {chart.height}px;"
    return f'<div id="{containerId}" style="{style}"></div>'


def _renderChartInitScript(chart: Chart) -> str:
    """Generate the JavaScript initialization code for the chart.

    Uses native LWC panes for multi-pane support. Single chart instance
    with multiple panes provides automatic time sync and unified crosshair.

    Args:
        chart: The chart to render.

    Returns:
        JavaScript code string (without script tags).
    """
    containerId = f"container_{chart.id}"
    panes = chart.panes
    chartVar = f"chart_{chart.id}"

    # Build chart options
    chartOptions = dict(chart.options)
    chartOptions["width"] = chart.width
    chartOptions["height"] = chart.height
    optionsJs = json.dumps(chartOptions)

    jsLines = [
        f"const {chartVar} = LightweightCharts.createChart(",
        f"    document.getElementById('{containerId}'),",
        f"    {optionsJs}",
        ");",
    ]

    # Process each pane
    for i, pane in enumerate(panes):
        paneVar = f"pane_{pane.id}"

        if i == 0:
            # First pane - get reference to auto-created pane 0
            jsLines.append(f"const {paneVar} = {chartVar}.panes()[0];")
        else:
            # Additional panes - create via addPane()
            jsLines.append(f"const {paneVar} = {chartVar}.addPane();")

        # Set stretch factor for proportional sizing
        jsLines.append(f"{paneVar}.setStretchFactor({pane.stretchFactor});")

        # Add series to this pane
        for series in pane.series:
            jsLines.append(_renderSeriesJs(series, paneVar))

            # Add rectangles if any (plugin)
            rectangles = extractRectangles(series)
            if rectangles:
                jsLines.append(renderRectangleJs(chartVar, series.id, rectangles))

        # Add marker tooltips if any markers have tooltip data (plugin)
        tooltips = extractMarkerTooltips(pane)
        if tooltips:
            jsLines.append(renderTooltipJs(chartVar, containerId, tooltips))

    return "\n    ".join(jsLines)


def renderFragment(chart: Chart) -> str:
    """Render a chart fragment for embedding in custom HTML.

    Returns container div and init script, but NOT:
    - DOCTYPE/html/head/body wrapper
    - LWC library (use getLwcScript() separately)
    - Plugin scripts (use getPluginScripts() separately)

    Args:
        chart: The chart to render.

    Returns:
        HTML fragment string with container and script.
    """
    containerId = f"container_{chart.id}"
    panes = chart.panes

    if not panes:
        style = f"width: {chart.width}px; height: {chart.height}px;"
        return f'''<div id="{containerId}" style="{style}">
    <p>No data to display</p>
</div>'''

    containerHtml = _renderContainerHtml(chart)
    initScript = _renderChartInitScript(chart)

    return f"""{containerHtml}
<script>
{initScript}
</script>"""


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

    # Build container HTML
    containerHtml = _renderContainerHtml(chart)

    # Build chart JS
    allChartJs = _renderChartInitScript(chart)

    # Check if any series has rectangles (to include primitive class)
    hasRectangles = any(series.rectangles for pane in panes for series in pane.series)
    rectangleScript = (
        f"\n    <script>{RECTANGLE_PRIMITIVE_JS}</script>" if hasRectangles else ""
    )

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
    </style>
</head>
<body>
    {containerHtml}
    <script>{lwcJs}</script>{rectangleScript}
    <script>
    {allChartJs}
    </script>
</body>
</html>"""
