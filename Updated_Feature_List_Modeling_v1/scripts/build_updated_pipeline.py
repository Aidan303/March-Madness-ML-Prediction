from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "Updated_Feature_List_Modeling_v1"
OUT_CONFIG = OUT_ROOT / "config"
OUT_DATA = OUT_ROOT / "data"

FULL_STAT_DIR = ROOT / "Good_Data" / "Full Stat Package"
sys.path.insert(0, str(FULL_STAT_DIR))

from stat_engine import get_stat  # noqa: E402

HIST_MASTER_PATH = (
    ROOT
    / "Good_Data"
    / "Master Data"
    / "Master CSV File and Support Files"
    / "master_features_all_teams_historical.csv"
)
CUR_MASTER_PATH = (
    ROOT
    / "Good_Data"
    / "Master Data"
    / "Master CSV File and Support Files"
    / "master_features_all_teams_2026.csv"
)
LOCKED_CORE_PATH = (
    ROOT
    / "Good_Data"
    / "Master Data"
    / "Pruned Feature Sets (Gold)"
    / "locked_feature_set_core.csv"
)
FULL_STAT_TEAM_PATH = ROOT / "Good_Data" / "Full Stat Package" / "Full_Stat_Package_Team.csv"

KAGGLE_DIR = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"
REG_DETAILED_RESULTS_PATH = KAGGLE_DIR / "MRegularSeasonDetailedResults.csv"
TOURNEY_COMPACT_RESULTS_PATH = KAGGLE_DIR / "MNCAATourneyCompactResults.csv"

SEEDS_PATH = KAGGLE_DIR / "MNCAATourneySeeds.csv"
SLOTS_PATH = KAGGLE_DIR / "MNCAATourneySlots.csv"

ROUND_DAY_THRESHOLDS = {
    "reached_sweet16": 143,
    "reached_elite8": 145,
    "reached_final4": 152,
    "reached_title_game": 154,
}

ID_COLS = ["Season", "TeamID", "TeamName", "ConfAbbrev", "is_tourney_team", "tourney_seed_num"]


# Existing master features that already represent a stat concept.
# If a Michigan-enabled stat maps to one of these columns, it should NOT be added
# as a new feature column.
MASTER_STAT_ALIAS_TO_FEATURE: dict[str, str] = {
    "ORtg**Adj": "kp_adjoe",
    "Net Rtg**Adj": "kp_adjem",
    "Pace**Adj": "kp_adjtempo",
    "AST/TOV": "rs_ast_to_ratio",
    "DRB": "rs_drb",
    "FGM": "rs_fgm",
    "FGA": "rs_fga",
    "3PM": "rs_fgm3",
    "3PA": "rs_fga3",
    "FTM": "rs_ftm",
    "FTA": "rs_fta",
    "FT%": "rs_ft_pct",
    "FTA Rate": "rs_ft_rate",
    "ORB": "rs_orb",
    "AST": "rs_ast",
    "TOV": "rs_to",
    "STL": "rs_stl",
    "BLK": "rs_blk",
    "PF": "rs_pf",
    "BLKD": "rs_opp_blk",
    "Wins": "rs_win_pct",
}


def norm_abbrev_to_feature_col(abbrev: str) -> str:
    x = abbrev.strip().lower()
    x = re.sub(r"[^a-z0-9]+", "_", x)
    x = x.strip("_")
    return f"usp_{x}"


def load_feature_set(path: Path) -> list[str]:
    return pd.read_csv(path)["feature_name"].astype(str).tolist()


