"""KenPom-based statistics (Adjusted stats)."""

from __future__ import annotations

from typing import Any


def _extract_stat(kenpom_row: dict[str, Any], stat_key: str) -> float | None:
    """Safely extract stat from KenPom dict, returning None if missing."""
    if kenpom_row is None:
        return None
    val = kenpom_row.get(stat_key)
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Primary adjusted stats
# ─────────────────────────────────────────────────────────────────────────────


def calc_kp_adjoe(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Adjusted Offensive Efficiency (points per 100 possessions, pace-adjusted)."""
    return _extract_stat(kenpom_row, "kp_adjoe")


def calc_kp_adjde(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Adjusted Defensive Efficiency (points allowed per 100 possessions, pace-adjusted)."""
    return _extract_stat(kenpom_row, "kp_adjde")


def calc_kp_adjtempo(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Adjusted Tempo (possessions per game, adjust for strength of schedule)."""
    return _extract_stat(kenpom_row, "kp_adjtempo")


def calc_kp_adjem(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Adjusted Efficiency Margin (AdjOE - AdjDE)."""
    return _extract_stat(kenpom_row, "kp_adjem")


def calc_kp_adjnetrtg(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Adjusted Net Rating (alias for AdjEM)."""
    return _extract_stat(kenpom_row, "kp_adjnetrtg")


# ─────────────────────────────────────────────────────────────────────────────
# Adjusted deltas / strength adjustments
# ─────────────────────────────────────────────────────────────────────────────


def calc_kp_factor_ortg_adj(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Offensive Efficiency adjustment factor (AdjOE specific)."""
    return _extract_stat(kenpom_row, "kp_factor_ortg_adj")


def calc_kp_factor_drtg_adj(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Defensive Efficiency adjustment factor (AdjDE specific)."""
    return _extract_stat(kenpom_row, "kp_factor_drtg_adj")


def calc_kp_factor_tempo_adj(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Tempo adjustment factor (AdjTempo specific)."""
    return _extract_stat(kenpom_row, "kp_factor_tempo_adj")


# ─────────────────────────────────────────────────────────────────────────────
# Ranking and seeding
# ─────────────────────────────────────────────────────────────────────────────


def calc_kp_rank_overall(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Overall Ranking (by Adjusted Net Rating)."""
    return _extract_stat(kenpom_row, "kp_rank_overall")


def calc_kp_rank_offrtg(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Offensive Efficiency Ranking."""
    return _extract_stat(kenpom_row, "kp_rank_offrtg")


def calc_kp_rank_defrtg(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Defensive Efficiency Ranking."""
    return _extract_stat(kenpom_row, "kp_rank_defrtg")


def calc_kp_rank_tempo(kenpom_row: dict[str, Any]) -> float | None:
    """KenPom Tempo Ranking."""
    return _extract_stat(kenpom_row, "kp_rank_tempo")


def calc_kp_seed(kenpom_row: dict[str, Any]) -> float | None:
    """NCAA Tournament Seed (if available from KenPom predictions)."""
    return _extract_stat(kenpom_row, "kp_seed")
