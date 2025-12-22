"""Marker tooltips plugin for litecharts.

This plugin adds hover tooltips to markers. When a marker has an 'id' and 'tooltip'
field, hovering over it displays custom metadata.

This is a custom enhancement - LWC doesn't have built-in marker tooltips.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pane import Pane


def extractMarkerTooltips(pane: Pane) -> dict[str, dict[str, object]]:
    """Extract tooltip data from markers that have 'id' and 'tooltip' fields.

    Args:
        pane: The pane to extract tooltips from.

    Returns:
        Dict mapping marker IDs to tooltip data.
    """
    tooltips: dict[str, dict[str, object]] = {}
    for series in pane.series:
        for marker in series.markers:
            markerId = marker.get("id")
            tooltip = marker.get("tooltip")
            if markerId and tooltip:
                tooltips[markerId] = dict(tooltip)
    return tooltips


def renderTooltipJs(
    chartVar: str, containerId: str, tooltips: dict[str, dict[str, object]]
) -> str:
    """Generate JS code for tooltip DOM and crosshairMove subscription.

    Args:
        chartVar: The JS variable name of the chart.
        containerId: The HTML container ID for the pane.
        tooltips: Dict mapping marker IDs to tooltip data.

    Returns:
        JavaScript code string.
    """
    tooltipVar = f"tooltip_{chartVar}"
    tooltipsDataVar = f"markerTooltips_{chartVar}"

    tooltipsJson = json.dumps(tooltips)

    return f"""// Marker tooltips
    const {tooltipsDataVar} = {tooltipsJson};
    const {tooltipVar} = document.createElement('div');
    {tooltipVar}.style.cssText = 'position:absolute;display:none;padding:8px 12px;' +
        'background:rgba(0,0,0,0.85);color:white;border-radius:4px;' +
        'font-size:12px;pointer-events:none;z-index:1000;max-width:250px;';
    document.getElementById('{containerId}').style.position = 'relative';
    document.getElementById('{containerId}').appendChild({tooltipVar});
    {chartVar}.subscribeCrosshairMove(function(param) {{
        if (param.hoveredObjectId && {tooltipsDataVar}[param.hoveredObjectId]) {{
            const data = {tooltipsDataVar}[param.hoveredObjectId];
            let html = data.title ? '<strong>' + data.title + '</strong><br>' : '';
            if (data.fields) {{
                for (const [key, val] of Object.entries(data.fields)) {{
                    html += '<span style="color:#aaa">' + key + ':</span> ';
                    html += val + '<br>';
                }}
            }}
            {tooltipVar}.innerHTML = html;
            {tooltipVar}.style.display = 'block';
            if (param.point) {{
                {tooltipVar}.style.left = (param.point.x + 15) + 'px';
                {tooltipVar}.style.top = (param.point.y - 15) + 'px';
            }}
        }} else {{
            {tooltipVar}.style.display = 'none';
        }}
    }});"""
