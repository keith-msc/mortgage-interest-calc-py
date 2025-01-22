"""File export operations for mortgage calculator."""

import csv
from decimal import Decimal
from typing import List, Dict
from ..core.validation import format_currency, validate_file_name

def export_amortization_schedule_to_csv(
    schedule: List[Dict],
    file_name: str,
    currency_symbol: str,
    principal: Decimal,
    annual_rate: Decimal,
    months: int,
    monthly_payment: Decimal,
    total_interest: Decimal
) -> None:
    """
    Export the amortization schedule to a CSV file with a summary section.

    Args:
        schedule (List[Dict]): The amortization schedule
        file_name (str): Name for the CSV file
        currency_symbol (str): Currency symbol for formatting
        principal (Decimal): Original loan amount
        annual_rate (Decimal): Annual interest rate
        months (int): Total number of months
        monthly_payment (Decimal): Monthly payment amount
        total_interest (Decimal): Total interest paid

    Raises:
        ValueError: If filename is invalid
        IOError: If there's an error writing to the file
    """
    try:
        # Validate and clean filename
        clean_file_name = validate_file_name(file_name)
        
        with open(clean_file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            # Write loan summary section
            total_cost = principal + total_interest
            writer.writerow(['Loan Summary'])
            writer.writerow(['Principal Amount',
                           format_currency(principal, currency_symbol)])
            writer.writerow(['Annual Interest Rate', f"{annual_rate}%"])
            writer.writerow(['Loan Term',
                           f"{months//12} years {months%12} months"])
            writer.writerow(['Monthly Payment',
                           format_currency(monthly_payment, currency_symbol)])
            writer.writerow(['Total Interest',
                           format_currency(total_interest, currency_symbol)])
            writer.writerow(['Total Cost',
                           format_currency(total_cost, currency_symbol)])
            writer.writerow([])  # Empty row for spacing
            
            # Write amortization schedule
            writer.writerow(['Amortization Schedule'])
            fieldnames = [
                'Date', 'Month', 'Payment', 'Principal Payment',
                'Interest Payment', 'LTV', 'Remaining Balance'
            ]
            dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            dict_writer.writeheader()
            
            for payment_info in schedule:
                dict_writer.writerow({
                    'Date': payment_info['Date'],
                    'Month': payment_info['Month'],
                    'Payment': format_currency(
                        payment_info['Payment'], currency_symbol
                    ),
                    'Principal Payment': format_currency(
                        payment_info['Principal Payment'], currency_symbol
                    ),
                    'Interest Payment': format_currency(
                        payment_info['Interest Payment'], currency_symbol
                    ),
                    'LTV': f"{payment_info['LTV']:.1f}%",
                    'Remaining Balance': format_currency(
                        payment_info['Remaining Balance'], currency_symbol
                    )
                })
        
        print(f"\nAmortization schedule successfully exported to {clean_file_name}")
    
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def print_loan_summary(
    principal: Decimal,
    annual_rate: Decimal,
    months: int,
    monthly_payment: Decimal,
    total_interest: Decimal,
    currency_symbol: str
) -> None:
    """
    Print a summary of the loan details to the console.

    Args:
        principal (Decimal): Original loan amount
        annual_rate (Decimal): Annual interest rate
        months (int): Total number of months
        monthly_payment (Decimal): Monthly payment amount
        total_interest (Decimal): Total interest paid
        currency_symbol (str): Currency symbol for formatting
    """
    total_cost = principal + total_interest
    interest_percentage = (total_interest / total_cost) * 100
    
    print("\n=== Loan Summary ===")
    print(f"Principal Amount: {format_currency(principal, currency_symbol)}")
    print(f"Annual Interest Rate: {annual_rate}%")
    print(f"Loan Term: {months//12} years {months%12} months")
    print(f"Monthly Payment: {format_currency(monthly_payment, currency_symbol)}")
    print(
        f"Total Interest: {format_currency(total_interest, currency_symbol)} "
        f"({interest_percentage:.1f}% of total cost)"
    )
    print(f"Total Cost: {format_currency(total_cost, currency_symbol)}")
    print("=" * 50)

def print_amortization_schedule(
    schedule: List[Dict],
    currency_symbol: str
) -> None:
    """
    Print the amortization schedule in a formatted table to the console.

    Args:
        schedule (List[Dict]): The amortization schedule
        currency_symbol (str): Currency symbol for formatting
    """
    header = (
        f"{'Date':<15}{'Month':<7}{'Payment':<15}"
        f"{'Principal':<18}{'Interest':<15}{'LTV':<8}{'Balance':<18}"
    )
    print("\n=== Amortization Schedule ===")
    print(header)
    print("-" * len(header))
    
    for payment_info in schedule:
        payment = format_currency(payment_info['Payment'], currency_symbol)
        principal_payment = format_currency(
            payment_info['Principal Payment'], currency_symbol
        )
        interest_payment = format_currency(
            payment_info['Interest Payment'], currency_symbol
        )
        balance = format_currency(
            payment_info['Remaining Balance'], currency_symbol
        )
        ltv = f"{payment_info['LTV']:.1f}%"
        
        print(
            f"{payment_info['Date']:<15}"
            f"{payment_info['Month']:<7}"
            f"{payment:<15}"
            f"{principal_payment:<18}"
            f"{interest_payment:<15}"
            f"{ltv:<8}"
            f"{balance:<18}"
        )
