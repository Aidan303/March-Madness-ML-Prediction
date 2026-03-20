# Stage 4 Final Model Selection Memo

Date: 2026-03-13

## Decision Summary

Final selected models:
- Bracket objective: BRK_BASE_CORE with sigmoid calibration
- Champion objective: CHAMP_BASE_CORE with raw probabilities (no additional calibration)

Primary selection metric:
- test_log_loss on locked holdout seasons 2022-2025

Locked split:
- Train seasons: 2003-2019, 2021
- Test seasons: 2022-2025

## Evidence From Stage 4

### Bracket objective (BRK_BASE_CORE)

| Variant | Test Log Loss | Test AUC | Upset Acc (abs(seed_gap) >= 5) |
|---|---:|---:|---:|
| sigmoid | 0.571511 | 0.773585 | 0.782051 |
| raw | 0.574580 | 0.773864 | 0.782051 |
| isotonic | 0.697103 | 0.774108 | 0.782051 |

Result:
- Sigmoid improves the primary metric versus raw by 0.003070 (lower is better) with similar AUC and unchanged upset accuracy.
- Isotonic materially underperforms on log loss.

Selection:
- Use sigmoid-calibrated BRK_BASE_CORE.

### Champion objective (CHAMP_BASE_CORE)

| Variant | Test Log Loss | Test AUC | Champion Top-1 | Champion Top-4 |
|---|---:|---:|---:|---:|
| raw | 0.052426 | 0.931903 | 0.00 | 0.50 |
| isotonic | 0.053349 | 0.929104 | 0.00 | 0.50 |
| sigmoid | 0.056712 | 0.929104 | 0.00 | 0.50 |

Result:
- Raw probabilities are best on the primary metric.
- Additional calibration does not improve top-k championship ranking outcomes on the holdout seasons.

Selection:
- Use raw CHAMP_BASE_CORE.

## Production Recommendation

Adopt the following Stage 4 outputs as the current production candidates:
- Bracket production candidate: BRK_BASE_CORE + sigmoid calibration
- Champion production candidate: CHAMP_BASE_CORE (raw)

## Supporting Artifacts

- Results/Model Refinement/stage4_hardening_results.csv
- Results/Model Refinement/stage4_stability_by_season.csv
- Reports/Model Refinement/STAGE4_HARDENING_SUMMARY.md
- Reports/Model Creation/STEP3_MODEL_COMPARISON_REPORT.md

## Notes

- This memo intentionally covers only Steps 1 and 2 from the agreed plan.
- No additional pipeline stages were executed as part of this memo step.
