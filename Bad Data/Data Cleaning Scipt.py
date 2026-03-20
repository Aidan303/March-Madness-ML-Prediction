from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
STATS_TABLES_DIR = BASE_DIR / "Data" / "Historic Data" / "Kenpom Data" / "Stats Tables"
NCAA_SUMMARY_DIR = BASE_DIR / "Data" / "Historic Data" / "NCAA Summary Data"
TEAM_NAME_MAPPING_CSV = (
	BASE_DIR
	/ "Data"
	/ "Historic Data"
	/ "Kenpom Data"
	/ "Reference Tables"
	/ "REF _ NCAAM Conference and ESPN Team Name Mapping.csv"
)
OUTPUT_CSV = (
	BASE_DIR
	/ "Data"
	/ "Historic Data"
	/ "Kenpom Data"
	/ "Cleaned"
	/ "Kenpom_Master_TeamSeason.csv"
)
CHECKPOINT_DIR = OUTPUT_CSV.parent / "checkpoints"
DATA_QUALITY_DIR = OUTPUT_CSV.parent / "data_quality"
COMBINED_OUTPUT_CSV = (
	BASE_DIR
	/ "Data"
	/ "Historic Data"
	/ "Combined"
	/ "Cleaned"
	/ "TeamSeason_Master_Kenpom_NCAA.csv"
)
KENPOM_ONLY_OUTPUT_CSV = (
	BASE_DIR
	/ "Data"
	/ "Historic Data"
	/ "Combined"
	/ "Cleaned"
	/ "TeamSeason_Master_Kenpom_ONLY.csv"
)
NCAA_CHECKPOINT_DIR = COMBINED_OUTPUT_CSV.parent / "checkpoints"
NCAA_DATA_QUALITY_DIR = COMBINED_OUTPUT_CSV.parent / "data_quality"
GOLD_DIR = COMBINED_OUTPUT_CSV.parent / "gold"
GOLD_LATEST_CSV = GOLD_DIR / "TeamSeason_Master_Kenpom_NCAA_GOLD.csv"
KENPOM_ONLY_GOLD_LATEST_CSV = GOLD_DIR / "TeamSeason_Master_Kenpom_ONLY_GOLD.csv"

KEY_COLUMNS = ["team_season_key", "Season", "TeamName_std"]
EXCLUDED_FILES = {"INT _ KenPom _ Summary.csv"}

# Keep a deterministic order. Pre-Tournament summary is used; regular Summary is excluded.
PREFERRED_FILE_ORDER = [
	"INT _ KenPom _ Summary (Pre-Tournament).csv",
	"INT _ KenPom _ Efficiency.csv",
	"INT _ KenPom _ Offense.csv",
	"INT _ KenPom _ Defense.csv",
	"INT _ KenPom _ Point Distribution.csv",
	"INT _ KenPom _ Miscellaneous Team Stats.csv",
	"INT _ KenPom _ Height.csv",
]

_TEAM_NAME_CANONICAL_MAP: dict[str, str] | None = None
_TEAM_NAME_COMPACT_MAP: dict[str, str] | None = None


def normalize_column_name(value: str) -> str:
	lowered = str(value).strip().lower()
	lowered = re.sub(r"[^a-z0-9]+", "_", lowered)
	return re.sub(r"_+", "_", lowered).strip("_")


def standardize_team_name(value: object) -> str:
	if pd.isna(value):
		return ""
	text = str(value).strip().upper()
	text = re.sub(r"[^A-Z0-9\s]", "", text)
	text = re.sub(r"\s+", " ", text).strip()
	return text


def compact_team_name(value: str) -> str:
	return re.sub(r"[^A-Z0-9]", "", value)


