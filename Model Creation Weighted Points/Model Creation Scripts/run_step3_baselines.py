from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRACKET_SCRIPT = ROOT / "Model Creation" / "Model Creation Scripts" / "Bracket Model" / "run_bracket_baselines.py"
CHAMP_SCRIPT = ROOT / "Model Creation" / "Model Creation Scripts" / "Champion Model" / "run_champion_baselines.py"


def run_script(path: Path) -> None:
    print(f"Running {path.name}...")
    proc = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Script failed: {path}")


def main() -> None:
    run_script(BRACKET_SCRIPT)
    run_script(CHAMP_SCRIPT)
    print("Step 3 baseline runs completed and step3_run_results.csv updated.")


if __name__ == "__main__":
    main()
