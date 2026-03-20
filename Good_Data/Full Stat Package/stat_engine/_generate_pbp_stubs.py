"""
Generator script to create pbp_stubs.py from Full_Stat_Package_Team.csv.
Finds all stats with Data Source == "pbp" and creates NotImplementedError stubs for each.

Run: python _generate_pbp_stubs.py
"""

import csv
import os
import re


def normalize_name_to_function(name: str) -> str:
    """Convert stat name to Python function name (calc_ABBREV)."""
    abbrev = name.strip().lower()
    # Replace spaces and special chars with underscores
    abbrev = re.sub(r"[^\w]+", "_", abbrev)
    # Remove leading/trailing underscores
    abbrev = abbrev.strip("_")
    return f"calc_{abbrev}"


def main():
    csv_path = os.path.join("..", "Full_Stat_Package_Team.csv")
    
    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found")
        return

    pbp_stats = []
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_source = row.get("Data Source", "").strip()
            if data_source == "pbp":
                abbrev = row.get("Abbrev", "").strip()
                stat_name = row.get("Stat Name", "").strip()
                description = row.get("Description", "").strip()
                pbp_stats.append((abbrev, stat_name, description))
    
    if not pbp_stats:
        print("No PBP stats found in CSV")
        return

    print(f"Found {len(pbp_stats)} PBP-only stats")

    # Generate pbp_stubs.py content
    output_lines = [
        '"""PBP (play-by-play) statistics stubs.\n',
        '\n',
        'These functions raise NotImplementedError until PBP data is available.\n',
        '"""\n',
        '\n',
        "from __future__ import annotations\n",
        "\n",
        "import pandas as pd\n",
        "\n",
        "\n",
    ]

    for abbrev, stat_name, description in pbp_stats:
        func_name = normalize_name_to_function(abbrev)
        output_lines.append(
            f'def {func_name}(df: pd.DataFrame, agg: bool = True) -> float | pd.Series:\n'
        )
        # Escape description to avoid docstring issues
        escaped_desc = (
            description.replace('"""', r'\"\"\"')
            .replace("\\", "\\\\")
            .replace("\n", " ")
        )
        output_lines.append(f'    """{escaped_desc}"""\n')
        output_lines.append(
            f'    raise NotImplementedError("PBP data not yet available: {abbrev}")\n'
        )
        output_lines.append("\n")
        output_lines.append("\n")

    pbp_stubs_path = "pbp_stubs.py"
    with open(pbp_stubs_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"Generated {pbp_stubs_path} with {len(pbp_stats)} stub functions")
    print(f"Example stubs:")
    for i, (abbrev, stat_name, desc) in enumerate(pbp_stats[:3]):
        func_name = normalize_name_to_function(abbrev)
        print(f"  {func_name} ({abbrev})")
    if len(pbp_stats) > 3:
        print(f"  ... and {len(pbp_stats) - 3} more")


if __name__ == "__main__":
    main()
