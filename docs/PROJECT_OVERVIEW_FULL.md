# March Madness Prediction Modeling Project - Full Technical Overview

## 1. Project Overview
This project is an end-to-end machine learning system for predicting NCAA Men's March Madness outcomes. It combines multi-source college basketball data, engineered team-level features, calibrated classification models, and bracket simulation logic to generate:

- Game-by-game tournament win probabilities
- Full bracket advancement predictions
- Team-level championship probability rankings

The system is designed for practical annual use: retrain on all available historical seasons, ingest current-season data, and produce tournament predictions once official seeds and slots are released.

## 2. Why This Project Matters
March Madness is a high-variance prediction environment with structural constraints:

- Single-elimination tournament creates high uncertainty and upset risk
- Bracket dependency means each game prediction changes future matchups
- Available data evolves over time, especially around Selection Sunday and First Four results

This project addresses those challenges with production-style data validation, versioned feature locking, explicit run gates, and simulation logic that mirrors real bracket flow.

## 3. Core Objectives
The project was built to meet five main goals:

1. Build one consistent, model-ready dataset across many seasons
2. Train robust tournament prediction models using only pre-game information
3. Generate full-bracket predictions that propagate model choices round-by-round
4. Produce interpretable outputs for technical and non-technical audiences
5. Support repeatable yearly execution with minimal manual intervention

## 4. Data Sources and Scope
### Historical Scope
- Seasons used: 2003 onward (excluding 2020 due to tournament cancellation)
- Historical training data includes regular season and tournament outcomes

### Current-Season Scope
- Dedicated 2026 current-season pipeline executed for live prediction
- Current season processing mirrors historical schema to prevent train/inference drift

### Main Data Domains
- Team metadata and IDs
- Tournament seeds and slot structure
- Historical tournament results
- Team performance and strength metrics (including KenPom-derived inputs)

Data files are managed under the `Good_Data` folder, while model-ready outputs are written to structured subfolders for bracket and champion models.

## 5. Feature Engineering and Data Pipeline
The pipeline converts raw season data into standardized model inputs.

### Highlights
- Team-season feature table built for both historical and current seasons
- Delta-style matchup features generated as Team A minus Team B values
- Seed-aware features included (seed numbers and seed gap)
- Feature schema checks enforce consistency across historical and current data
- QA and pre-flight checks prevent invalid or incomplete runs

### 2026 Execution Design
A dedicated 2026 master feature build script uses the same logic as historical builds. This enabled successful 2026 model-ready rebuilds and production inference runs without ad hoc feature changes.

## 6. Modeling Approach
Two calibrated binary classifiers are used:

### A. Bracket Game Model
- Predicts probability that Team A wins each matchup
- Trained on historical tournament game rows
- Uses locked feature set and calibration choice from a model manifest

### B. Champion Model
- Predicts each tournament team's probability of winning the national title
- Trained on historical team-season rows with championship labels

### Model Governance
- Model and feature configuration is loaded from a lock manifest
- Feature sets are frozen in gold/pruned files
- Training seasons are programmatically selected based on target inference season

This setup is designed to support reproducibility and controlled iteration.

## 7. Bracket Simulation Logic
A key engineering component is the bracket simulator.

### Production Simulation Behavior
- Slots are resolved in strict round order
- Winners feed into future slots through a slot winner map
- No future game is resolved from real outcomes once simulation begins

### First Four Handling
The final production logic intentionally treats First Four games as known inputs:

- Play-in winners are pulled from actual First Four results
- Round of 64 onward is fully model-driven
- This matches a practical prediction workflow where final 64 teams are known before full bracket lock submission

This design removes unnecessary uncertainty from play-in games while preserving full predictive challenge for the main bracket.

## 8. Inference and Operational Workflow
The inference script supports:

- Live-season mode (2026) with strict readiness gates
- Historical simulation mode (for backtesting years like 2025, 2024, 2023)

### Live Run Gating (2026)
The script blocks execution until required prerequisites are present:

- Seeds available
- Slots available
- First Four results available
- Model-ready bracket/champion current-season files available

This prevents accidental runs on partial data.

## 9. Evaluation Strategy
Backtesting is performed by rerunning historical seasons as if they were live.

A winner-only scoring framework was used for recent validation:

- Correctness based on winner sets by round (participant mismatch in later rounds does not auto-penalize winner calls)
- Weighted bracket scoring by round:
  - Round of 64: 1 point per correct winner
  - Round of 32: 2 points
  - Sweet 16: 4 points
  - Elite 8: 8 points
  - Final Four: 16 points
  - Championship: 32 points

### Recent Backtest Snapshot
- 2025: strong performance, high weighted score
- 2024: moderate performance
- 2023: weaker performance, showing year-to-year volatility

This variance reflects the true difficulty of tournament prediction and highlights calibration and upset modeling as high-impact improvement areas.

## 10. Explainability and Presentation
To improve usability beyond raw CSV output, the project includes text-based bracket interpretation utilities:

- Reads prediction CSVs and renders human-readable bracket views
- Supports both modern slot-based outputs and legacy formats
- Groups output by tournament rounds for easy review

This makes results easier to audit and present to non-technical audiences.

## 11. Engineering Practices Demonstrated
This project demonstrates production-minded ML engineering skills:

- End-to-end data pipeline design
- Feature schema governance and drift prevention
- Configuration-driven model loading and locking
- Pre-flight run validation and defensive checks
- Simulation correctness and dependency propagation
- Reproducible historical backtesting
- Clear separation of raw data, model-ready data, scripts, and results

## 12. Business and Product Value
Potential practical use cases include:

- Bracket support tools for fans and analysts
- Scenario planning for media coverage
- Educational demonstrations of predictive modeling under uncertainty
- Portfolio demonstration of applied ML engineering in a dynamic domain

The system is intentionally built so it can be operated each season with predictable steps instead of one-off notebook experimentation.

## 13. Project Structure (High Level)
- Good_Data: cleaned datasets, base competition files, and model-ready inputs
- Model Creation: scripts, configs, locked manifests, and production results
- Concept Testing: experimentation scripts used during development

## 14. Tools and Technologies
- Python
- Pandas and NumPy for data processing
- Scikit-learn for model training and calibration
- File-based manifest/config design for reproducible model operation

## 15. Current Status and Next Milestone
### Current Status
- 2026 pipeline and inference flow are fully wired and executed
- Historical validation runs are complete
- Production outputs for all three branches are generated and available for review

### Next Milestone
For future reruns after any late data changes:

1. Refresh seeds, slots, and First Four results
2. Rebuild model-ready current-season tables
3. Re-run 2026 inference
4. Export bracket and champion predictions
5. Generate readable bracket summary for final review

## 16. Recruiter Summary
This project showcases strong applied ML and data engineering execution in a difficult prediction setting. It combines modeling, data quality control, simulation correctness, and operational readiness in a way that mirrors real production workflows. The work demonstrates not only algorithm development, but also reliability engineering, reproducibility, and communication-focused output design.
