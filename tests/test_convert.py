"""Tests for convert.py module."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from litecharts.convert import (
    toLwcOhlcData,
    toLwcSingleValueData,
    toUnixTimestamp,
)

from .conftest import DataMapping


class TestToUnixTimestamp:
    """Tests for toUnixTimestamp function."""

    def test_int_passthrough(self) -> None:
        """Integer timestamps are returned as-is."""
        assert toUnixTimestamp(1609459200) == 1609459200

    def test_float_truncated(self) -> None:
        """Float timestamps are truncated to int."""
        assert toUnixTimestamp(1609459200.999) == 1609459200

    def test_iso_string_utc(self) -> None:
        """ISO strings with Z suffix are parsed as UTC."""
        result = toUnixTimestamp("2021-01-01T00:00:00Z")
        assert result == 1609459200

    def test_iso_string_with_offset(self) -> None:
        """ISO strings with timezone offset are parsed correctly."""
        result = toUnixTimestamp("2021-01-01T01:00:00+01:00")
        assert result == 1609459200

    def test_datetime_naive_assumed_utc(self) -> None:
        """Naive datetime objects are treated as UTC."""
        dt = datetime(2021, 1, 1, 0, 0, 0)
        result = toUnixTimestamp(dt)
        assert result == 1609459200

    def test_datetime_aware(self) -> None:
        """Aware datetime objects are converted correctly."""
        dt = datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        result = toUnixTimestamp(dt)
        assert result == 1609459200

    def test_unsupported_type_raises(self) -> None:
        """Unsupported types raise TypeError."""
        with pytest.raises(TypeError, match="Unsupported time type"):
            toUnixTimestamp([1, 2, 3])  # type: ignore[arg-type]


class TestToLwcOhlcData:
    """Tests for toLwcOhlcData function."""

    def test_list_of_dicts(self, sample_ohlc_dicts: list[DataMapping]) -> None:
        """List of dicts is normalized."""
        result = toLwcOhlcData(sample_ohlc_dicts)
        assert len(result) == 3
        assert result[0]["time"] == 1609459200
        assert result[0].get("open") == 100.0

    def test_list_of_dicts_with_string_time(self) -> None:
        """String times in dicts are converted."""
        data: list[DataMapping] = [
            {
                "time": "2021-01-01T00:00:00Z",
                "open": 100.0,
                "high": 110.0,
                "low": 95.0,
                "close": 105.0,
            }
        ]
        result = toLwcOhlcData(data)
        assert result[0]["time"] == 1609459200


class TestToLwcSingleValueData:
    """Tests for toLwcSingleValueData function."""

    def test_list_of_dicts(self, sample_single_value_dicts: list[DataMapping]) -> None:
        """List of dicts is normalized."""
        result = toLwcSingleValueData(sample_single_value_dicts)
        assert len(result) == 3
        assert result[0]["time"] == 1609459200
        assert result[0].get("value") == 100.0

    def test_list_of_dicts_with_string_time(self) -> None:
        """String times in dicts are converted."""
        data: list[DataMapping] = [{"time": "2021-01-01T00:00:00Z", "value": 100.0}]
        result = toLwcSingleValueData(data)
        assert result[0]["time"] == 1609459200
