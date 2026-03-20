# Step 3 Model Comparison Report

## Scope
This report summarizes Stage 3 model experiments for:
- Bracket game outcome prediction
- Champion-only prediction

Data source:
- `Model Creation/Results/Model Creation/step3_run_results.csv`

Locked split:
- Train seasons: 2003-2019, 2021
- Test seasons: 2022-2025

## Runs Executed

### Bracket Objective
| Run ID | Model | Feature Set | Test Log Loss | Test AUC | Upset Acc (abs(seed_gap) >= 5) |
|---|---|---|---:|---:|---:|
| BRK_BASE_CORE | Logistic | core | **0.574580** | **0.773864** | **0.782051** |
| BRK_BASE_EXT | Logistic | extended | 0.578296 | 0.770230 | 0.750000 |
| BRK_BASE_EXP | Logistic | experimental | 0.581409 | 0.769965 | 0.756410 |
| BRK_TREE_SET1 | Tree | core | 0.599980 | 0.769311 | 0.772436 |
| BRK_TREE_SET2 | Tree | extended | 0.613245 | 0.763742 | 0.753205 |

### Champion Objective
| Run ID | Model | Feature Set | Test Log Loss | Test AUC | Top-1 Hit Rate | Top-4 Hit Rate |
|---|---|---|---:|---:|---:|---:|
| CHAMP_BASE_CORE | Logistic | core | **0.052426** | **0.931903** | 0.00 | 0.50 |
| CHAMP_BASE_EXT | Logistic | extended | 0.066174 | 0.908582 | 0.25 | **0.75** |
| CHAMP_BASE_EXP | Logistic | experimental | 0.065385 | 0.900187 | 0.25 | **0.75** |
| CHAMP_TREE_SET1 | Tree | core | 0.099174 | 0.887127 | 0.00 | **0.75** |
| CHAMP_TREE_SET2 | Tree | experimental | 0.126798 | **0.931903** | 0.25 | 0.50 |

## Advancement Logic Applied
Top-2 feature sets from baseline stage were advanced to tree stage:
- Bracket: `core`, `extended`
- Champion: `core`, `experimental`

This follows the locked Stage 3B rule (advance top 2 per objective).

## Interpretation and Comparison

### 1) Bracket Model Comparison
- Primary metric (`test_log_loss`) clearly favors **BRK_BASE_CORE**.
- Tree models did not improve log loss relative to logistic baselines.
- BRK_BASE_CORE also has the strongest upset accuracy in this run.

Bracket conclusion:
- **Preferred model at this stage: BRK_BASE_CORE (Logistic + core set)**
- Reason: best probability quality (log loss) and best overall AUC while maintaining strong upset accuracy.

### 2) Champion Model Comparison
- Primary metric (`test_log_loss`) strongly favors **CHAMP_BASE_CORE**.
- Tree models do not improve the primary metric and underperform on calibration quality.
- Top-4 rate is higher for CHAMP_BASE_EXT/EXP, but both underperform core on the primary metric.

Champion conclusion:
- **Preferred model at this stage: CHAMP_BASE_CORE (Logistic + core set)**
- Reason: strongest primary metric and strong AUC under locked split.

## Selected Models (Pre-Calibration)
- Bracket selected candidate: **BRK_BASE_CORE**
- Champion selected candidate: **CHAMP_BASE_CORE**

These are the candidates to carry into the calibration step.

## Locked Advancement to Stage 4
- Bracket promotion (locked): **BRK_BASE_CORE**
- Champion promotion (locked): **CHAMP_BASE_CORE**

Stage 4 is restricted to calibration and stability checks for these two promoted candidates only.

## Notes
- Results are from one locked historical split (2022-2025 holdout).
- Tree-stage runs were intentionally constrained to top-2 feature sets for efficiency.
- Final production choice should be confirmed after calibration metrics are evaluated on the same test seasons.
