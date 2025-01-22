"""Tests for core functionality."""

import pytest
from decimal import Decimal, InvalidOperation
from datetime import datetime
from hypothesis import given, strategies as st

from mortgage_calculator.core.calculations import (
    calculate_monthly_payment,
    create_amortization_schedule,
    validate_loan_inputs
)
from mortgage_calculator.core.validation import (
    validate_month_year,
    get_month_number,
    format_currency,
    validate_currency_choice,
    validate_file_name
)

# Test Core Calculations

def test_calculate_monthly_payment_standard():
    """Test monthly payment calculation with standard values."""
    principal = Decimal('100000')
    annual_rate = Decimal('5')
    months = 360  # 30 years
    expected = Decimal('536.82')  # Pre-calculated value
    result = calculate_monthly_payment(principal, annual_rate, months)
    assert abs(result - expected) < Decimal('0.01')

def test_calculate_monthly_payment_zero_interest():
    """Test monthly payment calculation with zero interest rate."""
    principal = Decimal('100000')
    annual_rate = Decimal('0')
    months = 360
    expected = Decimal('277.78')  # 100000/360
    result = calculate_monthly_payment(principal, annual_rate, months)
    assert abs(result - expected) < Decimal('0.01')

def test_calculate_monthly_payment_invalid_inputs():
    """Test monthly payment calculation with invalid inputs."""
    with pytest.raises(ValueError):
        calculate_monthly_payment(Decimal('-100000'), Decimal('5'), 360)
    with pytest.raises(ValueError):
        calculate_monthly_payment(Decimal('100000'), Decimal('5'), 0)

def test_validate_loan_inputs():
    """Test loan input validation."""
    # Valid inputs
    validate_loan_inputs(Decimal('100000'), Decimal('5'), 360)
    
    # Invalid inputs
    with pytest.raises(ValueError):
        validate_loan_inputs(Decimal('0'), Decimal('5'), 360)
    with pytest.raises(ValueError):
        validate_loan_inputs(Decimal('100000'), Decimal('-1'), 360)
    with pytest.raises(ValueError):
        validate_loan_inputs(Decimal('100000'), Decimal('5'), 0)
    with pytest.raises(ValueError):
        validate_loan_inputs(Decimal('2000000000'), Decimal('5'), 360)

# Test Validation Functions

def test_format_currency():
    """Test currency formatting."""
    assert format_currency(1234.56, '€') == '€1,234.56'
    assert format_currency(1000000, '$') == '$1,000,000.00'
    assert format_currency(0.99, '£') == '£0.99'

def test_get_month_number():
    """Test month name to number conversion."""
    assert get_month_number('January') == 1
    assert get_month_number('jan') == 1
    assert get_month_number('December') == 12
    assert get_month_number('dec') == 12
    assert get_month_number('invalid') is None

def test_validate_month_year():
    """Test month and year validation."""
    assert validate_month_year('January', 2023) is not None
    assert validate_month_year('jan', 2023) is not None
    assert validate_month_year('invalid', 2023) is None
    assert validate_month_year('January', -1) is None

def test_validate_currency_choice():
    """Test currency choice validation."""
    assert validate_currency_choice('euro') == '€'
    assert validate_currency_choice('dollar') == '$'
    assert validate_currency_choice('sterling') == '£'
    with pytest.raises(ValueError):
        validate_currency_choice('invalid')

def test_validate_file_name():
    """Test filename validation."""
    # Valid filenames
    assert validate_file_name('test.csv') == 'test.csv'
    assert validate_file_name('my-file.csv') == 'my-file.csv'
    assert validate_file_name('file_1.csv') == 'file_1.csv'
    
    # Invalid filenames
    with pytest.raises(ValueError):
        validate_file_name('../test.csv')  # Path traversal
    with pytest.raises(ValueError):
        validate_file_name('test$.csv')  # Invalid characters
    with pytest.raises(ValueError):
        validate_file_name('con.csv')  # Reserved name

# Integration Tests

def test_full_amortization_schedule():
    """Test complete amortization schedule generation."""
    principal = Decimal('100000')
    annual_rate = Decimal('5')
    months = 360
    start_date = datetime(2023, 1, 1)
    
    schedule, total_interest = create_amortization_schedule(
        principal, annual_rate, months, start_date
    )
    
    # Test schedule properties
    assert len(schedule) == months
    assert all(payment['Payment'] > Decimal('0') for payment in schedule)
    assert all(payment['Remaining Balance'] >= Decimal('0') for payment in schedule)
    assert schedule[-1]['Remaining Balance'] < Decimal('0.01')  # Final balance ~0
    
    # Test total interest is positive
    assert total_interest > Decimal('0')
    
    # Test payment breakdown
    first_payment = schedule[0]
    assert first_payment['Principal Payment'] > Decimal('0')
    assert first_payment['Interest Payment'] > Decimal('0')
    assert abs(first_payment['Payment'] - (
        first_payment['Principal Payment'] + first_payment['Interest Payment']
    )) < Decimal('0.01')

# Property-based Tests

@given(
    principal=st.decimals(min_value=1000, max_value=1000000, places=2),
    annual_rate=st.decimals(min_value=0, max_value=25, places=2),
    months=st.integers(min_value=12, max_value=360)
)
def test_payment_calculation_properties(principal, annual_rate, months):
    """Property-based test for payment calculations."""
    principal = Decimal(str(principal))
    annual_rate = Decimal(str(annual_rate))
    
    # Calculate monthly payment
    monthly_payment = calculate_monthly_payment(principal, annual_rate, months)
    
    # Properties that should always hold
    assert monthly_payment > Decimal('0')
    if annual_rate == Decimal('0'):
        assert monthly_payment == principal / Decimal(months)
    else:
        assert monthly_payment > (principal / Decimal(months))
