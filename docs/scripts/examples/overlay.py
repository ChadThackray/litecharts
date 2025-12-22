from litecharts import CandlestickSeries, LineSeries, createChart

# Sample OHLC data
ohlc_data = [
    {"time": 1609459200, "open": 100, "high": 105, "low": 95, "close": 102},
    {"time": 1609545600, "open": 102, "high": 107, "low": 99, "close": 104},
    {"time": 1609632000, "open": 104, "high": 109, "low": 101, "close": 106},
    {"time": 1609718400, "open": 106, "high": 111, "low": 103, "close": 108},
    {"time": 1609804800, "open": 108, "high": 113, "low": 105, "close": 110},
    {"time": 1609891200, "open": 110, "high": 115, "low": 107, "close": 112},
    {"time": 1609977600, "open": 112, "high": 117, "low": 109, "close": 114},
    {"time": 1610064000, "open": 114, "high": 119, "low": 111, "close": 116},
    {"time": 1610150400, "open": 116, "high": 121, "low": 113, "close": 118},
    {"time": 1610236800, "open": 118, "high": 123, "low": 115, "close": 120},
]

# 5-period moving average (calculated from close prices)
ma_data = [
    {"time": 1609804800, "value": 106},
    {"time": 1609891200, "value": 108},
    {"time": 1609977600, "value": 110},
    {"time": 1610064000, "value": 112},
    {"time": 1610150400, "value": 114},
    {"time": 1610236800, "value": 116},
]

# Create chart
chart = createChart({"width": 800, "height": 400})

# Add candlesticks
candles = chart.addSeries(
    CandlestickSeries,
    {
        "upColor": "#26a69a",
        "downColor": "#ef5350",
        "borderVisible": False,
        "wickUpColor": "#26a69a",
        "wickDownColor": "#ef5350",
    },
)
candles.setData(ohlc_data)

# Add moving average line
ma_line = chart.addSeries(
    LineSeries,
    {
        "color": "#2196F3",
        "lineWidth": 2,
    },
)
ma_line.setData(ma_data)

chart.show()
