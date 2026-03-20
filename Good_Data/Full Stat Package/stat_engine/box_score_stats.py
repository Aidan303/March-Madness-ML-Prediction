"""Box score-computable basketball statistics."""

from __future__ import annotations

import pandas as pd

from .stat_helpers import build_count_stat, build_ratio_stat, finalize_series, safe_divide


# ─────────────────────────────────────────────────────────────────────────────
# Shooting stats: raw counts and percentages
# ─────────────────────────────────────────────────────────────────────────────


def calc_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goals made."""
    return build_count_stat(df, "fgm", agg=agg)


def calc_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal attempts."""
    return build_count_stat(df, "fga", agg=agg)


def calc_fg_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Field goal percentage (FGM / FGA)."""
    return build_ratio_stat(df, "fgm", "fga", agg=agg)


def calc_2pm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """2-point field goals made."""
    return build_count_stat(df, "fgm2", agg=agg)


def calc_2pa(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """2-point field goal attempts."""
    return build_count_stat(df, "fga2", agg=agg)


def calc_2p_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """2-point field goal percentage (2PM / 2PA)."""
    return build_ratio_stat(df, "fgm2", "fga2", agg=agg)


def calc_3pm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """3-point field goals made."""
    return build_count_stat(df, "fgm3", agg=agg)


def calc_3pa(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """3-point field goal attempts."""
    return build_count_stat(df, "fga3", agg=agg)


def calc_3p_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """3-point field goal percentage (3PM / 3PA)."""
    return build_ratio_stat(df, "fgm3", "fga3", agg=agg)


def calc_3p_ar(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """3-point attempt rate (3PA / FGA)."""
    return build_ratio_stat(df, "fga3", "fga", agg=agg)


def calc_ftm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Free throws made."""
    return build_count_stat(df, "ftm", agg=agg)


