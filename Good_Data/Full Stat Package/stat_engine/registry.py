"""Central stat registry mapping abbreviations to functions and metadata."""

from __future__ import annotations

import csv
import os
import re
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from . import box_score_stats, kenpom_stats, pbp_stubs
from .stat_helpers import build_count_stat, build_ratio_stat, finalize_series, safe_divide


def _abbrev_to_function_name(abbrev: str) -> str:
    """Convert stat abbreviation to Python function name (calc_XXX)."""
    func_name = abbrev.strip().lower()
    # Replace spaces and special chars with underscores
    func_name = re.sub(r"[^\w]+", "_", func_name)
    # Remove leading/trailing underscores
    func_name = func_name.strip("_")
    return f"calc_{func_name}"


# Explicit abbrev → function name overrides where auto-translation fails.
# Keys are exact Full_Stat_Package_Team.csv abbreviations.
_ABBREV_ALIASES: dict[str, str] = {
    "%2PTS":       "calc_pct_pts_2p",
    "%3PTS":       "calc_pct_pts_3p",
    "%FTPTS":      "calc_pct_pts_ft",
    # Percentage stats: regex strips '%' but functions use _pct suffix
    "FG%":          "calc_fg_pct",
    "FT%":          "calc_ft_pct",
    "2P%":          "calc_2p_pct",
    "3P%":          "calc_3p_pct",
    "eFG%":         "calc_efg_pct",
    "TS%":          "calc_ts_pct",
    "TOV%":         "calc_tov_pct",
    "ORB%":         "calc_orb_pct",
    "DRB%":         "calc_drb_pct",
    "REB%":         "calc_trb_pct",
    # TOV naming: function uses 'to' not 'tov'
    "TOV":          "calc_to",
    # 3PAr: function uses 3p_ar not 3par
    "3PAr":         "calc_3p_ar",
    # FTA/FTM rate naming mismatches
    "FTA Rate":     "calc_ft_rate",
    "FTM Rate":     "calc_ft_pct",
    # Opponent/AGST stats: use calc_opp_* functions
    "FGM AGST":     "calc_opp_fgm",
    "FGA AGST":     "calc_opp_fga",
    "3PM AGST":     "calc_opp_3pm",
    "3PA AGST":     "calc_opp_3pa",
    "TOV AGST":     "calc_opp_to",
    # KenPom **Adj: pace-adjusted values (the actual adjusted number)
    "ORtg**Adj":    "calc_kp_adjoe",
    "DRtg**Adj":    "calc_kp_adjde",
    "Net Rtg**Adj": "calc_kp_adjem",
    "Pace**Adj":    "calc_kp_adjtempo",
    # KenPom Adj: adjustment delta/factor applied to reach **Adj
    "ORtg Adj":     "calc_kp_factor_ortg_adj",
    "DRtg Adj":     "calc_kp_factor_drtg_adj",
    "Pace Adj":     "calc_kp_factor_tempo_adj",
}

# Normalizer suffix patterns: strip suffix → route to base function,
# then auto-apply the corresponding normalizer in get_stat().
_NORMALIZER_SUFFIXES: dict[str, str] = {
    "/G":   "per_game",
    "/40":  "per_40",
    "/100": "per_100",
}


