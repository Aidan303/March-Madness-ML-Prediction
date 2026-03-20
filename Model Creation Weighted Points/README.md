# Model Creation Weighted Points Branch

## Purpose
This folder contains the weighted-points variant of the production modeling branch.

## Scope
- Uses weighted-points scoring/selection logic for model evaluation and choice.
- Keeps output structure parallel to the original branch for easy side-by-side comparison.

## Main Structure
- [Model Creation Scripts](Model%20Creation%20Scripts): weighted model selection plus production inference scripts.
- [Config](Config): weighted and base lock manifests.
- [Reports](Reports): model creation, refinement, and production summaries.
- [Results](Results): weighted production outputs and comparison reports.

## Important Scripts
- [Model Creation Scripts/run_weighted_points_model_selection.py](Model%20Creation%20Scripts/run_weighted_points_model_selection.py)
- [Model Creation Scripts/compare_baseline_vs_weighted_points.py](Model%20Creation%20Scripts/compare_baseline_vs_weighted_points.py)
- [Model Creation Scripts/Production Model/run_2026_inference.py](Model%20Creation%20Scripts/Production%20Model/run_2026_inference.py)
- [Model Creation Scripts/Production Model/interpret_bracket_text.py](Model%20Creation%20Scripts/Production%20Model/interpret_bracket_text.py)

## Production Run
From repo root:

```powershell
python "Model Creation Weighted Points/Model Creation Scripts/Production Model/run_2026_inference.py"
```

## Primary Outputs
- [Results/Production/2026_bracket_predictions_weighted_points.csv](Results/Production/2026_bracket_predictions_weighted_points.csv)
- [Results/Production/2026_champion_predictions_weighted_points.csv](Results/Production/2026_champion_predictions_weighted_points.csv)

## 2026 Run Status
- 2026 production inference has been executed in this branch.
- The two production CSV outputs above reflect the generated 2026 weighted-branch predictions.

## Lock Manifest
- [Config/final_model_lock_manifest_weighted_points.json](Config/final_model_lock_manifest_weighted_points.json)

## Related Docs
- [Reports/Model Creation/STEP3_MODEL_COMPARISON_REPORT.md](Reports/Model%20Creation/STEP3_MODEL_COMPARISON_REPORT.md)
- [Reports/Model Refinement/STAGE4_MODEL_SELECTION_MEMO.md](Reports/Model%20Refinement/STAGE4_MODEL_SELECTION_MEMO.md)
- [Reports/Production/PRODUCTION_TEST_RESULTS_WRITEUP.md](Reports/Production/PRODUCTION_TEST_RESULTS_WRITEUP.md)
