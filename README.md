# Mortgage Interest Calculator (Amortization)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

A user-friendly mortgage calculator that helps you understand your loan payments, interest costs, and payment schedule. Get clear visualizations and detailed breakdowns of your mortgage payments.

## Prerequisites

1. Python Installation
   - Download and install Python 3.6 or higher from [python.org](https://python.org)
   - During installation on Windows, check "Add Python to PATH"
   - Verify installation: `python --version`

2. Virtual Environment (Recommended)
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Pip Installation (if needed)
   - Pip should come with Python, verify with: `pip --version`
   - If missing, install with: `python -m ensurepip --upgrade`

## Quick Start

```bash
# Clone the repository
git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
cd mortgage-interest-calc-py

# Set up and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the calculator
python run_calculator.py
```

## Features

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
   - Loan amount (e.g., 250000)
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
   - `amortization_schedule_payments.png`
   - `amortization_schedule_balance.png`

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
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Testing

```bash
# Run tests with coverage
pytest --cov=mortgage_calculator tests/

# Format code
black .

# Type checking
mypy .

# Lint code
pylint mortgage_calculator/
```

## Technical Details

### Input Parameters

| Parameter | Description | Example | Validation |
|-----------|-------------|---------|------------|
| Loan Amount | Total mortgage amount | 250000 | > 0, < 1B |
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
