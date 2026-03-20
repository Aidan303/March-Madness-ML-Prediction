from __future__ import annotations

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

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(Path(__file__).resolve().parent))
BASE_MANIFEST = ROOT / "Model Creation" / "Config" / "final_model_lock_manifest.json"
WEIGHTED_MANIFEST = ROOT / "Model Creation Weighted Points" / "Config" / "final_model_lock_manifest_weighted_points.json"
RESULTS_DIR = ROOT / "Model Creation Weighted Points" / "Results" / "Model Refinement"

KAGGLE = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"
MODEL_READY = ROOT / "Good_Data" / "Model Ready Data"
HIST_MASTER = ROOT / "Good_Data" / "Master Data" / "Master CSV File and Support Files" / "master_features_all_teams_historical.csv"
LOCKED_DIR = ROOT / "Good_Data" / "Master Data" / "Pruned Feature Sets (Gold)"

WEIGHTS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32}


def slot_round(slot: str) -> int:
    for r in range(1, 7):
        if slot.startswith(f"R{r}"):
            return r
    return 0


def day_to_round(day: int) -> int | None:
    if day in (136, 137):
        return 1
    if day in (138, 139):
        return 2
    if day in (143, 144):
        return 3
    if day in (145, 146):
        return 4
    if day == 152:
        return 5
    if day == 154:
        return 6
    return None


def bracket_x_cols(df: pd.DataFrame) -> List[str]:
    exclude = {"Season", "DayNum", "Slot", "TeamAID", "TeamBID", "target_teamA_win"}
    return [c for c in df.columns if c not in exclude]


def logistic_pipeline() -> Pipeline:
    from common_utils import logistic_baseline_pipeline

    return logistic_baseline_pipeline()


def rf_pipeline() -> Pipeline:
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


def gbm_pipeline() -> Pipeline:
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


def calibrated(estimator, method: str):
    return CalibratedClassifierCV(estimator=estimator, method=method, cv=3)


