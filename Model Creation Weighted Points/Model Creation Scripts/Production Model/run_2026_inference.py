"""
run_2026_inference.py

2026 tournament inference mode.

Trains both locked models on ALL available historical seasons (no test holdout),
then scores 2026 tournament matchups for the bracket and champion predictions.

Prerequisites — must all exist before running:
  1. master_features_all_teams_2026.csv built (run build_master_features_2026.py)
  2. MNCAATourneySeeds.csv has 2026 rows   ← available after Selection Sunday (March 15)
  3. MNCAATourneySlots.csv has 2026 rows   ← available after Selection Sunday
  4. build_model_ready_tables.py has been run  ← populates bracket/champion 2026 files

Outputs (written to Model Creation/Results/Production/):
  2026_bracket_predictions.csv   — all 63 predicted matchups with win probabilities
  2026_champion_predictions.csv  — all 64 tourney teams ranked by championship probability
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common_utils import (  # noqa: E402
    logistic_baseline_pipeline,
)

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "Model Creation Weighted Points" / "Config" / "final_model_lock_manifest_weighted_points.json"
KAGGLE        = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"
MODEL_READY   = ROOT / "Good_Data" / "Model Ready Data"
LOCKED_DIR    = ROOT / "Good_Data" / "Master Data" / "Pruned Feature Sets (Gold)"
HIST_MASTER   = ROOT / "Good_Data" / "Master Data" / "Master CSV File and Support Files" / "master_features_all_teams_historical.csv"
CURR_MASTER   = ROOT / "Good_Data" / "Master Data" / "Master CSV File and Support Files" / "master_features_all_teams_2026.csv"
OUT_DIR       = ROOT / "Model Creation Weighted Points" / "Results" / "Production"

LIVE_SEASON = 2026


def _train_seasons_for(target_season: int) -> List[int]:
    """All seasons available for training before the target season."""
    return [s for s in range(2003, target_season) if s != 2020]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_manifest() -> Dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_feature_set(name: str) -> List[str]:
    df = pd.read_csv(LOCKED_DIR / f"locked_feature_set_{name}.csv")
    return df["feature_name"].tolist()


def _base_estimator(model_family: str):
    if model_family == "logistic":
        return logistic_baseline_pipeline()
    if model_family == "rf":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=600,
                        max_depth=None,
                        min_samples_leaf=2,
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        )
    if model_family == "gbm":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    GradientBoostingClassifier(
                        n_estimators=500,
                        learning_rate=0.03,
                        max_depth=2,
                        random_state=42,
                    ),
                ),
            ]
        )
    if model_family == "xgb":
        try:
            from xgboost import XGBClassifier  # type: ignore
        except Exception as exc:
            raise ValueError("xgb model_family selected but xgboost is not installed") from exc
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    XGBClassifier(
                        n_estimators=700,
                        learning_rate=0.03,
                        max_depth=4,
                        subsample=0.9,
                        colsample_bytree=0.8,
                        objective="binary:logistic",
                        eval_metric="logloss",
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        )
    raise ValueError(f"Unsupported model_family: {model_family}")


def build_model(model_family: str, calibration: str):
    base = _base_estimator(model_family)
    if calibration == "raw":
        return base
    if calibration in {"sigmoid", "isotonic"}:
        return CalibratedClassifierCV(estimator=base, method=calibration, cv=3)
    raise ValueError(f"Unsupported calibration: {calibration}")


def bracket_X_cols(df: pd.DataFrame) -> List[str]:
    """Feature columns for the bracket model derived from a training DataFrame."""
    exclude = {"Season", "DayNum", "Slot", "TeamAID", "TeamBID", "target_teamA_win"}
    return [c for c in df.columns if c not in exclude]


def champion_X_cols(df: pd.DataFrame) -> List[str]:
    """Feature columns for the champion model derived from a training DataFrame."""
    exclude = {
        "Season", "TeamID", "TeamName", "ConfAbbrev",
        "is_tourney_team",
        "is_champion", "reached_sweet16", "reached_elite8",
        "reached_final4", "reached_title_game",
    }
    return [c for c in df.columns if c not in exclude]


def _is_slot_ref(s: str) -> bool:
    """True for prior-round winner refs like R1W1, R2X3, R5YZ, R6CH."""
    return len(s) >= 2 and s[0] == "R" and s[1].isdigit()


def _slot_round(slot: str) -> int:
    """Return the round number for a slot name (R1→1, R2→2, …, R6→6, other→0)."""
    for r in range(1, 7):
        if slot.startswith(f"R{r}"):
            return r
    return 0  # play-in or unrecognised


# ─────────────────────────────────────────────────────────────────────────────
# Bracket inference
# ─────────────────────────────────────────────────────────────────────────────

def _build_matchup_row(
    slot: str,
    ta_id: int,
    tb_id: int,
    team_index: pd.DataFrame,
    core_features: List[str],
    x_cols: List[str],
    target_season: int,
) -> pd.DataFrame | None:
    """
    Build a single-row DataFrame of bracket model features for (ta_id, tb_id).
    Returns None if either team is missing from the feature index.
    """
    if ta_id not in team_index.index or tb_id not in team_index.index:
        return None
    ta = team_index.loc[ta_id]
    tb = team_index.loc[tb_id]

    seed_a = ta.get("tourney_seed_num", np.nan)
    seed_b = tb.get("tourney_seed_num", np.nan)

    row: Dict = {
        "Season": target_season,
        "Slot": slot,
        "TeamAID": ta_id,
        "TeamBID": tb_id,
        "TeamA_seed_num": seed_a,
        "TeamB_seed_num": seed_b,
        "seed_gap": (seed_b - seed_a) if (pd.notna(seed_a) and pd.notna(seed_b)) else np.nan,
    }
    for f in core_features:
        av = ta[f] if f in ta.index else np.nan
        bv = tb[f] if f in tb.index else np.nan
        row[f"delta_{f}"] = av - bv

    df_row = pd.DataFrame([row])
    # Align to exact training column order; fill any gaps with NaN
    missing = [c for c in x_cols if c not in df_row.columns]
    for c in missing:
        df_row[c] = np.nan
    return df_row[x_cols]


def run_bracket_inference(
    manifest: Dict,
    team_features: pd.DataFrame,           # team features for target season
    bracket_readiness_check: pd.DataFrame, # pre-built file used only for readiness gate
    slots: pd.DataFrame,                   # MNCAATourneySlots for target season
    seeds: pd.DataFrame,                   # MNCAATourneySeeds for target season
    core_features: List[str],
    target_season: int,
    train_seasons: List[int],
    actual_playin_results: pd.DataFrame,   # MNCAATourneyCompactResults rows for play-in games
) -> pd.DataFrame:
    """
    Train the bracket model on historical seasons, then simulate the tournament
    starting from the Round of 64 using ONLY model-predicted winners.

    Play-in winners are resolved from actual_playin_results (real outcomes),
    not model predictions — the model's job begins at the Round of 64.

    Every subsequent round is driven exclusively by the model's own prior-round
    predictions.  The slot_winner dict is seeded with:
      - direct seed assignments (e.g. W01 → TeamID)
      - actual play-in winners (e.g. W16 → winner of W16a vs W16b)
    Then all Round of 64 through Championship slots are simulated in order,
    with each game's predicted winner written back to slot_winner so downstream
    rounds resolve correctly.
    """
    cfg = manifest["models"]["bracket"]
    hist_path = ROOT / str(cfg["dataset_relpath"])
    df_hist = pd.read_csv(hist_path)

    df_train = df_hist[df_hist["Season"].isin(train_seasons)].copy()
    x_cols   = bracket_X_cols(df_hist)

    print(f"  Bracket model: training on {len(df_train)} games "
          f"({df_train['Season'].nunique()} seasons), {len(x_cols)} features")

    model = build_model(str(cfg.get("model_family", "logistic")), str(cfg["calibration"]))
    model.fit(df_train[x_cols], df_train["target_teamA_win"].astype(int).values)

    if len(bracket_readiness_check) == 0 and len(seeds) == 0:
        print(f"  WARNING: No {target_season} bracket data found — skipping bracket inference.")
        return pd.DataFrame()

    # ── Resolution table ──────────────────────────────────────────────────────
    seed_to_team: Dict[str, int] = dict(
        zip(seeds["Seed"].astype(str), seeds["TeamID"].astype(int))
    )
    slot_winner: Dict[str, int] = dict(seed_to_team)

    team_index = team_features.set_index("TeamID")

    # ── Sort all slots by round ───────────────────────────────────────────────
    all_slots = slots.copy()
    all_slots["_round"] = all_slots["Slot"].apply(_slot_round)
    all_slots = all_slots.sort_values(["_round", "Slot"]).reset_index(drop=True)

    # ── Resolve play-in winners from ACTUAL results (round 0) ────────────────
    # The model does not predict play-in games; actual results are used so that
    # the correct 64 teams are seeded into the Round of 64 simulation.
    playin_slots = all_slots[all_slots["_round"] == 0]
    for _, sl_row in playin_slots.iterrows():
        slot = str(sl_row["Slot"])
        ta_id = slot_winner.get(str(sl_row["StrongSeed"]))
        tb_id = slot_winner.get(str(sl_row["WeakSeed"]))
        if ta_id is None or tb_id is None:
            continue
        match = actual_playin_results[
            ((actual_playin_results["WTeamID"] == ta_id) & (actual_playin_results["LTeamID"] == tb_id)) |
            ((actual_playin_results["WTeamID"] == tb_id) & (actual_playin_results["LTeamID"] == ta_id))
        ]
        if len(match) > 0:
            slot_winner[slot] = int(match.iloc[0]["WTeamID"])
        # If actual result not yet available, leave slot unresolved —
        # the R1 game depending on it will be skipped gracefully.

    # ── Model simulation: Round of 64 onward (skip round 0) ──────────────────
    main_slots = all_slots[all_slots["_round"] > 0]
    all_rows = []
    for _, sl_row in main_slots.iterrows():
        slot = str(sl_row["Slot"])
        ss   = str(sl_row["StrongSeed"])
        ws   = str(sl_row["WeakSeed"])

        # Resolve both participants from slot_winner.
        # For direct-seed slots (e.g. R1W1 with W01 vs W16) this finds the team
        # assigned to "W01" and the model-predicted winner of the "W16" play-in.
        # For later-round slots (e.g. R2W1 with R1W1 vs R1W8) this finds the
        # model-predicted winners of those R1 games.
        ta_id = slot_winner.get(ss)
        tb_id = slot_winner.get(ws)
        if ta_id is None or tb_id is None:
            # Dependency unresolvable — malformed slot data; skip silently.
            continue

        X_row = _build_matchup_row(slot, ta_id, tb_id, team_index, core_features, x_cols, target_season)
        if X_row is None:
            # Team missing from 2026 feature index; advance strong-seed team.
            slot_winner[slot] = ta_id
            continue

        p      = float(model.predict_proba(X_row)[0, 1])
        winner = ta_id if p >= 0.5 else tb_id

        # Record predicted winner so downstream slots can resolve against this slot.
        slot_winner[slot] = winner

        ta_seed = team_index.loc[ta_id, "tourney_seed_num"] if ta_id in team_index.index else np.nan
        tb_seed = team_index.loc[tb_id, "tourney_seed_num"] if tb_id in team_index.index else np.nan

        all_rows.append({
            "Season":           target_season,
            "Slot":             slot,
            "Round":            _slot_round(slot),
            "TeamAID":          ta_id,
            "TeamBID":          tb_id,
            "TeamA_seed_num":   ta_seed,
            "TeamB_seed_num":   tb_seed,
            "seed_gap":         (tb_seed - ta_seed) if (pd.notna(ta_seed) and pd.notna(tb_seed)) else np.nan,
            "p_teamA_win":      round(p, 6),
            "predicted_winner": winner,
        })

    preds = pd.DataFrame(all_rows).sort_values(["Round", "Slot"]).reset_index(drop=True)

    # Join team names for readability
    teams = pd.read_csv(KAGGLE / "MTeams.csv")[["TeamID", "TeamName"]]
    id_to_name = dict(zip(teams["TeamID"], teams["TeamName"]))
    preds["TeamA_name"]   = preds["TeamAID"].map(id_to_name)
    preds["TeamB_name"]   = preds["TeamBID"].map(id_to_name)
    preds["Winner_name"]  = preds["predicted_winner"].map(id_to_name)

    return preds


# ─────────────────────────────────────────────────────────────────────────────
# Champion inference
# ─────────────────────────────────────────────────────────────────────────────

def run_champion_inference(
    manifest: Dict,
    champion_cur: pd.DataFrame,
    train_seasons: List[int],
) -> pd.DataFrame:
    """
    Train champion model on the given training seasons, then score every
    tourney team in champion_cur for their probability of winning the championship.
    """
    cfg = manifest["models"]["champion"]
    hist_path = ROOT / str(cfg["dataset_relpath"])
    df_hist = pd.read_csv(hist_path)

    df_train = df_hist[df_hist["Season"].isin(train_seasons)].copy()
    x_cols   = champion_X_cols(df_hist)

    print(f"  Champion model: training on {len(df_train)} team-seasons "
          f"({df_train['Season'].nunique()} seasons), {len(x_cols)} features")

    model = build_model(str(cfg.get("model_family", "logistic")), str(cfg["calibration"]))
    model.fit(df_train[x_cols], df_train["is_champion"].astype(int).values)

    if len(champion_cur) == 0:
        print("  WARNING: No champion candidate data found — skipping champion inference.")
        return pd.DataFrame()

    # Align to training feature columns (label cols won't exist for live seasons)
    candidate = champion_cur.copy()
    for c in x_cols:
        if c not in candidate.columns:
            candidate[c] = np.nan

    p_champ = model.predict_proba(candidate[x_cols])[:, 1]

    preds = candidate[["Season", "TeamID", "TeamName", "tourney_seed_num"]].copy()
    preds["p_champion"] = p_champ.round(6)
    preds["rank"]       = preds["p_champion"].rank(method="first", ascending=False).astype(int)
    preds = preds.sort_values("rank").reset_index(drop=True)

    return preds


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run bracket and champion inference for a given season."
    )
    p.add_argument(
        "--season", type=int, default=LIVE_SEASON,
        help=f"Season to predict (default: {LIVE_SEASON}). "
             "Pass a historical season (e.g. 2025) to validate the simulation."
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    target_season = args.season
    train_seasons = _train_seasons_for(target_season)
    is_live       = (target_season == LIVE_SEASON)

    manifest      = load_manifest()
    core_features = load_feature_set("core")
    feat_set      = manifest["models"]["bracket"]["feature_set"]  # "core"

    bracket_dir  = MODEL_READY / "Bracket Model"
    champion_dir = MODEL_READY / "Champion Model"
    shared_dir   = MODEL_READY / "Shared"

    seeds_df = pd.read_csv(KAGGLE / "MNCAATourneySeeds.csv")
    slots_df = pd.read_csv(KAGGLE / "MNCAATourneySlots.csv")
    seeds_season = seeds_df[seeds_df["Season"] == target_season].copy()
    slots_season = slots_df[slots_df["Season"] == target_season].copy()

    if is_live:
        # Live 2026 run — read from pre-built model-ready files
        bracket_r1_path   = bracket_dir  / f"bracket_games_{feat_set}_{target_season}.csv"
        champion_cur_path = champion_dir / f"champion_{feat_set}_{target_season}.csv"
        team_feat_path    = shared_dir   / f"team_season_features_{feat_set}_{target_season}.csv"

        bracket_check  = pd.read_csv(bracket_r1_path)   if bracket_r1_path.exists()   else pd.DataFrame()
        champion_cur   = pd.read_csv(champion_cur_path)  if champion_cur_path.exists() else pd.DataFrame()
        team_features  = pd.read_csv(team_feat_path)     if team_feat_path.exists()    else pd.DataFrame()

        results_df   = pd.read_csv(KAGGLE / "MNCAATourneyCompactResults.csv")
        playin_results = results_df[
            (results_df["Season"] == target_season) & (results_df["DayNum"] < 136)
        ].copy()

        seeds_ready  = len(seeds_season) > 0
        slots_ready  = len(slots_season) > 0
        playin_ready = len(playin_results) > 0
        r1_ready     = len(bracket_check) > 0
        champ_ready  = len(champion_cur) > 0

        print("=" * 60)
        print(f"{target_season} INFERENCE — PRE-RUN CHECK")
        print(f"  seeds in MNCAATourneySeeds  : {'YES (' + str(len(seeds_season)) + ' rows)' if seeds_ready else 'NO — run after Selection Sunday'}")
        print(f"  slots in MNCAATourneySlots  : {'YES (' + str(len(slots_season)) + ' rows)' if slots_ready else 'NO — run after Selection Sunday'}")
        print(f"  play-in results             : {'YES (' + str(len(playin_results)) + ' games)' if playin_ready else 'NO — run after First Four (Mar 18-19)'}")
        print(f"  bracket_games_core_{target_season}.csv : {'YES (' + str(len(bracket_check)) + ' matchups)' if r1_ready else 'EMPTY — run build_model_ready_tables.py'}")
        print(f"  champion_core_{target_season}.csv      : {'YES (' + str(len(champion_cur)) + ' teams)' if champ_ready else 'EMPTY — run build_model_ready_tables.py'}")
        print("=" * 60)

        if not (seeds_ready and slots_ready and playin_ready and r1_ready and champ_ready):
            print("\nOne or more prerequisites are missing.  See messages above.")
            print("Complete data collection, then re-run this script.")
            return
    else:
        # Historical validation run — build team features directly from historical master
        print("=" * 60)
        print(f"{target_season} HISTORICAL SIMULATION")
        print(f"  Training seasons : {train_seasons[0]}–{train_seasons[-1]} (excl. 2020)")
        print(f"  Seeds found      : {len(seeds_season)}")
        print(f"  Slots found      : {len(slots_season)}")
        print("=" * 60)

        if len(seeds_season) == 0 or len(slots_season) == 0:
            print(f"\nNo seeds/slots for Season={target_season} in base data files.")
            return

        hist_master  = pd.read_csv(HIST_MASTER)
        team_features = hist_master[hist_master["Season"] == target_season].copy()
        if len(team_features) == 0:
            print(f"\nNo rows for Season={target_season} in historical master.")
            return

        # Build champion candidate set: tourney teams from historical master
        champion_cur = team_features[team_features["is_tourney_team"] == 1].copy()
        # Readiness check placeholder — just needs to be non-empty to pass the gate
        bracket_check = seeds_season

        results_df   = pd.read_csv(KAGGLE / "MNCAATourneyCompactResults.csv")
        playin_results = results_df[
            (results_df["Season"] == target_season) & (results_df["DayNum"] < 136)
        ].copy()
        print(f"  Play-in results  : {len(playin_results)} games resolved from actual data")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Bracket ──────────────────────────────────────────────────────────────
    print("\n[Bracket Model]")
    bracket_preds = run_bracket_inference(
        manifest, team_features, bracket_check, slots_season, seeds_season,
        core_features, target_season, train_seasons, playin_results
    )

    if len(bracket_preds) > 0:
        out_brk = OUT_DIR / f"{target_season}_bracket_predictions_weighted_points.csv"
        bracket_preds.to_csv(out_brk, index=False)
        print(f"  Saved: {out_brk}")
        print()
        print("  PREDICTED BRACKET RESULTS:")
        round_names = {0: "Play-In", 1: "Round of 64", 2: "Round of 32",
                       3: "Sweet 16", 4: "Elite 8", 5: "Final Four", 6: "Championship"}
        for rnd in sorted(bracket_preds["Round"].unique()):
            rnd_df = bracket_preds[bracket_preds["Round"] == rnd]
            print(f"\n  --- {round_names.get(rnd, f'Round {rnd}')} ---")
            for _, row in rnd_df.iterrows():
                conf   = f"({row['p_teamA_win']:.0%})" if row['predicted_winner'] == row['TeamAID'] else f"({1-row['p_teamA_win']:.0%})"
                winner = row['Winner_name']
                loser  = row['TeamB_name'] if row['predicted_winner'] == row['TeamAID'] else row['TeamA_name']
                seed_a = f"({int(row['TeamA_seed_num'])})" if pd.notna(row.get('TeamA_seed_num')) else ""
                seed_b = f"({int(row['TeamB_seed_num'])})" if pd.notna(row.get('TeamB_seed_num')) else ""
                w_seed = seed_a if row['predicted_winner'] == row['TeamAID'] else seed_b
                l_seed = seed_b if row['predicted_winner'] == row['TeamAID'] else seed_a
                print(f"    [{row['Slot']:6s}]  {winner}{w_seed}  def.  {loser}{l_seed}  {conf}")

    # ── Champion ─────────────────────────────────────────────────────────────
    print("\n[Champion Model]")
    champion_preds = run_champion_inference(manifest, champion_cur, train_seasons)

    if len(champion_preds) > 0:
        out_chmp = OUT_DIR / f"{target_season}_champion_predictions_weighted_points.csv"
        champion_preds.to_csv(out_chmp, index=False)
        print(f"  Saved: {out_chmp}")
        print()
        print("  TOP 10 CHAMPIONSHIP PROBABILITY:")
        top10 = champion_preds.head(10)
        for _, row in top10.iterrows():
            seed_str = f"(#{int(row['tourney_seed_num'])})" if pd.notna(row['tourney_seed_num']) else ""
            print(f"    #{int(row['rank']):2d}  {row['TeamName']:30s} {seed_str:6s}  {row['p_champion']:.2%}")

    print("\nDone.")


if __name__ == "__main__":
    main()
