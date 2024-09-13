# Mortgage Interest Calculator

A simple Python script to calculate and generate an amortization schedule for a mortgage loan.

## Features

- **Calculate Monthly Payments**: Computes monthly payments based on loan amount, interest rate, and loan term.
- **Generate Amortization Schedule**: Creates a schedule detailing each payment's principal and interest components, remaining balance, and Loan-to-Value (LTV) ratio.
- **Export to CSV**: Saves the amortization schedule to a CSV file.
- **Display and Save Graphs**: Visualizes the amortization schedule with graphs showing:
  - Principal and interest payments over time.
  - Remaining balance over the loan term.
- **Currency Symbol Support**: Choose between Euro (€), Dollar ($), or Sterling (£) symbols.

## Installation

### Prerequisites

- **Python 3.x** must be installed on your system.

### Steps

1. **Download the Script**

   Clone the repository or download the script directly.

   ```bash
   git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
   cd mortgage-interest-calc-py
   ```

2. **Create a Virtual Environment (Recommended)**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

   - On **Windows**:

     ```bash
     venv\Scripts\activate
     ```

4. **Install Required Packages**

   Install the necessary Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` file, install the packages manually:

   ```bash
   pip install python-dateutil matplotlib numpy
   ```

## Usage

Run the script using Python:

```bash
python amortization_schedule.py
```

### Input Prompts

The script will prompt you for the following inputs:

1. **Loan Amount (Principal)**: The total amount of the loan (e.g., `100000`).
2. **Annual Interest Rate**: The annual interest rate in percent (e.g., `5`).
3. **Loan Term in Months**: The total number of months over which the loan will be repaid (e.g., `360`).
4. **Start Month**: The month when the loan starts (`1` for January, `12` for December).
5. **Start Year**: The year when the loan starts (e.g., `2023`).
6. **Currency Symbol**: Choose your currency symbol by entering `'euro'`, `'dollar'`, or `'sterling'`.
7. **CSV File Name**: The name of the CSV file to export the amortization schedule (e.g., `schedule.csv`).
8. **Graphs**: Option to display and save graphs of the amortization schedule.

### Example Run

```plaintext
Enter the loan amount (principal): 200000
Enter the annual interest rate (in %): 3.5
Enter the loan term in months: 360
Enter the start month (1-12): 6
Enter the start year (e.g., 2023): 2023
Choose your currency symbol - enter 'euro', 'dollar', or 'sterling': sterling
Enter the CSV file name to export (e.g., schedule.csv): mortgage_schedule.csv
Would you like to see and save graphs of the amortization schedule? (yes/no): yes
Amortization schedule payments graph saved as 'amortization_schedule_payments.png'
Remaining balance graph saved as 'amortization_schedule_balance.png'
```

### Output Files

- **CSV File**: The amortization schedule is exported to the specified CSV file.
- **Graphs**:
  - `amortization_schedule_payments.png`: Graph showing principal and interest payments over time.
  - `amortization_schedule_balance.png`: Graph showing the remaining balance over time.

## Notes

- **Graphs**: If you choose to view the graphs, they will be displayed and saved in the current directory.
- **Virtual Environment**: Remember to activate your virtual environment each time before running the script:

  - On **macOS/Linux**:

    ```bash
    source venv/bin/activate
    ```

  - On **Windows**:

    ```bash
    venv\Scripts\activate
    ```

## Dependencies

- **python-dateutil**
- **matplotlib**
- **numpy**

These are listed in the `requirements.txt` file.

### `requirements.txt` Contents

```text
python-dateutil==2.8.2
matplotlib>=3.5.0
numpy>=1.21.0
```

## Quick Start

If you're familiar with Python and virtual environments, here's a quick summary:

```bash
# Clone the repository
git clone https://github.com/keith-msc/mortgage-interest-calc-py.git
cd mortgage-interest-calc-py

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python amortization_schedule.py
```

## Contact

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/keith-msc/mortgage-interest-calc-py) or contact the maintainer.

