import pandas as pd
from pathlib import Path

DIR = Path("Good_Data/march-machine-learning-mania-2026")

def load(name, n=None):
    p = DIR / name
    return pd.read_csv(p, nrows=n) if n else pd.read_csv(p)

def check_pk(name, cols, sample=None):
    df = load(name, sample)
    total = len(df)
    dupes = int(df.duplicated(subset=cols).sum())
    nulls = int(df[cols].isnull().any(axis=1).sum())
    status = "PASS" if dupes == 0 and nulls == 0 else "FAIL"
    return dict(table=name, pk="+".join(cols), rows_checked=total,
                duplicate_keys=dupes, null_in_key=nulls, status=status)

def check_fk(child_name, child_col, parent_name, parent_col):
    child = load(child_name)
    parent = load(parent_name)
    valid = set(parent[parent_col].astype(str))
    orphans = int((~child[child_col].astype(str).isin(valid)).sum())
    status = "PASS" if orphans == 0 else "FAIL"
    return dict(child=child_name, child_col=child_col, parent=parent_name,
                parent_col=parent_col, rows_checked=len(child),
                orphan_rows=orphans, status=status)

pk_checks = [
    check_pk("MTeams.csv",                          ["TeamID"]),
    check_pk("MSeasons.csv",                         ["Season"]),
    check_pk("Conferences.csv",                      ["ConfAbbrev"]),
    check_pk("Cities.csv",                           ["CityID"]),
    check_pk("MTeamSpellings.csv",                   ["TeamNameSpelling"]),
    check_pk("MTeamConferences.csv",                 ["Season", "TeamID"]),
    check_pk("MNCAATourneySeeds.csv",                ["Season", "TeamID"]),
    check_pk("MNCAATourneySlots.csv",                ["Season", "Slot"]),
    check_pk("MNCAATourneySeedRoundSlots.csv",       ["Seed", "GameRound"]),
    check_pk("MTeamCoaches.csv",                     ["Season", "TeamID", "FirstDayNum"]),
    check_pk("MSecondaryTourneyTeams.csv",           ["Season", "SecondaryTourney", "TeamID"]),
    check_pk("MRegularSeasonCompactResults.csv",     ["Season", "DayNum", "WTeamID", "LTeamID"], sample=100),
    check_pk("MRegularSeasonDetailedResults.csv",    ["Season", "DayNum", "WTeamID", "LTeamID"], sample=100),
    check_pk("MNCAATourneyCompactResults.csv",       ["Season", "DayNum", "WTeamID", "LTeamID"]),
    check_pk("MNCAATourneyDetailedResults.csv",      ["Season", "DayNum", "WTeamID", "LTeamID"]),
    check_pk("MMasseyOrdinals.csv",                  ["Season", "RankingDayNum", "SystemName", "TeamID"], sample=100),
    check_pk("MGameCities.csv",                      ["Season", "DayNum", "WTeamID", "LTeamID"], sample=100),
    check_pk("MConferenceTourneyGames.csv",          ["Season", "DayNum", "WTeamID", "LTeamID"]),
    check_pk("MSecondaryTourneyCompactResults.csv",  ["Season", "DayNum", "WTeamID", "LTeamID"]),
]

fk_checks = [
    check_fk("MTeamConferences.csv",               "TeamID",      "MTeams.csv",      "TeamID"),
    check_fk("MTeamConferences.csv",               "ConfAbbrev",  "Conferences.csv", "ConfAbbrev"),
    check_fk("MTeamConferences.csv",               "Season",      "MSeasons.csv",    "Season"),
    check_fk("MNCAATourneySeeds.csv",              "TeamID",      "MTeams.csv",       "TeamID"),
    check_fk("MNCAATourneySeeds.csv",              "Season",      "MSeasons.csv",     "Season"),
    check_fk("MTeamCoaches.csv",                   "TeamID",      "MTeams.csv",       "TeamID"),
    check_fk("MTeamCoaches.csv",                   "Season",      "MSeasons.csv",     "Season"),
    check_fk("MGameCities.csv",                    "CityID",      "Cities.csv",       "CityID"),
    check_fk("MConferenceTourneyGames.csv",        "ConfAbbrev",  "Conferences.csv",  "ConfAbbrev"),
    check_fk("MNCAATourneyCompactResults.csv",     "WTeamID",     "MTeams.csv",       "TeamID"),
    check_fk("MNCAATourneyCompactResults.csv",     "LTeamID",     "MTeams.csv",       "TeamID"),
    check_fk("MRegularSeasonCompactResults.csv",   "WTeamID",     "MTeams.csv",       "TeamID"),
    check_fk("MRegularSeasonCompactResults.csv",   "LTeamID",     "MTeams.csv",       "TeamID"),
    check_fk("MMasseyOrdinals.csv",                "TeamID",      "MTeams.csv",       "TeamID"),
    check_fk("MSecondaryTourneyCompactResults.csv","WTeamID",     "MTeams.csv",       "TeamID"),
    check_fk("MSecondaryTourneyCompactResults.csv","LTeamID",     "MTeams.csv",       "TeamID"),
]

pk_df = pd.DataFrame(pk_checks)
fk_df = pd.DataFrame(fk_checks)

print("=== PRIMARY KEY CHECKS ===")
print(pk_df.to_string(index=False))
print()
print("=== FOREIGN KEY CHECKS ===")
print(fk_df.to_string(index=False))
print()
pk_pass = (pk_df.status == "PASS").all()
fk_pass = (fk_df.status == "PASS").all()
print(f"PK overall: {'ALL PASS' if pk_pass else 'FAILURES FOUND'}")
print(f"FK overall: {'ALL PASS' if fk_pass else 'FAILURES FOUND'}")
