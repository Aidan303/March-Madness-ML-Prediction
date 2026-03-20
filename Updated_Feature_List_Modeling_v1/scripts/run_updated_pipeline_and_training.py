from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "Updated_Feature_List_Modeling_v1" / "scripts"

BUILD_SCRIPT = SCRIPT_DIR / "build_updated_pipeline.py"
TRAIN_SCRIPT = SCRIPT_DIR / "train_updated_models.py"


def run_script(path: Path) -> None:
    print(f"Running {path.name}...")
    proc = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Script failed: {path}")


def main() -> None:
    run_script(BUILD_SCRIPT)
    run_script(TRAIN_SCRIPT)
    print("Updated feature pipeline and model training completed.")


if __name__ == "__main__":
    main()
