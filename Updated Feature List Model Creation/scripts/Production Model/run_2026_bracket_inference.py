from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "Updated Feature List Model Creation" / "config" / "final_model_lock_manifest_updated.json"
KAGGLE = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"
DATA_DIR = ROOT / "Updated Feature List Model Creation" / "data"
OUT_DIR = ROOT / "Updated Feature List Model Creation" / "results" / "Production"

LIVE_SEASON = 2026


def _train_seasons_for(target_season: int) -> List[int]:
    return [s for s in range(2003, target_season) if s != 2020]


def load_manifest() -> Dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def logistic_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(solver="lbfgs", max_iter=5000)),
        ]
    )


def build_model(calibration: str):
    base = logistic_pipeline()
    if calibration == "raw":
        return base
    if calibration in {"sigmoid", "isotonic"}:
        return CalibratedClassifierCV(estimator=base, method=calibration, cv=5)
    raise ValueError(f"Unsupported calibration: {calibration}")


def bracket_x_cols(df: pd.DataFrame) -> List[str]:
    exclude = {"Season", "DayNum", "Slot", "TeamAID", "TeamBID", "target_teamA_win"}
    return [c for c in df.columns if c not in exclude]


def _is_slot_ref(s: str) -> bool:
    return len(s) >= 2 and s[0] == "R" and s[1].isdigit()


def _slot_round(slot: str) -> int:
    for r in range(1, 7):
        if str(slot).startswith(f"R{r}"):
            return r
    return 0


def _build_matchup_row(
    slot: str,
    ta_id: int,
    tb_id: int,
    team_index: pd.DataFrame,
    feature_cols_for_delta: List[str],
    x_cols: List[str],
    target_season: int,
) -> pd.DataFrame | None:
    if ta_id not in team_index.index or tb_id not in team_index.index:
        return None

    ta = team_index.loc[ta_id]
    tb = team_index.loc[tb_id]

    seed_a = ta.get("tourney_seed_num", np.nan)
    seed_b = tb.get("tourney_seed_num", np.nan)

    row: Dict[str, object] = {
        "Season": target_season,
        "Slot": slot,
        "TeamAID": ta_id,
        "TeamBID": tb_id,
        "TeamA_seed_num": seed_a,
        "TeamB_seed_num": seed_b,
        "seed_gap": (seed_b - seed_a) if (pd.notna(seed_a) and pd.notna(seed_b)) else np.nan,
    }

    for f in feature_cols_for_delta:
        av = ta[f] if f in ta.index else np.nan
        bv = tb[f] if f in tb.index else np.nan
        row[f"delta_{f}"] = av - bv

    df_row = pd.DataFrame([row])
    for c in x_cols:
        if c not in df_row.columns:
            df_row[c] = np.nan
    return df_row[x_cols]


