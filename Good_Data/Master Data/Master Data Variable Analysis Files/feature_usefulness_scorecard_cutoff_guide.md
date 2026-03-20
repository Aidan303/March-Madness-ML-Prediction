# Feature Usefulness Scorecard Cutoff Guide

This guide defines how to fill and interpret the scorecard file:
- Good_Data/Master Data/feature_usefulness_scorecard_template.csv

No cutoffs are applied automatically. This is a post-analysis interpretation standard only.

## Significance Band
Based on FDR-adjusted q-value from univariate tests.
- strong: q < 0.01
- moderate: 0.01 <= q < 0.05
- weak: 0.05 <= q < 0.10
- not_significant: q >= 0.10

## Univariate Predictive Band
Based on binary-target AUC and log-loss lift versus baseline.
- strong: AUC >= 0.60 and log-loss lift >= 3.0%
- moderate: AUC >= 0.56 and log-loss lift >= 1.0%
- weak: AUC >= 0.53 and log-loss lift >= 0.25%
- near_noise: below weak thresholds

## Multivariate Band
Based on permutation/SHAP percentile and single-feature ablation effect.
- core_level: median importance percentile >= 80 and ablation delta >= 0.75%
- useful: percentile 60-79 and ablation delta 0.30%-0.74%
- situational: percentile 40-59 and ablation delta 0.10%-0.29%
- low: below situational thresholds

## Stability Band
Based on walk-forward fold behavior.
- stable: sign stability >= 80% and importance rank std <= 15
- mostly_stable: sign stability 65%-79% or rank std 16-25
- unstable: sign stability < 65% or rank std > 25

## Overall Recommendation Label
Fill after all scorecard columns are populated.
- core: strong multivariate contribution and stable over time
- strong_but_unstable: high contribution with weak stability
- situational: useful for specific target family or rounds
- low_value: minimal signal across targets and models

## Target-Specific Interpretation
- game target columns: use tournament matchup winner labels
- champion target columns: use champion-only labels (highly imbalanced)
- roundflags columns: aggregate utility across Sweet16+, Elite8+, Final4+, Champion flags

## Reminder
- Keep all variables during full analysis.
- Do not prune duplicates or near-duplicates until scorecard is complete and reviewed.
