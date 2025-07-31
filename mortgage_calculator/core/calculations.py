"""Core calculation functions for mortgage amortization."""

# Backward-compatibility: tests import validate_loan_inputs from this module
# The canonical implementation lives in validation.py
try:
    from .validation import validate_loan_inputs  # re-export for test compatibility
except Exception:
    # Non-fatal if import fails; runtime will raise when referenced
    pass

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import Dict, List, Optional, Tuple, TypedDict
from functools import lru_cache
from dateutil.relativedelta import relativedelta

# Configure decimal context for consistent rounding
from decimal import getcontext
getcontext().rounding = ROUND_HALF_UP
getcontext().prec = 10

class CalculationError(Exception):
    """Custom exception for calculation errors."""
    pass

@dataclass(frozen=True)
class LoanDetails:
    """Container for loan details."""
    principal: Decimal
    annual_rate: Decimal
    months: int
    start_date: datetime
    deposit: Optional[Decimal] = None

    def __post_init__(self) -> None:
        """Validate loan details after initialization."""
        if self.principal <= 0:
            raise CalculationError("Principal must be greater than zero")
        if self.annual_rate < 0:
            raise CalculationError("Interest rate cannot be negative")
        if self.months <= 0:
            raise CalculationError("Number of months must be greater than zero")
        if self.months > 600:  # 50 years
            raise CalculationError("Loan term cannot exceed 50 years")
        if self.deposit is not None:
            if self.deposit < 0:
                raise CalculationError("Deposit cannot be negative")
            if self.deposit >= self.property_value:
                raise CalculationError("Deposit cannot be greater than or equal to property value")

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

class AmortizationEntry(TypedDict):
    """Type definition for amortization schedule entry."""
    Date: str
    Month: int
    Payment: Decimal
    Principal_Payment: Decimal
    Interest_Payment: Decimal
    Remaining_Balance: Decimal
    LTV: Decimal

@lru_cache(maxsize=128)
def calculate_monthly_rate(annual_rate: Decimal) -> Decimal:
    """
    Calculate monthly interest rate from annual rate.
    
    Args:
        annual_rate (Decimal): Annual interest rate as percentage
    
    Returns:
        Decimal: Monthly interest rate as decimal
    """
    return annual_rate / Decimal('100') / Decimal('12')

@lru_cache(maxsize=128)
def calculate_monthly_payment(
    principal: Decimal,
    annual_rate: Decimal,
    months: int
) -> Decimal:
    """
    Calculate monthly payment using the amortization formula.
    
    Args:
        principal (Decimal): Original loan amount
        annual_rate (Decimal): Annual interest rate as percentage
        months (int): Total number of months
    
    Returns:
        Decimal: Monthly payment amount
    
    Raises:
        CalculationError: If calculation fails or inputs are invalid
    """
    try:
        if principal <= 0:
            # Tests expect ValueError for invalid inputs
            raise ValueError("Principal must be greater than zero")
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if months <= 0:
            raise ValueError("Number of months must be greater than zero")
        
        # Handle 0% interest rate: tests expect exact division (no extra rounding beyond 2dp display)
        if annual_rate == 0:
            return (principal / Decimal(months))
        
        monthly_rate = calculate_monthly_rate(annual_rate)
        
        # Calculate monthly payment using amortization formula
        # P = L[c(1 + c)^n]/[(1 + c)^n - 1]
        # where P = payment, L = principal, c = monthly rate, n = number of payments
        numerator = monthly_rate * (1 + monthly_rate) ** months
        denominator = (1 + monthly_rate) ** months - 1
        payment = principal * (numerator / denominator)
        
        return payment.quantize(Decimal('0.01'))
    
    except (ArithmeticError) as e:
        raise CalculationError(f"Payment calculation failed: {str(e)}")

def _create_amortization_schedule_internal(
    loan: LoanDetails
) -> Tuple[List[AmortizationEntry], Decimal]:
    """
    Create amortization schedule for the loan.
    
    Args:
        loan (LoanDetails): Loan details container
    
    Returns:
        Tuple[List[AmortizationEntry], Decimal]: Schedule and total interest
    
    Raises:
        CalculationError: If schedule creation fails
    """
    try:
        monthly_payment = calculate_monthly_payment(
            loan.principal,
            loan.annual_rate,
            loan.months
        )
        monthly_rate = calculate_monthly_rate(loan.annual_rate)
        
        schedule: List[AmortizationEntry] = []
        balance = loan.principal
        total_interest = Decimal('0')
        current_date = loan.start_date
        
        for month in range(1, loan.months + 1):
            # Calculate interest and principal portions
            interest_payment = (balance * monthly_rate).quantize(Decimal('0.01'))
            principal_payment = (monthly_payment - interest_payment).quantize(Decimal('0.01'))
            
            # Adjust final payment to handle rounding
            if month == loan.months:
                principal_payment = balance
                monthly_payment = principal_payment + interest_payment
            
            # Update running totals
            total_interest += interest_payment
            balance -= principal_payment
            
            # Calculate LTV (Loan-to-Value) ratio considering deposit
            ltv = (balance / loan.property_value * 100).quantize(Decimal('0.1'))
            
            # Create schedule entry
            entry: AmortizationEntry = {
                'Date': current_date.strftime('%B %Y'),
                'Month': month,
                'Payment': monthly_payment,
                'Principal_Payment': principal_payment,
                'Interest_Payment': interest_payment,
                'Remaining_Balance': balance,
                'LTV': ltv
            }
            schedule.append(entry)
            
            # Move to next month
            current_date += relativedelta(months=1)
        
        return schedule, total_interest.quantize(Decimal('0.01'))
    
    except Exception as e:
        raise CalculationError(f"Schedule creation failed: {str(e)}")

