"""
interpret_bracket_text.py

Reads a bracket prediction CSV and prints a simple text representation of the
bracket similar to a visual bracket image.

Supports two input formats:
1) 2026 inference format (preferred): has Slot / Round / Winner columns
2) Legacy production test format: has DayNum + TeamAID/TeamBID + p_teamA_win

Usage examples:
  python "Model Creation/Model Creation Scripts/Production Model/interpret_bracket_text.py"
  python "Model Creation/Model Creation Scripts/Production Model/interpret_bracket_text.py" --input "Model Creation/Results/Production/2026_bracket_predictions.csv"
  python "Model Creation/Model Creation Scripts/Production Model/interpret_bracket_text.py" --season 2026 --save
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "Model Creation" / "Results" / "Production" / "2026_bracket_predictions.csv"
FALLBACK_INPUT = ROOT / "Model Creation" / "Results" / "Production" / "production_predictions_bracket.csv"
TEAMS_PATH = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data" / "MTeams.csv"

REGION_LABELS = {
    "W": "West",
    "X": "East",
    "Y": "South",
    "Z": "Midwest",
}


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render bracket predictions as text")
    p.add_argument("--input", type=str, default="", help="Path to bracket prediction CSV")
    p.add_argument("--season", type=int, default=0, help="Season to render (default: latest in file)")
    p.add_argument("--save", action="store_true", help="Also save rendered text to a .txt next to input")
    return p.parse_args()


def _load_input(input_arg: str) -> Path:
    if input_arg:
        p = Path(input_arg)
        if not p.is_absolute():
            p = ROOT / p
        return p
    if DEFAULT_INPUT.exists():
        return DEFAULT_INPUT
    return FALLBACK_INPUT


def _team_name_map() -> Dict[int, str]:
    if not TEAMS_PATH.exists():
        return {}
    t = pd.read_csv(TEAMS_PATH, usecols=["TeamID", "TeamName"])
    return dict(zip(t["TeamID"].astype(int), t["TeamName"].astype(str)))


def _slot_round(slot: str) -> int:
    m = re.match(r"^R(\d)", str(slot))
    return int(m.group(1)) if m else 0


def _fmt_prob(p_teamA_win: float, winner_is_a: bool) -> str:
    if pd.isna(p_teamA_win):
        return ""
    conf = p_teamA_win if winner_is_a else (1.0 - p_teamA_win)
    return f" ({conf:.0%})"


def _render_modern(df: pd.DataFrame, season: int, name_map: Dict[int, str]) -> str:
    d = df[df["Season"] == season].copy()
    if len(d) == 0:
        return f"No rows found for Season={season}."

    if "Round" not in d.columns:
        d["Round"] = d["Slot"].map(_slot_round)

    # Ensure useful name columns exist
    if "TeamA_name" not in d.columns:
        d["TeamA_name"] = d["TeamAID"].map(name_map)
    if "TeamB_name" not in d.columns:
        d["TeamB_name"] = d["TeamBID"].map(name_map)
    if "Winner_name" not in d.columns and "predicted_winner" in d.columns:
        d["Winner_name"] = d["predicted_winner"].map(name_map)

    lines: List[str] = []
    lines.append(f"MARCH MADNESS {season} - TEXT BRACKET")
    lines.append("=" * 72)

    # Play-in (Round 0 / non-R slots)
    playin = d[d["Round"] == 0].sort_values("Slot")
    if len(playin):
        lines.append("\nPLAY-IN GAMES")
        lines.append("-" * 72)
        for _, r in playin.iterrows():
            a_name = str(r.get("TeamA_name", r["TeamAID"]))
            b_name = str(r.get("TeamB_name", r["TeamBID"]))
            winner = int(r["predicted_winner"]) if "predicted_winner" in r and pd.notna(r["predicted_winner"]) else int(r["TeamAID"])
            winner_is_a = (winner == int(r["TeamAID"]))
            w_name = a_name if winner_is_a else b_name
            slot = str(r["Slot"])
            lines.append(f"[{slot:>6}] {a_name} vs {b_name}  ->  {w_name}{_fmt_prob(r.get('p_teamA_win', np.nan), winner_is_a)}")

    # Regional rounds 1-4
    for reg in ["W", "X", "Y", "Z"]:
        reg_name = REGION_LABELS.get(reg, reg)
        reg_rows = d[d["Slot"].astype(str).str.contains(reg, regex=False)]
        if len(reg_rows) == 0:
            continue

        lines.append(f"\n{reg_name.upper()} REGION ({reg})")
        lines.append("-" * 72)

        for rnd, label in [(1, "Round of 64"), (2, "Round of 32"), (3, "Sweet 16"), (4, "Elite 8")]:
            rr = reg_rows[reg_rows["Round"] == rnd].copy()
            if len(rr) == 0:
                continue
            rr = rr.sort_values("Slot")
            lines.append(f"{label}:")
            for _, r in rr.iterrows():
                a_name = str(r.get("TeamA_name", r["TeamAID"]))
                b_name = str(r.get("TeamB_name", r["TeamBID"]))
                winner = int(r["predicted_winner"]) if "predicted_winner" in r and pd.notna(r["predicted_winner"]) else int(r["TeamAID"])
                winner_is_a = (winner == int(r["TeamAID"]))
                w_name = a_name if winner_is_a else b_name
                slot = str(r["Slot"])

                a_seed = r.get("TeamA_seed_num", np.nan)
                b_seed = r.get("TeamB_seed_num", np.nan)
                a_seed_txt = f"({int(a_seed)}) " if pd.notna(a_seed) else ""
                b_seed_txt = f"({int(b_seed)}) " if pd.notna(b_seed) else ""

                lines.append(
                    f"  [{slot:>6}] {a_seed_txt}{a_name} vs {b_seed_txt}{b_name}"
                    f"  ->  {w_name}{_fmt_prob(r.get('p_teamA_win', np.nan), winner_is_a)}"
                )

    # Final Four and Championship
    ff = d[d["Round"] == 5].sort_values("Slot")
    ch = d[d["Round"] == 6].sort_values("Slot")

    if len(ff):
        lines.append("\nFINAL FOUR")
        lines.append("-" * 72)
        for _, r in ff.iterrows():
            a_name = str(r.get("TeamA_name", r["TeamAID"]))
            b_name = str(r.get("TeamB_name", r["TeamBID"]))
            winner = int(r["predicted_winner"]) if "predicted_winner" in r and pd.notna(r["predicted_winner"]) else int(r["TeamAID"])
            winner_is_a = (winner == int(r["TeamAID"]))
            w_name = a_name if winner_is_a else b_name
            lines.append(f"[{str(r['Slot']):>6}] {a_name} vs {b_name}  ->  {w_name}{_fmt_prob(r.get('p_teamA_win', np.nan), winner_is_a)}")

    if len(ch):
        lines.append("\nNATIONAL CHAMPIONSHIP")
        lines.append("-" * 72)
        r = ch.iloc[0]
        a_name = str(r.get("TeamA_name", r["TeamAID"]))
        b_name = str(r.get("TeamB_name", r["TeamBID"]))
        winner = int(r["predicted_winner"]) if "predicted_winner" in r and pd.notna(r["predicted_winner"]) else int(r["TeamAID"])
        winner_is_a = (winner == int(r["TeamAID"]))
        w_name = a_name if winner_is_a else b_name
        lines.append(f"[{str(r['Slot']):>6}] {a_name} vs {b_name}  ->  {w_name}{_fmt_prob(r.get('p_teamA_win', np.nan), winner_is_a)}")
        lines.append("=" * 72)
        lines.append(f"PREDICTED NATIONAL CHAMPION: {w_name}")

    return "\n".join(lines)


def _render_legacy(df: pd.DataFrame, season: int, name_map: Dict[int, str]) -> str:
    d = df[df["Season"] == season].copy()
    if len(d) == 0:
        return f"No rows found for Season={season}."

    def _legacy_round_label(day_num: int) -> str:
        # Standard men's NCAA tournament calendar buckets
        if day_num in {134, 135}:
            return "Play-In"
        if day_num in {136, 137}:
            return "Round of 64"
        if day_num in {138, 139}:
            return "Round of 32"
        if day_num in {143, 144}:
            return "Sweet 16"
        if day_num in {145, 146}:
            return "Elite 8"
        if day_num == 152:
            return "Final Four"
        if day_num == 154:
            return "National Championship"
        return f"Day {day_num}"

    round_order = {
        "Play-In": 0,
        "Round of 64": 1,
        "Round of 32": 2,
        "Sweet 16": 3,
        "Elite 8": 4,
        "Final Four": 5,
        "National Championship": 6,
    }

    # Remove mirrored duplicates: (A,B) and (B,A) for same season/day/game pairing.
    d["team_low"] = d[["TeamAID", "TeamBID"]].min(axis=1)
    d["team_high"] = d[["TeamAID", "TeamBID"]].max(axis=1)
    d["pair_key"] = (
        d["Season"].astype(str)
        + "|" + d["DayNum"].astype(str)
        + "|" + d["team_low"].astype(str)
        + "|" + d["team_high"].astype(str)
    )
    d = d.sort_values(["DayNum", "team_low", "team_high", "TeamAID"]).drop_duplicates(subset=["pair_key"], keep="first")

    d["round_label"] = d["DayNum"].astype(int).map(_legacy_round_label)
    d["round_order"] = d["round_label"].map(lambda x: round_order.get(x, 999))

    d["TeamA_name"] = d["TeamAID"].map(name_map).fillna(d["TeamAID"].astype(str))
    d["TeamB_name"] = d["TeamBID"].map(name_map).fillna(d["TeamBID"].astype(str))
    d["pred_winner"] = np.where(d["p_teamA_win"] >= 0.5, d["TeamA_name"], d["TeamB_name"])

    lines: List[str] = []
    lines.append(f"MARCH MADNESS {season} - ROUND-BY-ROUND BRACKET (LEGACY FORMAT)")
    lines.append("=" * 72)
    for rlabel in d.sort_values(["round_order", "DayNum"])["round_label"].drop_duplicates().tolist():
        dd = d[d["round_label"] == rlabel].copy().sort_values(["DayNum", "team_low", "team_high"])

        # Extra guardrail: ensure each team appears once per round.
        used_teams = set()
        kept_rows = []
        for _, r in dd.iterrows():
            ta = int(r["TeamAID"])
            tb = int(r["TeamBID"])
            if ta in used_teams or tb in used_teams:
                continue
            kept_rows.append(r)
            used_teams.add(ta)
            used_teams.add(tb)

        lines.append(f"\n{rlabel.upper()}")
        lines.append("-" * 72)
        for r in kept_rows:
            winner_is_a = bool(r["p_teamA_win"] >= 0.5)
            conf = r["p_teamA_win"] if winner_is_a else (1.0 - r["p_teamA_win"])
            lines.append(
                f"{r['TeamA_name']} vs {r['TeamB_name']}  ->  {r['pred_winner']} ({conf:.0%})"
            )
    return "\n".join(lines)


def main() -> None:
    args = _parse_args()
    input_path = _load_input(args.input)

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Tip: pass --input to a valid bracket prediction CSV.")
        return

    df = pd.read_csv(input_path)
    if len(df) == 0:
        print(f"Input file is empty: {input_path}")
        return

    season = int(args.season) if args.season else int(df["Season"].max())
    name_map = _team_name_map()

    modern_schema = {"Slot", "TeamAID", "TeamBID"}.issubset(df.columns)
    if modern_schema:
        txt = _render_modern(df, season, name_map)
    else:
        txt = _render_legacy(df, season, name_map)

    print(txt)

    if args.save:
        out_path = input_path.with_name(input_path.stem + "_text_view.txt")
        out_path.write_text(txt, encoding="utf-8")
        print(f"\nSaved text bracket to: {out_path}")


if __name__ == "__main__":
    main()
