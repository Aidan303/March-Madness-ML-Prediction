from __future__ import annotations

from pathlib import Path
import re

import pandas as pd

_BASE_DATA_DIR = (
    Path(__file__).resolve().parents[2] / "march-machine-learning-mania-2026-base-data"
)
_DEFAULT_KENPOM_PATH = Path(__file__).resolve().parents[2] / "Sample Kenpom data for 2026.csv"


def _normalize_name(name: object) -> str:
    if not isinstance(name, str):
        return ""
    lowered = name.strip().lower()
    lowered = lowered.replace("&", "and")
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


def _resolve_base_data_dir(data_dir: str | Path | None) -> Path:
    if data_dir is None:
        return _BASE_DATA_DIR
    return Path(data_dir)


def _resolve_kenpom_path(kenpom_path: str | Path | None) -> Path:
    if kenpom_path is None:
        return _DEFAULT_KENPOM_PATH
    return Path(kenpom_path)


def _team_name_spellings(team_id: int, base_dir: Path) -> set[str]:
    spellings_path = base_dir / "MTeamSpellings.csv"
    teams_path = base_dir / "MTeams.csv"

    if not spellings_path.exists():
        raise FileNotFoundError(f"Missing spellings file: {spellings_path}")
    if not teams_path.exists():
        raise FileNotFoundError(f"Missing teams file: {teams_path}")

    spellings_df = pd.read_csv(spellings_path)
    teams_df = pd.read_csv(teams_path)

    names: set[str] = set()

    spell_rows = spellings_df[spellings_df["TeamID"] == team_id]
    for val in spell_rows["TeamNameSpelling"].tolist():
        norm = _normalize_name(val)
        if norm:
            names.add(norm)

    team_rows = teams_df[teams_df["TeamID"] == team_id]
    if team_rows.empty:
        raise ValueError(f"Unknown TeamID in MTeams.csv: {team_id}")

    official_name = team_rows.iloc[0]["TeamName"]
    norm_official = _normalize_name(official_name)
    if norm_official:
        names.add(norm_official)

    return names


def _kenpom_aliases(row: pd.Series) -> dict[str, float | int | str | None]:
    alias_map = {
        "Tempo": "kp_tempo",
        "AdjTempo": "kp_adjtempo",
        "OE": "kp_oe",
        "AdjOE": "kp_adjoe",
        "DE": "kp_de",
        "AdjDE": "kp_adjde",
        "AdjEM": "kp_adjem",
        "RankTempo": "kp_rank_tempo",
        "RankAdjTempo": "kp_rank_adjtempo",
        "RankOE": "kp_rank_oe",
        "RankAdjOE": "kp_rank_adjoe",
        "RankDE": "kp_rank_de",
        "RankAdjDE": "kp_rank_adjde",
        "RankAdjEM": "kp_rank_adjem",
        "Seed": "kp_seed",
    }

    out: dict[str, float | int | str | None] = {}
    for src, dst in alias_map.items():
        out[dst] = row[src] if src in row.index else None

    # Useful aliases expected by downstream feature pipelines.
    out["kp_adjnetrtg"] = out.get("kp_adjem")
    out["kp_team_name"] = row["TeamName"] if "TeamName" in row.index else None
    out["kp_season"] = row["Season"] if "Season" in row.index else None
    return out


def load_kenpom(
    team_id: int,
    season: int,
    kenpom_path: str | Path | None = None,
    data_dir: str | Path | None = None,
) -> dict[str, float | int | str | None]:
    """Load one team's KenPom row for a season.

    Returns a dict containing both original KenPom columns and `kp_*` aliases.
    Name resolution uses Kaggle spellings to bridge naming differences (e.g.
    "Abilene Chr" vs "Abilene Christian").
    """
    kp_path = _resolve_kenpom_path(kenpom_path)
    base_dir = _resolve_base_data_dir(data_dir)

    if not kp_path.exists():
        raise FileNotFoundError(f"Missing KenPom file: {kp_path}")

    kp_df = pd.read_csv(kp_path)
    if "Season" not in kp_df.columns or "TeamName" not in kp_df.columns:
        raise ValueError("KenPom file must contain 'Season' and 'TeamName' columns")

    kp_season = kp_df[kp_df["Season"] == season].copy()
    if kp_season.empty:
        raise ValueError(f"No KenPom rows found for season {season}")

    candidates = _team_name_spellings(team_id, base_dir)
    kp_season["_norm_name"] = kp_season["TeamName"].apply(_normalize_name)

    matches = kp_season[kp_season["_norm_name"].isin(candidates)].copy()
    if matches.empty:
        preview = ", ".join(sorted(list(candidates))[:8])
        raise ValueError(
            f"No KenPom match for TeamID={team_id}, season={season}. "
            f"Candidate normalized names: {preview}"
        )

    if len(matches) > 1:
        # Prefer exact official team name match if available; otherwise take first.
        teams_df = pd.read_csv(base_dir / "MTeams.csv")
        official = teams_df.loc[teams_df["TeamID"] == team_id, "TeamName"]
        official_norm = _normalize_name(official.iloc[0]) if not official.empty else ""
        exact = matches[matches["_norm_name"] == official_norm]
        if not exact.empty:
            chosen = exact.iloc[0]
        else:
            chosen = matches.iloc[0]
    else:
        chosen = matches.iloc[0]

    # Merge raw KenPom row fields with standardized aliases.
    raw = {k: (None if pd.isna(v) else v) for k, v in chosen.drop(labels=["_norm_name"]).to_dict().items()}
    out = dict(raw)
    out.update(_kenpom_aliases(chosen))
    out["team_id"] = team_id
    out["season"] = season

    return out
