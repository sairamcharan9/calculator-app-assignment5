"""
Tests for the Operations Module
================================

Parameterized tests covering all six arithmetic operations:
add, subtract, multiply, divide, power, root — including edge cases
(zero, negative numbers, decimals, large numbers, division by zero,
root by zero).

Also tests the strategy registry helpers ``get_operation`` and
``get_supported_operations``.
"""

import pytest
from decimal import Decimal

from app.exceptions import DivisionByZeroError, InvalidOperationError
from app.operations import (
    add,
    subtract,
    multiply,
    divide,
    power,
    root,
    get_operation,
    get_supported_operations,
    OPERATIONS,
)


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("2"), Decimal("3"), Decimal("5")),
        (Decimal("0"), Decimal("0"), Decimal("0")),
        (Decimal("-1"), Decimal("1"), Decimal("0")),
        (Decimal("-5"), Decimal("-3"), Decimal("-8")),
        (Decimal("1.5"), Decimal("2.5"), Decimal("4.0")),
        (Decimal("999999999"), Decimal("1"), Decimal("1000000000")),
        (Decimal("0.1"), Decimal("0.2"), Decimal("0.3")),
    ],
    ids=[
        "pos+pos",
        "zero+zero",
        "neg+pos",
        "neg+neg",
        "dec+dec",
        "large_boundary",
        "small_dec",
    ],
)
def test_add(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test addition with various inputs."""
    assert add(a, b) == expected


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("5"), Decimal("3"), Decimal("2")),
        (Decimal("0"), Decimal("0"), Decimal("0")),
        (Decimal("-1"), Decimal("-1"), Decimal("0")),
        (Decimal("3"), Decimal("5"), Decimal("-2")),
        (Decimal("10.5"), Decimal("0.5"), Decimal("10.0")),
    ],
    ids=["pos-pos", "zero-zero", "neg-neg", "result_neg", "dec_sub"],
)
def test_subtract(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test subtraction with various inputs."""
    assert subtract(a, b) == expected


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("4"), Decimal("3"), Decimal("12")),
        (Decimal("0"), Decimal("100"), Decimal("0")),
        (Decimal("-2"), Decimal("3"), Decimal("-6")),
        (Decimal("-3"), Decimal("-4"), Decimal("12")),
        (Decimal("1.5"), Decimal("2"), Decimal("3.0")),
    ],
    ids=["pos*pos", "zero_factor", "neg*pos", "neg*neg", "dec*int"],
)
def test_multiply(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test multiplication with various inputs."""
    assert multiply(a, b) == expected


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("10"), Decimal("2"), Decimal("5")),
        (Decimal("7"), Decimal("2"), Decimal("3.5")),
        (Decimal("0"), Decimal("5"), Decimal("0")),
        (Decimal("-10"), Decimal("2"), Decimal("-5")),
        (Decimal("-10"), Decimal("-2"), Decimal("5")),
    ],
    ids=["even", "decimal_result", "zero_dividend", "neg_dividend", "both_neg"],
)
def test_divide(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test division with various inputs."""
    assert divide(a, b) == expected


def test_divide_by_zero() -> None:
    """Test that dividing by zero raises DivisionByZeroError."""
    with pytest.raises(DivisionByZeroError):
        divide(Decimal("10"), Decimal("0"))


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("2"), Decimal("8"), Decimal("256")),
        (Decimal("5"), Decimal("0"), Decimal("1")),
        (Decimal("10"), Decimal("1"), Decimal("10")),
        (Decimal("3"), Decimal("3"), Decimal("27")),
    ],
    ids=["2^8", "n^0", "n^1", "3^3"],
)
def test_power(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test power with various inputs."""
    assert power(a, b) == expected


# ---------------------------------------------------------------------------
# root
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("9"), Decimal("2"), Decimal("3")),
        (Decimal("27"), Decimal("3"), Decimal("3")),
        (Decimal("1"), Decimal("5"), Decimal("1")),
    ],
    ids=["sqrt_9", "cbrt_27", "root_1"],
)
def test_root(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test root with various inputs."""
    assert root(a, b) == expected


def test_root_by_zero() -> None:
    """Test that root with degree zero raises DivisionByZeroError."""
    with pytest.raises(DivisionByZeroError):
        root(Decimal("9"), Decimal("0"))


# ---------------------------------------------------------------------------
# Strategy registry helpers
# ---------------------------------------------------------------------------


class TestStrategyRegistry:
    """Tests for the operation lookup and listing helpers."""

    @pytest.mark.parametrize(
        "name",
        ["add", "subtract", "multiply", "divide", "power", "root"],
        ids=["add", "subtract", "multiply", "divide", "power", "root"],
    )
    def test_get_operation_valid(self, name: str) -> None:
        """Known names return a callable."""
        func = get_operation(name)
        assert callable(func)

    def test_get_operation_invalid(self) -> None:
        """Unknown names raise InvalidOperationError."""
        with pytest.raises(InvalidOperationError, match="Unknown operation"):
            get_operation("modulo")

    def test_get_supported_operations(self) -> None:
        """All six operations are returned."""
        ops = get_supported_operations()
        assert set(ops) == {"add", "subtract", "multiply", "divide", "power", "root"}

    def test_operations_dict(self) -> None:
        """OPERATIONS dict contains all expected keys."""
        assert len(OPERATIONS) == 6
