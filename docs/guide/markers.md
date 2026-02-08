# Markers

Add visual annotations to any series using `createSeriesMarkers()`.

## Basic Markers

```python
from litecharts import createChart, CandlestickSeries, createSeriesMarkers

chart = createChart({"width": 800, "height": 400})
candles = chart.addSeries(CandlestickSeries)
candles.setData([
    {"time": 1609459200, "open": 132.43, "high": 134.54, "low": 131.10, "close": 133.72},
    {"time": 1609545600, "open": 133.75, "high": 135.20, "low": 130.93, "close": 131.96},
    {"time": 1609632000, "open": 132.00, "high": 133.61, "low": 126.38, "close": 126.60},
    {"time": 1609718400, "open": 127.72, "high": 131.05, "low": 126.43, "close": 130.92},
    {"time": 1609804800, "open": 130.85, "high": 131.26, "low": 128.54, "close": 129.41},
])

createSeriesMarkers(candles, [
    {"time": 1609459200, "position": "belowBar", "shape": "arrowUp", "color": "#26a69a", "text": "Buy"},
    {"time": 1609718400, "position": "aboveBar", "shape": "arrowDown", "color": "#ef5350", "text": "Sell"},
])

chart.show()
```

## Marker Options

| Field | Type | Description |
|-------|------|-------------|
| `time` | `int` | Unix timestamp for the marker position |
| `position` | `str` | `"aboveBar"`, `"belowBar"`, or `"inBar"` |
| `shape` | `str` | `"circle"`, `"square"`, `"arrowUp"`, or `"arrowDown"` |
| `color` | `str` | Marker color (e.g. `"#f44336"`) |
| `text` | `str` | Label displayed next to the marker |
| `size` | `int` | Marker size multiplier (default: 1) |

## Marker Handles

`createSeriesMarkers()` returns a `SeriesMarkersApi` handle that lets you manage the marker group after creation:

```python
handle = createSeriesMarkers(candles, [
    {"time": 1609459200, "position": "belowBar", "shape": "arrowUp", "color": "#26a69a"},
])

# Read back markers
handle.markers()

# Replace markers
handle.setMarkers([
    {"time": 1609545600, "position": "aboveBar", "shape": "arrowDown", "color": "#ef5350"},
])

# Remove this marker group entirely
handle.detach()
```

## Multiple Marker Groups

Each call to `createSeriesMarkers()` creates an independent group. Groups are rendered together but managed separately:

```python
# Buy signals
buys = createSeriesMarkers(candles, [
    {"time": 1609459200, "position": "belowBar", "shape": "arrowUp", "color": "#26a69a", "text": "Buy"},
])

# Sell signals
sells = createSeriesMarkers(candles, [
    {"time": 1609718400, "position": "aboveBar", "shape": "arrowDown", "color": "#ef5350", "text": "Sell"},
])

# Remove only the sell signals
sells.detach()
```

You can also access markers through the series:

- `series.markers` — all markers flattened across all groups
- `series.markerGroups` — list of `SeriesMarkersApi` handles
