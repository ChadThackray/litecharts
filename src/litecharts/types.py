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
    minMove: float


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

    backgroundColor: str
    textColor: str
    fontSize: int
    fontFamily: str


class GridLineOptions(TypedDict, total=False):
    """Options for grid lines."""

    color: str
    style: int
    visible: bool


class GridOptions(TypedDict, total=False):
    """Grid options for the chart."""

    vertLines: GridLineOptions
    horzLines: GridLineOptions


class CrosshairLineOptions(TypedDict, total=False):
    """Options for crosshair lines."""

    color: str
    width: int
    style: int
    visible: bool
    labelVisible: bool
    labelBackgroundColor: str


class CrosshairOptions(TypedDict, total=False):
    """Crosshair options."""

    mode: int
    vertLine: CrosshairLineOptions
    horzLine: CrosshairLineOptions


class TimeScaleOptions(TypedDict, total=False):
    """Time scale options."""

    rightOffset: int
    barSpacing: int
    minBarSpacing: float
    fixLeftEdge: bool
    fixRightEdge: bool
    lockVisibleTimeRangeOnResize: bool
    rightBarStaysOnScroll: bool
    borderVisible: bool
    borderColor: str
    visible: bool
    timeVisible: bool
    secondsVisible: bool
    shiftVisibleRangeOnNewBar: bool
    allowShiftVisibleRangeOnWhitespaceReplacement: bool
    ticksVisible: bool
    uniformDistribution: bool
    minimumHeight: int
    allowBoldLabels: bool


class PriceScaleOptions(TypedDict, total=False):
    """Price scale options."""

    autoScale: bool
    mode: int
    invertScale: bool
    alignLabels: bool
    scaleMargins: PriceScaleMargins
    borderVisible: bool
    borderColor: str
    textColor: str
    entireTextOnly: bool
    visible: bool
    ticksVisible: bool
    minimumWidth: int


class HandleScrollOptions(TypedDict, total=False):
    """Handle scroll options."""

    mouseWheel: bool
    pressedMouseMove: bool
    horzTouchDrag: bool
    vertTouchDrag: bool


class HandleScaleOptions(TypedDict, total=False):
    """Handle scale options."""

    axisPressedMouseMove: bool | AxisPressedMouseMoveOptions
    axisDoubleClickReset: bool | AxisDoubleClickOptions
    mouseWheel: bool
    pinch: bool


class KineticScrollOptions(TypedDict, total=False):
    """Kinetic scroll options."""

    touch: bool
    mouse: bool


class LocalizationOptions(TypedDict, total=False):
    """Localization options."""

    locale: str
    dateFormat: str


class WatermarkOptions(TypedDict, total=False):
    """Watermark options."""

    visible: bool
    color: str
    text: str
    fontSize: int
    fontFamily: str
    fontStyle: str
    horzAlign: Literal["left", "center", "right"]
    vertAlign: Literal["top", "center", "bottom"]


class ChartOptions(TypedDict, total=False):
    """Options for creating a chart."""

    width: int
    height: int
    autoSize: bool
    layout: LayoutOptions
    grid: GridOptions
    crosshair: CrosshairOptions
    timeScale: TimeScaleOptions
    rightPriceScale: PriceScaleOptions
    leftPriceScale: PriceScaleOptions
    overlayPriceScales: dict[str, PriceScaleOptions]
    handleScroll: HandleScrollOptions | bool
    handleScale: HandleScaleOptions | bool
    kineticScroll: KineticScrollOptions
    localization: LocalizationOptions
    watermark: WatermarkOptions


class PriceLineOptions(TypedDict, total=False):
    """Options for price lines."""

    id: str
    price: float
    color: str
    lineWidth: int
    lineStyle: int
    lineVisible: bool
    axisLabelVisible: bool
    title: str
    axisLabelColor: str
    axisLabelTextColor: str


class LastPriceAnimationOptions(TypedDict, total=False):
    """Options for last price animation."""

    mode: int


