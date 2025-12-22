# Series Types

litecharts supports all series types from TradingView Lightweight Charts.

## Available Series

### CandlestickSeries

The most common chart type for financial data, showing open, high, low, and close prices.

```python
from litecharts import createChart, CandlestickSeries

chart = createChart()
candles = chart.addSeries(CandlestickSeries)
candles.setData([
    {"time": 1609459200, "open": 100, "high": 105, "low": 95, "close": 102},
])
```

### LineSeries

Simple line chart connecting data points.

```python
from litecharts import createChart, LineSeries

chart = createChart()
line = chart.addSeries(LineSeries)
line.setData([
    {"time": 1609459200, "value": 100},
    {"time": 1609545600, "value": 105},
])
```

### AreaSeries

Line chart with filled area below.

```python
from litecharts import createChart, AreaSeries

chart = createChart()
area = chart.addSeries(AreaSeries)
area.setData([
    {"time": 1609459200, "value": 100},
])
```

### HistogramSeries

Vertical bars, useful for volume data.

```python
from litecharts import createChart, HistogramSeries

chart = createChart()
histogram = chart.addSeries(HistogramSeries)
histogram.setData([
    {"time": 1609459200, "value": 1000, "color": "#26a69a"},
])
```

### BarSeries

OHLC bars without candle bodies.

```python
from litecharts import createChart, BarSeries

chart = createChart()
bars = chart.addSeries(BarSeries)
bars.setData([
    {"time": 1609459200, "open": 100, "high": 105, "low": 95, "close": 102},
])
```

### BaselineSeries

Line chart with different colors above/below a baseline.

```python
from litecharts import createChart, BaselineSeries

chart = createChart()
baseline = chart.addSeries(BaselineSeries, {"baseValue": {"type": "price", "price": 100}})
baseline.setData([
    {"time": 1609459200, "value": 102},
])
```
