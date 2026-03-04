"""
Special Commands Module
=======================

This module centralizes the definitions of all special commands available
in the calculator's REPL interface. Each command is defined in a
structured dictionary that includes its name, a short description,
and the method in the `Calculator` class that handles its execution.

By centralizing these definitions, the command structure is made more
maintainable and extensible. Adding new commands or modifying existing
ones can be done in a single location without altering the main REPL logic.
This approach decouples the command definitions from their implementation,
improving code organization and readability.

The command dictionary is used by the `Calculator` class to populate its
command handling logic, ensuring that all commands are processed uniformly.
"""

SPECIAL_COMMANDS = {
    "help": {
        "description": "Show this help message.",
        "handler": "_handle_help"
    },
    "?": {
        "description": "Alias for help.",
        "handler": "_handle_help"
    },
    "history": {
        "description": "Show calculation history.",
        "handler": "_handle_history"
    },
    "clear": {
        "description": "Clear calculation history.",
        "handler": "_handle_clear"
    },
    "undo": {
        "description": "Undo the last action.",
        "handler": "_handle_undo"
    },
    "redo": {
        "description": "Redo the last undone action.",
        "handler": "_handle_redo"
    },
    "save": {
        "description": "Save history to CSV.",
        "handler": "_handle_save"
    },
    "load": {
        "description": "Load history from CSV.",
        "handler": "_handle_load"
    },
    "exit": {
        "description": "Exit the calculator.",
        "handler": None  # Special case handled in the REPL loop
    }
}
