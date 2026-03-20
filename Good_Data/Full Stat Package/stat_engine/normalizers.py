from __future__ import annotations

from typing import Callable, Literal

import numpy as np
import pandas as pd

from .stat_helpers import safe_divide

StatFn = Callable[..., float | pd.Series]
AggregateMode = Literal["from_aggregate_total", "mean_of_per_game_values"]


def _coerce_series(value: float | pd.Series, index: pd.Index) -> pd.Series:
    if isinstance(value, pd.Series):
        return pd.to_numeric(value, errors="coerce")
    # Broadcast scalar across rows when needed.
    return pd.Series([value] * len(index), index=index, dtype="float64")


def _game_minutes(team_games_df: pd.DataFrame, regulation_minutes: float = 40.0, ot_minutes: float = 5.0) -> pd.Series:
    num_ot = pd.to_numeric(team_games_df.get("num_ot", 0), errors="coerce").fillna(0)
    return regulation_minutes + (ot_minutes * num_ot)


def _possessions(team_games_df: pd.DataFrame, poss_col: str = "poss_est") -> pd.Series:
    if poss_col not in team_games_df.columns:
        raise KeyError(f"Missing required possessions column: {poss_col}")
    return pd.to_numeric(team_games_df[poss_col], errors="coerce")


def per_game(
    base_fn: StatFn,
    team_games_df: pd.DataFrame,
    agg: bool = True,
    aggregate_mode: AggregateMode = "from_aggregate_total",
    **kwargs,
) -> float | pd.Series:
    """Normalize an additive base stat to per-game.

    For `agg=False`, returns the per-game series from `base_fn(..., agg=False)`.
    For `agg=True`:
      - from_aggregate_total: base_fn(..., agg=True) / game_count
      - mean_of_per_game_values: mean(base_fn(..., agg=False))
    """
    games = len(team_games_df)
    if games == 0:
        return float("nan") if agg else pd.Series(dtype="float64")

    if not agg:
        return _coerce_series(base_fn(team_games_df, agg=False, **kwargs), team_games_df.index)

    if aggregate_mode == "mean_of_per_game_values":
        series = _coerce_series(base_fn(team_games_df, agg=False, **kwargs), team_games_df.index)
        return float(series.mean())

    total = float(base_fn(team_games_df, agg=True, **kwargs))
    return safe_divide(total, float(games))


def per_40(
    base_fn: StatFn,
    team_games_df: pd.DataFrame,
    agg: bool = True,
    aggregate_mode: AggregateMode = "from_aggregate_total",
    regulation_minutes: float = 40.0,
    ot_minutes: float = 5.0,
    **kwargs,
) -> float | pd.Series:
    """Normalize a base stat to per-40 minutes using game minutes + OT."""
    minutes = _game_minutes(team_games_df, regulation_minutes=regulation_minutes, ot_minutes=ot_minutes)

    if not agg:
        series = _coerce_series(base_fn(team_games_df, agg=False, **kwargs), team_games_df.index)
        return series.divide(minutes.replace({0: np.nan})).mul(40.0)

    if len(team_games_df) == 0:
        return float("nan")

    if aggregate_mode == "mean_of_per_game_values":
        game_vals = _coerce_series(base_fn(team_games_df, agg=False, **kwargs), team_games_df.index)
        per_game_40 = game_vals.divide(minutes.replace({0: np.nan})).mul(40.0)
        return float(per_game_40.mean())

    total = float(base_fn(team_games_df, agg=True, **kwargs))
    total_minutes = float(minutes.sum())
    return safe_divide(total * 40.0, total_minutes)


def per_100_poss(
    base_fn: StatFn,
    team_games_df: pd.DataFrame,
    agg: bool = True,
    poss_col: str = "poss_est",
    aggregate_mode: AggregateMode = "from_aggregate_total",
    **kwargs,
) -> float | pd.Series:
    """Normalize a base stat to per-100 possessions."""
    poss = _possessions(team_games_df, poss_col=poss_col)

    if not agg:
        series = _coerce_series(base_fn(team_games_df, agg=False, **kwargs), team_games_df.index)
        return series.divide(poss.replace({0: np.nan})).mul(100.0)

    if len(team_games_df) == 0:
        return float("nan")

    if aggregate_mode == "mean_of_per_game_values":
        game_vals = _coerce_series(base_fn(team_games_df, agg=False, **kwargs), team_games_df.index)
        per_game_100 = game_vals.divide(poss.replace({0: np.nan})).mul(100.0)
        return float(per_game_100.mean())

    total = float(base_fn(team_games_df, agg=True, **kwargs))
    total_poss = float(poss.sum())
    return safe_divide(total * 100.0, total_poss)
