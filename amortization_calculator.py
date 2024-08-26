from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv

def validate_month_year(month, year):
    try:
        start_date = datetime(year=year, month=month, day=1)
        return start_date
    except ValueError:
        return None

def calculate_monthly_payment(principal, annual_rate, months):
    monthly_rate = (annual_rate / 100) / 12
    monthly_payment = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    return monthly_payment

def create_amortization_schedule(principal, annual_rate, months, start_date):
    monthly_payment = calculate_monthly_payment(principal, annual_rate, months)
    monthly_rate = (annual_rate / 100) / 12
    balance = principal
    current_date = start_date

    amortization_schedule = []

    for i in range(1, months + 1):
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest
        balance = max(balance - principal_payment, 0)  # Ensuring balance doesn't go negative due to rounding
        ltv = (balance / principal) * 100  # Calculate LTV ratio as a percentage
        amortization_schedule.append({
            'Date': current_date.strftime("%B %Y"),  
            'Month': i,
            'Payment': f"{monthly_payment:.2f}",
            'Principal Payment': f"{principal_payment:.2f}",
            'Interest Payment': f"{interest:.2f}",
            'Remaining Balance': f"{balance:.2f}",
            'LTV': f"{ltv:.1f}%"  # Format LTV to one decimal point
        })
        current_date += relativedelta(months=1)  # Correctly increment the month

    return amortization_schedule

def print_amortization_schedule(schedule):
    print(f"{'Date':<20} {'Month':<6} {'Payment':<10} {'Principal':<15} {'Interest':<10} {'LTV':<8} {'Balance':<10}")
    for payment_info in schedule:
        print(f"{payment_info['Date']:<20} {payment_info['Month']:<6} {payment_info['Payment']:<10} {payment_info['Principal Payment']:<15} {payment_info['Interest Payment']:<10} {payment_info['LTV']:<8} {payment_info['Remaining Balance']:<10}")

def export_amortization_schedule_to_csv(schedule, file_name):
    with open(file_name, 'w', newline='') as csv_file:
        fieldnames = ['Date', 'Month', 'Payment', 'Principal Payment', 'Interest Payment', 'LTV', 'Remaining Balance']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for payment_info in schedule:
            writer.writerow(payment_info)
        print(f"Amortization schedule successfully exported to {file_name}")

if __name__ == "__main__":
    principal = float(input("Enter the loan amount (principal): "))
    annual_rate = float(input("Enter the annual interest rate (in %): "))
    months = int(input("Enter the loan term in months: "))
    start_month = int(input("Enter the start month (MM): "))
    start_year = int(input("Enter the start year (YYYY): "))

    start_date = validate_month_year(start_month, start_year)
    if not start_date:
        print("Invalid start month or year. Please try again.")
    else:
        schedule = create_amortization_schedule(principal, annual_rate, months, start_date)
        print_amortization_schedule(schedule)
        # Specify the file name for the CSV file
        csv_file_name = "amortization_schedule.csv"
        # Write the amortization schedule to the CSV file using the new function
        export_amortization_schedule_to_csv(schedule, csv_file_name)