# March Madness Exploratory Modeling Findings

Date: 2026-03-11
Dataset: `Data/College_Team_Stats.csv`
Scripts:
- `Concept Testing/Clustering_Testing.py`
- `Concept Testing/Linear_Regression_Testing.py`
- `Concept Testing/Regularized_Regression_Testing.py`

## 1. Scope And Objective
This iteration documents the comparison between the original baseline run and two implemented improvements:
1. Recommendation 3: regularized regression comparison (`Ridge` and `Lasso`) to improve coefficient stability under multicollinearity.
2. Recommendation 4: expanded density clustering search (data-adaptive DBSCAN grid) to better test non-spherical cluster structure.

All context groups remained included in this pass (`Overall`, `Conf.`, `Home`, `Away`, and unprefixed season totals).

## 2. Clustering Conclusions
### 2.1 Methods Compared
The updated clustering script evaluated:
1. KMeans across `k = 2..10`
2. DBSCAN across an expanded data-adaptive `eps` grid and broader `min_samples` set

### 2.2 Best Clustering Method
Best method in this updated run: `DBSCAN (eps=4.128, min_samples=3)`

Comparison to original baseline:
1. Original winner: `KMeans (k=2)` with silhouette `0.1836` and Davies-Bouldin `1.8055`
2. Updated winner: `DBSCAN` with silhouette `0.2224` and Davies-Bouldin `0.9430`

Interpretation:
1. After broadening density search, DBSCAN found valid multi-cluster solutions and outperformed KMeans on separation metrics.
2. The change indicates the original DBSCAN miss was likely parameter-search limitation, not definitive absence of density structure.

### 2.3 Tier Structure Observed
Selected DBSCAN cluster sizes:
1. Noise `-1`: 56 teams
2. Cluster `0`: 306 teams
3. Cluster `1`: 3 teams

Comparison to baseline KMeans split:
1. Baseline KMeans produced a balanced 2-tier split (`196` vs `169`).
2. Updated DBSCAN yields better silhouette but an imbalanced structure with a very small elite/outlier micro-cluster.

Practical interpretation:
1. DBSCAN is currently stronger on geometric separation.
2. KMeans remains easier to operationalize for broad tiering due to balance.
3. Both views are useful: DBSCAN for anomaly/special-case detection and KMeans for broad segmentation.

Visual artifacts generated:
- `Concept Testing/outputs/cluster_scatter_pca.png`
- `Concept Testing/outputs/cluster_scatter_pca_dbscan.png`

The DBSCAN-specific plot now provides a dedicated visual for the selected updated method.

## 3. Linear Regression Conclusions (OLS + Regularization)
Model target: `Overall W-L%`

### 3.1 OLS Comparison: Original vs No-Record-Variables
Original OLS (with direct record variables):
1. `R-squared = 0.999`
2. Dominant predictors: `Overall W`, `Overall L`
3. Extreme multicollinearity, including infinite VIF for direct record terms

Updated OLS (`--exclude-record-features`):
1. `R-squared = 0.983`
2. Significant predictors shift to context wins/losses and quality signals
3. Infinite VIF issue from direct record terms removed, though multicollinearity remains high overall

### 3.2 Statistically Significant Predictors (p < 0.05) In Updated OLS
The following non-intercept predictors were significant at `p < 0.05` after removing direct record variables:

| Predictor | Coefficient | p-value | Direction |
|---|---:|---:|---|
| Away W | 0.015063455 | 7.59e-22 | Positive |
| Away L | -0.012255934 | 2.03e-21 | Negative |
| Home W | 0.011836555 | 1.48e-20 | Positive |
| Home L | -0.012930457 | 7.33e-17 | Negative |
| Points Opp. | -0.000088161 | 0.013925 | Negative |
| Overall SRS | 0.002184848 | 0.039574 | Positive |

Key shift from original:
1. The model now emphasizes contextual game performance and team quality (`SRS`) rather than direct record identity terms.
2. Coefficient interpretation is more meaningful for basketball process variables, even with remaining correlation.

### 3.3 Regularized Regression Findings (Recommendation 3)
Regularization run (`Regularized_Regression_Testing.py --exclude-record-features`) selected:
1. Ridge alpha: `2.75853`
2. Lasso alpha: `0.000371211`
3. Lasso non-zero coefficients: `18/27`

What changed versus OLS:
1. Coefficients were shrunk toward more stable magnitudes under collinearity.
2. Lasso zeroed several redundant predictors, producing an implicit feature-pruning signal.
3. Core directional signals remained consistent (`Away W`/`Home W` positive, `Away L`/`Home L` negative, `Points Opp.` negative, `Overall SRS` positive).

## 4. Diagnostic Risks And Interpretation Caveats
### 4.1 Multicollinearity Remains Material
Even after removing direct record variables, high VIF persists in several box-score families (`Points Tm.`, `FG`, `FT`, `3P`, attempts and percentages).

Implication:
1. OLS p-values and individual coefficient magnitudes still require caution.
2. Regularized models are better suited for stable ranking under this feature geometry.

### 4.2 DBSCAN Practicality Tradeoff
DBSCAN now wins metric-wise but yields one very small non-noise cluster.

Implication:
1. This may capture true elite outliers, but can be less actionable for balanced tier-based downstream pipelines.
2. Use both DBSCAN and KMeans outputs depending on whether the task is anomaly detection or broad stratification.

## 5. Combined Conclusions Across Both Scripts
1. Recommendation 3 succeeded: regularization added stability and clearer feature-selection signal under heavy predictor overlap.
2. Recommendation 4 succeeded: expanded density search produced valid DBSCAN solutions and improved clustering metrics over baseline KMeans.
3. Original baseline remains useful as a reference point:
   - KMeans for balanced broad tiers
   - Updated DBSCAN for density-based structure and outlier labeling
4. Updated regression interpretation is stronger after excluding direct record variables, with meaningful context-performance predictors surfacing.

## 6. Recommendations For Next Iteration
1. Keep dual clustering outputs: retain both KMeans and DBSCAN artifacts for complementary use cases.
2. Add a minimum cluster-size rule for DBSCAN selection to prevent tiny clusters from dominating method choice when operational tiering is the objective.
3. Compare predictive performance of OLS vs Ridge/Lasso on holdout data (not just coefficient behavior).
4. Introduce HDBSCAN as a next density model to improve cluster robustness without fixed `eps` dependence.
5. Promote the regularized coefficient table as the default feature-importance reference for modeling decisions under multicollinearity.

## 7. Key Output Artifacts
- `Concept Testing/outputs/clustered_team_tiers.csv`
- `Concept Testing/outputs/cluster_profiles_zscore_means.csv`
- `Concept Testing/outputs/cluster_scatter_pca.png`
- `Concept Testing/outputs/cluster_scatter_pca_dbscan.png`
- `Concept Testing/outputs/dbscan_candidate_results.csv`
- `Concept Testing/outputs/ols_coefficients_significance.csv`
- `Concept Testing/outputs/ols_coefficients_significance_no_record_vars.csv`
- `Concept Testing/outputs/ols_vif_table.csv`
- `Concept Testing/outputs/ols_vif_table_no_record_vars.csv`
- `Concept Testing/outputs/regularized_vs_ols_coefficients_no_record_vars.csv`