def load_team_name_canonical_map() -> dict[str, str]:
	global _TEAM_NAME_CANONICAL_MAP, _TEAM_NAME_COMPACT_MAP
	if _TEAM_NAME_CANONICAL_MAP is not None:
		return _TEAM_NAME_CANONICAL_MAP

	canonical_map: dict[str, str] = {}
	if TEAM_NAME_MAPPING_CSV.exists():
		mapping_df = pd.read_csv(TEAM_NAME_MAPPING_CSV)
		mapping_df.columns = [str(col).strip() for col in mapping_df.columns]
		norm_cols = {normalize_column_name(c): c for c in mapping_df.columns}

		team_col = norm_cols.get("teamname")
		mapped_col = norm_cols.get("mapped_espn_team_name")

		if team_col and mapped_col:
			for _, row in mapping_df[[team_col, mapped_col]].dropna(how="all").iterrows():
				raw_name = standardize_team_name(row.get(team_col))
				mapped_name = standardize_team_name(row.get(mapped_col))
				if raw_name and mapped_name:
					canonical_map[raw_name] = mapped_name
					canonical_map[mapped_name] = mapped_name

	# High-value explicit aliases in case they are missing from the reference file.
	manual_aliases = {
		"BOISE ST": "BOISE STATE",
		"BRIGHAM YOUNG": "BYU",
		"BRIGHAM YOUNG NCAA": "BYU",
		"NEVADALAS VEGAS": "UNLV",
		"NEVADALAS VEGAS NCAA": "UNLV",
		"MARYLANDBALTIMORE COUNTY": "UMBC",
		"MARYLANDBALTIMORE COUNTY NCAA": "UMBC",
		"LOYOLA IL": "LOYOLA CHICAGO",
		"LOYOLA IL NCAA": "LOYOLA CHICAGO",
		"FDU": "FAIRLEIGH DICKINSON",
		"FDU NCAA": "FAIRLEIGH DICKINSON",
		"PRAIRIE VIEW": "PRAIRIE VIEW AM",
		"PRAIRIE VIEW NCAA": "PRAIRIE VIEW AM",
		"APPALACHIAN STATE": "APP STATE",
		"APPALACHIAN STATE NCAA": "APP STATE",
		"TEXASRIO GRANDE VALLEY": "UT RIO GRANDE VALLEY",
		"TEXASRIO GRANDE VALLEY NCAA": "UT RIO GRANDE VALLEY",
		"MASSACHUSETTSLOWELL": "UMASS LOWELL",
		"MASSACHUSETTSLOWELL NCAA": "UMASS LOWELL",
		"WINSTOMSALEM": "WINSTONSALEM",
		"WINSTOMSALEM NCAA": "WINSTONSALEM",
	}
	for alias, canonical in manual_aliases.items():
		canonical_map[standardize_team_name(alias)] = standardize_team_name(canonical)

	# Build compact form map for spacing/punctuation variation handling.
	compact_candidates: dict[str, set[str]] = {}
	for alias_name, canonical_name in canonical_map.items():
		comp = compact_team_name(alias_name)
		if not comp:
			continue
		compact_candidates.setdefault(comp, set()).add(canonical_name)

	compact_map: dict[str, str] = {}
	for comp, canon_set in compact_candidates.items():
		if len(canon_set) == 1:
			compact_map[comp] = next(iter(canon_set))

	_TEAM_NAME_CANONICAL_MAP = canonical_map
	_TEAM_NAME_COMPACT_MAP = compact_map
	print(f"Loaded canonical team-name map entries: {len(_TEAM_NAME_CANONICAL_MAP)}")
	print(f"Loaded compact team-name map entries: {len(_TEAM_NAME_COMPACT_MAP)}")
	return _TEAM_NAME_CANONICAL_MAP


def canonicalize_team_name(value: object) -> str:
	std = standardize_team_name(value)
	if not std:
		return std
	name_map = load_team_name_canonical_map()
	compact_map = _TEAM_NAME_COMPACT_MAP or {}

	# Candidate variants to catch common random suffixes or spacing issues.
	candidates = [std]

	# Remove trailing numeric tokens (e.g., duplicate export artifacts like "TEAM 1").
	trimmed_numeric = re.sub(r"\s+\d+$", "", std).strip()
	if trimmed_numeric and trimmed_numeric not in candidates:
		candidates.append(trimmed_numeric)

	# Try progressive trailing token trim for random suffix words.
	tokens = std.split()
	for cut in [1, 2]:
		if len(tokens) - cut >= 1:
			trimmed = " ".join(tokens[: len(tokens) - cut]).strip()
			if trimmed and trimmed not in candidates:
				candidates.append(trimmed)

	for cand in candidates:
		if cand in name_map:
			return name_map[cand]
		comp = compact_team_name(cand)
		if comp in compact_map:
			return compact_map[comp]

	# Fallback to raw standardized name.
	return std


def normalize_season(value: object) -> str:
	if pd.isna(value):
		return ""
	text = str(value).strip()
	if re.fullmatch(r"\d+\.0", text):
		return text.split(".")[0]
	return text


def build_team_season_key(season: str, team_name_std: str) -> str:
	return f"{season}__{team_name_std}"


