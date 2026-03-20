from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RUN_RESULTS = ROOT / "Model Creation" / "Results" / "Model Creation" / "step3_run_results.csv"


def rank_bracket(df: pd.DataFrame) -> pd.DataFrame:
    # Priority: log loss asc, AUC desc, upset acc desc
    out = df.sort_values(
        by=["test_log_loss", "test_auc", "upset_acc_seedgap_ge_5"],
        ascending=[True, False, False],
    ).reset_index(drop=True)
    return out


def rank_champion(df: pd.DataFrame) -> pd.DataFrame:
    # Priority: champion log loss asc, top4 desc, top1 desc
    out = df.sort_values(
        by=["test_log_loss", "champ_top4_rate", "champ_top1_rate"],
        ascending=[True, False, False],
    ).reset_index(drop=True)
    return out


def main() -> None:
    df = pd.read_csv(RUN_RESULTS)
    df["selected_for_next_stage"] = df["selected_for_next_stage"].astype("object")

    base_brk = df[df["run_id"].isin(["BRK_BASE_CORE", "BRK_BASE_EXT", "BRK_BASE_EXP"])].copy()
    base_chp = df[df["run_id"].isin(["CHAMP_BASE_CORE", "CHAMP_BASE_EXT", "CHAMP_BASE_EXP"])].copy()

    rb = rank_bracket(base_brk)
    rc = rank_champion(base_chp)

    top2_brk = rb.head(2)["feature_set"].tolist()
    top2_chp = rc.head(2)["feature_set"].tolist()

    # Mark selected_for_next_stage for baselines
    baseline_ids = set(base_brk["run_id"]).union(set(base_chp["run_id"]))
    for rid in baseline_ids:
        df.loc[df["run_id"] == rid, "selected_for_next_stage"] = "no"

    df.loc[df["run_id"].isin(rb.head(2)["run_id"].tolist()), "selected_for_next_stage"] = "yes"
    df.loc[df["run_id"].isin(rc.head(2)["run_id"].tolist()), "selected_for_next_stage"] = "yes"

    # Populate tree-stage feature sets and clear previous metrics for those rows
    df.loc[df["run_id"] == "BRK_TREE_SET1", "feature_set"] = top2_brk[0]
    df.loc[df["run_id"] == "BRK_TREE_SET2", "feature_set"] = top2_brk[1]
    df.loc[df["run_id"] == "CHAMP_TREE_SET1", "feature_set"] = top2_chp[0]
    df.loc[df["run_id"] == "CHAMP_TREE_SET2", "feature_set"] = top2_chp[1]

    for rid in ["BRK_TREE_SET1", "BRK_TREE_SET2", "CHAMP_TREE_SET1", "CHAMP_TREE_SET2"]:
        df.loc[df["run_id"] == rid, "selected_for_next_stage"] = "pending"
        for c in [
            "test_log_loss",
            "test_auc",
            "upset_acc_seedgap_ge_5",
            "champ_top1_rate",
            "champ_top4_rate",
            "notes",
        ]:
            df.loc[df["run_id"] == rid, c] = pd.NA

    df.to_csv(RUN_RESULTS, index=False)

    print("Selected top-2 feature sets for tree stage:")
    print(f"  Bracket:  {top2_brk}")
    print(f"  Champion: {top2_chp}")


if __name__ == "__main__":
    main()