def build_team_game_index(detailed_results: pd.DataFrame, seasons: set[int]) -> dict[tuple[int, int], pd.DataFrame]:
    det = detailed_results[detailed_results["Season"].isin(seasons)].copy()

    winner_rows = pd.DataFrame(
        {
            "season": det["Season"],
            "day_num": det["DayNum"],
            "team_id": det["WTeamID"],
            "opp_id": det["LTeamID"],
            "pts": det["WScore"],
            "opp_pts": det["LScore"],
            "fgm": det["WFGM"],
            "fga": det["WFGA"],
            "fgm3": det["WFGM3"],
            "fga3": det["WFGA3"],
            "ftm": det["WFTM"],
            "fta": det["WFTA"],
            "orb": det["WOR"],
            "drb": det["WDR"],
            "ast": det["WAst"],
            "to": det["WTO"],
            "stl": det["WStl"],
            "blk": det["WBlk"],
            "pf": det["WPF"],
            "opp_fgm": det["LFGM"],
            "opp_fga": det["LFGA"],
            "opp_fgm3": det["LFGM3"],
            "opp_fga3": det["LFGA3"],
            "opp_ftm": det["LFTM"],
            "opp_fta": det["LFTA"],
            "opp_orb": det["LOR"],
            "opp_drb": det["LDR"],
            "opp_ast": det["LAst"],
            "opp_to": det["LTO"],
            "opp_stl": det["LStl"],
            "opp_blk": det["LBlk"],
            "opp_pf": det["LPF"],
            "num_ot": det["NumOT"],
            "win": 1,
        }
    )

    loser_rows = pd.DataFrame(
        {
            "season": det["Season"],
            "day_num": det["DayNum"],
            "team_id": det["LTeamID"],
            "opp_id": det["WTeamID"],
            "pts": det["LScore"],
            "opp_pts": det["WScore"],
            "fgm": det["LFGM"],
            "fga": det["LFGA"],
            "fgm3": det["LFGM3"],
            "fga3": det["LFGA3"],
            "ftm": det["LFTM"],
            "fta": det["LFTA"],
            "orb": det["LOR"],
            "drb": det["LDR"],
            "ast": det["LAst"],
            "to": det["LTO"],
            "stl": det["LStl"],
            "blk": det["LBlk"],
            "pf": det["LPF"],
            "opp_fgm": det["WFGM"],
            "opp_fga": det["WFGA"],
            "opp_fgm3": det["WFGM3"],
            "opp_fga3": det["WFGA3"],
            "opp_ftm": det["WFTM"],
            "opp_fta": det["WFTA"],
            "opp_orb": det["WOR"],
            "opp_drb": det["WDR"],
            "opp_ast": det["WAst"],
            "opp_to": det["WTO"],
            "opp_stl": det["WStl"],
            "opp_blk": det["WBlk"],
            "opp_pf": det["WPF"],
            "num_ot": det["NumOT"],
            "win": 0,
        }
    )

    all_games = pd.concat([winner_rows, loser_rows], ignore_index=True)
    all_games = all_games.sort_values(["season", "day_num", "team_id", "opp_id"]).reset_index(drop=True)

    all_games["fgm2"] = all_games["fgm"] - all_games["fgm3"]
    all_games["fga2"] = all_games["fga"] - all_games["fga3"]
    all_games["opp_fgm2"] = all_games["opp_fgm"] - all_games["opp_fgm3"]
    all_games["opp_fga2"] = all_games["opp_fga"] - all_games["opp_fga3"]
    all_games["trb"] = all_games["orb"] + all_games["drb"]
    all_games["opp_trb"] = all_games["opp_orb"] + all_games["opp_drb"]

    own_poss = all_games["fga"] - all_games["orb"] + all_games["to"] + 0.44 * all_games["fta"]
    opp_poss = all_games["opp_fga"] - all_games["opp_orb"] + all_games["opp_to"] + 0.44 * all_games["opp_fta"]
    all_games["poss_est"] = (own_poss + opp_poss) / 2.0
    all_games["poss_est_off"] = own_poss
    all_games["poss_est_def"] = opp_poss

    out: dict[tuple[int, int], pd.DataFrame] = {}
    for (season, team_id), grp in all_games.groupby(["season", "team_id"], sort=False):
        out[(int(season), int(team_id))] = grp.reset_index(drop=True)
    return out


