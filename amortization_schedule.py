# Requires installation of python-dateutil and matplotlib packages
# Install via pip:
# pip install python-dateutil matplotlib

from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, getcontext
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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

def format_currency(amount, currency_symbol):
    """Format currency with thousands separator and currency symbol."""
    return f"{currency_symbol}{amount:,.2f}"

def print_loan_summary(principal, annual_rate, months, monthly_payment, total_interest, currency_symbol):
    """Print a summary of the loan details."""
    total_cost = principal + total_interest
    interest_percentage = (total_interest / total_cost) * 100
    
    print("\n=== Loan Summary ===")
    print(f"Principal Amount: {format_currency(principal, currency_symbol)}")
    print(f"Annual Interest Rate: {annual_rate}%")
    print(f"Loan Term: {months//12} years {months%12} months")
    print(f"Monthly Payment: {format_currency(monthly_payment, currency_symbol)}")
    print(f"Total Interest: {format_currency(total_interest, currency_symbol)} ({interest_percentage:.1f}% of total cost)")
    print(f"Total Cost: {format_currency(total_cost, currency_symbol)}")
    print("=" * 50)

def print_amortization_schedule(schedule, currency_symbol):
    """
    Print the amortization schedule in a formatted table.

    Args:
        schedule (list): The amortization schedule as a list of dictionaries.
        currency_symbol (str): The currency symbol to use in the output.
    """
    header = f"{'Date':<15}{'Month':<7}{'Payment':<15}{'Principal':<18}{'Interest':<15}{'LTV':<8}{'Balance':<18}"
    print("\n=== Amortization Schedule ===")
    print(header)
    print("-" * len(header))
    for payment_info in schedule:
        payment = format_currency(payment_info['Payment'], currency_symbol)
        principal_payment = format_currency(payment_info['Principal Payment'], currency_symbol)
        interest_payment = format_currency(payment_info['Interest Payment'], currency_symbol)
        balance = format_currency(payment_info['Remaining Balance'], currency_symbol)
        ltv = f"{payment_info['LTV']:.1f}%"
        print(f"{payment_info['Date']:<15}{payment_info['Month']:<7}{payment:<15}{principal_payment:<18}{interest_payment:<15}{ltv:<8}{balance:<18}")

