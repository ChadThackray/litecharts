"""Tests for series.py module."""

from __future__ import annotations

from litecharts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    create_series_markers,
)

from .conftest import DataMapping


class TestCandlestickSeries:
    """Tests for CandlestickSeries class."""

    def test_series_type(self) -> None:
        """Series type is Candlestick."""
        series = CandlestickSeries()
        assert series.series_type == "Candlestick"

    def test_default_options(self) -> None:
        """Default options is empty dict."""
        series = CandlestickSeries()
        assert series.options == {}

    def test_custom_options(self) -> None:
        """Custom options are stored."""
        series = CandlestickSeries({"up_color": "#00ff00"})
        assert series.options.get("up_color") == "#00ff00"

    def test_id_generated(self) -> None:
        """Series ID is generated."""
        series = CandlestickSeries()
        assert series.id.startswith("series_")

    def test_set_data_converts_ohlc(self, sample_ohlc_dicts: list[DataMapping]) -> None:
        """set_data converts OHLC data correctly."""
        series = CandlestickSeries()
        series.set_data(sample_ohlc_dicts)
        assert len(series.data) == 3
        assert series.data[0]["time"] == 1609459200
        assert series.data[0].get("open") == 100.0

    def test_update_appends_data(self) -> None:
        """update appends a single data point."""
        series = CandlestickSeries()
        series.update(
            {
                "time": 1609459200,
                "open": 100.0,
                "high": 110.0,
                "low": 95.0,
                "close": 105.0,
            }
        )
        assert len(series.data) == 1

    def test_create_series_markers(self) -> None:
        """create_series_markers stores normalized markers."""
        series = CandlestickSeries()
        create_series_markers(
            series, [{"time": 1609459200, "position": "above_bar", "shape": "circle"}]
        )
        assert len(series.markers) == 1
        assert series.markers[0]["time"] == 1609459200

    def test_create_series_markers_with_tooltip(self) -> None:
        """create_series_markers preserves tooltip data."""
        series = CandlestickSeries()
        create_series_markers(
            series,
            [
                {
                    "time": 1609459200,
                    "position": "above_bar",
                    "shape": "arrow_down",
                    "color": "#ff0000",
                    "id": "trade-1",
                    "tooltip": {
                        "title": "Sell Signal",
                        "fields": {"Price": "$100", "PnL": "+$50"},
                    },
                }
            ],
        )
        assert len(series.markers) == 1
        assert series.markers[0]["id"] == "trade-1"
        assert series.markers[0]["tooltip"]["title"] == "Sell Signal"
        assert series.markers[0]["tooltip"]["fields"]["PnL"] == "+$50"


class TestLineSeries:
    """Tests for LineSeries class."""

    def test_series_type(self) -> None:
        """Series type is Line."""
        series = LineSeries()
        assert series.series_type == "Line"

    def test_set_data_converts_single_value(
        self, sample_single_value_dicts: list[DataMapping]
    ) -> None:
        """set_data converts single-value data correctly."""
        series = LineSeries()
        series.set_data(sample_single_value_dicts)
        assert len(series.data) == 3
        assert series.data[0].get("value") == 100.0


class TestAreaSeries:
    """Tests for AreaSeries class."""

    def test_series_type(self) -> None:
        """Series type is Area."""
        series = AreaSeries()
        assert series.series_type == "Area"


class TestBarSeries:
    """Tests for BarSeries class."""

    def test_series_type(self) -> None:
        """Series type is Bar."""
        series = BarSeries()
        assert series.series_type == "Bar"


class TestHistogramSeries:
    """Tests for HistogramSeries class."""

    def test_series_type(self) -> None:
        """Series type is Histogram."""
        series = HistogramSeries()
        assert series.series_type == "Histogram"


class TestBaselineSeries:
    """Tests for BaselineSeries class."""

    def test_series_type(self) -> None:
        """Series type is Baseline."""
        series = BaselineSeries()
        assert series.series_type == "Baseline"


class TestRectangles:
    """Tests for rectangle primitive functionality."""

    def test_add_rectangle_stores_data(self) -> None:
        """add_rectangle stores rectangle data."""
        series = CandlestickSeries()
        series.add_rectangle(
            start_time=1609459200,
            end_time=1609545600,
            start_price=100.0,
            end_price=110.0,
            color="rgba(0, 255, 0, 0.2)",
        )
        assert len(series.rectangles) == 1
        assert series.rectangles[0]["start_time"] == 1609459200
        assert series.rectangles[0]["end_time"] == 1609545600
        assert series.rectangles[0]["start_price"] == 100.0
        assert series.rectangles[0]["end_price"] == 110.0
        assert series.rectangles[0]["color"] == "rgba(0, 255, 0, 0.2)"

    def test_add_multiple_rectangles(self) -> None:
        """Multiple rectangles can be added."""
        series = CandlestickSeries()
        series.add_rectangle(
            start_time=1609459200,
            end_time=1609545600,
            start_price=100.0,
            end_price=110.0,
        )
        series.add_rectangle(
            start_time=1609545600,
            end_time=1609632000,
            start_price=105.0,
            end_price=95.0,
            color="rgba(255, 0, 0, 0.2)",
        )
        assert len(series.rectangles) == 2

    def test_add_rectangle_default_color(self) -> None:
        """Default color is semi-transparent green."""
        series = LineSeries()
        series.add_rectangle(
            start_time=1609459200,
            end_time=1609545600,
            start_price=100.0,
            end_price=110.0,
        )
        assert series.rectangles[0]["color"] == "rgba(0, 255, 0, 0.2)"

    def test_rectangles_empty_by_default(self) -> None:
        """Rectangles list is empty by default."""
        series = CandlestickSeries()
        assert series.rectangles == []
