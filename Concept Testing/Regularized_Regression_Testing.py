from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm


DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "Data" / "College_Team_Stats.csv"
)
DEFAULT_TARGET_COLUMN = "Overall W-L%"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
DIRECT_RECORD_FEATURES = {"Overall W", "Overall L", "Overall G"}


def load_and_prepare_data(
    csv_path: Path,
    target_column: str,
    exclude_record_features: bool,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, list[str]]:
    raw_df = pd.read_csv(csv_path)
    raw_df.columns = [str(col).strip() for col in raw_df.columns]
    raw_df = raw_df.dropna(axis=1, how="all")

    if target_column not in raw_df.columns:
        raise ValueError(f"Target column '{target_column}' not found in CSV.")

    id_like_columns = {"Rk", "School", target_column}

    numeric_df = raw_df.apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(raw_df[target_column], errors="coerce")

    candidate_columns = [
        col
        for col in numeric_df.columns
        if col not in id_like_columns and numeric_df[col].notna().any()
    ]

    dropped_columns: list[str] = []
    if exclude_record_features:
        dropped_columns = [col for col in candidate_columns if col in DIRECT_RECORD_FEATURES]
        candidate_columns = [col for col in candidate_columns if col not in DIRECT_RECORD_FEATURES]

    X = numeric_df[candidate_columns].copy()
    return raw_df, X, y, dropped_columns


def fit_ols_coefficients(X: pd.DataFrame, y: pd.Series) -> pd.Series:
    X_design = sm.add_constant(X, has_constant="add")
    model = sm.OLS(y, X_design).fit()
    return model.params.drop("const", errors="ignore")


def run_regularized_comparison(
    csv_path: Path,
    target_column: str,
    exclude_record_features: bool,
) -> None:
    raw_df, X_raw, y_raw, dropped_columns = load_and_prepare_data(
        csv_path,
        target_column,
        exclude_record_features=exclude_record_features,
    )

    print("=== Data Summary ===")
    print(f"Rows: {len(raw_df)}")
    print(f"Predictor count: {X_raw.shape[1]}")
    print(f"Target column: {target_column}")
    if dropped_columns:
        print(f"Dropped direct record predictors: {', '.join(dropped_columns)}")

    imputer = SimpleImputer(strategy="median")
    X_imputed = pd.DataFrame(imputer.fit_transform(X_raw), columns=X_raw.columns, index=X_raw.index)

    y = y_raw.fillna(y_raw.median())

    variances = X_imputed.var(ddof=0)
    keep_columns = variances[variances > 0].index.tolist()
    X_model = X_imputed[keep_columns]

    # OLS baseline coefficients for stability comparison.
    ols_coefs = fit_ols_coefficients(X_model, y)

    ridge_alphas = np.logspace(-3, 4, 60)
    ridge_pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("ridge", RidgeCV(alphas=ridge_alphas, cv=5)),
        ]
    )
    ridge_pipe.fit(X_model, y)
    ridge_model = ridge_pipe.named_steps["ridge"]
    ridge_coefs = pd.Series(ridge_model.coef_, index=X_model.columns, name="ridge_coef")

    lasso_alphas = np.logspace(-4, 1, 80)
    lasso_pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "lasso",
                LassoCV(alphas=lasso_alphas, cv=5, random_state=42, max_iter=20000),
            ),
        ]
    )
    lasso_pipe.fit(X_model, y)
    lasso_model = lasso_pipe.named_steps["lasso"]
    lasso_coefs = pd.Series(lasso_model.coef_, index=X_model.columns, name="lasso_coef")

    comparison_df = pd.DataFrame(
        {
            "feature": X_model.columns,
            "ols_coef": ols_coefs.reindex(X_model.columns).values,
            "ridge_coef": ridge_coefs.reindex(X_model.columns).values,
            "lasso_coef": lasso_coefs.reindex(X_model.columns).values,
        }
    )
    comparison_df["abs_ols_coef"] = comparison_df["ols_coef"].abs()
    comparison_df["abs_ridge_coef"] = comparison_df["ridge_coef"].abs()
    comparison_df["abs_lasso_coef"] = comparison_df["lasso_coef"].abs()
    comparison_df["ridge_vs_ols_abs_ratio"] = comparison_df["abs_ridge_coef"] / comparison_df["abs_ols_coef"].replace(0, np.nan)
    comparison_df["lasso_zeroed"] = (comparison_df["lasso_coef"].abs() < 1e-9).astype(int)

    nonzero_lasso = int((comparison_df["lasso_coef"].abs() >= 1e-9).sum())

    print("\n=== Regularization Summary ===")
    print(f"Ridge selected alpha: {ridge_model.alpha_:.6g}")
    print(f"Lasso selected alpha: {lasso_model.alpha_:.6g}")
    print(f"Lasso non-zero coefficients: {nonzero_lasso}/{len(comparison_df)}")

    print("\nTop 15 by |Ridge coefficient|:")
    print(
        comparison_df.sort_values("abs_ridge_coef", ascending=False)[
            ["feature", "ols_coef", "ridge_coef", "lasso_coef", "lasso_zeroed"]
        ]
        .head(15)
        .to_string(index=False)
    )

    print("\nTop 15 by |Lasso coefficient|:")
    print(
        comparison_df.sort_values("abs_lasso_coef", ascending=False)[
            ["feature", "ols_coef", "ridge_coef", "lasso_coef", "lasso_zeroed"]
        ]
        .head(15)
        .to_string(index=False)
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "_no_record_vars" if exclude_record_features else ""
    output_path = OUTPUT_DIR / f"regularized_vs_ols_coefficients{suffix}.csv"
    comparison_df.sort_values("abs_ridge_coef", ascending=False).to_csv(output_path, index=False)

    print("\nSaved output:")
    print(f"- {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare OLS, Ridge, and Lasso coefficients for stability under multicollinearity."
    )
    parser.add_argument(
        "--csv-path",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to the team stats CSV.",
    )
    parser.add_argument(
        "--target-column",
        type=str,
        default=DEFAULT_TARGET_COLUMN,
        help="Target column for regression.",
    )
    parser.add_argument(
        "--exclude-record-features",
        action="store_true",
        help="Exclude direct record features (Overall W, Overall L, Overall G).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_regularized_comparison(
        args.csv_path,
        args.target_column,
        exclude_record_features=args.exclude_record_features,
    )
