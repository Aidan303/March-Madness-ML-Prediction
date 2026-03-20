from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common_utils import (  # noqa: E402
    CHAMPION_DATASET,
    TEST_SEASONS,
    TRAIN_SEASONS,
    champion_topk_metrics,
    logistic_baseline_pipeline,
    safe_auc,
    safe_logloss,
    season_split,
    update_run_row,
    fmt_season_list,
)

RUN_ID_MAP = {
    "core": "CHAMP_BASE_CORE",
    "extended": "CHAMP_BASE_EXT",
    "experimental": "CHAMP_BASE_EXP",
}


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


def run_one(feature_set: str, csv_path: Path) -> None:
    df = pd.read_csv(csv_path)
    tr, te = season_split(df)

    X_cols = feature_cols(df)
    X_tr, y_tr = tr[X_cols], tr["is_champion"].astype(int).values
    X_te, y_te = te[X_cols], te["is_champion"].astype(int).values

    model = logistic_baseline_pipeline()
    model.fit(X_tr, y_tr)
    p_te = model.predict_proba(X_te)[:, 1]

    top1, top4 = champion_topk_metrics(te, p_te)

    metrics = {
        "model_family": "logistic",
        "feature_set": feature_set,
        "train_seasons": fmt_season_list(TRAIN_SEASONS),
        "test_seasons": fmt_season_list(TEST_SEASONS),
        "test_log_loss": safe_logloss(y_te, p_te),
        "test_auc": safe_auc(y_te, p_te),
        "upset_acc_seedgap_ge_5": np.nan,
        "champ_top1_rate": top1,
        "champ_top4_rate": top4,
        "selected_for_next_stage": np.nan,
        "notes": f"rows_train={len(tr)}; rows_test={len(te)}; n_features={len(X_cols)}",
    }

    run_id = RUN_ID_MAP[feature_set]
    update_run_row(run_id, metrics)
    print(f"Updated {run_id} from {csv_path.name}")


def main() -> None:
    for feature_set, path in CHAMPION_DATASET.items():
        run_one(feature_set, path)


if __name__ == "__main__":
    main()
