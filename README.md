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

## Usage

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the script using Python:

   ```bash
   python amortization_calculator.py

## Example:

**Input:**

``` bash
Enter the loan amount (principal): 250000
Enter the annual interest rate (in %): 5
Enter the loan term in months: 360
Enter the start month (MM): 08
Enter the start year (YYYY): 2024


Date                 Month  Payment    Principal       Interest  Balance    LTV     
August 2024          1      1342.05    342.05          1000.00   249657.95  99.9%   
September 2024       2      1342.05    343.48          998.57    249314.47  99.7%   
October 2024         3      1342.05    344.91          997.14    248969.55  99.6%   
...