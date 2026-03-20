from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
KAGGLE = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"
MODEL_READY = ROOT / "Good_Data" / "Model Ready Data"
HIST_MASTER = ROOT / "Good_Data" / "Master Data" / "Master CSV File and Support Files" / "master_features_all_teams_historical.csv"
MANIFEST_PATH = ROOT / "Model Creation" / "Config" / "final_model_lock_manifest.json"
OUT_DIR = ROOT / "Model Creation" / "Results" / "Production"

SEASONS = [2023, 2024, 2025]
WEIGHTS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32}
ROUND_NAMES = {
    1: "Round of 64",
    2: "Round of 32",
    3: "Sweet 16",
    4: "Elite 8",
    5: "Final Four",
    6: "Championship",
}


def load_manifest() -> Dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def train_seasons_for(target_season: int) -> List[int]:
    return [s for s in range(2003, target_season) if s != 2020]


def bracket_x_cols(df: pd.DataFrame) -> List[str]:
    exclude = {"Season", "DayNum", "Slot", "TeamAID", "TeamBID", "target_teamA_win"}
    return [c for c in df.columns if c not in exclude]


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


def logistic_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(solver="lbfgs", max_iter=5000)),
        ]
    )


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


def get_model_specs(manifest: Dict) -> List[Tuple[str, object]]:
    specs: List[Tuple[str, object]] = []

    locked_cal = str(manifest["models"]["bracket"]["calibration"])
    if locked_cal == "raw":
        specs.append(("locked_baseline", logistic_pipeline()))
    else:
        specs.append((f"locked_baseline_{locked_cal}", calibrated(logistic_pipeline(), locked_cal)))

    specs.extend(
        [
            ("logreg_raw", logistic_pipeline()),
            ("logreg_sigmoid", calibrated(logistic_pipeline(), "sigmoid")),
            ("logreg_isotonic", calibrated(logistic_pipeline(), "isotonic")),
            ("rf_raw", rf_pipeline()),
            ("rf_sigmoid", calibrated(rf_pipeline(), "sigmoid")),
            ("gbm_raw", gbm_pipeline()),
            ("gbm_sigmoid", calibrated(gbm_pipeline(), "sigmoid")),
        ]
    )

    # Optional XGBoost variant if available in environment
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
        specs.append(("xgb_raw", xgb))
        specs.append(("xgb_sigmoid", calibrated(xgb, "sigmoid")))
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

    df_row = pd.DataFrame([row])
    for c in x_cols:
        if c not in df_row.columns:
            df_row[c] = np.nan
    return df_row[x_cols]


def simulate_bracket(
    model,
    season: int,
    df_hist: pd.DataFrame,
    team_features: pd.DataFrame,
    seeds: pd.DataFrame,
    slots: pd.DataFrame,
    playin_results: pd.DataFrame,
    core_features: List[str],
) -> pd.DataFrame:
    train_seasons = train_seasons_for(season)
    train_df = df_hist[df_hist["Season"].isin(train_seasons)].copy()

    x_cols = bracket_x_cols(df_hist)
    model.fit(train_df[x_cols], train_df["target_teamA_win"].astype(int).values)

    team_index = team_features.set_index("TeamID")
    slot_winner: Dict[str, int] = dict(zip(seeds["Seed"].astype(str), seeds["TeamID"].astype(int)))

    all_slots = slots.copy()
    all_slots["_round"] = all_slots["Slot"].apply(slot_round)
    all_slots = all_slots.sort_values(["_round", "Slot"]).reset_index(drop=True)

    playins = all_slots[all_slots["_round"] == 0]
    for _, sl in playins.iterrows():
        slot = str(sl["Slot"])
        ta_id = slot_winner.get(str(sl["StrongSeed"]))
        tb_id = slot_winner.get(str(sl["WeakSeed"]))
        if ta_id is None or tb_id is None:
            continue
        match = playin_results[
            ((playin_results["WTeamID"] == ta_id) & (playin_results["LTeamID"] == tb_id))
            | ((playin_results["WTeamID"] == tb_id) & (playin_results["LTeamID"] == ta_id))
        ]
        if len(match) > 0:
            slot_winner[slot] = int(match.iloc[0]["WTeamID"])

    rows = []
    main_slots = all_slots[all_slots["_round"] > 0]
    for _, sl in main_slots.iterrows():
        slot = str(sl["Slot"])
        ta_id = slot_winner.get(str(sl["StrongSeed"]))
        tb_id = slot_winner.get(str(sl["WeakSeed"]))
        if ta_id is None or tb_id is None:
            continue

        x_row = build_matchup_row(slot, ta_id, tb_id, team_index, core_features, x_cols, season)
        if x_row is None:
            slot_winner[slot] = ta_id
            continue

        p = float(model.predict_proba(x_row)[0, 1])
        winner = ta_id if p >= 0.5 else tb_id
        slot_winner[slot] = winner
        rows.append({"Season": season, "Slot": slot, "Round": slot_round(slot), "predicted_winner": winner})

    return pd.DataFrame(rows)


