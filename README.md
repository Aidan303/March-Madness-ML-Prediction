# March Madness Prediction Modeling Project

End-to-end modeling system for NCAA Men's March Madness bracket and champion prediction.

This repository contains three production model branches (original, weighted points, and updated feature list), the shared data pipelines that feed them, and supporting experiment/utilities.

## 2026 Execution Status
- 2026 model-ready tables were rebuilt.
- 2026 production inference was executed for original, weighted-points, and updated-feature branches.
- Branch outputs and cross-branch comparison artifacts are present in this workspace.

## Project Outcomes
- Tournament game winner probabilities by slot.
- Full bracket simulation from Round of 64 through championship.
- Team-level title probability rankings.
- Side-by-side comparison report for 2026 outputs across all model branches.

## Quick Start (2026 Full Refresh / Re-Run)
Run from project root after seeds, slots, and First Four outcomes are available.

1. Build shared model-ready tables:
```powershell
python "Good_Data/Model Ready Data/build_model_ready_tables.py"
```
2. Build updated-feature branch model-ready tables:
```powershell
python "Updated_Feature_List_Modeling_v1/scripts/build_updated_pipeline.py"
```
3. Run 2026 production inference for each branch:
```powershell
python "Model Creation/Model Creation Scripts/Production Model/run_2026_inference.py"
python "Model Creation Weighted Points/Model Creation Scripts/Production Model/run_2026_inference.py"
python "Updated_Feature_List_Modeling_v1/scripts/Production Model/run_2026_inference.py" --season 2026
```

## Repository Map
- [Good_Data](Good_Data): source datasets, support files, stat package, and model-ready build scripts.
- [Model Creation](Model%20Creation): original production modeling branch.
- [Model Creation Weighted Points](Model%20Creation%20Weighted%20Points): weighted-points production modeling branch.
- [Updated_Feature_List_Modeling_v1](Updated_Feature_List_Modeling_v1): branch with expanded feature set from newly enabled stats.
- [Concept Testing](Concept%20Testing): experimentation scripts and report-generation helpers.
- [bracket vizualisations](bracket%20vizualisations): scripted PNG bracket rendering for reader-facing visuals.
- [docs](docs): high-level technical overview docs.

## Model Branches
- Original branch: [Model Creation](Model%20Creation) (outputs in [Model Creation/Results/Production](Model%20Creation/Results/Production)).
- Weighted points branch: [Model Creation Weighted Points](Model%20Creation%20Weighted%20Points) (outputs in [Model Creation Weighted Points/Results/Production](Model%20Creation%20Weighted%20Points/Results/Production)).
- Updated feature list branch: [Updated_Feature_List_Modeling_v1](Updated_Feature_List_Modeling_v1) (outputs in [Updated_Feature_List_Modeling_v1/results/Production](Updated_Feature_List_Modeling_v1/results/Production)).

## Core 2026 Artifacts
- Cross-branch comparison report: [2026_Production_Model_Comparison.md](2026_Production_Model_Comparison.md)
- Updated branch lock manifest: [Updated_Feature_List_Modeling_v1/config/final_model_lock_manifest_updated.json](Updated_Feature_List_Modeling_v1/config/final_model_lock_manifest_updated.json)
- Original branch lock manifest: [Model Creation/Config/final_model_lock_manifest.json](Model%20Creation/Config/final_model_lock_manifest.json)
- Weighted branch lock manifest: [Model Creation Weighted Points/Config/final_model_lock_manifest_weighted_points.json](Model%20Creation%20Weighted%20Points/Config/final_model_lock_manifest_weighted_points.json)

## Documentation Index
- Technical overview: [docs/PROJECT_OVERVIEW_FULL.md](docs/PROJECT_OVERVIEW_FULL.md)
- Docs index: [docs/README.md](docs/README.md)
- Data area guide: [Good_Data/README.md](Good_Data/README.md)
- Original branch guide: [Model Creation/README.md](Model%20Creation/README.md)
- Weighted branch guide: [Model Creation Weighted Points/README.md](Model%20Creation%20Weighted%20Points/README.md)
- Updated-feature branch guide: [Updated_Feature_List_Modeling_v1/README.md](Updated_Feature_List_Modeling_v1/README.md)
- Experiment area guide: [Concept Testing/README.md](Concept%20Testing/README.md)
- Bracket visualization guide: [bracket vizualisations/README.md](bracket%20vizualisations/README.md)

## Notes For Observers
- Training/evaluation logic is branch-specific, but all branches consume the same base tournament structures and team identifiers.
- Later-round slots can contain different participants per branch because earlier predictions change bracket paths.
- The comparison report explicitly calls out these divergences for rounds 4-6.
