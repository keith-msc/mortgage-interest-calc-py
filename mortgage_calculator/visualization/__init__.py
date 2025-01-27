"""Visualization package initialization."""

from .plotting import (
    PlotConfig,
    plot_amortization_schedule,
    plot_balance_over_time,
    PlottingError
)

__all__ = [
    'PlotConfig',
    'plot_amortization_schedule',
    'plot_balance_over_time',
    'PlottingError'
]
