from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "Updated Feature List Model Creation"
DATA_DIR = OUT_ROOT / "data"
RESULTS_DIR = OUT_ROOT / "results"

BRACKET_PATH = DATA_DIR / "bracket_games_updated_core_historical.csv"
CHAMPION_PATH = DATA_DIR / "champion_updated_core_historical.csv"

TRAIN_SEASONS = list(range(2003, 2020)) + [2021]
TEST_SEASONS = [2022, 2023, 2024, 2025]


def season_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_df = df[df["Season"].isin(TRAIN_SEASONS)].copy()
    test_df = df[df["Season"].isin(TEST_SEASONS)].copy()
    return train_df, test_df


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


def champion_topk_metrics(df_test: pd.DataFrame, p: np.ndarray) -> tuple[float, float]:
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


def bracket_feature_cols(df: pd.DataFrame) -> list[str]:
    exclude = {"Season", "DayNum", "TeamAID", "TeamBID", "target_teamA_win"}
    return [c for c in df.columns if c not in exclude]


def champion_feature_cols(df: pd.DataFrame) -> list[str]:
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


def logistic_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(solver="lbfgs", max_iter=5000)),
        ]
    )


def tree_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            (
                "model",
                HistGradientBoostingClassifier(
                    learning_rate=0.05,
                    max_depth=4,
                    max_iter=300,
                    random_state=42,
                ),
            ),
        ]
    )


def build_model(model_family: str, calibration: str):
    if model_family == "logistic":
        base = logistic_pipeline()
    elif model_family == "tree":
        base = tree_pipeline()
    else:
        raise ValueError(f"Unsupported model_family: {model_family}")

    if calibration == "raw":
        return base
    if calibration in {"sigmoid", "isotonic"}:
        return CalibratedClassifierCV(estimator=base, method=calibration, cv=5)
    raise ValueError(f"Unsupported calibration: {calibration}")


def evaluate_bracket(df: pd.DataFrame, model_family: str, calibration: str) -> tuple[dict[str, object], pd.DataFrame]:
    tr, te = season_split(df)
    x_cols = bracket_feature_cols(df)

    x_tr = tr[x_cols]
    y_tr = tr["target_teamA_win"].astype(int).values
    x_te = te[x_cols]
    y_te = te["target_teamA_win"].astype(int).values

    model = build_model(model_family, calibration)
    model.fit(x_tr, y_tr)
    p_te = model.predict_proba(x_te)[:, 1]

    metrics = {
        "objective": "bracket",
        "model_family": model_family,
        "calibration": calibration,
        "train_seasons": "|".join(str(x) for x in TRAIN_SEASONS),
        "test_seasons": "|".join(str(x) for x in TEST_SEASONS),
        "test_log_loss": safe_logloss(y_te, p_te),
        "test_auc": safe_auc(y_te, p_te),
        "upset_acc_seedgap_ge_5": upset_accuracy_seedgap_ge_5(te, p_te),
        "champ_top1_rate": np.nan,
        "champ_top4_rate": np.nan,
        "rows_train": len(tr),
        "rows_test": len(te),
        "n_features": len(x_cols),
    }

    pred = te[["Season", "DayNum", "TeamAID", "TeamBID", "target_teamA_win"]].copy()
    pred["model_family"] = model_family
    pred["calibration"] = calibration
    pred["p_teamA_win"] = p_te
    return metrics, pred


def evaluate_champion(df: pd.DataFrame, model_family: str, calibration: str) -> tuple[dict[str, object], pd.DataFrame]:
    tr, te = season_split(df)
    x_cols = champion_feature_cols(df)

    x_tr = tr[x_cols]
    y_tr = tr["is_champion"].astype(int).values
    x_te = te[x_cols]
    y_te = te["is_champion"].astype(int).values

    model = build_model(model_family, calibration)
    model.fit(x_tr, y_tr)
    p_te = model.predict_proba(x_te)[:, 1]

    top1, top4 = champion_topk_metrics(te, p_te)

    metrics = {
        "objective": "champion",
        "model_family": model_family,
        "calibration": calibration,
        "train_seasons": "|".join(str(x) for x in TRAIN_SEASONS),
        "test_seasons": "|".join(str(x) for x in TEST_SEASONS),
        "test_log_loss": safe_logloss(y_te, p_te),
        "test_auc": safe_auc(y_te, p_te),
        "upset_acc_seedgap_ge_5": np.nan,
        "champ_top1_rate": top1,
        "champ_top4_rate": top4,
        "rows_train": len(tr),
        "rows_test": len(te),
        "n_features": len(x_cols),
    }

    pred = te[["Season", "TeamID", "is_champion"]].copy()
    pred["model_family"] = model_family
    pred["calibration"] = calibration
    pred["p_champion"] = p_te
    pred["pred_rank_in_season"] = pred.groupby("Season")["p_champion"].rank(method="first", ascending=False).astype(int)
    return metrics, pred


