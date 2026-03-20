from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MODEL_READY_DIR = ROOT / "Good_Data" / "Model Ready Data"
SHARED_DIR = MODEL_READY_DIR / "Shared"
BRACKET_DIR = MODEL_READY_DIR / "Bracket Model"
CHAMPION_DIR = MODEL_READY_DIR / "Champion Model"
MANIFEST_DIR = MODEL_READY_DIR / "Manifests"

HISTORICAL_MASTER_PATH = ROOT / "Good_Data" / "Master Data" / "Master CSV File and Support Files" / "master_features_all_teams_historical.csv"
CURRENT_MASTER_PATH = ROOT / "Good_Data" / "Master Data" / "Master CSV File and Support Files" / "master_features_all_teams_2026.csv"
LOCKED_DIR = ROOT / "Good_Data" / "Master Data" / "Pruned Feature Sets (Gold)"
KAGGLE_DIR = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"

SEEDS_PATH = KAGGLE_DIR / "MNCAATourneySeeds.csv"
SLOTS_PATH = KAGGLE_DIR / "MNCAATourneySlots.csv"
RESULTS_PATH = KAGGLE_DIR / "MNCAATourneyCompactResults.csv"

CORE_SET_PATH = LOCKED_DIR / "locked_feature_set_core.csv"
EXT_SET_PATH = LOCKED_DIR / "locked_feature_set_extended.csv"
EXP_SET_PATH = LOCKED_DIR / "locked_feature_set_experimental.csv"

CURRENT_SEASON = 2026
ROUND_DAY_THRESHOLDS = {
    "reached_sweet16": 143,
    "reached_elite8": 145,
    "reached_final4": 152,
    "reached_title_game": 154,
}

ID_COLS = ["Season", "TeamID", "TeamName", "ConfAbbrev", "is_tourney_team", "tourney_seed_num"]


