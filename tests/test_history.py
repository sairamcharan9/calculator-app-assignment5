"""
Tests for the History Module
==============================

Tests for CalculationHistory (pandas-backed), observer notifications,
LoggingObserver, CSV save/load, and DataFrame get/set.
"""

import os
import pytest
import pandas as pd
from decimal import Decimal
from unittest.mock import MagicMock

from app.calculation import Calculation
from app.operations import add, subtract
from app.history import (
    CalculationHistory,
    CalculationObserver,
    LoggingObserver,
    AutoSaveObserver,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def history(tmp_path) -> CalculationHistory:
    """Provide a fresh CalculationHistory using a temp CSV path."""
    return CalculationHistory(csv_path=str(tmp_path / "test_history.csv"))


@pytest.fixture
def sample_calc() -> Calculation:
    """Provide a sample add calculation."""
    return Calculation(Decimal("2"), Decimal("3"), add, "add")


@pytest.fixture
def sample_calc2() -> Calculation:
    """Provide a sample subtract calculation."""
    return Calculation(Decimal("10"), Decimal("4"), subtract, "subtract")


# ---------------------------------------------------------------------------
# CalculationHistory basic operations
# ---------------------------------------------------------------------------


class TestCalculationHistoryBasics:
    """Test add, get_all, clear, len, repr."""

    def test_empty_history(self, history: CalculationHistory) -> None:
        """New history is empty."""
        assert len(history) == 0
        assert history.get_all() == []

    def test_add_and_get_all(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """Adding a calculation appears in get_all."""
        history.add(sample_calc)
        rows = history.get_all()
        assert len(rows) == 1
        assert rows[0]["operation"] == "add"

    def test_multiple_adds(
        self, history: CalculationHistory, sample_calc, sample_calc2
    ) -> None:
        """Multiple additions are stored in order."""
        history.add(sample_calc)
        history.add(sample_calc2)
        assert len(history) == 2

    def test_clear(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """Clearing removes all rows."""
        history.add(sample_calc)
        history.clear()
        assert len(history) == 0

    def test_repr(self, history: CalculationHistory) -> None:
        """Repr shows count."""
        assert "0 calculations" in repr(history)


# ---------------------------------------------------------------------------
# DataFrame get / set
# ---------------------------------------------------------------------------


class TestDataFrame:
    """Test get_dataframe and set_dataframe."""

    def test_get_dataframe(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """get_dataframe returns a copy."""
        history.add(sample_calc)
        df = history.get_dataframe()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1

    def test_set_dataframe(self, history: CalculationHistory) -> None:
        """set_dataframe replaces the internal DataFrame."""
        new_df = pd.DataFrame(
            [{"operand_a": "1", "operand_b": "2", "operation": "add", "result": "3"}]
        )
        history.set_dataframe(new_df)
        assert len(history) == 1


# ---------------------------------------------------------------------------
# Observer pattern
# ---------------------------------------------------------------------------


class TestObserverPattern:
    """Test observer registration and notification."""

    def test_add_and_notify_observer(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """Observer's on_calculation is called when a calc is added."""
        mock_observer = MagicMock(spec=CalculationObserver)
        history.add_observer(mock_observer)
        history.add(sample_calc)
        mock_observer.on_calculation.assert_called_once_with(sample_calc)

    def test_remove_observer(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """Removed observer is no longer notified."""
        mock_observer = MagicMock(spec=CalculationObserver)
        history.add_observer(mock_observer)
        history.remove_observer(mock_observer)
        history.add(sample_calc)
        mock_observer.on_calculation.assert_not_called()


# ---------------------------------------------------------------------------
# LoggingObserver
# ---------------------------------------------------------------------------


class TestLoggingObserver:
    """Tests for LoggingObserver."""

    def test_logs_calculation(self, sample_calc: Calculation) -> None:
        """Calculation is logged to internal list."""
        observer = LoggingObserver()
        observer.on_calculation(sample_calc)
        assert len(observer.log_messages) == 1
        assert "[LOG]" in observer.log_messages[0]

    def test_integration_with_history(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """LoggingObserver is notified through history.add."""
        observer = LoggingObserver()
        history.add_observer(observer)
        history.add(sample_calc)
        assert len(observer.log_messages) == 1


# ---------------------------------------------------------------------------
# CSV persistence
# ---------------------------------------------------------------------------


class TestCSVPersistence:
    """Tests for save_to_csv and load_from_csv."""

    def test_save_and_load(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """Saving and loading preserves data."""
        history.add(sample_calc)
        history.save_to_csv()

        new_history = CalculationHistory(csv_path=history.csv_path)
        count = new_history.load_from_csv()
        assert count == 1
        assert len(new_history) == 1

    def test_save_custom_path(
        self, history: CalculationHistory, sample_calc: Calculation, tmp_path
    ) -> None:
        """save_to_csv with explicit path override."""
        history.add(sample_calc)
        custom = str(tmp_path / "custom.csv")
        returned = history.save_to_csv(custom)
        assert returned == custom
        assert os.path.exists(custom)

    def test_load_nonexistent_file(self, history: CalculationHistory) -> None:
        """Loading from a nonexistent file returns 0."""
        count = history.load_from_csv("/nonexistent/path.csv")
        assert count == 0

    def test_load_custom_path(
        self, history: CalculationHistory, sample_calc: Calculation, tmp_path
    ) -> None:
        """load_from_csv with explicit path override."""
        history.add(sample_calc)
        custom = str(tmp_path / "custom.csv")
        history.save_to_csv(custom)

        history.clear()
        count = history.load_from_csv(custom)
        assert count == 1

    def test_load_csv_missing_columns(self, tmp_path) -> None:
        """Loading a CSV that is missing expected columns fills them."""
        csv_path = str(tmp_path / "bad.csv")
        pd.DataFrame([{"foo": "bar"}]).to_csv(csv_path, index=False)
        h = CalculationHistory(csv_path=csv_path)
        count = h.load_from_csv()
        assert count == 1
