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
from unittest.mock import MagicMock, patch
import logging

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
def history_setup(tmp_path):
    """Provide a fresh CalculationHistory using a temp CSV path."""
    history_dir = str(tmp_path / "data")
    log_dir = str(tmp_path / "logs")
    return history_dir, log_dir


@pytest.fixture
def history(history_setup) -> CalculationHistory:
    history_dir, _ = history_setup
    return CalculationHistory(history_dir=history_dir, history_file="test_history.csv")


@pytest.fixture
def sample_calc() -> Calculation:
    """Provide a sample add calculation."""
    return Calculation(Decimal("2"), Decimal("3"), add, "add", precision=2)


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
        assert "timestamp" in rows[0]

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

    def test_history_full(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """Test that the history does not exceed the max size."""
        history.max_size = 1
        history.add(sample_calc)
        history.add(sample_calc)
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
        """Test that a removed observer is not notified."""
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

    def test_logs_calculation(self, sample_calc: Calculation, history_setup) -> None:
        """Calculation is logged to file."""
        _, log_dir = history_setup
        log_file = "test_calc.log"
        observer = LoggingObserver(log_dir=log_dir, log_file=log_file)

        # We might need to handle the singleton logger in tests
        with MagicMock() as mock_logger:
            observer.logger = mock_logger
            observer.on_calculation(sample_calc)
            mock_logger.info.assert_called_once()

    def test_logging_observer_init_no_dir(self, tmp_path) -> None:
        """Test that the LoggingObserver creates the log directory if it doesn't exist."""
        log_dir = tmp_path / "logs"
        assert not log_dir.exists()
        LoggingObserver(log_dir=str(log_dir))
        assert log_dir.exists()


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

        new_history = CalculationHistory(history_dir=history.history_dir, history_file=history.history_file)
        count = new_history.load_from_csv()
        assert count == 1
        assert len(new_history) == 1

    def test_load_nonexistent_file(self, history: CalculationHistory) -> None:
        """Loading from a nonexistent file returns 0."""
        count = history.load_from_csv("/nonexistent/path.csv")
        assert count == 0

    def test_auto_save_observer(self, history: CalculationHistory, sample_calc: Calculation):
        """Test that the auto save observer saves the history."""
        observer = AutoSaveObserver(history, enabled=True)
        history.add_observer(observer)
        history.add(sample_calc)
        assert os.path.exists(history.csv_path)

    def test_auto_save_observer_disabled(
        self, history: CalculationHistory, sample_calc: Calculation
    ) -> None:
        """Test that the auto save observer does not save the history when disabled."""
        observer = AutoSaveObserver(history, enabled=False)
        history.add_observer(observer)
        history.add(sample_calc)
        assert not os.path.exists(history.csv_path)

    def test_load_malformed_csv(self, history: CalculationHistory) -> None:
        """Test that loading a malformed CSV file returns 0."""
        with patch('pandas.read_csv', side_effect=Exception("Mocked error")):
            count = history.load_from_csv()
            assert count == 0

    def test_load_csv_with_missing_columns(self, history: CalculationHistory) -> None:
        """Test that loading a CSV with missing columns still works."""
        df = pd.DataFrame({"a": [1], "b": [2]})
        df.to_csv(history.csv_path, index=False)
        count = history.load_from_csv()
        assert count == 1
        assert "result" in history.get_dataframe().columns

    def test_save_to_csv_no_dir(self, history: CalculationHistory) -> None:
        """Test that save_to_csv creates the directory if it doesn't exist."""
        history_dir = history.history_dir + "/new"
        history.history_dir = history_dir
        history.csv_path = os.path.join(history.history_dir, history.history_file)
        history.save_to_csv()
        assert os.path.exists(history.csv_path)
