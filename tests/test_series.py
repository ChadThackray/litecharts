"""Tests for series.py module."""

from __future__ import annotations

from litecharts.series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    SeriesMarkersApi,
    createSeriesMarkers,
)

from .conftest import DataMapping


class TestCandlestickSeries:
    """Tests for CandlestickSeries class."""

    def test_series_type(self) -> None:
        """Series type is Candlestick."""
        series = CandlestickSeries()
        assert series.seriesType == "Candlestick"

    def test_default_options(self) -> None:
        """Default options is empty dict."""
        series = CandlestickSeries()
        assert series.options == {}

    def test_custom_options(self) -> None:
        """Custom options are stored."""
        series = CandlestickSeries({"upColor": "#00ff00"})
        assert series.options.get("upColor") == "#00ff00"

    def test_id_generated(self) -> None:
        """Series ID is generated."""
        series = CandlestickSeries()
        assert series.id.startswith("series_")

    def test_set_data_converts_ohlc(self, sample_ohlc_dicts: list[DataMapping]) -> None:
        """setData converts OHLC data correctly."""
        series = CandlestickSeries()
        series.setData(sample_ohlc_dicts)
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
        """createSeriesMarkers stores normalized markers."""
        series = CandlestickSeries()
        createSeriesMarkers(
            series, [{"time": 1609459200, "position": "aboveBar", "shape": "circle"}]
        )
        assert len(series.markers) == 1
        assert series.markers[0]["time"] == 1609459200

    def test_create_series_markers_with_tooltip(self) -> None:
        """createSeriesMarkers preserves tooltip data."""
        series = CandlestickSeries()
        createSeriesMarkers(
            series,
            [
                {
                    "time": 1609459200,
                    "position": "aboveBar",
                    "shape": "arrowDown",
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


class TestSeriesMarkersApi:
    """Tests for the handle-based marker API (SeriesMarkersApi)."""

    def test_returns_handle(self) -> None:
        """createSeriesMarkers returns a SeriesMarkersApi handle."""
        series = CandlestickSeries()
        handle = createSeriesMarkers(
            series, [{"time": 1609459200, "position": "aboveBar", "shape": "circle"}]
        )
        assert isinstance(handle, SeriesMarkersApi)

    def test_handle_markers(self) -> None:
        """handle.markers() returns the group's markers."""
        series = CandlestickSeries()
        handle = createSeriesMarkers(
            series, [{"time": 1609459200, "position": "aboveBar", "shape": "circle"}]
        )
        assert len(handle.markers()) == 1
        assert handle.markers()[0]["time"] == 1609459200

    def test_handle_set_markers(self) -> None:
        """handle.setMarkers() replaces the group's markers."""
        series = CandlestickSeries()
        handle = createSeriesMarkers(
            series, [{"time": 1609459200, "position": "aboveBar", "shape": "circle"}]
        )
        handle.setMarkers(
            [{"time": 1609545600, "position": "belowBar", "shape": "arrowUp"}]
        )
        assert len(handle.markers()) == 1
        assert handle.markers()[0]["time"] == 1609545600
        assert series.markers[0]["time"] == 1609545600

    def test_handle_detach(self) -> None:
        """handle.detach() removes the group from the series."""
        series = CandlestickSeries()
        handle = createSeriesMarkers(
            series, [{"time": 1609459200, "position": "aboveBar", "shape": "circle"}]
        )
        assert len(series.markers) == 1
        handle.detach()
        assert len(series.markers) == 0
        assert len(series.markerGroups) == 0

    def test_handle_detach_idempotent(self) -> None:
        """handle.detach() is idempotent — calling twice does not raise."""
        series = CandlestickSeries()
        handle = createSeriesMarkers(
            series, [{"time": 1609459200, "position": "aboveBar", "shape": "circle"}]
        )
        handle.detach()
        handle.detach()  # should not raise
        assert len(series.markerGroups) == 0

    def test_multiple_groups_independent(self) -> None:
        """Multiple createSeriesMarkers calls create independent groups."""
        series = CandlestickSeries()
        h1 = createSeriesMarkers(
            series, [{"time": 1609459200, "position": "aboveBar", "shape": "circle"}]
        )
        h2 = createSeriesMarkers(
            series, [{"time": 1609545600, "position": "belowBar", "shape": "arrowUp"}]
        )
        assert len(series.markerGroups) == 2
        assert len(series.markers) == 2
        assert h1.markers()[0]["time"] == 1609459200
        assert h2.markers()[0]["time"] == 1609545600

    def test_detach_one_preserves_other(self) -> None:
        """Detaching one group preserves the other."""
        series = CandlestickSeries()
        h1 = createSeriesMarkers(
            series, [{"time": 1609459200, "position": "aboveBar", "shape": "circle"}]
        )
        h2 = createSeriesMarkers(
            series, [{"time": 1609545600, "position": "belowBar", "shape": "arrowUp"}]
        )
        h1.detach()
        assert len(series.markerGroups) == 1
        assert len(series.markers) == 1
        assert series.markers[0]["time"] == 1609545600
        assert h2.markers()[0]["time"] == 1609545600

    def test_flattened_markers_across_groups(self) -> None:
        """series.markers returns all markers flattened across groups."""
        series = CandlestickSeries()
        createSeriesMarkers(
            series,
            [
                {"time": 1609459200, "position": "aboveBar", "shape": "circle"},
                {"time": 1609545600, "position": "aboveBar", "shape": "circle"},
            ],
        )
        createSeriesMarkers(
            series, [{"time": 1609632000, "position": "belowBar", "shape": "arrowUp"}]
        )
        assert len(series.markers) == 3


class TestLineSeries:
    """Tests for LineSeries class."""

    def test_series_type(self) -> None:
        """Series type is Line."""
        series = LineSeries()
        assert series.seriesType == "Line"

    def test_set_data_converts_single_value(
        self, sample_single_value_dicts: list[DataMapping]
    ) -> None:
        """setData converts single-value data correctly."""
        series = LineSeries()
        series.setData(sample_single_value_dicts)
        assert len(series.data) == 3
        assert series.data[0].get("value") == 100.0


class TestAreaSeries:
    """Tests for AreaSeries class."""

    def test_series_type(self) -> None:
        """Series type is Area."""
        series = AreaSeries()
        assert series.seriesType == "Area"


class TestBarSeries:
    """Tests for BarSeries class."""

    def test_series_type(self) -> None:
        """Series type is Bar."""
        series = BarSeries()
        assert series.seriesType == "Bar"


class TestHistogramSeries:
    """Tests for HistogramSeries class."""

    def test_series_type(self) -> None:
        """Series type is Histogram."""
        series = HistogramSeries()
        assert series.seriesType == "Histogram"


class TestBaselineSeries:
    """Tests for BaselineSeries class."""

    def test_series_type(self) -> None:
        """Series type is Baseline."""
        series = BaselineSeries()
        assert series.seriesType == "Baseline"


class TestRectangles:
    """Tests for rectangle primitive functionality."""

    def test_add_rectangle_stores_data(self) -> None:
        """addRectangle stores rectangle data."""
        series = CandlestickSeries()
        series.addRectangle(
            startTime=1609459200,
            endTime=1609545600,
            startPrice=100.0,
            endPrice=110.0,
            color="rgba(0, 255, 0, 0.2)",
        )
        assert len(series.rectangles) == 1
        assert series.rectangles[0]["startTime"] == 1609459200
        assert series.rectangles[0]["endTime"] == 1609545600
        assert series.rectangles[0]["startPrice"] == 100.0
        assert series.rectangles[0]["endPrice"] == 110.0
        assert series.rectangles[0]["color"] == "rgba(0, 255, 0, 0.2)"

    def test_add_multiple_rectangles(self) -> None:
        """Multiple rectangles can be added."""
        series = CandlestickSeries()
        series.addRectangle(
            startTime=1609459200,
            endTime=1609545600,
            startPrice=100.0,
            endPrice=110.0,
        )
        series.addRectangle(
            startTime=1609545600,
            endTime=1609632000,
            startPrice=105.0,
            endPrice=95.0,
            color="rgba(255, 0, 0, 0.2)",
        )
        assert len(series.rectangles) == 2

    def test_add_rectangle_default_color(self) -> None:
        """Default color is semi-transparent green."""
        series = LineSeries()
        series.addRectangle(
            startTime=1609459200,
            endTime=1609545600,
            startPrice=100.0,
            endPrice=110.0,
        )
        assert series.rectangles[0]["color"] == "rgba(0, 255, 0, 0.2)"

    def test_rectangles_empty_by_default(self) -> None:
        """Rectangles list is empty by default."""
        series = CandlestickSeries()
        assert series.rectangles == []
