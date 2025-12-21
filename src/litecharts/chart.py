"""Chart class and factory function."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from .pane import Pane
from .series import (
    AreaSeries,
    BarSeries,
    BaselineSeries,
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
        ChartOptions,
        HistogramSeriesOptions,
        LineSeriesOptions,
        PaneOptions,
    )


def _in_jupyter() -> bool:
    """Check if running in a Jupyter environment."""
    try:
        from IPython import get_ipython  # type: ignore[attr-defined]

        ip = get_ipython()  # type: ignore[no-untyped-call]
        if ip is None:
            return False
        return "IPKernelApp" in ip.config
    except (ImportError, AttributeError):
        return False


class Chart:
    """Main chart class."""

    def __init__(self, options: ChartOptions | None = None) -> None:
        """Initialize the chart.

        Args:
            options: Chart options.
        """
        self._id = f"chart_{uuid.uuid4().hex[:8]}"
        self._options: ChartOptions = options.copy() if options else {}
        self._panes: list[Pane] = []
        self._default_pane: Pane | None = None

    @property
    def id(self) -> str:
        """Return the chart ID."""
        return self._id

    @property
    def options(self) -> ChartOptions:
        """Return the chart options."""
        return self._options

    @property
    def panes(self) -> list[Pane]:
        """Return all panes in the chart."""
        return self._panes

    @property
    def width(self) -> int:
        """Return the chart width."""
        result = self._options.get("width", 800)
        if isinstance(result, int):
            return result
        return 800

    @property
    def height(self) -> int:
        """Return the chart height."""
        result = self._options.get("height", 600)
        if isinstance(result, int):
            return result
        return 600

    def _get_default_pane(self) -> Pane:
        """Get or create the default pane."""
        if self._default_pane is None:
            self._default_pane = Pane()
            self._panes.append(self._default_pane)
        return self._default_pane

    def add_pane(self, options: PaneOptions | None = None) -> Pane:
        """Add a new pane to the chart.

        Args:
            options: Pane options including height_ratio.

        Returns:
            The created Pane.
        """
        pane = Pane(options)
        self._panes.append(pane)
        return pane

    def add_candlestick_series(
        self, options: CandlestickSeriesOptions | None = None
    ) -> CandlestickSeries:
        """Add a candlestick series to the default pane.

        Args:
            options: Candlestick series options.

        Returns:
            The created CandlestickSeries.
        """
        return self._get_default_pane().add_candlestick_series(options)

    def add_line_series(self, options: LineSeriesOptions | None = None) -> LineSeries:
        """Add a line series to the default pane.

        Args:
            options: Line series options.

        Returns:
            The created LineSeries.
        """
        return self._get_default_pane().add_line_series(options)

    def add_area_series(self, options: AreaSeriesOptions | None = None) -> AreaSeries:
        """Add an area series to the default pane.

        Args:
            options: Area series options.

        Returns:
            The created AreaSeries.
        """
        return self._get_default_pane().add_area_series(options)

    def add_bar_series(self, options: BarSeriesOptions | None = None) -> BarSeries:
        """Add a bar series to the default pane.

        Args:
            options: Bar series options.

        Returns:
            The created BarSeries.
        """
        return self._get_default_pane().add_bar_series(options)

    def add_histogram_series(
        self, options: HistogramSeriesOptions | None = None
    ) -> HistogramSeries:
        """Add a histogram series to the default pane.

        Args:
            options: Histogram series options.

        Returns:
            The created HistogramSeries.
        """
        return self._get_default_pane().add_histogram_series(options)

    def add_baseline_series(
        self, options: BaselineSeriesOptions | None = None
    ) -> BaselineSeries:
        """Add a baseline series to the default pane.

        Args:
            options: Baseline series options.

        Returns:
            The created BaselineSeries.
        """
        return self._get_default_pane().add_baseline_series(options)

    def to_html(self) -> str:
        """Generate self-contained HTML for the chart.

        Returns:
            HTML string.
        """
        from .render import render_chart

        return render_chart(self)

    def show(self) -> None:
        """Display the chart.

        Auto-detects environment: uses Jupyter inline display if in a notebook,
        otherwise opens in a browser.
        """
        if _in_jupyter():
            self.show_notebook()
        else:
            self.show_browser()

    def show_notebook(self) -> None:
        """Display the chart inline in a Jupyter notebook."""
        from IPython.display import HTML, display

        display(HTML(self.to_html()))  # type: ignore[no-untyped-call]

    def show_browser(self) -> None:
        """Open the chart in the default web browser."""
        import tempfile
        import webbrowser

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(self.to_html())
            temp_path = f.name

        webbrowser.open(f"file://{temp_path}")

    def save(self, path: str | Path) -> None:
        """Save the chart to an HTML file.

        Args:
            path: File path to save to.
        """
        path = Path(path)
        path.write_text(self.to_html(), encoding="utf-8")


def create_chart(options: ChartOptions | None = None) -> Chart:
    """Create a new chart.

    Args:
        options: Chart options.

    Returns:
        A new Chart instance.
    """
    return Chart(options)
