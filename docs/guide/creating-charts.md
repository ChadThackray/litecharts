# Creating Charts

## Basic Chart

Create a chart with `createChart()`:

```python
from litecharts import createChart, CandlestickSeries

chart = createChart()
candles = chart.addSeries(CandlestickSeries)
candles.setData(data)
chart.show()
```

## Chart Options

Pass options to customize the chart:

```python
chart = createChart({
    "width": 800,
    "height": 600,
    "layout": {
        "background": {"type": "solid", "color": "#1e1e1e"},
        "textColor": "#d1d4dc",
    },
    "grid": {
        "vertLines": {"color": "#2B2B43"},
        "horzLines": {"color": "#2B2B43"},
    },
})
```

## Display Methods

### show()

Auto-detects environment and displays the chart:

```python
chart.show()  # Jupyter inline or browser window
```

### toHtml()

Get the chart as a self-contained HTML string:

```python
html = chart.toHtml()
with open("chart.html", "w") as f:
    f.write(html)
```

### save()

Save directly to a file:

```python
chart.save("chart.html")
```

## Dashboard / Multi-Chart Pages

For dashboards with multiple charts, use `toFragment()` to avoid duplicating
the LWC library (~200KB) in each chart:

```python
from litecharts import (
    createChart, CandlestickSeries, LineSeries,
    getLwcScript, getPluginScripts, getDefaultStyles
)

# Create charts
chart1 = createChart({"width": 400, "height": 300})
chart1.addSeries(CandlestickSeries).setData(btc_data)

chart2 = createChart({"width": 400, "height": 300})
chart2.addSeries(LineSeries).setData(eth_data)

# Combine into single page
html = f'''<!DOCTYPE html>
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
</html>'''

with open("dashboard.html", "w") as f:
    f.write(html)
```

### Fragment API

| Function | Description |
|----------|-------------|
| `chart.toFragment()` | Returns container divs + init script (no library) |
| `getLwcScript()` | Returns `<script>` tag with LWC library |
| `getPluginScripts()` | Returns `<script>` tags for all plugins |
| `getDefaultStyles(chartId)` | Returns CSS for chart container |

### Important Notes

- **Script ordering**: `getLwcScript()` and `getPluginScripts()` must be in
  `<head>` (or before any fragments) because fragment init scripts call
  `LightweightCharts.createChart()`.

- **Plugin scripts**: `getPluginScripts()` includes all plugin code (rectangles,
  etc.) — just include it once, no per-chart detection needed.

- **Styles**: `getDefaultStyles()` returns only container-scoped CSS (flexbox
  for pane stacking), not body-level styles like background color.