def select_bracket_winner(results_df: pd.DataFrame) -> pd.Series:
    best_upset = results_df["upset_acc_seedgap_ge_5"].max()
    guardrail_min = best_upset - 0.02 if pd.notna(best_upset) else -np.inf

    eligible = results_df[results_df["upset_acc_seedgap_ge_5"].fillna(-np.inf) >= guardrail_min].copy()
    if eligible.empty:
        eligible = results_df.copy()

    eligible = eligible.sort_values(["test_log_loss", "test_auc"], ascending=[True, False]).reset_index(drop=True)
    return eligible.iloc[0]


def select_champion_winner(results_df: pd.DataFrame) -> pd.Series:
    top4_values = sorted(results_df["champ_top4_rate"].dropna().unique().tolist(), reverse=True)
    top4_cut = top4_values[1] if len(top4_values) >= 2 else (top4_values[0] if top4_values else -np.inf)
    eligible = results_df[results_df["champ_top4_rate"].fillna(-np.inf) >= top4_cut].copy()
    if eligible.empty:
        eligible = results_df.copy()

    eligible = eligible.sort_values(["test_log_loss", "test_auc"], ascending=[True, False]).reset_index(drop=True)
    return eligible.iloc[0]


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    bracket_df = pd.read_csv(BRACKET_PATH)
    champion_df = pd.read_csv(CHAMPION_PATH)

    run_grid = [
        ("logistic", "raw"),
        ("logistic", "sigmoid"),
        ("logistic", "isotonic"),
        ("tree", "raw"),
        ("tree", "sigmoid"),
        ("tree", "isotonic"),
    ]

    all_metrics: list[dict[str, object]] = []
    bracket_preds: list[pd.DataFrame] = []
    champion_preds: list[pd.DataFrame] = []

    for model_family, calibration in run_grid:
        m_b, p_b = evaluate_bracket(bracket_df, model_family, calibration)
        m_c, p_c = evaluate_champion(champion_df, model_family, calibration)

        all_metrics.append(m_b)
        all_metrics.append(m_c)
        bracket_preds.append(p_b)
        champion_preds.append(p_c)

        print(f"Completed {model_family}_{calibration}")

    metrics_df = pd.DataFrame(all_metrics)
    bracket_metrics = metrics_df[metrics_df["objective"] == "bracket"].copy().reset_index(drop=True)
    champion_metrics = metrics_df[metrics_df["objective"] == "champion"].copy().reset_index(drop=True)

    bracket_winner = select_bracket_winner(bracket_metrics)
    champion_winner = select_champion_winner(champion_metrics)

    selected_df = pd.DataFrame(
        [
            {
                "objective": "bracket",
                "selected_model_family": bracket_winner["model_family"],
                "selected_calibration": bracket_winner["calibration"],
                "test_log_loss": bracket_winner["test_log_loss"],
                "test_auc": bracket_winner["test_auc"],
                "upset_acc_seedgap_ge_5": bracket_winner["upset_acc_seedgap_ge_5"],
                "champ_top1_rate": np.nan,
                "champ_top4_rate": np.nan,
            },
            {
                "objective": "champion",
                "selected_model_family": champion_winner["model_family"],
                "selected_calibration": champion_winner["calibration"],
                "test_log_loss": champion_winner["test_log_loss"],
                "test_auc": champion_winner["test_auc"],
                "upset_acc_seedgap_ge_5": np.nan,
                "champ_top1_rate": champion_winner["champ_top1_rate"],
                "champ_top4_rate": champion_winner["champ_top4_rate"],
            },
        ]
    )

    metrics_path = RESULTS_DIR / "updated_model_run_metrics.csv"
    bracket_pred_path = RESULTS_DIR / "updated_model_predictions_bracket_all_variants.csv"
    champion_pred_path = RESULTS_DIR / "updated_model_predictions_champion_all_variants.csv"
    selected_path = RESULTS_DIR / "updated_model_selected_for_production.csv"

    metrics_df.to_csv(metrics_path, index=False)
    pd.concat(bracket_preds, ignore_index=True).to_csv(bracket_pred_path, index=False)
    pd.concat(champion_preds, ignore_index=True).to_csv(champion_pred_path, index=False)
    selected_df.to_csv(selected_path, index=False)

    print(f"Wrote {metrics_path}")
    print(f"Wrote {bracket_pred_path}")
    print(f"Wrote {champion_pred_path}")
    print(f"Wrote {selected_path}")


if __name__ == "__main__":
    main()

