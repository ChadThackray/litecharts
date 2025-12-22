"""Pane class for multi-pane chart layouts."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from .series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    BaseSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)

if TYPE_CHECKING:
    from .types import (
        AreaSeriesOptions,
        BarSeriesOptions,
        BaselineSeriesOptions,
        CandlestickSeriesOptions,
        HistogramSeriesOptions,
        LineSeriesOptions,
        OhlcInput,
        PaneOptions,
        SingleValueInput,
    )


class Pane:
    """A chart pane that can contain multiple series."""

    def __init__(self, options: PaneOptions | None = None) -> None:
        """Initialize the pane.

        Args:
            options: Pane options including height_ratio.
        """
        self._id = f"pane_{uuid.uuid4().hex[:8]}"
        self._options: PaneOptions = options.copy() if options else {}
        self._series: list[BaseSeries[SingleValueInput] | BaseSeries[OhlcInput]] = []

    @property
    def id(self) -> str:
        """Return the pane ID."""
        return self._id

    @property
    def options(self) -> PaneOptions:
        """Return the pane options."""
        return self._options

    @property
    def series(self) -> list[BaseSeries[SingleValueInput] | BaseSeries[OhlcInput]]:
        """Return all series in this pane."""
        return self._series

    @property
    def height_ratio(self) -> float:
        """Return the height ratio for this pane."""
        result = self._options.get("height_ratio", 1.0)
        if isinstance(result, (int, float)):
            return float(result)
        return 1.0

    def add_candlestick_series(
        self, options: CandlestickSeriesOptions | None = None
    ) -> CandlestickSeries:
        """Add a candlestick series to the pane.

        Args:
            options: Candlestick series options.

        Returns:
            The created CandlestickSeries.
        """
        series = CandlestickSeries(options)
        self._series.append(series)
        return series

    def add_line_series(self, options: LineSeriesOptions | None = None) -> LineSeries:
        """Add a line series to the pane.

        Args:
            options: Line series options.

        Returns:
            The created LineSeries.
        """
        series = LineSeries(options)
        self._series.append(series)
        return series

    def add_area_series(self, options: AreaSeriesOptions | None = None) -> AreaSeries:
        """Add an area series to the pane.

        Args:
            options: Area series options.

        Returns:
            The created AreaSeries.
        """
        series = AreaSeries(options)
        self._series.append(series)
        return series

    def add_bar_series(self, options: BarSeriesOptions | None = None) -> BarSeries:
        """Add a bar series to the pane.

        Args:
            options: Bar series options.

        Returns:
            The created BarSeries.
        """
        series = BarSeries(options)
        self._series.append(series)
        return series

    def add_histogram_series(
        self, options: HistogramSeriesOptions | None = None
    ) -> HistogramSeries:
        """Add a histogram series to the pane.

        Args:
            options: Histogram series options.

        Returns:
            The created HistogramSeries.
        """
        series = HistogramSeries(options)
        self._series.append(series)
        return series

    def add_baseline_series(
        self, options: BaselineSeriesOptions | None = None
    ) -> BaselineSeries:
        """Add a baseline series to the pane.

        Args:
            options: Baseline series options.

        Returns:
            The created BaselineSeries.
        """
        series = BaselineSeries(options)
        self._series.append(series)
        return series
