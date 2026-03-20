import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.inspection import permutation_importance
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[3]


def resolve_unique_file(filename: str) -> Path:
    matches = list((ROOT / "Good_Data").rglob(filename))
    if not matches:
        raise FileNotFoundError(f"Could not find required file: {filename}")
    matches = sorted(matches, key=lambda p: (len(p.parts), str(p)))
    return matches[0]


MASTER_PATH = resolve_unique_file("master_features_all_teams_historical.csv")
TEMPLATE_PATH = resolve_unique_file("feature_usefulness_scorecard_template.csv")
RESULTS_DIR = TEMPLATE_PATH.parent
OUT_PATH = RESULTS_DIR / "feature_usefulness_scorecard_results.csv"
SUMMARY_PATH = RESULTS_DIR / "feature_usefulness_analysis_summary.csv"


def find_kaggle_dir() -> Path:
    candidates = [
        ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data",
        ROOT / "Good_Data" / "march-machine-learning-mania-2026",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("Could not find Kaggle base data directory under Good_Data.")


KAGGLE_DIR = find_kaggle_dir()
TOURNEY_RESULTS_PATH = KAGGLE_DIR / "MNCAATourneyCompactResults.csv"
SEEDS_PATH = KAGGLE_DIR / "MNCAATourneySeeds.csv"

ID_COLS = ["Season", "TeamID", "TeamName", "ConfAbbrev", "is_tourney_team"]
FEATURE_EXCLUDE = set(ID_COLS)
ROUND_TARGETS = [
    "reached_sweet16",
    "reached_elite8",
    "reached_final4",
    "reached_title_game",
]


# Round-day thresholds are stable in modern NCAA data and sufficient for pre-model audit flags.
ROUND_DAY_THRESHOLDS = {
    "reached_sweet16": 143,
    "reached_elite8": 145,
    "reached_final4": 152,
    "reached_title_game": 154,
}


def oriented_auc(y_true, x):
    try:
        auc = roc_auc_score(y_true, x)
        return max(auc, 1.0 - auc)
    except Exception:
        return np.nan


def one_feature_cv_logloss_lift(x, y, n_splits=5, seed=42):
    mask = (~pd.isna(x)) & (~pd.isna(y))
    x = np.asarray(x[mask], dtype=float)
    y = np.asarray(y[mask], dtype=int)

    if len(np.unique(y)) < 2 or len(y) < 50:
        return np.nan

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    ll_model = []
    ll_base = []

    for tr_idx, te_idx in skf.split(x.reshape(-1, 1), y):
        x_tr, x_te = x[tr_idx].reshape(-1, 1), x[te_idx].reshape(-1, 1)
        y_tr, y_te = y[tr_idx], y[te_idx]

        model = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "clf",
                LogisticRegression(
                    penalty="l2",
                    solver="liblinear",
                    max_iter=2000,
                ),
            ),
        ])
        model.fit(x_tr, y_tr)
        p_model = model.predict_proba(x_te)[:, 1]

        base_p = np.full_like(y_te, y_tr.mean(), dtype=float)

        ll_model.append(log_loss(y_te, p_model, labels=[0, 1]))
        ll_base.append(log_loss(y_te, base_p, labels=[0, 1]))

    m = float(np.mean(ll_model))
    b = float(np.mean(ll_base))
    if b <= 0:
        return np.nan
    return (b - m) / b * 100.0


def one_feature_logit_stats(x, y):
    mask = (~pd.isna(x)) & (~pd.isna(y))
    x = np.asarray(x[mask], dtype=float)
    y = np.asarray(y[mask], dtype=int)

    if len(np.unique(y)) < 2 or len(y) < 50:
        return np.nan, np.nan, np.nan

    std = np.std(x)
    if std < 1e-10:
        return np.nan, np.nan, np.nan

    xz = (x - np.mean(x)) / std
    X = sm.add_constant(xz)

    try:
        res = sm.Logit(y, X).fit(disp=False)
        coef = float(res.params[1])
        pval = float(res.pvalues[1])
        odds_ratio = float(np.exp(coef))
        return coef, pval, odds_ratio
    except Exception:
        return np.nan, np.nan, np.nan


