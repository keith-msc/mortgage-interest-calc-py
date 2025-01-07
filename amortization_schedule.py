# Requires installation of python-dateutil and matplotlib packages
# Install via pip:
# pip install python-dateutil matplotlib

from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, getcontext
import csv
import matplotlib.pyplot as plt

getcontext().prec = 10  # Set desired precision for Decimal calculations

def get_month_number(month_str):
    """
    Convert month name to month number.

    Args:
        month_str (str): Month name (e.g., 'January', 'Jan', 'JANUARY', 'JAN')

    Returns:
        int: Month number (1-12) if valid, None if invalid
    """
    month_str = month_str.strip().lower()
    month_map = {
        'january': 1, 'jan': 1,
        'february': 2, 'feb': 2,
        'march': 3, 'mar': 3,
        'april': 4, 'apr': 4,
        'may': 5,
        'june': 6, 'jun': 6,
        'july': 7, 'jul': 7,
        'august': 8, 'aug': 8,
        'september': 9, 'sep': 9, 'sept': 9,
        'october': 10, 'oct': 10,
        'november': 11, 'nov': 11,
        'december': 12, 'dec': 12
    }
    return month_map.get(month_str)

def validate_month_year(month_str, year):
    """
    Validate and return a datetime object for the first day of the given month and year.

    Args:
        month_str (str): Month name (e.g., 'January', 'Jan')
        year (int): Year (e.g., 2023)

    Returns:
        datetime.datetime or None: The datetime object if valid, else None.
    """
    month_num = get_month_number(month_str)
    if month_num is None:
        return None
    
    try:
        start_date = datetime(year=year, month=month_num, day=1)
        return start_date
    except ValueError:
        return None

def calculate_monthly_payment(principal, annual_rate, months):
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