class BaseSeriesOptions(TypedDict, total=False):
    """Base options shared by all series types."""

    title: str
    visible: bool
    priceLineVisible: bool
    lastValueVisible: bool
    priceLineWidth: int
    priceLineColor: str
    priceLineStyle: int
    baseLineVisible: bool
    baseLineColor: str
    baseLineWidth: int
    baseLineStyle: int
    priceFormat: PriceFormat
    priceScaleId: str
    autoScaleMargins: AutoScaleMargins


class CandlestickSeriesOptions(BaseSeriesOptions, total=False):
    """Options for candlestick series."""

    upColor: str
    downColor: str
    wickVisible: bool
    borderVisible: bool
    borderColor: str
    borderUpColor: str
    borderDownColor: str
    wickColor: str
    wickUpColor: str
    wickDownColor: str


class LineSeriesOptions(BaseSeriesOptions, total=False):
    """Options for line series."""

    color: str
    lineWidth: int
    lineStyle: int
    lineType: int
    lineVisible: bool
    pointMarkersVisible: bool
    pointMarkersRadius: float
    crosshairMarkerVisible: bool
    crosshairMarkerRadius: float
    crosshairMarkerBorderColor: str
    crosshairMarkerBackgroundColor: str
    crosshairMarkerBorderWidth: float
    lastPriceAnimation: int


class AreaSeriesOptions(BaseSeriesOptions, total=False):
    """Options for area series."""

    topColor: str
    bottomColor: str
    invertFilledArea: bool
    lineColor: str
    lineStyle: int
    lineWidth: int
    lineType: int
    lineVisible: bool
    pointMarkersVisible: bool
    pointMarkersRadius: float
    crosshairMarkerVisible: bool
    crosshairMarkerRadius: float
    crosshairMarkerBorderColor: str
    crosshairMarkerBackgroundColor: str
    crosshairMarkerBorderWidth: float
    lastPriceAnimation: int


class BarSeriesOptions(BaseSeriesOptions, total=False):
    """Options for bar series."""

    upColor: str
    downColor: str
    openVisible: bool
    thinBars: bool


class HistogramSeriesOptions(BaseSeriesOptions, total=False):
    """Options for histogram series."""

    color: str
    base: float


class BaselineSeriesOptions(BaseSeriesOptions, total=False):
    """Options for baseline series."""

    baseValue: BaseValuePrice
    topFillColor1: str
    topFillColor2: str
    topLineColor: str
    topLineStyle: int
    topLineWidth: int
    bottomFillColor1: str
    bottomFillColor2: str
    bottomLineColor: str
    bottomLineStyle: int
    bottomLineWidth: int
    lineType: int
    lineVisible: bool
    pointMarkersVisible: bool
    pointMarkersRadius: float
    crosshairMarkerVisible: bool
    crosshairMarkerRadius: float
    crosshairMarkerBorderColor: str
    crosshairMarkerBackgroundColor: str
    crosshairMarkerBorderWidth: float
    lastPriceAnimation: int


class PaneOptions(TypedDict, total=False):
    """Options for chart panes."""

    stretchFactor: float


class MarkerTooltip(TypedDict, total=False):
    """Tooltip content for a marker.

    Displayed when hovering over a marker that has an 'id' field.
    """

    title: str
    fields: dict[str, str]


class Marker(TypedDict, total=False):
    """Marker to display on a series."""

    time: int
    position: Literal["aboveBar", "belowBar", "inBar"]
    shape: Literal["circle", "square", "arrowUp", "arrowDown"]
    color: str
    text: str
    size: int
    id: str
    tooltip: MarkerTooltip


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


class RectangleOptions(TypedDict, total=False):
    """Options for drawing a rectangle primitive on a series.

    Used for highlighting trade zones, support/resistance areas, etc.
    """

    startTime: int
    endTime: int
    startPrice: float
    endPrice: float
    color: str
