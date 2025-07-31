"""File export operations for mortgage calculator."""

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Literal, Union

from ..core.validation import format_currency

class ExportError(Exception):
    """Custom exception for export operations."""
    pass

@dataclass
class LoanSummary:
    """Container for loan summary information."""
    principal: Decimal
    annual_rate: Decimal
    months: int
    monthly_payment: Decimal
    total_interest: Decimal
    currency_symbol: str
    deposit: Optional[Decimal] = None

    @property
    def total_cost(self) -> Decimal:
        """Calculate total cost of the loan."""
        return self.principal + self.total_interest

    @property
    def interest_percentage(self) -> float:
        """Calculate interest as percentage of total cost."""
        return float((self.total_interest / self.total_cost) * 100)

    @property
    def years(self) -> int:
        """Get whole years from months."""
        return self.months // 12

    @property
    def remaining_months(self) -> int:
        """Get remaining months after years."""
        return self.months % 12

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

    def format_amount(self, amount: Decimal) -> str:
        """Format monetary amount with currency symbol."""
        return format_currency(amount, self.currency_symbol)

def export_amortization_schedule(
    schedule: List[dict],
    loan_summary: LoanSummary,
    file_path: str,
    format_type: Literal["csv", "txt"] = "csv"
) -> None:
    """
    Export the amortization schedule to a file.

    Args:
        schedule (List[dict]): The amortization schedule
        loan_summary (LoanSummary): Loan summary information
        file_path (str): Path for the output file
        format_type (Literal["csv", "txt"]): Output format type

    Raises:
        ExportError: If there's an error during export
    """
    try:
        # Create output directory if needed
        output_dir = Path(file_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if format_type == "csv":
            _export_to_csv(schedule, loan_summary, file_path)
        elif format_type == "txt":
            _export_to_txt(schedule, loan_summary, file_path)
        else:
            raise ExportError(f"Unsupported format type: {format_type}")
        
    except IOError as e:
        raise ExportError(f"Failed to write to file: {str(e)}") from e
    except Exception as e:
        raise ExportError(f"Export failed: {str(e)}") from e


def export_amortization_schedule_to_csv(
    schedule: List[dict],
    file_name: str,
    currency_symbol: str,
    principal: Decimal,
    annual_rate: Decimal,
    months: int,
    monthly_payment: Decimal,
    total_interest: Decimal,
    deposit: Optional[Decimal] = None,
) -> None:
    """
    Backward-compatible helper expected by tests.
    Constructs a LoanSummary and delegates to export_amortization_schedule with CSV format.
    """
    # Validate filename using existing validator behavior
    from ..core.validation import validate_file_name
    file_name = validate_file_name(file_name)

    loan_summary = LoanSummary(
        principal=principal,
        annual_rate=annual_rate,
        months=months,
        monthly_payment=monthly_payment,
        total_interest=total_interest,
        currency_symbol=currency_symbol,
        deposit=deposit,
    )
    export_amortization_schedule(schedule, loan_summary, file_name, format_type="csv")


# NOTE: Remove duplicate definition to avoid shadowing the validated one above

def _export_to_csv(
    schedule: List[dict],
    loan_summary: LoanSummary,
    file_path: str
) -> None:
    """Export schedule to CSV format."""
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
    
        # Columns for both summary and schedule rows
        fieldnames = [
            'Date', 'Month', 'Payment', 'Principal_Payment',
            'Interest_Payment', 'LTV', 'Remaining_Balance'
        ]
        dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
        # Write summary rows FIRST (tests expect 'Loan Summary' at row[0][0])
        # Tests also read rows[1][0] and expect it to contain 'Principal Amount'
        summary_rows = [
            {
                'Date': 'Loan Summary',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            },
            {
                'Date': 'Principal Amount',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': loan_summary.format_amount(loan_summary.principal)
            },
            *([] if loan_summary.deposit is None else [{
                'Date': 'Deposit',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': f"{loan_summary.format_amount(loan_summary.deposit)} ({loan_summary.deposit_percentage:.1f}%)"
            }]),
            {
                'Date': 'Monthly Payment',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': loan_summary.format_amount(loan_summary.monthly_payment)
            },
            {
                'Date': 'Annual Interest Rate',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': f"{loan_summary.annual_rate}%"
            },
            {
                'Date': 'Term',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': f"{loan_summary.years} years {loan_summary.remaining_months} months"
            },
            {
                'Date': 'Total Interest',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': loan_summary.format_amount(loan_summary.total_interest)
            },
            {
                'Date': 'Total Cost',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': loan_summary.format_amount(loan_summary.total_cost)
            },
            {
                'Date': '',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            },
            {
                'Date': 'Amortization Schedule',
                'Month': '',
                'Payment': '',
                'Principal_Payment': '',
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            }
        ]
        
        # Write summary rows
        for row in summary_rows:
            dict_writer.writerow(row)
        
        # Then write a blank line-equivalent (already added at end of summary_rows) and a label row included above
        # Now write the header BEFORE schedule data to satisfy CSV readability after the summary block
        dict_writer.writeheader()
        
        # Write schedule rows
        def _normalize_payment_row(row: dict) -> dict:
            # Accept both display-style keys with spaces and internal snake_case keys
            principal_key = 'Principal_Payment' if 'Principal_Payment' in row else ('Principal Payment' if 'Principal Payment' in row else None)
            interest_key = 'Interest_Payment' if 'Interest_Payment' in row else ('Interest Payment' if 'Interest Payment' in row else None)
            balance_key = 'Remaining_Balance' if 'Remaining_Balance' in row else ('Remaining Balance' if 'Remaining Balance' in row else None)
            ltv_key = 'LTV'
            if principal_key is None or interest_key is None or balance_key is None or 'Payment' not in row or 'Date' not in row or 'Month' not in row or ltv_key not in row:
                raise KeyError("Schedule row missing required keys")
            return {
                'Date': row['Date'],
                'Month': row['Month'],
                'Payment': loan_summary.format_amount(row['Payment']),
                'Principal_Payment': loan_summary.format_amount(row[principal_key]),
                'Interest_Payment': loan_summary.format_amount(row[interest_key]),
                'LTV': f"{row[ltv_key]:.1f}%",
                'Remaining_Balance': loan_summary.format_amount(row[balance_key])
            }
        
        for payment in schedule:
            dict_writer.writerow(_normalize_payment_row(payment))

def _export_to_txt(
    schedule: List[dict],
    loan_summary: LoanSummary,
    file_path: str
) -> None:
    """Export schedule to formatted text file."""
    with open(file_path, 'w') as txt_file:
        # Write loan summary
        txt_file.write("=== Loan Summary ===\n")
        txt_file.write(f"Property Value: {loan_summary.format_amount(loan_summary.property_value)}\n")
        if loan_summary.deposit is not None:
            txt_file.write(
                f"Deposit: {loan_summary.format_amount(loan_summary.deposit)} "
                f"({loan_summary.deposit_percentage:.1f}%)\n"
            )
        txt_file.write(f"Loan Amount: {loan_summary.format_amount(loan_summary.principal)}\n")
        txt_file.write(f"Annual Interest Rate: {loan_summary.annual_rate}%\n")
        txt_file.write(
            f"Loan Term: {loan_summary.years} years {loan_summary.remaining_months} months\n"
        )
        txt_file.write(
            f"Monthly Payment: {loan_summary.format_amount(loan_summary.monthly_payment)}\n"
        )
        txt_file.write(
            f"Total Interest: {loan_summary.format_amount(loan_summary.total_interest)} "
            f"({loan_summary.interest_percentage:.1f}% of total cost)\n"
        )
        txt_file.write(f"Total Cost: {loan_summary.format_amount(loan_summary.total_cost)}\n")
        txt_file.write("=" * 80 + "\n\n")
        
        # Write schedule header
        header = (
            f"{'Date':<15}{'Month':<7}{'Payment':<15}"
            f"{'Principal':<18}{'Interest':<15}{'LTV':<8}{'Balance':<18}\n"
        )
        txt_file.write("=== Amortization Schedule ===\n")
        txt_file.write(header)
        txt_file.write("-" * 80 + "\n")
        
        # Write schedule entries
        for payment in schedule:
            txt_file.write(
                f"{payment['Date']:<15}"
                f"{payment['Month']:<7}"
                f"{loan_summary.format_amount(payment['Payment']):<15}"
                f"{loan_summary.format_amount(payment['Principal_Payment']):<18}"
                f"{loan_summary.format_amount(payment['Interest_Payment']):<15}"
                f"{payment['LTV']:.1f}%{' ':<3}"
                f"{loan_summary.format_amount(payment['Remaining_Balance']):<18}\n"
            )

def print_loan_summary(
    principal: Decimal = None,
    annual_rate: Decimal = None,
    months: int = None,
    monthly_payment: Decimal = None,
    total_interest: Decimal = None,
    currency_symbol: str = None,
    deposit: Optional[Decimal] = None,
    loan_summary: Optional[LoanSummary] = None,
) -> None:
    """
    Backward-compatible print function that accepts keyword args as used in tests,
    while still supporting passing a LoanSummary instance via loan_summary.
    """
    if loan_summary is None:
        if None in (principal, annual_rate, months, monthly_payment, total_interest, currency_symbol):
            raise TypeError("Missing required arguments for print_loan_summary")
        loan_summary = LoanSummary(
            principal=principal,
            annual_rate=annual_rate,
            months=months,
            monthly_payment=monthly_payment,
            total_interest=total_interest,
            currency_symbol=currency_symbol,
            deposit=deposit,
        )

    print("\n=== Loan Summary ===")
    print(f"Property Value: {loan_summary.format_amount(loan_summary.property_value)}")
    if loan_summary.deposit is not None:
        print(
            f"Deposit: {loan_summary.format_amount(loan_summary.deposit)} "
            f"({loan_summary.deposit_percentage:.1f}%)"
        )
    print(f"Loan Amount: {loan_summary.format_amount(loan_summary.principal)}")
    print(f"Annual Interest Rate: {loan_summary.annual_rate}%")
    print(
        f"Loan Term: {loan_summary.years} years {loan_summary.remaining_months} months"
    )
    print(f"Monthly Payment: {loan_summary.format_amount(loan_summary.monthly_payment)}")
    print(
        f"Total Interest: {loan_summary.format_amount(loan_summary.total_interest)} "
        f"({loan_summary.interest_percentage:.1f}% of total cost)"
    )
    print(f"Total Cost: {loan_summary.format_amount(loan_summary.total_cost)}")
    print("=" * 80)

def print_amortization_schedule(
    schedule: List[dict],
    loan_summary: Union["LoanSummary", str],
    max_entries: Optional[int] = None
) -> None:
    """
    Print the amortization schedule in a formatted table to the console.
    
    Args:
        schedule (List[dict]): The amortization schedule
        loan_summary (LoanSummary): Loan summary information or currency symbol (legacy)
        max_entries (Optional[int]): Maximum number of entries to print
    """
    header = (
        f"{'Date':<15}{'Month':<7}{'Payment':<15}"
        f"{'Principal':<18}{'Interest':<15}{'LTV':<8}{'Balance':<18}"
    )
    print("\n=== Amortization Schedule ===")
    print(header)
    print("-" * len(header))
    
    # Normalize legacy usage where loan_summary might be a currency symbol string
    if isinstance(loan_summary, str):
        class _TmpSummary:
            def __init__(self, symbol: str) -> None:
                self.currency_symbol = symbol
            def format_amount(self, amount: Decimal) -> str:
                from ..core.validation import format_currency
                return format_currency(amount, self.currency_symbol)
        legacy_summary = _TmpSummary(loan_summary)
    else:
        legacy_summary = loan_summary

    display_schedule = schedule[:max_entries] if max_entries else schedule

    def _norm(row: dict) -> dict:
        principal_key = 'Principal_Payment' if 'Principal_Payment' in row else ('Principal Payment' if 'Principal Payment' in row else None)
        interest_key = 'Interest_Payment' if 'Interest_Payment' in row else ('Interest Payment' if 'Interest Payment' in row else None)
        balance_key = 'Remaining_Balance' if 'Remaining_Balance' in row else ('Remaining Balance' if 'Remaining Balance' in row else None)
        return {
            'Date': row['Date'],
            'Month': row['Month'],
            'Payment': row['Payment'],
            'Principal_Payment': row[principal_key],
            'Interest_Payment': row[interest_key],
            'LTV': row['LTV'],
            'Remaining_Balance': row[balance_key],
        }

    for payment in map(_norm, display_schedule):
        print(
            f"{payment['Date']:<15}"
            f"{payment['Month']:<7}"
            f"{legacy_summary.format_amount(payment['Payment']):<15}"
            f"{legacy_summary.format_amount(payment['Principal_Payment']):<18}"
            f"{legacy_summary.format_amount(payment['Interest_Payment']):<15}"
            f"{payment['LTV']:.1f}%{' ':<3}"
            f"{legacy_summary.format_amount(payment['Remaining_Balance']):<18}"
        )
    
    if max_entries and len(schedule) > max_entries:
        print(f"\n... {len(schedule) - max_entries} more entries ...")