def source_token_from_filename(file_path: Path) -> str:
	stem = file_path.stem
	stem = stem.replace("INT _ KenPom _", "").strip()
	token = normalize_column_name(stem)
	return f"kenpom_{token}"


def ncaa_source_token() -> str:
	return "ncaa_summary"


def prefix_non_key_columns(df: pd.DataFrame, key_columns: set[str], token: str) -> pd.DataFrame:
	new_columns: list[str] = []
	seen: dict[str, int] = {}

	for idx, col in enumerate(df.columns):
		if col in key_columns:
			new_columns.append(col)
			continue

		norm = normalize_column_name(col)
		if not norm:
			norm = f"col_{idx}"
		base_name = f"{token}__{norm}"

		if base_name not in seen:
			seen[base_name] = 1
			new_columns.append(base_name)
		else:
			seen[base_name] += 1
			new_columns.append(f"{base_name}__{seen[base_name]}")

	out = df.copy()
	out.columns = new_columns
	return out


def resolve_key_columns(df: pd.DataFrame, file_name: str) -> tuple[str, str]:
	normalized_to_original = {normalize_column_name(col): col for col in df.columns}

	season_col = normalized_to_original.get("season")
	team_col = normalized_to_original.get("teamname") or normalized_to_original.get("team")

	if season_col is None or team_col is None:
		raise ValueError(
			f"Required key columns not found in {file_name}. "
			"Expected Season and TeamName/Team."
		)

	return season_col, team_col


def list_input_files() -> list[Path]:
	available = {p.name: p for p in STATS_TABLES_DIR.glob("*.csv")}
	selected: list[Path] = []

	for file_name in PREFERRED_FILE_ORDER:
		if file_name in EXCLUDED_FILES:
			continue
		path = available.get(file_name)
		if path is not None:
			selected.append(path)

	# Include any additional CSVs not in the preferred order and not excluded.
	for file_name, path in sorted(available.items()):
		if file_name in EXCLUDED_FILES:
			continue
		if path not in selected:
			selected.append(path)

	return selected


def list_ncaa_files() -> list[Path]:
	csv_files = list(NCAA_SUMMARY_DIR.glob("*.csv"))
	return sorted(csv_files, key=lambda p: p.name)


def parse_ncaa_season_end_year(file_path: Path) -> str:
	match = re.search(r"(\d{4})-(\d{2})", file_path.stem)
	if not match:
		raise ValueError(f"Could not parse season from NCAA file name: {file_path.name}")
	start_year = match.group(1)
	end_suffix = match.group(2)
	end_year = f"{start_year[:2]}{end_suffix}"
	return end_year


def clean_kenpom_file(file_path: Path) -> pd.DataFrame:
	df = pd.read_csv(file_path)
	df.columns = [str(col).strip() for col in df.columns]

	season_col, team_col = resolve_key_columns(df, file_path.name)

	df["Season"] = df[season_col].map(normalize_season)
	df["TeamName_std"] = df[team_col].map(canonicalize_team_name)
	df["team_season_key"] = df.apply(
		lambda row: build_team_season_key(row["Season"], row["TeamName_std"]),
		axis=1,
	)

	duplicate_count = int(df["team_season_key"].duplicated().sum())
	if duplicate_count > 0:
		print(f"[{file_path.name}] duplicate keys found: {duplicate_count}. Keeping first occurrence.")
		df = df.drop_duplicates(subset=["team_season_key"], keep="first")

	token = source_token_from_filename(file_path)
	df = prefix_non_key_columns(
		df,
		key_columns={"Season", season_col, team_col, "TeamName_std", "team_season_key"},
		token=token,
	)

	stats_columns = [
		c
		for c in df.columns
		if c not in {season_col, team_col, "Season", "TeamName_std", "team_season_key"}
	]
	cleaned = df[["team_season_key", "Season", "TeamName_std", *stats_columns]].copy()
	return cleaned


