from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


@dataclass
class GamePrediction:
    slot: str
    round_num: int
    team_a_id: int
    team_b_id: int
    team_a_name: str
    team_b_name: str
    team_a_seed: float
    team_b_seed: float
    predicted_winner_id: int
    winner_name: str
    p_team_a_win: float

    @property
    def winner_probability(self) -> float:
        if self.predicted_winner_id == self.team_a_id:
            return self.p_team_a_win
        return 1.0 - self.p_team_a_win


def parse_float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_int(value: str, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def load_predictions(csv_path: Path) -> Dict[str, GamePrediction]:
    predictions: Dict[str, GamePrediction] = {}
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slot = (row.get("Slot") or "").strip()
            if not slot:
                continue
            predictions[slot] = GamePrediction(
                slot=slot,
                round_num=parse_int(row.get("Round"), 0),
                team_a_id=parse_int(row.get("TeamAID"), 0),
                team_b_id=parse_int(row.get("TeamBID"), 0),
                team_a_name=(row.get("TeamA_name") or "").strip(),
                team_b_name=(row.get("TeamB_name") or "").strip(),
                team_a_seed=parse_float(row.get("TeamA_seed_num"), 0.0),
                team_b_seed=parse_float(row.get("TeamB_seed_num"), 0.0),
                predicted_winner_id=parse_int(row.get("predicted_winner"), 0),
                winner_name=(row.get("Winner_name") or "").strip(),
                p_team_a_win=parse_float(row.get("p_teamA_win"), 0.5),
            )
    return predictions


def format_seed(seed: float) -> str:
    if seed <= 0:
        return ""
    return str(int(seed))


def format_team_line(seed: float, name: str) -> str:
    seed_str = format_seed(seed)
    if seed_str:
        return f"({seed_str}) {name}"
    return name


def draw_game_box(
    ax: plt.Axes,
    x: float,
    y: float,
    game: GamePrediction,
    box_w: float,
    box_h: float,
    facecolor: str,
    edgecolor: str,
    fontsize: int,
) -> None:
    box = FancyBboxPatch(
        (x - box_w / 2.0, y - box_h / 2.0),
        box_w,
        box_h,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=0.8,
        edgecolor=edgecolor,
        facecolor=facecolor,
        zorder=2,
    )
    ax.add_patch(box)

    team_a = format_team_line(game.team_a_seed, game.team_a_name)
    team_b = format_team_line(game.team_b_seed, game.team_b_name)
    text = (
        f"{team_a}\n"
        f"vs\n"
        f"{team_b}\n"
        f"W: {game.winner_name} ({game.winner_probability:.1%})"
    )
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        family="DejaVu Sans",
        zorder=3,
    )


def connect_boxes(
    ax: plt.Axes,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str = "#6b7280",
) -> None:
    mid_x = (x1 + x2) / 2.0
    ax.plot([x1, mid_x], [y1, y1], color=color, linewidth=0.8, zorder=1)
    ax.plot([mid_x, mid_x], [y1, y2], color=color, linewidth=0.8, zorder=1)
    ax.plot([mid_x, x2], [y2, y2], color=color, linewidth=0.8, zorder=1)


def region_slot(round_num: int, region: str, idx: int) -> str:
    return f"R{round_num}{region}{idx}"


def find_semifinal_slot(predictions: Dict[str, GamePrediction], regions: Tuple[str, str]) -> str:
    region_set = set(regions)
    for slot, game in predictions.items():
        if game.round_num != 5:
            continue
        m = re.match(r"^R5([WXYZ]{2})$", slot)
        if not m:
            continue
        if set(m.group(1)) == region_set:
            return slot
    raise ValueError(f"Could not find semifinal slot for regions {regions}")


