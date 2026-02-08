# Customization

Customize charts and series to match your preferences.

## Chart Layout

```python
chart = createChart({
    "layout": {
        "background": {"type": "solid", "color": "#ffffff"},
        "textColor": "#333333",
    },
})
```

### Dark Theme

```python
chart = createChart({
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

## Series Styling

### Candlestick Colors

```python
candles = chart.addSeries(CandlestickSeries, {
    "upColor": "#26a69a",
    "downColor": "#ef5350",
    "borderVisible": False,
    "wickUpColor": "#26a69a",
    "wickDownColor": "#ef5350",
})
```

### Line Series

```python
line = chart.addSeries(LineSeries, {
    "color": "#2196F3",
    "lineWidth": 2,
    "lineStyle": 0,  # 0=solid, 1=dotted, 2=dashed
})
```

### Area Series

```python
area = chart.addSeries(AreaSeries, {
    "topColor": "rgba(33, 150, 243, 0.4)",
    "bottomColor": "rgba(33, 150, 243, 0.0)",
    "lineColor": "#2196F3",
    "lineWidth": 2,
})
```

## Time Scale

```python
chart = createChart({
    "timeScale": {
        "timeVisible": True,
        "secondsVisible": False,
        "borderColor": "#2B2B43",
    },
})
```

### Fit Content

Auto-fit the visible time range to show all data points:

```python
chart = createChart({"width": 800, "height": 400})
candles = chart.addSeries(CandlestickSeries)
candles.setData(data)

chart.fitContent()
chart.show()
```

This calls `timeScale().fitContent()` in the generated JS. Best for small/medium datasets — for large datasets the default behavior (anchored to the right edge) may be preferable.

## Price Scale

```python
chart = createChart({
    "rightPriceScale": {
        "borderColor": "#2B2B43",
        "scaleMargins": {
            "top": 0.1,
            "bottom": 0.1,
        },
    },
})
```

## Full Options Reference

For all available options, see the [Lightweight Charts documentation](https://tradingview.github.io/lightweight-charts/docs/api).
