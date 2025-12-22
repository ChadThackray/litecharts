"""Tests for chart.py module."""

from __future__ import annotations

from litecharts.chart import Chart, create_chart
from litecharts.pane import Pane
from litecharts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)

from .conftest import DataMapping


class TestChart:
    """Tests for Chart class."""

    def test_id_generated(self) -> None:
        """Chart ID is generated."""
        chart = Chart()
        assert chart.id.startswith("chart_")

    def test_default_options(self) -> None:
        """Default options is empty dict."""
        chart = Chart()
        assert chart.options == {}

    def test_custom_options(self) -> None:
        """Custom options are stored."""
        chart = Chart({"width": 1000, "height": 800})
        assert chart.options["width"] == 1000
        assert chart.options["height"] == 800

    def test_default_width(self) -> None:
        """Default width is 800."""
        chart = Chart()
        assert chart.width == 800

    def test_custom_width(self) -> None:
        """Custom width is returned."""
        chart = Chart({"width": 1200})
        assert chart.width == 1200

    def test_default_height(self) -> None:
        """Default height is 600."""
        chart = Chart()
        assert chart.height == 600

    def test_custom_height(self) -> None:
        """Custom height is returned."""
        chart = Chart({"height": 900})
        assert chart.height == 900

    def test_panes_initially_empty(self) -> None:
        """Panes list is initially empty."""
        chart = Chart()
        assert chart.panes == []


class TestChartAddPane:
    """Tests for Chart add_pane method."""

    def test_add_pane(self) -> None:
        """add_pane creates and adds pane."""
        chart = Chart()
        pane = chart.add_pane()
        assert isinstance(pane, Pane)
        assert len(chart.panes) == 1
        assert chart.panes[0] is pane

    def test_add_pane_with_options(self) -> None:
        """add_pane passes options."""
        chart = Chart()
        pane = chart.add_pane({"height_ratio": 0.5})
        assert pane.height_ratio == 0.5

    def test_add_multiple_panes(self) -> None:
        """Multiple panes can be added."""
        chart = Chart()
        chart.add_pane({"height_ratio": 2.0})
        chart.add_pane({"height_ratio": 1.0})
        assert len(chart.panes) == 2


class TestChartAddSeries:
    """Tests for Chart add series methods (via default pane)."""

    def test_add_candlestick_series_creates_default_pane(self) -> None:
        """add_candlestick_series creates default pane if needed."""
        chart = Chart()
        series = chart.add_candlestick_series()
        assert isinstance(series, CandlestickSeries)
        assert len(chart.panes) == 1

    def test_add_candlestick_series_reuses_default_pane(self) -> None:
        """Subsequent series use same default pane."""
        chart = Chart()
        chart.add_candlestick_series()
        chart.add_line_series()
        assert len(chart.panes) == 1
        assert len(chart.panes[0].series) == 2

    def test_add_line_series(self) -> None:
        """add_line_series creates LineSeries."""
        chart = Chart()
        series = chart.add_line_series()
        assert isinstance(series, LineSeries)

    def test_add_area_series(self) -> None:
        """add_area_series creates AreaSeries."""
        chart = Chart()
        series = chart.add_area_series()
        assert isinstance(series, AreaSeries)

    def test_add_bar_series(self) -> None:
        """add_bar_series creates BarSeries."""
        chart = Chart()
        series = chart.add_bar_series()
        assert isinstance(series, BarSeries)

    def test_add_histogram_series(self) -> None:
        """add_histogram_series creates HistogramSeries."""
        chart = Chart()
        series = chart.add_histogram_series()
        assert isinstance(series, HistogramSeries)

    def test_add_baseline_series(self) -> None:
        """add_baseline_series creates BaselineSeries."""
        chart = Chart()
        series = chart.add_baseline_series()
        assert isinstance(series, BaselineSeries)


class TestChartToHtml:
    """Tests for Chart to_html method."""

    def test_to_html_empty_chart(self) -> None:
        """Empty chart produces valid HTML with no data message."""
        chart = Chart()
        html = chart.to_html()
        assert "<!DOCTYPE html>" in html
        assert "No data to display" in html

    def test_to_html_with_series(self, sample_ohlc_dicts: list[DataMapping]) -> None:
        """Chart with data produces HTML with script tags."""
        chart = Chart()
        series = chart.add_candlestick_series()
        series.set_data(sample_ohlc_dicts)
        html = chart.to_html()
        assert "<!DOCTYPE html>" in html
        assert "<script>" in html
        assert "LightweightCharts.createChart" in html


class TestCreateChart:
    """Tests for create_chart factory function."""

    def test_create_chart_returns_chart(self) -> None:
        """create_chart returns Chart instance."""
        chart = create_chart()
        assert isinstance(chart, Chart)

    def test_create_chart_with_options(self) -> None:
        """create_chart passes options."""
        chart = create_chart({"width": 1000})
        assert chart.width == 1000
