"""Data loading module for macro analysis system."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Literal
import random

DataSource = Literal["mock", "api"]


@dataclass(frozen=True)
class MacroSeries:
    """Container for monthly macro time series."""

    dates: List[str]
    values: List[float]


def _gen_month_labels(months: int = 12) -> List[str]:
    """Generate YYYY-MM labels for the recent months."""
    today = date.today()
    labels: List[str] = []
    year, month = today.year, today.month

    for _ in range(months):
        labels.append(f"{year:04d}-{month:02d}")
        month -= 1
        if month == 0:
            month = 12
            year -= 1

    labels.reverse()
    return labels


def _build_trend_series(base: float, drift: float, noise: float, months: int = 12) -> List[float]:
    """Generate an easy-to-control synthetic time series."""
    values: List[float] = []
    current = base
    for _ in range(months):
        current += drift + random.uniform(-noise, noise)
        values.append(round(current, 2))
    return values


def _load_from_mock(months: int = 12, seed: int = 42) -> Dict[str, MacroSeries]:
    """Return simulated macro data."""
    random.seed(seed)
    dates = _gen_month_labels(months=months)

    return {
        "interest_rate": MacroSeries(dates=dates, values=_build_trend_series(2.0, 0.07, 0.08, months)),
        "cpi": MacroSeries(dates=dates, values=_build_trend_series(1.8, 0.03, 0.06, months)),
        "pmi": MacroSeries(dates=dates, values=_build_trend_series(49.0, 0.18, 0.45, months)),
        "vix": MacroSeries(dates=dates, values=_build_trend_series(17.0, 0.02, 0.9, months)),
        "dxy": MacroSeries(dates=dates, values=_build_trend_series(100.0, -0.06, 0.35, months)),
        "equity_index": MacroSeries(dates=dates, values=_build_trend_series(4200.0, 28.0, 35.0, months)),
        "bond_yield_10y": MacroSeries(dates=dates, values=_build_trend_series(2.2, 0.03, 0.08, months)),
    }


def _load_from_api() -> Dict[str, MacroSeries]:
    """Placeholder for real API integration.

    Replace this function with actual API calls (FRED, TradingEconomics, etc.)
    and map the output to `MacroSeries`.
    """
    raise NotImplementedError("API source is not configured yet. Please use source='mock' or implement your API adapters.")


def load_macro_data(source: DataSource = "mock", months: int = 12) -> Dict[str, MacroSeries]:
    """Public entry for loading macro and market validation data."""
    if source == "mock":
        return _load_from_mock(months=months)
    if source == "api":
        return _load_from_api()
    raise ValueError(f"Unsupported source: {source}")
