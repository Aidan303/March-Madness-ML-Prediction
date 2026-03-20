from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = ROOT / "Good_Data" / "Master Data" / "Master Data Variable Analysis Files"
MASTER_PATH = ROOT / "Good_Data" / "Master Data" / "Master CSV File and Support Files" / "master_features_all_teams_historical.csv"
SCORECARD_PATH = ANALYSIS_DIR / "feature_usefulness_scorecard_results.csv"

OUT_MANIFEST = OUTPUT_DIR / "locked_feature_sets_manifest.csv"
OUT_CORE = OUTPUT_DIR / "locked_feature_set_core.csv"
OUT_EXTENDED = OUTPUT_DIR / "locked_feature_set_extended.csv"
OUT_EXPERIMENTAL = OUTPUT_DIR / "locked_feature_set_experimental.csv"
OUT_SUMMARY = OUTPUT_DIR / "locked_feature_sets_summary.md"

ABS_CORR_STRICT = 0.90
ABS_CORR_LENIENT = 0.97


def nanmean_safe(values):
    values = np.array(values, dtype=float)
    if np.all(np.isnan(values)):
        return np.nan
    return float(np.nanmean(values))


def calc_rank_score(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()

    work["avg_perm_pctile"] = work[
        [
            "target_game_perm_importance_pctile",
            "target_champ_perm_importance_pctile",
            "target_roundflags_perm_importance_pctile",
        ]
    ].mean(axis=1, skipna=True)

    work["max_univ_auc"] = work[
        ["target_game_univ_auc", "target_champ_univ_auc", "target_roundflags_auc_avg"]
    ].max(axis=1, skipna=True)

    work["sign_stability"] = work[
        ["target_game_sign_stability_pct", "target_champ_sign_stability_pct"]
    ].max(axis=1, skipna=True)

    # Composite score for tie-breaking and redundancy representative selection.
    # Weighted toward predictive importance first.
    work["rank_score"] = (
        0.55 * (work["avg_perm_pctile"].fillna(0) / 100.0)
        + 0.30 * work["max_univ_auc"].fillna(0)
        + 0.15 * (work["sign_stability"].fillna(50) / 100.0)
    )

    return work


def correlation_prune(master_df: pd.DataFrame, features: list[str], score_map: dict[str, float], threshold: float):
    if not features:
        return [], {}, []

    numeric = master_df[features].apply(pd.to_numeric, errors="coerce")
    corr = numeric.corr().abs()

    ordered = sorted(features, key=lambda f: score_map.get(f, 0), reverse=True)
    kept = []
    dropped_by = {}

    for f in ordered:
        redundant = False
        for k in kept:
            c = corr.loc[f, k] if (f in corr.index and k in corr.columns) else np.nan
            if pd.notna(c) and c >= threshold:
                redundant = True
                dropped_by[f] = (k, float(c))
                break
        if not redundant:
            kept.append(f)

    dropped = [f for f in ordered if f not in kept]
    return kept, dropped_by, dropped


def write_set(path: Path, set_name: str, features: list[str]):
    pd.DataFrame({"set_name": set_name, "feature_name": features}).to_csv(path, index=False)


def main():
    scorecard = pd.read_csv(SCORECARD_PATH)
    master = pd.read_csv(MASTER_PATH)

    audited = scorecard[scorecard["include_for_audit"] == 1].copy()
    audited = calc_rank_score(audited)

    # Keep seed as a mandatory baseline feature in all locked sets.
    mandatory = {"tourney_seed_num"}

    # 1) Experimental set: all audited features (no pruning) for broad model exploration.
    experimental_set = sorted(audited["feature_name"].tolist())

    # 2) Extended set candidates: retain everything except low-value features,
    # then apply lenient redundancy pruning.
    ext_candidates = audited[
        (audited["overall_recommendation"] != "low_value") | (audited["feature_name"].isin(mandatory))
    ]["feature_name"].tolist()

    # 3) Core set candidates: strongest predictive features only before strict pruning.
    core_candidates = audited[
        (
            (audited["avg_perm_pctile"] >= 70)
            | (audited["max_univ_auc"] >= 0.75)
            | (audited["cutoff_multivariate_band"].isin(["core_level", "useful"]))
            | (audited["feature_name"].isin(mandatory))
        )
        & ((audited["overall_recommendation"] != "low_value") | (audited["feature_name"].isin(mandatory)))
    ]["feature_name"].tolist()

    score_map = dict(zip(audited["feature_name"], audited["rank_score"]))

    core_kept, core_dropped_by, _ = correlation_prune(master, core_candidates, score_map, ABS_CORR_STRICT)
    ext_kept, ext_dropped_by, _ = correlation_prune(master, ext_candidates, score_map, ABS_CORR_LENIENT)

    # Enforce mandatory features.
    for m in mandatory:
        if m in experimental_set and m not in core_kept:
            core_kept.append(m)
        if m in experimental_set and m not in ext_kept:
            ext_kept.append(m)

    core_set = sorted(set(core_kept))
    extended_set = sorted(set(ext_kept))

    # Guarantee hierarchy: core subset of extended subset of experimental.
    extended_set = sorted(set(extended_set).union(core_set))
    experimental_set = sorted(set(experimental_set).union(extended_set))

    # Write set files.
    write_set(OUT_CORE, "core", core_set)
    write_set(OUT_EXTENDED, "extended", extended_set)
    write_set(OUT_EXPERIMENTAL, "experimental", experimental_set)

    # Build manifest with assignment and reason notes.
    membership = []
    for f in experimental_set:
        in_core = int(f in core_set)
        in_extended = int(f in extended_set)
        in_experimental = 1

        note = ""
        if f in core_dropped_by:
            k, c = core_dropped_by[f]
            note = f"Dropped from core due to high correlation with {k} (|r|={c:.3f})"
        elif f in ext_dropped_by:
            k, c = ext_dropped_by[f]
            note = f"Dropped from extended due to near-duplicate with {k} (|r|={c:.3f})"

        membership.append(
            {
                "feature_name": f,
                "in_core": in_core,
                "in_extended": in_extended,
                "in_experimental": in_experimental,
                "note": note,
            }
        )

    manifest = pd.DataFrame(membership).sort_values(["in_core", "in_extended", "feature_name"], ascending=[False, False, True])
    manifest.to_csv(OUT_MANIFEST, index=False)

    # Build human summary markdown.
    lines = []
    lines.append("# Locked Feature Sets\n")
    lines.append("These sets are frozen outputs from the current scorecard and are intended for model training/testing experiments.\n")
    lines.append("## Lock Rules Used\n")
    lines.append(f"- Core: strong predictors with strict redundancy pruning at |r| >= {ABS_CORR_STRICT:.2f}\n")
    lines.append(f"- Extended: non-low-value predictors with lenient redundancy pruning at |r| >= {ABS_CORR_LENIENT:.2f}\n")
    lines.append("- Experimental: all audited predictors (no pruning)\n")
    lines.append("- Mandatory in all sets: tourney_seed_num\n")
    lines.append("\n## Counts\n")
    lines.append(f"- Core features: {len(core_set)}\n")
    lines.append(f"- Extended features: {len(extended_set)}\n")
    lines.append(f"- Experimental features: {len(experimental_set)}\n")

    top_core = audited[audited["feature_name"].isin(core_set)].sort_values("rank_score", ascending=False).head(20)
    lines.append("\n## Top Core Features (by rank_score)\n")
    for _, r in top_core.iterrows():
        lines.append(
            f"- {r['feature_name']} (group={r['feature_group']}, avg_perm={r['avg_perm_pctile']:.1f}, max_auc={r['max_univ_auc']:.3f})\n"
        )

    OUT_SUMMARY.write_text("".join(lines), encoding="utf-8")

    print("Locked feature sets written:")
    print(f"  {OUT_CORE}")
    print(f"  {OUT_EXTENDED}")
    print(f"  {OUT_EXPERIMENTAL}")
    print(f"  {OUT_MANIFEST}")
    print(f"  {OUT_SUMMARY}")
    print(f"Counts: core={len(core_set)}, extended={len(extended_set)}, experimental={len(experimental_set)}")


if __name__ == "__main__":
    main()
