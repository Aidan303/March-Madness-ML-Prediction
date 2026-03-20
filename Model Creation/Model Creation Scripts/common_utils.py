from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
MODEL_CREATION_DIR = ROOT / "Model Creation"
MODEL_READY_DIR = ROOT / "Good_Data" / "Model Ready Data"

TRAIN_SEASONS = list(range(2003, 2020)) + [2021]
TEST_SEASONS = [2022, 2023, 2024, 2025]

BRACKET_DATASET = {
    "core": MODEL_READY_DIR / "Bracket Model" / "bracket_games_core_historical.csv",
    "extended": MODEL_READY_DIR / "Bracket Model" / "bracket_games_extended_historical.csv",
    "experimental": MODEL_READY_DIR / "Bracket Model" / "bracket_games_experimental_historical.csv",
}

CHAMPION_DATASET = {
    "core": MODEL_READY_DIR / "Champion Model" / "champion_core_historical.csv",
    "extended": MODEL_READY_DIR / "Champion Model" / "champion_extended_historical.csv",
    "experimental": MODEL_READY_DIR / "Champion Model" / "champion_experimental_historical.csv",
}

RUN_RESULTS_TEMPLATE = MODEL_CREATION_DIR / "Templates" / "step3_run_results_template.csv"
RUN_RESULTS_OUTPUT = MODEL_CREATION_DIR / "Results" / "Model Creation" / "step3_run_results.csv"


def season_split(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_df = df[df["Season"].isin(TRAIN_SEASONS)].copy()
    test_df = df[df["Season"].isin(TEST_SEASONS)].copy()
    return train_df, test_df


def logistic_baseline_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    solver="lbfgs",
                    max_iter=5000,
                ),
            ),
        ]
    )


def safe_auc(y_true: np.ndarray, p: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2:
        return np.nan
    return float(roc_auc_score(y_true, p))


def safe_logloss(y_true: np.ndarray, p: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2:
        return np.nan
    return float(log_loss(y_true, p, labels=[0, 1]))


def upset_accuracy_seedgap_ge_5(df_test: pd.DataFrame, p: np.ndarray) -> float:
    if "seed_gap" not in df_test.columns:
        return np.nan

    mask = df_test["seed_gap"].abs() >= 5
    sub = df_test.loc[mask].copy()
    if len(sub) == 0:
        return np.nan

    y_true = sub["target_teamA_win"].astype(int).values
    p_sub = p[mask.values]
    y_pred = (p_sub >= 0.5).astype(int)
    return float((y_pred == y_true).mean())


def champion_topk_metrics(df_test: pd.DataFrame, p: np.ndarray) -> Tuple[float, float]:
    tmp = df_test[["Season", "TeamID", "is_champion"]].copy()
    tmp["p"] = p

    top1_hits = []
    top4_hits = []

    for _, g in tmp.groupby("Season"):
        gs = g.sort_values("p", ascending=False).reset_index(drop=True)
        champ_rows = gs[gs["is_champion"] == 1]
        if champ_rows.empty:
            continue
        champ_team = int(champ_rows.iloc[0]["TeamID"])

        top1 = set(gs.head(1)["TeamID"].astype(int).tolist())
        top4 = set(gs.head(4)["TeamID"].astype(int).tolist())

        top1_hits.append(1 if champ_team in top1 else 0)
        top4_hits.append(1 if champ_team in top4 else 0)

    if not top1_hits:
        return np.nan, np.nan

    return float(np.mean(top1_hits)), float(np.mean(top4_hits))


def ensure_run_results_file() -> Path:
    RUN_RESULTS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if not RUN_RESULTS_OUTPUT.exists():
        if RUN_RESULTS_TEMPLATE.exists():
            df = pd.read_csv(RUN_RESULTS_TEMPLATE)
            df.to_csv(RUN_RESULTS_OUTPUT, index=False)
        else:
            raise FileNotFoundError(f"Missing template: {RUN_RESULTS_TEMPLATE}")
    return RUN_RESULTS_OUTPUT


def update_run_row(run_id: str, metrics: Dict[str, object]) -> None:
    out_path = ensure_run_results_file()
    df = pd.read_csv(out_path)

    if run_id not in set(df["run_id"].astype(str)):
        raise ValueError(f"run_id {run_id} not found in {out_path}")

    idx = df.index[df["run_id"].astype(str) == run_id][0]
    for k, v in metrics.items():
        if k in df.columns:
            if isinstance(v, str):
                df[k] = df[k].astype("object")
            df.loc[idx, k] = v

    df.to_csv(out_path, index=False)


def fmt_season_list(values: List[int]) -> str:
    return "|".join(str(v) for v in values)
