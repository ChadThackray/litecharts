"""Plugins for litecharts - custom enhancements beyond the thin wrapper."""

from .draw_rectangle import (
    RECTANGLE_PRIMITIVE_JS,
    extract_rectangles,
    render_rectangle_js,
)
from .marker_tooltips import extract_marker_tooltips, render_tooltip_js

__all__ = [
    "RECTANGLE_PRIMITIVE_JS",
    "extract_marker_tooltips",
    "extract_rectangles",
    "render_rectangle_js",
    "render_tooltip_js",
]
