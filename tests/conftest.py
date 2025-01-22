"""Test configuration and shared fixtures."""

import pytest
from decimal import Decimal
from datetime import datetime
import os
import tempfile
import shutil
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data that persists across all tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="session")
def sample_loan_data():
    """Provide sample loan data for tests."""
    return {
        'principal': Decimal('100000.00'),
        'annual_rate': Decimal('5.0'),
        'months': 360,  # 30 years
        'start_date': datetime(2023, 1, 1),
        'currency_symbol': '€'
    }

@pytest.fixture(scope="session")
def sample_schedule():
    """Provide a sample amortization schedule for tests."""
    return [
        {
            'Date': 'January 2023',
            'Month': 1,
            'Payment': Decimal('1000.00'),
            'Principal Payment': Decimal('800.00'),
            'Interest Payment': Decimal('200.00'),
            'Remaining Balance': Decimal('99200.00'),
            'LTV': Decimal('99.2')
        },
        {
            'Date': 'February 2023',
            'Month': 2,
            'Payment': Decimal('1000.00'),
            'Principal Payment': Decimal('801.67'),
            'Interest Payment': Decimal('198.33'),
            'Remaining Balance': Decimal('98398.33'),
            'LTV': Decimal('98.4')
        }
    ]

@pytest.fixture(scope="function")
def temp_output_dir(tmpdir):
    """Create a temporary directory for test outputs."""
    output_dir = tmpdir.mkdir("output")
    return Path(output_dir)

@pytest.fixture(scope="function")
def matplotlib_config():
    """Configure matplotlib for testing."""
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    return matplotlib

@pytest.fixture(autouse=True)
def cleanup_files():
    """Clean up any test files after each test."""
    yield
    # Clean up any generated files
    patterns = ['*.csv', '*.png']
    for pattern in patterns:
        for file in Path('.').glob(pattern):
            try:
                file.unlink()
            except Exception:
                pass
