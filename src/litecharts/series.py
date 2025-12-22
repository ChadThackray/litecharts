"""Series classes for litecharts."""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from .convert import toLwcOhlcData, toLwcSingleValueData
from .types import OhlcInput, SingleValueInput

if TYPE_CHECKING:
    from .types import (
        AreaSeriesOptions,
        BarSeriesOptions,
        BaselineSeriesOptions,
        BaseSeriesOptions,
        CandlestickSeriesOptions,
        HistogramSeriesOptions,
        LineSeriesOptions,
        Marker,
        OhlcData,
        PriceLineOptions,
        RectangleOptions,
        SingleValueData,
    )

DataInputT = TypeVar("DataInputT", SingleValueInput, OhlcInput)


class BaseSeries(ABC, Generic[DataInputT]):
    """Base class for all series types."""

    _seriesType: str = "Line"

    def __init__(self, options: BaseSeriesOptions | None = None) -> None:
        """Initialize the series.

        Args:
            options: Series options.
        """
        self._id = f"series_{uuid.uuid4().hex[:8]}"
        self._options: BaseSeriesOptions = options.copy() if options else {}
        self._data: list[OhlcData | SingleValueData] = []
        self._markers: list[Marker] = []
        self._priceLines: list[PriceLineOptions] = []
        self._rectangles: list[RectangleOptions] = []

    @property
    def id(self) -> str:
        """Return the series ID."""
        return self._id

    @property
    def seriesType(self) -> str:
        """Return the series type name."""
        return self._seriesType

    @property
    def options(self) -> BaseSeriesOptions:
        """Return the series options."""
        return self._options

    @property
    def data(self) -> list[OhlcData | SingleValueData]:
        """Return the series data."""
        return self._data

    @property
    def markers(self) -> list[Marker]:
        """Return the series markers."""
        return self._markers

    @property
    def priceLines(self) -> list[PriceLineOptions]:
        """Return the series price lines."""
        return self._priceLines

    @property
    def rectangles(self) -> list[RectangleOptions]:
        """Return the series rectangles."""
        return self._rectangles

    def addRectangle(
        self,
        startTime: int,
        endTime: int,
        startPrice: float,
        endPrice: float,
        color: str = "rgba(0, 255, 0, 0.2)",
    ) -> None:
        """Add a rectangle primitive to the series.

        Rectangles are drawn behind the candles and can be used to highlight
        trade zones, support/resistance areas, or other regions of interest.

        Args:
            startTime: Start time (Unix timestamp).
            endTime: End time (Unix timestamp).
            startPrice: Start price (vertical position).
            endPrice: End price (vertical position).
            color: Fill color (default: semi-transparent green).

        Example:
            >>> series.addRectangle(
            ...     startTime=1609459200,
            ...     endTime=1609545600,
            ...     startPrice=100.0,
            ...     endPrice=110.0,
            ...     color="rgba(0, 255, 0, 0.2)"
            ... )
        """
        from .convert import toUnixTimestamp

        rect: RectangleOptions = {
            "startTime": toUnixTimestamp(startTime),
            "endTime": toUnixTimestamp(endTime),
            "startPrice": startPrice,
            "endPrice": endPrice,
            "color": color,
        }
        self._rectangles.append(rect)

    def createPriceLine(self, options: PriceLineOptions) -> None:
        """Create a horizontal price line on the series.

        Args:
            options: Price line options (price is required).

        Example:
            >>> series.createPriceLine({
            ...     "price": 100.0,
            ...     "color": "#ff0000",
            ...     "lineStyle": 2,  # Dashed
            ...     "title": "Support"
            ... })
        """
        self._priceLines.append(options)

    def setData(self, data: DataInputT) -> None:
        """Set the series data.

        Args:
            data: Data as list of dicts, pandas DataFrame/Series, or numpy array.
        """
        self._data = self._convertData(data)

    @abstractmethod
    def _convertData(self, data: DataInputT) -> list[OhlcData | SingleValueData]:
        """Convert data to LWC format."""
        ...

    def update(self, bar: OhlcData | SingleValueData) -> None:
        """Update with a single data point.

        Args:
            bar: Single data point dict.
        """
        from .convert import toUnixTimestamp

        normalized: OhlcData | SingleValueData = bar.copy()
        if "time" in normalized:
            normalized["time"] = toUnixTimestamp(normalized["time"])
        self._data.append(normalized)


