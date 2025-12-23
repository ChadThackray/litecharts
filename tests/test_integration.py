"""Integration tests and hash-based regression tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litecharts import Chart, createChart, createSeriesMarkers
from litecharts.series import (
    AreaSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
)

from .conftest import DataMapping

if TYPE_CHECKING:
    from collections.abc import Callable


class TestEndToEndChartCreation:
    """End-to-end tests for chart creation flows."""

    def test_simple_candlestick_chart(
        self, sample_ohlc_dicts: list[DataMapping]
    ) -> None:
        """Create a simple candlestick chart."""
        chart = createChart({"width": 800, "height": 600})
        series = chart.addSeries(CandlestickSeries, {"upColor": "#26a69a"})
        series.setData(sample_ohlc_dicts)

        assert len(chart.panes) == 1
        assert len(chart.panes[0].series) == 1
        assert chart.panes[0].series[0].seriesType == "Candlestick"
        assert len(chart.panes[0].series[0].data) == 3

    def test_multi_series_chart(
        self,
        sample_ohlc_dicts: list[DataMapping],
        sample_single_value_dicts: list[DataMapping],
    ) -> None:
        """Create chart with multiple series in same pane."""
        chart = createChart()
        candle = chart.addSeries(CandlestickSeries)
        candle.setData(sample_ohlc_dicts)
        line = chart.addSeries(LineSeries, {"color": "#ff0000"})
        line.setData(sample_single_value_dicts)

        assert len(chart.panes) == 1
        assert len(chart.panes[0].series) == 2

    def test_multi_pane_chart(
        self,
        sample_ohlc_dicts: list[DataMapping],
        sample_single_value_dicts: list[DataMapping],
    ) -> None:
        """Create chart with multiple panes."""
        chart = createChart({"width": 800, "height": 800})

        # Main price pane
        price_pane = chart.addPane({"stretchFactor": 3.0})
        candle = price_pane.addSeries(CandlestickSeries)
        candle.setData(sample_ohlc_dicts)

        # Volume pane
        volume_pane = chart.addPane({"stretchFactor": 1.0})
        histogram = volume_pane.addSeries(HistogramSeries, {"color": "#26a69a"})
        histogram.setData(sample_single_value_dicts)

        assert len(chart.panes) == 2
        assert chart.panes[0].stretchFactor == 3.0
        assert chart.panes[1].stretchFactor == 1.0

    def test_chart_with_markers(self, sample_ohlc_dicts: list[DataMapping]) -> None:
        """Create chart with markers on series."""
        chart = createChart()
        series = chart.addSeries(CandlestickSeries)
        series.setData(sample_ohlc_dicts)
        createSeriesMarkers(
            series,
            [
                {
                    "time": 1609459200,
                    "position": "aboveBar",
                    "shape": "arrowDown",
                    "color": "#f44336",
                }
            ],
        )

        assert len(series.markers) == 1
        assert series.markers[0]["position"] == "aboveBar"

    def test_chart_with_marker_tooltips(
        self, sample_ohlc_dicts: list[DataMapping]
    ) -> None:
        """Create chart with marker tooltips."""
        chart = createChart()
        series = chart.addSeries(CandlestickSeries)
        series.setData(sample_ohlc_dicts)
        createSeriesMarkers(
            series,
            [
                {
                    "time": 1609459200,
                    "position": "aboveBar",
                    "shape": "arrowDown",
                    "color": "#f44336",
                    "id": "trade-1",
                    "tooltip": {
                        "title": "Sell Signal",
                        "fields": {"Price": "$100", "PnL": "+$50"},
                    },
                }
            ],
        )

        assert len(series.markers) == 1
        assert series.markers[0]["tooltip"]["title"] == "Sell Signal"

        # Verify HTML contains tooltip code
        html = chart.toHtml()
        assert "subscribeCrosshairMove" in html
        assert "markerTooltips_" in html
        assert "trade-1" in html
        assert "Sell Signal" in html

    def test_chart_with_rectangles(self, sample_ohlc_dicts: list[DataMapping]) -> None:
        """Create chart with rectangle primitives."""
        chart = createChart()
        series = chart.addSeries(CandlestickSeries)
        series.setData(sample_ohlc_dicts)

        # Add a trade zone rectangle
        series.addRectangle(
            startTime=1609459200,
            endTime=1609545600,
            startPrice=100.0,
            endPrice=110.0,
            color="rgba(0, 255, 0, 0.2)",
        )

        assert len(series.rectangles) == 1

        # Verify HTML contains rectangle primitive code
        html = chart.toHtml()
        assert "RectanglePrimitive" in html
        assert "RectanglePrimitivePaneView" in html
        assert "RectanglePrimitiveRenderer" in html
        assert "attachPrimitive" in html
        assert "startTime" in html
        assert "endTime" in html
        assert "startPrice" in html
        assert "endPrice" in html

    def test_chart_without_rectangles_excludes_primitive(
        self, sample_ohlc_dicts: list[DataMapping]
    ) -> None:
        """Chart without rectangles does not include primitive JS."""
        chart = createChart()
        series = chart.addSeries(CandlestickSeries)
        series.setData(sample_ohlc_dicts)

        # No rectangles added
        html = chart.toHtml()
        assert "RectanglePrimitive" not in html


class TestHtmlOutputRegression:
    """Hash-based regression tests for HTML output."""

    def test_empty_chart_html(self, hash_checker: Callable[[str, str], None]) -> None:
        """Empty chart HTML output is stable."""
        chart = Chart()
        # Override ID for deterministic output
        chart._id = "chart_test0001"
        html = chart.toHtml()
        hash_checker("empty_chart", html)

    def test_simple_candlestick_html(
        self,
        sample_ohlc_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Simple candlestick chart HTML output is stable."""
        chart = Chart({"width": 800, "height": 600})
        chart._id = "chart_test0002"
        pane = chart.addPane()
        pane._id = "pane_test0001"
        series = pane.addSeries(
            CandlestickSeries, {"upColor": "#26a69a", "downColor": "#ef5350"}
        )
        series._id = "series_test0001"
        series.setData(sample_ohlc_dicts)

        html = chart.toHtml()
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

        price_pane = chart.addPane({"stretchFactor": 3.0})
        price_pane._id = "pane_test0002"
        candle = price_pane.addSeries(CandlestickSeries)
        candle._id = "series_test0002"
        candle.setData(sample_ohlc_dicts)

        volume_pane = chart.addPane({"stretchFactor": 1.0})
        volume_pane._id = "pane_test0003"
        histogram = volume_pane.addSeries(HistogramSeries, {"color": "#26a69a"})
        histogram._id = "series_test0003"
        histogram.setData(sample_single_value_dicts)

        html = chart.toHtml()
        hash_checker("multi_pane", html)

    def test_line_series_html(
        self,
        sample_single_value_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Line series chart HTML output is stable."""
        chart = Chart({"width": 600, "height": 400})
        chart._id = "chart_test0004"
        pane = chart.addPane()
        pane._id = "pane_test0004"
        series = pane.addSeries(LineSeries, {"color": "#2196f3", "lineWidth": 2})
        series._id = "series_test0004"
        series.setData(sample_single_value_dicts)

        html = chart.toHtml()
        hash_checker("line_series", html)

    def test_area_series_html(
        self,
        sample_single_value_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Area series chart HTML output is stable."""
        chart = Chart()
        chart._id = "chart_test0005"
        pane = chart.addPane()
        pane._id = "pane_test0005"
        series = pane.addSeries(
            AreaSeries,
            {
                "lineColor": "#2196f3",
                "topColor": "rgba(33, 150, 243, 0.4)",
                "bottomColor": "rgba(33, 150, 243, 0.0)",
            },
        )
        series._id = "series_test0005"
        series.setData(sample_single_value_dicts)

        html = chart.toHtml()
        hash_checker("area_series", html)

    def test_chart_with_markers_html(
        self,
        sample_ohlc_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Chart with markers HTML output is stable."""
        chart = Chart()
        chart._id = "chart_test0006"
        pane = chart.addPane()
        pane._id = "pane_test0006"
        series = pane.addSeries(CandlestickSeries)
        series._id = "series_test0006"
        series.setData(sample_ohlc_dicts)
        createSeriesMarkers(
            series,
            [
                {
                    "time": 1609459200,
                    "position": "aboveBar",
                    "shape": "arrowDown",
                    "color": "#f44336",
                    "text": "Sell",
                    "id": "sell-1",
                    "tooltip": {
                        "title": "Sell Signal",
                        "fields": {"Price": "$105", "PnL": "+$10"},
                    },
                },
                {
                    "time": 1609632000,
                    "position": "belowBar",
                    "shape": "arrowUp",
                    "color": "#4caf50",
                    "text": "Buy",
                    "id": "buy-1",
                    "tooltip": {
                        "title": "Buy Signal",
                        "fields": {"Price": "$115", "Size": "100"},
                    },
                },
            ],
        )

        html = chart.toHtml()
        hash_checker("chart_with_markers", html)

    def test_chart_with_price_lines_html(
        self,
        sample_ohlc_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Chart with price lines HTML output is stable."""
        chart = Chart()
        chart._id = "chart_test0007"
        pane = chart.addPane()
        pane._id = "pane_test0007"
        series = pane.addSeries(CandlestickSeries)
        series._id = "series_test0007"
        series.setData(sample_ohlc_dicts)

        # Add price lines at support and resistance levels
        series.createPriceLine(
            {
                "price": 100.0,
                "color": "#4caf50",
                "lineWidth": 2,
                "lineStyle": 2,  # Dashed
                "title": "Support",
                "axisLabelVisible": True,
            }
        )
        series.createPriceLine(
            {
                "price": 115.0,
                "color": "#f44336",
                "lineWidth": 2,
                "lineStyle": 0,  # Solid
                "title": "Resistance",
                "axisLabelVisible": True,
            }
        )

        html = chart.toHtml()
        hash_checker("chart_with_price_lines", html)

    def test_chart_with_rectangles_html(
        self,
        sample_ohlc_dicts: list[DataMapping],
        hash_checker: Callable[[str, str], None],
    ) -> None:
        """Chart with rectangle primitives HTML output is stable."""
        chart = Chart()
        chart._id = "chart_test0008"
        pane = chart.addPane()
        pane._id = "pane_test0008"
        series = pane.addSeries(CandlestickSeries)
        series._id = "series_test0008"
        series.setData(sample_ohlc_dicts)

        # Add trade zone rectangles
        series.addRectangle(
            startTime=1609459200,
            endTime=1609545600,
            startPrice=100.0,
            endPrice=108.0,
            color="rgba(76, 175, 80, 0.2)",  # Green for profit
        )
        series.addRectangle(
            startTime=1609545600,
            endTime=1609632000,
            startPrice=110.0,
            endPrice=105.0,
            color="rgba(244, 67, 54, 0.2)",  # Red for loss
        )

        html = chart.toHtml()
        hash_checker("chart_with_rectangles", html)
