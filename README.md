# Mortgage Interest Calculator (Amortization Schedule)

This Python script calculates the monthly payments and generates a complete amortization schedule for a given loan. It also computes the Loan-to-Value (LTV) ratio over time, providing insights into the loan balance relative to the original loan amount.

## Features

- **Monthly Payment Calculation**: Automatically calculates the fixed monthly payment based on the loan amount, interest rate, and loan term.
- **Amortization Schedule**: Generates a detailed month-by-month breakdown of the loan repayment, including principal, interest, and remaining balance.
- **Loan-to-Value (LTV) Ratio**: Calculates and displays the LTV ratio for each month, showing how the loan balance decreases relative to the original loan amount.
- **Date-Based Schedule**: The schedule starts from a user-specified month and year, with dates formatted as `Month YYYY`.

## Requirements

- Python 3.x

## Installation

1. Clone the repository or download the script file directly.
2. Ensure that you have Python 3.x installed on your system.
3. Set up a virtual environment (venv) to manage dependencies.

### Setting Up a Virtual Environment

1. **Navigate to the project directory:**

   ```bash
   cd /path/to/your/project/AmortizationCalc

### Create a virtual environment:

python3 -m venv venv

### Activate the virtual environment:

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate

   ### Install the required dependencies:
   pip install -r requirements.txt

   ### Run the script:
   python amortization_calculator.py

   ### Deactivate the virtual environment when you're done:
   deactivate

   ### Usage
   Run the script and follow the prompts to enter the required information:
   1. Loan amount
   2. Interest rate (as a percentage) 
   3. Loan term (in years)
   4. Start month (1-12)
   5. Start year (YYYY)
   6. The script will then display the monthly payment, the amortization schedule, and the LTV ratio for each month.
   
   ### Example Output
      Enter the loan amount (principal): 250000
      Enter the annual interest rate (in %): 5
      Enter the loan term in months: 360
      Enter the start month (MM): 08
      Enter the start year (YYYY): 2024

      Date                 Month  Payment    Principal       Interest  Balance    LTV     
```bash
August 2024          1      1698.10    342.05          1000.00   249657.95  99.9%   
September 2024       2      1698.10    343.48          998.57    249314.47  99.7%   
October 2024         3      1698.10    344.91          997.14    248969.55  99.6%   
```

   ### Full Directory Structure

AmortizationCalc/
├── amortization_calculator.py
├── requirements.txt
├── README.md
└── ... (other files)
