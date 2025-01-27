"""Data visualization functions for mortgage calculator."""

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Optional

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from dateutil.parser import parse

class PlottingError(Exception):
    """Custom exception for plotting errors."""
    pass

@dataclass
class PlotConfig:
    """Configuration for plot styling."""
    theme: str = "light"  # "light" or "dark"
    show_annotations: bool = True
    dpi: int = 100
    figsize: tuple[int, int] = (12, 8)  # Increased height
    annotation_fontsize: int = 8
    title_fontsize: int = 14
    label_fontsize: int = 12
    title_pad: int = 20  # Added padding for title
    top_margin: float = 0.92  # Controls space at top
    bottom_margin: float = 0.12  # Controls space at bottom
    
    def apply_theme(self) -> None:
        """Apply theme settings to matplotlib."""
        if self.theme == "dark":
            plt.style.use('dark_background')
            self.colors = {
                'principal': '#00ff00',  # Bright green
                'interest': '#ff4444',   # Bright red
                'balance': '#00ffff',    # Cyan
                'grid': '#333333',       # Dark gray
                'text': '#ffffff'        # White
            }
        else:
            plt.style.use('default')
            self.colors = {
                'principal': '#2ecc71',  # Green
                'interest': '#e74c3c',   # Red
                'balance': '#3498db',    # Blue
                'grid': '#ecf0f1',       # Light gray
                'text': '#2c3e50'        # Dark gray
            }

def plot_amortization_schedule(
    schedule: List[Dict],
    currency_symbol: str,
    principal: Decimal,
    save_path: str,
    config: Optional[PlotConfig] = None
) -> None:
    """
    Create payment breakdown visualization.
    
    Args:
        schedule (List[Dict]): Amortization schedule
        currency_symbol (str): Currency symbol for formatting
        principal (Decimal): Original loan amount
        save_path (str): Path to save the plot
        config (Optional[PlotConfig]): Plot configuration
    
    Raises:
        PlottingError: If plotting fails
    """
    try:
        # Use default config if none provided
        if config is None:
            config = PlotConfig()
        
        # Apply theme
        config.apply_theme()
        
        # Create figure with adjusted layout
        fig = plt.figure(figsize=config.figsize, dpi=config.dpi)
        plt.subplots_adjust(
            top=config.top_margin,
            bottom=config.bottom_margin
        )
        
        # Extract data
        months = [entry['Month'] for entry in schedule]
        principal_payments = [float(entry['Principal_Payment']) for entry in schedule]
        interest_payments = [float(entry['Interest_Payment']) for entry in schedule]
        
        # Create stacked bar chart
        plt.bar(months, principal_payments, label='Principal',
                color=config.colors['principal'])
        plt.bar(months, interest_payments, bottom=principal_payments,
                label='Interest', color=config.colors['interest'])
        
        # Customize plot
        plt.title('Monthly Payment Breakdown\nPrincipal vs Interest',
                 fontsize=config.title_fontsize,
                 color=config.colors['text'],
                 pad=config.title_pad)
        plt.xlabel('Month', fontsize=config.label_fontsize,
                  color=config.colors['text'])
        plt.ylabel(f'Payment Amount ({currency_symbol})',
                  fontsize=config.label_fontsize, color=config.colors['text'])
        
        # Add grid
        plt.grid(True, alpha=0.3, color=config.colors['grid'])
        
        # Customize legend
        plt.legend(loc='upper right')
        
        # Add annotations if enabled
        if config.show_annotations:
            # Add total loan amount with adjusted spacing
            plt.annotate(
                f'Total Loan: {currency_symbol}{float(principal):,.2f}',
                xy=(0.02, 0.95), xycoords='axes fraction',  # Moved down slightly
                fontsize=config.annotation_fontsize + 2,  # Slightly larger font
                color=config.colors['text'],
                bbox=dict(  # Added background box
                    facecolor='white' if config.theme == "light" else 'black',
                    alpha=0.8,
                    edgecolor='none',
                    pad=3
                ),
                annotation_clip=False  # Ensures annotation isn't clipped
            )
            
            # Add key milestones
            for year in [1, 5, 10, 15, 20, 25, 30]:
                month = year * 12
                if month <= len(schedule):
                    plt.axvline(x=month, color='gray', linestyle='--', alpha=0.3)
                    plt.annotate(
                        f'{year}y',
                        xy=(month, plt.ylim()[1]),
                        xytext=(0, 10), textcoords='offset points',
                        ha='center', fontsize=config.annotation_fontsize,
                        color=config.colors['text']
                    )
        
        # Save plot
        plt.tight_layout()
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        raise PlottingError(f"Failed to create payment breakdown plot: {str(e)}")

