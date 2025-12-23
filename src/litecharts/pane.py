"""Pane class for multi-pane chart layouts."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, overload

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
            options: Pane options including stretchFactor.
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
    def stretchFactor(self) -> float:
        """Return the stretch factor for this pane."""
        result = self._options.get("stretchFactor", 1.0)
        if isinstance(result, (int, float)):
            return float(result)
        return 1.0

    @overload
    def addSeries(
        self,
        seriesType: type[CandlestickSeries],
        options: CandlestickSeriesOptions | None = None,
    ) -> CandlestickSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[LineSeries],
        options: LineSeriesOptions | None = None,
    ) -> LineSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[AreaSeries],
        options: AreaSeriesOptions | None = None,
    ) -> AreaSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[BarSeries],
        options: BarSeriesOptions | None = None,
    ) -> BarSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[HistogramSeries],
        options: HistogramSeriesOptions | None = None,
    ) -> HistogramSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[BaselineSeries],
        options: BaselineSeriesOptions | None = None,
    ) -> BaselineSeries: ...

    def addSeries(
        self,
        seriesType: type[
            CandlestickSeries
            | LineSeries
            | AreaSeries
            | BarSeries
            | HistogramSeries
            | BaselineSeries
        ],
        options: CandlestickSeriesOptions
        | LineSeriesOptions
        | AreaSeriesOptions
        | BarSeriesOptions
        | HistogramSeriesOptions
        | BaselineSeriesOptions
        | None = None,
    ) -> BaseSeries[SingleValueInput] | BaseSeries[OhlcInput]:
        """Add a series to the pane.

        Args:
            seriesType: The series class (e.g., CandlestickSeries, LineSeries).
            options: Series options specific to the series type.

        Returns:
            The created series instance.
        """
        series = seriesType(options)  # type: ignore[arg-type]
        self._series.append(series)
        return series
