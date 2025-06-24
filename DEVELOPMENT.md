# Development Guide

## Project Status
- ✅ **Migrated to uv** - Fast package management implemented
- ✅ **Core functionality** - Mortgage calculations, visualization, export working
- ✅ **Clean codebase** - Removed legacy files and build artifacts
- ⚠️ **Test issues** - Import errors in test suite need fixing

## Architecture

### Core Components
- `mortgage_calculator/core/calculations.py` - Financial calculation engine
- `mortgage_calculator/core/validation.py` - Input validation and formatting
- `mortgage_calculator/io/cli.py` - Command line interface
- `mortgage_calculator/io/export.py` - CSV export functionality
- `mortgage_calculator/visualization/plotting.py` - Chart generation with matplotlib

### Data Flow
1. User input via CLI → Validation → Financial calculations
2. Results → Console display + CSV export + Chart generation

## Development Workflow

### Setup
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Testing
```bash
uv run pytest --cov=mortgage_calculator tests/  # Run with coverage
uv run pytest tests/test_core.py -v            # Single module
```

### Code Quality
```bash
uv run black .                    # Format code
uv run mypy .                     # Type checking
uv run pylint mortgage_calculator/ # Linting
```

## Current Issues

### Test Suite Fixes Needed
1. **Import errors** in `tests/test_core.py`:
   - `validate_loan_inputs` function not found in calculations.py
2. **Import errors** in `tests/test_io.py`:
   - `export_amortization_schedule_to_csv` function name mismatch

### Potential Improvements
- Add type hints throughout codebase
- Implement proper logging instead of print statements
- Add configuration file support (YAML/TOML)
- Create web interface using FastAPI
- Add more comprehensive error handling

## Release Checklist
- [ ] Fix test suite import issues
- [ ] Run full test suite with 100% pass rate
- [ ] Code formatting with black
- [ ] Type checking with mypy
- [ ] Update version in setup.py
- [ ] Generate clean example outputs

## Performance Notes
- **uv** provides ~10x faster dependency installation vs pip
- Matplotlib font cache builds on first run (one-time delay)
- CSV export handles large amortization schedules efficiently
- Memory usage scales linearly with loan term length