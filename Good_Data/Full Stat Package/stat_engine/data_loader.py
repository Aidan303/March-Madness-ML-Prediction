from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd

DataType = Literal["regular", "tourney", "both"]

_BASE_DATA_DIR = (
    Path(__file__).resolve().parents[2] / "march-machine-learning-mania-2026-base-data"
)

_CANONICAL_COLUMNS = [
    "season",
    "day_num",
    "team_id",
    "opp_id",
    "pts",
    "opp_pts",
    "fgm",
    "fga",
    "fgm3",
    "fga3",
    "ftm",
    "fta",
    "orb",
    "drb",
    "ast",
    "to",
    "stl",
    "blk",
    "pf",
    "opp_fgm",
    "opp_fga",
    "opp_fgm3",
    "opp_fga3",
    "opp_ftm",
    "opp_fta",
    "opp_orb",
    "opp_drb",
    "opp_ast",
    "opp_to",
    "opp_stl",
    "opp_blk",
    "opp_pf",
    "is_home",
    "num_ot",
    "win",
]


def _resolve_base_data_dir(data_dir: str | Path | None) -> Path:
    if data_dir is None:
        return _BASE_DATA_DIR
    return Path(data_dir)


def _read_results_csv(csv_path: Path, season: int) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing results file: {csv_path}")

    df = pd.read_csv(csv_path)
    return df[df["Season"] == season].copy()


def _winner_is_home(loc: object) -> object:
    if loc == "H":
        return True
    if loc == "A":
        return False
    return pd.NA


def _loser_is_home(loc: object) -> object:
    if loc == "H":
        return False
    if loc == "A":
        return True
    return pd.NA


def _to_team_rows(results_df: pd.DataFrame) -> pd.DataFrame:
    winner_rows = pd.DataFrame(
        {
            "season": results_df["Season"],
            "day_num": results_df["DayNum"],
            "team_id": results_df["WTeamID"],
            "opp_id": results_df["LTeamID"],
            "pts": results_df["WScore"],
            "opp_pts": results_df["LScore"],
            "fgm": results_df["WFGM"],
            "fga": results_df["WFGA"],
            "fgm3": results_df["WFGM3"],
            "fga3": results_df["WFGA3"],
            "ftm": results_df["WFTM"],
            "fta": results_df["WFTA"],
            "orb": results_df["WOR"],
            "drb": results_df["WDR"],
            "ast": results_df["WAst"],
            "to": results_df["WTO"],
            "stl": results_df["WStl"],
            "blk": results_df["WBlk"],
            "pf": results_df["WPF"],
            "opp_fgm": results_df["LFGM"],
            "opp_fga": results_df["LFGA"],
            "opp_fgm3": results_df["LFGM3"],
            "opp_fga3": results_df["LFGA3"],
            "opp_ftm": results_df["LFTM"],
            "opp_fta": results_df["LFTA"],
            "opp_orb": results_df["LOR"],
            "opp_drb": results_df["LDR"],
            "opp_ast": results_df["LAst"],
            "opp_to": results_df["LTO"],
            "opp_stl": results_df["LStl"],
            "opp_blk": results_df["LBlk"],
            "opp_pf": results_df["LPF"],
            "is_home": results_df["WLoc"].map(_winner_is_home),
            "num_ot": results_df["NumOT"],
            "win": 1,
        }
    )

    loser_rows = pd.DataFrame(
        {
            "season": results_df["Season"],
            "day_num": results_df["DayNum"],
            "team_id": results_df["LTeamID"],
            "opp_id": results_df["WTeamID"],
            "pts": results_df["LScore"],
            "opp_pts": results_df["WScore"],
            "fgm": results_df["LFGM"],
            "fga": results_df["LFGA"],
            "fgm3": results_df["LFGM3"],
            "fga3": results_df["LFGA3"],
            "ftm": results_df["LFTM"],
            "fta": results_df["LFTA"],
            "orb": results_df["LOR"],
            "drb": results_df["LDR"],
            "ast": results_df["LAst"],
            "to": results_df["LTO"],
            "stl": results_df["LStl"],
            "blk": results_df["LBlk"],
            "pf": results_df["LPF"],
            "opp_fgm": results_df["WFGM"],
            "opp_fga": results_df["WFGA"],
            "opp_fgm3": results_df["WFGM3"],
            "opp_fga3": results_df["WFGA3"],
            "opp_ftm": results_df["WFTM"],
            "opp_fta": results_df["WFTA"],
            "opp_orb": results_df["WOR"],
            "opp_drb": results_df["WDR"],
            "opp_ast": results_df["WAst"],
            "opp_to": results_df["WTO"],
            "opp_stl": results_df["WStl"],
            "opp_blk": results_df["WBlk"],
            "opp_pf": results_df["WPF"],
            "is_home": results_df["WLoc"].map(_loser_is_home),
            "num_ot": results_df["NumOT"],
            "win": 0,
        }
    )

    out = pd.concat([winner_rows, loser_rows], ignore_index=True)
    out = out[_CANONICAL_COLUMNS].sort_values(["day_num", "team_id", "opp_id"]).reset_index(drop=True)
    return out


