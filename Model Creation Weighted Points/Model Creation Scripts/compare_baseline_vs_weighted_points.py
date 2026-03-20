from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
KAGGLE = ROOT / "Good_Data" / "march-machine-learning-mania-2026-base-data"
BASE_PROD = ROOT / "Model Creation" / "Results" / "Production"
WPTS_PROD = ROOT / "Model Creation Weighted Points" / "Results" / "Production"

SEASONS = [2023, 2024, 2025]
WEIGHTS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32}
ROUND_NAMES = {
    1: "Round of 64",
    2: "Round of 32",
    3: "Sweet 16",
    4: "Elite 8",
    5: "Final Four",
    6: "Championship",
}


def day_to_round(day: int) -> int | None:
    if day in (136, 137):
        return 1
    if day in (138, 139):
        return 2
    if day in (143, 144):
        return 3
    if day in (145, 146):
        return 4
    if day == 152:
        return 5
    if day == 154:
        return 6
    return None


def score_prediction(pred_path: Path, actual_main: pd.DataFrame) -> Dict[str, float]:
    preds = pd.read_csv(pred_path)

    out: Dict[str, float] = {}
    total_points = 0
    total_max = 0
    total_error = 0
    total_correct = 0

    for rnd in [1, 2, 3, 4, 5, 6]:
        pred_set = set(preds[preds["Round"] == rnd]["predicted_winner"].astype(int).tolist())
        act_set = set(actual_main[actual_main["Round"] == rnd]["WTeamID"].astype(int).tolist())

        correct = len(pred_set.intersection(act_set))
        error = len(pred_set.symmetric_difference(act_set))
        pts = correct * WEIGHTS[rnd]
        mx = len(act_set) * WEIGHTS[rnd]

        out[f"r{rnd}_correct"] = correct
        out[f"r{rnd}_error"] = error
        out[f"r{rnd}_points"] = pts
        out[f"r{rnd}_max_points"] = mx

        total_correct += correct
        total_error += error
        total_points += pts
        total_max += mx

    out["total_correct"] = total_correct
    out["total_error"] = total_error
    out["total_points"] = total_points
    out["max_points"] = total_max
    out["points_pct"] = total_points / total_max if total_max else 0.0
    out["point_gap"] = total_max - total_points
    return out