def create_amortization_schedule(principal, annual_rate, months, start_date):
    """
    Create an amortization schedule for the loan.

    Args:
        principal (Decimal): The loan amount.
        annual_rate (Decimal): The annual interest rate in percent.
        months (int): The loan term in months.
        start_date (datetime.datetime): The start date of the loan.

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
            # Calculate the interest for the current period
            interest = balance * monthly_rate

        # Calculate the principal payment for the current period
        principal_payment = monthly_payment - interest

        # Ensure that the last payment adjusts for any rounding issues
        if balance - principal_payment < Decimal('-0.01'):
            principal_payment = balance
            monthly_payment = principal_payment + interest
            balance = Decimal('0.00')
        else:
            balance -= principal_payment
            balance = max(balance, Decimal('0.00'))  # Ensure balance doesn't go negative due to rounding

        # Calculate LTV ratio as a percentage
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
        current_date += relativedelta(months=1)  # Correctly increment the month
        total_interest += interest

    return amortization_schedule, total_interest

def print_amortization_schedule(schedule, currency_symbol):
    """
    Print the amortization schedule in a formatted table.

    Args:
        schedule (list): The amortization schedule as a list of dictionaries.
        currency_symbol (str): The currency symbol to use in the output.
    """
    header = f"{'Date':<15}{'Month':<7}{'Payment':<15}{'Principal':<18}{'Interest':<15}{'LTV':<8}{'Balance':<18}"
    print(header)
    print("-" * len(header))
    for payment_info in schedule:
        payment = f"{currency_symbol}{payment_info['Payment']:.2f}"
        principal_payment = f"{currency_symbol}{payment_info['Principal Payment']:.2f}"
        interest_payment = f"{currency_symbol}{payment_info['Interest Payment']:.2f}"
        balance = f"{currency_symbol}{payment_info['Remaining Balance']:.2f}"
        ltv = f"{payment_info['LTV']:.1f}%"
        print(f"{payment_info['Date']:<15}{payment_info['Month']:<7}{payment:<15}{principal_payment:<18}{interest_payment:<15}{ltv:<8}{balance:<18}")

def export_amortization_schedule_to_csv(schedule, file_name, currency_symbol):
    """
    Export the amortization schedule to a CSV file.

    Args:
        schedule (list): The amortization schedule as a list of dictionaries.
        file_name (str): The name of the CSV file to export to.
        currency_symbol (str): The currency symbol to use in the output.

    Raises:
        ValueError: If the filename contains invalid characters.
        IOError: If there's an error writing to the file.
    """
    # Validate filename
    import os
    if os.path.sep in file_name or '..' in file_name:
        raise ValueError("Invalid characters in filename")
    
    try:
        with open(file_name, 'w', newline='') as csv_file:
            fieldnames = ['Date', 'Month', 'Payment', 'Principal Payment', 'Interest Payment', 'LTV', 'Remaining Balance']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for payment_info in schedule:
                writer.writerow({
                    'Date': payment_info['Date'],
                    'Month': payment_info['Month'],
                    'Payment': f"{currency_symbol}{payment_info['Payment']:.2f}",
                    'Principal Payment': f"{currency_symbol}{payment_info['Principal Payment']:.2f}",
                    'Interest Payment': f"{currency_symbol}{payment_info['Interest Payment']:.2f}",
                    'LTV': f"{payment_info['LTV']:.1f}%",
                    'Remaining Balance': f"{currency_symbol}{payment_info['Remaining Balance']:.2f}"
                })
        print(f"Amortization schedule successfully exported to {file_name}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def plot_amortization_schedule(schedule, currency_symbol):
    """
    Plot the amortization schedule showing principal and interest payments over time.
    The function displays and saves the plots to image files.

    Args:
        schedule (list): The amortization schedule as a list of dictionaries.
        currency_symbol (str): The currency symbol to use in the plots.

    Raises:
        Exception: If there's an error creating or saving the plots.
    """
    try:
        months = [payment['Month'] for payment in schedule]
        principal_payments = [payment['Principal Payment'] for payment in schedule]
        interest_payments = [payment['Interest Payment'] for payment in schedule]
        balances = [payment['Remaining Balance'] for payment in schedule]

        # Plotting the principal and interest payments
        fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
        ax.plot(months, principal_payments, label='Principal Payment', color='green')
        ax.plot(months, interest_payments, label='Interest Payment', color='red')
        ax.set_title('Amortization Schedule')
        ax.set_xlabel('Month')
        ax.set_ylabel(f'Amount ({currency_symbol})')
        ax.legend()
        ax.grid(True)
        # Save the plot to a file
        plt.savefig('amortization_schedule_payments.png')
        print("Amortization schedule payments graph saved as 'amortization_schedule_payments.png'")
        plt.show()

        # Plotting the remaining balance over time
        fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
        ax.plot(months, balances, label='Remaining Balance', color='blue')
        ax.set_title('Remaining Balance Over Time')
        ax.set_xlabel('Month')
        ax.set_ylabel(f'Balance ({currency_symbol})')
        ax.legend()
        ax.grid(True)
        # Save the plot to a file
        plt.savefig('amortization_schedule_balance.png')
        print("Remaining balance graph saved as 'amortization_schedule_balance.png'")
        plt.show()
    except Exception as e:
        print(f"An error occurred while creating the plots: {e}")

def validate_loan_inputs(principal, annual_rate, months):
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
    if principal > Decimal('1000000000'):  # 1 billion limit
        raise ValueError("Principal amount is unreasonably high.")
    if annual_rate < 0:
        raise ValueError("Annual interest rate cannot be negative.")
    if annual_rate > Decimal('100'):
        raise ValueError("Annual interest rate cannot exceed 100%.")
    if months <= 0:
        raise ValueError("Loan term must be greater than zero months.")
    if months > 600:  # 50 years limit
        raise ValueError("Loan term cannot exceed 600 months (50 years).")

def main():
    """
    Main function to run the amortization schedule script.
    """
    # Prompt user for inputs with input validation
    try:
        principal_input = input("Enter the loan amount (principal): ")
        principal = Decimal(principal_input)

        annual_rate_input = input("Enter the annual interest rate (in %): ")
        annual_rate = Decimal(annual_rate_input)

        months_input = input("Enter the loan term in months: ")
        months = int(months_input)

        # Validate all loan inputs together
        validate_loan_inputs(principal, annual_rate, months)

        start_month_input = input("Enter the start month (e.g., January, Jan): ")
        start_year_input = input("Enter the start year (e.g., 2023): ")
        
        try:
            start_year = int(start_year_input)
            if start_year <= 0:
                print("Start year must be a positive integer.")
                return
        except ValueError:
            print("Invalid year. Please enter a numeric value.")
            return

        # Validate the start date
        start_date = validate_month_year(start_month_input, start_year)
        if not start_date:
            print("Invalid month name or year. Please try again.")
            return

    except ValueError as e:
        print(f"Invalid input: {str(e)}")
        return

    # Prompt user for currency symbol
    currency_choice = input("Choose your currency symbol - enter 'euro', 'dollar', or 'sterling': ").strip().lower()
    if currency_choice == 'euro':
        currency_symbol = '€'
    elif currency_choice == 'dollar':
        currency_symbol = '$'
    elif currency_choice == 'sterling':
        currency_symbol = '£'
    else:
        print("Invalid currency choice. Defaulting to dollar ($).")
        currency_symbol = '$'

    # Create the amortization schedule
    schedule, total_interest = create_amortization_schedule(principal, annual_rate, months, start_date)

    # Print the amortization schedule
    print_amortization_schedule(schedule, currency_symbol)

    # Print total interest paid over the life of the loan
    print(f"\nTotal interest paid over the life of the loan: {currency_symbol}{total_interest:.2f}")

    # Export the amortization schedule to CSV
    csv_file_name = input("Enter the CSV file name to export (e.g., schedule.csv): ")
    if not csv_file_name.endswith('.csv'):
        csv_file_name += '.csv'

    export_amortization_schedule_to_csv(schedule, csv_file_name, currency_symbol)

    # Ask user if they want to see a graph
    plot_choice = input("Would you like to see and save graphs of the amortization schedule? (yes/no): ").strip().lower()
    if plot_choice in ('yes', 'y'):
        plot_amortization_schedule(schedule, currency_symbol)

if __name__ == "__main__":
    main()
