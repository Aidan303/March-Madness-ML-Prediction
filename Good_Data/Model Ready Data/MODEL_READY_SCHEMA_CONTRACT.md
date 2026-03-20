# Model Ready Data Schema Contract

This contract defines the planned model-ready sheets for both modeling objectives:
1. Bracket game outcome prediction
2. Champion-only prediction

No training logic is defined here. This is a data schema and build-order specification.

## Folder Plan

Recommended structure under this folder:
- Shared/
- Bracket Model/
- Champion Model/
- Manifests/

## Source Inputs

Primary feature sources:
- Good_Data/Master Data/Master CSV File and Support Files/master_features_all_teams_historical.csv
- Good_Data/Master Data/Master CSV File and Support Files/master_features_all_teams_2026.csv (when available)

Locked feature sets:
- Good_Data/Master Data/Pruned Feature Sets (Gold)/locked_feature_set_core.csv
- Good_Data/Master Data/Pruned Feature Sets (Gold)/locked_feature_set_extended.csv
- Good_Data/Master Data/Pruned Feature Sets (Gold)/locked_feature_set_experimental.csv

Tournament structure/results sources:
- Good_Data/march-machine-learning-mania-2026-base-data/MNCAATourneyCompactResults.csv
- Good_Data/march-machine-learning-mania-2026-base-data/MNCAATourneySeeds.csv
- Good_Data/march-machine-learning-mania-2026-base-data/MNCAATourneySlots.csv

## Master File Strategy

Two separate master files are part of the intended long-term design:

1. Historical master
- File: `Good_Data/Master Data/Master CSV File and Support Files/master_features_all_teams_historical.csv`
- Purpose: canonical historical training/backtesting source
- Coverage: historical seasons only
- Current intended range: 2003-2025, excluding 2020

2. 2026 master
- File: `Good_Data/Master Data/Master CSV File and Support Files/master_features_all_teams_2026.csv`
- Purpose: canonical 2026 inference source
- Coverage: 2026 only
- Schema requirement: must match the historical master schema so downstream model-ready generation is reusable

The 2026 master will be built from the same good-data sources used for the historical master, filtered to 2026 records only. When 2026 KenPom pre-tournament summary data is gathered, it will be merged with the 2026 good-data slice to complete the 2026 master in the same format as the historical file.

## End-State Workflow

The intended end-to-end workflow is:

1. Build `master_features_all_teams_historical.csv`
2. Build `master_features_all_teams_2026.csv`
3. Generate model-ready historical and 2026 tables from those two master files
4. Split historical model-ready data into training and test sets using an 80/20 rule
5. Use the historical split to train and tune models
6. Freeze the tuned model configuration
7. Run the tuned model on 2026 model-ready data to generate final 2026 predictions

Interpretation rule:
- Historical master/model-ready tables exist for training, validation, and testing
- 2026 master/model-ready tables exist for final forward-looking prediction only

## Locked Feature Sets (Counts)
- core: 15
- extended: 57
- experimental: 72

## Shared Sheets

### 1) team_season_features_core_historical.csv
Primary key:
- Season, TeamID

Required columns:
- Season, TeamID, TeamName, ConfAbbrev, is_tourney_team, tourney_seed_num
- all features from locked core set

Coverage:
- Historical seasons available in master table

### 2) team_season_features_extended_historical.csv
Primary key:
- Season, TeamID

Required columns:
- same identity columns as core
- all features from locked extended set

### 3) team_season_features_experimental_historical.csv
Primary key:
- Season, TeamID

Required columns:
- same identity columns as core
- all features from locked experimental set

### 4) team_season_features_core_2026.csv
Primary key:
- Season, TeamID

Required columns:
- same schema as team_season_features_core_historical.csv

Coverage:
- current prediction season only (for example 2026)

### 5) team_season_features_extended_2026.csv
Primary key:
- Season, TeamID

Required columns:
- same schema as extended historical

### 6) team_season_features_experimental_2026.csv
Primary key:
- Season, TeamID

Required columns:
- same schema as experimental historical

### 7) tournament_team_labels_historical.csv
Primary key:
- Season, TeamID

Required columns:
- Season, TeamID
- is_tourney_team
- tourney_seed_num
- reached_sweet16
- reached_elite8
- reached_final4
- reached_title_game
- is_champion

Purpose:
- single shared target table for champion and round-level analyses

