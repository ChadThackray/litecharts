"""Data conversion utilities for litecharts."""

from __future__ import annotations

import calendar
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from .types import DataValue, OhlcData, SingleValueData

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd


def toUnixTimestamp(timeValue: int | float | str | datetime) -> int:
    """Convert various time formats to UTC Unix timestamp (seconds).

    Args:
        timeValue: Time value as int (passthrough), float, ISO string, or datetime.

    Returns:
        Unix timestamp in seconds (UTC).

    Raises:
        TypeError: If timeValue type is not supported.
    """
    if isinstance(timeValue, int):
        return timeValue

    if isinstance(timeValue, float):
        return int(timeValue)

    if isinstance(timeValue, str):
        dt = datetime.fromisoformat(timeValue.replace("Z", "+00:00"))
        return int(calendar.timegm(dt.utctimetuple()))

    if isinstance(timeValue, datetime):
        if timeValue.tzinfo is None:
            timeValue = timeValue.replace(tzinfo=timezone.utc)
        return int(calendar.timegm(timeValue.utctimetuple()))

    # Check for pandas Timestamp via duck typing
    if hasattr(timeValue, "timestamp"):
        return int(timeValue.timestamp())

    msg = f"Unsupported time type: {type(timeValue).__name__}"
    raise TypeError(msg)


def _normalizeOhlcColumns(columns: Sequence[str]) -> dict[str, str]:
    """Create mapping from lowercase column names to actual column names.

    Args:
        columns: Sequence of column names.

    Returns:
        Mapping from standard names to actual column names.
    """
    columnMap: dict[str, str] = {}
    standardNames = {"time", "open", "high", "low", "close", "volume", "value"}

    for col in columns:
        lower = col.lower()
        if lower in standardNames:
            columnMap[lower] = col

    return columnMap


def _convertDataframeToOhlc(df: pd.DataFrame) -> list[OhlcData | SingleValueData]:
    """Convert a pandas DataFrame to OHLC data format.

    Args:
        df: pandas DataFrame with OHLC columns.

    Returns:
        List of dicts with time, open, high, low, close.
    """
    columns = list(df.columns)
    colMap = _normalizeOhlcColumns(columns)

    result: list[OhlcData | SingleValueData] = []

    # Check if index is datetime-like
    index = df.index
    hasDatetimeIndex = hasattr(index, "to_pydatetime") or hasattr(index, "asi8")

    for i, row in enumerate(df.itertuples(index=True)):
        data: OhlcData = {}

        # Handle time from index or column
        if "time" in colMap:
            data["time"] = toUnixTimestamp(getattr(row, colMap["time"]))
        elif hasDatetimeIndex:
            idxVal = index[i]
            data["time"] = toUnixTimestamp(idxVal)
        else:
            msg = "DataFrame must have a 'time' column or datetime index"
            raise ValueError(msg)

        # Map OHLC columns
        for stdName in ("open", "high", "low", "close"):
            if stdName in colMap:
                data[stdName] = float(getattr(row, colMap[stdName]))

        # Optional volume
        if "volume" in colMap:
            data["volume"] = float(getattr(row, colMap["volume"]))

        result.append(data)

    return result


