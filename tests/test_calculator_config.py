"""
Tests for the Calculator Config Module
========================================

Tests for CalculatorConfig: loading from .env, environment variables,
boolean/integer parsing, and error handling.
"""

import os
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def env_file(tmp_path):
    """Create a temporary .env file and return its path."""
    env = tmp_path / ".env"
    env.write_text(
        "HISTORY_FILE=test_history.csv\n"
        "AUTO_SAVE=true\n"
        "MAX_HISTORY=500\n"
    )
    return str(env)


@pytest.fixture(autouse=True)
def clean_env():
    """Remove calculator-related env vars before and after each test."""
    keys = ["HISTORY_FILE", "AUTO_SAVE", "MAX_HISTORY"]
    saved = {}
    for k in keys:
        saved[k] = os.environ.pop(k, None)
    yield
    for k in keys:
        if saved[k] is not None:
            os.environ[k] = saved[k]
        else:
            os.environ.pop(k, None)


# ---------------------------------------------------------------------------
# Loading from .env
# ---------------------------------------------------------------------------


class TestConfigLoading:
    """Tests for loading configuration."""

    def test_defaults(self, tmp_path) -> None:
        """Without a .env file, defaults are used."""
        cfg = CalculatorConfig(env_path=str(tmp_path / "nonexistent.env"))
        assert cfg.history_file == "history.csv"
        assert cfg.auto_save is True
        assert cfg.max_history == 1000

    def test_load_from_env_file(self, env_file: str) -> None:
        """Values from the .env file are loaded correctly."""
        cfg = CalculatorConfig(env_path=env_file)
        assert cfg.history_file == "test_history.csv"
        assert cfg.auto_save is True
        assert cfg.max_history == 500

    def test_repr(self, env_file: str) -> None:
        """Repr includes all settings."""
        cfg = CalculatorConfig(env_path=env_file)
        r = repr(cfg)
        assert "test_history.csv" in r
        assert "auto_save" in r


# ---------------------------------------------------------------------------
# Boolean parsing
# ---------------------------------------------------------------------------


class TestBooleanParsing:
    """Tests for _parse_bool."""

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("yes", True),
            ("false", False),
            ("False", False),
            ("0", False),
            ("no", False),
        ],
        ids=[
            "true", "True", "TRUE", "1", "yes",
            "false", "False", "0", "no",
        ],
    )
    def test_valid_booleans(self, value: str, expected: bool) -> None:
        """Valid boolean strings are parsed correctly."""
        assert CalculatorConfig._parse_bool(value, "TEST") == expected

    @pytest.mark.parametrize(
        "value",
        ["maybe", "2", ""],
        ids=["maybe", "two", "empty"],
    )
    def test_invalid_booleans(self, value: str) -> None:
        """Invalid boolean strings raise ConfigurationError."""
        with pytest.raises(ConfigurationError, match="Invalid boolean"):
            CalculatorConfig._parse_bool(value, "TEST")


# ---------------------------------------------------------------------------
# Integer parsing
# ---------------------------------------------------------------------------


class TestIntegerParsing:
    """Tests for _parse_positive_int."""

    @pytest.mark.parametrize(
        "value, expected",
        [("1", 1), ("100", 100), ("999999", 999999)],
        ids=["one", "hundred", "large"],
    )
    def test_valid_integers(self, value: str, expected: int) -> None:
        """Valid positive integers are parsed correctly."""
        assert CalculatorConfig._parse_positive_int(value, "TEST") == expected

    def test_non_integer(self) -> None:
        """Non-integer strings raise ConfigurationError."""
        with pytest.raises(ConfigurationError, match="Invalid integer"):
            CalculatorConfig._parse_positive_int("abc", "TEST")

    def test_zero_integer(self) -> None:
        """Zero raises ConfigurationError (must be positive)."""
        with pytest.raises(ConfigurationError, match="positive integer"):
            CalculatorConfig._parse_positive_int("0", "TEST")

    def test_negative_integer(self) -> None:
        """Negative values raise ConfigurationError."""
        with pytest.raises(ConfigurationError, match="positive integer"):
            CalculatorConfig._parse_positive_int("-5", "TEST")
