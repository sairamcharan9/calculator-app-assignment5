"""
Tests for the Exceptions Module
================================

Verifies the exception hierarchy: all custom exceptions inherit from
``CalculationError``, which inherits from ``Exception``.
"""

import pytest

from app.exceptions import (
    CalculationError,
    ConfigurationError,
    DivisionByZeroError,
    InvalidInputError,
    InvalidOperationError,
)


# ---------------------------------------------------------------------------
# Hierarchy checks
# ---------------------------------------------------------------------------


class TestExceptionHierarchy:
    """Verify that all custom exceptions belong to the correct hierarchy."""

    @pytest.mark.parametrize(
        "exc_class",
        [
            InvalidOperationError,
            InvalidInputError,
            DivisionByZeroError,
            ConfigurationError,
        ],
        ids=[
            "InvalidOperationError",
            "InvalidInputError",
            "DivisionByZeroError",
            "ConfigurationError",
        ],
    )
    def test_subclass_of_calculation_error(self, exc_class: type) -> None:
        """Each custom exception should be a subclass of CalculationError."""
        assert issubclass(exc_class, CalculationError)

    def test_calculation_error_is_exception(self) -> None:
        """CalculationError itself should be a subclass of Exception."""
        assert issubclass(CalculationError, Exception)


# ---------------------------------------------------------------------------
# Raising and catching
# ---------------------------------------------------------------------------


class TestExceptionRaising:
    """Verify that each exception can be raised and caught with a message."""

    @pytest.mark.parametrize(
        "exc_class, message",
        [
            (CalculationError, "base error"),
            (InvalidOperationError, "unknown op"),
            (InvalidInputError, "bad input"),
            (DivisionByZeroError, "div by zero"),
            (ConfigurationError, "bad config"),
        ],
        ids=[
            "CalculationError",
            "InvalidOperationError",
            "InvalidInputError",
            "DivisionByZeroError",
            "ConfigurationError",
        ],
    )
    def test_raise_with_message(self, exc_class: type, message: str) -> None:
        """Each exception stores its message correctly."""
        with pytest.raises(exc_class, match=message):
            raise exc_class(message)