def _add_derived_columns(team_df: pd.DataFrame) -> pd.DataFrame:
    team_df = team_df.copy()

    team_df["fgm2"] = team_df["fgm"] - team_df["fgm3"]
    team_df["fga2"] = team_df["fga"] - team_df["fga3"]
    team_df["opp_fgm2"] = team_df["opp_fgm"] - team_df["opp_fgm3"]
    team_df["opp_fga2"] = team_df["opp_fga"] - team_df["opp_fga3"]

    team_df["trb"] = team_df["orb"] + team_df["drb"]
    team_df["opp_trb"] = team_df["opp_orb"] + team_df["opp_drb"]

    own_poss = team_df["fga"] - team_df["orb"] + team_df["to"] + 0.44 * team_df["fta"]
    opp_poss = team_df["opp_fga"] - team_df["opp_orb"] + team_df["opp_to"] + 0.44 * team_df["opp_fta"]
    team_df["poss_est"] = (own_poss + opp_poss) / 2.0

    # Defensive possessions can differ slightly from offensive estimate due to rounding.
    team_df["poss_est_off"] = own_poss
    team_df["poss_est_def"] = opp_poss

    return team_df


def load_team_season(
    team_id: int,
    season: int,
    data_dir: str | Path | None = None,
    data_type: DataType = "regular",
) -> pd.DataFrame:
    """Load canonical team-game rows for one team and season.

    Parameters
    ----------
    team_id:
        Kaggle TeamID for the target team.
    season:
        Season to load (e.g. 2026).
    data_dir:
        Directory containing Kaggle base-data CSV files. Defaults to
        Good_Data/march-machine-learning-mania-2026-base-data.
    data_type:
        Which game set to include: "regular", "tourney", or "both".

    Returns
    -------
    pd.DataFrame
        Team-centric game rows in canonical format with derived columns.
    """
    valid_types: set[DataType] = {"regular", "tourney", "both"}
    if data_type not in valid_types:
        raise ValueError(f"data_type must be one of {valid_types}, got {data_type!r}")

    base_dir = _resolve_base_data_dir(data_dir)
    pieces: list[pd.DataFrame] = []

    if data_type in {"regular", "both"}:
        regular_results = _read_results_csv(base_dir / "MRegularSeasonDetailedResults.csv", season)
        pieces.append(_to_team_rows(regular_results))

    if data_type in {"tourney", "both"}:
        tourney_results = _read_results_csv(base_dir / "MNCAATourneyDetailedResults.csv", season)
        pieces.append(_to_team_rows(tourney_results))

    if not pieces:
        return pd.DataFrame(columns=_CANONICAL_COLUMNS)

    all_games = pd.concat(pieces, ignore_index=True)
    team_games = all_games[all_games["team_id"] == team_id].copy()
    team_games = team_games.sort_values(["day_num", "opp_id"]).reset_index(drop=True)

    if team_games.empty:
        return _add_derived_columns(team_games)

    numeric_cols = [
        "pts",
        "opp_pts",
        "fgm",
        "fga",
        "fgm3",
        "fga3",
        "ftm",
        "fta",
        "orb",
        "drb",
        "ast",
        "to",
        "stl",
        "blk",
        "pf",
        "opp_fgm",
        "opp_fga",
        "opp_fgm3",
        "opp_fga3",
        "opp_ftm",
        "opp_fta",
        "opp_orb",
        "opp_drb",
        "opp_ast",
        "opp_to",
        "opp_stl",
        "opp_blk",
        "opp_pf",
        "num_ot",
        "win",
    ]

    for col in numeric_cols:
        team_games[col] = pd.to_numeric(team_games[col], errors="coerce")

    team_games["is_home"] = team_games["is_home"].astype("boolean")

    return _add_derived_columns(team_games)