def clean_ncaa_file(file_path: Path) -> pd.DataFrame:
	try:
		df = pd.read_csv(file_path)
	except Exception as exc:
		raise RuntimeError(f"Failed reading NCAA CSV file {file_path.name}: {exc}") from exc

	df.columns = [str(col).strip() for col in df.columns]
	df = df.dropna(axis=1, how="all")

	normalized_to_original = {normalize_column_name(col): col for col in df.columns}
	school_col = normalized_to_original.get("school") or normalized_to_original.get("teamname") or normalized_to_original.get("team")

	# NCAA files often include a first metadata header row; retry with header row 2.
	if school_col is None:
		try:
			df = pd.read_csv(file_path, header=1)
		except Exception as exc:
			raise RuntimeError(f"Failed reading NCAA CSV file {file_path.name} with header=1: {exc}") from exc

		df.columns = [str(col).strip() for col in df.columns]
		df = df.dropna(axis=1, how="all")
		normalized_to_original = {normalize_column_name(col): col for col in df.columns}
		school_col = normalized_to_original.get("school") or normalized_to_original.get("teamname") or normalized_to_original.get("team")

	if school_col is None:
		raise ValueError(
			f"Required team-name column not found in NCAA file: {file_path.name}. "
			"Expected School/TeamName/Team."
		)

	season = parse_ncaa_season_end_year(file_path)
	df["Season"] = season
	df["TeamName_std"] = df[school_col].map(canonicalize_team_name)
	df["team_season_key"] = df.apply(
		lambda row: build_team_season_key(row["Season"], row["TeamName_std"]),
		axis=1,
	)

	duplicate_count = int(df["team_season_key"].duplicated().sum())
	if duplicate_count > 0:
		print(f"[{file_path.name}] duplicate keys found: {duplicate_count}. Keeping first occurrence.")
		df = df.drop_duplicates(subset=["team_season_key"], keep="first")

	token = ncaa_source_token()
	df = prefix_non_key_columns(
		df,
		key_columns={school_col, "Season", "TeamName_std", "team_season_key"},
		token=token,
	)

	stats_columns = [
		c
		for c in df.columns
		if c not in {school_col, "Season", "TeamName_std", "team_season_key"}
	]
	cleaned = df[["team_season_key", "Season", "TeamName_std", *stats_columns]].copy()
	return cleaned


