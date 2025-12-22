"""Series classes for litecharts."""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from .convert import to_lwc_ohlc_data, to_lwc_single_value_data
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

    _series_type: str = "Line"

    def __init__(self, options: BaseSeriesOptions | None = None) -> None:
        """Initialize the series.

        Args:
            options: Series options.
        """
        self._id = f"series_{uuid.uuid4().hex[:8]}"
        self._options: BaseSeriesOptions = options.copy() if options else {}
        self._data: list[OhlcData | SingleValueData] = []
        self._markers: list[Marker] = []
        self._price_lines: list[PriceLineOptions] = []
        self._rectangles: list[RectangleOptions] = []

    @property
    def id(self) -> str:
        """Return the series ID."""
        return self._id

    @property
    def series_type(self) -> str:
        """Return the series type name."""
        return self._series_type

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
    def price_lines(self) -> list[PriceLineOptions]:
        """Return the series price lines."""
        return self._price_lines

    @property
    def rectangles(self) -> list[RectangleOptions]:
        """Return the series rectangles."""
        return self._rectangles

    def add_rectangle(
        self,
        start_time: int,
        end_time: int,
        start_price: float,
        end_price: float,
        color: str = "rgba(0, 255, 0, 0.2)",
    ) -> None:
        """Add a rectangle primitive to the series.

        Rectangles are drawn behind the candles and can be used to highlight
        trade zones, support/resistance areas, or other regions of interest.

        Args:
            start_time: Start time (Unix timestamp).
            end_time: End time (Unix timestamp).
            start_price: Start price (vertical position).
            end_price: End price (vertical position).
            color: Fill color (default: semi-transparent green).

        Example:
            >>> series.add_rectangle(
            ...     start_time=1609459200,
            ...     end_time=1609545600,
            ...     start_price=100.0,
            ...     end_price=110.0,
            ...     color="rgba(0, 255, 0, 0.2)"
            ... )
        """
        from .convert import to_unix_timestamp

        rect: RectangleOptions = {
            "start_time": to_unix_timestamp(start_time),
            "end_time": to_unix_timestamp(end_time),
            "start_price": start_price,
            "end_price": end_price,
            "color": color,
        }
        self._rectangles.append(rect)

    def create_price_line(self, options: PriceLineOptions) -> None:
        """Create a horizontal price line on the series.

        Args:
            options: Price line options (price is required).

        Example:
            >>> series.create_price_line({
            ...     "price": 100.0,
            ...     "color": "#ff0000",
            ...     "line_style": 2,  # Dashed
            ...     "title": "Support"
            ... })
        """
        self._price_lines.append(options)

    def set_data(self, data: DataInputT) -> None:
        """Set the series data.

        Args:
            data: Data as list of dicts, pandas DataFrame/Series, or numpy array.
        """
        self._data = self._convert_data(data)

    @abstractmethod
    def _convert_data(self, data: DataInputT) -> list[OhlcData | SingleValueData]:
        """Convert data to LWC format."""
        ...

    def update(self, bar: OhlcData | SingleValueData) -> None:
        """Update with a single data point.

        Args:
            bar: Single data point dict.
        """
        from .convert import to_unix_timestamp

        normalized: OhlcData | SingleValueData = bar.copy()
        if "time" in normalized:
            normalized["time"] = to_unix_timestamp(normalized["time"])
        self._data.append(normalized)


class CandlestickSeries(BaseSeries[OhlcInput]):
    """Candlestick chart series."""

    _series_type = "Candlestick"

    def __init__(self, options: CandlestickSeriesOptions | None = None) -> None:
        """Initialize the candlestick series.

        Args:
            options: Candlestick series options.
        """
        super().__init__(options)

    def _convert_data(self, data: OhlcInput) -> list[OhlcData | SingleValueData]:
        """Convert data to OHLC format."""
        return to_lwc_ohlc_data(data)


class LineSeries(BaseSeries[SingleValueInput]):
    """Line chart series."""

    _series_type = "Line"

    def __init__(self, options: LineSeriesOptions | None = None) -> None:
        """Initialize the line series.

        Args:
            options: Line series options.
        """
        super().__init__(options)

    def _convert_data(self, data: SingleValueInput) -> list[OhlcData | SingleValueData]:
        """Convert data to single-value format."""
        return to_lwc_single_value_data(data)


class AreaSeries(BaseSeries[SingleValueInput]):
    """Area chart series."""

    _series_type = "Area"

    def __init__(self, options: AreaSeriesOptions | None = None) -> None:
        """Initialize the area series.

        Args:
            options: Area series options.
        """
        super().__init__(options)

    def _convert_data(self, data: SingleValueInput) -> list[OhlcData | SingleValueData]:
        """Convert data to single-value format."""
        return to_lwc_single_value_data(data)


class BarSeries(BaseSeries[OhlcInput]):
    """Bar chart series (OHLC bars)."""

    _series_type = "Bar"

    def __init__(self, options: BarSeriesOptions | None = None) -> None:
        """Initialize the bar series.

        Args:
            options: Bar series options.
        """
        super().__init__(options)

    def _convert_data(self, data: OhlcInput) -> list[OhlcData | SingleValueData]:
        """Convert data to OHLC format."""
        return to_lwc_ohlc_data(data)


class HistogramSeries(BaseSeries[SingleValueInput]):
    """Histogram chart series."""

    _series_type = "Histogram"

    def __init__(self, options: HistogramSeriesOptions | None = None) -> None:
        """Initialize the histogram series.

        Args:
            options: Histogram series options.
        """
        super().__init__(options)

    def _convert_data(self, data: SingleValueInput) -> list[OhlcData | SingleValueData]:
        """Convert data to single-value format."""
        return to_lwc_single_value_data(data)


class BaselineSeries(BaseSeries[SingleValueInput]):
    """Baseline chart series."""

    _series_type = "Baseline"

    def __init__(self, options: BaselineSeriesOptions | None = None) -> None:
        """Initialize the baseline series.

        Args:
            options: Baseline series options.
        """
        super().__init__(options)

    def _convert_data(self, data: SingleValueInput) -> list[OhlcData | SingleValueData]:
        """Convert data to single-value format."""
        return to_lwc_single_value_data(data)


def create_series_markers(
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
        >>> series = chart.add_series(CandlestickSeries)
        >>> series.set_data(ohlc_data)
        >>> create_series_markers(series, [
        ...     {"time": 1609459200, "position": "above_bar", "shape": "arrow_down",
        ...      "color": "#f44336", "text": "Sell"}
        ... ])
    """
    from .convert import to_unix_timestamp

    series._markers = []
    for marker in markers:
        normalized: Marker = marker.copy()
        if "time" in normalized:
            normalized["time"] = to_unix_timestamp(normalized["time"])
        series._markers.append(normalized)
