"""Mortgage calculator package initialization."""

__version__ = "1.0.0"
__author__ = "Keith Morgan"
__email__ = "keith.morgan@ucdconnect.ie"

from .core import (
    LoanDetails,
    AmortizationEntry,
    calculate_monthly_payment,
    create_amortization_schedule,
    calculate_total_cost,
    calculate_interest_percentage,
    CalculationError,
    validate_loan_inputs,
    validate_month_year,
    validate_currency_choice,
    validate_file_name,
    format_currency,
    format_percentage,
    LoanValidationError
)

from .io import (
    UserInput,
    collect_user_input,
    print_colored,
    print_error,
    print_progress,
    print_success,
    print_welcome_message,
    print_completion_message,
    CLIError,
    LoanSummary,
    export_amortization_schedule,
    print_loan_summary,
    print_amortization_schedule,
    ExportError
)

from .visualization import (
    PlotConfig,
    plot_amortization_schedule,
    plot_balance_over_time,
    PlottingError
)

__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    
    # Core functionality
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
    'LoanValidationError',
    
    # IO functionality
    'UserInput',
    'collect_user_input',
    'print_colored',
    'print_error',
    'print_progress',
    'print_success',
    'print_welcome_message',
    'print_completion_message',
    'CLIError',
    'LoanSummary',
    'export_amortization_schedule',
    'print_loan_summary',
    'print_amortization_schedule',
    'ExportError',
    
    # Visualization functionality
    'PlotConfig',
    'plot_amortization_schedule',
    'plot_balance_over_time',
    'PlottingError'
]
