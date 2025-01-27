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
        
        # Write loan summary section
        writer.writerow(['Loan Summary'])
        writer.writerow(['Principal Amount',
                        loan_summary.format_amount(loan_summary.principal)])
        writer.writerow(['Annual Interest Rate', f"{loan_summary.annual_rate}%"])
        writer.writerow(['Loan Term',
                        f"{loan_summary.years} years {loan_summary.remaining_months} months"])
        writer.writerow(['Monthly Payment',
                        loan_summary.format_amount(loan_summary.monthly_payment)])
        writer.writerow(['Total Interest',
                        loan_summary.format_amount(loan_summary.total_interest)])
        writer.writerow(['Total Cost',
                        loan_summary.format_amount(loan_summary.total_cost)])
        writer.writerow([])  # Empty row for spacing
        
        # Write amortization schedule
        writer.writerow(['Amortization Schedule'])
        fieldnames = [
            'Date', 'Month', 'Payment', 'Principal_Payment',
            'Interest_Payment', 'LTV', 'Remaining_Balance'
        ]
        dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        
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
        txt_file.write(f"Principal Amount: {loan_summary.format_amount(loan_summary.principal)}\n")
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
    print(f"Principal Amount: {loan_summary.format_amount(loan_summary.principal)}")
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
