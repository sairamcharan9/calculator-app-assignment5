# Advanced Calculator App

An enhanced command-line calculator application built in Python with advanced design patterns, pandas-based history management, undo/redo support, and high test coverage.

## Features

- **Interactive REPL** — Read-Eval-Print Loop for continuous calculations.
- **Enhanced Arithmetic Operations**:
  - `add`, `subtract`, `multiply`, `divide`, `power`, `root`, `modulus`, `int_divide`, `percent`, `abs_diff`.
- **Design Patterns**:
  - **Observer Pattern** — `LoggingObserver` and `AutoSaveObserver`.
  - **Memento Pattern** — Undo and redo functionality.
  - **Strategy Pattern** — Operations as interchangeable callables.
  - **Factory Pattern** — `CalculationFactory` for creating calculations.
  - **Facade Pattern** — `Calculator` class as a unified interface.
- **Data Persistence** — History managed with pandas and saved to CSV.
- **Configuration** — Flexible setup using a `.env` file and `python-dotenv`.
- **Robust Error Handling** — Custom exceptions and input validation (LBYL + EAFP).
- **Comprehensive Logging** — Details logged to a file using Python's `logging` module.

## Configuration (.env)

Create a `.env` file in the root directory to customize the application:

```env
CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_DIR=data
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1e10
CALCULATOR_DEFAULT_ENCODING=utf-8
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the calculator:
```bash
python main.py
```

### Supported Commands

| **Command**    | **Syntax**                  | **Description**                                             |
|----------------|-----------------------------|-------------------------------------------------------------|
| `add`          | `add <num1> <num2>`         | Adds two numbers.                                           |
| `subtract`     | `subtract <num1> <num2>`    | Subtracts the second number from the first.                 |
| `multiply`     | `multiply <num1> <num2>`    | Multiplies two numbers.                                     |
| `divide`       | `divide <num1> <num2>`      | Divides the first number by the second.                     |
| `power`        | `power <base> <exp>`        | Raises a number to the power of an exponent.                |
| `root`         | `root <num> <n>`            | Calculates the nth root of a number.                        |
| `modulus`      | `modulus <num1> <num2>`     | Finds the remainder of a division.                          |
| `int_divide`   | `int_divide <num1> <num2>`  | Performs integer division.                                  |
| `percent`      | `percent <num1> <num2>`     | Calculates the percentage of the first number to the second.|
| `abs_diff`     | `abs_diff <num1> <num2>`    | Calculates the absolute difference between two numbers.     |
| `history`      | `history`                   | Displays the calculation history.                           |
| `clear`        | `clear`                     | Clears the calculation history.                             |
| `undo`         | `undo`                      | Undoes the last calculation.                                |
| `redo`         | `redo`                      | Redoes the last undone calculation.                         |
| `save`         | `save`                      | Manually saves the calculation history to a file.           |
| `load`         | `load`                      | Loads the calculation history from a file.                  |
| `help`         | `help`                      | Displays the list of available commands.                    |
| `exit`         | `exit`                      | Exits the application.                                      |

Example:
```
>>> add 10 5
Result: 10 + 5 = 15.00
>>> modulus 10 3
Result: 10 % 3 = 1.00
>>> undo
Undo successful.
```

## Testing

Run tests with coverage:
```bash
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

## CI/CD

GitHub Actions automatically runs tests and enforces a 90% coverage threshold on every push or pull request to the `main` branch.
