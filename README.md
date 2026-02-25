# Calculator App

A professional-grade, command-line calculator application built in Python with advanced design patterns, pandas-based history management, undo/redo support, and 100% test coverage.

## Features

- **Interactive REPL** — Read-Eval-Print Loop for continuous calculations
- **Six arithmetic operations** — `add`, `subtract`, `multiply`, `divide`, `power`, `root`
- **Design Patterns**:
  - **Observer Pattern** — Logging and auto-save observers on calculation history
  - **Memento Pattern** — Undo and redo functionality
  - **Strategy Pattern** — Operations stored as interchangeable callables
  - **Factory Pattern** — `CalculationFactory` creates calculations by name
  - **Facade Pattern** — `Calculator` class wraps all subsystems
- **Data management with pandas** — History stored as a `DataFrame`, persisted to CSV
- **Configuration with dotenv** — `HISTORY_FILE`, `AUTO_SAVE`, `MAX_HISTORY` from `.env`
- **Robust error handling** — LBYL validation + EAFP exception handling
- **Decimal precision** — Uses Python's `Decimal` type
- **100% test coverage** — Enforced via CI pipeline

## Project Structure

```
calculator-app-assignment5/
├── app/
│   ├── __init__.py               # Package docstring
│   ├── calculator_repl.py        # Calculator REPL (Facade pattern)
│   ├── calculation.py            # Calculation model + Factory pattern
│   ├── calculator_config.py      # Configuration (dotenv)
│   ├── calculator_memento.py     # Memento pattern (undo/redo)
│   ├── exceptions.py             # Custom exception hierarchy
│   ├── history.py                # Pandas history + Observer pattern
│   ├── input_validators.py       # LBYL input validation
│   └── operations.py             # Arithmetic ops (Strategy pattern)
├── tests/
│   ├── __init__.py
│   ├── test_calculations.py      # Calculation + Factory tests
│   ├── test_calculator_config.py # Config tests
│   ├── test_calculator_memento.py # Memento undo/redo tests
│   ├── test_calculator_repl.py   # REPL integration tests
│   ├── test_exceptions.py        # Exception hierarchy tests
│   ├── test_history.py           # History + Observer tests
│   ├── test_input_validators.py  # Validator tests
│   └── test_operations.py        # Operations tests
├── .github/
│   └── workflows/
│       └── python-app.yml        # GitHub Actions CI pipeline
├── main.py                       # Application entry point
├── .env.example                  # Example configuration
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
```

## Architecture

| Module | Responsibility | Pattern |
|---|---|---|
| `app.operations` | Pure arithmetic functions + strategy registry | **Strategy** |
| `app.calculation` | Calculation model + factory creation | **Factory** |
| `app.history` | Pandas DataFrame history + observer notifications | **Observer** |
| `app.calculator_memento` | Undo/redo state snapshots | **Memento** |
| `app.calculator_config` | Environment-based config via dotenv | — |
| `app.calculator_repl` | REPL wrapping all subsystems | **Facade** |
| `app.input_validators` | LBYL input validation | **LBYL** |
| `app.exceptions` | Custom exception hierarchy | — |

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:sairamcharan9/calculator-app-assignment5.git
cd calculator-app-assignment5
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure (optional)

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

Available settings:
| Variable | Default | Description |
|---|---|---|
| `HISTORY_FILE` | `history.csv` | Path to CSV history file |
| `AUTO_SAVE` | `true` | Auto-save after each calculation |
| `MAX_HISTORY` | `1000` | Maximum history entries |

## Usage

### Start the calculator

```bash
python main.py
```

### REPL commands

| Command | Description | Example |
|---|---|---|
| `add <a> <b>` | Addition | `add 5 3` → `5 + 3 = 8` |
| `subtract <a> <b>` | Subtraction | `subtract 10 4` → `10 - 4 = 6` |
| `multiply <a> <b>` | Multiplication | `multiply 6 7` → `6 * 7 = 42` |
| `divide <a> <b>` | Division | `divide 20 4` → `20 / 4 = 5` |
| `power <a> <b>` | Exponentiation | `power 2 8` → `2 ^ 8 = 256` |
| `root <a> <b>` | Nth root | `root 9 2` → `9 √ 2 = 3` |
| `history` | Show calculation history | |
| `clear` | Clear calculation history | |
| `undo` | Undo last action | |
| `redo` | Redo last undone action | |
| `save` | Save history to CSV | |
| `load` | Load history from CSV | |
| `help` or `?` | Show help message | |
| `exit` | Quit the calculator | |

### Example session

```
================================
   Welcome to the Calculator!
================================
Type 'help' for available commands.
Type 'exit' to quit.

>>> add 10 5
Result: 10 + 5 = 15

>>> power 2 8
Result: 2 ^ 8 = 256

>>> history
=== Calculation History ===
  1. 10 add 5 = 15
  2. 2 power 8 = 256

Total: 2 calculation(s)

>>> undo
Undo successful.

>>> save
History saved to 'history.csv'.

>>> exit
Goodbye!
```

## Running Tests

```bash
# Run all tests with verbose output
pytest

# Run tests with coverage report
pytest --cov=app

# Run tests with coverage and enforce 100% threshold
pytest --cov=app tests/
coverage report --fail-under=100
```

## Continuous Integration

The project uses **GitHub Actions** (`.github/workflows/python-app.yml`) to automatically:

1. Run all tests on every push and pull request to `main`
2. Generate a coverage report
3. **Enforce 100% code coverage** — the build fails if coverage drops below 100%

## Design Patterns

### Observer Pattern
`LoggingObserver` and `AutoSaveObserver` subscribe to `CalculationHistory`. When a calculation is added, all observers are notified automatically.

### Memento Pattern
`CalculatorMemento` captures history state snapshots. `MementoCaretaker` maintains undo/redo stacks, enabling users to revert or reapply changes.

### Strategy Pattern
Arithmetic operations are stored in the `OPERATIONS` dictionary as interchangeable callables, making it easy to add new operations.

### Factory Pattern
`CalculationFactory.create()` maps operation name strings to `Calculation` instances, decoupling creation logic from usage.

### Facade Pattern
The `Calculator` class provides a unified interface to configuration, history, memento, observers, validators, and operations.

## Error Handling

- **LBYL** (Look Before You Leap) — Input format and operation name are validated before processing (`input_validators.py`)
- **EAFP** (Easier to Ask Forgiveness than Permission) — Invalid numbers and operation errors are caught via exception handling (`calculator_repl.py`, `operations.py`)
