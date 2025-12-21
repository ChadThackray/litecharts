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

    def set_markers(self, markers: list[Marker]) -> None:
        """Set markers on the series.

        Args:
            markers: List of marker dicts.
        """
        from .convert import to_unix_timestamp

        self._markers = []
        for marker in markers:
            normalized: Marker = marker.copy()
            if "time" in normalized:
                time_val = normalized["time"]
                normalized["time"] = to_unix_timestamp(time_val)
            self._markers.append(normalized)


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
