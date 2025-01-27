"""Command-line interface for mortgage calculator."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
import sys
from typing import Optional, Tuple

from ..core.validation import (
    validate_loan_inputs,
    validate_month_year,
    validate_currency_choice,
    validate_file_name,
    LoanValidationError
)

class CLIError(Exception):
    """Custom exception for CLI operations."""
    pass

@dataclass
class UserInput:
    """Container for validated user input."""
    principal: Decimal
    annual_rate: Decimal
    total_months: int
    start_date: datetime
    currency_symbol: str
    export_filename: str
    deposit: Optional[Decimal] = None
    show_graphs: bool = True

    @property
    def property_value(self) -> Decimal:
        """Calculate total property value."""
        return self.principal + (self.deposit or Decimal('0'))

    @property
    def deposit_percentage(self) -> Optional[Decimal]:
        """Calculate deposit as percentage of property value."""
        if self.deposit is None or self.deposit == 0:
            return None
        return (self.deposit / self.property_value * 100).quantize(Decimal('0.1'))

def print_colored(message: str, color: str = "white") -> None:
    """
    Print colored text to the console.
    
    Args:
        message (str): Message to print
        color (str): Color name (red, green, yellow, blue, magenta, cyan, white)
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m'
    }
    reset = '\033[0m'
    
    color_code = colors.get(color.lower(), colors['white'])
    print(f"{color_code}{message}{reset}")

def print_error(message: str) -> None:
    """Print error message in red."""
    print_colored(f"Error: {message}", "red")

def print_success(message: str) -> None:
    """Print success message in green."""
    print_colored(message, "green")

def print_progress(message: str) -> None:
    """Print progress message in cyan."""
    print_colored(message, "cyan")

def print_welcome_message() -> None:
    """Print welcome message and basic instructions."""
    print("\n=== Mortgage Calculator ===")
    print("Calculate your mortgage payments and view amortization schedule")
    print("Enter the following details to begin:")
    print("-" * 50)

def print_completion_message() -> None:
    """Print completion message."""
    print_success("\nCalculation completed successfully!")
    print("Check the output directory for detailed results.")

def _get_decimal_input(
    prompt: str,
    min_value: float = 0,
    optional: bool = False
) -> Optional[Decimal]:
    """
    Get and validate decimal input from user.
    
    Args:
        prompt (str): Input prompt message
        min_value (float): Minimum allowed value
    
    Returns:
        Decimal: Validated decimal value
    
    Raises:
        CLIError: If input is invalid
    """
    while True:
        try:
            value = input(prompt).strip().replace(',', '')
            if not value:
                if optional:
                    return None
                raise CLIError("Input cannot be empty")
            
            decimal_value = Decimal(value)
            if decimal_value <= min_value:
                raise CLIError(f"Value must be greater than {min_value}")
            
            return decimal_value
            
        except InvalidOperation:
            print_error("Please enter a valid number")
        except CLIError as e:
            print_error(str(e))

def _get_date_input() -> datetime:
    """
    Get and validate date input from user.
    
    Returns:
        datetime: Validated start date
    
    Raises:
        CLIError: If input is invalid
    """
    while True:
        try:
            month = input("Enter start month (e.g., January or Jan): ").strip()
            year_str = input("Enter start year (YYYY): ").strip()
            
            if not month or not year_str:
                raise CLIError("Month and year cannot be empty")
            
            try:
                year = int(year_str)
            except ValueError:
                raise CLIError("Year must be a number")
            
            date = validate_month_year(month, year)
            if date is None:
                raise CLIError("Invalid month/year combination")
            
            return date
            
        except CLIError as e:
            print_error(str(e))

