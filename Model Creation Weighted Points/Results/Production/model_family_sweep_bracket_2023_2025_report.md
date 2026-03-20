# Bracket Model Family Sweep Report

## Objective
Evaluate multiple bracket model families on seasons 2023-2025 using winner-set comparison by round and weighted points (1,2,4,8,16,32).

## Best Overall Model
- Model: rf_raw
- Avg points: 100.00/192.00
- Avg points %: 52.08%
- Avg point gap: 92.00
- Avg winner-set error: 41.33

## Leaderboard (Overall)
| Rank | Model | Avg Points | Avg Points % | Avg Point Gap | Avg Winner-Set Error |
|---:|---|---:|---:|---:|---:|
| 1 | rf_raw | 100.00/192.00 | 52.08% | 92.00 | 41.33 |
| 2 | gbm_raw | 99.00/192.00 | 51.56% | 93.00 | 40.00 |
| 3 | rf_sigmoid | 98.33/192.00 | 51.22% | 93.67 | 41.33 |
| 4 | gbm_sigmoid | 92.33/192.00 | 48.09% | 99.67 | 41.33 |
| 5 | locked_baseline_sigmoid | 91.67/192.00 | 47.74% | 100.33 | 45.33 |
| 6 | logreg_raw | 91.67/192.00 | 47.74% | 100.33 | 45.33 |
| 7 | logreg_sigmoid | 91.67/192.00 | 47.74% | 100.33 | 45.33 |
| 8 | logreg_isotonic | 89.67/192.00 | 46.70% | 102.33 | 45.33 |

## Per-Season Best Models
### 2023
- Best model: rf_raw
- Points: 57/192 (29.69%)
- Point gap: 135
- Winner-set error: 52

### 2024
- Best model: rf_sigmoid
- Points: 137/192 (71.35%)
- Point gap: 55
- Winner-set error: 40

### 2025
- Best model: locked_baseline_sigmoid
- Points: 135/192 (70.31%)
- Point gap: 57
- Winner-set error: 32
