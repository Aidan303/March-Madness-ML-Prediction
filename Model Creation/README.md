# Model Creation (Original Branch)

## Purpose
This folder contains the original production modeling branch.

## Scope
- Trains/evaluates bracket and champion models on historical data.
- Selects production configuration with manifest-locked settings.
- Runs production inference for target season outputs.

## Main Structure
- [Model Creation Scripts](Model%20Creation%20Scripts): training, selection, hardening, and production inference scripts.
- [Config](Config): lock manifests and branch configuration.
- [Reports](Reports): experiment, refinement, and production writeups.
- [Results](Results): generated predictions and evaluation outputs.

## Important Scripts
- [Model Creation Scripts/run_step3_baselines.py](Model%20Creation%20Scripts/run_step3_baselines.py)
- [Model Creation Scripts/run_step3_trees.py](Model%20Creation%20Scripts/run_step3_trees.py)
- [Model Creation Scripts/run_stage4_hardening.py](Model%20Creation%20Scripts/run_stage4_hardening.py)
- [Model Creation Scripts/Production Model/run_2026_inference.py](Model%20Creation%20Scripts/Production%20Model/run_2026_inference.py)
- [Model Creation Scripts/Production Model/interpret_bracket_text.py](Model%20Creation%20Scripts/Production%20Model/interpret_bracket_text.py)

## Production Run
From repo root:

```powershell
python "Model Creation/Model Creation Scripts/Production Model/run_2026_inference.py"
```

## Primary Outputs
- [Results/Production/2026_bracket_predictions.csv](Results/Production/2026_bracket_predictions.csv)
- [Results/Production/2026_champion_predictions.csv](Results/Production/2026_champion_predictions.csv)

## 2026 Run Status
- 2026 production inference has been executed in this branch.
- The two production CSV outputs above reflect the generated 2026 branch predictions.

## Lock Manifest
- [Config/final_model_lock_manifest.json](Config/final_model_lock_manifest.json)

## Related Docs
- [Reports/Model Creation/STEP3_MODEL_COMPARISON_REPORT.md](Reports/Model%20Creation/STEP3_MODEL_COMPARISON_REPORT.md)
- [Reports/Model Refinement/STAGE4_MODEL_SELECTION_MEMO.md](Reports/Model%20Refinement/STAGE4_MODEL_SELECTION_MEMO.md)
- [Reports/Production/PRODUCTION_TEST_RESULTS_WRITEUP.md](Reports/Production/PRODUCTION_TEST_RESULTS_WRITEUP.md)
