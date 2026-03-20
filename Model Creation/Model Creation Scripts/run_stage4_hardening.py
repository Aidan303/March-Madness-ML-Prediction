from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV

sys.path.append(str(Path(__file__).resolve().parents[0]))
from common_utils import (  # noqa: E402
    BRACKET_DATASET,
    CHAMPION_DATASET,
    MODEL_CREATION_DIR,
    TEST_SEASONS,
    TRAIN_SEASONS,
    champion_topk_metrics,
    logistic_baseline_pipeline,
    safe_auc,
    safe_logloss,
    season_split,
    upset_accuracy_seedgap_ge_5,
)

OUT_RESULTS = MODEL_CREATION_DIR / "Results" / "Model Refinement" / "stage4_hardening_results.csv"
OUT_STABILITY = MODEL_CREATION_DIR / "Results" / "Model Refinement" / "stage4_stability_by_season.csv"
OUT_SUMMARY_MD = MODEL_CREATION_DIR / "Reports" / "Model Refinement" / "STAGE4_HARDENING_SUMMARY.md"


def bracket_feature_cols(df: pd.DataFrame) -> List[str]:
    exclude = {
        "Season",
        "DayNum",
        "TeamAID",
        "TeamBID",
        "target_teamA_win",
    }
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


def evaluate_bracket_variant(
    variant: str,
    X_tr: pd.DataFrame,
    y_tr: np.ndarray,
    X_te: pd.DataFrame,
    y_te: np.ndarray,
    te_df: pd.DataFrame,
) -> Dict[str, object]:
    if variant == "raw":
        model = logistic_baseline_pipeline()
    elif variant in {"sigmoid", "isotonic"}:
        base = logistic_baseline_pipeline()
        model = CalibratedClassifierCV(estimator=base, method=variant, cv=5)
    else:
        raise ValueError(f"Unknown variant: {variant}")

    model.fit(X_tr, y_tr)
    p_te = model.predict_proba(X_te)[:, 1]

    return {
        "objective": "bracket",
        "run_id": "BRK_BASE_CORE",
        "feature_set": "core",
        "variant": variant,
        "train_seasons": "|".join(str(s) for s in TRAIN_SEASONS),
        "test_seasons": "|".join(str(s) for s in TEST_SEASONS),
        "test_log_loss": safe_logloss(y_te, p_te),
        "test_auc": safe_auc(y_te, p_te),
        "upset_acc_seedgap_ge_5": upset_accuracy_seedgap_ge_5(te_df, p_te),
        "champ_top1_rate": np.nan,
        "champ_top4_rate": np.nan,
        "rows_train": len(X_tr),
        "rows_test": len(X_te),
        "n_features": X_tr.shape[1],
    }, p_te


def evaluate_champion_variant(
    variant: str,
    X_tr: pd.DataFrame,
    y_tr: np.ndarray,
    X_te: pd.DataFrame,
    y_te: np.ndarray,
    te_df: pd.DataFrame,
) -> Dict[str, object]:
    if variant == "raw":
        model = logistic_baseline_pipeline()
    elif variant in {"sigmoid", "isotonic"}:
        base = logistic_baseline_pipeline()
        model = CalibratedClassifierCV(estimator=base, method=variant, cv=5)
    else:
        raise ValueError(f"Unknown variant: {variant}")

    model.fit(X_tr, y_tr)
    p_te = model.predict_proba(X_te)[:, 1]
    top1, top4 = champion_topk_metrics(te_df, p_te)

    return {
        "objective": "champion",
        "run_id": "CHAMP_BASE_CORE",
        "feature_set": "core",
        "variant": variant,
        "train_seasons": "|".join(str(s) for s in TRAIN_SEASONS),
        "test_seasons": "|".join(str(s) for s in TEST_SEASONS),
        "test_log_loss": safe_logloss(y_te, p_te),
        "test_auc": safe_auc(y_te, p_te),
        "upset_acc_seedgap_ge_5": np.nan,
        "champ_top1_rate": top1,
        "champ_top4_rate": top4,
        "rows_train": len(X_tr),
        "rows_test": len(X_te),
        "n_features": X_tr.shape[1],
    }, p_te


def bracket_stability_by_season(te_df: pd.DataFrame, p: np.ndarray, variant: str) -> pd.DataFrame:
    tmp = te_df.copy()
    tmp["p"] = p
    rows = []

    for season, g in tmp.groupby("Season"):
        y_true = g["target_teamA_win"].astype(int).values
        p_season = g["p"].values
        rows.append(
            {
                "objective": "bracket",
                "variant": variant,
                "Season": int(season),
                "test_log_loss": safe_logloss(y_true, p_season),
                "test_auc": safe_auc(y_true, p_season),
                "upset_acc_seedgap_ge_5": upset_accuracy_seedgap_ge_5(g, p_season),
                "champ_top1_rate": np.nan,
                "champ_top4_rate": np.nan,
            }
        )

    return pd.DataFrame(rows)