def ensure_dirs() -> None:
    for d in [SHARED_DIR, BRACKET_DIR, CHAMPION_DIR, MANIFEST_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def load_feature_set(path: Path) -> list[str]:
    df = pd.read_csv(path)
    return df["feature_name"].tolist()


def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def key_qa(df: pd.DataFrame, keys: list[str]) -> str:
    if not set(keys).issubset(df.columns):
        return "missing_key_columns"
    if len(df) == 0:
        return "ok_empty"
    if df[keys].isnull().any(axis=1).any():
        return "null_keys"
    if df.duplicated(subset=keys).any():
        return "duplicate_keys"
    return "ok"


def build_shared(
    historical_master: pd.DataFrame,
    current_master: pd.DataFrame,
    feature_sets: dict[str, list[str]],
) -> tuple[dict[str, pd.DataFrame], list[dict]]:
    outputs = {}
    manifest = []

    for set_name, features in feature_sets.items():
        cols = ID_COLS + features
        cols = list(dict.fromkeys(cols))

        hist = historical_master[cols].copy()
        cur = current_master[cols].copy() if len(current_master) else historical_master.iloc[0:0][cols].copy()

        hist_name = f"team_season_features_{set_name}_historical.csv"
        cur_name = f"team_season_features_{set_name}_{CURRENT_SEASON}.csv"

        hist_path = SHARED_DIR / hist_name
        cur_path = SHARED_DIR / cur_name

        save_csv(hist, hist_path)
        save_csv(cur, cur_path)

        outputs[f"shared_{set_name}_hist"] = hist
        outputs[f"shared_{set_name}_cur"] = cur

        manifest.append(
            {
                "sheet_name": hist_name,
                "model_family": "shared",
                "feature_set": set_name,
                "key_columns": "Season|TeamID",
                "target_columns": "",
                "season_scope": "historical",
            }
        )
        manifest.append(
            {
                "sheet_name": cur_name,
                "model_family": "shared",
                "feature_set": set_name,
                "key_columns": "Season|TeamID",
                "target_columns": "",
                "season_scope": str(CURRENT_SEASON),
            }
        )

    return outputs, manifest


def build_tournament_labels(master: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    # Restrict to tournament teams for historical seasons in master.
    labels = master[master["is_tourney_team"] == 1][["Season", "TeamID", "is_tourney_team", "tourney_seed_num"]].copy()

    # Champion by season is the winner of the latest day game.
    last_games = results.sort_values(["Season", "DayNum"]).groupby("Season").tail(1)
    champion_map = dict(zip(last_games["Season"], last_games["WTeamID"]))

    w = results[["Season", "DayNum", "WTeamID"]].rename(columns={"WTeamID": "TeamID"})
    l = results[["Season", "DayNum", "LTeamID"]].rename(columns={"LTeamID": "TeamID"})
    long_games = pd.concat([w, l], ignore_index=True)
    max_day = long_games.groupby(["Season", "TeamID"]) ["DayNum"].max().reset_index(name="max_day")

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

    keep = ["Season", "DayNum", "TeamAID", "TeamBID", "target_teamA_win", "TeamA_seed_num", "TeamB_seed_num", "seed_gap"]
    keep += [f"delta_{f}" for f in features]
    out = out[keep]
    return out


def empty_bracket_current(features: list[str]) -> pd.DataFrame:
    cols = ["Season", "Slot", "TeamAID", "TeamBID", "TeamA_seed_num", "TeamB_seed_num", "seed_gap"]
    cols += [f"delta_{f}" for f in features]
    out = pd.DataFrame(columns=cols)
    out["Season"] = pd.Series(dtype="int64")
    return out


def build_bracket_current_2026(
    seeds_df: pd.DataFrame,
    slots_df: pd.DataFrame,
    current_master: pd.DataFrame,
    features: list[str],
) -> pd.DataFrame:
    """
    Build pre-tournament bracket matchup pairs for the current season.

    Resolves every slot where BOTH StrongSeed and WeakSeed are direct team
    assignments (e.g. W01, X11a, Y16b) rather than prior-round winner
    references (e.g. R1W1, R2X3).  This covers all 4 play-in games and all
    32 Round-1 games whose play-in side is also a direct seed reference in
    MNCAATourneySeeds.csv (which Kaggle includes as separate 'a'/'b' entries).

    Falls back to empty_bracket_current() when 2026 seeds/slots are absent,
    so the script is safe to run before Selection Sunday.
    """
    s26 = seeds_df[seeds_df["Season"] == CURRENT_SEASON].copy()
    sl26 = slots_df[slots_df["Season"] == CURRENT_SEASON].copy()

    if len(s26) == 0 or len(sl26) == 0:
        return empty_bracket_current(features)

    # seed string (e.g. "W01", "X11a") → TeamID
    seed_to_team: dict[str, int] = dict(
        zip(s26["Seed"].astype(str), s26["TeamID"].astype(int))
    )

    def _is_slot_ref(s: str) -> bool:
        """True for prior-round winner refs like R1W1, R2X3, R5YZ, R6CH."""
        return len(s) >= 2 and s[0] == "R" and s[1].isdigit()

    team_index = current_master.set_index("TeamID")

    def _make_row(slot: str, ta_id: int, tb_id: int) -> dict | None:
        if ta_id not in team_index.index or tb_id not in team_index.index:
            return None
        ta = team_index.loc[ta_id]
        tb = team_index.loc[tb_id]
        seed_a = ta["tourney_seed_num"] if "tourney_seed_num" in ta.index else np.nan
        seed_b = tb["tourney_seed_num"] if "tourney_seed_num" in tb.index else np.nan
        row: dict = {
            "Season": CURRENT_SEASON,
            "Slot": slot,
            "TeamAID": ta_id,
            "TeamBID": tb_id,
            "TeamA_seed_num": seed_a,
            "TeamB_seed_num": seed_b,
            "seed_gap": (seed_b - seed_a) if (pd.notna(seed_a) and pd.notna(seed_b)) else np.nan,
        }
        for f in features:
            av = ta[f] if f in ta.index else np.nan
            bv = tb[f] if f in tb.index else np.nan
            row[f"delta_{f}"] = av - bv
        return row

    rows = []
    for _, sl_row in sl26.iterrows():
        slot = str(sl_row["Slot"])
        ss = str(sl_row["StrongSeed"])
        ws = str(sl_row["WeakSeed"])

        # Skip slots where either side is a prior-round winner (R2+ games)
        if _is_slot_ref(ss) or _is_slot_ref(ws):
            continue

        ta_id = seed_to_team.get(ss)
        tb_id = seed_to_team.get(ws)
        if ta_id is None or tb_id is None:
            continue

        row = _make_row(slot, ta_id, tb_id)
        if row:
            rows.append(row)

    if not rows:
        return empty_bracket_current(features)

    keep = (
        ["Season", "Slot", "TeamAID", "TeamBID", "TeamA_seed_num", "TeamB_seed_num", "seed_gap"]
        + [f"delta_{f}" for f in features]
    )
    return pd.DataFrame(rows)[keep].reset_index(drop=True)


def build_champion_historical(team_features: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    out = team_features.merge(labels, on=["Season", "TeamID", "is_tourney_team", "tourney_seed_num"], how="inner")
    out = out[out["is_tourney_team"] == 1].copy()
    out = out.sort_values(["Season", "TeamID"]).reset_index(drop=True)
    return out


def build_champion_current(team_features_current: pd.DataFrame) -> pd.DataFrame:
    out = team_features_current[team_features_current["is_tourney_team"] == 1].copy()
    out = out.sort_values(["Season", "TeamID"]).reset_index(drop=True)
    return out


def main() -> None:
    ensure_dirs()

    historical_master = pd.read_csv(HISTORICAL_MASTER_PATH)
    if CURRENT_MASTER_PATH.exists():
        current_master = pd.read_csv(CURRENT_MASTER_PATH)
    else:
        current_master = historical_master.iloc[0:0].copy()

    historical_seasons = sorted(historical_master["Season"].dropna().astype(int).unique().tolist())

    results = pd.read_csv(RESULTS_PATH)
    results = results[results["Season"].isin(historical_seasons)].copy()
    _seeds = pd.read_csv(SEEDS_PATH)
    _slots = pd.read_csv(SLOTS_PATH)

    core = load_feature_set(CORE_SET_PATH)
    extended = load_feature_set(EXT_SET_PATH)
    experimental = load_feature_set(EXP_SET_PATH)
    feature_sets = {
        "core": core,
        "extended": extended,
        "experimental": experimental,
    }

    schema_rows = []
    build_rows = []

    # Shared features
    shared_outputs, shared_schema = build_shared(historical_master, current_master, feature_sets)
    schema_rows.extend(shared_schema)

    for name, df in shared_outputs.items():
        if name.endswith("_hist"):
            file_name = f"team_season_features_{name.split('_')[1]}_historical.csv"
        else:
            file_name = f"team_season_features_{name.split('_')[1]}_{CURRENT_SEASON}.csv"
        build_rows.append(
            {
                "run_timestamp": utc_now_iso(),
                "source_master_rows": len(historical_master),
                "source_locked_sets": "core|extended|experimental",
                "output_sheet": file_name,
                "output_rows": len(df),
                "output_columns": len(df.columns),
                "qa_status": key_qa(df, ["Season", "TeamID"]),
            }
        )

    # Labels
    labels = build_tournament_labels(historical_master, results)
    labels_name = "tournament_team_labels_historical.csv"
    save_csv(labels, SHARED_DIR / labels_name)
    schema_rows.append(
        {
            "sheet_name": labels_name,
            "model_family": "shared",
            "feature_set": "labels",
            "key_columns": "Season|TeamID",
            "target_columns": "reached_sweet16|reached_elite8|reached_final4|reached_title_game|is_champion",
            "season_scope": "historical",
        }
    )
    build_rows.append(
        {
            "run_timestamp": utc_now_iso(),
            "source_master_rows": len(historical_master),
            "source_locked_sets": "labels_from_results",
            "output_sheet": labels_name,
            "output_rows": len(labels),
            "output_columns": len(labels.columns),
            "qa_status": key_qa(labels, ["Season", "TeamID"]),
        }
    )

    # Bracket historical targets
    targets = build_bracket_targets(results)
    targets_name = "bracket_games_historical_targets.csv"
    save_csv(targets, BRACKET_DIR / targets_name)
    schema_rows.append(
        {
            "sheet_name": targets_name,
            "model_family": "bracket",
            "feature_set": "targets",
            "key_columns": "Season|DayNum|TeamAID|TeamBID",
            "target_columns": "target_teamA_win",
            "season_scope": "historical",
        }
    )
    build_rows.append(
        {
            "run_timestamp": utc_now_iso(),
            "source_master_rows": len(historical_master),
            "source_locked_sets": "targets_from_results",
            "output_sheet": targets_name,
            "output_rows": len(targets),
            "output_columns": len(targets.columns),
            "qa_status": key_qa(targets, ["Season", "DayNum", "TeamAID", "TeamBID"]),
        }
    )

    # Bracket feature sheets historical + 2026 placeholder
    for set_name, features in feature_sets.items():
        hist_team = shared_outputs[f"shared_{set_name}_hist"]

        hist_bracket = build_bracket_features(targets, hist_team, features)
        hist_name = f"bracket_games_{set_name}_historical.csv"
        save_csv(hist_bracket, BRACKET_DIR / hist_name)

        cur_bracket = build_bracket_current_2026(_seeds, _slots, current_master, features)
        cur_name = f"bracket_games_{set_name}_{CURRENT_SEASON}.csv"
        save_csv(cur_bracket, BRACKET_DIR / cur_name)

        schema_rows.append(
            {
                "sheet_name": hist_name,
                "model_family": "bracket",
                "feature_set": set_name,
                "key_columns": "Season|DayNum|TeamAID|TeamBID",
                "target_columns": "target_teamA_win",
                "season_scope": "historical",
            }
        )
        schema_rows.append(
            {
                "sheet_name": cur_name,
                "model_family": "bracket",
                "feature_set": set_name,
                "key_columns": "Season|Slot|TeamAID|TeamBID",
                "target_columns": "",
                "season_scope": str(CURRENT_SEASON),
            }
        )

        build_rows.append(
            {
                "run_timestamp": utc_now_iso(),
                "source_master_rows": len(historical_master),
                "source_locked_sets": set_name,
                "output_sheet": hist_name,
                "output_rows": len(hist_bracket),
                "output_columns": len(hist_bracket.columns),
                "qa_status": key_qa(hist_bracket, ["Season", "DayNum", "TeamAID", "TeamBID"]),
            }
        )
        build_rows.append(
            {
                "run_timestamp": utc_now_iso(),
                "source_master_rows": len(historical_master),
                "source_locked_sets": set_name,
                "output_sheet": cur_name,
                "output_rows": len(cur_bracket),
                "output_columns": len(cur_bracket.columns),
                "qa_status": key_qa(cur_bracket, ["Season", "Slot", "TeamAID", "TeamBID"]) if len(cur_bracket) > 0 else "ok_empty_pending_2026_bracket_release",
            }
        )

    # Bracket teams 2026 placeholder
    if len(current_master):
        bracket_teams_2026 = (
            current_master[current_master["is_tourney_team"] == 1][["Season", "TeamID", "tourney_seed_num", "TeamName"]]
            .rename(columns={"tourney_seed_num": "Seed"})
            .sort_values(["Season", "TeamID"])
            .reset_index(drop=True)
        )
    else:
        bracket_teams_2026 = pd.DataFrame(columns=["Season", "TeamID", "Seed", "TeamName"])
    bracket_teams_name = f"bracket_teams_{CURRENT_SEASON}.csv"
    save_csv(bracket_teams_2026, BRACKET_DIR / bracket_teams_name)

    schema_rows.append(
        {
            "sheet_name": bracket_teams_name,
            "model_family": "bracket",
            "feature_set": "participants",
            "key_columns": "Season|TeamID",
            "target_columns": "",
            "season_scope": str(CURRENT_SEASON),
        }
    )
    build_rows.append(
        {
            "run_timestamp": utc_now_iso(),
            "source_master_rows": len(historical_master),
            "source_locked_sets": "participants",
            "output_sheet": bracket_teams_name,
            "output_rows": len(bracket_teams_2026),
            "output_columns": len(bracket_teams_2026.columns),
            "qa_status": "ok_empty_pending_2026_seeds_release",
        }
    )

    # Champion sheets
    for set_name, _features in feature_sets.items():
        hist_team = shared_outputs[f"shared_{set_name}_hist"]
        cur_team = shared_outputs[f"shared_{set_name}_cur"]

        champ_hist = build_champion_historical(hist_team, labels)
        champ_hist_name = f"champion_{set_name}_historical.csv"
        save_csv(champ_hist, CHAMPION_DIR / champ_hist_name)

        champ_cur = build_champion_current(cur_team)
        champ_cur_name = f"champion_{set_name}_{CURRENT_SEASON}.csv"
        save_csv(champ_cur, CHAMPION_DIR / champ_cur_name)

        schema_rows.append(
            {
                "sheet_name": champ_hist_name,
                "model_family": "champion",
                "feature_set": set_name,
                "key_columns": "Season|TeamID",
                "target_columns": "is_champion|reached_sweet16|reached_elite8|reached_final4|reached_title_game",
                "season_scope": "historical",
            }
        )
        schema_rows.append(
            {
                "sheet_name": champ_cur_name,
                "model_family": "champion",
                "feature_set": set_name,
                "key_columns": "Season|TeamID",
                "target_columns": "",
                "season_scope": str(CURRENT_SEASON),
            }
        )

        build_rows.append(
            {
                "run_timestamp": utc_now_iso(),
                "source_master_rows": len(historical_master),
                "source_locked_sets": set_name,
                "output_sheet": champ_hist_name,
                "output_rows": len(champ_hist),
                "output_columns": len(champ_hist.columns),
                "qa_status": key_qa(champ_hist, ["Season", "TeamID"]),
            }
        )
        build_rows.append(
            {
                "run_timestamp": utc_now_iso(),
                "source_master_rows": len(historical_master),
                "source_locked_sets": set_name,
                "output_sheet": champ_cur_name,
                "output_rows": len(champ_cur),
                "output_columns": len(champ_cur.columns),
                "qa_status": "ok_empty_pending_2026_master_update" if len(champ_cur) == 0 else key_qa(champ_cur, ["Season", "TeamID"]),
            }
        )

    # Write manifests
    schema_manifest = pd.DataFrame(schema_rows).sort_values(["model_family", "sheet_name"]).reset_index(drop=True)
    build_manifest = pd.DataFrame(build_rows)

    save_csv(schema_manifest, MANIFEST_DIR / "schema_manifest.csv")
    save_csv(build_manifest, MANIFEST_DIR / "build_manifest.csv")

    print("Model-ready table build complete.")
    print(f"  Shared sheets:   {len(list(SHARED_DIR.glob('*.csv')))}")
    print(f"  Bracket sheets:  {len(list(BRACKET_DIR.glob('*.csv')))}")
    print(f"  Champion sheets: {len(list(CHAMPION_DIR.glob('*.csv')))}")
    print(f"  Manifests:       {len(list(MANIFEST_DIR.glob('*.csv')))}")


if __name__ == "__main__":
    main()

