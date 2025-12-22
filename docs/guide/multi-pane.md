# Multi-Pane Charts

Create charts with multiple synchronized panes, useful for showing price and volume together.

## Basic Multi-Pane

```python
from litecharts import createChart, CandlestickSeries, HistogramSeries

chart = createChart({"width": 800, "height": 600})

# Main pane for price
mainPane = chart.addPane({"heightRatio": 3})
candles = mainPane.addSeries(CandlestickSeries)
candles.setData(ohlcData)

# Secondary pane for volume
volumePane = chart.addPane({"heightRatio": 1})
volume = volumePane.addSeries(HistogramSeries)
volume.setData(volumeData)

chart.show()
```

## Pane Options

### Height Ratio

Control relative pane sizes with `heightRatio`:

```python
# Price pane takes 3/4 of the height
mainPane = chart.addPane({"heightRatio": 3})

# Volume pane takes 1/4 of the height
volumePane = chart.addPane({"heightRatio": 1})
```

## Synchronized Time Scale

All panes automatically share the same time scale. Scrolling or zooming one pane affects all panes.

## Multiple Series Per Pane

Add multiple series to the same pane:

```python
mainPane = chart.addPane()

# Candlesticks
candles = mainPane.addSeries(CandlestickSeries)
candles.setData(ohlcData)

# Overlay a line (e.g., moving average)
ma = mainPane.addSeries(LineSeries, {"color": "#2196F3"})
ma.setData(maData)
```