def draw_region(
    ax: plt.Axes,
    predictions: Dict[str, GamePrediction],
    region: str,
    x_cols: List[float],
    y_origin: float,
    y_step: float,
    box_w: float,
    box_h: float,
    facecolor: str,
    edgecolor: str,
    fontsize: int,
) -> Tuple[float, float, str]:
    # Region bracket slot progression by slot IDs:
    # R2?1 <- (R1?1, R1?8)
    # R2?2 <- (R1?2, R1?7)
    # R2?3 <- (R1?3, R1?6)
    # R2?4 <- (R1?4, R1?5)
    # R3?1 <- (R2?1, R2?4)
    # R3?2 <- (R2?2, R2?3)

    # Display order is defined bottom-to-top because matplotlib y increases upward.
    # This yields the desired top-to-bottom visual order: 1, 8, 5, 4, 6, 3, 7, 2.
    r1_display_order = [2, 7, 3, 6, 4, 5, 8, 1]
    r2_display_order = [1, 4, 2, 3]

    r2_feed = {1: (1, 8), 2: (2, 7), 3: (3, 6), 4: (4, 5)}
    r3_feed = {1: (1, 4), 2: (2, 3)}

    y_round_1 = [y_origin + i * y_step for i in range(8)]
    y_r1_by_slot = {slot_idx: y_round_1[pos] for pos, slot_idx in enumerate(r1_display_order)}

    y_round_2 = [
        (y_r1_by_slot[r2_feed[slot_idx][0]] + y_r1_by_slot[r2_feed[slot_idx][1]]) / 2.0
        for slot_idx in r2_display_order
    ]
    y_r2_by_slot = {slot_idx: y_round_2[pos] for pos, slot_idx in enumerate(r2_display_order)}

    y_round_3 = [
        (y_r2_by_slot[r3_feed[slot_idx][0]] + y_r2_by_slot[r3_feed[slot_idx][1]]) / 2.0
        for slot_idx in [1, 2]
    ]
    y_r3_by_slot = {1: y_round_3[0], 2: y_round_3[1]}

    y_round_4 = [(y_r3_by_slot[1] + y_r3_by_slot[2]) / 2.0]

    coords: Dict[str, Tuple[float, float]] = {}

    for i in r1_display_order:
        slot = region_slot(1, region, i)
        game = predictions[slot]
        x = x_cols[0]
        y = y_r1_by_slot[i]
        draw_game_box(ax, x, y, game, box_w, box_h, facecolor, edgecolor, fontsize)
        coords[slot] = (x, y)

    for i in r2_display_order:
        slot = region_slot(2, region, i)
        game = predictions[slot]
        x = x_cols[1]
        y = y_r2_by_slot[i]
        draw_game_box(ax, x, y, game, box_w, box_h, facecolor, edgecolor, fontsize)
        coords[slot] = (x, y)
        feed_1, feed_2 = r2_feed[i]
        p1 = coords[region_slot(1, region, feed_1)]
        p2 = coords[region_slot(1, region, feed_2)]
        connect_boxes(ax, p1[0], p1[1], x, y)
        connect_boxes(ax, p2[0], p2[1], x, y)

    for i in [1, 2]:
        slot = region_slot(3, region, i)
        game = predictions[slot]
        x = x_cols[2]
        y = y_r3_by_slot[i]
        draw_game_box(ax, x, y, game, box_w, box_h, facecolor, edgecolor, fontsize)
        coords[slot] = (x, y)
        feed_1, feed_2 = r3_feed[i]
        p1 = coords[region_slot(2, region, feed_1)]
        p2 = coords[region_slot(2, region, feed_2)]
        connect_boxes(ax, p1[0], p1[1], x, y)
        connect_boxes(ax, p2[0], p2[1], x, y)

    slot = region_slot(4, region, 1)
    game = predictions[slot]
    x = x_cols[3]
    y = y_round_4[0]
    draw_game_box(ax, x, y, game, box_w, box_h, facecolor, edgecolor, fontsize)
    coords[slot] = (x, y)
    connect_boxes(ax, coords[region_slot(3, region, 1)][0], coords[region_slot(3, region, 1)][1], x, y)
    connect_boxes(ax, coords[region_slot(3, region, 2)][0], coords[region_slot(3, region, 2)][1], x, y)

    return x, y, slot


