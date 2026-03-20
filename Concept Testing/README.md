# Concept Testing

## Purpose
This folder contains exploratory scripts, comparison generators, and intermediate experimentation outputs.

## Scope
- Prototype modeling experiments.
- Comparative analytics scripts.
- Utility scripts used to format or enrich observer-facing reports.

## Key Scripts
- [model_family_sweep_bracket.py](model_family_sweep_bracket.py)
- [Clustering_Testing.py](Clustering_Testing.py)
- [Linear_Regression_Testing.py](Linear_Regression_Testing.py)
- [Regularized_Regression_Testing.py](Regularized_Regression_Testing.py)
- [add_separator_columns.ps1](add_separator_columns.ps1)
- [highlight_bracket_disagreements.ps1](highlight_bracket_disagreements.ps1)
- [add_late_round_matchup_columns.ps1](add_late_round_matchup_columns.ps1)

## Related Writeups
- [Modeling_Findings_Writeup.md](Modeling_Findings_Writeup.md)
- [Modeling_Findings_Writeup_Iteration2.md](Modeling_Findings_Writeup_Iteration2.md)

## Observer Note
These scripts are useful for analysis and presentation, but they are not the canonical production entrypoints. Production runs should be executed from branch production scripts under [../Model Creation](../Model%20Creation), [../Model Creation Weighted Points](../Model%20Creation%20Weighted%20Points), and [../Updated Feature List Model Creation](../Updated%20Feature%20List%20Model%20Creation).

## Practical Usage
- Use these scripts to regenerate comparison presentation formatting after new 2026 production outputs are generated.
- Keep production-inference execution in branch production folders to avoid run-path confusion.

