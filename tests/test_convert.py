"""Tests for convert.py module."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from litecharts.convert import (
    convert_options_to_js,
    to_camel_case,
    to_lwc_ohlc_data,
    to_lwc_single_value_data,
    to_unix_timestamp,
)

from .conftest import DataMapping


class TestToUnixTimestamp:
    """Tests for to_unix_timestamp function."""

    def test_int_passthrough(self) -> None:
        """Integer timestamps are returned as-is."""
        assert to_unix_timestamp(1609459200) == 1609459200

    def test_float_truncated(self) -> None:
        """Float timestamps are truncated to int."""
        assert to_unix_timestamp(1609459200.999) == 1609459200

    def test_iso_string_utc(self) -> None:
        """ISO strings with Z suffix are parsed as UTC."""
        result = to_unix_timestamp("2021-01-01T00:00:00Z")
        assert result == 1609459200

    def test_iso_string_with_offset(self) -> None:
        """ISO strings with timezone offset are parsed correctly."""
        result = to_unix_timestamp("2021-01-01T01:00:00+01:00")
        assert result == 1609459200

    def test_datetime_naive_assumed_utc(self) -> None:
        """Naive datetime objects are treated as UTC."""
        dt = datetime(2021, 1, 1, 0, 0, 0)
        result = to_unix_timestamp(dt)
        assert result == 1609459200

    def test_datetime_aware(self) -> None:
        """Aware datetime objects are converted correctly."""
        dt = datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        result = to_unix_timestamp(dt)
        assert result == 1609459200

    def test_unsupported_type_raises(self) -> None:
        """Unsupported types raise TypeError."""
        with pytest.raises(TypeError, match="Unsupported time type"):
            to_unix_timestamp([1, 2, 3])  # type: ignore[arg-type]


class TestToCamelCase:
    """Tests for to_camel_case function."""

    def test_single_word(self) -> None:
        """Single words are unchanged."""
        assert to_camel_case("color") == "color"

    def test_two_words(self) -> None:
        """Two word snake_case is converted."""
        assert to_camel_case("background_color") == "backgroundColor"

    def test_multiple_words(self) -> None:
        """Multiple word snake_case is converted."""
        assert to_camel_case("this_is_a_test") == "thisIsATest"

    def test_already_camel(self) -> None:
        """Already camelCase strings pass through."""
        assert to_camel_case("backgroundColor") == "backgroundColor"


class TestConvertOptionsToJs:
    """Tests for convert_options_to_js function."""

    def test_flat_dict(self) -> None:
        """Flat dicts have keys converted."""
        options = {"background_color": "#000", "line_width": 2}
        result = convert_options_to_js(options)
        assert result == {"backgroundColor": "#000", "lineWidth": 2}

    def test_nested_dict(self) -> None:
        """Nested dicts are recursively converted."""
        options = {
            "time_scale": {
                "right_offset": 5,
                "bar_spacing": 10,
            }
        }
        result = convert_options_to_js(options)
        assert result == {
            "timeScale": {
                "rightOffset": 5,
                "barSpacing": 10,
            }
        }

    def test_non_dict_values_unchanged(self) -> None:
        """Non-dict values are preserved."""
        options = {"values": [1, 2, 3], "name": "test"}
        result = convert_options_to_js(options)
        assert result == {"values": [1, 2, 3], "name": "test"}


class TestToLwcOhlcData:
    """Tests for to_lwc_ohlc_data function."""

    def test_list_of_dicts(self, sample_ohlc_dicts: list[DataMapping]) -> None:
        """List of dicts is normalized."""
        result = to_lwc_ohlc_data(sample_ohlc_dicts)
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
        result = to_lwc_ohlc_data(data)
        assert result[0]["time"] == 1609459200


class TestToLwcSingleValueData:
    """Tests for to_lwc_single_value_data function."""

    def test_list_of_dicts(self, sample_single_value_dicts: list[DataMapping]) -> None:
        """List of dicts is normalized."""
        result = to_lwc_single_value_data(sample_single_value_dicts)
        assert len(result) == 3
        assert result[0]["time"] == 1609459200
        assert result[0].get("value") == 100.0

    def test_list_of_dicts_with_string_time(self) -> None:
        """String times in dicts are converted."""
        data: list[DataMapping] = [{"time": "2021-01-01T00:00:00Z", "value": 100.0}]
        result = to_lwc_single_value_data(data)
        assert result[0]["time"] == 1609459200
