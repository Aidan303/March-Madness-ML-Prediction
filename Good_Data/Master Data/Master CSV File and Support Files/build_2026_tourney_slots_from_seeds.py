from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
KAGGLE_DIR = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"
SEEDS_PATH = KAGGLE_DIR / "MNCAATourneySeeds.csv"
SLOTS_PATH = KAGGLE_DIR / "MNCAATourneySlots.csv"

TARGET_SEASON = 2026
TEMPLATE_SEASON = 2025


def _playin_base_seeds_for_2026(seeds: pd.DataFrame) -> list[str]:
    s26 = seeds[seeds["Season"] == TARGET_SEASON].copy()
    if len(s26) == 0:
        raise ValueError(f"No Season={TARGET_SEASON} rows found in {SEEDS_PATH}")

    playin = s26[s26["Seed"].astype(str).str.endswith(("a", "b"))].copy()
    if len(playin) == 0:
        return []

    playin["base_seed"] = playin["Seed"].astype(str).str.slice(0, 3)
    counts = playin.groupby("base_seed").size().reset_index(name="n")
    bad = counts[counts["n"] != 2]
    if len(bad):
        raise ValueError(
            "Play-in seed groups must have exactly 2 rows (a/b) each. Bad groups:\n"
            + bad.to_string(index=False)
        )

    return sorted(counts["base_seed"].tolist())


def _build_2026_slots(slots: pd.DataFrame, playin_base_seeds: list[str]) -> pd.DataFrame:
    t = slots[slots["Season"] == TEMPLATE_SEASON].copy()
    if len(t) == 0:
        raise ValueError(f"No Season={TEMPLATE_SEASON} rows found in {SLOTS_PATH}")

    t["is_playin_slot"] = t["Slot"].astype(str).str.match(r"^[WXYZ][0-9]{2}$")

    # Keep tournament structure from template year (R1..R6), only swap play-in slot rows.
    base = t[~t["is_playin_slot"]][["Slot", "StrongSeed", "WeakSeed"]].copy()

    playin_rows = pd.DataFrame(
        {
            "Slot": playin_base_seeds,
            "StrongSeed": [f"{s}a" for s in playin_base_seeds],
            "WeakSeed": [f"{s}b" for s in playin_base_seeds],
        }
    )

    out = pd.concat([base, playin_rows], ignore_index=True)
    out.insert(0, "Season", TARGET_SEASON)

    # Preserve conventional ordering: rounds first, play-ins last (sorted).
    out["_ord_group"] = out["Slot"].astype(str).str.match(r"^R[1-6]").map({True: 0, False: 1})
    out["_ord_slot"] = out["Slot"].astype(str)
    out = out.sort_values(["_ord_group", "_ord_slot"]).drop(columns=["_ord_group", "_ord_slot"]).reset_index(drop=True)

    return out


def _validate_slots(slots_2026: pd.DataFrame, seeds: pd.DataFrame) -> None:
    if slots_2026.duplicated(subset=["Season", "Slot"]).any():
        raise ValueError("Duplicate Slot values found for 2026.")

    if len(slots_2026) != 67:
        raise ValueError(f"Expected 67 slot rows for a 68-team tournament, got {len(slots_2026)}")

    # Ensure each play-in base slot appears in Round 1 references.
    playin_bases = slots_2026[slots_2026["Slot"].astype(str).str.match(r"^[WXYZ][0-9]{2}$")]["Slot"].tolist()
    r1 = slots_2026[slots_2026["Slot"].astype(str).str.match(r"^R1")]
    for base in playin_bases:
        appears = ((r1["StrongSeed"] == base) | (r1["WeakSeed"] == base)).any()
        if not appears:
            raise ValueError(f"Play-in base slot {base} is not referenced by any Round 1 slot.")

    # Ensure play-in slot teams exist in seeds file as a/b.
    s26 = seeds[seeds["Season"] == TARGET_SEASON].copy()
    seed_set = set(s26["Seed"].astype(str).tolist())
    for base in playin_bases:
        if f"{base}a" not in seed_set or f"{base}b" not in seed_set:
            raise ValueError(f"Missing seed rows for play-in slot {base}: expected {base}a and {base}b")


def _replace_2026_rows(slots_all: pd.DataFrame, slots_2026: pd.DataFrame, dry_run: bool) -> None:
    before_total = len(slots_all)
    before_2026 = int((slots_all["Season"] == TARGET_SEASON).sum())

    kept = slots_all[slots_all["Season"] != TARGET_SEASON].copy()
    updated = pd.concat([kept, slots_2026], ignore_index=True)

    # Keep full file stable by sorting on season then slot.
    updated = updated.sort_values(["Season", "Slot"]).reset_index(drop=True)

    if not dry_run:
        updated.to_csv(SLOTS_PATH, index=False)

    print("Slot file update summary")
    print(f"  Target season         : {TARGET_SEASON}")
    print(f"  Existing rows removed : {before_2026}")
    print(f"  New rows appended     : {len(slots_2026)}")
    print(f"  Total rows before     : {before_total}")
    print(f"  Total rows after      : {len(updated)}")
    print(f"  Write mode            : {'DRY RUN (no file written)' if dry_run else 'WRITE'}")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build Season 2026 MNCAATourneySlots rows from existing 2026 seeds and a template year."
    )
    p.add_argument("--dry-run", action="store_true", help="Validate and preview without writing MNCAATourneySlots.csv")
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    if not SEEDS_PATH.exists():
        raise FileNotFoundError(f"Missing seeds file: {SEEDS_PATH}")
    if not SLOTS_PATH.exists():
        raise FileNotFoundError(f"Missing slots file: {SLOTS_PATH}")

    seeds = pd.read_csv(SEEDS_PATH)
    slots = pd.read_csv(SLOTS_PATH)

    playin_base = _playin_base_seeds_for_2026(seeds)
    slots_2026 = _build_2026_slots(slots, playin_base)

    _validate_slots(slots_2026, seeds)

    print("Build summary")
    print(f"  Template season       : {TEMPLATE_SEASON}")
    print(f"  Play-in base slots    : {', '.join(playin_base) if playin_base else '(none)'}")
    print(f"  Generated 2026 rows   : {len(slots_2026)}")

    _replace_2026_rows(slots, slots_2026, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
