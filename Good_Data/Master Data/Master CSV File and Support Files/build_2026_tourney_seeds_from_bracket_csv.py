from __future__ import annotations

import argparse
import difflib
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
KAGGLE_DIR = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"
INPUT_PATH = ROOT / "Good_Data" / "Data Support Files" / "NCAA_Bracket_Seeds_2026.csv"
OUTPUT_PATH = KAGGLE_DIR / "MNCAATourneySeeds.csv"
OVERRIDES_PATH = ROOT / "Good_Data" / "Data Support Files" / "team_name_manual_overrides_2026.json"

TARGET_SEASON = 2026
REGION_TO_CODE = {
    "east": "W",
    "south": "X",
    "midwest": "Y",
    "west": "Z",
}

# Common source-name variants that may not appear verbatim in Kaggle tables.
BUILTIN_NAME_ALIASES = {
    "queens": 1474,
}


def _normalize_name(value: str) -> str:
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", "", text)
    return text


def _normalize_region(value: str) -> str:
    return str(value).strip().lower()


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    for col in df.columns:
        key = re.sub(r"[^a-z0-9]+", "", str(col).strip().lower())
        rename_map[col] = key
    return df.rename(columns=rename_map)


def _parse_playin(value: object) -> bool:
    s = str(value).strip().lower()
    return s in {"yes", "y", "true", "1", "playin", "play-in"}


def _load_name_to_team_id() -> tuple[dict[str, int], dict[str, str]]:
    teams = pd.read_csv(KAGGLE_DIR / "MTeams.csv")
    spellings = pd.read_csv(KAGGLE_DIR / "MTeamSpellings.csv")

    name_to_id: dict[str, int] = {}
    norm_to_display: dict[str, str] = {}

    for r in teams.itertuples(index=False):
        norm = _normalize_name(r.TeamName)
        name_to_id[norm] = int(r.TeamID)
        norm_to_display[norm] = str(r.TeamName)

    for r in spellings.itertuples(index=False):
        norm = _normalize_name(r.TeamNameSpelling)
        if norm not in name_to_id:
            name_to_id[norm] = int(r.TeamID)
            norm_to_display[norm] = str(r.TeamNameSpelling)

    return name_to_id, norm_to_display


def _load_overrides() -> dict[str, int]:
    if not OVERRIDES_PATH.exists():
        return {}
    with OVERRIDES_PATH.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return {str(k): int(v) for k, v in raw.items()}


def _save_overrides(overrides: dict[str, int]) -> None:
    OVERRIDES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OVERRIDES_PATH.open("w", encoding="utf-8") as f:
        json.dump(dict(sorted(overrides.items())), f, indent=2)


def _suggest_names(query_norm: str, known_names: dict[str, str]) -> list[str]:
    candidates = list(known_names.keys())
    matches = difflib.get_close_matches(query_norm, candidates, n=8, cutoff=0.45)
    return [known_names[m] for m in matches]


def _resolve_team_id(
    raw_name: str,
    name_to_id: dict[str, int],
    norm_to_display: dict[str, str],
    overrides: dict[str, int],
    interactive: bool,
) -> int:
    norm = _normalize_name(raw_name)

    if norm in overrides:
        return overrides[norm]
    if norm in BUILTIN_NAME_ALIASES:
        return BUILTIN_NAME_ALIASES[norm]
    if norm in name_to_id:
        return name_to_id[norm]

    if not interactive:
        raise ValueError(f"Unmatched team name (non-interactive mode): {raw_name}")

    suggestions = _suggest_names(norm, norm_to_display)
    print("\nName match required")
    print(f"  Source team: {raw_name}")
    if suggestions:
        print("  Closest known names:")
        for i, s in enumerate(suggestions, start=1):
            print(f"    {i}. {s}")

    while True:
        response = input("Enter TeamID for this team (or 'skip' to abort): ").strip()
        if response.lower() == "skip":
            raise ValueError(f"Manual mapping skipped for team: {raw_name}")
        if response.isdigit():
            team_id = int(response)
            overrides[norm] = team_id
            return team_id
        print("Invalid input. Enter a numeric TeamID or 'skip'.")


def _validate_required_columns(df: pd.DataFrame) -> None:
    required = {"seed", "team", "region", "playinteam"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            "Missing required columns in NCAA_Bracket_Seeds_2026.csv: "
            + ", ".join(sorted(missing))
        )


