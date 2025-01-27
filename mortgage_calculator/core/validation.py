"""Input validation and formatting functions."""

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Optional

class LoanValidationError(Exception):
    """Custom exception for loan validation errors."""
    pass

def validate_loan_inputs(
    principal: Decimal,
    annual_rate: Decimal,
    months: int
) -> None:
    """
    Validate loan input parameters.
    
    Args:
        principal (Decimal): Original loan amount
        annual_rate (Decimal): Annual interest rate
        months (int): Total number of months
    
    Raises:
        LoanValidationError: If any input is invalid
    """
    if principal <= 0:
        raise LoanValidationError("Principal must be greater than zero")
    if principal > Decimal('1000000000'):  # 1 billion
        raise LoanValidationError("Principal amount is unreasonably large")
    
    if annual_rate < 0:
        raise LoanValidationError("Interest rate cannot be negative")
    if annual_rate > 25:
        raise LoanValidationError("Interest rate cannot exceed 25%")
    
    if months <= 0:
        raise LoanValidationError("Loan term must be greater than zero months")
    if months > 600:  # 50 years
        raise LoanValidationError("Loan term cannot exceed 50 years")

def validate_month_year(month_str: str, year: int) -> Optional[datetime]:
    """
    Validate and parse month and year into datetime.
    
    Args:
        month_str (str): Month name (e.g., "January" or "Jan")
        year (int): Year number
    
    Returns:
        Optional[datetime]: Parsed datetime or None if invalid
    """
    # Map of valid month names and abbreviations
    month_map = {
        'january': 1, 'jan': 1,
        'february': 2, 'feb': 2,
        'march': 3, 'mar': 3,
        'april': 4, 'apr': 4,
        'may': 5,
        'june': 6, 'jun': 6,
        'july': 7, 'jul': 7,
        'august': 8, 'aug': 8,
        'september': 9, 'sep': 9, 'sept': 9,
        'october': 10, 'oct': 10,
        'november': 11, 'nov': 11,
        'december': 12, 'dec': 12
    }
    
    try:
        month_num = month_map.get(month_str.lower())
        if not month_num:
            return None
        
        if year <= 1900 or year > 2100:
            return None
            
        return datetime(year, month_num, 1)
    except (ValueError, AttributeError):
        return None

def validate_currency_choice(choice: str) -> str:
    """
    Validate and convert currency choice to symbol.
    
    Args:
        choice (str): Currency name (euro, dollar, sterling)
    
    Returns:
        str: Currency symbol
    
    Raises:
        ValueError: If currency choice is invalid
    """
    currency_map = {
        'euro': '€',
        'eur': '€',
        'dollar': '$',
        'usd': '$',
        'sterling': '£',
        'gbp': '£',
        'pound': '£'
    }
    
    symbol = currency_map.get(choice.lower())
    if not symbol:
        raise ValueError(
            "Invalid currency choice. Please choose 'euro', 'dollar', or 'sterling'"
        )
    
    return symbol

def validate_file_name(file_name: str) -> str:
    """
    Validate and clean file name for export.
    
    Args:
        file_name (str): Proposed file name
    
    Returns:
        str: Cleaned file name
    
    Raises:
        ValueError: If file name is invalid
    """
    # Remove any directory path
    file_name = Path(file_name).name
    
    # Check for empty name
    if not file_name:
        raise ValueError("File name cannot be empty")
    
    # Remove or replace invalid characters
    clean_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)
    
    # Ensure it has an extension
    if not clean_name.endswith(('.csv', '.txt')):
        clean_name += '.csv'
    
    return clean_name

def format_currency(amount: Decimal, symbol: str) -> str:
    """
    Format decimal amount as currency string.
    
    Args:
        amount (Decimal): Amount to format
        symbol (str): Currency symbol
    
    Returns:
        str: Formatted currency string
    """
    try:
        # Format with thousands separator and 2 decimal places
        formatted = f"{amount:,.2f}"
        
        # Add currency symbol based on type
        if symbol == '€':
            return f"{symbol}{formatted}"
        elif symbol == '£':
            return f"£{formatted}"
        else:  # Default to $ format
            return f"${formatted}"
            
    except (InvalidOperation, ValueError, TypeError):
        return f"{symbol}0.00"

def format_percentage(value: Decimal, decimal_places: int = 1) -> str:
    """
    Format decimal value as percentage string.
    
    Args:
        value (Decimal): Value to format
        decimal_places (int): Number of decimal places
    
    Returns:
        str: Formatted percentage string
    """
    try:
        return f"{value:.{decimal_places}f}%"
    except (InvalidOperation, ValueError, TypeError):
        return "0.0%"