def build_tournament_labels(master: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    labels = master[master["is_tourney_team"] == 1][["Season", "TeamID", "is_tourney_team", "tourney_seed_num"]].copy()

    last_games = results.sort_values(["Season", "DayNum"]).groupby("Season").tail(1)
    champion_map = dict(zip(last_games["Season"], last_games["WTeamID"]))

    w = results[["Season", "DayNum", "WTeamID"]].rename(columns={"WTeamID": "TeamID"})
    l = results[["Season", "DayNum", "LTeamID"]].rename(columns={"LTeamID": "TeamID"})
    long_games = pd.concat([w, l], ignore_index=True)
    max_day = long_games.groupby(["Season", "TeamID"])["DayNum"].max().reset_index(name="max_day")

    labels = labels.merge(max_day, on=["Season", "TeamID"], how="left")

    for flag, day in ROUND_DAY_THRESHOLDS.items():
        labels[flag] = (labels["max_day"] >= day).fillna(False).astype(int)

    labels["is_champion"] = labels.apply(
        lambda r: int(champion_map.get(r["Season"], -1) == r["TeamID"]), axis=1
    )

    labels.loc[labels["is_champion"] == 1, "reached_title_game"] = 1
    labels = labels.drop(columns=["max_day"])
    labels = labels.sort_values(["Season", "TeamID"]).reset_index(drop=True)
    return labels


def build_bracket_targets(results: pd.DataFrame) -> pd.DataFrame:
    a = results[["Season", "DayNum", "WTeamID", "LTeamID"]].rename(
        columns={"WTeamID": "TeamAID", "LTeamID": "TeamBID"}
    )
    b = results[["Season", "DayNum", "LTeamID", "WTeamID"]].rename(
        columns={"LTeamID": "TeamAID", "WTeamID": "TeamBID"}
    )
    a["target_teamA_win"] = 1
    b["target_teamA_win"] = 0
    out = pd.concat([a, b], ignore_index=True).sort_values(["Season", "DayNum", "TeamAID", "TeamBID"])
    return out.reset_index(drop=True)


def build_bracket_features(targets: pd.DataFrame, team_features: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    base_cols = list(dict.fromkeys(["tourney_seed_num"] + features))
    left = team_features[["Season", "TeamID"] + base_cols].copy()
    right = left.copy()

    left_cols = {c: f"A_{c}" for c in base_cols}
    right_cols = {c: f"B_{c}" for c in base_cols}

    out = targets.merge(
        left.rename(columns={"TeamID": "TeamAID", **left_cols}),
        on=["Season", "TeamAID"],
        how="left",
    ).merge(
        right.rename(columns={"TeamID": "TeamBID", **right_cols}),
        on=["Season", "TeamBID"],
        how="left",
    )

    out["TeamA_seed_num"] = out["A_tourney_seed_num"]
    out["TeamB_seed_num"] = out["B_tourney_seed_num"]
    out["seed_gap"] = out["TeamB_seed_num"] - out["TeamA_seed_num"]

    for f in features:
        out[f"delta_{f}"] = out[f"A_{f}"] - out[f"B_{f}"]

    keep = [
        "Season",
        "DayNum",
        "TeamAID",
        "TeamBID",
        "target_teamA_win",
        "TeamA_seed_num",
        "TeamB_seed_num",
        "seed_gap",
    ]
    keep += [f"delta_{f}" for f in features]
    return out[keep]


def build_champion_historical(team_features: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    out = team_features.merge(labels, on=["Season", "TeamID", "is_tourney_team", "tourney_seed_num"], how="inner")
    out = out[out["is_tourney_team"] == 1].copy()
    out = out.sort_values(["Season", "TeamID"]).reset_index(drop=True)
    return out


def safe_get_stat(abbrev: str, data_source: str, team_games_df: pd.DataFrame | None, kenpom_row: dict[str, object]) -> float | None:
    try:
        if "kenpom" in data_source and "box_score" not in data_source:
            v = get_stat(abbrev, kenpom_row=kenpom_row)
        else:
            v = get_stat(abbrev, team_games_df=team_games_df, kenpom_row=kenpom_row)
        if v is None:
            return None
        if hasattr(v, "item"):
            try:
                return float(v.item())
            except Exception:
                return float(v)
        return float(v)
    except Exception:
        return None


def main() -> None:
    OUT_CONFIG.mkdir(parents=True, exist_ok=True)
    OUT_DATA.mkdir(parents=True, exist_ok=True)

    print("[1/7] Loading base tables...")
    hist_master = pd.read_csv(HIST_MASTER_PATH)
    cur_master = pd.read_csv(CUR_MASTER_PATH) if CUR_MASTER_PATH.exists() else hist_master.iloc[0:0].copy()
    # Keep prior file read for compatibility, but updated pipeline now starts from
    # the full historical master feature universe rather than locked core.
    _ = load_feature_set(LOCKED_CORE_PATH)
    master_base_features = [c for c in hist_master.columns if c not in ID_COLS]

    full_stats = pd.read_csv(FULL_STAT_TEAM_PATH)
    full_stats["Abbrev"] = full_stats["Abbrev"].astype(str).str.strip()
    full_stats["Data Source"] = full_stats["Data Source"].astype(str).str.strip()

    model_stats = full_stats[full_stats["Data Source"].str.contains("box_score|kenpom", case=False, regex=True)].copy()
    model_stats = model_stats.drop_duplicates(subset=["Abbrev"]).reset_index(drop=True)

    seasons = set(hist_master["Season"].dropna().astype(int).tolist())
    if len(cur_master):
        seasons.update(cur_master["Season"].dropna().astype(int).tolist())

    print("[2/7] Building team-game index from detailed results...")
    detailed = pd.read_csv(REG_DETAILED_RESULTS_PATH)
    team_games_index = build_team_game_index(detailed, seasons)

    print("[3/7] Identifying newly enabled stats (Michigan 2026 gate)...")
    michigan_team_id = 1276
    michigan_season = 2026
    mich_df = team_games_index.get((michigan_season, michigan_team_id), pd.DataFrame())
    mich_row = cur_master[(cur_master["Season"] == michigan_season) & (cur_master["TeamID"] == michigan_team_id)]
    kenpom_mich = mich_row.iloc[0].to_dict() if not mich_row.empty else {}

    enabled_missing_stats: list[str] = []
    stat_source_map: dict[str, str] = {}

    for _, row in model_stats.iterrows():
        abbrev = str(row["Abbrev"]).strip()
        source = str(row["Data Source"]).strip()
        stat_source_map[abbrev] = source

        if abbrev in MASTER_STAT_ALIAS_TO_FEATURE and MASTER_STAT_ALIAS_TO_FEATURE[abbrev] in master_base_features:
            continue

        value = safe_get_stat(abbrev, source, mich_df, kenpom_mich)
        if value is not None:
            enabled_missing_stats.append(abbrev)

    enabled_missing_stats = sorted(set(enabled_missing_stats))

    stat_map_rows = []
    used_new_cols: set[str] = set()
    for abbrev in enabled_missing_stats:
        feature_col = norm_abbrev_to_feature_col(abbrev)
        # Skip if this candidate duplicates an existing master feature name or
        # another newly-generated feature name.
        if feature_col in master_base_features or feature_col in used_new_cols:
            continue
        used_new_cols.add(feature_col)
        stat_map_rows.append(
            {
                "abbrev": abbrev,
                "feature_name": feature_col,
                "data_source": stat_source_map.get(abbrev, ""),
            }
        )
    stat_map_df = pd.DataFrame(stat_map_rows)

    print(f"  Newly enabled (and not in locked core map): {len(stat_map_df)} stats")

    print("[4/7] Computing added stat features for all team-seasons...")
    added_records: list[dict[str, object]] = []
    combined_master = pd.concat([hist_master, cur_master], ignore_index=True)
    combined_master = combined_master.drop_duplicates(subset=["Season", "TeamID"]).reset_index(drop=True)

    total_rows = len(combined_master)
    for i, row in enumerate(combined_master.itertuples(index=False), start=1):
        season = int(getattr(row, "Season"))
        team_id = int(getattr(row, "TeamID"))
        team_games = team_games_index.get((season, team_id))
        kenpom_row = row._asdict()

        rec: dict[str, object] = {"Season": season, "TeamID": team_id}

        for stat_row in stat_map_df.itertuples(index=False):
            abbrev = str(stat_row.abbrev)
            source = str(stat_row.data_source)
            feature_col = str(stat_row.feature_name)
            rec[feature_col] = safe_get_stat(abbrev, source, team_games, kenpom_row)

        added_records.append(rec)

        if i % 250 == 0 or i == total_rows:
            print(f"  computed {i}/{total_rows} team-seasons")

    added_df = pd.DataFrame(added_records)

    hist_updated = hist_master.merge(added_df, on=["Season", "TeamID"], how="left")
    cur_updated = cur_master.merge(added_df, on=["Season", "TeamID"], how="left") if len(cur_master) else cur_master.copy()

    hist_updated_path = OUT_DATA / "master_features_all_teams_historical_updated_core.csv"
    cur_updated_path = OUT_DATA / "master_features_all_teams_2026_updated_core.csv"
    hist_updated.to_csv(hist_updated_path, index=False)
    cur_updated.to_csv(cur_updated_path, index=False)

    print("[5/7] Writing updated feature-set config...")
    new_feature_names = stat_map_df["feature_name"].tolist()
    updated_feature_list = list(dict.fromkeys(master_base_features + new_feature_names))

    updated_feature_set_df = pd.DataFrame(
        {
            "set_name": ["updated_core"] * len(updated_feature_list),
            "feature_name": updated_feature_list,
        }
    )
    updated_feature_set_path = OUT_CONFIG / "locked_feature_set_updated_core.csv"
    updated_feature_set_df.to_csv(updated_feature_set_path, index=False)

    stat_map_path = OUT_CONFIG / "updated_core_added_stat_mapping.csv"
    stat_map_df.to_csv(stat_map_path, index=False)

    print("[6/7] Building model-ready historical tables (updated_core)...")
    historical_seasons = sorted(hist_updated["Season"].dropna().astype(int).unique().tolist())

    tourney_results = pd.read_csv(TOURNEY_COMPACT_RESULTS_PATH)
    tourney_results = tourney_results[tourney_results["Season"].isin(historical_seasons)].copy()

    labels = build_tournament_labels(hist_updated, tourney_results)
    labels_path = OUT_DATA / "tournament_team_labels_historical_updated_core.csv"
    labels.to_csv(labels_path, index=False)

    team_feature_cols = list(dict.fromkeys(ID_COLS + updated_feature_list))
    team_features = hist_updated[team_feature_cols].copy()
    team_features_path = OUT_DATA / "team_season_features_updated_core_historical.csv"
    team_features.to_csv(team_features_path, index=False)

    bracket_targets = build_bracket_targets(tourney_results)
    bracket_hist = build_bracket_features(bracket_targets, team_features, updated_feature_list)
    bracket_hist_path = OUT_DATA / "bracket_games_updated_core_historical.csv"
    bracket_hist.to_csv(bracket_hist_path, index=False)

    champion_hist = build_champion_historical(team_features, labels)
    champion_hist_path = OUT_DATA / "champion_updated_core_historical.csv"
    champion_hist.to_csv(champion_hist_path, index=False)

    print("[7/7] Writing build summary...")
    summary = pd.DataFrame(
        [
            {"item": "build_timestamp_utc", "value": utc_now_iso()},
            {"item": "enabled_missing_stats_count", "value": len(stat_map_df)},
            {"item": "original_master_feature_count", "value": len(master_base_features)},
            {"item": "updated_core_feature_count", "value": len(updated_feature_list)},
            {"item": "historical_team_season_rows", "value": len(hist_updated)},
            {"item": "historical_bracket_rows", "value": len(bracket_hist)},
            {"item": "historical_champion_rows", "value": len(champion_hist)},
        ]
    )
    summary_path = OUT_DATA / "pipeline_build_summary.csv"
    summary.to_csv(summary_path, index=False)

    print("Build complete.")
    print(f"  {hist_updated_path}")
    print(f"  {cur_updated_path}")
    print(f"  {updated_feature_set_path}")
    print(f"  {stat_map_path}")
    print(f"  {bracket_hist_path}")
    print(f"  {champion_hist_path}")
    print(f"  {summary_path}")


if __name__ == "__main__":
    main()
