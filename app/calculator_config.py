"""
Calculator Configuration Module (dotenv)
==========================================

Loads application settings from environment variables (with ``.env`` file
support via ``python-dotenv``).  Validates values and raises
``ConfigurationError`` for invalid settings.

Settings:
    - ``HISTORY_FILE``: path to the CSV history file (default ``history.csv``)
    - ``AUTO_SAVE``: ``"true"`` / ``"false"`` toggle (default ``"true"``)
    - ``MAX_HISTORY``: maximum rows to keep in history (default ``1000``)
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Loads and validates calculator settings from the environment.

    Attributes:
        history_file: Path to the CSV history file.
        auto_save: Whether to auto-save after each calculation.
        max_history: Maximum number of rows retained in history.
    """

    def __init__(self, env_path: str | None = None) -> None:
        """Load config from environment / ``.env`` file.

        Args:
            env_path: Optional explicit path to a ``.env`` file.
        """
        load_dotenv(dotenv_path=env_path, override=True)

        self.history_file: str = os.getenv("HISTORY_FILE", "history.csv")
        self.auto_save: bool = self._parse_bool(
            os.getenv("AUTO_SAVE", "true"), "AUTO_SAVE"
        )
        self.max_history: int = self._parse_positive_int(
            os.getenv("MAX_HISTORY", "1000"), "MAX_HISTORY"
        )

    # -- helpers ------------------------------------------------------------

    @staticmethod
    def _parse_bool(value: str, name: str) -> bool:
        """Convert a string to a boolean.

        Raises:
            ConfigurationError: If the value is not ``true`` or ``false``.
        """
        lower = value.strip().lower()
        if lower in ("true", "1", "yes"):
            return True
        if lower in ("false", "0", "no"):
            return False
        raise ConfigurationError(
            f"Invalid boolean value for {name}: '{value}'. "
            "Use 'true' or 'false'."
        )

    @staticmethod
    def _parse_positive_int(value: str, name: str) -> int:
        """Convert a string to a positive integer.

        Raises:
            ConfigurationError: If the value is not a valid positive integer.
        """
        try:
            result = int(value)
        except ValueError:
            raise ConfigurationError(
                f"Invalid integer value for {name}: '{value}'."
            )
        if result <= 0:
            raise ConfigurationError(
                f"{name} must be a positive integer, got {result}."
            )
        return result

    def __repr__(self) -> str:
        return (
            f"CalculatorConfig(history_file='{self.history_file}', "
            f"auto_save={self.auto_save}, max_history={self.max_history})"
        )
