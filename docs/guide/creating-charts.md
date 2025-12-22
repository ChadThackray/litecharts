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
