# Master Features Dataset Overview

## Dataset
- **File:** `Good_Data/Master Data/Master CSV File and Support Files/master_features_all_teams_historical.csv`
- **Grain:** One row per `Season + TeamID`
- **Coverage:** 2003-2025, excluding 2020 (no NCAA tournament)
- **Rows:** 7,628
- **Columns:** 75
- **Unique Teams:** 371
- **Tournament Team-Seasons:** 1,472 (~66.9 per season)

## Purpose
This dataset is the unified modeling table for March Madness prediction work. It combines:
- Pre-tournament KenPom summary metrics
- Regular-season game-derived team statistics
- Tournament seed labels
- Conference context
- A custom consistency/upset-risk feature family (LMS)

The dataset is designed to support both:
- Team strength modeling
- Upset risk modeling for seed-based matchups

## Data Sources in Project Space

### 1) Good data (Kaggle base tables)
Folder:
- `Good_Data/march-machine-learning-mania-2026-base-data/`

Tables used:
- `MTeams.csv`
- `MTeamSpellings.csv`
- `MTeamConferences.csv`
- `MNCAATourneySeeds.csv`
- `MRegularSeasonCompactResults.csv`
- `MRegularSeasonDetailedResults.csv`
- `MNCAATourneyCompactResults.csv`

### 2) KenPom pre-tournament table from prior data assets
File:
- `Bad Data/Historic Data/Kenpom Data/Stats Tables/INT _ KenPom _ Summary (Pre-Tournament).csv`

This source is included because it is explicitly pre-tournament and adds advanced efficiency variables not present in the Kaggle base tables as raw metrics.

### 3) Build script
File:
- `Good_Data/Master Data/Master CSV File and Support Files/build_master_features.py`

## Build Method

### Step 1: Base roster of team-seasons
- Start from `MTeamConferences.csv`
- Keep all D1 teams per season in 2003-2025 (excluding 2020)
- Join `MTeams.csv` for canonical team names

### Step 2: KenPom merge
- Load pre-tournament KenPom summary table
- Resolve `TeamName -> TeamID` via:
  - direct match against `MTeams.TeamName`
  - alias match via `MTeamSpellings.TeamNameSpelling`
  - manual alias map for unresolved historical naming differences
- Merge on `Season, TeamID`

### Step 3: Regular-season aggregation
- Use `MRegularSeasonDetailedResults.csv`
- Convert to two-perspective long form (winner and loser perspective) so each game contributes one row per team
- Aggregate to team-season means and derived rates

### Step 4: Engineered LMS features (consistency/upset-risk family)
- Use `MRegularSeasonCompactResults.csv` for full regular-season game coverage
- Create team-perspective game margins
- Join opponent quality proxy via season-level `kp_rankadjem`
- Regress game margin on opponent rank percentile per team-season
- Generate LMS metrics:
  - `lms_slope`
  - `lms_r2`
  - `lms_residual_std`
  - `lms_consistency`
  - `lms_margin_vs_weak_surplus`

### Step 5: Tournament label merge
- Join `MNCAATourneySeeds.csv`
- Add:
  - `is_tourney_team` (0/1)
  - `tourney_seed_num` (numeric seed extracted from seed string)

## Feature Groups (75 total)
- **Identity/labels (6):** season, team identifiers, conference, tournament flags
- **KenPom features (14):** tempo/offense/defense/efficiency (raw + adjusted + rank)
- **Regular-season features (50):** scoring, shooting splits, rebound rates, turnover rates, four-factor style rates, opponent splits
- **LMS engineered features (5):** consistency and opponent-level dependence signals

## Leakage Controls
- Only pre-tournament information is used for team features.
- Tournament results are not used as master feature inputs.

## Coverage and Quality Notes
- KenPom coverage is 99.9% of team-seasons in this period.
- LMS coverage is effectively complete (requires enough games/opponent rank context).
- 2020 is excluded due to canceled tournament.

## Rebuild Command
From project root:

```powershell
python "Good_Data/Master Data/Master CSV File and Support Files/build_master_features.py"
```

## Intended Next Use
- Train matchup-level models (higher-seed upset probability, round advancement, champion probability)
- Use LMS features as interaction terms with seed gap and opponent quality metrics
- Compare model behavior with and without LMS for upset sensitivity analysis

## Model-Ready Column Dictionary (77 Columns)

### Identity and Labels (6)
- `Season`: NCAA season year.
- `TeamID`: Kaggle canonical team identifier.
- `TeamName`: Canonical team name from `MTeams`.
- `ConfAbbrev`: Conference abbreviation for that season.
- `is_tourney_team`: 1 if team received an NCAA tournament seed, else 0.
- `tourney_seed_num`: Numeric NCAA seed (1-16), null for non-tournament teams.

