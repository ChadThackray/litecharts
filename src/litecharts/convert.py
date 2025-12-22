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


def to_unix_timestamp(time_value: int | float | str | datetime) -> int:
    """Convert various time formats to UTC Unix timestamp (seconds).

    Args:
        time_value: Time value as int (passthrough), float, ISO string, or datetime.

    Returns:
        Unix timestamp in seconds (UTC).

    Raises:
        TypeError: If time_value type is not supported.
    """
    if isinstance(time_value, int):
        return time_value

    if isinstance(time_value, float):
        return int(time_value)

    if isinstance(time_value, str):
        dt = datetime.fromisoformat(time_value.replace("Z", "+00:00"))
        return int(calendar.timegm(dt.utctimetuple()))

    if isinstance(time_value, datetime):
        if time_value.tzinfo is None:
            time_value = time_value.replace(tzinfo=timezone.utc)
        return int(calendar.timegm(time_value.utctimetuple()))

    # Check for pandas Timestamp via duck typing
    if hasattr(time_value, "timestamp"):
        return int(time_value.timestamp())

    msg = f"Unsupported time type: {type(time_value).__name__}"
    raise TypeError(msg)


def _normalize_ohlc_columns(columns: Sequence[str]) -> dict[str, str]:
    """Create mapping from lowercase column names to actual column names.

    Args:
        columns: Sequence of column names.

    Returns:
        Mapping from standard names to actual column names.
    """
    column_map: dict[str, str] = {}
    standard_names = {"time", "open", "high", "low", "close", "volume", "value"}

    for col in columns:
        lower = col.lower()
        if lower in standard_names:
            column_map[lower] = col

    return column_map


def _convert_dataframe_to_ohlc(df: pd.DataFrame) -> list[OhlcData | SingleValueData]:
    """Convert a pandas DataFrame to OHLC data format.

    Args:
        df: pandas DataFrame with OHLC columns.

    Returns:
        List of dicts with time, open, high, low, close.
    """
    columns = list(df.columns)
    col_map = _normalize_ohlc_columns(columns)

    result: list[OhlcData | SingleValueData] = []

    # Check if index is datetime-like
    index = df.index
    has_datetime_index = hasattr(index, "to_pydatetime") or hasattr(index, "asi8")

    for i, row in enumerate(df.itertuples(index=True)):
        data: OhlcData = {}

        # Handle time from index or column
        if "time" in col_map:
            data["time"] = to_unix_timestamp(getattr(row, col_map["time"]))
        elif has_datetime_index:
            idx_val = index[i]
            data["time"] = to_unix_timestamp(idx_val)
        else:
            msg = "DataFrame must have a 'time' column or datetime index"
            raise ValueError(msg)

        # Map OHLC columns
        for std_name in ("open", "high", "low", "close"):
            if std_name in col_map:
                data[std_name] = float(getattr(row, col_map[std_name]))

        # Optional volume
        if "volume" in col_map:
            data["volume"] = float(getattr(row, col_map["volume"]))

        result.append(data)

    return result


def _convert_dataframe_to_single_value(
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
    has_datetime_index = hasattr(index, "to_pydatetime") or hasattr(index, "asi8")

    # Check if this is a Series-like object
    if hasattr(df, "items") and not hasattr(df, "columns"):
        # It's a Series
        assert isinstance(df, pd.Series)
        for idx_val, value in df.items():
            item_data: SingleValueData = {"value": float(value)}
            if has_datetime_index:
                item_data["time"] = to_unix_timestamp(idx_val)  # type: ignore[arg-type]
            else:
                item_data["time"] = int(idx_val)  # type: ignore[call-overload]
            result.append(item_data)
        return result

    # It's a DataFrame
    assert isinstance(df, pd.DataFrame)
    columns = list(df.columns)
    col_map = _normalize_ohlc_columns(columns)

    for i, row in enumerate(df.itertuples(index=True)):
        data: SingleValueData = {}

        # Handle time
        if "time" in col_map:
            data["time"] = to_unix_timestamp(getattr(row, col_map["time"]))
        elif has_datetime_index:
            idx_val = index[i]
            data["time"] = to_unix_timestamp(idx_val)
        else:
            msg = "DataFrame must have a 'time' column or datetime index"
            raise ValueError(msg)

        # Get value column
        if "value" in col_map:
            data["value"] = float(getattr(row, col_map["value"]))
        elif len(columns) == 1 or (len(columns) == 2 and "time" in col_map):
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


def _convert_numpy_to_ohlc(
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
    array_list = arr.tolist()
    result: list[OhlcData | SingleValueData] = []

    for row in array_list:
        if len(row) >= 5:
            data: OhlcData = {
                "time": to_unix_timestamp(row[0]),
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
                    time=to_unix_timestamp(row[0]),
                    value=float(row[1]),
                )
            )
        else:
            msg = f"Unexpected array row length: {len(row)}"
            raise ValueError(msg)

    return result


def _convert_list_of_dicts(
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
            normalized["time"] = to_unix_timestamp(normalized["time"])
        result.append(normalized)

    return result


def to_lwc_ohlc_data(
    data: pd.DataFrame | np.ndarray[Any, Any] | list[Mapping[str, DataValue]],
) -> list[OhlcData | SingleValueData]:
    """Convert various data formats to LWC OHLC data format.

    Args:
        data: Data as list of dicts, pandas DataFrame, or numpy array.

    Returns:
        List of dicts with time, open, high, low, close.
    """
    if isinstance(data, list):
        return _convert_list_of_dicts(data)

    # pandas DataFrame (check before numpy since DataFrame has shape too)
    if hasattr(data, "itertuples") and hasattr(data, "columns"):
        return _convert_dataframe_to_ohlc(data)  # type: ignore[arg-type]

    # numpy array
    return _convert_numpy_to_ohlc(data)


def to_lwc_single_value_data(
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
        return _convert_list_of_dicts(data)

    # pandas Series or DataFrame
    if hasattr(data, "index") and (hasattr(data, "columns") or hasattr(data, "items")):
        return _convert_dataframe_to_single_value(data)  # type: ignore[arg-type]

    # numpy array
    return _convert_numpy_to_ohlc(data)


def to_camel_case(name: str) -> str:
    """Convert snake_case to camelCase.

    Args:
        name: Snake case string.

    Returns:
        Camel case string.
    """
    parts = name.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


def convert_options_to_js(options: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively convert option keys from snake_case to camelCase.

    Args:
        options: Dict with snake_case keys (typically a TypedDict).

    Returns:
        Dict with camelCase keys.
    """
    result: dict[str, Any] = {}

    for key, value in options.items():
        camel_key = to_camel_case(key)

        if isinstance(value, dict):
            result[camel_key] = convert_options_to_js(value)
        else:
            result[camel_key] = value

    return result


def convert_options_to_js_list(
    items: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Convert a list of dicts with snake_case keys to camelCase.

    Args:
        items: List of dicts.

    Returns:
        List of dicts with camelCase keys.
    """
    return [convert_options_to_js(item) for item in items]
