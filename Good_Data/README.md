# Good_Data Guide

## Purpose
This folder is the data backbone of the project.

## Scope
- Raw and support datasets used across branches.
- Stat package and stat-engine components.
- Master feature tables and model-ready builders shared by production branches.

## Key Subfolders
- [march-machine-learning-mania-2026-base-data](march-machine-learning-mania-2026-base-data): Kaggle-style base tournament/season files.
- [Model Ready Data](Model%20Ready%20Data): scripts and outputs used to build branch-ready bracket/champion model tables.
- [Master Data](Master%20Data): team-season master features and locked/pruned feature references.
- [Data Support Files](Data%20Support%20Files): architecture and data quality notes.
- [Full Stat Package](Full%20Stat%20Package): stat registry and stat engine modules.

## Common Entry Point
Build shared model-ready tables from repo root:

```powershell
python "Good_Data/Model Ready Data/build_model_ready_tables.py"
```

## Observer Checklist
- Confirm seeds, slots, and First Four rows exist in base data before 2026 production runs.
- Confirm model-ready outputs are regenerated after any base-data update.
- Confirm schema expectations using the model-ready schema contract.

## 2026 Status Note
- Shared model-ready tables have already been rebuilt for 2026 workflows in this workspace.
- If base tournament inputs change, re-run the shared model-ready builder before re-running branch inference.

## Related Docs
- [Model Ready Data/MODEL_READY_SCHEMA_CONTRACT.md](Model%20Ready%20Data/MODEL_READY_SCHEMA_CONTRACT.md)
- [Data Support Files/DATA_ARCHITECTURE_AND_QUALITY.md](Data%20Support%20Files/DATA_ARCHITECTURE_AND_QUALITY.md)
- [Full Stat Package/README.md](Full%20Stat%20Package/README.md)
