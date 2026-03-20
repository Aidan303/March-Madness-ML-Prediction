# Step 3 Experiment Matrix

This document locks the exact historical split, run order, and selection rules for model development.

## 1. Historical Split (Locked)

Historical seasons available in model-ready tables:
- 2003-2019, 2021-2025 (22 seasons)

80/20 season split rule:
- Training seasons (18): 2003-2019, 2021
- Test seasons (4): 2022, 2023, 2024, 2025

Notes:
- The same split is used for bracket and champion tracks.
- 2026 data is excluded from all Step 3 training/testing.

## 2. Data Inputs (Step 3)

Bracket track historical tables:
- Good_Data/Model Ready Data/Bracket Model/bracket_games_core_historical.csv
- Good_Data/Model Ready Data/Bracket Model/bracket_games_extended_historical.csv
- Good_Data/Model Ready Data/Bracket Model/bracket_games_experimental_historical.csv

Champion track historical tables:
- Good_Data/Model Ready Data/Champion Model/champion_core_historical.csv
- Good_Data/Model Ready Data/Champion Model/champion_extended_historical.csv
- Good_Data/Model Ready Data/Champion Model/champion_experimental_historical.csv

## 3. Stage 3A: Baseline Sweep (All 3 Sets)

Model family:
- Regularized logistic regression

Bracket runs:
1. BRK_BASE_CORE
2. BRK_BASE_EXT
3. BRK_BASE_EXP

Champion runs:
1. CHAMP_BASE_CORE
2. CHAMP_BASE_EXT
3. CHAMP_BASE_EXP

## 4. Stage 3B: Advancement Rule (Top 2 Sets)

For each objective separately, rank baseline runs and advance the top 2 feature sets.

Bracket ranking priority:
1. Primary: test log loss (lower is better)
2. Secondary: test AUC (higher is better)
3. Tie-breaker: upset accuracy for seed-gap >= 5 games (higher is better)

Champion ranking priority:
1. Primary: test champion log loss (lower is better)
2. Secondary: champion in top-4 rate on test seasons (higher is better)
3. Tie-breaker: champion in top-1 rate on test seasons (higher is better)

## 5. Stage 3C: Tree/Boosting Runs (Top 2 Sets Only)

Model family:
- Gradient boosting trees (or equivalent tree ensemble)

Bracket runs:
1. BRK_TREE_SET1
2. BRK_TREE_SET2

Champion runs:
1. CHAMP_TREE_SET1
2. CHAMP_TREE_SET2

Set1 and Set2 are placeholders for the two advanced feature sets from Stage 3B.

## 6. Stage 3D: Final Selection Rule

Bracket final pick:
- Best test log loss among all completed bracket runs
- Must not degrade upset accuracy by more than 2 percentage points versus best upset run

Champion final pick:
- Best champion log loss among all completed champion runs
- Must be in top-2 for champion top-4 rate

If two models are effectively tied (<= 0.5% relative difference on primary metric), choose the simpler one.

## 7. Calibration (Post-Selection)

Apply probability calibration to the selected bracket and champion models on training data only.
Evaluate calibrated model on the locked test seasons.

## 8. Required Output Artifacts

Store in Model Creation folder:
- step3_run_results.csv
- step3_selected_models.md
- step3_metric_summary_by_season.csv

Required columns for run results:
- run_id
- objective
- model_family
- feature_set
- train_seasons
- test_seasons
- test_log_loss
- test_auc
- upset_acc_seedgap_ge_5 (bracket only)
- champ_top1_rate (champion only)
- champ_top4_rate (champion only)
- selected_for_next_stage

## 9. Guardrails

- No use of 2026 rows in training/testing.
- Same split for all runs.
- No feature changes during Step 3; only model family and locked feature-set choice may vary.
- Any rerun must keep the same run_id with version suffix (for example BRK_BASE_CORE_v2).