def calc_fta(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Free throw attempts."""
    return build_count_stat(df, "fta", agg=agg)


def calc_ft_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Free throw percentage (FTM / FTA)."""
    return build_ratio_stat(df, "ftm", "fta", agg=agg)


# ─────────────────────────────────────────────────────────────────────────────
# Advanced shooting efficiency
# ─────────────────────────────────────────────────────────────────────────────


def calc_efg_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Effective field goal percentage: (FGM + 0.5 * 3PM) / FGA."""
    fgm_series = pd.to_numeric(df["fgm"], errors="coerce")
    fgm3_series = pd.to_numeric(df["fgm3"], errors="coerce")
    fga_series = pd.to_numeric(df["fga"], errors="coerce")

    numerator = fgm_series + 0.5 * fgm3_series
    if not agg:
        return numerator.divide(fga_series.replace({0: float("nan")}))

    return safe_divide(float(numerator.sum()), float(fga_series.sum()))


def calc_ts_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """True shooting percentage: PTS / (2 * TSA), where TSA = FGA + 0.44 * FTA."""
    pts_series = pd.to_numeric(df["pts"], errors="coerce")
    fga_series = pd.to_numeric(df["fga"], errors="coerce")
    fta_series = pd.to_numeric(df["fta"], errors="coerce")

    tsa = fga_series + 0.44 * fta_series
    numerator = pts_series
    denominator = 2 * tsa

    if not agg:
        return numerator.divide(denominator.replace({0: float("nan")}))

    return safe_divide(float(numerator.sum()), float(denominator.sum()))


def calc_ft_rate(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Free throw rate: FTA / FGA."""
    return build_ratio_stat(df, "fta", "fga", agg=agg)


# ─────────────────────────────────────────────────────────────────────────────
# Points and scoring breakdown
# ─────────────────────────────────────────────────────────────────────────────


def calc_pts(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Points scored."""
    return build_count_stat(df, "pts", agg=agg)


def calc_pts_2p(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Points from 2-pointers: 2PM * 2."""
    fgm2_series = pd.to_numeric(df["fgm2"], errors="coerce")
    pts_2p = fgm2_series * 2
    return finalize_series(pts_2p, agg=agg, mode="sum")


def calc_pts_3p(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Points from 3-pointers: 3PM * 3."""
    fgm3_series = pd.to_numeric(df["fgm3"], errors="coerce")
    pts_3p = fgm3_series * 3
    return finalize_series(pts_3p, agg=agg, mode="sum")


def calc_pts_ft(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Points from free throws: FTM * 1."""
    return build_count_stat(df, "ftm", agg=agg)


def calc_pct_pts_2p(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """% of total points from 2-pointers."""
    pts_2p_series = pd.to_numeric(df["fgm2"], errors="coerce") * 2
    pts_series = pd.to_numeric(df["pts"], errors="coerce")

    if not agg:
        return pts_2p_series.divide(pts_series.replace({0: float("nan")}))

    return safe_divide(float(pts_2p_series.sum()), float(pts_series.sum()))


def calc_pct_pts_3p(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """% of total points from 3-pointers."""
    pts_3p_series = pd.to_numeric(df["fgm3"], errors="coerce") * 3
    pts_series = pd.to_numeric(df["pts"], errors="coerce")

    if not agg:
        return pts_3p_series.divide(pts_series.replace({0: float("nan")}))

    return safe_divide(float(pts_3p_series.sum()), float(pts_series.sum()))


def calc_pct_pts_ft(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """% of total points from free throws."""
    ftm_series = pd.to_numeric(df["ftm"], errors="coerce")
    pts_series = pd.to_numeric(df["pts"], errors="coerce")

    if not agg:
        return ftm_series.divide(pts_series.replace({0: float("nan")}))

    return safe_divide(float(ftm_series.sum()), float(pts_series.sum()))


# ─────────────────────────────────────────────────────────────────────────────
# Rebounding stats
# ─────────────────────────────────────────────────────────────────────────────


def calc_orb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Offensive rebounds."""
    return build_count_stat(df, "orb", agg=agg)


def calc_drb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Defensive rebounds."""
    return build_count_stat(df, "drb", agg=agg)


def calc_trb(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total rebounds."""
    return build_count_stat(df, "trb", agg=agg)


def calc_orb_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Offensive rebound percentage: ORB / (ORB + Opp DRB)."""
    orb_series = pd.to_numeric(df["orb"], errors="coerce")
    opp_drb_series = pd.to_numeric(df["opp_drb"], errors="coerce")

    denom = orb_series + opp_drb_series

    if not agg:
        return orb_series.divide(denom.replace({0: float("nan")}))

    return safe_divide(float(orb_series.sum()), float(denom.sum()))


def calc_drb_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Defensive rebound percentage: DRB / (DRB + Opp ORB)."""
    drb_series = pd.to_numeric(df["drb"], errors="coerce")
    opp_orb_series = pd.to_numeric(df["opp_orb"], errors="coerce")

    denom = drb_series + opp_orb_series

    if not agg:
        return drb_series.divide(denom.replace({0: float("nan")}))

    return safe_divide(float(drb_series.sum()), float(denom.sum()))


def calc_trb_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Total rebound percentage: TRB / (TRB + Opp TRB)."""
    return build_ratio_stat(df, "trb", "opp_trb", agg=agg)


# ─────────────────────────────────────────────────────────────────────────────
# Other individual stats
# ─────────────────────────────────────────────────────────────────────────────


def calc_ast(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Assists."""
    return build_count_stat(df, "ast", agg=agg)


def calc_to(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Turnovers."""
    return build_count_stat(df, "to", agg=agg)


def calc_stl(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Steals."""
    return build_count_stat(df, "stl", agg=agg)


def calc_blk(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Blocks."""
    return build_count_stat(df, "blk", agg=agg)


def calc_pf(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Personal fouls."""
    return build_count_stat(df, "pf", agg=agg)


# ─────────────────────────────────────────────────────────────────────────────
# Four Factors and Pace/Efficiency
# ─────────────────────────────────────────────────────────────────────────────


def calc_tov_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Turnover percentage: TOV / (FGA + 0.44 * FTA + TOV)."""
    to_series = pd.to_numeric(df["to"], errors="coerce")
    fga_series = pd.to_numeric(df["fga"], errors="coerce")
    fta_series = pd.to_numeric(df["fta"], errors="coerce")

    denom = fga_series + 0.44 * fta_series + to_series

    if not agg:
        return to_series.divide(denom.replace({0: float("nan")}))

    return safe_divide(float(to_series.sum()), float(denom.sum()))


def calc_pace(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Possessions per game, using poss_est and game count."""
    poss_series = pd.to_numeric(df["poss_est"], errors="coerce")

    if not agg:
        return poss_series

    return float(poss_series.mean()) if not poss_series.empty else float("nan")


def calc_ortg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Offensive rating (raw): PTS / Poss * 100."""
    pts_series = pd.to_numeric(df["pts"], errors="coerce")
    poss_series = pd.to_numeric(df["poss_est"], errors="coerce")

    ortg = pts_series.divide(poss_series.replace({0: float("nan")})) * 100

    if not agg:
        return ortg

    return safe_divide(float(pts_series.sum()), float(poss_series.sum())) * 100


def calc_drtg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Defensive rating (raw): Opp PTS / Opp Poss * 100."""
    opp_pts_series = pd.to_numeric(df["opp_pts"], errors="coerce")
    opp_poss_series = pd.to_numeric(df["poss_est"], errors="coerce")

    drtg = opp_pts_series.divide(opp_poss_series.replace({0: float("nan")})) * 100

    if not agg:
        return drtg

    return safe_divide(float(opp_pts_series.sum()), float(opp_poss_series.sum())) * 100


def calc_net_rtg(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Net rating: ORtg - DRtg."""
    ortg_series = pd.to_numeric(calc_ortg(df, agg=False), errors="coerce")
    drtg_series = pd.to_numeric(calc_drtg(df, agg=False), errors="coerce")

    net = ortg_series - drtg_series

    if not agg:
        return net

    return float(net.mean()) if not net.empty else float("nan")


# ─────────────────────────────────────────────────────────────────────────────
# Opponent stats (for reference; these use defensive perspective)
# ─────────────────────────────────────────────────────────────────────────────


def calc_opp_fgm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Opponent field goals made."""
    return build_count_stat(df, "opp_fgm", agg=agg)


def calc_opp_fga(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Opponent field goal attempts."""
    return build_count_stat(df, "opp_fga", agg=agg)


def calc_opp_fg_pct(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Opponent field goal percentage."""
    return build_ratio_stat(df, "opp_fgm", "opp_fga", agg=agg)


def calc_opp_3pm(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Opponent 3-pointers made."""
    return build_count_stat(df, "opp_fgm3", agg=agg)


def calc_opp_3pa(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Opponent 3-point attempts."""
    return build_count_stat(df, "opp_fga3", agg=agg)


def calc_opp_ast(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Opponent assists."""
    return build_count_stat(df, "opp_ast", agg=agg)


def calc_opp_to(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:
    """Opponent turnovers."""
    return build_count_stat(df, "opp_to", agg=agg)
