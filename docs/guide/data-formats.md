# Data Formats

litecharts accepts multiple data formats for convenience.

## List of Dictionaries

The most explicit format, matching the Lightweight Charts API directly.

```python
candles.setData([
    {"time": 1609459200, "open": 100, "high": 105, "low": 95, "close": 102},
    {"time": 1609545600, "open": 102, "high": 110, "low": 100, "close": 108},
])
```

Time can be:
- Unix timestamp (seconds)
- ISO date string: `"2021-01-01"`
- Object: `{"year": 2021, "month": 1, "day": 1}`

## Pandas DataFrame

Pass a DataFrame directly. The index is used as the time axis.

```python
import pandas as pd

df = pd.DataFrame({
    "open": [100, 102],
    "high": [105, 110],
    "low": [95, 100],
    "close": [102, 108],
}, index=pd.to_datetime(["2021-01-01", "2021-01-02"]))

candles.setData(df)
```

For line/area series, use a `value` column or a single-column DataFrame.

## NumPy Array

For OHLC data, columns are: `[time, open, high, low, close]`

```python
import numpy as np

arr = np.array([
    [1609459200, 100, 105, 95, 102],
    [1609545600, 102, 110, 100, 108],
])

candles.setData(arr)
```

For line/area series, columns are: `[time, value]`