def _build_2026_seed_rows(df_raw: pd.DataFrame, interactive: bool) -> tuple[pd.DataFrame, dict[str, int], int]:
    df = _normalize_columns(df_raw)
    _validate_required_columns(df)

    # Keep deterministic order from input for play-in a/b assignment.
    df = df.copy().reset_index(drop=False).rename(columns={"index": "input_order"})

    df["seed_num"] = pd.to_numeric(df["seed"], errors="coerce")
    if df["seed_num"].isna().any():
        bad = df[df["seed_num"].isna()][["seed", "team"]]
        raise ValueError(f"Non-numeric seed values found:\n{bad.to_string(index=False)}")

    df["seed_num"] = df["seed_num"].astype(int)
    out_of_range = df[~df["seed_num"].between(1, 16)]
    if len(out_of_range):
        raise ValueError(
            "Seed numbers must be in 1..16. Bad rows:\n"
            + out_of_range[["seed_num", "team", "region"]].to_string(index=False)
        )

    df["region_norm"] = df["region"].map(_normalize_region)
    unknown_region = df[~df["region_norm"].isin(REGION_TO_CODE.keys())]
    if len(unknown_region):
        raise ValueError(
            "Unknown region values found. Allowed: East, South, Midwest, West. Bad rows:\n"
            + unknown_region[["team", "region"]].to_string(index=False)
        )

    df["region_code"] = df["region_norm"].map(REGION_TO_CODE)
    df["is_playin"] = df["playinteam"].map(_parse_playin)

    name_to_id, norm_to_display = _load_name_to_team_id()
    overrides = _load_overrides()

    team_ids = []
    manual_count = 0
    for r in df.itertuples(index=False):
        before = len(overrides)
        team_id = _resolve_team_id(
            raw_name=r.team,
            name_to_id=name_to_id,
            norm_to_display=norm_to_display,
            overrides=overrides,
            interactive=interactive,
        )
        if len(overrides) > before:
            manual_count += 1
        team_ids.append(team_id)
    df["TeamID"] = team_ids

    _save_overrides(overrides)

    # Play-in handling: assign a/b by TeamID order per (region, seed).
    # Lower TeamID gets suffix 'a', higher TeamID gets suffix 'b'.
    playin = df[df["is_playin"]].copy()
    if len(playin):
        grp_sizes = playin.groupby(["region_code", "seed_num"]).size().reset_index(name="n")
        bad_sizes = grp_sizes[grp_sizes["n"] != 2]
        if len(bad_sizes):
            raise ValueError(
                "Play-in pairs must have exactly 2 teams per (Region, Seed). Bad groups:\n"
                + bad_sizes.to_string(index=False)
            )

    non_playin = df[~df["is_playin"]].copy()
    dup_non_playin = (
        non_playin.groupby(["region_code", "seed_num"]).size().reset_index(name="n")
    )
    dup_non_playin = dup_non_playin[dup_non_playin["n"] > 1]
    if len(dup_non_playin):
        raise ValueError(
            "Duplicate non-play-in teams for same (Region, Seed). Bad groups:\n"
            + dup_non_playin.to_string(index=False)
        )

    df = df.sort_values(["region_code", "seed_num", "TeamID", "input_order"]).copy()
    df["pair_idx"] = df.groupby(["region_code", "seed_num", "is_playin"]).cumcount()
    df["suffix"] = ""
    df.loc[df["is_playin"] & (df["pair_idx"] == 0), "suffix"] = "a"
    df.loc[df["is_playin"] & (df["pair_idx"] == 1), "suffix"] = "b"

    df["Seed"] = df["region_code"] + df["seed_num"].astype(str).str.zfill(2) + df["suffix"]

    seed_dupes = df[df.duplicated(subset=["Seed"], keep=False)].sort_values("Seed")
    if len(seed_dupes):
        raise ValueError("Duplicate Kaggle Seed values generated:\n" + seed_dupes[["Seed", "team"]].to_string(index=False))

    out = df[["Seed", "TeamID"]].copy()
    out.insert(0, "Season", TARGET_SEASON)
    out = out.sort_values(["Season", "Seed", "TeamID"]).reset_index(drop=True)

    return out, overrides, manual_count


def _replace_2026_rows(new_rows: pd.DataFrame, dry_run: bool) -> None:
    seeds = pd.read_csv(OUTPUT_PATH)
    before_total = len(seeds)
    before_2026 = int((seeds["Season"] == TARGET_SEASON).sum())

    kept = seeds[seeds["Season"] != TARGET_SEASON].copy()
    updated = pd.concat([kept, new_rows], ignore_index=True)
    updated = updated.sort_values(["Season", "Seed", "TeamID"]).reset_index(drop=True)

    if not dry_run:
        updated.to_csv(OUTPUT_PATH, index=False)

    print("\nSeed file update summary")
    print(f"  Target season                : {TARGET_SEASON}")
    print(f"  Existing rows removed        : {before_2026}")
    print(f"  New rows appended            : {len(new_rows)}")
    print(f"  Total rows before            : {before_total}")
    print(f"  Total rows after             : {len(updated)}")
    print(f"  Write mode                   : {'DRY RUN (no file written)' if dry_run else 'WRITE'}")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build 2026 MNCAATourneySeeds rows from NCAA_Bracket_Seeds_2026.csv and replace Season=2026 rows."
    )
    p.add_argument("--dry-run", action="store_true", help="Validate and preview without writing MNCAATourneySeeds.csv")
    p.add_argument(
        "--non-interactive",
        action="store_true",
        help="Fail instead of prompting when a team name cannot be matched",
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input seed source not found: {INPUT_PATH}")
    if not OUTPUT_PATH.exists():
        raise FileNotFoundError(f"Target seeds file not found: {OUTPUT_PATH}")

    src = pd.read_csv(INPUT_PATH)
    new_rows, overrides, manual_count = _build_2026_seed_rows(
        src,
        interactive=not args.non_interactive,
    )

    print("Build summary")
    print(f"  Source rows                  : {len(src)}")
    print(f"  Output rows                  : {len(new_rows)}")
    print(f"  Play-in rows                 : {int(new_rows['Seed'].str.endswith(('a', 'b')).sum())}")
    print(f"  Manual mappings used/added   : {manual_count}")

    if len(new_rows) not in {64, 68}:
        print("  WARNING: Expected 64 or 68 rows for tournament seeds.")

    # Final defensive checks before write
    if new_rows["TeamID"].isna().any():
        raise ValueError("TeamID has null values after mapping.")
    if new_rows.duplicated(subset=["Season", "Seed"]).any():
        raise ValueError("Duplicate Season+Seed rows detected in generated output.")

    _replace_2026_rows(new_rows, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
