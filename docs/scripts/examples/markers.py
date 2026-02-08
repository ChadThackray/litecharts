from litecharts import CandlestickSeries, createChart, createSeriesMarkers

# Create a chart with specific dimensions
chart = createChart({"width": 800, "height": 400})

# Add a candlestick series
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

# Set the data
candles.setData(
    [
        {"time": 1609459200, "open": 132.43, "high": 134.54, "low": 131.10, "close": 133.72},
        {"time": 1609545600, "open": 133.75, "high": 135.20, "low": 130.93, "close": 131.96},
        {"time": 1609632000, "open": 132.00, "high": 133.61, "low": 126.38, "close": 126.60},
        {"time": 1609718400, "open": 127.72, "high": 131.05, "low": 126.43, "close": 130.92},
        {"time": 1609804800, "open": 130.85, "high": 131.26, "low": 128.54, "close": 129.41},
        {"time": 1609891200, "open": 129.21, "high": 130.17, "low": 127.86, "close": 128.98},
        {"time": 1609977600, "open": 128.78, "high": 132.63, "low": 128.53, "close": 132.05},
        {"time": 1610064000, "open": 132.43, "high": 132.63, "low": 130.23, "close": 130.92},
        {"time": 1610150400, "open": 129.19, "high": 130.17, "low": 128.50, "close": 128.80},
        {"time": 1610236800, "open": 128.50, "high": 129.69, "low": 126.86, "close": 128.98},
        {"time": 1610323200, "open": 128.76, "high": 131.45, "low": 128.49, "close": 130.89},
        {"time": 1610409600, "open": 130.80, "high": 131.00, "low": 128.76, "close": 128.91},
        {"time": 1610496000, "open": 128.78, "high": 130.22, "low": 127.00, "close": 130.21},
        {"time": 1610582400, "open": 130.04, "high": 132.94, "low": 128.31, "close": 132.03},
        {"time": 1610668800, "open": 131.70, "high": 131.70, "low": 126.86, "close": 127.14},
    ]
)

# Add buy/sell markers
createSeriesMarkers(
    candles,
    [
        {"time": 1609459200, "position": "belowBar", "shape": "arrowUp", "color": "#26a69a", "text": "Buy"},
        {"time": 1609804800, "position": "aboveBar", "shape": "arrowDown", "color": "#ef5350", "text": "Sell"},
        {"time": 1610236800, "position": "belowBar", "shape": "arrowUp", "color": "#26a69a", "text": "Buy"},
        {"time": 1610582400, "position": "aboveBar", "shape": "arrowDown", "color": "#ef5350", "text": "Sell"},
    ],
)

# Fit all data into view
chart.fitContent()

# Display the chart
chart.show()