## Bracket Model Sheets

### 1) bracket_games_historical_targets.csv
Primary key:
- Season, DayNum, TeamAID, TeamBID

Required columns:
- Season, DayNum, TeamAID, TeamBID
- target_teamA_win (1/0)
- optional metadata: WTeamID, LTeamID from source game row

Construction:
- duplicate each historical tournament game into two oriented rows
  - TeamA = winner, TeamB = loser, target=1
  - TeamA = loser, TeamB = winner, target=0

### 2) bracket_games_core_historical.csv
Primary key:
- Season, DayNum, TeamAID, TeamBID

Required columns:
- keys from target sheet
- for each core feature f: delta_f = TeamA_f - TeamB_f
- seed context fields:
  - TeamA_seed_num
  - TeamB_seed_num
  - seed_gap = TeamB_seed_num - TeamA_seed_num

Target column:
- target_teamA_win

### 3) bracket_games_extended_historical.csv
Same schema pattern as core, using extended set features.

### 4) bracket_games_experimental_historical.csv
Same schema pattern as core, using experimental set features.

### 5) bracket_teams_2026.csv
Primary key:
- Season, TeamID

Required columns:
- Season, TeamID, Seed
- TeamName (if available)

Purpose:
- current bracket participants and seed mapping used to generate game pairs

### 6) bracket_games_core_2026.csv
Primary key:
- Season, Slot, TeamAID, TeamBID

Required columns:
- Season, Slot, TeamAID, TeamBID
- same feature engineering schema as historical core bracket data

No target column.

### 7) bracket_games_extended_2026.csv
Same schema pattern as core 2026, using extended features.

### 8) bracket_games_experimental_2026.csv
Same schema pattern as core 2026, using experimental features.

## Champion Model Sheets

### 1) champion_core_historical.csv
Primary key:
- Season, TeamID

Required columns:
- Season, TeamID, TeamName, ConfAbbrev, is_tourney_team, tourney_seed_num
- core feature set columns
- labels from tournament_team_labels_historical:
  - is_champion
  - reached_sweet16
  - reached_elite8
  - reached_final4
  - reached_title_game

Required filter:
- is_tourney_team = 1

### 2) champion_extended_historical.csv
Same schema pattern as champion_core_historical, with extended set.

### 3) champion_experimental_historical.csv
Same schema pattern as champion_core_historical, with experimental set.

### 4) champion_core_2026.csv
Primary key:
- Season, TeamID

Required columns:
- same feature schema as champion_core_historical, without label columns

Required filter:
- is_tourney_team = 1

### 5) champion_extended_2026.csv
Same schema pattern as core 2026 with extended set.

### 6) champion_experimental_2026.csv
Same schema pattern as core 2026 with experimental set.

## Manifest Sheets

### 1) schema_manifest.csv
Columns:
- sheet_name
- model_family (shared, bracket, champion)
- feature_set (core, extended, experimental, labels, targets)
- key_columns
- target_columns
- season_scope (historical/2026)

### 2) build_manifest.csv
Columns:
- run_timestamp
- source_master_hash_or_rowcount
- source_scorecard_path
- source_locked_set_paths
- output_sheet
- output_rows
- output_columns
- qa_status

## Build Order (Planned)

1. Build shared team-season sheets (historical/2026 by set)
2. Build tournament_team_labels_historical
3. Build bracket historical target sheet
4. Build bracket feature sheets (historical, then 2026)
5. Build champion sheets (historical, then 2026)
6. Write schema_manifest and build_manifest

## QA Requirements

Every model-ready sheet must pass:
- primary key uniqueness check
- expected columns check against schema contract
- null checks on key columns
- set hierarchy check (core subset of extended subset of experimental)
- historical/2026 schema parity within each model family
- leakage check:
  - no tournament outcome labels present in any 2026/inference sheet

## Confirmed Modeling Conventions

- Use explicit 2026 suffixes for inference-year sheets.
- Use slot-based keys for bracket inference sheets (`Season`, `Slot`) as the primary game identifier.
- Default champion predictor datasets to tournament teams only (`is_tourney_team = 1`).

## Decision Rule on Single Folder vs Model Subfolders

Decision:
- Use model subfolders under Model Ready Data for clarity and lower operational risk.

Reason:
- Bracket and champion sheets have different grains and targets.
- Shared sheets avoid duplication while preserving separation of concerns.