def univariate_scan(df, feature_cols, target_col):
    rows = []
    y = df[target_col]
    for f in feature_cols:
        x = df[f]
        auc = oriented_auc(y, x)
        ll_lift = one_feature_cv_logloss_lift(x, y)
        coef, pval, odds = one_feature_logit_stats(x, y)
        rows.append(
            {
                "feature_name": f,
                "auc": auc,
                "logloss_lift_pct": ll_lift,
                "coef_std": coef,
                "p": pval,
                "odds_ratio": odds,
            }
        )

    out = pd.DataFrame(rows)
    mask = out["p"].notna()
    out["q_fdr"] = np.nan
    if mask.sum() > 0:
        _, qvals, _, _ = multipletests(out.loc[mask, "p"], alpha=0.05, method="fdr_bh")
        out.loc[mask, "q_fdr"] = qvals
    return out


def build_temporal_folds(seasons, n_folds=5, min_train=8):
    s = np.array(sorted(pd.Series(seasons).dropna().astype(int).unique()))
    if len(s) <= min_train + 1:
        return []

    test_seasons = s[min_train:]
    chunks = [c for c in np.array_split(test_seasons, n_folds) if len(c) > 0]

    folds = []
    for chunk in chunks:
        test_start = int(chunk[0])
        tr = s[s < test_start]
        te = chunk
        if len(tr) == 0 or len(te) == 0:
            continue
        folds.append((set(tr.tolist()), set(te.tolist())))
    return folds