def build_markdown(summary_df: pd.DataFrame, round_df: pd.DataFrame, out_path: Path) -> None:
    lines: List[str] = []
    lines.append("# Baseline vs Weighted Points Comparison (2023-2025)")
    lines.append("")

    avg = summary_df.agg(
        {
            "baseline_total_points": "mean",
            "weighted_total_points": "mean",
            "delta_points": "mean",
            "baseline_points_pct": "mean",
            "weighted_points_pct": "mean",
            "delta_points_pct": "mean",
            "baseline_total_error": "mean",
            "weighted_total_error": "mean",
            "delta_error": "mean",
        }
    )

    lines.append("## Overall Average Delta")
    lines.append(f"- Baseline avg points: {avg['baseline_total_points']:.2f}/192")
    lines.append(f"- Weighted avg points: {avg['weighted_total_points']:.2f}/192")
    lines.append(f"- Avg point delta (weighted - baseline): {avg['delta_points']:.2f}")
    lines.append(f"- Baseline avg points %: {avg['baseline_points_pct']:.2%}")
    lines.append(f"- Weighted avg points %: {avg['weighted_points_pct']:.2%}")
    lines.append(f"- Avg points % delta: {avg['delta_points_pct']:.2%}")
    lines.append(f"- Baseline avg winner-set error: {avg['baseline_total_error']:.2f}")
    lines.append(f"- Weighted avg winner-set error: {avg['weighted_total_error']:.2f}")
    lines.append(f"- Avg error delta (weighted - baseline): {avg['delta_error']:.2f}")
    lines.append("")

    lines.append("## By Season")
    lines.append("| Season | Baseline Points | Weighted Points | Delta | Baseline % | Weighted % | Delta % | Baseline Error | Weighted Error | Delta Error |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in summary_df.sort_values("season").iterrows():
        lines.append(
            f"| {int(r['season'])} | {int(r['baseline_total_points'])}/192 | {int(r['weighted_total_points'])}/192 | "
            f"{int(r['delta_points'])} | {r['baseline_points_pct']:.2%} | {r['weighted_points_pct']:.2%} | "
            f"{r['delta_points_pct']:.2%} | {int(r['baseline_total_error'])} | {int(r['weighted_total_error'])} | {int(r['delta_error'])} |"
        )
    lines.append("")

    lines.append("## Per-Round Delta (Weighted - Baseline)")
    lines.append("| Season | Round | Baseline Points | Weighted Points | Delta Points | Baseline Error | Weighted Error | Delta Error |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|---:|")
    for _, r in round_df.sort_values(["season", "round"]).iterrows():
        lines.append(
            f"| {int(r['season'])} | {ROUND_NAMES[int(r['round'])]} | {int(r['baseline_points'])} | {int(r['weighted_points'])} | "
            f"{int(r['delta_points'])} | {int(r['baseline_error'])} | {int(r['weighted_error'])} | {int(r['delta_error'])} |"
        )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    WPTS_PROD.mkdir(parents=True, exist_ok=True)

    actual_all = pd.read_csv(KAGGLE / "MNCAATourneyCompactResults.csv")

    season_rows = []
    round_rows = []

    for season in SEASONS:
        actual_main = actual_all[(actual_all["Season"] == season) & (actual_all["DayNum"] >= 136)].copy()
        actual_main["Round"] = actual_main["DayNum"].map(day_to_round)
        actual_main = actual_main[actual_main["Round"].notna()].copy()

        base_path = BASE_PROD / f"{season}_bracket_predictions.csv"
        wpts_path = WPTS_PROD / f"{season}_bracket_predictions_weighted_points.csv"

        base_score = score_prediction(base_path, actual_main)
        wpts_score = score_prediction(wpts_path, actual_main)

        season_rows.append(
            {
                "season": season,
                "baseline_total_points": base_score["total_points"],
                "weighted_total_points": wpts_score["total_points"],
                "delta_points": wpts_score["total_points"] - base_score["total_points"],
                "baseline_points_pct": base_score["points_pct"],
                "weighted_points_pct": wpts_score["points_pct"],
                "delta_points_pct": wpts_score["points_pct"] - base_score["points_pct"],
                "baseline_total_error": base_score["total_error"],
                "weighted_total_error": wpts_score["total_error"],
                "delta_error": wpts_score["total_error"] - base_score["total_error"],
            }
        )

        for rnd in [1, 2, 3, 4, 5, 6]:
            round_rows.append(
                {
                    "season": season,
                    "round": rnd,
                    "baseline_points": base_score[f"r{rnd}_points"],
                    "weighted_points": wpts_score[f"r{rnd}_points"],
                    "delta_points": wpts_score[f"r{rnd}_points"] - base_score[f"r{rnd}_points"],
                    "baseline_error": base_score[f"r{rnd}_error"],
                    "weighted_error": wpts_score[f"r{rnd}_error"],
                    "delta_error": wpts_score[f"r{rnd}_error"] - base_score[f"r{rnd}_error"],
                }
            )

    summary_df = pd.DataFrame(season_rows)
    round_df = pd.DataFrame(round_rows)

    summary_csv = WPTS_PROD / "baseline_vs_weighted_points_summary_2023_2025.csv"
    round_csv = WPTS_PROD / "baseline_vs_weighted_points_round_deltas_2023_2025.csv"
    report_md = WPTS_PROD / "baseline_vs_weighted_points_report_2023_2025.md"

    summary_df.to_csv(summary_csv, index=False)
    round_df.to_csv(round_csv, index=False)
    build_markdown(summary_df, round_df, report_md)

    print(f"Wrote {summary_csv}")
    print(f"Wrote {round_csv}")
    print(f"Wrote {report_md}")


if __name__ == "__main__":
    main()
