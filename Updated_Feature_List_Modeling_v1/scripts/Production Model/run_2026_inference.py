from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = ROOT / "Updated_Feature_List_Modeling_v1" / "scripts" / "Production Model"

BRACKET_SCRIPT = SCRIPT_DIR / "run_2026_bracket_inference.py"
CHAMPION_SCRIPT = SCRIPT_DIR / "run_2026_champion_inference.py"


def run_script(path: Path, season: int) -> None:
    print(f"Running {path.name} for season {season}...")
    proc = subprocess.run(
        [sys.executable, str(path), "--season", str(season)],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Script failed: {path}")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run both updated locked 2026 production inference scripts.")
    p.add_argument("--season", type=int, default=2026, help="Season to predict (default: 2026)")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    season = int(args.season)

    run_script(BRACKET_SCRIPT, season)
    run_script(CHAMPION_SCRIPT, season)

    print("Updated production inference completed for both bracket and champion.")


if __name__ == "__main__":
    main()
