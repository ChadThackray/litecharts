# litecharts

[![PyPI version](https://badge.fury.io/py/litecharts.svg)](https://pypi.org/project/litecharts/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typed](https://img.shields.io/badge/typed-strict-blue.svg)](https://mypy-lang.org/)
[![Docs](https://img.shields.io/badge/docs-online-blue.svg)](https://chadthackray.github.io/litecharts/)

> **Warning:** This library is in alpha. The API may change unexpectedly between versions.

Thin Python wrapper for [TradingView Lightweight Charts](https://tradingview.github.io/lightweight-charts/). **[Documentation](https://chadthackray.github.io/litecharts/)**

## Installation

```bash
pip install litecharts
```

## Quick Start

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

## Features

- Candlestick, Line, Area, Bar, Histogram, and Baseline series
- Multi-pane layouts with synced time scales
- Pandas DataFrame and NumPy array support
- Jupyter notebook integration
- Self-contained HTML output

## Data Input

Accepts multiple formats:

```python
# List of dicts
candles.setData([{"time": 1609459200, "open": 100, "high": 105, "low": 95, "close": 102}])

# Pandas DataFrame
import pandas as pd
df = pd.DataFrame({"open": [100], "high": [105], "low": [95], "close": [102]},
                  index=pd.to_datetime(["2021-01-01"]))
candles.setData(df)

# NumPy array (columns: time, open, high, low, close)
import numpy as np
arr = np.array([[1609459200, 100, 105, 95, 102]])
candles.setData(arr)
```

## Multi-Pane Charts

```python
from litecharts import createChart, CandlestickSeries, HistogramSeries

chart = createChart({"width": 800, "height": 600})

# Main pane
mainPane = chart.addPane({"stretchFactor": 3})
candles = mainPane.addSeries(CandlestickSeries)
candles.setData(ohlcData)

# Volume pane
volumePane = chart.addPane({"stretchFactor": 1})
volume = volumePane.addSeries(HistogramSeries)
volume.setData(volumeData)

chart.show()
```

## License

MIT - see [LICENSE](LICENSE)

This package bundles [Lightweight Charts](https://github.com/tradingview/lightweight-charts) by TradingView, Inc., licensed under Apache 2.0. See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