def score_winner_sets(preds: pd.DataFrame, actual_round_winners: pd.DataFrame) -> Dict[str, float]:
    out: Dict[str, float] = {}
    total_points = 0
    total_max = 0
    total_error = 0
    total_correct = 0

    for rnd in [1, 2, 3, 4, 5, 6]:
        pred_set = set(preds[preds["Round"] == rnd]["predicted_winner"].astype(int).tolist())
        act_set = set(actual_round_winners[actual_round_winners["Round"] == rnd]["WTeamID"].astype(int).tolist())

        correct = len(pred_set.intersection(act_set))
        winner_set_error = len(pred_set.symmetric_difference(act_set))

        pts = correct * WEIGHTS[rnd]
        mx = len(act_set) * WEIGHTS[rnd]

        out[f"r{rnd}_correct"] = correct
        out[f"r{rnd}_winner_set_error"] = winner_set_error
        out[f"r{rnd}_points"] = pts
        out[f"r{rnd}_max_points"] = mx

        total_points += pts
        total_max += mx
        total_error += winner_set_error
        total_correct += correct

    out["total_correct_winners"] = total_correct
    out["total_winner_set_error"] = total_error
    out["total_points"] = total_points
    out["max_points"] = total_max
    out["points_pct"] = (total_points / total_max) if total_max else np.nan
    out["point_gap"] = total_max - total_points
    return out


def build_markdown_report(per_season_df: pd.DataFrame, summary_df: pd.DataFrame, out_path: Path) -> None:
    lines: List[str] = []
    lines.append("# Bracket Model Family Sweep Report")
    lines.append("")
    lines.append("## Objective")
    lines.append("Evaluate multiple bracket model families on seasons 2023-2025 using winner-set comparison by round and weighted points (1,2,4,8,16,32).")
    lines.append("")

    best = summary_df.iloc[0]
    lines.append("## Best Overall Model")
    lines.append(f"- Model: {best['model_name']}")
    lines.append(f"- Avg points: {best['avg_points']:.2f}/{best['avg_max_points']:.2f}")
    lines.append(f"- Avg points %: {best['avg_points_pct']:.2%}")
    lines.append(f"- Avg point gap: {best['avg_point_gap']:.2f}")
    lines.append(f"- Avg winner-set error: {best['avg_winner_set_error']:.2f}")
    lines.append("")

    lines.append("## Leaderboard (Overall)")
    lines.append("| Rank | Model | Avg Points | Avg Points % | Avg Point Gap | Avg Winner-Set Error |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for i, (_, r) in enumerate(summary_df.iterrows(), start=1):
        lines.append(
            f"| {i} | {r['model_name']} | {r['avg_points']:.2f}/{r['avg_max_points']:.2f} | "
            f"{r['avg_points_pct']:.2%} | {r['avg_point_gap']:.2f} | {r['avg_winner_set_error']:.2f} |"
        )
    lines.append("")

    lines.append("## Per-Season Best Models")
    for season in sorted(per_season_df["season"].unique()):
        sub = per_season_df[per_season_df["season"] == season].sort_values(
            ["total_points", "total_winner_set_error"], ascending=[False, True]
        )
        top = sub.iloc[0]
        lines.append(f"### {season}")
        lines.append(f"- Best model: {top['model_name']}")
        lines.append(f"- Points: {int(top['total_points'])}/{int(top['max_points'])} ({top['points_pct']:.2%})")
        lines.append(f"- Point gap: {int(top['point_gap'])}")
        lines.append(f"- Winner-set error: {int(top['total_winner_set_error'])}")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest()
    core_features = pd.read_csv(
        ROOT / "Good_Data" / "Master Data" / "Pruned Feature Sets (Gold)" / "locked_feature_set_core.csv"
    )["feature_name"].tolist()

    bracket_hist = pd.read_csv(MODEL_READY / "Bracket Model" / "bracket_games_core_historical.csv")
    hist_master = pd.read_csv(HIST_MASTER)
    seeds_all = pd.read_csv(KAGGLE / "MNCAATourneySeeds.csv")
    slots_all = pd.read_csv(KAGGLE / "MNCAATourneySlots.csv")
    actual_all = pd.read_csv(KAGGLE / "MNCAATourneyCompactResults.csv")

    model_specs = get_model_specs(manifest)

    records: List[Dict] = []
    for model_name, model in model_specs:
        print(f"\n=== Running model: {model_name} ===")
        for season in SEASONS:
            print(f"  Season {season} ...")
            team_features = hist_master[hist_master["Season"] == season].copy()
            seeds = seeds_all[seeds_all["Season"] == season].copy()
            slots = slots_all[slots_all["Season"] == season].copy()

            playins = actual_all[(actual_all["Season"] == season) & (actual_all["DayNum"] < 136)].copy()
            actual_main = actual_all[(actual_all["Season"] == season) & (actual_all["DayNum"] >= 136)].copy()
            actual_main["Round"] = actual_main["DayNum"].map(day_to_round)
            actual_main = actual_main[actual_main["Round"].notna()].copy()

            preds = simulate_bracket(
                model=model,
                season=season,
                df_hist=bracket_hist,
                team_features=team_features,
                seeds=seeds,
                slots=slots,
                playin_results=playins,
                core_features=core_features,
            )

            scores = score_winner_sets(preds, actual_main)
            rec = {"model_name": model_name, "season": season}
            rec.update(scores)
            records.append(rec)

    per_season_df = pd.DataFrame(records).sort_values(
        ["season", "total_points", "total_winner_set_error"], ascending=[True, False, True]
    )

    summary_df = (
        per_season_df.groupby("model_name", as_index=False)
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

    out_season = OUT_DIR / "model_family_sweep_bracket_2023_2025_by_season.csv"
    out_summary = OUT_DIR / "model_family_sweep_bracket_2023_2025_overall.csv"
    out_report = OUT_DIR / "model_family_sweep_bracket_2023_2025_report.md"

    per_season_df.to_csv(out_season, index=False)
    summary_df.to_csv(out_summary, index=False)
    build_markdown_report(per_season_df, summary_df, out_report)

    print("\nSaved outputs:")
    print(f"  {out_season}")
    print(f"  {out_summary}")
    print(f"  {out_report}")


if __name__ == "__main__":
    main()
