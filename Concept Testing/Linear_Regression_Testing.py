from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.impute import SimpleImputer
from statsmodels.stats.outliers_influence import variance_inflation_factor


DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "Data" / "College_Team_Stats.csv"
)
DEFAULT_TARGET_COLUMN = "Overall W-L%"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
DIRECT_RECORD_FEATURES = {"Overall W", "Overall L", "Overall G"}


def infer_context_family(column_name: str) -> str:
    lower_name = column_name.lower().strip()
    if lower_name.startswith("overall "):
        return "overall"
    if lower_name.startswith("conf"):
        return "conf"
    if lower_name.startswith("home "):
        return "home"
    if lower_name.startswith("away "):
        return "away"
    return "season_total"


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
    if y.isna().all():
        raise ValueError(f"Target column '{target_column}' could not be parsed as numeric.")

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


def print_data_summary(raw_df: pd.DataFrame, X: pd.DataFrame, y: pd.Series, target_column: str) -> None:
    context_counts = {"overall": 0, "conf": 0, "home": 0, "away": 0, "season_total": 0}
    for col in X.columns:
        context_counts[infer_context_family(col)] += 1

    print("=== Data Summary ===")
    print(f"Rows: {len(raw_df)}")
    print(f"Columns (after dropping empty placeholders): {raw_df.shape[1]}")
    print(f"Target column: {target_column}")
    print(f"Target missing values: {int(y.isna().sum())}")
    print(f"Predictor count: {X.shape[1]}")
    print("Predictor context coverage:")
    for family, count in context_counts.items():
        print(f"  - {family}: {count}")


def compute_vif_table(X: pd.DataFrame) -> pd.DataFrame:
    X_const = sm.add_constant(X, has_constant="add")
    vif_rows = []
    for i, col in enumerate(X_const.columns):
        if col == "const":
            continue
        vif_rows.append(
            {
                "feature": col,
                "vif": variance_inflation_factor(X_const.values, i),
            }
        )
    vif_df = pd.DataFrame(vif_rows).sort_values("vif", ascending=False)
    return vif_df


def standardized_effect_sizes(model: sm.regression.linear_model.RegressionResultsWrapper, X: pd.DataFrame, y: pd.Series) -> pd.Series:
    y_std = y.std(ddof=0)
    if y_std == 0:
        return pd.Series(index=X.columns, data=np.nan)

    coeffs = model.params.drop("const", errors="ignore")
    x_std = X.std(ddof=0)
    return (coeffs * x_std / y_std).reindex(X.columns)


def run_ols_analysis(csv_path: Path, target_column: str, exclude_record_features: bool) -> None:
    raw_df, X_raw, y_raw, dropped_columns = load_and_prepare_data(
        csv_path,
        target_column,
        exclude_record_features=exclude_record_features,
    )
    print_data_summary(raw_df, X_raw, y_raw, target_column)
    if dropped_columns:
        print(f"Dropped direct record predictors: {', '.join(dropped_columns)}")

    imputer = SimpleImputer(strategy="median")
    X_imputed = pd.DataFrame(imputer.fit_transform(X_raw), columns=X_raw.columns, index=X_raw.index)

    y = y_raw.copy()
    y = y.fillna(y.median())

    # Remove zero-variance predictors to avoid singular matrix issues.
    variances = X_imputed.var(ddof=0)
    keep_columns = variances[variances > 0].index.tolist()
    dropped_zero_var = sorted(set(X_imputed.columns) - set(keep_columns))
    if dropped_zero_var:
        print(f"Dropped zero-variance predictors: {len(dropped_zero_var)}")
    X_model = X_imputed[keep_columns]

    X_design = sm.add_constant(X_model, has_constant="add")
    model = sm.OLS(y, X_design).fit()

    print("\n=== OLS Summary ===")
    print(model.summary())

    coef_table = model.summary2().tables[1].copy()
    coef_table = coef_table.rename(
        columns={
            "Coef.": "coef",
            "Std.Err.": "std_err",
            "t": "t_stat",
            "P>|t|": "p_value",
            "[0.025": "ci_lower",
            "0.975]": "ci_upper",
        }
    )

    std_effect = standardized_effect_sizes(model, X_model, y)
    coef_table["std_effect_size"] = np.nan
    for feature, value in std_effect.items():
        if feature in coef_table.index:
            coef_table.loc[feature, "std_effect_size"] = value

    ranked_significance = coef_table.drop(index="const", errors="ignore").copy()
    ranked_significance = ranked_significance.sort_values(["p_value", "std_effect_size"], ascending=[True, False])

    vif_df = compute_vif_table(X_model)

    print("\n=== Top Predictors By Significance (smallest p-value) ===")
    print(ranked_significance[["coef", "p_value", "std_effect_size"]].head(20).to_string())

    print("\n=== VIF (Top 20 Highest) ===")
    print(vif_df.head(20).to_string(index=False))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "_no_record_vars" if exclude_record_features else ""
    coef_output_path = OUTPUT_DIR / f"ols_coefficients_significance{suffix}.csv"
    vif_output_path = OUTPUT_DIR / f"ols_vif_table{suffix}.csv"

    coef_table.to_csv(coef_output_path)
    vif_df.to_csv(vif_output_path, index=False)

    print("\nSaved outputs:")
    print(f"- {coef_output_path}")
    print(f"- {vif_output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run OLS coefficient/significance exploration.")
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
    run_ols_analysis(
        args.csv_path,
        args.target_column,
        exclude_record_features=args.exclude_record_features,
    )