def plot_balance_over_time(
    schedule: List[Dict],
    currency_symbol: str,
    principal: Decimal,
    save_path: str,
    config: Optional[PlotConfig] = None
) -> None:
    """
    Create remaining balance visualization.
    
    Args:
        schedule (List[Dict]): Amortization schedule
        currency_symbol (str): Currency symbol for formatting
        principal (Decimal): Original loan amount
        save_path (str): Path to save the plot
        config (Optional[PlotConfig]): Plot configuration
    
    Raises:
        PlottingError: If plotting fails
    """
    try:
        # Use default config if none provided
        if config is None:
            config = PlotConfig()
        
        # Apply theme
        config.apply_theme()
        
        # Create figure with adjusted layout
        fig = plt.figure(figsize=config.figsize, dpi=config.dpi)
        plt.subplots_adjust(
            top=config.top_margin,
            bottom=config.bottom_margin
        )
        
        # Extract data
        dates = [parse(entry['Date']) for entry in schedule]
        balances = [float(entry['Remaining_Balance']) for entry in schedule]
        
        # Create line plot
        plt.plot(dates, balances, label='Remaining Balance',
                color=config.colors['balance'], linewidth=2)
        
        # Customize plot
        plt.title('Remaining Loan Balance Over Time',
                 fontsize=config.title_fontsize,
                 color=config.colors['text'],
                 pad=config.title_pad)
        plt.xlabel('Date', fontsize=config.label_fontsize,
                  color=config.colors['text'])
        plt.ylabel(f'Balance ({currency_symbol})',
                  fontsize=config.label_fontsize, color=config.colors['text'])
        
        # Format x-axis dates
        plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        
        # Add grid
        plt.grid(True, alpha=0.3, color=config.colors['grid'])
        
        # Format y-axis with currency
        plt.gca().yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, p: f'{currency_symbol}{x:,.0f}')
        )
        
        # Add annotations if enabled
        if config.show_annotations:
            # Add milestone markers for percentage paid (25%, 50%, 75%)
            milestones = [25, 50, 75]  # Percentage milestones
            for milestone in milestones:
                # Calculate percentage paid for each point
                percentages_paid = [100 - float(entry['LTV']) for entry in schedule]
                try:
                    # Find first occurrence where percentage paid reaches milestone
                    i = next(i for i, paid in enumerate(percentages_paid) if paid >= milestone)
                    plt.plot(dates[i], balances[i], 'o',
                           color=config.colors['text'])
                    plt.annotate(
                        f'{milestone}% Paid',
                        xy=(dates[i], balances[i]),
                        xytext=(10, 10),
                        textcoords='offset points',
                        fontsize=config.annotation_fontsize,
                        color=config.colors['text'],
                        bbox=dict(  # Add background box for better visibility
                            facecolor='white' if config.theme == "light" else 'black',
                            alpha=0.8,
                            edgecolor='none',
                            pad=2
                        )
                    )
                except StopIteration:
                    continue  # Skip if milestone not reached
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        
        # Save plot
        plt.tight_layout()
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        raise PlottingError(f"Failed to create balance plot: {str(e)}")
