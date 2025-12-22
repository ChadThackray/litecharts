"""Integration tests and hash-based regression tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litecharts import Chart, create_chart

from .conftest import DataMapping

if TYPE_CHECKING:
    from collections.abc import Callable


class TestEndToEndChartCreation:
    """End-to-end tests for chart creation flows."""

    def test_simple_candlestick_chart(
        self, sample_ohlc_dicts: list[DataMapping]
    ) -> None:
        """Create a simple candlestick chart."""
        chart = create_chart({"width": 800, "height": 600})
        series = chart.add_candlestick_series({"up_color": "#26a69a"})
        series.set_data(sample_ohlc_dicts)

        assert len(chart.panes) == 1
        assert len(chart.panes[0].series) == 1
        assert chart.panes[0].series[0].series_type == "Candlestick"
        assert len(chart.panes[0].series[0].data) == 3

    def test_multi_series_chart(
        self,
        sample_ohlc_dicts: list[DataMapping],
        sample_single_value_dicts: list[DataMapping],
    ) -> None:
        """Create chart with multiple series in same pane."""
        chart = create_chart()
        candle = chart.add_candlestick_series()
        candle.set_data(sample_ohlc_dicts)
        line = chart.add_line_series({"color": "#ff0000"})
        line.set_data(sample_single_value_dicts)

        assert len(chart.panes) == 1
        assert len(chart.panes[0].series) == 2

    def test_multi_pane_chart(
        self,
        sample_ohlc_dicts: list[DataMapping],
        sample_single_value_dicts: list[DataMapping],
    ) -> None:
        """Create chart with multiple panes."""
        chart = create_chart({"width": 800, "height": 800})

        # Main price pane
        price_pane = chart.add_pane({"height_ratio": 3.0})
        candle = price_pane.add_candlestick_series()
        candle.set_data(sample_ohlc_dicts)

        # Volume pane
        volume_pane = chart.add_pane({"height_ratio": 1.0})
        histogram = volume_pane.add_histogram_series({"color": "#26a69a"})
        histogram.set_data(sample_single_value_dicts)

        assert len(chart.panes) == 2
        assert chart.panes[0].height_ratio == 3.0
        assert chart.panes[1].height_ratio == 1.0

    def test_chart_with_markers(self, sample_ohlc_dicts: list[DataMapping]) -> None:
        """Create chart with markers on series."""
        chart = create_chart()
        series = chart.add_candlestick_series()
        series.set_data(sample_ohlc_dicts)
        series.set_markers(
            [
                {
                    "time": 1609459200,
                    "position": "above_bar",
                    "shape": "arrow_down",
                    "color": "#f44336",
                }
            ]
        )

        assert len(series.markers) == 1
        assert series.markers[0]["position"] == "above_bar"


class TestHtmlOutputRegression:
    """Hash-based regression tests for HTML output."""

    def test_empty_chart_html(self, hash_checker: Callable[[str, str], None]) -> None:
        """Empty chart HTML output is stable."""
        chart = Chart()
        # Override ID for deterministic output
        chart._id = "chart_test0001"
        html = chart.to_html()
        hash_checker("empty_chart", html)

    def test_simple_candlestick_html(
        self,
        sample_ohlc_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Simple candlestick chart HTML output is stable."""
        chart = Chart({"width": 800, "height": 600})
        chart._id = "chart_test0002"
        pane = chart.add_pane()
        pane._id = "pane_test0001"
        series = pane.add_candlestick_series(
            {"up_color": "#26a69a", "down_color": "#ef5350"}
        )
        series._id = "series_test0001"
        series.set_data(sample_ohlc_dicts)

        html = chart.to_html()
        hash_checker("simple_candlestick", html)

    def test_multi_pane_html(
        self,
        sample_ohlc_dicts: list[DataMapping],
        sample_single_value_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Multi-pane chart HTML output is stable."""
        chart = Chart({"width": 800, "height": 800})
        chart._id = "chart_test0003"

        price_pane = chart.add_pane({"height_ratio": 3.0})
        price_pane._id = "pane_test0002"
        candle = price_pane.add_candlestick_series()
        candle._id = "series_test0002"
        candle.set_data(sample_ohlc_dicts)

        volume_pane = chart.add_pane({"height_ratio": 1.0})
        volume_pane._id = "pane_test0003"
        histogram = volume_pane.add_histogram_series({"color": "#26a69a"})
        histogram._id = "series_test0003"
        histogram.set_data(sample_single_value_dicts)

        html = chart.to_html()
        hash_checker("multi_pane", html)

    def test_line_series_html(
        self,
        sample_single_value_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Line series chart HTML output is stable."""
        chart = Chart({"width": 600, "height": 400})
        chart._id = "chart_test0004"
        pane = chart.add_pane()
        pane._id = "pane_test0004"
        series = pane.add_line_series({"color": "#2196f3", "line_width": 2})
        series._id = "series_test0004"
        series.set_data(sample_single_value_dicts)

        html = chart.to_html()
        hash_checker("line_series", html)

    def test_area_series_html(
        self,
        sample_single_value_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Area series chart HTML output is stable."""
        chart = Chart()
        chart._id = "chart_test0005"
        pane = chart.add_pane()
        pane._id = "pane_test0005"
        series = pane.add_area_series(
            {
                "line_color": "#2196f3",
                "top_color": "rgba(33, 150, 243, 0.4)",
                "bottom_color": "rgba(33, 150, 243, 0.0)",
            }
        )
        series._id = "series_test0005"
        series.set_data(sample_single_value_dicts)

        html = chart.to_html()
        hash_checker("area_series", html)

    def test_chart_with_markers_html(
        self,
        sample_ohlc_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Chart with markers HTML output is stable."""
        chart = Chart()
        chart._id = "chart_test0006"
        pane = chart.add_pane()
        pane._id = "pane_test0006"
        series = pane.add_candlestick_series()
        series._id = "series_test0006"
        series.set_data(sample_ohlc_dicts)
        series.set_markers(
            [
                {
                    "time": 1609459200,
                    "position": "above_bar",
                    "shape": "arrow_down",
                    "color": "#f44336",
                    "text": "Sell",
                },
                {
                    "time": 1609632000,
                    "position": "below_bar",
                    "shape": "arrow_up",
                    "color": "#4caf50",
                    "text": "Buy",
                },
            ]
        )

        html = chart.to_html()
        hash_checker("chart_with_markers", html)
