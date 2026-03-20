# Stage 4 Hardening Summary

Focused scope:
- Bracket candidate: BRK_BASE_CORE
- Champion candidate: CHAMP_BASE_CORE

## Bracket objective

| Variant | Test Log Loss | Test AUC | Upset Acc (seed_gap abs >= 5) | Champion Top-1 | Champion Top-4 |
|---|---:|---:|---:|---:|---:|
| sigmoid | 0.571511 | 0.773585 | 0.782051 |  |  |
| raw | 0.574580 | 0.773864 | 0.782051 |  |  |
| isotonic | 0.697103 | 0.774108 | 0.782051 |  |  |

Selected calibration variant by primary metric (test_log_loss): **sigmoid**

## Champion objective

| Variant | Test Log Loss | Test AUC | Upset Acc (seed_gap abs >= 5) | Champion Top-1 | Champion Top-4 |
|---|---:|---:|---:|---:|---:|
| raw | 0.052426 | 0.931903 |  | 0.000000 | 0.500000 |
| isotonic | 0.053349 | 0.929104 |  | 0.000000 | 0.500000 |
| sigmoid | 0.056712 | 0.929104 |  | 0.000000 | 0.500000 |

Selected calibration variant by primary metric (test_log_loss): **raw**
