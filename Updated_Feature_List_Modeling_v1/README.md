# Updated Feature List Modeling v1

## Purpose
This branch extends the original feature set with newly enabled non-duplicate stats and provides its own training and production pipeline.

## Scope
- Start from original master features.
- Add newly enabled Michigan/stat-engine features that are not duplicates.
- Train/evaluate model variants and lock production choices.

## Main Structure
- [scripts](scripts): updated pipeline build, training, and production inference scripts.
- [config](config): feature mapping and updated lock manifest.
- [data](data): updated historical/current model-ready datasets.
- [results](results): updated model metrics, selections, and production outputs.

## Important Scripts
- [scripts/build_updated_pipeline.py](scripts/build_updated_pipeline.py)
- [scripts/train_updated_models.py](scripts/train_updated_models.py)
- [scripts/run_updated_pipeline_and_training.py](scripts/run_updated_pipeline_and_training.py)
- [scripts/Production Model/run_2026_inference.py](scripts/Production%20Model/run_2026_inference.py)
- [scripts/Production Model/run_2026_bracket_inference.py](scripts/Production%20Model/run_2026_bracket_inference.py)
- [scripts/Production Model/run_2026_champion_inference.py](scripts/Production%20Model/run_2026_champion_inference.py)

## Typical Workflow
1. Build updated branch tables:
```powershell
python "Updated_Feature_List_Modeling_v1/scripts/build_updated_pipeline.py"
```
2. Train and evaluate updated models:
```powershell
python "Updated_Feature_List_Modeling_v1/scripts/train_updated_models.py"
```
3. Run locked 2026 production inference:
```powershell
python "Updated_Feature_List_Modeling_v1/scripts/Production Model/run_2026_inference.py" --season 2026
```

## Primary Outputs
- [results/Production/2026_bracket_predictions.csv](results/Production/2026_bracket_predictions.csv)
- [results/Production/2026_champion_predictions.csv](results/Production/2026_champion_predictions.csv)
- [results/updated_model_run_metrics.csv](results/updated_model_run_metrics.csv)

## 2026 Run Status
- 2026 production inference has been executed in this branch.
- Production bracket and champion outputs are generated under [results/Production](results/Production).

## Lock Manifest
- [config/final_model_lock_manifest_updated.json](config/final_model_lock_manifest_updated.json)

## Related Docs
- [results/updated_model_run_metrics.csv](results/updated_model_run_metrics.csv)
- [results/updated_model_selected_for_production.csv](results/updated_model_selected_for_production.csv)
- [config/updated_core_added_stat_mapping.csv](config/updated_core_added_stat_mapping.csv)
