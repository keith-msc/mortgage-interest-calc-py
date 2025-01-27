"""Main entry point for the mortgage calculator application."""

from pathlib import Path
from typing import Optional

from .core.calculations import (
    calculate_monthly_payment,
    create_amortization_schedule,
    LoanDetails
)
from .io.cli import (
    collect_user_input,
    print_colored,
    print_error,
    print_progress,
    print_success,
    CLIError,
    UserInput
)
from .io.export import (
    export_amortization_schedule,
    print_loan_summary,
    print_amortization_schedule,
    LoanSummary,
    ExportError
)
from .visualization.plotting import (
    plot_amortization_schedule,
    plot_balance_over_time,
    PlotConfig,
    PlottingError
)

def create_output_directory() -> Path:
    """Create output directory for generated files."""
    output_dir = Path("mortgage_output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def process_loan_calculation(user_input: UserInput) -> Optional[tuple[LoanDetails, LoanSummary, list]]:
    """
    Process loan calculation based on user input.
    
    Args:
        user_input (UserInput): Validated user input data
    
    Returns:
        Optional[tuple[LoanDetails, LoanSummary, list]]: Loan details, summary and schedule if successful
    """
    try:
        print_progress("Calculating loan details")
        
        # Create loan details
        loan = LoanDetails(
            principal=user_input.principal,
            annual_rate=user_input.annual_rate,
            months=user_input.total_months,
            start_date=user_input.start_date
        )
        
        # Calculate monthly payment
        monthly_payment = calculate_monthly_payment(
            loan.principal,
            loan.annual_rate,
            loan.months
        )
        
        # Create amortization schedule
        schedule, total_interest = create_amortization_schedule(loan)
        
        # Create loan summary
        loan_summary = LoanSummary(
            principal=loan.principal,
            annual_rate=loan.annual_rate,
            months=loan.months,
            monthly_payment=monthly_payment,
            total_interest=total_interest,
            currency_symbol=user_input.currency_symbol
        )
        
        return loan, loan_summary, schedule
        
    except Exception as e:
        print_error(f"Calculation failed: {str(e)}")
        return None

def export_results(
    schedule: list,
    loan_summary: LoanSummary,
    output_dir: Path,
    filename: str
) -> Optional[Path]:
    """
    Export calculation results to file.
    
    Args:
        schedule (list): Amortization schedule
        loan_summary (LoanSummary): Loan summary information
        output_dir (Path): Output directory
        filename (str): Base filename
    
    Returns:
        Optional[Path]: Path to exported file if successful
    """
    try:
        print_progress("Exporting results")
        
        # Ensure filename has extension
        if not filename.endswith(('.csv', '.txt')):
            filename += '.csv'
        
        export_path = output_dir / filename
        export_amortization_schedule(
            schedule=schedule,
            loan_summary=loan_summary,
            file_path=str(export_path)
        )
        
        return export_path
    
    except ExportError as e:
        print_error(f"Export failed: {str(e)}")
        return None

def generate_visualizations(
    schedule: list,
    loan_summary: LoanSummary,
    output_dir: Path,
    dark_mode: bool = False
) -> None:
    """Generate visualization plots."""
    try:
        print_progress("Generating visualizations")
        
        plot_config = PlotConfig(
            theme="dark" if dark_mode else "light",
            show_annotations=True
        )
        
        # Payment breakdown plot
        payments_plot = output_dir / "payment_breakdown.png"
        plot_amortization_schedule(
            schedule=schedule,
            currency_symbol=loan_summary.currency_symbol,
            principal=loan_summary.principal,
            save_path=str(payments_plot),
            config=plot_config
        )
        print_colored(f"Payment breakdown plot saved as: {payments_plot}", "green")
        
        # Balance plot
        balance_plot = output_dir / "balance_progress.png"
        plot_balance_over_time(
            schedule=schedule,
            currency_symbol=loan_summary.currency_symbol,
            principal=loan_summary.principal,
            save_path=str(balance_plot),
            config=plot_config
        )
        print_colored(f"Balance progress plot saved as: {balance_plot}", "green")
        
    except PlottingError as e:
        print_error(f"Visualization failed: {str(e)}")

def main() -> None:
    """Main function to run the mortgage calculator."""
    try:
        # Collect user input
        user_input = collect_user_input()
        
        # Create output directory
        output_dir = create_output_directory()
        
        # Process calculations
        result = process_loan_calculation(user_input)
        if not result:
            return
        
        loan, loan_summary, schedule = result
        
        # Print initial results
        print_loan_summary(loan_summary)
        print_amortization_schedule(schedule, loan_summary, max_entries=12)
        
        # Export results
        export_path = export_results(
            schedule,
            loan_summary,
            output_dir,
            user_input.export_filename
        )
        if not export_path:
            return
        
        # Generate visualizations if requested
        if user_input.show_graphs:
            generate_visualizations(
                schedule,
                loan_summary,
                output_dir,
                dark_mode=False  # Could make this configurable
            )
        
        print_success("\nMortgage calculation completed successfully!")
        print_colored(f"All output files have been saved to: {output_dir}", "cyan")

    except CLIError as e:
        print_error(f"Input error: {str(e)}")
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        print_colored("Please try again with valid inputs.", "yellow")

if __name__ == '__main__':
    main()