def _make_count_fn(column: str) -> Callable:
    def _fn(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
        return build_count_stat(df, column, agg=agg)

    return _fn


def _make_ratio_fn(numerator_col: str, denominator_col: str, scale: float = 1.0) -> Callable:
    def _fn(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
        if agg:
            value = build_ratio_stat(df, numerator_col, denominator_col, agg=True)
            return float(value) * scale

        ratio = build_ratio_stat(df, numerator_col, denominator_col, agg=False)
        return pd.to_numeric(ratio, errors="coerce") * scale

    return _fn


def _make_diff_fn(team_col: str, opp_col: str) -> Callable:
    def _fn(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
        team_series = pd.to_numeric(df[team_col], errors="coerce")
        opp_series = pd.to_numeric(df[opp_col], errors="coerce")
        return finalize_series(team_series - opp_series, agg=agg, mode="sum")

    return _fn


def _get_dynamic_box_score_function(abbrev: str) -> Callable | None:
    """Return callable for formula-derivable box score stats not defined as calc_* functions."""
    count_map: dict[str, str] = {
        "2PA AGST": "opp_fga2",
        "2PM AGST": "opp_fgm2",
        "BLKD": "opp_blk",
        "DRB AGST": "opp_drb",
        "FTA AGST": "opp_fta",
        "FTM AGST": "opp_ftm",
        "ORB AGST": "opp_orb",
        "PFD": "opp_pf",
        "PTS AGST": "opp_pts",
        "REB": "trb",
        "REB AGST": "opp_trb",
        "tf": "opp_to",
        "tmDrb": "drb",
        "tmOrb": "orb",
        "tmReb": "trb",
        "tmTov": "to",
    }
    if abbrev in count_map:
        return _make_count_fn(count_map[abbrev])

    ratio_map: dict[str, tuple[str, str, float]] = {
        "AST Ratio": ("ast", "poss_est", 100.0),
        "AST/TOV": ("ast", "to", 1.0),
        "BLK/PF": ("blk", "pf", 1.0),
        "STL/PF": ("stl", "pf", 1.0),
        "STL/TOV": ("stl", "to", 1.0),
        "FTA Rate Agst": ("opp_fta", "opp_fga", 1.0),
        "ORB% Agst": ("opp_orb", "opp_orb", 0.0),  # handled below
        "TOV% Agst": ("opp_to", "opp_to", 0.0),    # handled below
        "eFG% Agst": ("opp_fgm", "opp_fga", 0.0),  # handled below
    }
    if abbrev in ratio_map:
        if abbrev == "ORB% Agst":
            def _orb_pct_agst_fn(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
                opp_orb = pd.to_numeric(df["opp_orb"], errors="coerce")
                drb = pd.to_numeric(df["drb"], errors="coerce")
                denom = opp_orb + drb
                if agg:
                    return safe_divide(float(opp_orb.sum()), float(denom.sum()))
                return opp_orb.divide(denom.replace({0: float("nan")}))

            return _orb_pct_agst_fn
        if abbrev == "TOV% Agst":
            def _tov_pct_agst_fn(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
                opp_to = pd.to_numeric(df["opp_to"], errors="coerce")
                opp_fga = pd.to_numeric(df["opp_fga"], errors="coerce")
                opp_fta = pd.to_numeric(df["opp_fta"], errors="coerce")
                denom = opp_fga + 0.44 * opp_fta + opp_to
                if agg:
                    return safe_divide(float(opp_to.sum()), float(denom.sum()))
                return opp_to.divide(denom.replace({0: float("nan")}))

            return _tov_pct_agst_fn
        if abbrev == "eFG% Agst":
            def _efg_agst_fn(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
                opp_fgm = pd.to_numeric(df["opp_fgm"], errors="coerce")
                opp_fgm3 = pd.to_numeric(df["opp_fgm3"], errors="coerce")
                opp_fga = pd.to_numeric(df["opp_fga"], errors="coerce")
                numerator = opp_fgm + 0.5 * opp_fgm3
                if agg:
                    return safe_divide(float(numerator.sum()), float(opp_fga.sum()))
                return numerator.divide(opp_fga.replace({0: float("nan")}))

            return _efg_agst_fn
        num_col, den_col, scale = ratio_map[abbrev]
        return _make_ratio_fn(num_col, den_col, scale=scale)

    diff_map: dict[str, tuple[str, str]] = {
        "2PA DIFF": ("fga2", "opp_fga2"),
        "2PM DIFF": ("fgm2", "opp_fgm2"),
        "3PA DIFF": ("fga3", "opp_fga3"),
        "3PM DIFF": ("fgm3", "opp_fgm3"),
        "DRB DIFF": ("drb", "opp_drb"),
        "FGA DIFF": ("fga", "opp_fga"),
        "FGM DIFF": ("fgm", "opp_fgm"),
        "FTA DIFF": ("fta", "opp_fta"),
        "FTM DIFF": ("ftm", "opp_ftm"),
        "ORB DIFF": ("orb", "opp_orb"),
        "PTS DIFF": ("pts", "opp_pts"),
        "REB DIFF": ("trb", "opp_trb"),
        "TOV DIFF": ("to", "opp_to"),
    }
    if abbrev in diff_map:
        team_col, opp_col = diff_map[abbrev]
        return _make_diff_fn(team_col, opp_col)

    if abbrev == "GP" or abbrev == "GP*":
        def _gp(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
            if agg:
                return float(len(df))
            return pd.Series([1.0] * len(df), index=df.index, dtype=float)

        return _gp

    if abbrev == "Wins":
        return _make_count_fn("win")

    if abbrev == "Losses":
        def _losses(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
            wins = pd.to_numeric(df["win"], errors="coerce")
            losses = 1.0 - wins
            return finalize_series(losses, agg=agg, mode="sum")

        return _losses

    if abbrev == "MP" or abbrev == "MP*":
        def _minutes_played(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
            num_ot = pd.to_numeric(df["num_ot"], errors="coerce")
            minutes = 40.0 + 5.0 * num_ot
            return finalize_series(minutes, agg=agg, mode="sum")

        return _minutes_played

    if abbrev == "POSS":
        return _make_count_fn("poss_est")

    if abbrev == "oPoss":
        return _make_count_fn("poss_est_off")

    if abbrev == "dPoss":
        return _make_count_fn("poss_est_def")

    if abbrev == "tsa":
        def _tsa(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
            fga = pd.to_numeric(df["fga"], errors="coerce")
            fta = pd.to_numeric(df["fta"], errors="coerce")
            tsa = fga + 0.44 * fta
            return finalize_series(tsa, agg=agg, mode="sum")

        return _tsa

    if abbrev == "tfP100":
        return _make_ratio_fn("opp_to", "poss_est", scale=100.0)

    if abbrev == "tfP40":
        def _tf_per_40(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
            forced = pd.to_numeric(df["opp_to"], errors="coerce")
            num_ot = pd.to_numeric(df["num_ot"], errors="coerce")
            minutes = 40.0 + 5.0 * num_ot
            if agg:
                return safe_divide(float(forced.sum()), float(minutes.sum())) * 40.0
            return forced.divide(minutes.replace({0: float("nan")})) * 40.0

        return _tf_per_40

    if abbrev == "tfPg":
        def _tf_per_game(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
            forced = pd.to_numeric(df["opp_to"], errors="coerce")
            return finalize_series(forced, agg=agg, mode="mean")

        return _tf_per_game

    if abbrev == "ORBTV DIFF":
        def _orbtv_diff(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
            team = pd.to_numeric(df["orb"], errors="coerce") + pd.to_numeric(df["opp_to"], errors="coerce")
            opp = pd.to_numeric(df["opp_orb"], errors="coerce") + pd.to_numeric(df["to"], errors="coerce")
            return finalize_series(team - opp, agg=agg, mode="sum")

        return _orbtv_diff

    if abbrev == "RBTV DIFF":
        def _rbtv_diff(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
            team = pd.to_numeric(df["trb"], errors="coerce") + pd.to_numeric(df["opp_to"], errors="coerce")
            opp = pd.to_numeric(df["opp_trb"], errors="coerce") + pd.to_numeric(df["to"], errors="coerce")
            return finalize_series(team - opp, agg=agg, mode="sum")

        return _rbtv_diff

    return None


def _get_function_for_stat(abbrev: str, data_source: str) -> Callable | None:
    """
    Lookup and return the function for a stat.

    Args:
        abbrev: Stat abbreviation (e.g., 'ORtg', 'FG%', 'KP AdjOE', '%AST ATB3')
        data_source: 'box_score', 'kenpom', 'pbp', or mixed like 'box_score, pbp'

    Returns:
        Callable function or None if not found
    """
    # Check explicit alias map before auto-translation
    if abbrev in _ABBREV_ALIASES:
        func_name = _ABBREV_ALIASES[abbrev]
    else:
        # Handle normalizer suffix patterns (/G, /40, /100):
        # route to the base stat's function; normalizer is applied at call time.
        for suffix in _NORMALIZER_SUFFIXES:
            if abbrev.endswith(suffix):
                base_abbrev = abbrev[: -len(suffix)]
                return _get_function_for_stat(base_abbrev, data_source)
        func_name = _abbrev_to_function_name(abbrev)

    # Handle mixed data sources: prioritize box_score > kenpom > pbp
    if "box_score" in data_source:
        module = box_score_stats
    elif "kenpom" in data_source:
        module = kenpom_stats
    elif "pbp" in data_source:
        module = pbp_stubs
    else:
        return None

    func = getattr(module, func_name, None)
    if func is not None:
        return func

    if "box_score" in data_source:
        return _get_dynamic_box_score_function(abbrev)

    return None


def _build_registry() -> dict[str, dict[str, Any]]:
    """
    Build the stat registry from Full_Stat_Package_Team.csv.

    Returns:
        STAT_REGISTRY dict mapping abbrev → metadata record
    """
    registry: dict[str, dict[str, Any]] = {}

    # Locate CSV file
    csv_path = Path(__file__).parent.parent / "Full_Stat_Package_Team.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Stat package CSV not found at {csv_path}")

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            abbrev = row.get("Abbrev", "").strip()
            if not abbrev:
                continue

            data_source = row.get("Data Source", "").strip() or "unknown"
            stat_name = row.get("Stat Name", "").strip()
            description = row.get("Description", "").strip()
            unit = row.get("Unit", "").strip()
            pctile_dir = row.get("Pctile Dir", "").strip().lower() or "desc"

            # Attempt to find the function
            func = _get_function_for_stat(abbrev, data_source)

            # Determine status
            if func is not None:
                # Function exists - it's either implemented or a stub
                if "pbp" in data_source and "box_score" not in data_source:
                    # Pure PBP stat (no box_score alternative)
                    status = "stub"
                else:
                    status = "implemented"
            else:
                # Function not found
                status = "unavailable"

            # Determine if normalizable (has box_score version)
            normalizable = "box_score" in data_source and status == "implemented"

            registry[abbrev] = {
                "abbrev": abbrev,
                "stat_name": stat_name,
                "description": description,
                "unit": unit,
                "data_source": data_source,
                "pctile_dir": pctile_dir,
                "normalizable": normalizable,
                "status": status,
                "function": func,  # Store function reference for quick lookup
            }

    return registry


# Build registry once at module import
STAT_REGISTRY = _build_registry()


def get_stat(
    abbrev: str,
    team_games_df: pd.DataFrame | None = None,
    kenpom_row: dict[str, Any] | None = None,
    agg: bool = True,
    normalize: str | None = None,
) -> float | pd.Series | None:
    """
    Get a stat value for a team season.

    Args:
        abbrev: Stat abbreviation (e.g., 'ORtg', 'FG%', 'KP AdjOE')
        team_games_df: DataFrame from load_team_season() (required for box_score stats)
        kenpom_row: Dict from load_kenpom() (required for kenpom stats)
        agg: Return season aggregate (True) or per-game series (False)
        normalize: Apply normalizer ('per_game', 'per_40', 'per_100', or None)

    Returns:
        Computed stat value (scalar if agg=True, series if agg=False)
        None if stat unavailable or insufficient data

    Raises:
        KeyError: If abbrev not in registry
        ValueError: If data requirements not met
        NotImplementedError: If PBP stat and data unavailable
    """
    if abbrev not in STAT_REGISTRY:
        raise KeyError(f"Unknown stat abbreviation: {abbrev}")

    meta = STAT_REGISTRY[abbrev]
    func = meta.get("function")
    data_source = meta.get("data_source")
    status = meta.get("status")

    # Check data availability
    if status == "unavailable":
        return None

    if status == "stub" or data_source == "pbp":
        raise NotImplementedError(
            f"PBP data not yet available: {abbrev}"
        )

    # Auto-apply normalizer for /G, /40, /100 suffix stats
    if normalize is None and "box_score" in (data_source or ""):
        for suffix, norm_name in _NORMALIZER_SUFFIXES.items():
            if abbrev.endswith(suffix):
                normalize = norm_name
                break

    if "box_score" in (data_source or ""):
        if team_games_df is None:
            raise ValueError(
                f"Box score stat '{abbrev}' requires team_games_df parameter"
            )
        result = func(team_games_df, agg=agg)

    elif data_source == "kenpom":
        if kenpom_row is None:
            raise ValueError(
                f"KenPom stat '{abbrev}' requires kenpom_row parameter"
            )
        result = func(kenpom_row)
        # KenPom stats are always scalar; agg parameter doesn't apply
        # but we return as-is (don't force conversion)

    else:
        return None

    # Apply normalizer if requested
    if normalize is not None:
        if data_source == "kenpom":
            raise ValueError(
                f"KenPom stats cannot be normalized ('{abbrev}' is already pace-adjusted)"
            )

        if not meta.get("normalizable"):
            raise ValueError(
                f"Stat '{abbrev}' cannot be normalized (status: {status})"
            )

        # Import normalizers
        from . import normalizers

        # Create a wrapper that handles the agg parameter
        def base_fn_wrapper(df, agg=True):
            return func(df, agg=agg)

        if normalize == "per_game":
            result = normalizers.per_game(base_fn_wrapper, team_games_df, agg=agg)
        elif normalize == "per_40":
            result = normalizers.per_40(base_fn_wrapper, team_games_df, agg=agg)
        elif normalize == "per_100":
            result = normalizers.per_100_poss(base_fn_wrapper, team_games_df, agg=agg)
        else:
            raise ValueError(
                f"Unknown normalizer: {normalize}. Options: 'per_game', 'per_40', 'per_100'"
            )

    return result


def stat_meta(abbrev: str) -> dict[str, Any]:
    """
    Get metadata for a stat.

    Args:
        abbrev: Stat abbreviation (e.g., 'ORtg')

    Returns:
        Dict with stat metadata:
        - abbrev, stat_name, description, unit
        - data_source (box_score, kenpom, pbp)
        - pctile_dir (desc=higher better, asc=lower better)
        - normalizable (can apply per_game/per_40/per_100)
        - status (implemented, stub, unavailable)

    Raises:
        KeyError: If abbrev not in registry
    """
    if abbrev not in STAT_REGISTRY:
        raise KeyError(f"Unknown stat abbreviation: {abbrev}")

    meta = STAT_REGISTRY[abbrev].copy()
    # Remove function reference from returned dict
    meta.pop("function", None)
    return meta


def list_stats(data_source: str | None = None, status: str | None = None) -> list[str]:
    """
    List available stat abbreviations, optionally filtered.

    Args:
        data_source: Filter by 'box_score', 'kenpom', or 'pbp' (None = all)
        status: Filter by 'implemented', 'stub', or 'unavailable' (None = all)

    Returns:
        Sorted list of stat abbreviations
    """
    abbrevs = []
    for abbrev, meta in STAT_REGISTRY.items():
        if data_source and meta["data_source"] != data_source:
            continue
        if status and meta["status"] != status:
            continue
        abbrevs.append(abbrev)

    return sorted(abbrevs)


def stats_by_source() -> dict[str, list[str]]:
    """
    Get stat counts grouped by data source.

    Returns:
        Dict with keys 'box_score', 'kenpom', 'pbp' and counts
    """
    result = {"box_score": [], "kenpom": [], "pbp": [], "unknown": []}
    for abbrev, meta in STAT_REGISTRY.items():
        source = meta.get("data_source", "unknown")
        if source in result:
            result[source].append(abbrev)
    return {key: sorted(vals) for key, vals in result.items()}


def stats_by_status() -> dict[str, list[str]]:
    """
    Get stat counts grouped by implementation status.

    Returns:
        Dict with keys 'implemented', 'stub', 'unavailable' and stat lists
    """
    result = {"implemented": [], "stub": [], "unavailable": []}
    for abbrev, meta in STAT_REGISTRY.items():
        status = meta.get("status", "unavailable")
        if status in result:
            result[status].append(abbrev)
    return {key: sorted(vals) for key, vals in result.items()}


def registry_summary() -> dict[str, int]:
    """
    Get summary statistics about the registry.

    Returns:
        Dict with total count and breakdown by source/status
    """
    by_source = stats_by_source()
    by_status = stats_by_status()

    return {
        "total": len(STAT_REGISTRY),
        "box_score": len(by_source["box_score"]),
        "kenpom": len(by_source["kenpom"]),
        "pbp": len(by_source["pbp"]),
        "implemented": len(by_status["implemented"]),
        "stub": len(by_status["stub"]),
        "unavailable": len(by_status["unavailable"]),
    }
