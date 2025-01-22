"""Tests for input/output functionality."""

import pytest
from decimal import Decimal
from datetime import datetime
import os
import csv
from unittest.mock import patch

from mortgage_calculator.io.export import (
    export_amortization_schedule_to_csv,
    print_loan_summary,
    print_amortization_schedule
)

# Test CSV Export
def test_export_amortization_schedule(temp_output_dir, sample_schedule):
    """Test CSV export functionality."""
    # Test parameters
    file_name = 'test_schedule.csv'  # Just the filename, not the full path
    currency_symbol = '€'
    principal = Decimal('100000')
    annual_rate = Decimal('5')
    months = 360
    monthly_payment = Decimal('1000')
    total_interest = Decimal('10000')

    # Change to temp directory for the test
    current_dir = os.getcwd()
    os.chdir(temp_output_dir)
    
    try:
        # Export the schedule
        export_amortization_schedule_to_csv(
            sample_schedule,
            file_name,
            currency_symbol,
            principal,
            annual_rate,
            months,
            monthly_payment,
            total_interest
        )

        # Verify file exists
        assert os.path.exists(file_name)

        # Read and verify content
        with open(file_name, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

            # Check header sections
            assert rows[0][0] == 'Loan Summary'
            assert 'Principal Amount' in rows[1][0]
            assert 'Amortization Schedule' in rows[8][0]

            # Check data rows
            header_row = rows[9]
            assert 'Date' in header_row
            assert 'Payment' in header_row
            assert 'LTV' in header_row

            # Check first data row
            first_data_row = rows[10]
            assert 'January 2023' in first_data_row[0]
            assert '€1,000.00' in first_data_row[2]  # Payment
    
    finally:
        # Change back to original directory
        os.chdir(current_dir)

def test_export_with_invalid_filename(sample_schedule):
    """Test CSV export with invalid filename."""
    with pytest.raises(ValueError):
        export_amortization_schedule_to_csv(
            sample_schedule,
            'test$.csv',  # Invalid character
            '€',
            Decimal('100000'),
            Decimal('5'),
            360,
            Decimal('1000'),
            Decimal('10000')
        )

# Test Console Output
def test_print_loan_summary(capsys):
    """Test loan summary printing."""
    print_loan_summary(
        principal=Decimal('100000'),
        annual_rate=Decimal('5'),
        months=360,
        monthly_payment=Decimal('1000'),
        total_interest=Decimal('10000'),
        currency_symbol='€'
    )
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert 'Loan Summary' in output
    assert '€100,000.00' in output
    assert '5%' in output
    assert '30 years' in output
    assert '€1,000.00' in output

def test_print_amortization_schedule(capsys, sample_schedule):
    """Test amortization schedule printing."""
    print_amortization_schedule(sample_schedule, '€')
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert 'Amortization Schedule' in output
    assert 'January 2023' in output
    assert '€1,000.00' in output
    assert '99.2%' in output

# Test CLI Input Functions
@patch('builtins.input')
def test_get_loan_amount(mock_input):
    """Test loan amount input."""
    from mortgage_calculator.io.cli import get_loan_amount
    
    # Test valid input
    mock_input.return_value = '100000'
    result = get_loan_amount()
    assert result == Decimal('100000')
    
    # Test invalid input
    mock_input.return_value = 'invalid'
    result = get_loan_amount()
    assert result is None

@patch('builtins.input')
def test_get_currency_symbol(mock_input):
    """Test currency choice input."""
    from mortgage_calculator.io.cli import get_currency_symbol
    
    # Test valid inputs
    mock_input.side_effect = ['euro']
    result = get_currency_symbol()
    assert result == '€'
    
    mock_input.side_effect = ['dollar']
    result = get_currency_symbol()
    assert result == '$'
    
    mock_input.side_effect = ['sterling']
    result = get_currency_symbol()
    assert result == '£'

@patch('builtins.input')
def test_get_visualization_preference(mock_input):
    """Test visualization preference input."""
    from mortgage_calculator.io.cli import get_visualization_preference
    
    # Test 'yes' responses
    for response in ['yes', 'y', 'YES', 'Y']:
        mock_input.return_value = response
        assert get_visualization_preference() is True
    
    # Test 'no' responses
    for response in ['no', 'n', 'NO', 'N']:
        mock_input.return_value = response
        assert get_visualization_preference() is False

@patch('builtins.input')
def test_get_export_filename(mock_input):
    """Test export filename input."""
    from mortgage_calculator.io.cli import get_export_filename
    
    # Test valid filename
    mock_input.return_value = 'test.csv'
    result = get_export_filename()
    assert result == 'test.csv'
