# Getting Started

litecharts is a thin Python wrapper for [TradingView Lightweight Charts](https://tradingview.github.io/lightweight-charts/), providing an easy way to create interactive financial charts.

::: warning Alpha Software
This library is in alpha. The API may change unexpectedly between versions.
:::

## Installation

```bash
pip install litecharts
```

## Quick Example

```python
from litecharts import createChart, CandlestickSeries

# Create a chart
chart = createChart({"width": 800, "height": 600})

# Add a candlestick series
candles = chart.addSeries(CandlestickSeries)
candles.setData([
    {"time": 1609459200, "open": 100, "high": 105, "low": 95, "close": 102},
    {"time": 1609545600, "open": 102, "high": 110, "low": 100, "close": 108},
    {"time": 1609632000, "open": 108, "high": 115, "low": 105, "close": 112},
])

# Display the chart
chart.show()  # Auto-detects Jupyter or opens browser
```

## What's Next?

- Learn about [different series types](/guide/series-types)
- See how to use [Pandas DataFrames](/guide/data-formats)
- Create [multi-pane layouts](/guide/multi-pane)
- Add [markers](/guide/markers) for buy/sell signals
