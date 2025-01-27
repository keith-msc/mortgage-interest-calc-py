"""Core package initialization."""

from .calculations import (
    LoanDetails,
    AmortizationEntry,
    calculate_monthly_payment,
    create_amortization_schedule,
    calculate_total_cost,
    calculate_interest_percentage,
    CalculationError
)

from .validation import (
    validate_loan_inputs,
    validate_month_year,
    validate_currency_choice,
    validate_file_name,
    format_currency,
    format_percentage,
    LoanValidationError
)

__all__ = [
    'LoanDetails',
    'AmortizationEntry',
    'calculate_monthly_payment',
    'create_amortization_schedule',
    'calculate_total_cost',
    'calculate_interest_percentage',
    'CalculationError',
    'validate_loan_inputs',
    'validate_month_year',
    'validate_currency_choice',
    'validate_file_name',
    'format_currency',
    'format_percentage',
    'LoanValidationError'
]
