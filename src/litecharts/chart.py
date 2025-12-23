"""Chart class and factory function."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import TYPE_CHECKING, overload

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
    from .series import BaseSeries
    from .types import (
        AreaSeriesOptions,
        BarSeriesOptions,
        BaselineSeriesOptions,
        CandlestickSeriesOptions,
        ChartOptions,
        HistogramSeriesOptions,
        LineSeriesOptions,
        OhlcInput,
        PaneOptions,
        SingleValueInput,
    )


def _inJupyter() -> bool:
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
        self._defaultPane: Pane | None = None

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

    def _getDefaultPane(self) -> Pane:
        """Get or create the default pane."""
        if self._defaultPane is None:
            self._defaultPane = Pane()
            self._panes.append(self._defaultPane)
        return self._defaultPane

    def addPane(self, options: PaneOptions | None = None) -> Pane:
        """Add a new pane to the chart.

        Args:
            options: Pane options including stretchFactor.

        Returns:
            The created Pane.
        """
        pane = Pane(options)
        self._panes.append(pane)
        return pane

    @overload
    def addSeries(
        self,
        seriesType: type[CandlestickSeries],
        options: CandlestickSeriesOptions | None = None,
        paneIndex: int | None = None,
    ) -> CandlestickSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[LineSeries],
        options: LineSeriesOptions | None = None,
        paneIndex: int | None = None,
    ) -> LineSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[AreaSeries],
        options: AreaSeriesOptions | None = None,
        paneIndex: int | None = None,
    ) -> AreaSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[BarSeries],
        options: BarSeriesOptions | None = None,
        paneIndex: int | None = None,
    ) -> BarSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[HistogramSeries],
        options: HistogramSeriesOptions | None = None,
        paneIndex: int | None = None,
    ) -> HistogramSeries: ...

    @overload
    def addSeries(
        self,
        seriesType: type[BaselineSeries],
        options: BaselineSeriesOptions | None = None,
        paneIndex: int | None = None,
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
        paneIndex: int | None = None,
    ) -> BaseSeries[SingleValueInput] | BaseSeries[OhlcInput]:
        """Add a series to a pane.

        Args:
            seriesType: The series class (e.g., CandlestickSeries, LineSeries).
            options: Series options specific to the series type.
            paneIndex: Index of the pane to add the series to. If None, uses
                the default pane (creating it if necessary). Note: explicit
                pane indices require the pane to already exist via addPane().
                Use paneIndex=None for automatic default pane creation.

        Returns:
            The created series instance.

        Raises:
            IndexError: If paneIndex is out of range (panes must be created
                with addPane() before using explicit indices).
        """
        if paneIndex is not None:
            if paneIndex < 0 or paneIndex >= len(self._panes):
                raise IndexError(f"Pane index {paneIndex} out of range")
            pane = self._panes[paneIndex]
        else:
            pane = self._getDefaultPane()

        return pane.addSeries(seriesType, options)  # type: ignore[arg-type]

    def toHtml(self) -> str:
        """Generate self-contained HTML for the chart.

        Returns:
            HTML string.
        """
        from .render import renderChart

        return renderChart(self)

    def toFragment(self) -> str:
        """Generate an HTML fragment for embedding in custom pages.

        Returns container divs and initialization script, but NOT the LWC library
        or full HTML document wrapper. Use with getLwcScript() and getPluginScripts()
        for dashboards with multiple charts.

        Example::

            from litecharts import (
                createChart, getLwcScript, getPluginScripts, CandlestickSeries
            )

            chart1 = createChart()
            chart1.addSeries(CandlestickSeries).setData(data1)

            chart2 = createChart()
            chart2.addSeries(CandlestickSeries).setData(data2)

            html = f'''
            <html>
            <head>
                {getLwcScript()}
                {getPluginScripts()}
            </head>
            <body>
                {chart1.toFragment()}
                {chart2.toFragment()}
            </body>
            </html>
            '''

        Returns:
            HTML fragment string.
        """
        from .render import renderFragment

        return renderFragment(self)

    def show(self) -> None:
        """Display the chart.

        Auto-detects environment: uses Jupyter inline display if in a notebook,
        otherwise opens in a browser.
        """
        if _inJupyter():
            self.showNotebook()
        else:
            self.showBrowser()

    def showNotebook(self) -> None:
        """Display the chart inline in a Jupyter notebook."""
        from IPython.display import HTML, display

        display(HTML(self.toHtml()))  # type: ignore[no-untyped-call]

    def showBrowser(self) -> None:
        """Open the chart in the default web browser."""
        import tempfile
        import webbrowser

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(self.toHtml())
            temp_path = f.name

        webbrowser.open(f"file://{temp_path}")

    def save(self, path: str | Path) -> None:
        """Save the chart to an HTML file.

        Args:
            path: File path to save to.
        """
        path = Path(path)
        path.write_text(self.toHtml(), encoding="utf-8")


def createChart(options: ChartOptions | None = None) -> Chart:
    """Create a new chart.

    Args:
        options: Chart options.

    Returns:
        A new Chart instance.
    """
    return Chart(options)
