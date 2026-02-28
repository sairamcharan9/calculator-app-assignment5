"""
Tests for the Input Validators Module
=======================================

Parameterized tests for LBYL validation helpers.
"""

import pytest
from decimal import Decimal

from app.input_validators import validate_input_parts, validate_numeric


# ---------------------------------------------------------------------------
# validate_input_parts
# ---------------------------------------------------------------------------


class TestValidateInputParts:
    """Tests for validate_input_parts."""

    @pytest.mark.parametrize(
        "parts",
        [
            ["add", "5", "3"],
            ["subtract", "10", "4"],
            ["multiply", "6", "7"],
            ["divide", "20", "4"],
            ["power", "2", "8"],
            ["root", "9", "2"],
            ["sqrt", "9"],
        ],
        ids=["add", "subtract", "multiply", "divide", "power", "root", "sqrt"],
    )
    def test_valid_input(self, parts: list[str]) -> None:
        """Valid three-token input with known operation returns None."""
        assert validate_input_parts(parts) is None

    @pytest.mark.parametrize(
        "parts",
        [
            ["add"],
            ["add", "5"],
            ["add", "5", "3", "2"],
            [],
            ["sqrt"],
            ["sqrt", "9", "3"],
        ],
        ids=["one_token", "two_tokens", "four_tokens", "empty", "sqrt_no_args", "sqrt_too_many_args"],
    )
    def test_wrong_token_count(self, parts: list[str]) -> None:
        """Incorrect number of tokens returns an error."""
        result = validate_input_parts(parts)
        assert result is not None
        assert "Invalid format" in result

    @pytest.mark.parametrize(
        "parts",
        [
            ["modulo", "5", "3"],
            ["unknown", "1", "2"],
        ],
        ids=["modulo", "unknown"],
    )
    def test_unknown_operation(self, parts: list[str]) -> None:
        """Unknown operation name returns an error."""
        result = validate_input_parts(parts)
        assert result is not None
        assert "Unknown operation" in result


# ---------------------------------------------------------------------------
# validate_numeric
# ---------------------------------------------------------------------------


class TestValidateNumeric:
    """Tests for validate_numeric."""

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("5", Decimal("5")),
            ("-3.14", Decimal("-3.14")),
            ("0", Decimal("0")),
            ("1E+2", Decimal("1E+2")),
        ],
        ids=["integer", "negative_decimal", "zero", "scientific"],
    )
    def test_valid_numbers(self, value: str, expected: Decimal) -> None:
        """Valid numeric strings convert to Decimal."""
        assert validate_numeric(value) == expected

    @pytest.mark.parametrize(
        "value",
        ["abc", "", "12.34.56", "hello"],
        ids=["letters", "empty", "double_dot", "word"],
    )
    def test_invalid_numbers(self, value: str) -> None:
        """Invalid numeric strings return None."""
        assert validate_numeric(value) is None
