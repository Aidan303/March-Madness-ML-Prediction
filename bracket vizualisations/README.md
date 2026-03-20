# Bracket Vizualisations

This folder contains bracket visualization scripts and generated PNG outputs.

## Purpose
Convert predicted bracket CSV outputs into reader-friendly visual bracket graphics.

## Region Layout Rules Implemented
- Four regions are mapped from slot IDs: `W`, `X`, `Y`, `Z`.
- Region trees preserve slot progression (`R1 -> R2 -> R3 -> R4`) with feeder matchups adjacent.
- Semifinal pairing is resolved from slot IDs (`R5..`) rather than hardcoding region pairs.
- Regions that feed the same semifinal are placed on the same vertical side (left or right):
  - Left side: Region W (top-left) and Region X (bottom-left) — games flow left → right
  - Right side: Region Z (top-right) and Region Y (bottom-right) — games flow right → left
- Left semifinal (W vs X) sits at x=19; right semifinal (Z vs Y) sits at x=27; championship centred between them at x=23.
- Seed ordering within each region (top to bottom): 1, 8, 5, 4, 6, 3, 7, 2.

## Script
- [build_bracket_visuals.py](build_bracket_visuals.py)

## Default Run (All Three Branches)
From project root:

```powershell
python "bracket vizualisations/build_bracket_visuals.py"
```

This generates:
- `bracket vizualisations/2026_bracket_updated_feature_list.png`
- `bracket vizualisations/2026_bracket_original.png`
- `bracket vizualisations/2026_bracket_weighted_points.png`

## Single-Input Run
```powershell
python "bracket vizualisations/build_bracket_visuals.py" --single-input "Model Creation/Results/Production/2026_bracket_predictions.csv" --single-output "bracket vizualisations/2026_bracket_custom.png" --title "2026 Bracket - Custom"
```

## Displayed Content Per Matchup Box
- Team A (with seed)
- Team B (with seed)
- Winner name
- Winner probability

Winner propagation is shown by placement in downstream slots.

## 2026 Generated Outputs
Generated 2026-03-18 from production inference CSVs:
- `2026_bracket_updated_feature_list.png` — Updated Feature List branch
- `2026_bracket_original.png` — Original branch
- `2026_bracket_weighted_points.png` — Weighted Points branch
