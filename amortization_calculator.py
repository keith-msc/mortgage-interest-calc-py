from datetime import datetime

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
        balance -= principal_payment
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
        next_month = current_date.month % 12 + 1
        next_year = current_date.year + (current_date.month // 12)
        current_date = current_date.replace(year=next_year, month=next_month)

    return amortization_schedule

def print_amortization_schedule(schedule):
    print(f"{'Date':<20} {'Month':<6} {'Payment':<10} {'Principal':<15} {'Interest':<10} {'LTV':<8} {'Balance':<10}")
    for payment_info in schedule:
        print(f"{payment_info['Date']:<20} {payment_info['Month']:<6} {payment_info['Payment']:<10} {payment_info['Principal Payment']:<15} {payment_info['Interest Payment']:<10} {payment_info['LTV']:<8} {payment_info['Remaining Balance']:<10}")

# User input
principal = float(input("Enter the loan amount (principal): "))
annual_rate = float(input("Enter the annual interest rate (in %): "))
months = int(input("Enter the loan term in months: "))

# Get and validate the start month and year
month = int(input("Enter the start month (MM): "))
year = int(input("Enter the start year (YYYY): "))
start_date = validate_month_year(month, year)

while start_date is None:
    print("Invalid month or year. Please try again.")
    month = int(input("Enter the start month (MM): "))
    year = int(input("Enter the start year (YYYY): "))
    start_date = validate_month_year(month, year)

# Generate and print the amortization schedule
amortization_schedule = create_amortization_schedule(principal, annual_rate, months, start_date)
print_amortization_schedule(amortization_schedule)
