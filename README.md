# Mortgage Interest Calculator (Amortization)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

A user-friendly mortgage calculator that helps you understand your loan payments, interest costs, and payment schedule. Provides clear visualizations and detailed breakdowns of your mortgage payments.

## Prerequisites

1. Python
   - Install Python 3.10 or higher from https://python.org
   - On Windows, check “Add Python to PATH” during installation
   - Verify installation:
     - macOS/Linux: `python3 --version`
     - Windows: `py --version`

2. Package manager
   - This project uses uv (fast Python package manager). Install: https://docs.astral.sh/uv/
   - Verify: `uv --version`

## Quick Start

```bash
# Clone the repository
git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
cd mortgage-interest-calc-py

# Create and activate virtual environment
uv venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -r requirements.txt

# Run the calculator
python run_calculator.py
```

Notes:
- If uv is not available, you can use the built-in venv and pip: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.

## Features

- Flexible deposit input: amount or percentage
- Precise monthly payment calculation (handles 0% interest correctly)
- Full amortization schedule with consistent rounding and last-payment correction
- Interest analysis: total interest and percentage of total cost
- Visual insights (optional): payment breakdown and remaining balance plots
- CSV/TXT export with summary first and normalized schedule keys
- Multi-currency support: €, $, £
- Robust input validation and helpful CLI prompts
- Backward-compatibility shims for legacy tests and APIs

## Usage

1. Run the calculator:
   ```bash
   python run_calculator.py
   ```

2. Enter your loan details when prompted:
   - Property value (e.g., 250000)
   - Deposit (optional):
     - Fixed amount (e.g., 50000)
     - Percentage (e.g., 20 for 20%)
     - Press Enter to skip deposit
   - Interest rate (e.g., 3.5)
   - Loan term in years and optional extra months (0-11)
   - Start month and year (e.g., Feb 2024)
   - Currency preference (euro/dollar/sterling)
   - Export filename (optional; press Enter to use default: amortization_schedule.csv)
   - Visualization preference (y/n; if matplotlib is not installed, plots are skipped)

3. Results include:
   - Monthly payment amount
   - Total interest cost and total cost
   - Complete amortization schedule (first 12 months printed in CLI)
   - Exported CSV/TXT with summary and full schedule
   - Visualization graphs if enabled:
     - `mortgage_output/payment_breakdown.png`
     - `mortgage_output/balance_progress.png`

## Requirements

- Python 3.10 or higher
- uv (recommended) or standard pip/venv
- matplotlib (optional, for graphs)
- python-dateutil (used internally for dates; installed via requirements)

## Example Output

Example inputs and excerpted outputs are shown in the issue tracker and match standard amortization math:
- Monthly payment: €1,626.60 for L=€455,000, r=2.5% APR, n=35 years
- Month 1 interest ≈ €947.92; principal ≈ €678.68; balance ≈ €454,321.32
- LTV decreases monotonically from ≈95.6% in the first month

<details>
<summary>Developer Documentation</summary>

## Project Structure

```
mortgage-interest-calc-py/
├── mortgage_calculator/
│   ├── core/
│   │   ├── calculations.py
│   │   └── validation.py
│   ├── io/
│   │   ├── cli.py
│   │   └── export.py
│   ├── visualization/
│   │   └── plotting.py
│   ├── __init__.py
│   └── main.py
├── tests/
├── setup.py
└── requirements.txt
```

## Development Setup

```bash
# Clone the repository
git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
cd mortgage-interest-calc-py

# Create venv
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -r requirements.txt

# Editable install (optional)
uv pip install -e .
```

## Testing and Tooling

```bash
# Run tests with coverage
uv run pytest --cov=mortgage_calculator tests/

# Format code
uv run black .

# Type checking
uv run mypy .

# Lint
uv run pylint mortgage_calculator/
```

### Technical Notes

- Input validation:
  - File names validated; default provided when pressing Enter
  - Month parsing supports full/abbrev names; consistent get_month_number
  - Currency normalization: euro/eur → €, dollar/usd → $, sterling/gbp/pound → £
- Amortization:
  - Handles 0% interest case via exact division
  - Rounds to 2 decimals; corrects final payment to zero out balance
- CLI/UX:
  - Uses defaults where appropriate
  - Visualization lazy-imported; skipped if matplotlib not present
- Exports:
  - Summary rows precede header
  - Schedule keys normalized (legacy and canonical supported)

## Contributing

Contributions are welcome! Please open an issue for major changes and submit a PR with tests where applicable.

### Development Process

1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make changes with tests
5. Run tests and linters
6. Open a PR

</details>

## License

This project is licensed under the GNU General Public License v3.0 — see the [LICENSE](LICENSE) file for details.

## Support

Need help?
1. Open or search [GitHub Issues](https://github.com/keith-msc/mortgage-interest-calc-py/issues)
2. Create a new issue if needed
