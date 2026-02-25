"""Shared test configuration and fixtures."""

import pytest
from decimal import Decimal

from app.calculation import Calculation
from app.operations import add, subtract, multiply, divide


@pytest.fixture
def sample_add_calc() -> Calculation:
    """Provide a sample addition Calculation."""
    return Calculation(Decimal("5"), Decimal("3"), add, "add")


@pytest.fixture
def sample_subtract_calc() -> Calculation:
    """Provide a sample subtraction Calculation."""
    return Calculation(Decimal("10"), Decimal("4"), subtract, "subtract")
