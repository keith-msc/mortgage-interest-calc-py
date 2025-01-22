"""Main entry point for the mortgage calculator application."""

from decimal import Decimal
from typing import Optional, Tuple

from .core import (
    calculate_monthly_payment,
    create_amortization_schedule,
    validate_loan_inputs
)
from .io import (
    print_welcome_message,
    get_loan_amount,
    get_interest_rate,
    get_loan_term,
    get_start_date,
    get_currency_symbol,
    get_visualization_preference,
    get_export_filename,
    print_completion_message,
    export_amortization_schedule_to_csv,
    print_loan_summary,
    print_amortization_schedule
)
from .visualization import (
    plot_amortization_schedule,
    plot_balance_over_time
)

def get_validated_inputs() -> Optional[Tuple[Decimal, Decimal, int, str]]:
    """
    Get and validate all required inputs from the user.
    
    Returns:
        Optional[Tuple[Decimal, Decimal, int, str]]: Tuple of (principal, rate, months, currency)
        or None if validation fails
    """
    # Get loan amount
    principal = get_loan_amount()
    if principal is None:
        return None

    # Get interest rate
    annual_rate = get_interest_rate()
    if annual_rate is None:
        return None

    # Get loan term
    term = get_loan_term()
    if term is None:
        return None
    years, additional_months = term
    total_months = (years * 12) + additional_months

    # Get start date
    start_date = get_start_date()
    if start_date is None:
        return None

    # Get currency
    currency_symbol = get_currency_symbol()

    # Validate all inputs together
    try:
        validate_loan_inputs(principal, annual_rate, total_months)
        return principal, annual_rate, total_months, start_date, currency_symbol
    except ValueError as e:
        print(f"Error: {e}")
        return None

def main() -> None:
    """Main function to run the mortgage calculator."""
    print_welcome_message()

    # Get and validate all inputs
    inputs = get_validated_inputs()
    if inputs is None:
        return

    principal, annual_rate, months, start_date, currency_symbol = inputs

    try:
        # Calculate monthly payment
        monthly_payment = calculate_monthly_payment(principal, annual_rate, months)

        # Create amortization schedule
        schedule, total_interest = create_amortization_schedule(
            principal, annual_rate, months, start_date
        )

        # Print loan summary and amortization schedule
        print_loan_summary(
            principal, annual_rate, months,
            monthly_payment, total_interest, currency_symbol
        )
        print_amortization_schedule(schedule, currency_symbol)

        # Export to CSV
        csv_file = get_export_filename()
        export_amortization_schedule_to_csv(
            schedule, csv_file, currency_symbol,
            principal, annual_rate, months,
            monthly_payment, total_interest
        )

        # Generate visualizations if requested
        if get_visualization_preference():
            # Create payment breakdown graph
            plot_amortization_schedule(
                schedule,
                currency_symbol,
                principal,
                'amortization_schedule_payments.png'
            )
            
            # Create balance over time graph
            plot_balance_over_time(
                schedule,
                currency_symbol,
                principal,
                'amortization_schedule_balance.png'
            )

        # Print completion message
        print_completion_message(monthly_payment, total_interest, currency_symbol, csv_file)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try again with valid inputs.")

if __name__ == '__main__':
    main()
