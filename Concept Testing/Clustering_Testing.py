from __future__ import annotations

import argparse
from pathlib import Path
import shutil

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler


DEFAULT_DATA_PATH = (
	Path(__file__).resolve().parents[1] / "Data" / "College_Team_Stats.csv"
)
DEFAULT_TARGET_COLUMN = "Overall W-L%"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def infer_context_family(column_name: str) -> str:
	lower_name = column_name.lower().strip()
	if lower_name.startswith("overall "):
		return "overall"
	if lower_name.startswith("conf"):
		return "conf"
	if lower_name.startswith("home "):
		return "home"
	if lower_name.startswith("away "):
		return "away"
	return "season_total"


def load_and_prepare_data(csv_path: Path, target_column: str) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
	raw_df = pd.read_csv(csv_path)
	raw_df.columns = [str(col).strip() for col in raw_df.columns]

	# Drop placeholder columns created by repeated commas in the source CSV.
	non_empty_df = raw_df.dropna(axis=1, how="all")

	id_like_columns = {"Rk", "School", target_column}

	numeric_df = non_empty_df.apply(pd.to_numeric, errors="coerce")
	candidate_columns = [
		col
		for col in numeric_df.columns
		if col not in id_like_columns and numeric_df[col].notna().any()
	]

	model_feature_df = numeric_df[candidate_columns].copy()
	return non_empty_df, model_feature_df, candidate_columns


def print_data_summary(raw_df: pd.DataFrame, feature_columns: list[str], target_column: str) -> None:
	context_counts = {"overall": 0, "conf": 0, "home": 0, "away": 0, "season_total": 0}
	for col in feature_columns:
		context_counts[infer_context_family(col)] += 1

	print("=== Data Summary ===")
	print(f"Rows: {len(raw_df)}")
	print(f"Columns (after dropping empty placeholders): {raw_df.shape[1]}")
	print(f"Target column (excluded from clustering): {target_column}")
	print(f"Numeric feature count: {len(feature_columns)}")
	print("Feature context coverage:")
	for family, count in context_counts.items():
		print(f"  - {family}: {count}")


def evaluate_kmeans(X_scaled: np.ndarray, k_min: int, k_max: int, random_state: int) -> dict:
	k_values = range(k_min, min(k_max, len(X_scaled) - 1) + 1)
	rows = []
	best = None

	for k in k_values:
		model = KMeans(n_clusters=k, random_state=random_state, n_init=20)
		labels = model.fit_predict(X_scaled)
		sil = silhouette_score(X_scaled, labels)
		dbi = davies_bouldin_score(X_scaled, labels)
		row = {
			"algorithm": "kmeans",
			"n_clusters": k,
			"params": {"n_clusters": k, "n_init": 20},
			"labels": labels,
			"model": model,
			"silhouette": sil,
			"davies_bouldin": dbi,
			"inertia": model.inertia_,
		}
		rows.append(row)
		if best is None or row["silhouette"] > best["silhouette"]:
			best = row

	if not rows:
		raise ValueError("Not enough rows to evaluate KMeans. Need at least 3 teams.")

	return {"all_results": rows, "best": best}


def build_dbscan_search_grid(X_scaled: np.ndarray) -> tuple[list[float], list[int]]:
	# Build eps candidates from k-distance quantiles so the search is data-adaptive.
	min_samples_grid = [3, 4, 5, 6, 8, 10, 12]
	eps_candidates: set[float] = set()

	for n_neighbors in min_samples_grid:
		nn = NearestNeighbors(n_neighbors=n_neighbors)
		nn.fit(X_scaled)
		distances, _ = nn.kneighbors(X_scaled)
		k_dist = distances[:, -1]

		for q in [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]:
			eps_candidates.add(round(float(np.quantile(k_dist, q)), 3))

	# Add fixed values to keep continuity with previous baseline run.
	eps_candidates.update({0.5, 0.75, 1.0, 1.25, 1.5, 1.8, 2.0})
	eps_grid = sorted(eps for eps in eps_candidates if eps > 0)
	return eps_grid, min_samples_grid


def evaluate_dbscan(X_scaled: np.ndarray) -> dict:
	eps_grid, min_samples_grid = build_dbscan_search_grid(X_scaled)
	rows = []
	best = None

	for eps in eps_grid:
		for min_samples in min_samples_grid:
			model = DBSCAN(eps=eps, min_samples=min_samples)
			labels = model.fit_predict(X_scaled)

			non_noise_mask = labels != -1
			non_noise_labels = labels[non_noise_mask]
			unique_clusters = np.unique(non_noise_labels)
			n_clusters = len(unique_clusters)
			n_noise = int(np.sum(labels == -1))

			if n_clusters < 2:
				continue
			if non_noise_mask.sum() <= n_clusters:
				continue

			sil = silhouette_score(X_scaled[non_noise_mask], non_noise_labels)
			dbi = davies_bouldin_score(X_scaled[non_noise_mask], non_noise_labels)
			row = {
				"algorithm": "dbscan",
				"n_clusters": n_clusters,
				"params": {"eps": eps, "min_samples": min_samples},
				"labels": labels,
				"model": model,
				"silhouette": sil,
				"davies_bouldin": dbi,
				"inertia": np.nan,
				"noise_points": n_noise,
			}
			rows.append(row)
			if best is None or row["silhouette"] > best["silhouette"]:
				best = row

	return {
		"all_results": rows,
		"best": best,
		"eps_grid": eps_grid,
		"min_samples_grid": min_samples_grid,
	}


