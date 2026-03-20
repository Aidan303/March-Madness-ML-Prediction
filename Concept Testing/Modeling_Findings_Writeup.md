# March Madness Exploratory Modeling Findings

Date: 2026-03-11
Dataset: `Data/College_Team_Stats.csv`
Scripts:
- `Concept Testing/Clustering_Testing.py`
- `Concept Testing/Linear_Regression_Testing.py`

## 1. Scope And Objective
This exploratory pass had two goals:
1. Identify broad team tiers using unsupervised clustering with unknown cluster count/shape.
2. Quantify linear relationships between team stats and season success using OLS, with emphasis on coefficients and statistical significance.

All context groups were included in the first pass (`Overall`, `Conf.`, `Home`, `Away`, and unprefixed season totals).

## 2. Clustering Conclusions
### 2.1 Methods Compared
The clustering script evaluated:
1. KMeans across `k = 2..10`
2. DBSCAN across an `eps` x `min_samples` grid

### 2.2 Best Clustering Method
Best method in this run: `KMeans (k=2)`

Key metrics from the run:
1. Best KMeans silhouette: `0.1836`
2. Best KMeans Davies-Bouldin: `1.8055`
3. DBSCAN result: no valid configuration found with at least 2 non-noise clusters under the tested parameter grid

Interpretation:
1. KMeans was the only method producing a stable, valid partition under current settings.
2. Silhouette `0.1836` indicates weak-to-moderate separation, so this is useful as a tiering baseline but not yet a strongly separated clustering structure.

### 2.3 Tier Structure Observed
Cluster sizes:
1. Cluster `0`: 196 teams
2. Cluster `1`: 169 teams

Cluster profile pattern (z-scored means) shows a clear quality split:
1. Cluster `0` is the stronger tier: higher `Overall W`, `Conf. W`, `Home W`, `Points Tm.` and lower losses.
2. Cluster `1` is the weaker tier: inverse pattern with lower wins and higher losses.

Top differentiators (from profile outputs and console summary):
1. `Overall W` and `Overall L`
2. `Conf. W` and `Conf. L`
3. `Home W` and `Home L`
4. `Away L`
5. `Points Tm.`

Visual artifact generated:
- `Concept Testing/outputs/cluster_scatter_pca.png`

This figure now includes labels for the top 10 teams by `Overall W-L%` to make elite-team positioning explicit.

## 3. Linear Regression Conclusions (OLS)
Model target: `Overall W-L%`

Overall model fit:
1. `R-squared = 0.999`
2. `Adjusted R-squared = 0.999`
3. F-statistic p-value is effectively `0.00`

These values indicate near-perfect explanatory fit in-sample, but interpretation must account for severe multicollinearity and near-identity relationships with record-derived predictors.

### 3.1 Statistically Significant Predictors (p < 0.05)
The following non-intercept predictors were significant at `p < 0.05`:

| Predictor | Coefficient | p-value | Direction |
|---|---:|---:|---|
| Overall W | 0.015572644 | 4.22e-111 | Positive |
| Overall L | -0.015502216 | 3.17e-101 | Negative |
| FGA | 0.000433806 | 2.14e-16 | Positive |
| FG% | 1.759469590 | 2.72e-17 | Positive |
| Overall SRS | 0.000798735 | 8.6008e-04 | Positive |
| Points Opp. | 0.000022100 | 0.006736 | Positive |
| Overall SOS | -0.000683819 | 0.017000 | Negative |
| FT% | 0.150349264 | 0.021533 | Positive |
| FTA | 0.000165474 | 0.026573 | Positive |
| 3P% | 0.162902853 | 0.034419 | Positive |
| 3PA | 0.000073300 | 0.042073 | Positive |

Intercept term (also significant):
1. `const = -0.434846633`, `p = 8.30e-06`

### 3.2 Important Coefficient Takeaways
1. `Overall W` and `Overall L` dominate magnitude/significance, which is expected because they are directly tied to the target outcome.
2. Efficiency/shooting terms (`FG%`, `FT%`, `3P%`) are significant and directionally consistent with basketball intuition.
3. Shot volume (`FGA`, `FTA`, `3PA`) is also significant, suggesting pace/usage variables contribute to variance in win rate in this specification.
4. `Overall SRS` is significant and positive, supporting strength-adjusted team quality signal.

## 4. Diagnostic Risks And Interpretation Caveats
### 4.1 Severe Multicollinearity
VIF diagnostics are very high for many predictors, including:
1. `Overall G`, `Overall W`, `Overall L` with infinite VIF
2. `Points Tm.` (~453,943)
3. `FG` (~236,534)
4. `FT` (~56,589)
5. `3P` (~27,726)

Implication:
1. Individual coefficient estimates are unstable under small perturbations.
2. p-values and signs for correlated predictors should be interpreted cautiously.
3. This is expected in the all-context first-pass setup and with direct record variables included.

### 4.2 Leakage-Like Explanatory Dominance
Because `Overall W` and `Overall L` are near-direct components of success, they can overshadow explanatory value from play-style and efficiency metrics.

Implication:
1. Current OLS is strong for exploratory signal discovery.
2. It is less suitable as a clean inferential model of independent stat contribution unless record-derived features are constrained.

## 5. Combined Conclusions Across Both Scripts
1. Clustering baseline winner: `KMeans` (DBSCAN did not yield a valid multi-cluster solution in tested grid).
2. Team tiers are primarily split by wins/losses and related context outcomes, indicating the clustering currently captures broad quality strata.
3. OLS identifies many significant basketball metrics, but multicollinearity is extreme, so coefficient-level inference is not yet robust for causal interpretation.
4. The two scripts are complementary:
   - Clustering provides team-tier segmentation.
   - OLS provides directional/statistical relevance of individual stats.

## 6. Recommendations For Next Iteration
1. Keep this run as baseline and archive the current outputs for reproducibility.
2. Run a second OLS specification excluding direct record variables (`Overall W`, `Overall L`, `Overall G`) to get cleaner inferential coefficients.
3. Add regularized regression comparison (Ridge/Lasso) for coefficient stability under high collinearity.
4. Expand density clustering alternatives (broader DBSCAN grid or HDBSCAN) if non-spherical structure remains a hypothesis.
5. For stakeholder communication, use `cluster_scatter_pca.png` plus a top-team table to explain where elite teams land in tier space.

## 7. Key Output Artifacts
- `Concept Testing/outputs/clustered_team_tiers.csv`
- `Concept Testing/outputs/cluster_profiles_zscore_means.csv`
- `Concept Testing/outputs/cluster_scatter_pca.png`
- `Concept Testing/outputs/ols_coefficients_significance.csv`
- `Concept Testing/outputs/ols_vif_table.csv`
