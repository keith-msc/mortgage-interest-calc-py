"""Visualization functions for mortgage amortization data."""

from decimal import Decimal
from typing import List, Dict
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def format_axis_labels(x: float, p: int) -> str:
    """Format y-axis labels with currency symbol and thousands separator."""
    from ..core.validation import format_currency
    return format_currency(Decimal(str(x)), '')  # Currency symbol added in plot title

def plot_amortization_schedule(
    schedule: List[Dict],
    currency_symbol: str,
    principal: Decimal,
    save_path: str = None
) -> None:
    """
    Plot the amortization schedule showing principal and interest payments over time.
    
    Args:
        schedule (List[Dict]): The amortization schedule
        currency_symbol (str): Currency symbol for formatting
        principal (Decimal): Original loan amount
        save_path (str, optional): Path to save the plot. If None, only displays.
    
    Raises:
        ValueError: If schedule is empty
        KeyError: If schedule entries are missing required fields
    """
    try:
        if not schedule:
            raise ValueError("Cannot create plot: schedule is empty")

        # Validate required fields
        required_fields = ['Month', 'Principal Payment', 'Interest Payment']
        if not all(field in schedule[0] for field in required_fields):
            raise KeyError("Schedule entries missing required fields")

        # Convert months to years for x-axis
        years = [float(payment['Month'])/12 for payment in schedule]
        principal_payments = [float(payment['Principal Payment']) for payment in schedule]
        interest_payments = [float(payment['Interest Payment']) for payment in schedule]
        
        # Calculate total cost for title
        total_cost = sum(principal_payments) + sum(interest_payments)
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
        
        # Plot payment components
        ax.plot(years, principal_payments, label='Principal Payment (Monthly)',
                color='green', linewidth=2)
        ax.plot(years, interest_payments, label='Interest Payment (Monthly)',
                color='red', linewidth=2)
        
        # Set title with loan summary
        title = (f'Amortization Schedule\n'
                f'Total Cost: {currency_symbol}{total_cost:,.2f}')
        ax.set_title(title, pad=20)
        
        # Set labels and formatting
        ax.set_xlabel('Years')
        ax.set_ylabel('Monthly Payment Amount')
        ax.yaxis.set_major_formatter(FuncFormatter(format_axis_labels))
        
        # Set x-axis ticks to show whole years
        max_years = max(years)
        ax.set_xticks(range(0, int(max_years) + 1, 5))
        
        # Enhance grid and legend
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='center right', bbox_to_anchor=(1.15, 0.5))
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"Payment breakdown graph saved as '{save_path}'")
        
        plt.show()
        plt.close()

    except Exception as e:
        print(f"An error occurred while creating the payment breakdown plot: {e}")
        raise

def plot_balance_over_time(
    schedule: List[Dict],
    currency_symbol: str,
    principal: Decimal,
    save_path: str = None
) -> None:
    """
    Plot the remaining balance over time with milestone markers.
    
    Args:
        schedule (List[Dict]): The amortization schedule
        currency_symbol (str): Currency symbol for formatting
        principal (Decimal): Original loan amount
        save_path (str, optional): Path to save the plot. If None, only displays.
    
    Raises:
        ValueError: If schedule is empty
        KeyError: If schedule entries are missing required fields
    """
    try:
        if not schedule:
            raise ValueError("Cannot create plot: schedule is empty")

        # Validate required fields
        if 'Remaining Balance' not in schedule[0]:
            raise KeyError("Schedule entries missing 'Remaining Balance' field")

        # Convert months to years for x-axis
        years = [float(payment['Month'])/12 for payment in schedule]
        balances = [float(payment['Remaining Balance']) for payment in schedule]
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot balance
        ax.plot(years, balances, label='Remaining Balance',
                color='blue', linewidth=2)
        
        # Set title with initial balance
        title = (f'Remaining Balance Over Time\n'
                f'Initial Balance: {currency_symbol}{float(principal):,.2f}')
        ax.set_title(title, pad=20)
        
        # Set labels and formatting
        ax.set_xlabel('Years')
        ax.set_ylabel('Balance')
        ax.yaxis.set_major_formatter(FuncFormatter(format_axis_labels))
        
        # Set x-axis ticks to show whole years
        max_years = max(years)
        ax.set_xticks(range(0, int(max_years) + 1, 5))
        
        # Enhance grid and legend
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper right')
        
        # Add milestone labels (25%, 50%, 75% paid off)
        for percentage in [0.75, 0.5, 0.25]:
            target_balance = float(principal) * percentage
            idx = next((i for i, b in enumerate(balances) if b <= target_balance), None)
            if idx is not None:
                ax.annotate(
                    f'{int((1-percentage)*100)}% Paid',
                    xy=(years[idx], balances[idx]),
                    xytext=(10, 10),
                    textcoords='offset points',
                    ha='left',
                    va='bottom'
                )
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"Balance over time graph saved as '{save_path}'")
        
        plt.show()
        plt.close()

    except Exception as e:
        print(f"An error occurred while creating the balance plot: {e}")
        raise