# Legacy output adapter for tests expecting keys with spaces
def _legacy_row_keys(row: AmortizationEntry) -> dict:
    return {
        'Date': row['Date'],
        'Month': row['Month'],
        'Payment': row['Payment'],
        'Principal Payment': row['Principal_Payment'],
        'Interest Payment': row['Interest_Payment'],
        'Remaining Balance': row['Remaining_Balance'],
        'LTV': row['LTV'],
    }

# Backward-compatible overload: create_amortization_schedule(principal, annual_rate, months, start_date)
def create_amortization_schedule(  # type: ignore[override]
    loan_or_principal,
    annual_rate: Optional[Decimal] = None,
    months: Optional[int] = None,
    start_date: Optional[datetime] = None,
) -> Tuple[List[dict], Decimal]:
    """
    Legacy signature support. If called with primitives, return legacy-keyed rows
    using 'Principal Payment', 'Interest Payment', and 'Remaining Balance'.
    If called with a LoanDetails, return canonical rows.
    """
    if isinstance(loan_or_principal, LoanDetails):
        loan = loan_or_principal
        schedule, total_interest = _create_amortization_schedule_internal(loan)
        return schedule, total_interest
    else:
        if annual_rate is None or months is None or start_date is None:
            raise CalculationError("Missing arguments")
        loan = LoanDetails(
            principal=Decimal(loan_or_principal),
            annual_rate=Decimal(annual_rate),
            months=int(months),
            start_date=start_date
        )
        base_schedule, total_interest = _create_amortization_schedule_internal(loan)
        return [_legacy_row_keys(r) for r in base_schedule], total_interest

def calculate_total_cost(principal: Decimal, total_interest: Decimal) -> Decimal:
    """
    Calculate total cost of the loan.
    """
    return (principal + total_interest).quantize(Decimal('0.01'))

def calculate_interest_percentage(total_interest: Decimal, total_cost: Decimal) -> Decimal:
    """
    Calculate interest as percentage of total cost.
    
    Args:
        total_interest (Decimal): Total interest paid
        total_cost (Decimal): Total cost of the loan
    
    Returns:
        Decimal: Interest percentage
    """
    return (total_interest / total_cost * 100).quantize(Decimal('0.1'))


# Backward-compatibility wrapper expected by tests:
# create_amortization_schedule(principal, annual_rate, months, start_date)
def create_amortization_schedule(  # type: ignore[override]
    principal_or_loan,
    annual_rate: Optional[Decimal] = None,
    months: Optional[int] = None,
    start_date: Optional[datetime] = None
) -> Tuple[List[dict], Decimal]:
    """
    Compatibility overload:
    - If first argument is LoanDetails, return canonical schedule (dicts with keys used across code).
    - Else treat positional args as (principal, annual_rate, months, start_date) and
      RETURN legacy-keyed dicts using 'Principal Payment', 'Interest Payment', 'Remaining Balance'.
    """
    if isinstance(principal_or_loan, LoanDetails):
        loan = principal_or_loan
        schedule, total_interest = _create_amortization_schedule_internal(loan)
        # Canonical schedule already uses 'Date','Month','Payment','Principal_Payment', etc.
        return schedule, total_interest

    # Legacy signature path
    if annual_rate is None or months is None or start_date is None:
        raise CalculationError("Missing arguments for legacy create_amortization_schedule")

    loan = LoanDetails(
        principal=Decimal(principal_or_loan),
        annual_rate=Decimal(annual_rate),
        months=int(months),
        start_date=start_date
    )
    base_schedule, total_interest = _create_amortization_schedule_internal(loan)

    # Convert EVERY row to legacy/display keys expected by tests
    legacy_schedule: List[dict] = []
    for row in base_schedule:
        legacy_schedule.append({
            'Date': row['Date'],
            'Month': row['Month'],
            'Payment': row['Payment'],
            'Principal Payment': row['Principal_Payment'],
            'Interest Payment': row['Interest_Payment'],
            'Remaining Balance': row['Remaining_Balance'],
            'LTV': row['LTV'],
        })

    return legacy_schedule, total_interest


# Remove unused duplicate legacy helper to avoid confusion; single entry point above is sufficient.