def _get_term_input() -> Tuple[int, int]:
    """
    Get and validate loan term input from user.
    
    Returns:
        Tuple[int, int]: Years and months
    
    Raises:
        CLIError: If input is invalid
    """
    while True:
        try:
            years = input("Enter loan term (years): ").strip()
            months = input("Additional months (0-11, optional): ").strip() or "0"
            
            try:
                years_int = int(years)
                months_int = int(months)
            except ValueError:
                raise CLIError("Years and months must be whole numbers")
            
            if years_int < 0 or months_int < 0:
                raise CLIError("Years and months cannot be negative")
            if months_int >= 12:
                raise CLIError("Additional months should be less than 12")
            if years_int == 0 and months_int == 0:
                raise CLIError("Total loan term must be greater than 0")
            
            total_months = (years_int * 12) + months_int
            if total_months > 600:  # 50 years
                raise CLIError("Loan term cannot exceed 50 years")
            
            return years_int, months_int
            
        except CLIError as e:
            print_error(str(e))

def collect_user_input() -> UserInput:
    """
    Collect and validate all user input.
    
    Returns:
        UserInput: Container with validated input
    
    Raises:
        CLIError: If any input is invalid
    """
    try:
        print_welcome_message()
        
        # Get property value and deposit
        property_value = _get_decimal_input(
            "Enter property value (e.g., 250000): ",
            min_value=0
        )
        
        # Get optional deposit
        deposit_type = input(
            "Choose to enter deposit as (1) amount or (2) percentage (press Enter for no deposit): "
        ).strip()
        
        deposit = None
        if deposit_type:
            if deposit_type not in ['1', '2']:
                raise CLIError("Please choose 1 for amount or 2 for percentage")
            
            if deposit_type == '1':
                deposit = _get_decimal_input(
                    "Enter deposit amount: ",
                    min_value=0
                )
                if deposit >= property_value:
                    raise CLIError("Deposit cannot be greater than or equal to property value")
                
            else:  # deposit_type == '2'
                deposit_percentage = _get_decimal_input(
                    "Enter deposit percentage (e.g., 20 for 20%): ",
                    min_value=0
                )
                if deposit_percentage >= 100:
                    raise CLIError("Deposit percentage cannot be 100% or greater")
                
                deposit = (property_value * deposit_percentage / 100).quantize(Decimal('0.01'))
            
            principal = property_value - deposit
            percentage = (deposit / property_value * 100).quantize(Decimal('0.1'))
            print_colored(
                f"Deposit: {deposit} ({percentage}% of property value)",
                "cyan"
            )
            print_colored(
                f"Loan amount after deposit: {principal}",
                "cyan"
            )
        else:
            principal = property_value
        
        # Get interest rate
        annual_rate = _get_decimal_input(
            "Enter annual interest rate (e.g., 3.5): ",
            min_value=0
        )
        
        # Get loan term
        years, months = _get_term_input()
        total_months = (years * 12) + months
        
        # Validate core loan parameters
        validate_loan_inputs(principal, annual_rate, total_months)
        
        # Get start date
        start_date = _get_date_input()
        
        # Get currency preference
        while True:
            try:
                currency = input(
                    "Choose currency (euro/dollar/sterling): "
                ).strip().lower()
                currency_symbol = validate_currency_choice(currency)
                break
            except ValueError as e:
                print_error(str(e))
        
        # Get export filename
        while True:
            try:
                filename = input(
                    "Enter filename for export (optional, press Enter for default): "
                ).strip() or "amortization_schedule"
                export_filename = validate_file_name(filename)
                break
            except ValueError as e:
                print_error(str(e))
        
        # Ask about graphs
        show_graphs = input(
            "Generate visualization graphs? (y/n, default: y): "
        ).strip().lower() != 'n'
        
        return UserInput(
            principal=principal,
            annual_rate=annual_rate,
            total_months=total_months,
            start_date=start_date,
            currency_symbol=currency_symbol,
            export_filename=export_filename,
            deposit=deposit,
            show_graphs=show_graphs
        )
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        raise CLIError(f"Failed to collect user input: {str(e)}")
