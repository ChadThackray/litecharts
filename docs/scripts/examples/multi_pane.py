from litecharts import CandlestickSeries, HistogramSeries, createChart

# Sample OHLC data
ohlc_data = [
    {"time": 1609459200, "open": 100, "high": 105, "low": 95, "close": 102},
    {"time": 1609545600, "open": 102, "high": 110, "low": 100, "close": 108},
    {"time": 1609632000, "open": 108, "high": 115, "low": 105, "close": 112},
    {"time": 1609718400, "open": 112, "high": 118, "low": 108, "close": 115},
    {"time": 1609804800, "open": 115, "high": 120, "low": 112, "close": 118},
    {"time": 1609891200, "open": 118, "high": 122, "low": 115, "close": 120},
    {"time": 1609977600, "open": 120, "high": 125, "low": 118, "close": 122},
    {"time": 1610064000, "open": 122, "high": 128, "low": 120, "close": 126},
    {"time": 1610150400, "open": 126, "high": 130, "low": 123, "close": 128},
    {"time": 1610236800, "open": 128, "high": 132, "low": 125, "close": 130},
]

# Sample volume data
volume_data = [
    {"time": 1609459200, "value": 10000, "color": "#26a69a"},
    {"time": 1609545600, "value": 15000, "color": "#26a69a"},
    {"time": 1609632000, "value": 12000, "color": "#26a69a"},
    {"time": 1609718400, "value": 18000, "color": "#26a69a"},
    {"time": 1609804800, "value": 14000, "color": "#26a69a"},
    {"time": 1609891200, "value": 11000, "color": "#26a69a"},
    {"time": 1609977600, "value": 16000, "color": "#26a69a"},
    {"time": 1610064000, "value": 20000, "color": "#26a69a"},
    {"time": 1610150400, "value": 13000, "color": "#26a69a"},
    {"time": 1610236800, "value": 17000, "color": "#26a69a"},
]

# Create chart
chart = createChart({"width": 800, "height": 500})

# Main pane (75% height)
main_pane = chart.addPane({"stretchFactor": 3})
candles = main_pane.addSeries(
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

# Volume pane (25% height)
volume_pane = chart.addPane({"stretchFactor": 1})
volume = volume_pane.addSeries(
    HistogramSeries,
    {"priceFormat": {"type": "volume"}},
)
volume.setData(volume_data)

chart.show()
