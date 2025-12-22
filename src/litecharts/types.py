"""TypedDict definitions mirroring LWC options structures."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, TypeAlias, TypedDict

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd

# Type alias for values in data point dictionaries (time, OHLC values, etc.)
DataValue: TypeAlias = int | float | str | datetime

# Input type aliases for series data
SingleValueInput: TypeAlias = (
    "pd.DataFrame"
    " | pd.Series[float]"
    " | np.ndarray[Any, Any]"
    " | list[Mapping[str, DataValue]]"
)
OhlcInput: TypeAlias = (
    "pd.DataFrame | np.ndarray[Any, Any] | list[Mapping[str, DataValue]]"
)


class PriceScaleMargins(TypedDict, total=False):
    """Margins for the price scale."""

    top: float
    bottom: float


class AxisPressedMouseMoveOptions(TypedDict, total=False):
    """Options for axis scaling via mouse drag."""

    time: bool
    price: bool


class AxisDoubleClickOptions(TypedDict, total=False):
    """Options for axis reset via double-click."""

    time: bool
    price: bool


class PriceFormat(TypedDict, total=False):
    """Price format options."""

    type: Literal["price", "volume", "percent", "custom"]
    precision: int
    min_move: float


class AutoScaleMargins(TypedDict, total=False):
    """Auto-scale margins in pixels."""

    above: float
    below: float


class BaseValuePrice(TypedDict, total=False):
    """Base value for baseline series."""

    type: Literal["price"]
    price: float


class LayoutOptions(TypedDict, total=False):
    """Layout options for the chart."""

    background_color: str
    text_color: str
    font_size: int
    font_family: str


class GridLineOptions(TypedDict, total=False):
    """Options for grid lines."""

    color: str
    style: int
    visible: bool


class GridOptions(TypedDict, total=False):
    """Grid options for the chart."""

    vert_lines: GridLineOptions
    horz_lines: GridLineOptions


class CrosshairLineOptions(TypedDict, total=False):
    """Options for crosshair lines."""

    color: str
    width: int
    style: int
    visible: bool
    label_visible: bool
    label_background_color: str


class CrosshairOptions(TypedDict, total=False):
    """Crosshair options."""

    mode: int
    vert_line: CrosshairLineOptions
    horz_line: CrosshairLineOptions


class TimeScaleOptions(TypedDict, total=False):
    """Time scale options."""

    right_offset: int
    bar_spacing: int
    min_bar_spacing: float
    fix_left_edge: bool
    fix_right_edge: bool
    lock_visible_time_range_on_resize: bool
    right_bar_stays_on_scroll: bool
    border_visible: bool
    border_color: str
    visible: bool
    time_visible: bool
    seconds_visible: bool
    shift_visible_range_on_new_bar: bool
    allow_shift_visible_range_on_whitespace_replacement: bool
    ticks_visible: bool
    uniform_distribution: bool
    minimum_height: int
    allow_bold_labels: bool


class PriceScaleOptions(TypedDict, total=False):
    """Price scale options."""

    auto_scale: bool
    mode: int
    invert_scale: bool
    align_labels: bool
    scale_margins: PriceScaleMargins
    border_visible: bool
    border_color: str
    text_color: str
    entire_text_only: bool
    visible: bool
    ticks_visible: bool
    minimum_width: int


class HandleScrollOptions(TypedDict, total=False):
    """Handle scroll options."""

    mouse_wheel: bool
    pressed_mouse_move: bool
    horz_touch_drag: bool
    vert_touch_drag: bool


class HandleScaleOptions(TypedDict, total=False):
    """Handle scale options."""

    axis_pressed_mouse_move: bool | AxisPressedMouseMoveOptions
    axis_double_click_reset: bool | AxisDoubleClickOptions
    mouse_wheel: bool
    pinch: bool


class KineticScrollOptions(TypedDict, total=False):
    """Kinetic scroll options."""

    touch: bool
    mouse: bool


class LocalizationOptions(TypedDict, total=False):
    """Localization options."""

    locale: str
    date_format: str


class WatermarkOptions(TypedDict, total=False):
    """Watermark options."""

    visible: bool
    color: str
    text: str
    font_size: int
    font_family: str
    font_style: str
    horz_align: Literal["left", "center", "right"]
    vert_align: Literal["top", "center", "bottom"]


class ChartOptions(TypedDict, total=False):
    """Options for creating a chart."""

    width: int
    height: int
    auto_size: bool
    layout: LayoutOptions
    grid: GridOptions
    crosshair: CrosshairOptions
    time_scale: TimeScaleOptions
    right_price_scale: PriceScaleOptions
    left_price_scale: PriceScaleOptions
    overlay_price_scales: dict[str, PriceScaleOptions]
    handle_scroll: HandleScrollOptions | bool
    handle_scale: HandleScaleOptions | bool
    kinetic_scroll: KineticScrollOptions
    localization: LocalizationOptions
    watermark: WatermarkOptions


class PriceLineOptions(TypedDict, total=False):
    """Options for price lines."""

    price: float
    color: str
    line_width: int
    line_style: int
    line_visible: bool
    axis_label_visible: bool
    title: str
    axis_label_color: str
    axis_label_text_color: str


class LastPriceAnimationOptions(TypedDict, total=False):
    """Options for last price animation."""

    mode: int


class BaseSeriesOptions(TypedDict, total=False):
    """Base options shared by all series types."""

    title: str
    visible: bool
    price_line_visible: bool
    last_value_visible: bool
    price_line_width: int
    price_line_color: str
    price_line_style: int
    base_line_visible: bool
    base_line_color: str
    base_line_width: int
    base_line_style: int
    price_format: PriceFormat
    price_scale_id: str
    auto_scale_margins: AutoScaleMargins


class CandlestickSeriesOptions(BaseSeriesOptions, total=False):
    """Options for candlestick series."""

    up_color: str
    down_color: str
    wick_visible: bool
    border_visible: bool
    border_color: str
    border_up_color: str
    border_down_color: str
    wick_color: str
    wick_up_color: str
    wick_down_color: str


class LineSeriesOptions(BaseSeriesOptions, total=False):
    """Options for line series."""

    color: str
    line_width: int
    line_style: int
    line_type: int
    line_visible: bool
    point_markers_visible: bool
    point_markers_radius: float
    crosshair_marker_visible: bool
    crosshair_marker_radius: float
    crosshair_marker_border_color: str
    crosshair_marker_background_color: str
    crosshair_marker_border_width: float
    last_price_animation: int


class AreaSeriesOptions(BaseSeriesOptions, total=False):
    """Options for area series."""

    top_color: str
    bottom_color: str
    invert_filled_area: bool
    line_color: str
    line_style: int
    line_width: int
    line_type: int
    line_visible: bool
    point_markers_visible: bool
    point_markers_radius: float
    crosshair_marker_visible: bool
    crosshair_marker_radius: float
    crosshair_marker_border_color: str
    crosshair_marker_background_color: str
    crosshair_marker_border_width: float
    last_price_animation: int


class BarSeriesOptions(BaseSeriesOptions, total=False):
    """Options for bar series."""

    up_color: str
    down_color: str
    open_visible: bool
    thin_bars: bool


class HistogramSeriesOptions(BaseSeriesOptions, total=False):
    """Options for histogram series."""

    color: str
    base: float


class BaselineSeriesOptions(BaseSeriesOptions, total=False):
    """Options for baseline series."""

    base_value: BaseValuePrice
    top_fill_color1: str
    top_fill_color2: str
    top_line_color: str
    top_line_style: int
    top_line_width: int
    bottom_fill_color1: str
    bottom_fill_color2: str
    bottom_line_color: str
    bottom_line_style: int
    bottom_line_width: int
    line_type: int
    line_visible: bool
    point_markers_visible: bool
    point_markers_radius: float
    crosshair_marker_visible: bool
    crosshair_marker_radius: float
    crosshair_marker_border_color: str
    crosshair_marker_background_color: str
    crosshair_marker_border_width: float
    last_price_animation: int


class PaneOptions(TypedDict, total=False):
    """Options for chart panes."""

    height_ratio: float


class Marker(TypedDict, total=False):
    """Marker to display on a series."""

    time: int
    position: Literal["above_bar", "below_bar", "in_bar"]
    shape: Literal["circle", "square", "arrow_up", "arrow_down"]
    color: str
    text: str
    size: int
    id: str


class OhlcData(TypedDict, total=False):
    """OHLC data point."""

    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class SingleValueData(TypedDict, total=False):
    """Single value data point (for line, histogram, etc.)."""

    time: int
    value: float
    color: str