### KenPom Pre-Tournament Features (14)
- `kp_tempo`: Raw tempo estimate.
- `kp_ranktempo`: National rank of raw tempo.
- `kp_adjtempo`: Adjusted tempo.
- `kp_rankadjtempo`: National rank of adjusted tempo.
- `kp_oe`: Raw offensive efficiency.
- `kp_rankoe`: National rank of raw offensive efficiency.
- `kp_adjoe`: Adjusted offensive efficiency.
- `kp_rankadjoe`: National rank of adjusted offensive efficiency.
- `kp_de`: Raw defensive efficiency.
- `kp_rankde`: National rank of raw defensive efficiency.
- `kp_adjde`: Adjusted defensive efficiency.
- `kp_rankadjde`: National rank of adjusted defensive efficiency.
- `kp_adjem`: Adjusted efficiency margin (`AdjOE - AdjDE`).
- `kp_rankadjem`: National rank of adjusted efficiency margin.

### Regular-Season Aggregate Box Score Features (50)
- `rs_games`: Number of regular-season games in detailed results.
- `rs_wins`: Number of regular-season wins.
- `rs_avg_pts_for`: Average points scored per game.
- `rs_avg_pts_against`: Average points allowed per game.
- `rs_avg_margin`: Average scoring margin per game.
- `rs_margin_std`: Standard deviation of game margins.
- `rs_fgm`: Average field goals made per game.
- `rs_fga`: Average field goals attempted per game.
- `rs_fgm3`: Average 3-point field goals made per game.
- `rs_fga3`: Average 3-point field goals attempted per game.
- `rs_ftm`: Average free throws made per game.
- `rs_fta`: Average free throws attempted per game.
- `rs_orb`: Average offensive rebounds per game.
- `rs_drb`: Average defensive rebounds per game.
- `rs_ast`: Average assists per game.
- `rs_to`: Average turnovers per game.
- `rs_stl`: Average steals per game.
- `rs_blk`: Average blocks per game.
- `rs_pf`: Average personal fouls per game.
- `rs_opp_fgm`: Average opponent field goals made per game.
- `rs_opp_fga`: Average opponent field goals attempted per game.
- `rs_opp_fgm3`: Average opponent 3-point field goals made per game.
- `rs_opp_fga3`: Average opponent 3-point field goals attempted per game.
- `rs_opp_ftm`: Average opponent free throws made per game.
- `rs_opp_fta`: Average opponent free throws attempted per game.
- `rs_opp_or`: Average opponent offensive rebounds per game.
- `rs_opp_dr`: Average opponent defensive rebounds per game.
- `rs_opp_ast`: Average opponent assists per game.
- `rs_opp_to`: Average opponent turnovers per game.
- `rs_opp_stl`: Average opponent steals per game.
- `rs_opp_blk`: Average opponent blocks per game.
- `rs_opp_pf`: Average opponent personal fouls per game.
- `rs_win_pct`: Regular-season win percentage.
- `rs_fg_pct`: Field-goal percentage.
- `rs_fg3_pct`: 3-point field-goal percentage.
- `rs_ft_pct`: Free-throw percentage.
- `rs_fg2_pct`: 2-point field-goal percentage.
- `rs_efg_pct`: Effective field-goal percentage.
- `rs_to_rate`: Turnover rate per possession proxy.
- `rs_or_pct`: Offensive rebound rate.
- `rs_dr_pct`: Defensive rebound rate.
- `rs_ft_rate`: Free-throw rate (`FTA/FGA`).
- `rs_ast_to_ratio`: Assist-to-turnover ratio.
- `rs_opp_fg_pct`: Opponent field-goal percentage allowed.
- `rs_opp_fg3_pct`: Opponent 3-point percentage allowed.
- `rs_opp_ft_pct`: Opponent free-throw percentage allowed.
- `rs_opp_fg2_pct`: Opponent 2-point percentage allowed.
- `rs_opp_efg_pct`: Opponent effective field-goal percentage allowed.
- `rs_opp_to_rate`: Opponent turnover rate forced.
- `rs_opp_ft_rate`: Opponent free-throw rate allowed.

### Engineered LMS Consistency and Upset-Risk Features (5)
- `lms_slope`: OLS slope from `margin ~ opponent_rank_percentile`; higher means larger margins vs weaker opponents.
- `lms_r2`: Variance in game margin explained by opponent quality.
- `lms_residual_std`: Volatility of performance after controlling for opponent quality.
- `lms_consistency`: `1 - abs(correlation)` between margin and opponent quality; higher means more opponent-independent performance.
- `lms_margin_vs_weak_surplus`: Mean margin vs below-median opponents minus overall mean margin; higher suggests stat-padding vs weaker teams.
