from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common_utils import (  # noqa: E402
    champion_topk_metrics,
    logistic_baseline_pipeline,
    safe_auc,
    safe_logloss,
    upset_accuracy_seedgap_ge_5,
)

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST = ROOT / "Model Creation" / "Config" / "final_model_lock_manifest.json"


def load_manifest(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def split_by_manifest(df: pd.DataFrame, train_seasons: List[int], test_seasons: List[int]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_df = df[df["Season"].isin(train_seasons)].copy()
    test_df = df[df["Season"].isin(test_seasons)].copy()
    return train_df, test_df


def bracket_feature_cols(df: pd.DataFrame) -> List[str]:
    exclude = {"Season", "DayNum", "TeamAID", "TeamBID", "target_teamA_win"}
    return [c for c in df.columns if c not in exclude]


def champion_feature_cols(df: pd.DataFrame) -> List[str]:
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


def build_model(calibration: str):
    if calibration == "raw":
        return logistic_baseline_pipeline()
    if calibration in {"sigmoid", "isotonic"}:
        base = logistic_baseline_pipeline()
        return CalibratedClassifierCV(estimator=base, method=calibration, cv=5)
    raise ValueError(f"Unsupported calibration setting: {calibration}")


def run_bracket(cfg: Dict[str, object], train_seasons: List[int], test_seasons: List[int]) -> Tuple[Dict[str, object], pd.DataFrame]:
    dataset = ROOT / str(cfg["dataset_relpath"])
    calibration = str(cfg["calibration"])

    df = pd.read_csv(dataset)
    tr, te = split_by_manifest(df, train_seasons, test_seasons)

    X_cols = bracket_feature_cols(df)
    X_tr = tr[X_cols]
    y_tr = tr[str(cfg["target_column"])].astype(int).values
    X_te = te[X_cols]
    y_te = te[str(cfg["target_column"])].astype(int).values

    model = build_model(calibration)
    model.fit(X_tr, y_tr)
    p_te = model.predict_proba(X_te)[:, 1]

    metrics = {
        "objective": "bracket",
        "run_id": str(cfg["run_id"]),
        "feature_set": str(cfg["feature_set"]),
        "model_family": str(cfg["model_family"]),
        "calibration": calibration,
        "train_seasons": "|".join(str(x) for x in train_seasons),
        "test_seasons": "|".join(str(x) for x in test_seasons),
        "test_log_loss": safe_logloss(y_te, p_te),
        "test_auc": safe_auc(y_te, p_te),
        "upset_acc_seedgap_ge_5": upset_accuracy_seedgap_ge_5(te, p_te),
        "champ_top1_rate": np.nan,
        "champ_top4_rate": np.nan,
        "rows_train": len(tr),
        "rows_test": len(te),
        "n_features": len(X_cols),
    }

    pred = te[["Season", "DayNum", "TeamAID", "TeamBID", "target_teamA_win"]].copy()
    pred["p_teamA_win"] = p_te

    return metrics, pred


def run_champion(cfg: Dict[str, object], train_seasons: List[int], test_seasons: List[int]) -> Tuple[Dict[str, object], pd.DataFrame]:
    dataset = ROOT / str(cfg["dataset_relpath"])
    calibration = str(cfg["calibration"])

    df = pd.read_csv(dataset)
    tr, te = split_by_manifest(df, train_seasons, test_seasons)

    X_cols = champion_feature_cols(df)
    X_tr = tr[X_cols]
    y_tr = tr[str(cfg["target_column"])].astype(int).values
    X_te = te[X_cols]
    y_te = te[str(cfg["target_column"])].astype(int).values

    model = build_model(calibration)
    model.fit(X_tr, y_tr)
    p_te = model.predict_proba(X_te)[:, 1]

    top1, top4 = champion_topk_metrics(te, p_te)

    metrics = {
        "objective": "champion",
        "run_id": str(cfg["run_id"]),
        "feature_set": str(cfg["feature_set"]),
        "model_family": str(cfg["model_family"]),
        "calibration": calibration,
        "train_seasons": "|".join(str(x) for x in train_seasons),
        "test_seasons": "|".join(str(x) for x in test_seasons),
        "test_log_loss": safe_logloss(y_te, p_te),
        "test_auc": safe_auc(y_te, p_te),
        "upset_acc_seedgap_ge_5": np.nan,
        "champ_top1_rate": top1,
        "champ_top4_rate": top4,
        "rows_train": len(tr),
        "rows_test": len(te),
        "n_features": len(X_cols),
    }

    pred = te[["Season", "TeamID", "is_champion"]].copy()
    pred["p_champion"] = p_te
    pred["pred_rank_in_season"] = pred.groupby("Season")["p_champion"].rank(method="first", ascending=False).astype(int)

    return metrics, pred


def main() -> None:
    manifest = load_manifest(DEFAULT_MANIFEST)

    split = manifest["locked_split"]
    train_seasons = [int(x) for x in split["train_seasons"]]
    test_seasons = [int(x) for x in split["test_seasons"]]

    models_cfg = manifest["models"]

    bracket_metrics, bracket_pred = run_bracket(models_cfg["bracket"], train_seasons, test_seasons)
    champion_metrics, champion_pred = run_champion(models_cfg["champion"], train_seasons, test_seasons)

    metrics_df = pd.DataFrame([bracket_metrics, champion_metrics])

    out_cfg = manifest["output_paths"]
    metrics_path = ROOT / str(out_cfg["metrics_csv"])
    bracket_path = ROOT / str(out_cfg["bracket_predictions_csv"])
    champion_path = ROOT / str(out_cfg["champion_predictions_csv"])

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    bracket_path.parent.mkdir(parents=True, exist_ok=True)
    champion_path.parent.mkdir(parents=True, exist_ok=True)

    metrics_df.to_csv(metrics_path, index=False)
    bracket_pred.to_csv(bracket_path, index=False)
    champion_pred.to_csv(champion_path, index=False)

    print(f"Wrote {metrics_path}")
    print(f"Wrote {bracket_path}")
    print(f"Wrote {champion_path}")


if __name__ == "__main__":
    main()