def _convertDataframeToSingleValue(
    df: pd.DataFrame | pd.Series[float],
) -> list[OhlcData | SingleValueData]:
    """Convert a pandas DataFrame/Series to single-value data format.

    Args:
        df: pandas DataFrame or Series with value data.

    Returns:
        List of dicts with time and value.
    """
    result: list[OhlcData | SingleValueData] = []
    index = df.index
    hasDatetimeIndex = hasattr(index, "to_pydatetime") or hasattr(index, "asi8")

    # Check if this is a Series-like object
    if hasattr(df, "items") and not hasattr(df, "columns"):
        # It's a Series
        assert isinstance(df, pd.Series)
        for idxVal, value in df.items():
            itemData: SingleValueData = {"value": float(value)}
            if hasDatetimeIndex:
                itemData["time"] = toUnixTimestamp(idxVal)  # type: ignore[arg-type]
            else:
                itemData["time"] = int(idxVal)  # type: ignore[call-overload]
            result.append(itemData)
        return result

    # It's a DataFrame
    assert isinstance(df, pd.DataFrame)
    columns = list(df.columns)
    colMap = _normalizeOhlcColumns(columns)

    for i, row in enumerate(df.itertuples(index=True)):
        data: SingleValueData = {}

        # Handle time
        if "time" in colMap:
            data["time"] = toUnixTimestamp(getattr(row, colMap["time"]))
        elif hasDatetimeIndex:
            idxVal = index[i]
            data["time"] = toUnixTimestamp(idxVal)
        else:
            msg = "DataFrame must have a 'time' column or datetime index"
            raise ValueError(msg)

        # Get value column
        if "value" in colMap:
            data["value"] = float(getattr(row, colMap["value"]))
        elif len(columns) == 1 or (len(columns) == 2 and "time" in colMap):
            # Single column (besides time) - use it as value
            for col in columns:
                if col.lower() != "time":
                    data["value"] = float(getattr(row, col))
                    break
        else:
            msg = "Cannot determine value column"
            raise ValueError(msg)

        result.append(data)

    return result


def _convertNumpyToOhlc(
    arr: np.ndarray[Any, Any],
) -> list[OhlcData | SingleValueData]:
    """Convert a numpy array to OHLC data format.

    Expects array with shape (n, 5) for [time, open, high, low, close]
    or (n, 6) for [time, open, high, low, close, volume].

    Args:
        arr: numpy array.

    Returns:
        List of dicts with OHLC data.
    """
    arrayList = arr.tolist()
    result: list[OhlcData | SingleValueData] = []

    for row in arrayList:
        if len(row) >= 5:
            data: OhlcData = {
                "time": toUnixTimestamp(row[0]),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
            }
            if len(row) >= 6:
                data["volume"] = float(row[5])
            result.append(data)
        elif len(row) == 2:
            result.append(
                SingleValueData(
                    time=toUnixTimestamp(row[0]),
                    value=float(row[1]),
                )
            )
        else:
            msg = f"Unexpected array row length: {len(row)}"
            raise ValueError(msg)

    return result


def _convertListOfDicts(
    data: list[Mapping[str, DataValue]],
) -> list[OhlcData | SingleValueData]:
    """Convert a list of dicts, normalizing time values.

    Args:
        data: List of dicts with time and value/OHLC data.

    Returns:
        List of dicts with normalized time values.
    """
    result: list[OhlcData | SingleValueData] = []

    for item in data:
        normalized: OhlcData | SingleValueData = dict(item)  # type: ignore[assignment]
        if "time" in normalized:
            normalized["time"] = toUnixTimestamp(normalized["time"])
        result.append(normalized)

    return result


def toLwcOhlcData(
    data: pd.DataFrame | np.ndarray[Any, Any] | list[Mapping[str, DataValue]],
) -> list[OhlcData | SingleValueData]:
    """Convert various data formats to LWC OHLC data format.

    Args:
        data: Data as list of dicts, pandas DataFrame, or numpy array.

    Returns:
        List of dicts with time, open, high, low, close.
    """
    if isinstance(data, list):
        return _convertListOfDicts(data)

    # pandas DataFrame (check before numpy since DataFrame has shape too)
    if hasattr(data, "itertuples") and hasattr(data, "columns"):
        return _convertDataframeToOhlc(data)  # type: ignore[arg-type]

    # numpy array
    return _convertNumpyToOhlc(data)


def toLwcSingleValueData(
    data: pd.DataFrame
    | pd.Series[float]
    | np.ndarray[Any, Any]
    | list[Mapping[str, DataValue]],
) -> list[OhlcData | SingleValueData]:
    """Convert various data formats to LWC single-value data format.

    Args:
        data: Data as list of dicts, pandas DataFrame/Series, or numpy array.

    Returns:
        List of dicts with time and value.
    """
    if isinstance(data, list):
        return _convertListOfDicts(data)

    # pandas Series or DataFrame
    if hasattr(data, "index") and (hasattr(data, "columns") or hasattr(data, "items")):
        return _convertDataframeToSingleValue(data)  # type: ignore[arg-type]

    # numpy array
    return _convertNumpyToOhlc(data)
