"""Tests for pane.py module."""

from __future__ import annotations

from litecharts.pane import Pane
from litecharts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)


class TestPane:
    """Tests for Pane class."""

    def test_id_generated(self) -> None:
        """Pane ID is generated."""
        pane = Pane()
        assert pane.id.startswith("pane_")

    def test_default_options(self) -> None:
        """Default options is empty dict."""
        pane = Pane()
        assert pane.options == {}

    def test_custom_options(self) -> None:
        """Custom options are stored."""
        pane = Pane({"stretchFactor": 2.0})
        assert pane.options["stretchFactor"] == 2.0

    def test_default_stretch_factor(self) -> None:
        """Default stretch factor is 1.0."""
        pane = Pane()
        assert pane.stretchFactor == 1.0

    def test_custom_stretch_factor(self) -> None:
        """Custom stretch factor is returned."""
        pane = Pane({"stretchFactor": 0.5})
        assert pane.stretchFactor == 0.5

    def test_series_initially_empty(self) -> None:
        """Series list is initially empty."""
        pane = Pane()
        assert pane.series == []


class TestPaneAddSeries:
    """Tests for Pane addSeries method."""

    def test_add_candlestick_series(self) -> None:
        """addSeries creates and adds CandlestickSeries."""
        pane = Pane()
        series = pane.addSeries(CandlestickSeries)
        assert isinstance(series, CandlestickSeries)
        assert len(pane.series) == 1
        assert pane.series[0] is series

    def test_add_candlestick_series_with_options(self) -> None:
        """addSeries passes options to CandlestickSeries."""
        pane = Pane()
        series = pane.addSeries(CandlestickSeries, {"upColor": "#00ff00"})
        assert series.options.get("upColor") == "#00ff00"

    def test_add_line_series(self) -> None:
        """addSeries creates and adds LineSeries."""
        pane = Pane()
        series = pane.addSeries(LineSeries)
        assert isinstance(series, LineSeries)
        assert len(pane.series) == 1

    def test_add_area_series(self) -> None:
        """addSeries creates and adds AreaSeries."""
        pane = Pane()
        series = pane.addSeries(AreaSeries)
        assert isinstance(series, AreaSeries)
        assert len(pane.series) == 1

    def test_add_bar_series(self) -> None:
        """addSeries creates and adds BarSeries."""
        pane = Pane()
        series = pane.addSeries(BarSeries)
        assert isinstance(series, BarSeries)
        assert len(pane.series) == 1

    def test_add_histogram_series(self) -> None:
        """addSeries creates and adds HistogramSeries."""
        pane = Pane()
        series = pane.addSeries(HistogramSeries)
        assert isinstance(series, HistogramSeries)
        assert len(pane.series) == 1

    def test_add_baseline_series(self) -> None:
        """addSeries creates and adds BaselineSeries."""
        pane = Pane()
        series = pane.addSeries(BaselineSeries)
        assert isinstance(series, BaselineSeries)
        assert len(pane.series) == 1

    def test_add_multiple_series(self) -> None:
        """Multiple series can be added to a pane."""
        pane = Pane()
        pane.addSeries(CandlestickSeries)
        pane.addSeries(LineSeries)
        pane.addSeries(HistogramSeries)
        assert len(pane.series) == 3