def choose_final_model(best_kmeans: dict, best_dbscan: dict | None) -> dict:
	if best_dbscan is None:
		return best_kmeans

	# Prefer DBSCAN when it is at least as separable within a small tolerance.
	if best_dbscan["silhouette"] >= best_kmeans["silhouette"] - 0.02:
		return best_dbscan
	return best_kmeans


def cluster_profile_summary(feature_df_scaled: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
	scaled_with_labels = feature_df_scaled.copy()
	scaled_with_labels["cluster_label"] = labels
	grouped = scaled_with_labels.groupby("cluster_label").mean(numeric_only=True)
	return grouped


def maybe_plot_kmeans_diagnostics(kmeans_results: list[dict]) -> None:
	try:
		import matplotlib.pyplot as plt
	except Exception:
		print("Matplotlib not available; skipping elbow/silhouette plots.")
		return

	sorted_results = sorted(kmeans_results, key=lambda row: row["n_clusters"])
	k_vals = [row["n_clusters"] for row in sorted_results]
	inertia_vals = [row["inertia"] for row in sorted_results]
	silhouette_vals = [row["silhouette"] for row in sorted_results]

	fig, axes = plt.subplots(1, 2, figsize=(12, 4))
	axes[0].plot(k_vals, inertia_vals, marker="o")
	axes[0].set_title("KMeans Elbow (Inertia)")
	axes[0].set_xlabel("k")
	axes[0].set_ylabel("Inertia")

	axes[1].plot(k_vals, silhouette_vals, marker="o")
	axes[1].set_title("KMeans Silhouette")
	axes[1].set_xlabel("k")
	axes[1].set_ylabel("Silhouette")

	plt.tight_layout()
	plt.show()


def save_cluster_scatter_plot(
	X_scaled: np.ndarray,
	labels: np.ndarray,
	raw_df: pd.DataFrame,
	target_column: str,
	output_path: Path,
	show_plot: bool,
) -> bool:
	try:
		import matplotlib.pyplot as plt
	except Exception:
		print("Matplotlib not available; skipping cluster scatter plot output.")
		return False

	pca = PCA(n_components=2, random_state=42)
	components = pca.fit_transform(X_scaled)

	fig, ax = plt.subplots(figsize=(10, 7))
	unique_labels = sorted(np.unique(labels))
	cmap = plt.get_cmap("tab10", max(len(unique_labels), 1))

	for idx, cluster_id in enumerate(unique_labels):
		mask = labels == cluster_id
		label_name = "Noise (-1)" if cluster_id == -1 else f"Cluster {cluster_id}"
		ax.scatter(
			components[mask, 0],
			components[mask, 1],
			s=35,
			alpha=0.8,
			label=label_name,
			color=cmap(idx),
		)

	variance_ratio = pca.explained_variance_ratio_
	ax.set_title("Team Tier Clusters (PCA Projection)")
	ax.set_xlabel(f"PC1 ({variance_ratio[0] * 100:.1f}% var)")
	ax.set_ylabel(f"PC2 ({variance_ratio[1] * 100:.1f}% var)")
	ax.legend(loc="best", fontsize=8)
	ax.grid(alpha=0.25)

	fig.tight_layout()

	# Label the top teams by win percentage to make best-team location explicit.
	if "School" in raw_df.columns and target_column in raw_df.columns:
		target_values = pd.to_numeric(raw_df[target_column], errors="coerce")
		top_index = target_values.nlargest(10).index
		for idx in top_index:
			if pd.isna(target_values.loc[idx]):
				continue
			team_name = str(raw_df.loc[idx, "School"])
			x_val = components[idx, 0]
			y_val = components[idx, 1]
			ax.scatter([x_val], [y_val], s=70, facecolors="none", edgecolors="black", linewidths=1.2)
			ax.annotate(
				team_name,
				(x_val, y_val),
				xytext=(5, 5),
				textcoords="offset points",
				fontsize=7,
			)

	fig.savefig(output_path, dpi=300, bbox_inches="tight")

	if show_plot:
		plt.show()
	else:
		plt.close(fig)

	return True


def run_clustering(csv_path: Path, target_column: str, show_plots: bool) -> None:
	raw_df, feature_df, feature_columns = load_and_prepare_data(csv_path, target_column)
	print_data_summary(raw_df, feature_columns, target_column)

	imputer = SimpleImputer(strategy="median")
	scaler = StandardScaler()

	X_imputed = imputer.fit_transform(feature_df)
	X_scaled = scaler.fit_transform(X_imputed)

	kmeans_eval = evaluate_kmeans(X_scaled, k_min=2, k_max=10, random_state=42)
	dbscan_eval = evaluate_dbscan(X_scaled)

	best_kmeans = kmeans_eval["best"]
	best_dbscan = dbscan_eval["best"]
	final_result = choose_final_model(best_kmeans, best_dbscan)

	print("\n=== Model Evaluation ===")
	print(
		f"Best KMeans -> k={best_kmeans['n_clusters']}, "
		f"silhouette={best_kmeans['silhouette']:.4f}, "
		f"davies_bouldin={best_kmeans['davies_bouldin']:.4f}"
	)
	if best_dbscan is not None:
		print(
			"Best DBSCAN -> "
			f"params={best_dbscan['params']}, "
			f"clusters={best_dbscan['n_clusters']}, "
			f"silhouette={best_dbscan['silhouette']:.4f}, "
			f"davies_bouldin={best_dbscan['davies_bouldin']:.4f}, "
			f"noise_points={best_dbscan['noise_points']}"
		)
	else:
		print("Best DBSCAN -> no valid configuration found with >=2 non-noise clusters.")
		print(
			"DBSCAN search grid tried: "
			f"eps={dbscan_eval['eps_grid']}, min_samples={dbscan_eval['min_samples_grid']}"
		)

	print(
		f"Selected model: {final_result['algorithm']} with params {final_result['params']} "
		f"(silhouette={final_result['silhouette']:.4f})"
	)

	final_labels = final_result["labels"]
	output_df = raw_df.copy()
	output_df["cluster_label"] = final_labels

	cluster_counts = output_df["cluster_label"].value_counts(dropna=False).sort_index()
	print("\nCluster counts:")
	print(cluster_counts.to_string())

	scaled_df = pd.DataFrame(X_scaled, columns=feature_columns)
	profiles = cluster_profile_summary(scaled_df, final_labels)

	print("\nTop distinguishing z-scored features per cluster:")
	for cluster_id in profiles.index:
		top_features = profiles.loc[cluster_id].abs().sort_values(ascending=False).head(8).index
		print(f"\nCluster {cluster_id}:")
		print(profiles.loc[cluster_id, top_features].sort_values(key=np.abs, ascending=False).to_string())

	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	labeled_output_path = OUTPUT_DIR / "clustered_team_tiers.csv"
	profile_output_path = OUTPUT_DIR / "cluster_profiles_zscore_means.csv"
	cluster_plot_path = OUTPUT_DIR / "cluster_scatter_pca.png"
	method_plot_path = OUTPUT_DIR / f"cluster_scatter_pca_{final_result['algorithm']}.png"
	dbscan_results_path = OUTPUT_DIR / "dbscan_candidate_results.csv"
	output_df.to_csv(labeled_output_path, index=False)
	profiles.to_csv(profile_output_path)

	if dbscan_eval["all_results"]:
		dbscan_rows = []
		for row in dbscan_eval["all_results"]:
			dbscan_rows.append(
				{
					"eps": row["params"]["eps"],
					"min_samples": row["params"]["min_samples"],
					"n_clusters": row["n_clusters"],
					"noise_points": row["noise_points"],
					"silhouette": row["silhouette"],
					"davies_bouldin": row["davies_bouldin"],
				}
			)
		pd.DataFrame(dbscan_rows).sort_values("silhouette", ascending=False).to_csv(
			dbscan_results_path,
			index=False,
		)
	plotted = save_cluster_scatter_plot(
		X_scaled,
		final_labels,
		raw_df,
		target_column,
		cluster_plot_path,
		show_plot=show_plots,
	)

	print("\nSaved outputs:")
	print(f"- {labeled_output_path}")
	print(f"- {profile_output_path}")
	if dbscan_eval["all_results"]:
		print(f"- {dbscan_results_path}")
	if plotted:
		print(f"- {cluster_plot_path}")
		if method_plot_path != cluster_plot_path:
			shutil.copyfile(cluster_plot_path, method_plot_path)
			print(f"- {method_plot_path}")

	if show_plots:
		maybe_plot_kmeans_diagnostics(kmeans_eval["all_results"])


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Explore team tiers via clustering models.")
	parser.add_argument(
		"--csv-path",
		type=Path,
		default=DEFAULT_DATA_PATH,
		help="Path to the team stats CSV.",
	)
	parser.add_argument(
		"--target-column",
		type=str,
		default=DEFAULT_TARGET_COLUMN,
		help="Target column to exclude from clustering.",
	)
	parser.add_argument(
		"--no-plots",
		action="store_true",
		help="Disable matplotlib diagnostics plots.",
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	run_clustering(args.csv_path, args.target_column, show_plots=not args.no_plots)
