"""File export operations for mortgage calculator."""

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Literal

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

def _export_to_csv(
    schedule: List[dict],
    loan_summary: LoanSummary,
    file_path: str
) -> None:
    """Export schedule to CSV format."""
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write loan summary section with consistent columns
        fieldnames = [
            'Date', 'Month', 'Payment', 'Principal_Payment',
            'Interest_Payment', 'LTV', 'Remaining_Balance'
        ]
        dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        
        # Write summary as special rows with consistent column count
        summary_rows = [
            {
                'Date': 'Loan Summary',
                'Month': '',
                'Payment': '',
                'Principal_Payment': f"Property Value: {loan_summary.format_amount(loan_summary.property_value)}",
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            },
            *([] if loan_summary.deposit is None else [{
                'Date': '',
                'Month': '',
                'Payment': '',
                'Principal_Payment': f"Deposit: {loan_summary.format_amount(loan_summary.deposit)} ({loan_summary.deposit_percentage:.1f}%)",
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            }]),
            {
                'Date': '',
                'Month': '',
                'Payment': '',
                'Principal_Payment': f"Loan Amount: {loan_summary.format_amount(loan_summary.principal)}",
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            },
            {
                'Date': '',
                'Month': '',
                'Payment': '',
                'Principal_Payment': f"Annual Rate: {loan_summary.annual_rate}%",
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            },
            {
                'Date': '',
                'Month': '',
                'Payment': '',
                'Principal_Payment': f"Term: {loan_summary.years} years {loan_summary.remaining_months} months",
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            },
            {
                'Date': '',
                'Month': '',
                'Payment': '',
                'Principal_Payment': f"Monthly Payment: {loan_summary.format_amount(loan_summary.monthly_payment)}",
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            },
            {
                'Date': '',
                'Month': '',
                'Payment': '',
                'Principal_Payment': f"Total Interest: {loan_summary.format_amount(loan_summary.total_interest)}",
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
            },
            {
                'Date': '',
                'Month': '',
                'Payment': '',
                'Principal_Payment': f"Total Cost: {loan_summary.format_amount(loan_summary.total_cost)}",
                'Interest_Payment': '',
                'LTV': '',
                'Remaining_Balance': ''
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
        # Write schedule rows
        
        for payment in schedule:
            formatted_payment = {
                'Date': payment['Date'],
                'Month': payment['Month'],
                'Payment': loan_summary.format_amount(payment['Payment']),
                'Principal_Payment': loan_summary.format_amount(payment['Principal_Payment']),
                'Interest_Payment': loan_summary.format_amount(payment['Interest_Payment']),
                'LTV': f"{payment['LTV']:.1f}%",
                'Remaining_Balance': loan_summary.format_amount(payment['Remaining_Balance'])
            }
            dict_writer.writerow(formatted_payment)

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

def print_loan_summary(loan_summary: LoanSummary) -> None:
    """
    Print a summary of the loan details to the console.

    Args:
        loan_summary (LoanSummary): Loan summary information
    """
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
    loan_summary: LoanSummary,
    max_entries: Optional[int] = None
) -> None:
    """
    Print the amortization schedule in a formatted table to the console.

    Args:
        schedule (List[dict]): The amortization schedule
        loan_summary (LoanSummary): Loan summary information
        max_entries (Optional[int]): Maximum number of entries to print
    """
    header = (
        f"{'Date':<15}{'Month':<7}{'Payment':<15}"
        f"{'Principal':<18}{'Interest':<15}{'LTV':<8}{'Balance':<18}"
    )
    print("\n=== Amortization Schedule ===")
    print(header)
    print("-" * len(header))
    
    display_schedule = schedule[:max_entries] if max_entries else schedule
    
    for payment in display_schedule:
        print(
            f"{payment['Date']:<15}"
            f"{payment['Month']:<7}"
            f"{loan_summary.format_amount(payment['Payment']):<15}"
            f"{loan_summary.format_amount(payment['Principal_Payment']):<18}"
            f"{loan_summary.format_amount(payment['Interest_Payment']):<15}"
            f"{payment['LTV']:.1f}%{' ':<3}"
            f"{loan_summary.format_amount(payment['Remaining_Balance']):<18}"
        )
    
    if max_entries and len(schedule) > max_entries:
        print(f"\n... {len(schedule) - max_entries} more entries ...")
