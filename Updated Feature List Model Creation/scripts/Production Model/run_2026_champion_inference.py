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


def champion_x_cols(df: pd.DataFrame) -> List[str]:
    exclude = {
        "Season",
        "TeamID",
        "TeamName",
        "ConfAbbrev",
        "is_tourney_team",
        "is_champion",
        "reached_sweet16",
        "reached_elite8",
        "reached_final4",
        "reached_title_game",
    }
    return [c for c in df.columns if c not in exclude]


def run_champion_inference(target_season: int) -> pd.DataFrame:
    manifest = load_manifest()
    cfg = manifest["models"]["champion"]

    hist_path = ROOT / str(cfg["dataset_relpath"])
    df_hist = pd.read_csv(hist_path)

    train_seasons = _train_seasons_for(target_season)
    df_train = df_hist[df_hist["Season"].isin(train_seasons)].copy()
    x_cols = champion_x_cols(df_hist)

    model = build_model(str(cfg["calibration"]))
    model.fit(df_train[x_cols], df_train[str(cfg["target_column"])].astype(int).values)

    team_features_path = DATA_DIR / f"master_features_all_teams_{target_season}_updated_core.csv"
    if not team_features_path.exists():
        raise FileNotFoundError(
            f"Missing updated team feature table for season {target_season}: {team_features_path}. "
            "Run Updated Feature List Model Creation/scripts/build_updated_pipeline.py first."
        )

    curr = pd.read_csv(team_features_path)
    candidates = curr[curr["is_tourney_team"] == 1].copy()
    if len(candidates) == 0:
        raise ValueError(f"No tourney teams found for season {target_season} in {team_features_path}")

    for c in x_cols:
        if c not in candidates.columns:
            candidates[c] = np.nan

    p = model.predict_proba(candidates[x_cols])[:, 1]

    preds = candidates[["Season", "TeamID", "TeamName", "tourney_seed_num"]].copy()
    preds["p_champion"] = p.round(6)
    preds["rank"] = preds["p_champion"].rank(method="first", ascending=False).astype(int)
    preds = preds.sort_values("rank").reset_index(drop=True)
    return preds


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run 2026 champion inference for updated locked model.")
    p.add_argument("--season", type=int, default=LIVE_SEASON, help=f"Season to predict (default: {LIVE_SEASON})")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    target_season = int(args.season)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    preds = run_champion_inference(target_season)

    out_path = OUT_DIR / f"{target_season}_champion_predictions.csv"
    preds.to_csv(out_path, index=False)

    print(f"Saved: {out_path}")
    print("Top 10 championship probabilities:")
    print(preds.head(10).to_string(index=False))


if __name__ == "__main__":
    main()

