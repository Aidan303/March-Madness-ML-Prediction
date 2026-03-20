# Locked Feature Sets
These sets are frozen outputs from the current scorecard and are intended for model training/testing experiments.
## Lock Rules Used
- Core: strong predictors with strict redundancy pruning at |r| >= 0.90
- Extended: non-low-value predictors with lenient redundancy pruning at |r| >= 0.97
- Experimental: all audited predictors (no pruning)
- Mandatory in all sets: tourney_seed_num

## Counts
- Core features: 15
- Extended features: 57
- Experimental features: 70

## Top Core Features (by rank_score)
- kp_adjem (group=kenpom, avg_perm=97.9, max_auc=0.930)
- tourney_seed_num (group=identity_or_label, avg_perm=92.7, max_auc=0.930)
- kp_adjoe (group=kenpom, avg_perm=89.9, max_auc=0.878)
- rs_pf (group=regular_season, avg_perm=89.5, max_auc=0.646)
- rs_drb (group=regular_season, avg_perm=76.2, max_auc=0.706)
- rs_ft_pct (group=regular_season, avg_perm=74.0, max_auc=0.627)
- rs_opp_blk (group=regular_season, avg_perm=68.6, max_auc=0.546)
- rs_ast_to_ratio (group=regular_season, avg_perm=70.2, max_auc=0.703)
- lms_residual_std (group=engineered_lms, avg_perm=71.0, max_auc=0.596)
- rs_ft_rate (group=regular_season, avg_perm=61.0, max_auc=0.551)
- rs_opp_ft_pct (group=regular_season, avg_perm=56.5, max_auc=0.602)
- kp_rankadjde (group=kenpom, avg_perm=44.3, max_auc=0.801)
- rs_win_pct (group=regular_season, avg_perm=33.9, max_auc=0.873)
- kp_rankoe (group=kenpom, avg_perm=43.7, max_auc=0.866)
- rs_fgm (group=regular_season, avg_perm=28.5, max_auc=0.793)