def get_model():
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "clf",
                LogisticRegression(
                    penalty="elasticnet",
                    solver="saga",
                    l1_ratio=0.5,
                    C=0.5,
                    max_iter=5000,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def multivariate_scan(df, feature_cols, target_col, season_col="Season", do_ablation=True):
    work = df[[season_col, target_col] + feature_cols].copy()
    work = work.dropna(subset=[target_col])

    folds = build_temporal_folds(work[season_col].values, n_folds=5, min_train=8)
    if not folds:
        return pd.DataFrame({"feature_name": feature_cols})

    coef_store = {f: [] for f in feature_cols}
    perm_store = {f: [] for f in feature_cols}
    ablation_store = {f: [] for f in feature_cols}

    full_ll = []
    base_ll = []

    for train_seasons, test_seasons in folds:
        tr = work[work[season_col].isin(train_seasons)]
        te = work[work[season_col].isin(test_seasons)]

        y_tr = tr[target_col].astype(int).values
        y_te = te[target_col].astype(int).values

        if len(np.unique(y_tr)) < 2 or len(np.unique(y_te)) < 2:
            continue

        X_tr = tr[feature_cols]
        X_te = te[feature_cols]

        model = get_model()
        model.fit(X_tr, y_tr)
        p = model.predict_proba(X_te)[:, 1]

        ll_full = log_loss(y_te, p, labels=[0, 1])
        ll_base = log_loss(y_te, np.full_like(y_te, y_tr.mean(), dtype=float), labels=[0, 1])
        full_ll.append(ll_full)
        base_ll.append(ll_base)

        coefs = model.named_steps["clf"].coef_[0]
        for i, f in enumerate(feature_cols):
            coef_store[f].append(float(coefs[i]))

        try:
            pi = permutation_importance(
                model,
                X_te,
                y_te,
                scoring="neg_log_loss",
                n_repeats=5,
                random_state=42,
                n_jobs=-1,
            )
            for i, f in enumerate(feature_cols):
                perm_store[f].append(float(pi.importances_mean[i]))
        except Exception:
            pass

        if do_ablation:
            for f in feature_cols:
                reduced = [c for c in feature_cols if c != f]
                model_r = get_model()
                model_r.fit(tr[reduced], y_tr)
                p_r = model_r.predict_proba(te[reduced])[:, 1]
                ll_r = log_loss(y_te, p_r, labels=[0, 1])
                delta_pct = (ll_r - ll_full) / max(ll_full, 1e-9) * 100.0
                ablation_store[f].append(float(delta_pct))

    out_rows = []
    for f in feature_cols:
        coefs = np.array(coef_store[f], dtype=float)
        perms = np.array(perm_store[f], dtype=float)
        abls = np.array(ablation_store[f], dtype=float)

        coef_mean = np.nan if coefs.size == 0 else float(np.nanmean(coefs))
        if coefs.size == 0:
            sign_stability = np.nan
        else:
            pos = np.mean(coefs > 0)
            neg = np.mean(coefs < 0)
            sign_stability = float(max(pos, neg) * 100.0)

        perm_mean = np.nan if perms.size == 0 else float(np.nanmean(perms))
        abl_mean = np.nan if abls.size == 0 else float(np.nanmean(abls))

        out_rows.append(
            {
                "feature_name": f,
                "multivar_coef_std": coef_mean,
                "sign_stability_pct": sign_stability,
                "perm_importance_raw": perm_mean,
                "ablation_logloss_delta_pct": abl_mean,
            }
        )

    out = pd.DataFrame(out_rows)

    # Percentile rank: higher raw importance = higher percentile.
    if out["perm_importance_raw"].notna().sum() > 0:
        ranks = out["perm_importance_raw"].rank(method="average", pct=True)
        out["perm_importance_pctile"] = ranks * 100.0
    else:
        out["perm_importance_pctile"] = np.nan

    # For now, SHAP percentile is left blank; can be added with tree SHAP later.
    out["shap_importance_pctile"] = np.nan

    if full_ll and base_ll:
        model_ll = float(np.mean(full_ll))
        base = float(np.mean(base_ll))
        ll_lift = (base - model_ll) / max(base, 1e-9) * 100.0
        print(f"  {target_col}: temporal multivariate log-loss lift = {ll_lift:.2f}%")

    return out


def significance_band(q):
    if pd.isna(q):
        return ""
    if q < 0.01:
        return "strong"
    if q < 0.05:
        return "moderate"
    if q < 0.10:
        return "weak"
    return "not_significant"


def univariate_band(auc, lift):
    if pd.isna(auc) or pd.isna(lift):
        return ""
    if auc >= 0.60 and lift >= 3.0:
        return "strong"
    if auc >= 0.56 and lift >= 1.0:
        return "moderate"
    if auc >= 0.53 and lift >= 0.25:
        return "weak"
    return "near_noise"


def multivariate_band(perm_pctile, ablation_delta):
    if pd.isna(perm_pctile) and pd.isna(ablation_delta):
        return ""
    p = -np.inf if pd.isna(perm_pctile) else perm_pctile
    a = -np.inf if pd.isna(ablation_delta) else ablation_delta
    if p >= 80 and a >= 0.75:
        return "core_level"
    if p >= 60 and a >= 0.30:
        return "useful"
    if p >= 40 and a >= 0.10:
        return "situational"
    return "low"


def stability_band(sign_stability, rank_std):
    if pd.isna(sign_stability) and pd.isna(rank_std):
        return ""
    if (not pd.isna(sign_stability) and sign_stability >= 80) and (
        not pd.isna(rank_std) and rank_std <= 15
    ):
        return "stable"
    if (
        (not pd.isna(sign_stability) and 65 <= sign_stability < 80)
        or (not pd.isna(rank_std) and 16 <= rank_std <= 25)
    ):
        return "mostly_stable"
    return "unstable"


def recommendation(sig_band, uni_band, multi_band, stab_band):
    if multi_band == "core_level" and stab_band == "stable":
        return "core", "High contribution and stable over time"
    if multi_band in {"core_level", "useful"} and stab_band == "unstable":
        return "strong_but_unstable", "Strong predictive impact with unstable fold behavior"
    if multi_band == "situational" or uni_band in {"strong", "moderate"}:
        return "situational", "Useful but target-specific or context-dependent"
    if sig_band == "not_significant" and multi_band == "low":
        return "low_value", "Low signal across statistical and predictive checks"
    return "situational", "Mixed evidence; keep for now pending pruning phase"


def main():
    print("Loading master data and scorecard template...")
    master = pd.read_csv(MASTER_PATH)
    scorecard = pd.read_csv(TEMPLATE_PATH)

    feature_cols = [c for c in master.columns if c not in FEATURE_EXCLUDE]
    for col in ["tourney_seed_num"]:
        if col in master.columns and col not in feature_cols:
            feature_cols.append(col)

    # Mark identifiers as not audited, keep all real features for analysis.
    scorecard["include_for_audit"] = scorecard["feature_name"].isin(feature_cols).astype(int)

    print("Building tournament labels (champion + round flags)...")
    tourney = pd.read_csv(TOURNEY_RESULTS_PATH)
    seeds = pd.read_csv(SEEDS_PATH)

    # Champion by season = winner of latest-day game.
    last_games = tourney.sort_values(["Season", "DayNum"]).groupby("Season").tail(1)
    champion_map = dict(zip(last_games["Season"], last_games["WTeamID"]))

    # Long team-game table to derive round reached using max day played.
    w = tourney[["Season", "DayNum", "WTeamID"]].rename(columns={"WTeamID": "TeamID"})
    l = tourney[["Season", "DayNum", "LTeamID"]].rename(columns={"LTeamID": "TeamID"})
    tg = pd.concat([w, l], ignore_index=True)
    max_day = tg.groupby(["Season", "TeamID"])["DayNum"].max().reset_index(name="max_day")

    teams_t = master[master["is_tourney_team"] == 1].copy()
    teams_t = teams_t.merge(max_day, on=["Season", "TeamID"], how="left")

    for flag, day_thr in ROUND_DAY_THRESHOLDS.items():
        teams_t[flag] = (teams_t["max_day"] >= day_thr).astype(int)

    teams_t["is_champion"] = (
        teams_t.apply(lambda r: int(champion_map.get(r["Season"], -1) == r["TeamID"]), axis=1)
    )

    # Ensure logical consistency.
    teams_t.loc[teams_t["is_champion"] == 1, "reached_title_game"] = 1
    teams_t = teams_t.drop(columns=["max_day"])

    print("Building matchup-level game winner table...")
    seasons_keep = set(master["Season"].unique())
    games = tourney[tourney["Season"].isin(seasons_keep)].copy()

    a = games[["Season", "WTeamID", "LTeamID"]].rename(
        columns={"WTeamID": "TeamA", "LTeamID": "TeamB"}
    )
    b = games[["Season", "LTeamID", "WTeamID"]].rename(
        columns={"LTeamID": "TeamA", "WTeamID": "TeamB"}
    )

    a["target_game_win"] = 1
    b["target_game_win"] = 0
    matchup = pd.concat([a, b], ignore_index=True)

    left = master[["Season", "TeamID"] + feature_cols].copy()
    right = master[["Season", "TeamID"] + feature_cols].copy()

    left_cols = {c: f"A_{c}" for c in feature_cols}
    right_cols = {c: f"B_{c}" for c in feature_cols}

    matchup = matchup.merge(
        left.rename(columns={"TeamID": "TeamA", **left_cols}),
        on=["Season", "TeamA"],
        how="left",
    )
    matchup = matchup.merge(
        right.rename(columns={"TeamID": "TeamB", **right_cols}),
        on=["Season", "TeamB"],
        how="left",
    )

    game_df = matchup[["Season", "target_game_win"]].copy()
    for f in feature_cols:
        game_df[f] = matchup[f"A_{f}"] - matchup[f"B_{f}"]

    print("Running univariate scans...")
    univ_game = univariate_scan(game_df, feature_cols, "target_game_win")
    univ_champ = univariate_scan(teams_t, feature_cols, "is_champion")

    # Round flags: average univariate AUC across round targets.
    round_auc = pd.DataFrame({"feature_name": feature_cols})
    auc_cols = []
    for rt in ROUND_TARGETS:
        if teams_t[rt].nunique() < 2:
            continue
        u = univariate_scan(teams_t, feature_cols, rt)[["feature_name", "auc"]].rename(
            columns={"auc": f"auc_{rt}"}
        )
        round_auc = round_auc.merge(u, on="feature_name", how="left")
        auc_cols.append(f"auc_{rt}")

    if auc_cols:
        round_auc["target_roundflags_auc_avg"] = round_auc[auc_cols].mean(axis=1)
    else:
        round_auc["target_roundflags_auc_avg"] = np.nan

    print("Running multivariate scans (temporal folds)...")
    mult_game = multivariate_scan(game_df, feature_cols, "target_game_win", do_ablation=True)
    mult_champ = multivariate_scan(teams_t, feature_cols, "is_champion", do_ablation=True)

    # Round flag multivariate: importance only (no ablation to keep runtime practical).
    round_perm_tables = []
    for rt in ROUND_TARGETS:
        if teams_t[rt].nunique() < 2:
            continue
        print(f"  Round target: {rt}")
        mt = multivariate_scan(teams_t, feature_cols, rt, do_ablation=False)
        mt = mt[["feature_name", "perm_importance_pctile"]].rename(
            columns={"perm_importance_pctile": f"perm_pctile_{rt}"}
        )
        round_perm_tables.append(mt)

    round_perm = pd.DataFrame({"feature_name": feature_cols})
    for t in round_perm_tables:
        round_perm = round_perm.merge(t, on="feature_name", how="left")

    rp_cols = [c for c in round_perm.columns if c.startswith("perm_pctile_")]
    if rp_cols:
        round_perm["target_roundflags_perm_importance_pctile"] = round_perm[rp_cols].mean(axis=1)
    else:
        round_perm["target_roundflags_perm_importance_pctile"] = np.nan

    print("Merging all metrics into scorecard...")
    sc = scorecard.copy()

    def assign_by_feature(sc_df, source_df, source_col, target_col):
        if source_col not in source_df.columns:
            return
        mapping = dict(zip(source_df["feature_name"], source_df[source_col]))
        sc_df[target_col] = sc_df["feature_name"].map(mapping)

    # Univariate game
    assign_by_feature(sc, univ_game, "auc", "target_game_univ_auc")
    assign_by_feature(sc, univ_game, "logloss_lift_pct", "target_game_univ_logloss_lift_pct")
    assign_by_feature(sc, univ_game, "p", "target_game_univ_p")
    assign_by_feature(sc, univ_game, "q_fdr", "target_game_univ_q_fdr")
    assign_by_feature(sc, univ_game, "odds_ratio", "target_game_univ_odds_ratio")

    # Univariate champion
    assign_by_feature(sc, univ_champ, "auc", "target_champ_univ_auc")
    assign_by_feature(sc, univ_champ, "logloss_lift_pct", "target_champ_univ_logloss_lift_pct")
    assign_by_feature(sc, univ_champ, "p", "target_champ_univ_p")
    assign_by_feature(sc, univ_champ, "q_fdr", "target_champ_univ_q_fdr")
    assign_by_feature(sc, univ_champ, "odds_ratio", "target_champ_univ_odds_ratio")

    # Multivariate game
    assign_by_feature(sc, mult_game, "multivar_coef_std", "target_game_multivar_coef_std")
    assign_by_feature(sc, mult_game, "sign_stability_pct", "target_game_sign_stability_pct")
    assign_by_feature(sc, mult_game, "perm_importance_pctile", "target_game_perm_importance_pctile")
    assign_by_feature(sc, mult_game, "shap_importance_pctile", "target_game_shap_importance_pctile")
    assign_by_feature(sc, mult_game, "ablation_logloss_delta_pct", "target_game_ablation_logloss_delta_pct")

    # Multivariate champion
    assign_by_feature(sc, mult_champ, "multivar_coef_std", "target_champ_multivar_coef_std")
    assign_by_feature(sc, mult_champ, "sign_stability_pct", "target_champ_sign_stability_pct")
    assign_by_feature(sc, mult_champ, "perm_importance_pctile", "target_champ_perm_importance_pctile")
    assign_by_feature(sc, mult_champ, "shap_importance_pctile", "target_champ_shap_importance_pctile")
    assign_by_feature(sc, mult_champ, "ablation_logloss_delta_pct", "target_champ_ablation_logloss_delta_pct")

    # Round aggregates
    assign_by_feature(sc, round_auc, "target_roundflags_auc_avg", "target_roundflags_auc_avg")
    assign_by_feature(
        sc,
        round_perm,
        "target_roundflags_perm_importance_pctile",
        "target_roundflags_perm_importance_pctile",
    )

    # Fill cutoff bands + recommendation
    sig_q = sc[["target_game_univ_q_fdr", "target_champ_univ_q_fdr"]].min(axis=1, skipna=True)

    uni_auc = sc[["target_game_univ_auc", "target_champ_univ_auc"]].max(axis=1, skipna=True)
    uni_lift = sc[
        [
            "target_game_univ_logloss_lift_pct",
            "target_champ_univ_logloss_lift_pct",
        ]
    ].max(axis=1, skipna=True)

    multi_perm = sc[
        [
            "target_game_perm_importance_pctile",
            "target_champ_perm_importance_pctile",
            "target_roundflags_perm_importance_pctile",
        ]
    ].max(axis=1, skipna=True)

    multi_ablation = sc[
        [
            "target_game_ablation_logloss_delta_pct",
            "target_champ_ablation_logloss_delta_pct",
        ]
    ].max(axis=1, skipna=True)

    sign_stab = sc[
        ["target_game_sign_stability_pct", "target_champ_sign_stability_pct"]
    ].max(axis=1, skipna=True)

    # Rank stability as std across target importance percentiles.
    sc["importance_rank_stability_std"] = sc[
        [
            "target_game_perm_importance_pctile",
            "target_champ_perm_importance_pctile",
            "target_roundflags_perm_importance_pctile",
        ]
    ].std(axis=1, skipna=True)

    sc["cutoff_significance_band"] = [significance_band(v) for v in sig_q]
    sc["cutoff_univariate_band"] = [univariate_band(a, l) for a, l in zip(uni_auc, uni_lift)]
    sc["cutoff_multivariate_band"] = [
        multivariate_band(p, a) for p, a in zip(multi_perm, multi_ablation)
    ]
    sc["cutoff_stability_band"] = [
        stability_band(s, r) for s, r in zip(sign_stab, sc["importance_rank_stability_std"])
    ]

    recs = [
        recommendation(s, u, m, st)
        for s, u, m, st in zip(
            sc["cutoff_significance_band"],
            sc["cutoff_univariate_band"],
            sc["cutoff_multivariate_band"],
            sc["cutoff_stability_band"],
        )
    ]
    sc["overall_recommendation"] = [r[0] for r in recs]
    sc["recommendation_reason"] = [r[1] for r in recs]

    # Keep identifiers out of recommendation logic.
    id_mask = sc["include_for_audit"] == 0
    for col in [
        "cutoff_significance_band",
        "cutoff_univariate_band",
        "cutoff_multivariate_band",
        "cutoff_stability_band",
        "overall_recommendation",
        "recommendation_reason",
    ]:
        sc.loc[id_mask, col] = ""

    # Save detailed scorecard.
    sc.to_csv(OUT_PATH, index=False)

    # Save compact summary table for quick review.
    summary_cols = [
        "feature_name",
        "feature_group",
        "target_game_univ_auc",
        "target_champ_univ_auc",
        "target_roundflags_auc_avg",
        "target_game_perm_importance_pctile",
        "target_champ_perm_importance_pctile",
        "target_roundflags_perm_importance_pctile",
        "overall_recommendation",
    ]
    sc[summary_cols].sort_values(
        by=["target_game_perm_importance_pctile", "target_champ_perm_importance_pctile"],
        ascending=False,
    ).to_csv(SUMMARY_PATH, index=False)

    print("Done.")
    print(f"  Scorecard results: {OUT_PATH}")
    print(f"  Compact summary:   {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