def build_specs(base_manifest: Dict) -> List[Dict[str, object]]:
    specs: List[Dict[str, object]] = []

    locked_cal = str(base_manifest["models"]["bracket"]["calibration"])
    if locked_cal == "raw":
        specs.append({"name": "locked_baseline_weighted_points", "family": "logistic", "calibration": "raw", "est": logistic_pipeline()})
    else:
        specs.append(
            {
                "name": f"locked_baseline_{locked_cal}_weighted_points",
                "family": "logistic",
                "calibration": locked_cal,
                "est": calibrated(logistic_pipeline(), locked_cal),
            }
        )

    specs.extend(
        [
            {"name": "logreg_raw_weighted_points", "family": "logistic", "calibration": "raw", "est": logistic_pipeline()},
            {
                "name": "logreg_sigmoid_weighted_points",
                "family": "logistic",
                "calibration": "sigmoid",
                "est": calibrated(logistic_pipeline(), "sigmoid"),
            },
            {
                "name": "logreg_isotonic_weighted_points",
                "family": "logistic",
                "calibration": "isotonic",
                "est": calibrated(logistic_pipeline(), "isotonic"),
            },
            {"name": "rf_raw_weighted_points", "family": "rf", "calibration": "raw", "est": rf_pipeline()},
            {
                "name": "rf_sigmoid_weighted_points",
                "family": "rf",
                "calibration": "sigmoid",
                "est": calibrated(rf_pipeline(), "sigmoid"),
            },
            {"name": "gbm_raw_weighted_points", "family": "gbm", "calibration": "raw", "est": gbm_pipeline()},
            {
                "name": "gbm_sigmoid_weighted_points",
                "family": "gbm",
                "calibration": "sigmoid",
                "est": calibrated(gbm_pipeline(), "sigmoid"),
            },
        ]
    )

    try:
        from xgboost import XGBClassifier  # type: ignore

        xgb = Pipeline(
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
        specs.append({"name": "xgb_raw_weighted_points", "family": "xgb", "calibration": "raw", "est": xgb})
        specs.append({"name": "xgb_sigmoid_weighted_points", "family": "xgb", "calibration": "sigmoid", "est": calibrated(xgb, "sigmoid")})
    except Exception:
        pass

    return specs


def build_matchup_row(
    slot: str,
    ta_id: int,
    tb_id: int,
    team_index: pd.DataFrame,
    core_features: List[str],
    x_cols: List[str],
    season: int,
) -> pd.DataFrame | None:
    if ta_id not in team_index.index or tb_id not in team_index.index:
        return None

    ta = team_index.loc[ta_id]
    tb = team_index.loc[tb_id]
    seed_a = ta.get("tourney_seed_num", np.nan)
    seed_b = tb.get("tourney_seed_num", np.nan)

    row: Dict = {
        "Season": season,
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

    out = pd.DataFrame([row])
    for c in x_cols:
        if c not in out.columns:
            out[c] = np.nan
    return out[x_cols]


def simulate_season(
    fitted_model,
    season: int,
    seeds: pd.DataFrame,
    slots: pd.DataFrame,
    playins: pd.DataFrame,
    team_features: pd.DataFrame,
    core_features: List[str],
    x_cols: List[str],
) -> pd.DataFrame:
    slot_winner: Dict[str, int] = dict(zip(seeds["Seed"].astype(str), seeds["TeamID"].astype(int)))
    team_index = team_features.set_index("TeamID")

    all_slots = slots.copy()
    all_slots["_round"] = all_slots["Slot"].apply(slot_round)
    all_slots = all_slots.sort_values(["_round", "Slot"]).reset_index(drop=True)

    playin_slots = all_slots[all_slots["_round"] == 0]
    for _, sl in playin_slots.iterrows():
        slot = str(sl["Slot"])
        ta_id = slot_winner.get(str(sl["StrongSeed"]))
        tb_id = slot_winner.get(str(sl["WeakSeed"]))
        if ta_id is None or tb_id is None:
            continue
        match = playins[
            ((playins["WTeamID"] == ta_id) & (playins["LTeamID"] == tb_id))
            | ((playins["WTeamID"] == tb_id) & (playins["LTeamID"] == ta_id))
        ]
        if len(match) > 0:
            slot_winner[slot] = int(match.iloc[0]["WTeamID"])

    rows = []
    for _, sl in all_slots[all_slots["_round"] > 0].iterrows():
        slot = str(sl["Slot"])
        ta_id = slot_winner.get(str(sl["StrongSeed"]))
        tb_id = slot_winner.get(str(sl["WeakSeed"]))
        if ta_id is None or tb_id is None:
            continue

        x_row = build_matchup_row(slot, ta_id, tb_id, team_index, core_features, x_cols, season)
        if x_row is None:
            slot_winner[slot] = ta_id
            continue

        p = float(fitted_model.predict_proba(x_row)[0, 1])
        winner = ta_id if p >= 0.5 else tb_id
        slot_winner[slot] = winner
        rows.append({"Season": season, "Round": slot_round(slot), "Slot": slot, "predicted_winner": winner})

    return pd.DataFrame(rows)


def score_by_round(preds: pd.DataFrame, actual_main: pd.DataFrame) -> Dict[str, float]:
    out: Dict[str, float] = {}
    total_points = 0
    total_max = 0
    total_error = 0

    for rnd in [1, 2, 3, 4, 5, 6]:
        pred_set = set(preds[preds["Round"] == rnd]["predicted_winner"].astype(int).tolist())
        act_set = set(actual_main[actual_main["Round"] == rnd]["WTeamID"].astype(int).tolist())

        correct = len(pred_set.intersection(act_set))
        err = len(pred_set.symmetric_difference(act_set))

        pts = correct * WEIGHTS[rnd]
        max_pts = len(act_set) * WEIGHTS[rnd]

        out[f"r{rnd}_correct"] = correct
        out[f"r{rnd}_winner_set_error"] = err
        out[f"r{rnd}_points"] = pts
        out[f"r{rnd}_max_points"] = max_pts

        total_points += pts
        total_max += max_pts
        total_error += err

    out["total_points"] = total_points
    out["max_points"] = total_max
    out["points_pct"] = total_points / total_max if total_max else np.nan
    out["point_gap"] = total_max - total_points
    out["total_winner_set_error"] = total_error
    return out


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    WEIGHTED_MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    base_manifest = json.loads(BASE_MANIFEST.read_text(encoding="utf-8"))
    split = base_manifest["locked_split"]
    train_seasons = [int(s) for s in split["train_seasons"]]
    test_seasons = [int(s) for s in split["test_seasons"]]

    bracket_hist = pd.read_csv(MODEL_READY / "Bracket Model" / "bracket_games_core_historical.csv")
    x_cols = bracket_x_cols(bracket_hist)
    train_df = bracket_hist[bracket_hist["Season"].isin(train_seasons)].copy()

    X_train = train_df[x_cols]
    y_train = train_df["target_teamA_win"].astype(int).values

    hist_master = pd.read_csv(HIST_MASTER)
    seeds_all = pd.read_csv(KAGGLE / "MNCAATourneySeeds.csv")
    slots_all = pd.read_csv(KAGGLE / "MNCAATourneySlots.csv")
    actual_all = pd.read_csv(KAGGLE / "MNCAATourneyCompactResults.csv")
    core_features = pd.read_csv(LOCKED_DIR / "locked_feature_set_core.csv")["feature_name"].tolist()

    records: List[Dict] = []
    specs = build_specs(base_manifest)

    for spec in specs:
        print(f"Running {spec['name']} ...")
        model = spec["est"]
        model.fit(X_train, y_train)

        for season in test_seasons:
            team_features = hist_master[hist_master["Season"] == season].copy()
            seeds = seeds_all[seeds_all["Season"] == season].copy()
            slots = slots_all[slots_all["Season"] == season].copy()
            playins = actual_all[(actual_all["Season"] == season) & (actual_all["DayNum"] < 136)].copy()
            actual_main = actual_all[(actual_all["Season"] == season) & (actual_all["DayNum"] >= 136)].copy()
            actual_main["Round"] = actual_main["DayNum"].map(day_to_round)
            actual_main = actual_main[actual_main["Round"].notna()].copy()

            preds = simulate_season(model, season, seeds, slots, playins, team_features, core_features, x_cols)
            scores = score_by_round(preds, actual_main)

            row = {
                "model_name": spec["name"],
                "model_family": spec["family"],
                "calibration": spec["calibration"],
                "season": season,
            }
            row.update(scores)
            records.append(row)

    df = pd.DataFrame(records)
    by_season_path = RESULTS_DIR / "weighted_points_model_selection_by_season.csv"
    summary_path = RESULTS_DIR / "weighted_points_model_selection_overall.csv"

    df.sort_values(["season", "total_points", "total_winner_set_error"], ascending=[True, False, True]).to_csv(by_season_path, index=False)

    summary = (
        df.groupby(["model_name", "model_family", "calibration"], as_index=False)
        .agg(
            avg_points=("total_points", "mean"),
            avg_max_points=("max_points", "mean"),
            avg_points_pct=("points_pct", "mean"),
            avg_point_gap=("point_gap", "mean"),
            avg_winner_set_error=("total_winner_set_error", "mean"),
        )
        .sort_values(["avg_points", "avg_winner_set_error"], ascending=[False, True])
        .reset_index(drop=True)
    )
    summary.to_csv(summary_path, index=False)

    best = summary.iloc[0]

    weighted_manifest = {
        "manifest_version": "2.0",
        "created_date": pd.Timestamp.utcnow().strftime("%Y-%m-%d"),
        "selection_basis": "Weighted points objective (1,2,4,8,16,32) on locked 80/20 split",
        "feature_policy": base_manifest.get("feature_policy", {}),
        "selection_evidence": {
            "weighted_selection_by_season_csv": "Model Creation Weighted Points/Results/Model Refinement/weighted_points_model_selection_by_season.csv",
            "weighted_selection_overall_csv": "Model Creation Weighted Points/Results/Model Refinement/weighted_points_model_selection_overall.csv",
        },
        "locked_split": {
            "train_seasons": train_seasons,
            "test_seasons": test_seasons,
        },
        "models": {
            "bracket": {
                "run_id": str(best["model_name"]),
                "objective": "bracket",
                "model_family": str(best["model_family"]),
                "feature_set": "core",
                "calibration": str(best["calibration"]),
                "selected_variant_metric": {
                    "metric": "avg_weighted_points",
                    "value": float(best["avg_points"]),
                },
                "dataset_relpath": "Good_Data/Model Ready Data/Bracket Model/bracket_games_core_historical.csv",
                "target_column": "target_teamA_win",
            },
            "champion": {
                "run_id": "CHAMP_BASE_CORE_weighted_points",
                "objective": "champion",
                "model_family": "logistic",
                "feature_set": "core",
                "calibration": "raw",
                "selected_variant_metric": {
                    "metric": "inherited_from_baseline_manifest",
                    "value": base_manifest["models"]["champion"]["selected_variant_metric"]["value"],
                },
                "dataset_relpath": "Good_Data/Model Ready Data/Champion Model/champion_core_historical.csv",
                "target_column": "is_champion",
            },
        },
        "output_paths": {
            "metrics_csv": "Model Creation Weighted Points/Results/Production/production_run_metrics_weighted_points.csv",
            "bracket_predictions_csv": "Model Creation Weighted Points/Results/Production/production_predictions_bracket_weighted_points.csv",
            "champion_predictions_csv": "Model Creation Weighted Points/Results/Production/production_predictions_champion_weighted_points.csv",
        },
    }

    WEIGHTED_MANIFEST.write_text(json.dumps(weighted_manifest, indent=2), encoding="utf-8")

    print(f"Wrote {by_season_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {WEIGHTED_MANIFEST}")


if __name__ == "__main__":
    main()