def create_bracket_figure(predictions: Dict[str, GamePrediction], title: str, output_path: Path) -> None:
    # Layout: W top-left, X bottom-left, Z top-right, Y bottom-right.
    # Left semi (W vs X) sits between the two left regions; right semi (Z vs Y)
    # sits between the two right regions.  Both semis land at the same vertical
    # midpoint so they are separated horizontally: left_semi â†’ championship â†’ right_semi.
    fig, ax = plt.subplots(figsize=(24, 12), dpi=180)

    box_w = 3.4
    box_h = 1.2
    y_step = 1.5
    top_origin = 14.0
    bottom_origin = 0.0

    # Left regions progress leftâ†’right; right regions progress rightâ†’left.
    # right_cols is shifted further right so the three centre boxes
    # (left semi / champ / right semi) have room between them.
    left_cols = [3.0, 7.0, 11.0, 15.0]
    right_cols = [43.0, 39.0, 35.0, 31.0]

    # Left side: W (top) and X (bottom).
    w_final = draw_region(
        ax,
        predictions,
        region="W",
        x_cols=left_cols,
        y_origin=top_origin,
        y_step=y_step,
        box_w=box_w,
        box_h=box_h,
        facecolor="#f8fafc",
        edgecolor="#94a3b8",
        fontsize=6,
    )
    x_final = draw_region(
        ax,
        predictions,
        region="X",
        x_cols=left_cols,
        y_origin=bottom_origin,
        y_step=y_step,
        box_w=box_w,
        box_h=box_h,
        facecolor="#f8fafc",
        edgecolor="#94a3b8",
        fontsize=6,
    )

    # Right side: Z (top) and Y (bottom).
    z_final = draw_region(
        ax,
        predictions,
        region="Z",
        x_cols=right_cols,
        y_origin=top_origin,
        y_step=y_step,
        box_w=box_w,
        box_h=box_h,
        facecolor="#f8fafc",
        edgecolor="#94a3b8",
        fontsize=6,
    )
    y_final = draw_region(
        ax,
        predictions,
        region="Y",
        x_cols=right_cols,
        y_origin=bottom_origin,
        y_step=y_step,
        box_w=box_w,
        box_h=box_h,
        facecolor="#f8fafc",
        edgecolor="#94a3b8",
        fontsize=6,
    )

    # Semifinal slots are resolved from slot IDs, not hardcoded pair labels.
    left_semi_slot = find_semifinal_slot(predictions, ("W", "X"))
    right_semi_slot = find_semifinal_slot(predictions, ("Z", "Y"))

    left_semi = predictions[left_semi_slot]
    right_semi = predictions[right_semi_slot]

    # Both semis land at the same vertical midpoint; separate them horizontally.
    # Spacing with box_w=3.4 (half=1.7): cols end at 15 and 31; semis at 19 and
    # 27; championship at 23.  Each adjacent pair has ~0.6 unit clearance.
    left_semi_x = 19.0
    right_semi_x = 27.0
    left_semi_y = (w_final[1] + x_final[1]) / 2.0
    right_semi_y = (z_final[1] + y_final[1]) / 2.0

    draw_game_box(ax, left_semi_x, left_semi_y, left_semi, box_w, box_h, "#eef2ff", "#6366f1", 7)
    draw_game_box(ax, right_semi_x, right_semi_y, right_semi, box_w, box_h, "#eef2ff", "#6366f1", 7)

    connect_boxes(ax, w_final[0], w_final[1], left_semi_x, left_semi_y)
    connect_boxes(ax, x_final[0], x_final[1], left_semi_x, left_semi_y)
    connect_boxes(ax, z_final[0], z_final[1], right_semi_x, right_semi_y)
    connect_boxes(ax, y_final[0], y_final[1], right_semi_x, right_semi_y)

    championship = predictions["R6CH"]
    champ_x = 23.0
    champ_y = (left_semi_y + right_semi_y) / 2.0
    draw_game_box(ax, champ_x, champ_y, championship, box_w + 0.4, box_h + 0.2, "#dcfce7", "#16a34a", 8)

    connect_boxes(ax, left_semi_x, left_semi_y, champ_x, champ_y)
    connect_boxes(ax, right_semi_x, right_semi_y, champ_x, champ_y)

    ax.text(9.0, top_origin + 11.5, "Region W", fontsize=10, fontweight="bold", ha="center")
    ax.text(9.0, bottom_origin + 11.5, "Region X", fontsize=10, fontweight="bold", ha="center")
    ax.text(37.0, top_origin + 11.5, "Region Z", fontsize=10, fontweight="bold", ha="center")
    ax.text(37.0, bottom_origin + 11.5, "Region Y", fontsize=10, fontweight="bold", ha="center")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=16)
    ax.set_xlim(0.0, 46.0)
    ax.set_ylim(-1.0, 28.0)
    ax.axis("off")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def default_inputs(project_root: Path) -> List[Tuple[str, Path, Path]]:
    output_dir = project_root / "bracket vizualisations"
    return [
        (
            "2026 Bracket - Updated Feature List",
            project_root / "Updated Feature List Model Creation" / "results" / "Production" / "2026_bracket_predictions.csv",
            output_dir / "2026_bracket_updated_feature_list.png",
        ),
        (
            "2026 Bracket - Original",
            project_root / "Model Creation" / "Results" / "Production" / "2026_bracket_predictions.csv",
            output_dir / "2026_bracket_original.png",
        ),
        (
            "2026 Bracket - Weighted Points",
            project_root / "Model Creation Weighted Points" / "Results" / "Production" / "2026_bracket_predictions_weighted_points.csv",
            output_dir / "2026_bracket_weighted_points.png",
        ),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate visual tournament bracket PNGs from predicted bracket CSV outputs. "
            "By default, creates visuals for updated/original/weighted branches."
        )
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root folder.",
    )
    parser.add_argument(
        "--single-input",
        type=Path,
        default=None,
        help="Optional single CSV input path.",
    )
    parser.add_argument(
        "--single-output",
        type=Path,
        default=None,
        help="Optional single PNG output path (used with --single-input).",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="2026 Bracket",
        help="Title used with single-input mode.",
    )
    return parser.parse_args()