def champion_stability_by_season(te_df: pd.DataFrame, p: np.ndarray, variant: str) -> pd.DataFrame:
    tmp = te_df.copy()
    tmp["p"] = p
    rows = []

    for season, g in tmp.groupby("Season"):
        y_true = g["is_champion"].astype(int).values
        p_season = g["p"].values
        top1, top4 = champion_topk_metrics(g, p_season)
        rows.append(
            {
                "objective": "champion",
                "variant": variant,
                "Season": int(season),
                "test_log_loss": safe_logloss(y_true, p_season),
                "test_auc": safe_auc(y_true, p_season),
                "upset_acc_seedgap_ge_5": np.nan,
                "champ_top1_rate": top1,
                "champ_top4_rate": top4,
            }
        )

    return pd.DataFrame(rows)


def build_summary_md(df_results: pd.DataFrame) -> str:
    out = []
    out.append("# Stage 4 Hardening Summary")
    out.append("")
    out.append("Focused scope:")
    out.append("- Bracket candidate: BRK_BASE_CORE")
    out.append("- Champion candidate: CHAMP_BASE_CORE")
    out.append("")

    for objective in ["bracket", "champion"]:
        d = df_results[df_results["objective"] == objective].sort_values("test_log_loss")
        best = d.iloc[0]

        out.append(f"## {objective.title()} objective")
        out.append("")
        out.append("| Variant | Test Log Loss | Test AUC | Upset Acc (seed_gap abs >= 5) | Champion Top-1 | Champion Top-4 |")
        out.append("|---|---:|---:|---:|---:|---:|")
        for _, r in d.iterrows():
            upset = "" if pd.isna(r["upset_acc_seedgap_ge_5"]) else f"{r['upset_acc_seedgap_ge_5']:.6f}"
            c1 = "" if pd.isna(r["champ_top1_rate"]) else f"{r['champ_top1_rate']:.6f}"
            c4 = "" if pd.isna(r["champ_top4_rate"]) else f"{r['champ_top4_rate']:.6f}"
            out.append(
                f"| {r['variant']} | {r['test_log_loss']:.6f} | {r['test_auc']:.6f} | {upset} | {c1} | {c4} |"
            )

        out.append("")
        out.append(
            f"Selected calibration variant by primary metric (test_log_loss): **{best['variant']}**"
        )
        out.append("")

    return "\n".join(out)


def main() -> None:
    OUT_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    OUT_STABILITY.parent.mkdir(parents=True, exist_ok=True)
    OUT_SUMMARY_MD.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    stability_frames = []

    # Bracket hardening on promoted winner only.
    df_b = pd.read_csv(BRACKET_DATASET["core"])
    tr_b, te_b = season_split(df_b)
    Xb = bracket_feature_cols(df_b)
    Xb_tr, yb_tr = tr_b[Xb], tr_b["target_teamA_win"].astype(int).values
    Xb_te, yb_te = te_b[Xb], te_b["target_teamA_win"].astype(int).values

    for variant in ["raw", "sigmoid", "isotonic"]:
        metrics, p = evaluate_bracket_variant(variant, Xb_tr, yb_tr, Xb_te, yb_te, te_b)
        rows.append(metrics)
        stability_frames.append(bracket_stability_by_season(te_b, p, variant))

    # Champion hardening on promoted winner only.
    df_c = pd.read_csv(CHAMPION_DATASET["core"])
    tr_c, te_c = season_split(df_c)
    Xc = champion_feature_cols(df_c)
    Xc_tr, yc_tr = tr_c[Xc], tr_c["is_champion"].astype(int).values
    Xc_te, yc_te = te_c[Xc], te_c["is_champion"].astype(int).values

    for variant in ["raw", "sigmoid", "isotonic"]:
        metrics, p = evaluate_champion_variant(variant, Xc_tr, yc_tr, Xc_te, yc_te, te_c)
        rows.append(metrics)
        stability_frames.append(champion_stability_by_season(te_c, p, variant))

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_RESULTS, index=False)

    stab_df = pd.concat(stability_frames, ignore_index=True)
    stab_df.to_csv(OUT_STABILITY, index=False)

    OUT_SUMMARY_MD.write_text(build_summary_md(out_df), encoding="utf-8")

    print(f"Wrote {OUT_RESULTS}")
    print(f"Wrote {OUT_STABILITY}")
    print(f"Wrote {OUT_SUMMARY_MD}")


if __name__ == "__main__":
    main()
