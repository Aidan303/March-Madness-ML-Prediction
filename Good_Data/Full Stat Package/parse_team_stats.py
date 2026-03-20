from __future__ import annotations

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# Paths (relative to this script's location)
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
INPUT_CSV  = HERE / "Full_Stat_Package.csv"
OUTPUT_CSV = HERE / "Full_Stat_Package_Team.csv"

# ---------------------------------------------------------------------------
# Acceptable team-level usage tokens
# Edit this set to change which usages qualify as "team based".
# All 10 unique tokens found in the source CSV:
#   Lineup, On/Off, Player Agg, Player Agg PBP,
#   Player Game, Player Game PBP,
#   Team Agg, Team Agg PBP, Team Game, Team Game PBP
# ---------------------------------------------------------------------------
ACCEPTABLE_TEAM_USES: set[str] = {
    "Team Game",
    "Team Agg",
    "Team Game PBP",
    "Team Agg PBP",
}


def parse_available_in(raw: str) -> list[str]:
    """Split a comma-separated 'Available In' cell into individual usage tokens."""
    if not isinstance(raw, str) or not raw.strip():
        return []
    return [token.strip() for token in raw.split(",") if token.strip()]


def is_team_stat(available_in_str: str) -> bool:
    """Return True if any token in the cell matches an acceptable team usage."""
    tokens = parse_available_in(available_in_str)
    return any(token in ACCEPTABLE_TEAM_USES for token in tokens)


def main() -> None:
    df = pd.read_csv(INPUT_CSV)

    team_mask = df["Available In"].apply(is_team_stat)
    team_df   = df[team_mask].reset_index(drop=True)

    team_df.to_csv(OUTPUT_CSV, index=False)

    total    = len(df)
    kept     = len(team_df)
    excluded = total - kept
    print(f"Source rows  : {total}")
    print(f"Team stats   : {kept}  -> {OUTPUT_CSV.name}")
    print(f"Excluded     : {excluded}  (player-only or unclassified)")


if __name__ == "__main__":
    main()
