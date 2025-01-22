"""Core calculation functions for mortgage amortization."""

from decimal import Decimal, ROUND_HALF_EVEN
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Tuple, Optional

# Configure decimal context
from decimal import getcontext
getcontext().prec = 12
getcontext().rounding = ROUND_HALF_EVEN

def calculate_monthly_payment(principal: Decimal, annual_rate: Decimal, months: int) -> Decimal:
    """
    Calculate the monthly payment for a loan.

    Args:
        principal (Decimal): The loan amount.
        annual_rate (Decimal): The annual interest rate in percent.
        months (int): The loan term in months.

    Returns:
        Decimal: The monthly payment amount.

    Raises:
        ValueError: If principal is negative or zero, or if months is zero.
    """
    if principal <= 0:
        raise ValueError("Principal must be greater than zero")
    if months <= 0:
        raise ValueError("Number of months must be greater than zero")
    
    if annual_rate == 0:
        monthly_payment = principal / Decimal(months)
    else:
        monthly_rate = (annual_rate / Decimal(100)) / Decimal(12)
        numerator = principal * monthly_rate * (1 + monthly_rate) ** months
        denominator = ((1 + monthly_rate) ** months) - Decimal(1)
        monthly_payment = numerator / denominator
    
    return monthly_payment

def create_amortization_schedule(
    principal: Decimal,
    annual_rate: Decimal,
    months: int,
    start_date: datetime
) -> Tuple[List[Dict], Decimal]:
    """
    Create an amortization schedule for the loan.

    Args:
        principal (Decimal): The loan amount.
        annual_rate (Decimal): The annual interest rate in percent.
        months (int): The loan term in months.
        start_date (datetime): The start date of the loan.

    Returns:
        tuple: A tuple containing the amortization schedule list and total interest paid.
    """
    monthly_payment = calculate_monthly_payment(principal, annual_rate, months)
    balance = principal
    current_date = start_date
    amortization_schedule = []
    total_interest = Decimal('0.00')

    for i in range(1, months + 1):
        if annual_rate == 0:
            interest = Decimal('0.00')
        else:
            monthly_rate = (annual_rate / Decimal(100)) / Decimal(12)
            interest = balance * monthly_rate

        principal_payment = monthly_payment - interest

        if balance - principal_payment < Decimal('-0.01'):
            principal_payment = balance
            monthly_payment = principal_payment + interest
            balance = Decimal('0.00')
        else:
            balance -= principal_payment
            balance = max(balance, Decimal('0.00'))

        ltv = (balance / principal) * Decimal('100')

        amortization_schedule.append({
            'Date': current_date.strftime("%B %Y"),
            'Month': i,
            'Payment': monthly_payment,
            'Principal Payment': principal_payment,
            'Interest Payment': interest,
            'Remaining Balance': balance,
            'LTV': ltv
        })
        current_date += relativedelta(months=1)
        total_interest += interest

    return amortization_schedule, total_interest

def validate_loan_inputs(principal: Decimal, annual_rate: Decimal, months: int) -> None:
    """
    Validate loan input parameters.

    Args:
        principal (Decimal): The loan amount.
        annual_rate (Decimal): The annual interest rate in percent.
        months (int): The loan term in months.

    Raises:
        ValueError: If any input parameters are invalid.
    """
    if principal <= 0:
        raise ValueError("Principal amount must be greater than zero.")
    if principal > Decimal('1000000000'):
        raise ValueError("Principal amount is unreasonably high (max: 1 billion).")
    
    if annual_rate < 0:
        raise ValueError("Annual interest rate cannot be negative.")
    if annual_rate > Decimal('100'):
        raise ValueError("Annual interest rate cannot exceed 100%.")
    if annual_rate > Decimal('25'):
        print("\nWarning: Interest rate is unusually high. Please verify this is correct.")
    
    if months <= 0:
        raise ValueError("Loan term must be greater than zero months.")
    if months > 600:
        raise ValueError("Loan term cannot exceed 600 months (50 years).")
    if months > 420:
        print("\nWarning: Loan term exceeds 35 years. Please verify this is correct.")
