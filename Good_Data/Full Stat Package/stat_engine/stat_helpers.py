from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

AggMode = Literal["sum", "mean"]


def safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two scalars and return NaN for zero/NaN denominators."""
    if pd.isna(denominator) or float(denominator) == 0.0:
        return float("nan")
    return float(numerator) / float(denominator)


def safe_divide_series(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Elementwise division with NaN where denominator is zero/NaN."""
    num = pd.to_numeric(numerator, errors="coerce")
    den = pd.to_numeric(denominator, errors="coerce")
    return num.divide(den.replace({0: np.nan}))


def finalize_series(values: pd.Series, agg: bool, mode: AggMode = "sum") -> float | pd.Series:
    """Return season aggregate scalar or per-game series from a per-game stat series."""
    series = pd.to_numeric(values, errors="coerce")
    if not agg:
        return series
    if mode == "mean":
        return float(series.mean()) if not series.empty else float("nan")
    return float(series.sum())


def build_count_stat(team_games_df: pd.DataFrame, column: str, agg: bool = True) -> float | pd.Series:
    """Generic additive stat from a single per-game numeric column."""
    if column not in team_games_df.columns:
        raise KeyError(f"Missing required column: {column}")
    series = pd.to_numeric(team_games_df[column], errors="coerce")
    return finalize_series(series, agg=agg, mode="sum")


def build_ratio_stat(
    team_games_df: pd.DataFrame,
    numerator_col: str,
    denominator_col: str,
    agg: bool = True,
) -> float | pd.Series:
    """Generic ratio stat. Aggregate mode computes ratio of season totals."""
    if numerator_col not in team_games_df.columns:
        raise KeyError(f"Missing required column: {numerator_col}")
    if denominator_col not in team_games_df.columns:
        raise KeyError(f"Missing required column: {denominator_col}")

    num_series = pd.to_numeric(team_games_df[numerator_col], errors="coerce")
    den_series = pd.to_numeric(team_games_df[denominator_col], errors="coerce")

    if not agg:
        return safe_divide_series(num_series, den_series)

    return safe_divide(float(num_series.sum()), float(den_series.sum()))