def validate_slots(predictions: Dict[str, GamePrediction]) -> None:
    required = ["R6CH", "R5WX", "R5YZ"]
    for region in ["W", "X", "Y", "Z"]:
        required.extend([region_slot(1, region, i) for i in range(1, 9)])
        required.extend([region_slot(2, region, i) for i in range(1, 5)])
        required.extend([region_slot(3, region, i) for i in range(1, 3)])
        required.append(region_slot(4, region, 1))

    missing = [slot for slot in required if slot not in predictions]
    if missing:
        raise ValueError(
            "Missing expected slots in bracket predictions: " + ", ".join(sorted(missing))
        )


def run_batch(items: Iterable[Tuple[str, Path, Path]]) -> None:
    for title, csv_input, png_output in items:
        if not csv_input.exists():
            raise FileNotFoundError(f"Missing input CSV: {csv_input}")
        predictions = load_predictions(csv_input)
        validate_slots(predictions)
        create_bracket_figure(predictions, title, png_output)
        print(f"Saved: {png_output}")


def main() -> None:
    args = parse_args()
    project_root = args.project_root.resolve()

    if args.single_input:
        single_input = args.single_input.resolve()
        if args.single_output:
            single_output = args.single_output.resolve()
        else:
            single_output = (project_root / "bracket vizualisations" / "2026_bracket_single.png").resolve()
        run_batch([(args.title, single_input, single_output)])
        return

    run_batch(default_inputs(project_root))


if __name__ == "__main__":
    main()

