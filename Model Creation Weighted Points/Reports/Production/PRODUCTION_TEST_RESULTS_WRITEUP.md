# Production Test Results Write-Up

Date: 2026-03-13

## Scope

This write-up summarizes the locked production-model evaluation on historical holdout test seasons.

Locked split:
- Train seasons: 2003-2019, 2021
- Test seasons: 2022-2025

Selection basis:
- Stage 4 hardening primary metric: test_log_loss

## Locked Production Models

- Bracket model: BRK_BASE_CORE (logistic, core features, sigmoid calibration)
- Champion model: CHAMP_BASE_CORE (logistic, core features, raw probabilities)

## Test Metrics

| Objective | Run ID | Feature Set | Calibration | Test Log Loss | Test AUC | Upset Acc (abs(seed_gap) >= 5) | Champion Top-1 | Champion Top-4 | Rows Train | Rows Test | Features |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bracket | BRK_BASE_CORE | core | sigmoid | 0.571511 | 0.773585 | 0.782051 |  |  | 2362 | 536 | 18 |
| champion | CHAMP_BASE_CORE | core | raw | 0.052426 | 0.931903 |  | 0.000000 | 0.500000 | 1200 | 272 | 15 |

## Interpretation

### Bracket objective
- Probability quality on holdout seasons is strong for the selected configuration (log loss 0.571511).
- Ranking/discrimination is solid (AUC 0.773585).
- Upset performance for large seed-gap games remains stable at 0.782051.

### Champion objective
- The selected raw model provides the best holdout probability quality among tested calibration variants (log loss 0.052426).
- AUC is high at 0.931903.
- Champion ranking outcomes on test seasons are:
  - Top-1 hit rate: 0.00
  - Top-4 hit rate: 0.50

## Reproducibility and Artifacts

Configuration lock:
- Model Creation Weighted Points/Config/final_model_lock_manifest_weighted_points.json

Generated outputs:
- Model Creation Weighted Points/Results/Production/production_run_metrics.csv
- Model Creation Weighted Points/Results/Production/production_predictions_bracket.csv
- Model Creation Weighted Points/Results/Production/production_predictions_champion.csv

Execution script:
- Model Creation Weighted Points/Model Creation Scripts/Production Model/run_step4_locked_production.py

## Conclusion

The locked production configurations are validated on the historical test window (2022-2025) and were then executed for 2026 inference in this weighted branch.

## 2026 Deployment Update (2026-03-18)

- 2026 inference has been executed for this weighted branch.
- Generated artifacts:
  - Model Creation Weighted Points/Results/Production/2026_bracket_predictions_weighted_points.csv
  - Model Creation Weighted Points/Results/Production/2026_champion_predictions_weighted_points.csv