def export_amortization_schedule_to_csv(schedule, file_name, currency_symbol, principal, annual_rate, months, monthly_payment, total_interest):
    """
    Export the amortization schedule to a CSV file with a summary section.

    Args:
        schedule (list): The amortization schedule as a list of dictionaries.
        file_name (str): The name of the CSV file to export to.
        currency_symbol (str): The currency symbol to use in the output.
        principal (Decimal): The loan amount.
        annual_rate (Decimal): The annual interest rate.
        months (int): The loan term in months.
        monthly_payment (Decimal): The monthly payment amount.
        total_interest (Decimal): The total interest paid over the loan term.

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
            writer = csv.writer(csv_file)
            
            # Write loan summary section
            total_cost = principal + total_interest
            writer.writerow(['Loan Summary'])
            writer.writerow(['Principal Amount', format_currency(principal, currency_symbol)])
            writer.writerow(['Annual Interest Rate', f"{annual_rate}%"])
            writer.writerow(['Loan Term', f"{months//12} years {months%12} months"])
            writer.writerow(['Monthly Payment', format_currency(monthly_payment, currency_symbol)])
            writer.writerow(['Total Interest', format_currency(total_interest, currency_symbol)])
            writer.writerow(['Total Cost', format_currency(total_cost, currency_symbol)])
            writer.writerow([])  # Empty row for spacing
            
            # Write amortization schedule
            writer.writerow(['Amortization Schedule'])
            fieldnames = ['Date', 'Month', 'Payment', 'Principal Payment', 'Interest Payment', 'LTV', 'Remaining Balance']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for payment_info in schedule:
                writer.writerow({
                    'Date': payment_info['Date'],
                    'Month': payment_info['Month'],
                    'Payment': format_currency(payment_info['Payment'], currency_symbol),
                    'Principal Payment': format_currency(payment_info['Principal Payment'], currency_symbol),
                    'Interest Payment': format_currency(payment_info['Interest Payment'], currency_symbol),
                    'LTV': f"{payment_info['LTV']:.1f}%",
                    'Remaining Balance': format_currency(payment_info['Remaining Balance'], currency_symbol)
                })
        print(f"\nAmortization schedule successfully exported to {file_name}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def plot_amortization_schedule(schedule, currency_symbol, principal):
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
        # Convert months to years for x-axis
        # Convert Decimal values to float for plotting
        years = [float(payment['Month'])/12 for payment in schedule]
        principal_payments = [float(payment['Principal Payment']) for payment in schedule]
        interest_payments = [float(payment['Interest Payment']) for payment in schedule]
        balances = [float(payment['Remaining Balance']) for payment in schedule]

        def format_axis_labels(x, p):
            """Format y-axis labels with thousands separator"""
            # Convert float back to Decimal for currency formatting
            return format_currency(Decimal(str(x)), currency_symbol)

        # Calculate total cost for title
        total_cost = sum(principal_payments) + sum(interest_payments)
        
        # Plotting the principal and interest payments
        fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
        ax.plot(years, principal_payments, label='Principal Payment (Monthly)', color='green', linewidth=2)
        ax.plot(years, interest_payments, label='Interest Payment (Monthly)', color='red', linewidth=2)
        
        # Set title with loan summary
        title = f'Amortization Schedule\nTotal Cost: {format_currency(total_cost, currency_symbol)}'
        ax.set_title(title, pad=20)
        
        ax.set_xlabel('Years')
        ax.set_ylabel(f'Monthly Payment Amount')
        
        # Format y-axis with currency
        ax.yaxis.set_major_formatter(FuncFormatter(format_axis_labels))
        
        # Set x-axis ticks to show whole years
        max_years = max(years)
        ax.set_xticks(range(0, int(max_years) + 1, 5))
        
        # Enhance grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Enhance legend
        ax.legend(loc='center right', bbox_to_anchor=(1.15, 0.5))
        # Save the plot to a file
        plt.savefig('amortization_schedule_payments.png', bbox_inches='tight')
        print("Amortization schedule payments graph saved as 'amortization_schedule_payments.png'")
        plt.show()
        plt.close()  # Close the first figure

        # Plotting the remaining balance over time
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(years, balances, label='Remaining Balance', color='blue', linewidth=2)
        
        # Set title with initial balance (using principal, not first month's remaining balance)
        title = f'Remaining Balance Over Time\nInitial Balance: {format_currency(Decimal(str(float(principal))), currency_symbol)}'
        ax.set_title(title, pad=20)
        
        ax.set_xlabel('Years')
        ax.set_ylabel('Balance')
        
        # Format y-axis with currency
        ax.yaxis.set_major_formatter(FuncFormatter(format_axis_labels))
        
        # Set x-axis ticks to show whole years
        ax.set_xticks(range(0, int(max_years) + 1, 5))
        
        # Enhance grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Enhance legend
        ax.legend(loc='upper right')
        
        # Add milestone labels (25%, 50%, 75% paid off)
        # Calculate percentages based on principal, not first month's remaining balance
        for percentage in [0.75, 0.5, 0.25]:
            idx = next((i for i, b in enumerate(balances) if b <= float(principal) * percentage), None)
            if idx is not None:
                ax.annotate(f'{int((1-percentage)*100)}% Paid',
                           xy=(years[idx], balances[idx]),
                           xytext=(10, 10), textcoords='offset points',
                           ha='left', va='bottom')
        # Save the plot to a file
        plt.savefig('amortization_schedule_balance.png', bbox_inches='tight')
        print("Remaining balance graph saved as 'amortization_schedule_balance.png'")
        plt.show()
        plt.close()  # Close the second figure
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
    # Validate principal amount
    if principal <= 0:
        raise ValueError("Principal amount must be greater than zero.")
    if principal > Decimal('1000000000'):  # 1 billion limit
        raise ValueError("Principal amount is unreasonably high (max: 1 billion).")
    
    # Validate interest rate
    if annual_rate < 0:
        raise ValueError("Annual interest rate cannot be negative.")
    if annual_rate > Decimal('100'):
        raise ValueError("Annual interest rate cannot exceed 100%.")
    if annual_rate > Decimal('25'):  # Warning for high rates
        print("\nWarning: Interest rate is unusually high. Please verify this is correct.")
    
    # Validate loan term
    if months <= 0:
        raise ValueError("Loan term must be greater than zero months.")
    if months > 600:  # 50 years limit
        raise ValueError("Loan term cannot exceed 600 months (50 years).")
    if months > 420:  # Warning for terms over 35 years
        print("\nWarning: Loan term exceeds 35 years. Please verify this is correct.")

def main():
    """
    Main function to run the amortization schedule script.
    """
    print("\n=== Mortgage Amortization Calculator ===")
    print("This calculator will help you understand your mortgage payments,")
    print("including how much interest you'll pay over the life of the loan.")
    print("=" * 50 + "\n")
    
    # Prompt user for inputs with input validation
    try:
        principal_input = input("Enter the loan amount (principal, e.g., 250000): ")
        principal = Decimal(principal_input)

        annual_rate_input = input("Enter the annual interest rate (e.g., 3.5 for 3.5%): ")
        annual_rate = Decimal(annual_rate_input)

        # Get loan term in years and months
        print("\nLoan Term:")
        years_input = input("  Enter years (e.g., 30): ")
        months_input = input("  Enter any additional months (0-11): ")
        
        try:
            years = int(years_input)
            additional_months = int(months_input)
            
            if years < 0:
                raise ValueError("Years cannot be negative.")
            if additional_months < 0 or additional_months > 11:
                raise ValueError("Additional months must be between 0 and 11.")
                
            # Convert to total months
            months = (years * 12) + additional_months
            
            # Validate all loan inputs together
            validate_loan_inputs(principal, annual_rate, months)
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print("Please enter valid numbers for years and months.")
            else:
                print(str(e))
            return

        print("\nLoan Start Date:")
        start_month_input = input("  Enter month (e.g., January, Jan): ")
        start_year_input = input("  Enter year (e.g., 2023): ")
        
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
    print("\nCurrency:")
    currency_choice = input("  Choose currency (euro/dollar/sterling): ").strip().lower()
    if currency_choice == 'euro':
        currency_symbol = '€'
    elif currency_choice == 'dollar':
        currency_symbol = '$'
    elif currency_choice == 'sterling':
        currency_symbol = '£'
    else:
        print("Invalid currency choice. Defaulting to dollar ($).")
        currency_symbol = '$'

    # Calculate monthly payment and create amortization schedule
    monthly_payment = calculate_monthly_payment(principal, annual_rate, months)
    schedule, total_interest = create_amortization_schedule(principal, annual_rate, months, start_date)

    # Print loan summary and amortization schedule
    print_loan_summary(principal, annual_rate, months, monthly_payment, total_interest, currency_symbol)
    print_amortization_schedule(schedule, currency_symbol)

    # Export the amortization schedule to CSV
    csv_file_name = input("Enter the CSV file name to export (e.g., schedule.csv): ")
    if not csv_file_name.endswith('.csv'):
        csv_file_name += '.csv'

    export_amortization_schedule_to_csv(schedule, csv_file_name, currency_symbol, 
                                      principal, annual_rate, months, monthly_payment, total_interest)

    # Ask user if they want to see graphs
    print("\nVisualization:")
    print("  Two graphs will be generated:")
    print("  1. Monthly payments breakdown (Principal vs Interest)")
    print("  2. Remaining balance over time with payoff milestones")
    plot_choice = input("  Would you like to see these graphs? (yes/no): ").strip().lower()
    if plot_choice in ('yes', 'y'):
        plot_amortization_schedule(schedule, currency_symbol, principal)
    
    print("\nCalculation complete!")
    print(f"Monthly Payment: {format_currency(monthly_payment, currency_symbol)}")
    print(f"Total Interest: {format_currency(total_interest, currency_symbol)}")
    print(f"Check {csv_file_name} for the detailed payment schedule.")

if __name__ == "__main__":
    main()
