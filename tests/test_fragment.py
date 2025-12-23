"""Tests for HTML fragment rendering."""

from __future__ import annotations

from litecharts import (
    CandlestickSeries,
    LineSeries,
    createChart,
    createSeriesMarkers,
    getDefaultStyles,
    getLwcScript,
    getPluginScripts,
)

from .conftest import DataMapping


class TestToFragment:
    """Tests for Chart.toFragment() method."""

    def test_returns_container_div(self) -> None:
        """Fragment contains container div with correct ID."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        assert f'id="container_{chart.id}"' in fragment

    def test_uses_native_panes(self) -> None:
        """Fragment uses native LWC pane API."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        # Native panes use chart.panes()[0] to get default pane
        assert ".panes()[0]" in fragment

    def test_no_doctype(self) -> None:
        """Fragment does NOT include DOCTYPE."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        assert "<!DOCTYPE" not in fragment

    def test_no_html_tag(self) -> None:
        """Fragment does NOT include <html> tag."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        assert "<html>" not in fragment
        assert "</html>" not in fragment

    def test_no_head_tag(self) -> None:
        """Fragment does NOT include <head> tag."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        assert "<head>" not in fragment
        assert "</head>" not in fragment

    def test_no_body_tag(self) -> None:
        """Fragment does NOT include <body> tag."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        assert "<body>" not in fragment
        assert "</body>" not in fragment

    def test_no_lwc_library(self) -> None:
        """Fragment does NOT include LWC library inline."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        # The LWC library is large and contains specific identifiers
        assert "LightweightCharts.createChart" in fragment  # Init code present
        # But the library definition itself should not be present
        # Library would contain things like version info or module boilerplate
        assert len(fragment) < 10000  # Fragment should be small, not ~200KB

    def test_includes_script_tags(self) -> None:
        """Fragment includes init script wrapped in script tags."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        assert "<script>" in fragment
        assert "</script>" in fragment

    def test_includes_create_chart_call(self) -> None:
        """Fragment includes createChart initialization."""
        chart = createChart()
        chart.addSeries(LineSeries).setData([{"time": 1609459200, "value": 100.0}])
        fragment = chart.toFragment()
        assert "LightweightCharts.createChart" in fragment

    def test_empty_chart_no_data_message(self) -> None:
        """Empty chart fragment shows no data message."""
        chart = createChart()
        fragment = chart.toFragment()
        assert "No data to display" in fragment

    def test_empty_chart_no_script(self) -> None:
        """Empty chart fragment has no script tag."""
        chart = createChart()
        fragment = chart.toFragment()
        assert "<script>" not in fragment

    def test_includes_marker_tooltip_js(
        self, sample_ohlc_dicts: list[DataMapping]
    ) -> None:
        """Fragment includes marker tooltip JS when markers have tooltips."""
        chart = createChart()
        series = chart.addSeries(CandlestickSeries)
        series.setData(sample_ohlc_dicts)
        createSeriesMarkers(
            series,
            [
                {
                    "id": "signal-1",  # id is required for tooltips to work
                    "time": 1609459200,
                    "position": "aboveBar",
                    "shape": "arrowDown",
                    "color": "#f44336",
                    "tooltip": {"title": "Signal", "body": "Buy signal"},
                }
            ],
        )
        fragment = chart.toFragment()
        assert "markerTooltips_" in fragment

    def test_multi_pane_uses_native_api(
        self, sample_ohlc_dicts: list[DataMapping]
    ) -> None:
        """Multi-pane fragment uses native LWC pane API (no manual sync)."""
        chart = createChart()
        pane1 = chart.addPane()
        pane1.addSeries(CandlestickSeries).setData(sample_ohlc_dicts)
        pane2 = chart.addPane()
        pane2.addSeries(LineSeries).setData([
            {"time": 1609459200, "value": 100.0},
            {"time": 1609545600, "value": 110.0},
        ])
        fragment = chart.toFragment()
        # Native panes don't need manual time sync
        assert "subscribeVisibleLogicalRangeChange" not in fragment
        # Uses addPane() for additional panes
        assert ".addPane()" in fragment
        # Sets stretch factor for sizing
        assert ".setStretchFactor(" in fragment


class TestGetLwcScript:
    """Tests for getLwcScript() function."""

    def test_returns_script_tag(self) -> None:
        """getLwcScript returns content wrapped in script tags."""
        script = getLwcScript()
        assert script.startswith("<script>")
        assert script.endswith("</script>")

    def test_contains_lwc_library(self) -> None:
        """getLwcScript contains the LWC library code."""
        script = getLwcScript()
        # The library should be substantial
        assert len(script) > 100000  # ~200KB minified

    def test_no_escaping_needed(self) -> None:
        """getLwcScript returns raw HTML - no extra escaping needed."""
        script = getLwcScript()
        # Should not contain escaped angle brackets
        assert "&lt;" not in script
        assert "&gt;" not in script


class TestGetPluginScripts:
    """Tests for getPluginScripts() function."""

    def test_returns_script_tag(self) -> None:
        """getPluginScripts returns content wrapped in script tags."""
        scripts = getPluginScripts()
        assert "<script>" in scripts
        assert "</script>" in scripts

    def test_contains_rectangle_primitive(self) -> None:
        """getPluginScripts contains rectangle primitive code."""
        scripts = getPluginScripts()
        assert "RectanglePrimitive" in scripts


class TestGetDefaultStyles:
    """Tests for getDefaultStyles() function."""

    def test_returns_container_scoped_css(self) -> None:
        """getDefaultStyles returns CSS comment for the container."""
        styles = getDefaultStyles("test123")
        assert "container_test123" in styles

    def test_no_flexbox_needed(self) -> None:
        """getDefaultStyles no longer needs flexbox (native panes handle layout)."""
        styles = getDefaultStyles("test123")
        # Native LWC panes handle layout internally
        assert "display: flex" not in styles

    def test_no_body_styles(self) -> None:
        """getDefaultStyles does NOT include body-level styles."""
        styles = getDefaultStyles("test123")
        assert "body" not in styles
        assert "margin:" not in styles
        assert "padding:" not in styles
        assert "background:" not in styles


class TestFragmentIntegration:
    """Integration tests for combining fragments."""

    def test_multiple_fragments_combine(
        self, sample_ohlc_dicts: list[DataMapping]
    ) -> None:
        """Multiple fragments can be combined with single library."""
        chart1 = createChart({"width": 400, "height": 300})
        chart1.addSeries(CandlestickSeries).setData(sample_ohlc_dicts)

        chart2 = createChart({"width": 400, "height": 300})
        chart2.addSeries(LineSeries).setData([
            {"time": 1609459200, "value": 100.0},
            {"time": 1609545600, "value": 110.0},
        ])

        html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        {getDefaultStyles(chart1.id)}
        {getDefaultStyles(chart2.id)}
    </style>
    {getLwcScript()}
    {getPluginScripts()}
</head>
<body>
    <div style="display: flex; gap: 20px;">
        {chart1.toFragment()}
        {chart2.toFragment()}
    </div>
</body>
</html>"""

        # Verify structure
        assert "<!DOCTYPE html>" in html
        assert f"container_{chart1.id}" in html
        assert f"container_{chart2.id}" in html
        # LWC library should appear only once
        assert html.count("LightweightCharts.createChart") == 2  # One per chart
        # Library source should appear only once (it's huge)
        assert html.count("<script>") == 4  # library + plugins + 2 chart scripts
