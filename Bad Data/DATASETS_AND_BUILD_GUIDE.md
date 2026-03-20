# Data Sets and Build Guide

This document explains what data sets exist, which ones to use for modeling, and how the build process works.

## Purpose

Use this guide to:
- Pick the correct training data set for each modeling task.
- Avoid data leakage.
- Reproduce the data build process.
- Understand where QA and gold-standard outputs are stored.

## Data Inventory

### 1) KenPom source tables (raw)
Path:
- `Data/Historic Data/Kenpom Data/Stats Tables/`

Notes:
- Includes multiple CSV tables (Efficiency, Offense, Defense, etc.).
- Uses `INT _ KenPom _ Summary (Pre-Tournament).csv`.
- Excludes `INT _ KenPom _ Summary.csv`.

Use when:
- Rebuilding cleaned KenPom master data from source.

### 2) NCAA summary source tables (raw)
Path:
- `Data/Historic Data/NCAA Summary Data/`

Notes:
- Currently treated as potentially post-tournament aggregated data.
- Not recommended for leakage-safe pre-tournament prediction workflows.

Use when:
- Historical exploratory analysis only, unless pre-tournament timing is verified.

### 3) KenPom cleaned master
Path:
- `Data/Historic Data/Kenpom Data/Cleaned/Kenpom_Master_TeamSeason.csv`

Notes:
- Team-season level cleaned table from KenPom sources.
- Key columns: `team_season_key`, `Season`, `TeamName_std`.

Use when:
- You need the cleaned KenPom-only base directly.

### 4) Combined cleaned (KenPom + NCAA)
Path:
- `Data/Historic Data/Combined/Cleaned/TeamSeason_Master_Kenpom_NCAA.csv`

Notes:
- Includes NCAA summary columns prefixed with `ncaa_summary__`.
- Not leakage-safe for pre-tournament prediction unless NCAA timing is proven safe.

Use when:
- Sensitivity checks or non-deployment exploratory comparisons.

### 5) KenPom-only model-ready master (recommended)
Path:
- `Data/Historic Data/Combined/Cleaned/TeamSeason_Master_Kenpom_ONLY.csv`

Notes:
- No `ncaa_summary__` columns.
- Built from pre-tournament-safe KenPom pipeline choices.

Use when:
- Training and validating pre-tournament predictive models.
- Main model-development track.

### 6) Gold-standard outputs
Path:
- `Data/Historic Data/Combined/Cleaned/gold/`

Key files:
- `TeamSeason_Master_Kenpom_ONLY_GOLD.csv` (latest stable KenPom-only gold)
- `TeamSeason_Master_Kenpom_NCAA_GOLD.csv` (latest stable combined gold)
- Timestamped snapshots and manifest files

Use when:
- Reproducible model runs.
- Sharing a frozen dataset version with collaborators.

## What to Use for Modeling

### Recommended default
Use:
- `Data/Historic Data/Combined/Cleaned/TeamSeason_Master_Kenpom_ONLY.csv`

Reason:
- Lowest leakage risk for pre-tournament prediction.
- Standardized keys and schema.
- QA-checked build process.

### Use of combined KenPom + NCAA data
Use only if:
- NCAA summary fields are verified to be pre-tournament snapshots.

If not verified:
- Treat combined data as exploratory only.
- Do not use for final performance claims.

## Season Coverage Guidance

Current context:
- Data exists for years from 1999 to 2025 overall.
- KenPom + NCAA overlap starts in 2007.

Practical guidance:
- For KenPom-only models: use available KenPom seasons.
- For any model requiring NCAA columns: limit to overlap years and verify leakage risk first.
- Prefer time-aware train/test splits by season (not random row splits).

## Build Process (Reproducible)

Script:
- `Data Cleaning Scipt.py`

### Recommended command (KenPom-only, QA enforced, gold locked)
```bash
python "Data Cleaning Scipt.py" --stage kenpom --enforce-qa --lock-gold
```

### Other useful command
```bash
python "Data Cleaning Scipt.py" --stage both --enforce-qa --lock-gold
```
Use this only when you explicitly want a combined KenPom+NCAA build.

## QA and Validation Outputs

KenPom QA reports:
- `Data/Historic Data/Kenpom Data/Cleaned/data_quality/kenpom_qa_checks.csv`

Combined QA reports:
- `Data/Historic Data/Combined/Cleaned/data_quality/ncaa_qa_checks.csv`

Other diagnostics are also written to each `data_quality/` directory (missingness, season coverage, merge diagnostics).

## Column and Key Standards

Key columns:
- `team_season_key`
- `Season`
- `TeamName_std`

Column prefix rules:
- KenPom feature columns start with `kenpom_`.
- NCAA feature columns start with `ncaa_summary__`.

Naming standardization:
- Team names are canonicalized in the pipeline.
- Requested alias fixes and typo corrections are baked into script logic.

## Leakage Policy

For pre-tournament prediction tasks:
- Safe default: KenPom-only model-ready data.
- Avoid NCAA summary features unless they are proven pre-tournament.

If combined data is used anyway:
- Label outputs as exploratory/non-deployable until timing is verified.

## Change Log Notes

Important process milestones:
- Added deterministic merge + QA checks.
- Added gold snapshot workflow with manifest files.
- Switched default run stage to KenPom-only for leakage-safe modeling.
- Added `TeamSeason_Master_Kenpom_ONLY.csv` as the main model-ready dataset.