def merge_into_master(master_df: pd.DataFrame | None, incoming_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
	incoming_keys = set(incoming_df["team_season_key"])

	if master_df is None:
		diagnostics = {
			"rows_before": 0,
			"rows_after": len(incoming_df),
			"matched_keys": 0,
			"new_keys": len(incoming_keys),
		}
		return incoming_df.copy(), diagnostics

	master_keys = set(master_df["team_season_key"])
	matched_keys = len(master_keys.intersection(incoming_keys))
	new_keys = len(incoming_keys - master_keys)

	rows_before = len(master_df)

	master = master_df.set_index("team_season_key")
	incoming = incoming_df.set_index("team_season_key")

	union_index = master.index.union(incoming.index)
	master = master.reindex(union_index)
	incoming = incoming.reindex(union_index)

	# Ensure key descriptor columns stay aligned and populated.
	for key_col in ["Season", "TeamName_std"]:
		if key_col not in master.columns:
			master[key_col] = pd.NA
		master[key_col] = master[key_col].combine_first(incoming[key_col])

	for col in incoming.columns:
		if col in {"Season", "TeamName_std"}:
			continue
		if col in master.columns:
			master[col] = master[col].combine_first(incoming[col])
		else:
			master[col] = incoming[col]

	merged = master.reset_index().rename(columns={"index": "team_season_key"})

	diagnostics = {
		"rows_before": rows_before,
		"rows_after": len(merged),
		"matched_keys": matched_keys,
		"new_keys": new_keys,
	}
	return merged, diagnostics


def write_checkpoint(master_df: pd.DataFrame, output_csv: Path, checkpoint_dir: Path, file_index: int, file_name: str) -> None:
	output_csv.parent.mkdir(parents=True, exist_ok=True)
	checkpoint_dir.mkdir(parents=True, exist_ok=True)

	# Overwrite checkpoint/master file after every processed source file.
	try:
		master_df.to_csv(output_csv, index=False)
	except PermissionError:
		ts = datetime.now().strftime("%Y%m%d_%H%M%S")
		fallback = output_csv.parent / f"{output_csv.stem}_locked_fallback_{ts}.csv"
		master_df.to_csv(fallback, index=False)
		print(
			f"[WARN] Output file locked; wrote checkpoint fallback instead: {fallback}"
		)

	safe_name = normalize_column_name(Path(file_name).stem)
	checkpoint_file = checkpoint_dir / f"{file_index:02d}_{safe_name}.csv"
	master_df.to_csv(checkpoint_file, index=False)


def finalize_master(master_df: pd.DataFrame) -> pd.DataFrame:
	ordered_front = [c for c in KEY_COLUMNS if c in master_df.columns]
	remaining = [c for c in master_df.columns if c not in ordered_front]
	finalized = master_df[ordered_front + remaining].copy()

	# Defensive re-normalization catches season formatting drift and late alias updates.
	if "Season" in finalized.columns:
		finalized["Season"] = finalized["Season"].map(normalize_season)
	if "TeamName_std" in finalized.columns:
		finalized["TeamName_std"] = finalized["TeamName_std"].map(canonicalize_team_name)
	if {"Season", "TeamName_std"}.issubset(finalized.columns):
		finalized["team_season_key"] = finalized.apply(
			lambda row: build_team_season_key(row["Season"], row["TeamName_std"]),
			axis=1,
		)

	# Remove a known bad row introduced by collection error.
	if {"Season", "TeamName_std"}.issubset(finalized.columns):
		bad_row_mask = (
			(finalized["Season"].astype(str).str.strip() == "2007")
			& (finalized["TeamName_std"].astype(str).str.strip() == "CAL STATE BAKERSFIELD")
		)
		finalized = finalized.loc[~bad_row_mask].copy()

	# Coalesce rows that collapse to the same key after normalization.
	if "team_season_key" in finalized.columns and finalized["team_season_key"].duplicated().any():
		def _first_populated(series: pd.Series) -> object:
			for val in series:
				if pd.notna(val) and str(val).strip() != "":
					return val
			return ""

		finalized = (
			finalized.groupby("team_season_key", as_index=False, sort=False)
			.agg(_first_populated)
		)

	finalized = finalized.sort_values("team_season_key").reset_index(drop=True)
	return finalized


def build_data_quality_reports(
	final_df: pd.DataFrame,
	per_file_stats: list[dict[str, object]],
	report_dir: Path,
	file_prefix: str = "",
) -> None:
	report_dir.mkdir(parents=True, exist_ok=True)

	# 1) Missingness profile by column.
	missingness_rows = []
	total_rows = len(final_df)
	for col in final_df.columns:
		missing_count = int(final_df[col].isna().sum())
		missing_pct = (missing_count / total_rows * 100.0) if total_rows else 0.0
		missingness_rows.append(
			{
				"column": col,
				"missing_count": missing_count,
				"missing_pct": round(missing_pct, 4),
				"non_null_count": int(total_rows - missing_count),
			}
		)
	missingness_df = pd.DataFrame(missingness_rows).sort_values(
		["missing_pct", "column"], ascending=[False, True]
	)

	# 2) Season-level coverage summary.
	season_group = final_df.groupby("Season", dropna=False)
	season_coverage_df = (
		season_group.agg(
			rows=("team_season_key", "size"),
			unique_teams=("TeamName_std", "nunique"),
		)
		.reset_index()
	)
	season_coverage_df["Season_sort"] = season_coverage_df["Season"].astype(str)
	season_coverage_df = season_coverage_df.sort_values("Season_sort").drop(columns=["Season_sort"])

	# 3) Per-file merge diagnostics from pipeline execution.
	merge_diag_df = pd.DataFrame(per_file_stats)

	missingness_path = report_dir / f"{file_prefix}missingness_by_column.csv"
	season_coverage_path = report_dir / f"{file_prefix}season_coverage_summary.csv"
	merge_diag_path = report_dir / f"{file_prefix}merge_diagnostics.csv"

	missingness_df.to_csv(missingness_path, index=False)
	season_coverage_df.to_csv(season_coverage_path, index=False)
	merge_diag_df.to_csv(merge_diag_path, index=False)

	print("\n=== Data Quality Reports ===")
	print(f"- {missingness_path}")
	print(f"- {season_coverage_path}")
	print(f"- {merge_diag_path}")


def run_dataset_qa(
	final_df: pd.DataFrame,
	report_dir: Path,
	qa_prefix: str,
	unmatched_vs_baseline_count: int | None = None,
	enforce: bool = False,
) -> tuple[bool, Path]:
	report_dir.mkdir(parents=True, exist_ok=True)

	columns = set(final_df.columns)
	stat_columns = [c for c in final_df.columns if c not in KEY_COLUMNS]
	non_prefixed_stat_count = sum(
		1
		for c in stat_columns
		if not (c.startswith("kenpom_") or c.startswith("ncaa_summary__"))
	)

	checks: list[dict[str, object]] = [
		{
			"check": "row_count_positive",
			"status": "PASS" if len(final_df) > 0 else "FAIL",
			"value": int(len(final_df)),
			"threshold_or_expectation": "> 0",
		},
		{
			"check": "required_key_columns_present",
			"status": "PASS" if set(KEY_COLUMNS).issubset(columns) else "FAIL",
			"value": int(sum(1 for c in KEY_COLUMNS if c in columns)),
			"threshold_or_expectation": f"all {len(KEY_COLUMNS)} key columns",
		},
		{
			"check": "duplicate_team_season_key_count",
			"status": "PASS" if int(final_df["team_season_key"].duplicated().sum()) == 0 else "FAIL",
			"value": int(final_df["team_season_key"].duplicated().sum()),
			"threshold_or_expectation": "== 0",
		},
		{
			"check": "blank_team_season_key_count",
			"status": "PASS"
			if int(final_df["team_season_key"].astype(str).str.strip().eq("").sum()) == 0
			else "FAIL",
			"value": int(final_df["team_season_key"].astype(str).str.strip().eq("").sum()),
			"threshold_or_expectation": "== 0",
		},
		{
			"check": "blank_teamname_std_count",
			"status": "PASS"
			if int(final_df["TeamName_std"].astype(str).str.strip().eq("").sum()) == 0
			else "FAIL",
			"value": int(final_df["TeamName_std"].astype(str).str.strip().eq("").sum()),
			"threshold_or_expectation": "== 0",
		},
		{
			"check": "season_decimal_suffix_count",
			"status": "PASS"
			if int(final_df["Season"].astype(str).str.contains(r"\\.0$").sum()) == 0
			else "FAIL",
			"value": int(final_df["Season"].astype(str).str.contains(r"\\.0$").sum()),
			"threshold_or_expectation": "== 0",
		},
		{
			"check": "non_prefixed_stat_column_count",
			"status": "PASS" if non_prefixed_stat_count == 0 else "FAIL",
			"value": int(non_prefixed_stat_count),
			"threshold_or_expectation": "== 0",
		},
	]

	if unmatched_vs_baseline_count is not None:
		checks.append(
			{
				"check": "ncaa_unmatched_vs_kenpom_count",
				"status": "PASS" if int(unmatched_vs_baseline_count) == 0 else "WARN",
				"value": int(unmatched_vs_baseline_count),
				"threshold_or_expectation": "== 0",
			}
		)

	qa_df = pd.DataFrame(checks)
	qa_path = report_dir / f"{qa_prefix}qa_checks.csv"
	qa_df.to_csv(qa_path, index=False)

	fail_count = int((qa_df["status"] == "FAIL").sum())
	warn_count = int((qa_df["status"] == "WARN").sum())
	pass_count = int((qa_df["status"] == "PASS").sum())

	print("\n=== QA Checks ===")
	print(f"PASS: {pass_count} | WARN: {warn_count} | FAIL: {fail_count}")
	print(f"- {qa_path}")

	passed = fail_count == 0
	if enforce and not passed:
		raise ValueError(f"QA checks failed. See report: {qa_path}")
	return passed, qa_path


def write_gold_snapshot(
	final_df: pd.DataFrame,
	source_csv_path: Path,
	qa_report_path: Path,
	qa_passed: bool,
	dataset_tag: str,
	latest_gold_path: Path,
) -> tuple[Path, Path]:
	GOLD_DIR.mkdir(parents=True, exist_ok=True)
	stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	snapshot_path = GOLD_DIR / f"{dataset_tag}_GOLD_{stamp}.csv"
	manifest_path = GOLD_DIR / f"{dataset_tag}_GOLD_{stamp}_manifest.txt"

	shutil.copy2(source_csv_path, snapshot_path)
	shutil.copy2(source_csv_path, latest_gold_path)

	manifest_lines = [
		f"created_at={datetime.now().isoformat(timespec='seconds')}",
		f"dataset_tag={dataset_tag}",
		f"source_csv={source_csv_path}",
		f"gold_latest_csv={latest_gold_path}",
		f"gold_snapshot_csv={snapshot_path}",
		f"row_count={len(final_df)}",
		f"column_count={len(final_df.columns)}",
		f"unique_team_season_keys={final_df['team_season_key'].nunique()}",
		f"qa_passed={qa_passed}",
		f"qa_report={qa_report_path}",
	]
	manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

	print("\n=== Gold Snapshot ===")
	print(f"Latest gold file: {latest_gold_path}")
	print(f"Timestamped snapshot: {snapshot_path}")
	print(f"Manifest: {manifest_path}")
	return snapshot_path, manifest_path


def run_merge_pipeline(enforce_qa: bool = False, lock_gold: bool = False) -> None:
	input_files = list_input_files()
	if not input_files:
		raise FileNotFoundError(f"No input CSV files found in {STATS_TABLES_DIR}")

	print("=== KenPom Merge Pipeline ===")
	print(f"Input directory: {STATS_TABLES_DIR}")
	print(f"Output file: {OUTPUT_CSV}")
	print(f"Files to process ({len(input_files)}):")
	for p in input_files:
		print(f"  - {p.name}")

	master_df: pd.DataFrame | None = None
	per_file_stats: list[dict[str, object]] = []

	for idx, file_path in enumerate(input_files, start=1):
		cleaned_df = clean_kenpom_file(file_path)
		master_df, diagnostics = merge_into_master(master_df, cleaned_df)
		assert master_df is not None

		write_checkpoint(master_df, OUTPUT_CSV, CHECKPOINT_DIR, idx, file_path.name)

		per_file_stats.append(
			{
				"file": file_path.name,
				"rows_in_file": len(cleaned_df),
				**diagnostics,
			}
		)

		print(
			f"[{idx}/{len(input_files)}] {file_path.name}: "
			f"rows_before={diagnostics['rows_before']}, rows_after={diagnostics['rows_after']}, "
			f"matched_keys={diagnostics['matched_keys']}, new_keys={diagnostics['new_keys']}"
		)

	final_df = finalize_master(master_df)
	final_output_path = OUTPUT_CSV
	try:
		final_df.to_csv(final_output_path, index=False)
	except PermissionError:
		ts = datetime.now().strftime("%Y%m%d_%H%M%S")
		final_output_path = OUTPUT_CSV.parent / f"{OUTPUT_CSV.stem}_locked_fallback_{ts}.csv"
		final_df.to_csv(final_output_path, index=False)
		print(f"[WARN] Final output file locked; wrote fallback final file: {final_output_path}")

	build_data_quality_reports(final_df, per_file_stats, DATA_QUALITY_DIR, file_prefix="kenpom_")
	qa_passed, qa_report_path = run_dataset_qa(
		final_df,
		DATA_QUALITY_DIR,
		qa_prefix="kenpom_",
		enforce=enforce_qa,
	)

	# Mirror a model-ready KenPom-only dataset in the combined/cleaned area.
	kenpom_only_output_path = KENPOM_ONLY_OUTPUT_CSV
	try:
		final_df.to_csv(kenpom_only_output_path, index=False)
	except PermissionError:
		ts = datetime.now().strftime("%Y%m%d_%H%M%S")
		kenpom_only_output_path = (
			KENPOM_ONLY_OUTPUT_CSV.parent
			/ f"{KENPOM_ONLY_OUTPUT_CSV.stem}_locked_fallback_{ts}.csv"
		)
		final_df.to_csv(kenpom_only_output_path, index=False)
		print(
			f"[WARN] KenPom-only output file locked; wrote fallback file: {kenpom_only_output_path}"
		)

	if lock_gold:
		write_gold_snapshot(
			final_df=final_df,
			source_csv_path=kenpom_only_output_path,
			qa_report_path=qa_report_path,
			qa_passed=qa_passed,
			dataset_tag="TeamSeason_Master_Kenpom_ONLY",
			latest_gold_path=KENPOM_ONLY_GOLD_LATEST_CSV,
		)

	duplicate_keys = int(final_df["team_season_key"].duplicated().sum())
	print("\n=== Final Summary ===")
	print(f"Processed files: {len(input_files)}")
	print(f"Final rows: {len(final_df)}")
	print(f"Unique keys: {final_df['team_season_key'].nunique()}")
	print(f"Duplicate keys: {duplicate_keys}")
	print(f"Final output: {final_output_path}")
	print(f"KenPom-only combined output: {kenpom_only_output_path}")
	print(f"Checkpoint directory: {CHECKPOINT_DIR}")


def run_ncaa_merge_pipeline(enforce_qa: bool = False, lock_gold: bool = False) -> None:
	if not OUTPUT_CSV.exists():
		raise FileNotFoundError(
			f"KenPom master file not found: {OUTPUT_CSV}. Run KenPom pipeline first."
		)

	ncaa_files = list_ncaa_files()
	if not ncaa_files:
		raise FileNotFoundError(f"No NCAA summary files found in {NCAA_SUMMARY_DIR}")

	print("\n=== NCAA Summary Merge Pipeline ===")
	print(f"Input directory: {NCAA_SUMMARY_DIR}")
	print(f"KenPom master input: {OUTPUT_CSV}")
	print(f"Combined output file: {COMBINED_OUTPUT_CSV}")
	print(f"Files to process ({len(ncaa_files)}):")
	for p in ncaa_files:
		print(f"  - {p.name}")

	master_df = pd.read_csv(OUTPUT_CSV)
	base_kenpom_keys = set(master_df["team_season_key"])
	per_file_stats: list[dict[str, object]] = []

	for idx, file_path in enumerate(ncaa_files, start=1):
		cleaned_df = clean_ncaa_file(file_path)
		master_df, diagnostics = merge_into_master(master_df, cleaned_df)

		write_checkpoint(master_df, COMBINED_OUTPUT_CSV, NCAA_CHECKPOINT_DIR, idx, file_path.name)

		per_file_stats.append(
			{
				"file": file_path.name,
				"rows_in_file": len(cleaned_df),
				**diagnostics,
			}
		)

		print(
			f"[{idx}/{len(ncaa_files)}] {file_path.name}: "
			f"rows_before={diagnostics['rows_before']}, rows_after={diagnostics['rows_after']}, "
			f"matched_keys={diagnostics['matched_keys']}, new_keys={diagnostics['new_keys']}"
		)

	final_df = finalize_master(master_df)
	final_output_path = COMBINED_OUTPUT_CSV
	try:
		final_df.to_csv(final_output_path, index=False)
	except PermissionError:
		ts = datetime.now().strftime("%Y%m%d_%H%M%S")
		final_output_path = COMBINED_OUTPUT_CSV.parent / f"{COMBINED_OUTPUT_CSV.stem}_locked_fallback_{ts}.csv"
		final_df.to_csv(final_output_path, index=False)
		print(f"[WARN] Final output file locked; wrote fallback final file: {final_output_path}")

	build_data_quality_reports(final_df, per_file_stats, NCAA_DATA_QUALITY_DIR, file_prefix="ncaa_")

	unmatched_vs_kenpom = final_df[~final_df["team_season_key"].isin(base_kenpom_keys)][
		["team_season_key", "Season", "TeamName_std"]
	].copy()
	unmatched_vs_kenpom = unmatched_vs_kenpom.sort_values(["Season", "TeamName_std"])
	unmatched_path = NCAA_DATA_QUALITY_DIR / "ncaa_unmatched_vs_kenpom_keys.csv"
	unmatched_vs_kenpom.to_csv(unmatched_path, index=False)

	qa_passed, qa_report_path = run_dataset_qa(
		final_df,
		NCAA_DATA_QUALITY_DIR,
		qa_prefix="ncaa_",
		unmatched_vs_baseline_count=len(unmatched_vs_kenpom),
		enforce=enforce_qa,
	)

	if lock_gold:
		write_gold_snapshot(
			final_df=final_df,
			source_csv_path=final_output_path,
			qa_report_path=qa_report_path,
			qa_passed=qa_passed,
			dataset_tag="TeamSeason_Master_Kenpom_NCAA",
			latest_gold_path=GOLD_LATEST_CSV,
		)

	duplicate_keys = int(final_df["team_season_key"].duplicated().sum())
	print("\n=== NCAA Merge Final Summary ===")
	print(f"Processed files: {len(ncaa_files)}")
	print(f"Final rows: {len(final_df)}")
	print(f"Unique keys: {final_df['team_season_key'].nunique()}")
	print(f"Duplicate keys: {duplicate_keys}")
	print(f"Final output: {final_output_path}")
	print(f"Checkpoint directory: {NCAA_CHECKPOINT_DIR}")
	print(f"Unmatched NCAA keys vs KenPom baseline: {len(unmatched_vs_kenpom)}")
	print(f"- {unmatched_path}")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Build KenPom and NCAA team-season master datasets.")
	parser.add_argument(
		"--stage",
		choices=["kenpom", "ncaa", "both"],
		default="kenpom",
		help="Which pipeline stage to run.",
	)
	parser.add_argument(
		"--enforce-qa",
		action="store_true",
		help="Fail the run if any QA checks return FAIL.",
	)
	parser.add_argument(
		"--lock-gold",
		action="store_true",
		help="Write/refresh gold snapshot files for the combined NCAA+KenPom output.",
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	if args.stage in {"kenpom", "both"}:
		run_merge_pipeline(enforce_qa=args.enforce_qa, lock_gold=args.lock_gold)
	if args.stage in {"ncaa", "both"}:
		run_ncaa_merge_pipeline(enforce_qa=args.enforce_qa, lock_gold=args.lock_gold)

