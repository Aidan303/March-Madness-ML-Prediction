from __future__ import annotations

from pathlib import Path
import sys
import pandas as pd

HERE = Path(__file__).resolve().parent
TEAM_CSV = HERE / "Full_Stat_Package_Team.csv"

TEAM_NON_PBP_TOKENS = {"Team Game", "Team Agg"}
TEAM_PBP_TOKENS = {"Team Game PBP", "Team Agg PBP"}
VALID_DATA_SOURCES = {"box_score", "pbp", "box_score, pbp", "kenpom"}


def parse_available_in(raw: object) -> list[str]:
    if not isinstance(raw, str) or not raw.strip():
        return []
    return [token.strip() for token in raw.split(",") if token.strip()]


def is_kenpom_stat(abbrev: object) -> bool:
    if not isinstance(abbrev, str):
        return False
    short = abbrev.strip()
    return short.endswith(" Adj") or short.endswith("**Adj")


def classify_row(abbrev: object, available_in: object) -> str:
    if is_kenpom_stat(abbrev):
        return "kenpom"

    tokens = set(parse_available_in(available_in))
    has_non_pbp_team = bool(tokens.intersection(TEAM_NON_PBP_TOKENS))
    has_pbp_team = bool(tokens.intersection(TEAM_PBP_TOKENS))

    if has_non_pbp_team and has_pbp_team:
        return "box_score, pbp"
    if has_non_pbp_team:
        return "box_score"
    if has_pbp_team:
        return "pbp"
    return ""


def main() -> None:
    df = pd.read_csv(TEAM_CSV)

    df["Data Source"] = [
        classify_row(abbrev, available_in)
        for abbrev, available_in in zip(df["Abbrev"], df["Available In"])
    ]

    df.to_csv(TEAM_CSV, index=False)

    counts = df["Data Source"].value_counts(dropna=False)
    print("Updated Data Source classification counts:")
    for key, value in counts.items():
        print(f"  {key or '<blank>'}: {value}")

    blank_mask = df["Data Source"].isna() | (df["Data Source"].astype(str).str.strip() == "")
    invalid_mask = ~blank_mask & ~df["Data Source"].isin(VALID_DATA_SOURCES)

    blank_count = int(blank_mask.sum())
    invalid_count = int(invalid_mask.sum())

    if blank_count == 0 and invalid_count == 0:
        print("Validation PASSED: all rows have a valid Data Source value.")
        return

    print("Validation FAILED:")
    print(f"  Blank Data Source rows   : {blank_count}")
    print(f"  Invalid Data Source rows : {invalid_count}")

    if blank_count > 0:
        print("\nSample blank rows (up to 10):")
        sample_blank = df.loc[blank_mask, ["Abbrev", "Stat Name", "Available In"]].head(10)
        for _, row in sample_blank.iterrows():
            print(f"  {row['Abbrev']} | {row['Stat Name']} | {row['Available In']}")

    if invalid_count > 0:
        print("\nSample invalid rows (up to 10):")
        sample_invalid = df.loc[invalid_mask, ["Abbrev", "Stat Name", "Available In", "Data Source"]].head(10)
        for _, row in sample_invalid.iterrows():
            print(
                f"  {row['Abbrev']} | {row['Stat Name']} | "
                f"{row['Available In']} | Data Source={row['Data Source']}"
            )

    sys.exit(1)


if __name__ == "__main__":
    main()