def run_bracket_inference(target_season: int) -> pd.DataFrame:
    manifest = load_manifest()
    cfg = manifest["models"]["bracket"]

    hist_path = ROOT / str(cfg["dataset_relpath"])
    df_hist = pd.read_csv(hist_path)

    train_seasons = _train_seasons_for(target_season)
    df_train = df_hist[df_hist["Season"].isin(train_seasons)].copy()
    x_cols = bracket_x_cols(df_hist)

    model = build_model(str(cfg["calibration"]))
    model.fit(df_train[x_cols], df_train[str(cfg["target_column"])].astype(int).values)

    team_features_path = DATA_DIR / f"master_features_all_teams_{target_season}_updated_core.csv"
    if not team_features_path.exists():
        raise FileNotFoundError(
            f"Missing updated team feature table for season {target_season}: {team_features_path}. "
            "Run Updated Feature List Model Creation/scripts/build_updated_pipeline.py first."
        )

    team_features = pd.read_csv(team_features_path)
    team_index = team_features.set_index("TeamID")

    seeds_df = pd.read_csv(KAGGLE / "MNCAATourneySeeds.csv")
    slots_df = pd.read_csv(KAGGLE / "MNCAATourneySlots.csv")
    results_df = pd.read_csv(KAGGLE / "MNCAATourneyCompactResults.csv")

    seeds = seeds_df[seeds_df["Season"] == target_season].copy()
    slots = slots_df[slots_df["Season"] == target_season].copy()
    playin_results = results_df[(results_df["Season"] == target_season) & (results_df["DayNum"] < 136)].copy()

    if len(seeds) == 0 or len(slots) == 0:
        raise ValueError(f"No seeds/slots found for season {target_season}.")

    # Infer base feature names from training columns that are expected to be delta_ features.
    feature_cols_for_delta = [c.replace("delta_", "", 1) for c in x_cols if c.startswith("delta_")]

    seed_to_team: Dict[str, int] = dict(zip(seeds["Seed"].astype(str), seeds["TeamID"].astype(int)))
    slot_winner: Dict[str, int] = dict(seed_to_team)

    all_slots = slots.copy()
    all_slots["Round"] = all_slots["Slot"].apply(_slot_round)
    all_slots = all_slots.sort_values(["Round", "Slot"]).reset_index(drop=True)

    # Resolve play-in winners from actual results.
    playin_slots = all_slots[all_slots["Round"] == 0]
    for _, sl_row in playin_slots.iterrows():
        slot = str(sl_row["Slot"])
        ta_id = slot_winner.get(str(sl_row["StrongSeed"]))
        tb_id = slot_winner.get(str(sl_row["WeakSeed"]))
        if ta_id is None or tb_id is None:
            continue

        match = playin_results[
            ((playin_results["WTeamID"] == ta_id) & (playin_results["LTeamID"] == tb_id))
            | ((playin_results["WTeamID"] == tb_id) & (playin_results["LTeamID"] == ta_id))
        ]
        if len(match) > 0:
            slot_winner[slot] = int(match.iloc[0]["WTeamID"])

    # Simulate rounds R1-R6 from model predictions.
    rows = []
    main_slots = all_slots[all_slots["Round"] > 0]
    for _, sl_row in main_slots.iterrows():
        slot = str(sl_row["Slot"])
        ss = str(sl_row["StrongSeed"])
        ws = str(sl_row["WeakSeed"])

        ta_id = slot_winner.get(ss)
        tb_id = slot_winner.get(ws)
        if ta_id is None or tb_id is None:
            continue

        x_row = _build_matchup_row(slot, ta_id, tb_id, team_index, feature_cols_for_delta, x_cols, target_season)
        if x_row is None:
            slot_winner[slot] = ta_id
            continue

        p = float(model.predict_proba(x_row)[0, 1])
        winner = ta_id if p >= 0.5 else tb_id
        slot_winner[slot] = winner

        ta_seed = team_index.loc[ta_id, "tourney_seed_num"] if ta_id in team_index.index else np.nan
        tb_seed = team_index.loc[tb_id, "tourney_seed_num"] if tb_id in team_index.index else np.nan

        rows.append(
            {
                "Season": target_season,
                "Slot": slot,
                "Round": _slot_round(slot),
                "TeamAID": ta_id,
                "TeamBID": tb_id,
                "TeamA_seed_num": ta_seed,
                "TeamB_seed_num": tb_seed,
                "seed_gap": (tb_seed - ta_seed) if (pd.notna(ta_seed) and pd.notna(tb_seed)) else np.nan,
                "p_teamA_win": round(p, 6),
                "predicted_winner": winner,
            }
        )

    preds = pd.DataFrame(rows).sort_values(["Round", "Slot"]).reset_index(drop=True)
    teams = pd.read_csv(KAGGLE / "MTeams.csv")[["TeamID", "TeamName"]]
    id_to_name = dict(zip(teams["TeamID"], teams["TeamName"]))
    preds["TeamA_name"] = preds["TeamAID"].map(id_to_name)
    preds["TeamB_name"] = preds["TeamBID"].map(id_to_name)
    preds["Winner_name"] = preds["predicted_winner"].map(id_to_name)

    return preds


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run 2026 bracket inference for updated locked model.")
    p.add_argument("--season", type=int, default=LIVE_SEASON, help=f"Season to predict (default: {LIVE_SEASON})")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    target_season = int(args.season)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    preds = run_bracket_inference(target_season)

    out_path = OUT_DIR / f"{target_season}_bracket_predictions.csv"
    preds.to_csv(out_path, index=False)

    print(f"Saved: {out_path}")
    if len(preds):
        print("Top bracket rows:")
        print(preds.head(10).to_string(index=False))


if __name__ == "__main__":
    main()

