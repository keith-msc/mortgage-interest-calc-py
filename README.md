# Mortgage Interest Calculator

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive mortgage amortization calculator that helps borrowers understand their loan payments, interest costs, and amortization schedule over time. Built with Python, it provides detailed visualizations and exportable data to aid in mortgage planning and analysis.

## Key Features

### Financial Calculations
- **Precise Payment Computation**: Calculate exact monthly payments using industry-standard amortization formulas
- **Flexible Loan Terms**: Support for any combination of years and months up to 50 years
- **Interest Analysis**: Detailed breakdown of interest vs. principal payments
- **LTV Tracking**: Monitor Loan-to-Value ratio throughout the loan term

### Data Visualization
- **Interactive Graphs**:
  - Payment Composition: Visual breakdown of principal and interest payments
  - Balance Tracking: Clear visualization of remaining balance with milestone markers
  - Progress Indicators: 25%, 50%, and 75% payoff milestone annotations

### Export Capabilities
- **Comprehensive CSV Export**: Complete amortization schedule with payment details
- **High-Quality Graphs**: Auto-generated PNG files for:
  - Monthly payment breakdown
  - Remaining balance progression
- **Summary Statistics**: Key loan metrics and total cost analysis

### International Support
- **Multi-Currency**: Support for Euro (€), US Dollar ($), and British Pound (£)
- **Flexible Date Handling**: Any loan start date with proper month/year validation
- **Standardized Formatting**: Thousands separators and consistent decimal places

## Installation

### System Requirements

- Python 3.x
- pip (Python package installer)
- 50MB free disk space
- Basic terminal/command line knowledge

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
cd mortgage-interest-calc-py

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Detailed Setup Guide

1. **Verify Python Installation**
   ```bash
   python3 --version  # Should be 3.x or higher
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
   cd mortgage-interest-calc-py
   ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

4. **Activate Environment**
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

Core requirements:
- python-dateutil==2.8.2
- matplotlib>=3.5.0
- numpy>=1.21.0

## Usage Guide

### Basic Usage

```bash
python amortization_schedule.py
```

### Input Parameters

| Parameter | Description | Example | Validation |
|-----------|-------------|---------|------------|
| Loan Amount | Total mortgage amount | 250000 | > 0, < 1B |
| Interest Rate | Annual rate (%) | 3.5 | 0-25% |
| Loan Term | Years + Months | 30y 0m | ≤ 50 years |
| Start Date | Loan start date | Jan 2023 | Valid date |
| Currency | Payment currency | euro/dollar/sterling | Valid choice |

### Generated Outputs

1. **Console Output**
   - Loan summary with key statistics
   - Monthly payment amount
   - Total interest cost
   - Payment schedule preview

2. **CSV Export**
   - Complete amortization schedule
   - Payment breakdowns
   - Running balances
   - LTV calculations

3. **Visualizations**
   - `amortization_schedule_payments.png`
   - `amortization_schedule_balance.png`

### Example Session

```plaintext
=== Mortgage Amortization Calculator ===
This calculator will help you understand your mortgage payments,
including how much interest you'll pay over the life of the loan.
==================================================

Enter the loan amount (principal, e.g., 250000): 200000
Enter the annual interest rate (e.g., 3.5 for 3.5%): 3.5
Enter the loan term in years: 30
Enter any additional months (0-11): 0
...
```

## Advanced Features

### Data Analysis
- Detailed payment breakdowns
- Interest vs. principal analysis
- LTV ratio tracking
- Milestone notifications

### Visualization Options
- Payment composition graphs
- Balance progression tracking
- Interactive matplotlib displays
- High-resolution PNG exports

### Export Capabilities
- Comprehensive CSV reports
- Professional-grade graphs
- Summary statistics

## Troubleshooting

### Common Issues

1. **Installation Problems**
   - Ensure Python 3.x is installed
   - Verify pip is up to date
   - Check virtual environment activation

2. **Runtime Errors**
   - Validate input parameters
   - Check file permissions
   - Verify matplotlib backend

3. **Graph Display Issues**
   - Ensure display server available
   - Check matplotlib configuration
   - Verify file write permissions

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| ValueError: Principal too high | Loan > 1B | Enter smaller amount |
| Invalid date | Wrong format | Use proper date format |
| Graph error | Display issues | Check environment |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch
3. Install development dependencies
4. Make your changes
5. Run tests
6. Submit PR

### Code Style

This project follows the Black code style. Please ensure your contributions are formatted accordingly:

```bash
pip install black
black .
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:

1. Check the [GitHub Issues](https://github.com/keith-msc/mortgage-interest-calc-py/issues)
2. Review the documentation
3. Open a new issue if needed

## Acknowledgments

- Built with Python and matplotlib
- Inspired by financial calculation tools
