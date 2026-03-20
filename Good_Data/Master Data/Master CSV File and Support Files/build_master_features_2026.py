"""
build_master_features_2026.py

Builds Good_Data/Master Data/Master CSV File and Support Files/master_features_all_teams_2026.csv

Covers all D1 men's basketball teams for Season 2026 only.
One row per TeamID.

Sources combined:
  - MTeamConferences           → base roster of all D1 teams for 2026
    - Sample Kenpom data for 2026.csv  → AdjEM, AdjOE, AdjDE, AdjTempo + raw values + ranks
                                                                                (single-header CSV)
  - MRegularSeasonDetailedResults    → aggregated box scores + four-factor rates per game
  - MNCAATourneySeeds                → tournament participation + numeric seed
                                        (will be NaN/0 until bracket is released)

Output schema is identical to master_features_all_teams_historical.csv (75 columns).
This file does NOT overwrite the validated historical master.

NOTE — Seeds:
  Selection Sunday is March 15, 2026. Re-run this script after appending 2026 rows
  to MNCAATourneySeeds.csv to populate is_tourney_team and tourney_seed_num.

NOTE — KenPom:
  Once the official pre-tournament KenPom CSV is available, append Season=2026 rows
  to Bad Data/Historic Data/Kenpom Data/Stats Tables/INT _ KenPom _ Summary (Pre-Tournament).csv
  and then the historical script will cover 2026 in future full rebuilds.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
_ROOT      = Path(__file__).resolve().parents[3]
KAGGLE     = _ROOT / 'Good_Data/march-machine-learning-mania-2026-base-data'
KENPOM_CSV = _ROOT / 'Good_Data/Sample Kenpom data for 2026.csv'
OUT_CSV    = (_ROOT / 'Good_Data/Master Data/Master CSV File and Support Files'
              / 'master_features_all_teams_2026.csv')

SEASON = 2026

# ── KenPom name → Kaggle TeamID manual aliases (carried over from historical) ─
KENPOM_MANUAL = {
    'ARKANSAS LITTLE ROCK':     1114,
    'ARKANSAS PINE BLUFF':      1115,
    'BETHUNE-COOKMAN':          1126,
    'BETHUNE COOKMAN':          1126,
    'CAL ST. BAKERSFIELD':      1167,
    'DIXIE ST.':                1469,
    'ILLINOIS CHICAGO':         1227,
    'LOUISIANA LAFAYETTE':      1418,
    'LOUISIANA MONROE':         1419,
    'MISSISSIPPI VALLEY ST.':   1290,
    'QUEENS':                   1474,
    'SAINT FRANCIS':            1384,
    'SOUTHEAST MISSOURI':       1369,
    'SOUTHEAST MISSOURI ST.':   1369,
    'SOUTHWEST MISSOURI ST.':   1283,
    'SOUTHWEST TEXAS ST.':      1402,
    'ST. FRANCIS NY':           1383,
    'ST. FRANCIS PA':           1384,
    'TARLETON ST.':             1470,
    'TENNESSEE MARTIN':         1404,
    'TEXAS A&M COMMERCE':       1477,
    'TEXAS A&M CORPUS CHRIS':   1394,
    'TEXAS A&M CORPUS CHRISTI': 1394,
    'TEXAS PAN AMERICAN':       1410,
    'UT RIO GRANDE VALLEY':     1410,
    'WINSTON-SALEM ST.':        1445,
    'WINSTON SALEM ST.':        1445,
    'WISCONSIN-GREEN BAY':      1453,
    'WISCONSIN GREEN BAY':      1453,
    'WISCONSIN-MILWAUKEE':      1454,
    'WISCONSIN MILWAUKEE':      1454,
}


def normed(s):
    return str(s).strip().upper()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Load raw data
# ─────────────────────────────────────────────────────────────────────────────
print("Loading raw data...")
teams     = pd.read_csv(KAGGLE / 'MTeams.csv')
confs_df  = pd.read_csv(KAGGLE / 'MTeamConferences.csv')
seeds_df  = pd.read_csv(KAGGLE / 'MNCAATourneySeeds.csv')
spellings = pd.read_csv(KAGGLE / 'MTeamSpellings.csv')
compact   = pd.read_csv(KAGGLE / 'MRegularSeasonCompactResults.csv')
detailed  = pd.read_csv(KAGGLE / 'MRegularSeasonDetailedResults.csv')

# Read the standard single-header CSV (Season, TeamName, Tempo, RankTempo, ..., Seed)
kenpom_raw = pd.read_csv(KENPOM_CSV)


# ─────────────────────────────────────────────────────────────────────────────
# 2. Resolve KenPom TeamName → Kaggle TeamID
# ─────────────────────────────────────────────────────────────────────────────
print("Resolving KenPom team names → TeamID...")
name_to_id = {normed(r.TeamName): r.TeamID for r in teams.itertuples()}
for r in spellings.itertuples():
    k = normed(r.TeamNameSpelling)
    if k not in name_to_id:
        name_to_id[k] = r.TeamID
name_to_id.update(KENPOM_MANUAL)

kenpom = kenpom_raw[kenpom_raw['Season'] == SEASON].copy()
kenpom['TeamID'] = kenpom['TeamName'].map(normed).map(name_to_id)

unresolved = kenpom[kenpom['TeamID'].isna()]['TeamName'].unique()
if len(unresolved):
    print(f"  WARNING: {len(unresolved)} KenPom names unresolved: {sorted(unresolved)}")
else:
    print("  All KenPom names resolved.")

kenpom = kenpom.dropna(subset=['TeamID'])
kenpom['TeamID'] = kenpom['TeamID'].astype(int)

kenpom_feat = kenpom[['Season', 'TeamID',
    'Tempo', 'RankTempo', 'AdjTempo', 'RankAdjTempo',
    'OE', 'RankOE', 'AdjOE', 'RankAdjOE',
    'DE', 'RankDE', 'AdjDE', 'RankAdjDE',
    'AdjEM', 'RankAdjEM',
]].copy()
kenpom_feat.columns = (
    ['Season', 'TeamID']
    + [f'kp_{c.lower()}' for c in kenpom_feat.columns[2:]]
)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Build base: all D1 team-seasons for 2026
# ─────────────────────────────────────────────────────────────────────────────
print("Building base table...")
base = (
    confs_df[confs_df['Season'] == SEASON]
    [['Season', 'TeamID', 'ConfAbbrev']].copy()
    .merge(teams[['TeamID', 'TeamName']], on='TeamID')
)
print(f"  Base rows: {len(base)}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Join KenPom features
# ─────────────────────────────────────────────────────────────────────────────
base = base.merge(kenpom_feat, on=['Season', 'TeamID'], how='left')
kp_coverage = base['kp_adjem'].notna().sum()
print(f"  KenPom coverage: {kp_coverage}/{len(base)} teams ({100*kp_coverage/len(base):.1f}%)")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Aggregate regular season detailed results
# ─────────────────────────────────────────────────────────────────────────────
print("Aggregating regular season box scores...")
det = detailed[detailed['Season'] == SEASON].copy()

_keep = ['Season', 'TeamID', 'OppID', 'pts_for', 'pts_against',
         'fgm', 'fga', 'fgm3', 'fga3', 'ftm', 'fta', 'orb', 'drb',
         'ast', 'to_', 'stl', 'blk', 'pf',
         'opp_fgm', 'opp_fga', 'opp_fgm3', 'opp_fga3',
         'opp_ftm', 'opp_fta', 'opp_or', 'opp_dr',
         'opp_ast', 'opp_to', 'opp_stl', 'opp_blk', 'opp_pf', 'win']

w_view = det.rename(columns={
    'WTeamID': 'TeamID', 'LTeamID': 'OppID',
    'WScore': 'pts_for',  'LScore': 'pts_against',
    'WFGM': 'fgm',   'WFGA': 'fga',   'WFGM3': 'fgm3',  'WFGA3': 'fga3',
    'WFTM': 'ftm',   'WFTA': 'fta',   'WOR': 'orb',      'WDR': 'drb',
    'WAst': 'ast',   'WTO': 'to_',    'WStl': 'stl',     'WBlk': 'blk',
    'WPF': 'pf',
    'LFGM': 'opp_fgm',  'LFGA': 'opp_fga',
    'LFGM3': 'opp_fgm3', 'LFGA3': 'opp_fga3',
    'LFTM': 'opp_ftm',  'LFTA': 'opp_fta',
    'LOR': 'opp_or',    'LDR': 'opp_dr',
    'LAst': 'opp_ast',  'LTO': 'opp_to',
    'LStl': 'opp_stl',  'LBlk': 'opp_blk',  'LPF': 'opp_pf',
}).assign(win=1)[_keep]

l_view = det.rename(columns={
    'LTeamID': 'TeamID', 'WTeamID': 'OppID',
    'LScore': 'pts_for',  'WScore': 'pts_against',
    'LFGM': 'fgm',   'LFGA': 'fga',   'LFGM3': 'fgm3',  'LFGA3': 'fga3',
    'LFTM': 'ftm',   'LFTA': 'fta',   'LOR': 'orb',      'LDR': 'drb',
    'LAst': 'ast',   'LTO': 'to_',    'LStl': 'stl',     'LBlk': 'blk',
    'LPF': 'pf',
    'WFGM': 'opp_fgm',  'WFGA': 'opp_fga',
    'WFGM3': 'opp_fgm3', 'WFGA3': 'opp_fga3',
    'WFTM': 'opp_ftm',  'WFTA': 'opp_fta',
    'WOR': 'opp_or',    'WDR': 'opp_dr',
    'WAst': 'opp_ast',  'WTO': 'opp_to',
    'WStl': 'opp_stl',  'WBlk': 'opp_blk',  'WPF': 'opp_pf',
}).assign(win=0)[_keep]

all_det = pd.concat([w_view, l_view], ignore_index=True)
all_det['margin'] = all_det['pts_for'] - all_det['pts_against']

g = all_det.groupby(['Season', 'TeamID'])
rs = g.agg(
    rs_games             = ('win',         'count'),
    rs_wins              = ('win',         'sum'),
    rs_avg_pts_for       = ('pts_for',     'mean'),
    rs_avg_pts_against   = ('pts_against', 'mean'),
    rs_avg_margin        = ('margin',      'mean'),
    rs_margin_std        = ('margin',      'std'),
    rs_fgm               = ('fgm',         'mean'),
    rs_fga               = ('fga',         'mean'),
    rs_fgm3              = ('fgm3',        'mean'),
    rs_fga3              = ('fga3',        'mean'),
    rs_ftm               = ('ftm',         'mean'),
    rs_fta               = ('fta',         'mean'),
    rs_orb               = ('orb',         'mean'),
    rs_drb               = ('drb',         'mean'),
    rs_ast               = ('ast',         'mean'),
    rs_to                = ('to_',         'mean'),
    rs_stl               = ('stl',         'mean'),
    rs_blk               = ('blk',         'mean'),
    rs_pf                = ('pf',          'mean'),
    rs_opp_fgm           = ('opp_fgm',     'mean'),
    rs_opp_fga           = ('opp_fga',     'mean'),
    rs_opp_fgm3          = ('opp_fgm3',    'mean'),
    rs_opp_fga3          = ('opp_fga3',    'mean'),
    rs_opp_ftm           = ('opp_ftm',     'mean'),
    rs_opp_fta           = ('opp_fta',     'mean'),
    rs_opp_or            = ('opp_or',      'mean'),
    rs_opp_dr            = ('opp_dr',      'mean'),
    rs_opp_ast           = ('opp_ast',     'mean'),
    rs_opp_to            = ('opp_to',      'mean'),
    rs_opp_stl           = ('opp_stl',     'mean'),
    rs_opp_blk           = ('opp_blk',     'mean'),
    rs_opp_pf            = ('opp_pf',      'mean'),
).reset_index()

# Derived rates
rs['rs_win_pct']        = rs['rs_wins']    / rs['rs_games']
rs['rs_fg_pct']         = rs['rs_fgm']     / rs['rs_fga']
rs['rs_fg3_pct']        = rs['rs_fgm3']    / rs['rs_fga3']
rs['rs_ft_pct']         = rs['rs_ftm']     / rs['rs_fta']
rs['rs_fg2_pct']        = (rs['rs_fgm'] - rs['rs_fgm3']) / (rs['rs_fga'] - rs['rs_fga3'])

rs['rs_efg_pct']        = (rs['rs_fgm'] + 0.5 * rs['rs_fgm3']) / rs['rs_fga']
rs['rs_to_rate']        = rs['rs_to'] / (rs['rs_fga'] + 0.44 * rs['rs_fta'] + rs['rs_to'])
rs['rs_or_pct']         = rs['rs_orb'] / (rs['rs_orb'] + rs['rs_opp_dr'])
rs['rs_dr_pct']         = rs['rs_drb'] / (rs['rs_drb'] + rs['rs_opp_or'])
rs['rs_ft_rate']        = rs['rs_fta'] / rs['rs_fga']
rs['rs_ast_to_ratio']   = rs['rs_ast'] / rs['rs_to'].replace(0, np.nan)

rs['rs_opp_fg_pct']     = rs['rs_opp_fgm']  / rs['rs_opp_fga']
rs['rs_opp_fg3_pct']    = rs['rs_opp_fgm3'] / rs['rs_opp_fga3']
rs['rs_opp_ft_pct']     = rs['rs_opp_ftm']  / rs['rs_opp_fta']
rs['rs_opp_fg2_pct']    = ((rs['rs_opp_fgm'] - rs['rs_opp_fgm3'])
                           / (rs['rs_opp_fga'] - rs['rs_opp_fga3']))
rs['rs_opp_efg_pct']    = (rs['rs_opp_fgm'] + 0.5 * rs['rs_opp_fgm3']) / rs['rs_opp_fga']
rs['rs_opp_to_rate']    = (rs['rs_opp_to']
                           / (rs['rs_opp_fga'] + 0.44 * rs['rs_opp_fta'] + rs['rs_opp_to']))
rs['rs_opp_ft_rate']    = rs['rs_opp_fta'] / rs['rs_opp_fga']

base = base.merge(rs, on=['Season', 'TeamID'], how='left')


# ─────────────────────────────────────────────────────────────────────────────
# 6. Level Maintenance Score (LMS)
# ─────────────────────────────────────────────────────────────────────────────
print("Computing Level Maintenance Score (LMS)...")

cmp = compact[compact['Season'] == SEASON].copy()

w_cmp = cmp[['Season', 'WTeamID', 'LTeamID', 'WScore', 'LScore']].rename(
    columns={'WTeamID': 'TeamID', 'LTeamID': 'OppID',
             'WScore': 'pts_for', 'LScore': 'pts_against'})
l_cmp = cmp[['Season', 'LTeamID', 'WTeamID', 'LScore', 'WScore']].rename(
    columns={'LTeamID': 'TeamID', 'WTeamID': 'OppID',
             'LScore': 'pts_for', 'WScore': 'pts_against'})
games_long = pd.concat([w_cmp, l_cmp], ignore_index=True)
games_long['margin'] = games_long['pts_for'] - games_long['pts_against']

# Opponent quality proxy: kp_rankadjem from the 2026 KenPom data in base
opp_quality = (base[['Season', 'TeamID', 'kp_rankadjem']]
               .rename(columns={'TeamID': 'OppID',
                                'kp_rankadjem': 'opp_rank'}))
games_long = games_long.merge(opp_quality, on=['Season', 'OppID'], how='left')
games_lms = games_long.dropna(subset=['opp_rank']).copy()

rank_max = games_lms.groupby('Season')['opp_rank'].transform('max')
rank_min = games_lms.groupby('Season')['opp_rank'].transform('min')
games_lms['opp_rank_pct'] = 1.0 - (games_lms['opp_rank'] - rank_min) / (rank_max - rank_min).replace(0, np.nan)


def _lms(grp):
    """OLS regression of margin ~ opp_rank_pct + derived consistency metrics."""
    if len(grp) < 5:
        return pd.Series({
            'lms_slope': np.nan, 'lms_r2': np.nan,
            'lms_residual_std': np.nan, 'lms_consistency': np.nan,
            'lms_margin_vs_weak_surplus': np.nan,
        })
    x = grp['opp_rank_pct'].values.astype(float)
    y = grp['margin'].values.astype(float)

    xm, ym = x.mean(), y.mean()
    ss_xx = np.sum((x - xm) ** 2)
    if ss_xx < 1e-10:
        return pd.Series({
            'lms_slope': np.nan, 'lms_r2': np.nan,
            'lms_residual_std': np.nan, 'lms_consistency': np.nan,
            'lms_margin_vs_weak_surplus': np.nan,
        })

    slope     = np.sum((x - xm) * (y - ym)) / ss_xx
    intercept = ym - slope * xm
    resid     = y - (slope * x + intercept)
    ss_res    = np.sum(resid ** 2)
    ss_tot    = np.sum((y - ym) ** 2)

    r2           = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    r            = np.sign(slope) * np.sqrt(max(0.0, r2)) if r2 is not np.nan else np.nan
    resid_std    = np.sqrt(ss_res / max(1, len(x) - 2))
    consistency  = 1.0 - abs(r) if r is not np.nan else np.nan

    median_q = np.median(x)
    weak_mask = x < median_q
    if weak_mask.sum() >= 3:
        surplus = float(y[weak_mask].mean() - ym)
    else:
        surplus = np.nan

    return pd.Series({
        'lms_slope':                  slope,
        'lms_r2':                     r2,
        'lms_residual_std':           resid_std,
        'lms_consistency':            consistency,
        'lms_margin_vs_weak_surplus': surplus,
    })


lms = (games_lms[['Season', 'TeamID', 'margin', 'opp_rank_pct']]
       .groupby(['Season', 'TeamID'])
       .apply(_lms, include_groups=False)
       .reset_index())
base = base.merge(lms, on=['Season', 'TeamID'], how='left')
print(f"  LMS computed for {lms['lms_slope'].notna().sum()}/{len(lms)} teams")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Tournament seeds
#    Will be all NaN/0 until Selection Sunday rows are added to MNCAATourneySeeds.csv
# ─────────────────────────────────────────────────────────────────────────────
print("Joining tournament seeds...")
seeds_sub = seeds_df[seeds_df['Season'] == SEASON].copy()
if len(seeds_sub) == 0:
    print("  No 2026 seeds found — is_tourney_team=0, tourney_seed_num=NaN for all teams.")
    print("  Re-run after appending 2026 rows to MNCAATourneySeeds.csv.")
else:
    print(f"  Found {len(seeds_sub)} seed rows for 2026.")

seeds_sub['tourney_seed_num'] = seeds_sub['Seed'].str.extract(r'(\d+)').astype(int)
seeds_sub = (seeds_sub[['Season', 'TeamID', 'tourney_seed_num']]
             .assign(is_tourney_team=1))
base = base.merge(seeds_sub, on=['Season', 'TeamID'], how='left')
base['is_tourney_team'] = base['is_tourney_team'].fillna(0).astype(int)


# ─────────────────────────────────────────────────────────────────────────────
# 8. Save
# ─────────────────────────────────────────────────────────────────────────────
id_cols  = ['Season', 'TeamID', 'TeamName', 'ConfAbbrev',
            'is_tourney_team', 'tourney_seed_num']
kp_cols  = [c for c in base.columns if c.startswith('kp_')]
rs_cols  = [c for c in base.columns if c.startswith('rs_')]
lms_cols = [c for c in base.columns if c.startswith('lms_')]
col_order = id_cols + kp_cols + rs_cols + lms_cols
base = base[col_order]

base.to_csv(OUT_CSV, index=False)
print(f"\nSaved: {OUT_CSV}")
print(f"Shape: {base.shape}  (1 season, {base['TeamID'].nunique()} unique teams)")
print(f"Columns: {len(base.columns)}")
print()
print("Column summary:")
print(f"  Identity / labels : {len(id_cols)}")
print(f"  KenPom features   : {len(kp_cols)}")
print(f"  Regular season    : {len(rs_cols)}")
print(f"  LMS (engineered)  : {len(lms_cols)}")

# Schema validation: ensure column count matches historical master
hist = pd.read_csv(
    _ROOT / 'Good_Data/Master Data/Master CSV File and Support Files/master_features_all_teams_historical.csv',
    nrows=1
)
hist_cols = list(hist.columns)
out_cols  = list(base.columns)
if hist_cols == out_cols:
    print("\nSchema check: PASS — columns match historical master exactly.")
else:
    missing = set(hist_cols) - set(out_cols)
    extra   = set(out_cols) - set(hist_cols)
    print(f"\nSchema check: WARN — mismatch found.")
    if missing:
        print(f"  Missing vs historical: {sorted(missing)}")
    if extra:
        print(f"  Extra vs historical:   {sorted(extra)}")
