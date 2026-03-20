from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common_utils import (  # noqa: E402
    CHAMPION_DATASET,
    RUN_RESULTS_OUTPUT,
    TEST_SEASONS,
    TRAIN_SEASONS,
    champion_topk_metrics,
    safe_auc,
    safe_logloss,
    season_split,
    update_run_row,
    fmt_season_list,
)


def feature_cols(df: pd.DataFrame) -> list[str]:
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


def run_one(run_id: str, feature_set: str) -> None:
    csv_path = CHAMPION_DATASET[feature_set]
    df = pd.read_csv(csv_path)
    tr, te = season_split(df)

    X_cols = feature_cols(df)
    X_tr, y_tr = tr[X_cols], tr["is_champion"].astype(int).values
    X_te, y_te = te[X_cols], te["is_champion"].astype(int).values

    model = tree_pipeline()
    model.fit(X_tr, y_tr)
    p_te = model.predict_proba(X_te)[:, 1]

    top1, top4 = champion_topk_metrics(te, p_te)

    metrics = {
        "model_family": "tree",
        "feature_set": feature_set,
        "train_seasons": fmt_season_list(TRAIN_SEASONS),
        "test_seasons": fmt_season_list(TEST_SEASONS),
        "test_log_loss": safe_logloss(y_te, p_te),
        "test_auc": safe_auc(y_te, p_te),
        "upset_acc_seedgap_ge_5": np.nan,
        "champ_top1_rate": top1,
        "champ_top4_rate": top4,
        "selected_for_next_stage": "pending_final_selection",
        "notes": f"rows_train={len(tr)}; rows_test={len(te)}; n_features={len(X_cols)}",
    }

    update_run_row(run_id, metrics)
    print(f"Updated {run_id} with feature_set={feature_set}")


def main() -> None:
    rr = pd.read_csv(RUN_RESULTS_OUTPUT)
    set1 = rr.loc[rr["run_id"] == "CHAMP_TREE_SET1", "feature_set"].iloc[0]
    set2 = rr.loc[rr["run_id"] == "CHAMP_TREE_SET2", "feature_set"].iloc[0]

    run_one("CHAMP_TREE_SET1", str(set1))
    run_one("CHAMP_TREE_SET2", str(set2))


if __name__ == "__main__":
    main()
