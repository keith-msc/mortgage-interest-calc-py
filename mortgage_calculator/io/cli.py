"""Command-line interface for mortgage calculator."""

from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Tuple, Optional

from ..core.validation import (
    validate_month_year,
    validate_currency_choice,
    format_currency,
    validate_file_name
)

def get_loan_amount() -> Optional[Decimal]:
    """
    Get and validate the loan amount from user input.
    
    Returns:
        Optional[Decimal]: The validated loan amount or None if invalid
    """
    try:
        principal_input = input("Enter the loan amount (principal, e.g., 250000): ")
        return Decimal(principal_input)
    except InvalidOperation:
        print("Invalid input: Please enter a numeric value for the loan amount.")
        return None

def get_interest_rate() -> Optional[Decimal]:
    """
    Get and validate the annual interest rate from user input.
    
    Returns:
        Optional[Decimal]: The validated interest rate or None if invalid
    """
    try:
        rate_input = input("Enter the annual interest rate (e.g., 3.5 for 3.5%): ")
        return Decimal(rate_input)
    except InvalidOperation:
        print("Invalid input: Please enter a numeric value for the interest rate.")
        return None

def get_loan_term() -> Optional[Tuple[int, int]]:
    """
    Get and validate the loan term in years and months from user input.
    
    Returns:
        Optional[Tuple[int, int]]: Tuple of (years, months) or None if invalid
    """
    print("\nLoan Term:")
    try:
        years = int(input("  Enter years (e.g., 30): "))
        months = int(input("  Enter any additional months (0-11): "))
        
        if years < 0:
            print("Years cannot be negative.")
            return None
        if months < 0 or months > 11:
            print("Additional months must be between 0 and 11.")
            return None
            
        return years, months
    except ValueError:
        print("Invalid input: Please enter valid numbers for years and months.")
        return None

def get_start_date() -> Optional[datetime]:
    """
    Get and validate the loan start date from user input.
    
    Returns:
        Optional[datetime]: The validated start date or None if invalid
    """
    print("\nLoan Start Date:")
    month_input = input("  Enter month (e.g., January, Jan): ")
    year_input = input("  Enter year (e.g., 2023): ")
    
    try:
        year = int(year_input)
        if year <= 0:
            print("Start year must be a positive integer.")
            return None
    except ValueError:
        print("Invalid year. Please enter a numeric value.")
        return None

    start_date = validate_month_year(month_input, year)
    if not start_date:
        print("Invalid month name or year. Please try again.")
        return None
    
    return start_date

def get_currency_symbol() -> str:
    """
    Get and validate the currency choice from user input.
    
    Returns:
        str: The currency symbol ('€', '$', or '£')
    """
    print("\nCurrency:")
    while True:
        try:
            currency_choice = input("  Choose currency (euro/dollar/sterling): ").strip()
            return validate_currency_choice(currency_choice)
        except ValueError as e:
            print(f"Error: {e}")
            print("Please try again.")

def get_visualization_preference() -> bool:
    """
    Get user preference for displaying visualization graphs.
    
    Returns:
        bool: True if user wants to see graphs, False otherwise
    """
    print("\nVisualization:")
    print("  Two graphs will be generated:")
    print("  1. Monthly payments breakdown (Principal vs Interest)")
    print("  2. Remaining balance over time with payoff milestones")
    choice = input("  Would you like to see these graphs? (yes/no): ").strip().lower()
    return choice in ('yes', 'y')

def get_export_filename() -> str:
    """
    Get the desired filename for CSV export from user input.
    
    Returns:
        str: The validated filename for CSV export
    """
    print("\nFile Export:")
    print("  Valid filename characters: letters, numbers, hyphen (-), underscore (_), period (.)")
    print("  Example: my-mortgage-2023.csv or mortgage_schedule_1.csv")
    
    while True:
        try:
            file_name = input("Enter the CSV file name: ").strip()
            return validate_file_name(file_name)
        except ValueError as e:
            print(f"\nError: {e}")
            print("Please try again with a valid filename.")

def print_welcome_message() -> None:
    """Print the welcome message and calculator description."""
    print("\n=== Mortgage Amortization Calculator ===")
    print("This calculator will help you understand your mortgage payments,")
    print("including how much interest you'll pay over the life of the loan.")
    print("=" * 50 + "\n")

def print_completion_message(monthly_payment: Decimal, total_interest: Decimal,
                           currency_symbol: str, csv_file: str) -> None:
    """
    Print the completion message with calculation results.
    
    Args:
        monthly_payment (Decimal): Monthly payment amount
        total_interest (Decimal): Total interest paid
        currency_symbol (str): Currency symbol for formatting
        csv_file (str): Name of the exported CSV file
    """
    print("\nCalculation complete!")
    print(f"Monthly Payment: {format_currency(monthly_payment, currency_symbol)}")
    print(f"Total Interest: {format_currency(total_interest, currency_symbol)}")
    print(f"Check {csv_file} for the detailed payment schedule.")