class CandlestickSeries(BaseSeries[OhlcInput]):
    """Candlestick chart series."""

    _seriesType = "Candlestick"

    def __init__(self, options: CandlestickSeriesOptions | None = None) -> None:
        """Initialize the candlestick series.

        Args:
            options: Candlestick series options.
        """
        super().__init__(options)

    def _convertData(self, data: OhlcInput) -> list[OhlcData | SingleValueData]:
        """Convert data to OHLC format."""
        return toLwcOhlcData(data)


class LineSeries(BaseSeries[SingleValueInput]):
    """Line chart series."""

    _seriesType = "Line"

    def __init__(self, options: LineSeriesOptions | None = None) -> None:
        """Initialize the line series.

        Args:
            options: Line series options.
        """
        super().__init__(options)

    def _convertData(self, data: SingleValueInput) -> list[OhlcData | SingleValueData]:
        """Convert data to single-value format."""
        return toLwcSingleValueData(data)


class AreaSeries(BaseSeries[SingleValueInput]):
    """Area chart series."""

    _seriesType = "Area"

    def __init__(self, options: AreaSeriesOptions | None = None) -> None:
        """Initialize the area series.

        Args:
            options: Area series options.
        """
        super().__init__(options)

    def _convertData(self, data: SingleValueInput) -> list[OhlcData | SingleValueData]:
        """Convert data to single-value format."""
        return toLwcSingleValueData(data)


class BarSeries(BaseSeries[OhlcInput]):
    """Bar chart series (OHLC bars)."""

    _seriesType = "Bar"

    def __init__(self, options: BarSeriesOptions | None = None) -> None:
        """Initialize the bar series.

        Args:
            options: Bar series options.
        """
        super().__init__(options)

    def _convertData(self, data: OhlcInput) -> list[OhlcData | SingleValueData]:
        """Convert data to OHLC format."""
        return toLwcOhlcData(data)


class HistogramSeries(BaseSeries[SingleValueInput]):
    """Histogram chart series."""

    _seriesType = "Histogram"

    def __init__(self, options: HistogramSeriesOptions | None = None) -> None:
        """Initialize the histogram series.

        Args:
            options: Histogram series options.
        """
        super().__init__(options)

    def _convertData(self, data: SingleValueInput) -> list[OhlcData | SingleValueData]:
        """Convert data to single-value format."""
        return toLwcSingleValueData(data)


class BaselineSeries(BaseSeries[SingleValueInput]):
    """Baseline chart series."""

    _seriesType = "Baseline"

    def __init__(self, options: BaselineSeriesOptions | None = None) -> None:
        """Initialize the baseline series.

        Args:
            options: Baseline series options.
        """
        super().__init__(options)

    def _convertData(self, data: SingleValueInput) -> list[OhlcData | SingleValueData]:
        """Convert data to single-value format."""
        return toLwcSingleValueData(data)


def createSeriesMarkers(
    series: BaseSeries[SingleValueInput] | BaseSeries[OhlcInput],
    markers: list[Marker],
) -> None:
    """Create markers on a series.

    This mirrors the LWC v5 API pattern where markers are created via
    a separate function rather than a method on the series.

    Args:
        series: The series to add markers to.
        markers: List of marker dicts.

    Example:
        >>> series = chart.addSeries(CandlestickSeries)
        >>> series.setData(ohlcData)
        >>> createSeriesMarkers(series, [
        ...     {"time": 1609459200, "position": "aboveBar", "shape": "arrowDown",
        ...      "color": "#f44336", "text": "Sell"}
        ... ])
    """
    from .convert import toUnixTimestamp

    series._markers = []
    for marker in markers:
        normalized: Marker = marker.copy()
        if "time" in normalized:
            normalized["time"] = toUnixTimestamp(normalized["time"])
        series._markers.append(normalized)
