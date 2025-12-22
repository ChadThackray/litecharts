"""Plugins for litecharts - custom enhancements beyond the thin wrapper."""

from .draw_rectangle import (
    RECTANGLE_PRIMITIVE_JS,
    extractRectangles,
    renderRectangleJs,
)
from .marker_tooltips import extractMarkerTooltips, renderTooltipJs

__all__ = [
    "RECTANGLE_PRIMITIVE_JS",
    "extractMarkerTooltips",
    "extractRectangles",
    "renderRectangleJs",
    "renderTooltipJs",
]
