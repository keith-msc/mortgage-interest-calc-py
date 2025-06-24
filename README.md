# Mortgage Interest Calculator (Amortization)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

A user-friendly mortgage calculator that helps you understand your loan payments, interest costs, and payment schedule. Get clear visualizations and detailed breakdowns of your mortgage payments.

## Prerequisites

1. Python Installation
   - Download and install Python 3.6 or higher from [python.org](https://python.org)
   - During installation on Windows, check "Add Python to PATH"
   - Verify installation: `python --version`

2. Pip Installation (if needed)
   - Pip should come with Python, verify with: `pip --version`
   - If missing, install with: `python -m ensurepip --upgrade`

## Quick Start

```bash
# Clone the repository
git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
cd mortgage-interest-calc-py

# Set up and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run the calculator
python run_calculator.py
```

## Features

- **Flexible Deposit Input**: Enter deposit as fixed amount or percentage of property value
- **Calculate Monthly Payments**: Get precise payment calculations using industry-standard formulas
- **Payment Schedule**: See a detailed breakdown of every payment over your loan term
- **Interest Analysis**: Understand how much interest you'll pay over time
- **Visual Insights**: View graphs showing:
  - Payment breakdown (Principal vs Interest)
  - Remaining balance over time
  - Key milestones (25%, 50%, 75% paid)
- **Export Options**:
  - Save payment schedule to CSV
  - Download visualization graphs
- **Multi-Currency Support**: Works with €, $, and £

## Usage

1. Run the calculator:
   ```bash
   python run_calculator.py
   ```

2. Enter your loan details:
   - Property value (e.g., 250000)
   - Deposit (optional):
     * Enter as fixed amount (e.g., 50000)
     * Enter as percentage (e.g., 20 for 20%)
     * Press Enter to skip deposit
   - Interest rate (e.g., 3.5)
   - Loan term in years
   - Start date
   - Currency preference

3. Get your results:
   - Monthly payment amount
   - Total interest cost
   - Complete payment schedule
   - Visual payment breakdown

## Example Output

The calculator will generate:
1. A CSV file with your complete payment schedule
2. Two visualization graphs:
   - `payment_breakdown.png`: Shows principal vs interest payments
   - `balance_progress.png`: Shows remaining balance over time

## Requirements

- Python 3.6 or higher
- 50MB free disk space

<details>
<summary>Developer Documentation</summary>

## Project Structure

```
mortgage-interest-calc-py/
├── mortgage_calculator/        # Main package
│   ├── core/                  # Core functionality
│   │   ├── calculations.py    # Financial calculations
│   │   └── validation.py      # Input validation
│   ├── io/                    # Input/Output handling
│   │   ├── cli.py            # Command line interface
│   │   └── export.py         # File export operations
│   ├── visualization/         # Data visualization
│   │   └── plotting.py       # Graph generation
│   ├── __init__.py           # Package initialization
│   └── main.py               # Main application logic
├── tests/                     # Test directory
├── setup.py                   # Package configuration
└── requirements.txt          # Dependencies
```

## Development Setup

```bash
# Clone the repository
git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
cd mortgage-interest-calc-py

# Set up virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Install in development mode
uv pip install -e .
```

## Testing

```bash
# Run tests with coverage
uv run pytest --cov=mortgage_calculator tests/

# Format code
uv run black .

# Type checking
uv run mypy .

# Lint code
uv run pylint mortgage_calculator/
```

## Technical Details

### Input Parameters

| Parameter | Description | Example | Validation |
|-----------|-------------|---------|------------|
| Property Value | Total property value | 250000 | > 0, < 1B |
| Deposit Amount | Initial payment (optional) | 50000 or 20% | < Property Value |
| Loan Amount | Property Value - Deposit | 200000 | > 0, < Property Value |
| Interest Rate | Annual rate (%) | 3.5 | 0-25% |
| Loan Term | Years + Months | 30y 0m | ≤ 50 years |
| Start Date | Loan start date | Jan 2023 | Valid date |
| Currency | Payment currency | euro/dollar/sterling | Valid choice |

### Development Tools
- **pytest**: Testing framework
- **black**: Code formatting
- **mypy**: Static type checking
- **pylint**: Code linting
- **hypothesis**: Property-based testing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Process
1. Fork the repository
2. Create your feature branch
3. Install development dependencies
4. Make your changes
5. Run tests and linting
6. Submit PR

</details>

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

Need help? Check out:
1. [GitHub Issues](https://github.com/keith-msc/mortgage-interest-calc-py/issues)
2. Open a new issue if needed
