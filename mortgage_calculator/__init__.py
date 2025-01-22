"""Mortgage calculator package for loan amortization and visualization."""

__version__ = '1.0.0'
__author__ = 'Keith Morgan'
__license__ = 'GNU GPL v3'

from .core import (
    calculate_monthly_payment,
    create_amortization_schedule,
    validate_loan_inputs,
    validate_month_year,
    format_currency,
    validate_currency_choice
)

from .io import (
    export_amortization_schedule_to_csv,
    print_loan_summary,
    print_amortization_schedule,
    print_welcome_message,
    get_loan_amount,
    get_interest_rate,
    get_loan_term,
    get_start_date,
    get_currency_symbol,
    get_visualization_preference,
    get_export_filename,
    print_completion_message
)

from .visualization import (
    plot_amortization_schedule,
    plot_balance_over_time
)

__all__ = [
    # Core functionality
    'calculate_monthly_payment',
    'create_amortization_schedule',
    'validate_loan_inputs',
    'validate_month_year',
    'format_currency',
    'validate_currency_choice',
    
    # IO operations
    'export_amortization_schedule_to_csv',
    'print_loan_summary',
    'print_amortization_schedule',
    'print_welcome_message',
    'get_loan_amount',
    'get_interest_rate',
    'get_loan_term',
    'get_start_date',
    'get_currency_symbol',
    'get_visualization_preference',
    'get_export_filename',
    'print_completion_message',
    
    # Visualization
    'plot_amortization_schedule',
    'plot_balance_over_time'
]
