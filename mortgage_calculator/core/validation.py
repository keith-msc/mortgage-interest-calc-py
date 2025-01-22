"""Input validation functions for mortgage calculator."""

from datetime import datetime
from typing import Optional, Dict

MONTH_MAP: Dict[str, int] = {}
# Build full month map programmatically
for idx in range(1, 13):
    month = datetime(2000, idx, 1).strftime('%B').lower()
    MONTH_MAP[month] = idx
    MONTH_MAP[month[:3]] = idx
    # Handle "sept" special case
    if idx == 9:
        MONTH_MAP['sept'] = idx

def get_month_number(month_str: str) -> Optional[int]:
    """
    Convert month name to number with comprehensive mapping.
    
    Args:
        month_str (str): Month name (e.g., 'January', 'Jan')
    
    Returns:
        Optional[int]: Month number (1-12) if valid, None if invalid
    """
    return MONTH_MAP.get(month_str.strip().lower())

def validate_month_year(month_str: str, year: int) -> Optional[datetime]:
    """
    Validate and return a datetime object for the first day of the given month and year.

    Args:
        month_str (str): Month name (e.g., 'January', 'Jan')
        year (int): Year (e.g., 2023)

    Returns:
        Optional[datetime]: The datetime object if valid, None if invalid
    """
    month_num = get_month_number(month_str)
    if month_num is None:
        return None
    
    try:
        start_date = datetime(year=year, month=month_num, day=1)
        return start_date
    except ValueError:
        return None

def format_currency(amount: float, currency_symbol: str) -> str:
    """
    Format currency with thousands separator and currency symbol.
    
    Args:
        amount (float): The amount to format
        currency_symbol (str): The currency symbol to use (e.g., '$', '€', '£')
    
    Returns:
        str: Formatted currency string
    """
    return f"{currency_symbol}{amount:,.2f}"

def validate_currency_choice(currency_choice: str) -> str:
    """
    Validate and return the appropriate currency symbol.
    
    Args:
        currency_choice (str): User's currency choice ('euro', 'dollar', 'sterling')
    
    Returns:
        str: Currency symbol ('€', '$', '£')
    
    Raises:
        ValueError: If currency choice is invalid
    """
    currency_map = {
        'euro': '€',
        'dollar': '$',
        'sterling': '£'
    }
    
    choice = currency_choice.strip().lower()
    if choice not in currency_map:
        raise ValueError(
            f"Invalid currency choice. Must be one of: {', '.join(currency_map.keys())}"
        )
    
    return currency_map[choice]

def validate_file_name(file_name: str) -> str:
    """
    Validate and clean file name for CSV export.
    
    Args:
        file_name (str): The proposed file name
    
    Returns:
        str: Cleaned file name with .csv extension
    
    Raises:
        ValueError: If file name contains invalid characters or is a reserved name
    """
    import re
    from pathlib import Path
    
    # Clean up the filename
    file_name = file_name.strip()
    
    # Remove .csv extension if present, we'll add it back later
    if file_name.lower().endswith('.csv'):
        file_name = file_name[:-4]
    
    # Strict filename validation
    if not re.match(r'^[\w\-\.]+$', file_name):
        raise ValueError(
            "Invalid filename. Only letters, numbers, hyphen (-), "
            "underscore (_), and period (.) are allowed"
        )
    
    # Block reserved system filenames
    if file_name.lower() in {'settings', 'config', 'con', 'prn', 'aux', 'nul'}:
        raise ValueError("Reserved system filename not permitted")
    
    # Add .csv extension
    file_name = file_name + '.csv'
    
    # Prevent directory traversal and normalize path
    try:
        clean_path = Path(file_name).resolve().relative_to(Path.cwd())
        return str(clean_path)
    except ValueError:
        raise ValueError("Filename cannot contain path components")
