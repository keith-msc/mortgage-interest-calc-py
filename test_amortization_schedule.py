import pytest
from decimal import Decimal
from datetime import datetime
from hypothesis import given, strategies as st
from amortization_schedule import (
    calculate_monthly_payment,
    create_amortization_schedule,
    validate_loan_inputs,
    validate_month_year,
    get_month_number,
    format_currency
)

# Unit Tests for Core Calculations

def test_export_amortization_schedule_to_csv(monkeypatch):
    """Test CSV export functionality"""
    import os
    
    # Create a temporary working directory for testing
    test_dir = "test_output"
    os.makedirs(test_dir, exist_ok=True)
    original_dir = os.getcwd()
    os.chdir(test_dir)
    
    try:
        principal = Decimal('100000')
        annual_rate = Decimal('5')
        months = 12
        start_date = datetime(2023, 1, 1)
        
        schedule, total_interest = create_amortization_schedule(
            principal, annual_rate, months, start_date
        )
        
        from amortization_schedule import export_amortization_schedule_to_csv
        
        # Test valid export
        export_amortization_schedule_to_csv(
            schedule, "test_schedule.csv", '€', principal, annual_rate, 
            months, schedule[0]['Payment'], total_interest
        )
        assert os.path.exists("test_schedule.csv")
        
        # Test invalid filename
        with pytest.raises(ValueError):
            export_amortization_schedule_to_csv(
                schedule, "../invalid/path.csv", '€', principal, annual_rate,
                months, schedule[0]['Payment'], total_interest
            )
    finally:
        os.chdir(original_dir)
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)

def test_plot_amortization_schedule(tmp_path):
    """Test graph generation functionality"""
    principal = Decimal('100000')
    annual_rate = Decimal('5')
    months = 12
    start_date = datetime(2023, 1, 1)
    
    schedule, _ = create_amortization_schedule(
        principal, annual_rate, months, start_date
    )
    
    # Change to temporary directory for testing
    import os
    original_dir = os.getcwd()
    os.chdir(str(tmp_path))
    
    try:
        from amortization_schedule import plot_amortization_schedule
        plot_amortization_schedule(schedule, '€', principal)
        
        # Verify files were created
        assert (tmp_path / "amortization_schedule_payments.png").exists()
        assert (tmp_path / "amortization_schedule_balance.png").exists()
    finally:
        os.chdir(original_dir)

def test_main_input_validation(monkeypatch, capsys):
    """Test main function input validation"""
    from amortization_schedule import main
    from decimal import InvalidOperation
    
    def run_with_inputs(input_values):
        inputs = iter(input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        try:
            main()
        except (StopIteration, InvalidOperation):
            pass  # Expected when inputs are exhausted or invalid
    
    # Test invalid principal
    run_with_inputs(['abc'])  # Should fail with invalid decimal
    captured = capsys.readouterr()
    assert "Mortgage Amortization Calculator" in captured.out
    
    # Test invalid interest rate
    run_with_inputs(['100000', 'abc'])
    captured = capsys.readouterr()
    assert "Mortgage Amortization Calculator" in captured.out
    
    # Test invalid month
    run_with_inputs(['100000', '5', '30', '0', 'invalid'])
    captured = capsys.readouterr()
    assert "Mortgage Amortization Calculator" in captured.out

def test_calculate_monthly_payment_standard():
    """Test monthly payment calculation with standard values"""
    principal = Decimal('100000')
    annual_rate = Decimal('5')
    months = 360  # 30 years
    expected = Decimal('536.82')  # Pre-calculated value
    result = calculate_monthly_payment(principal, annual_rate, months)
    assert abs(result - expected) < Decimal('0.01')

def test_calculate_monthly_payment_zero_interest():
    """Test monthly payment calculation with zero interest rate"""
    principal = Decimal('100000')
    annual_rate = Decimal('0')
    months = 360
    expected = Decimal('277.78')  # 100000/360
    result = calculate_monthly_payment(principal, annual_rate, months)
    assert abs(result - expected) < Decimal('0.01')

def test_calculate_monthly_payment_invalid_inputs():
    """Test monthly payment calculation with invalid inputs"""
    with pytest.raises(ValueError):
        calculate_monthly_payment(Decimal('-100000'), Decimal('5'), 360)
    with pytest.raises(ValueError):
        calculate_monthly_payment(Decimal('100000'), Decimal('5'), 0)

def test_validate_loan_inputs():
    """Test loan input validation"""
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

def test_format_currency():
    """Test currency formatting"""
    assert format_currency(Decimal('1234.56'), '€') == '€1,234.56'
    assert format_currency(Decimal('1000000'), '$') == '$1,000,000.00'
    assert format_currency(Decimal('0.99'), '£') == '£0.99'

def test_get_month_number():
    """Test month name to number conversion"""
    assert get_month_number('January') == 1
    assert get_month_number('jan') == 1
    assert get_month_number('December') == 12
    assert get_month_number('dec') == 12
    assert get_month_number('invalid') is None

def test_validate_month_year():
    """Test month and year validation"""
    assert validate_month_year('January', 2023) is not None
    assert validate_month_year('jan', 2023) is not None
    assert validate_month_year('invalid', 2023) is None
    assert validate_month_year('January', -1) is None

# Integration Tests

def test_full_amortization_schedule():
    """Test complete amortization schedule generation"""
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
    assert schedule[-1]['Remaining Balance'] < Decimal('0.01')  # Final balance should be ~0
    
    # Test total interest is positive
    assert total_interest > Decimal('0')
    
    # Test payment breakdown
    first_payment = schedule[0]
    assert first_payment['Principal Payment'] > Decimal('0')
    assert first_payment['Interest Payment'] > Decimal('0')
    assert abs(first_payment['Payment'] - (first_payment['Principal Payment'] + first_payment['Interest Payment'])) < Decimal('0.01')

def test_edge_case_scenarios():
    """Test various edge case scenarios"""
    # Test very small loan amount
    schedule, _ = create_amortization_schedule(
        Decimal('1000'), Decimal('5'), 12, datetime(2023, 1, 1)
    )
    assert len(schedule) == 12
    # Allow for minor rounding differences in final balance
    assert schedule[-1]['Remaining Balance'] < Decimal('0.05')

    # Test very short loan term
    schedule, _ = create_amortization_schedule(
        Decimal('10000'), Decimal('5'), 3, datetime(2023, 1, 1)
    )
    assert len(schedule) == 3
    # Allow for minor rounding differences in final balance
    assert schedule[-1]['Remaining Balance'] < Decimal('0.03')

    # Test zero interest rate
    schedule, total_interest = create_amortization_schedule(
        Decimal('12000'), Decimal('0'), 12, datetime(2023, 1, 1)
    )
    assert total_interest == Decimal('0')
    # Allow for minor rounding differences in final balance
    assert schedule[-1]['Remaining Balance'] < Decimal('0.03')

# Property-based Tests

@given(
    principal=st.decimals(min_value=1000, max_value=1000000, places=2),
    annual_rate=st.decimals(min_value=0, max_value=25, places=2),
    months=st.integers(min_value=12, max_value=360)
)
def test_payment_calculation_properties(principal, annual_rate, months):
    """Property-based test for payment calculations"""
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

if __name__ == '__main__':
    pytest.main(['-v', '--cov=amortization_schedule', 'test_amortization_schedule.py'])
