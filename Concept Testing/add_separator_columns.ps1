$path = '2026_Production_Model_Comparison.md'
$lines = Get-Content $path
$out = New-Object System.Collections.Generic.List[string]

foreach ($line in $lines) {
    if ($line.StartsWith('| TeamID | Team | Seed |')) {
        $out.Add('| TeamID | Team | Seed | <span style="background-color:#0b6bcb;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Updated p_champion</span> | <span style="background-color:#0b6bcb;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Updated Rank</span> |  | <span style="background-color:#1f2937;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Original p_champion</span> | <span style="background-color:#1f2937;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Original Rank</span> |  | <span style="background-color:#b45309;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Weighted p_champion</span> | <span style="background-color:#b45309;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Weighted Rank</span> |')
        continue
    }

    if ($line -eq '|---|---|---:|---:|---:|---:|---:|---:|---:|') {
        $out.Add('|---|---|---:|---:|---:|:---:|---:|---:|:---:|---:|---:|')
        continue
    }

    if ($line.StartsWith('| Slot | Round | Matchup |')) {
        $out.Add('| Slot | Round | Matchup | <span style="background-color:#0b6bcb;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Updated Winner</span> | <span style="background-color:#0b6bcb;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Updated Win Prob</span> |  | <span style="background-color:#1f2937;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Original Winner</span> | <span style="background-color:#1f2937;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Original Win Prob</span> |  | <span style="background-color:#b45309;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Weighted Winner</span> | <span style="background-color:#b45309;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Weighted Win Prob</span> |')
        continue
    }

    if ($line -eq '|---|---:|---|---|---:|---|---:|---|---:|') {
        $out.Add('|---|---:|---|---|---:|:---:|---|---:|:---:|---|---:|')
        continue
    }

    if ($line -match '^\|\s*\d+\s*\|') {
        $parts = $line -split '\|'
        $cells = @()
        for ($i = 1; $i -lt ($parts.Length - 1); $i++) {
            $cells += $parts[$i].Trim()
        }

        if ($cells.Count -eq 9) {
            $newCells = @($cells[0], $cells[1], $cells[2], $cells[3], $cells[4], '', $cells[5], $cells[6], '', $cells[7], $cells[8])
            $out.Add('| ' + ($newCells -join ' | ') + ' |')
            continue
        }
    }

    if ($line -match '^\|\s*R\d') {
        $parts = $line -split '\|'
        $cells = @()
        for ($i = 1; $i -lt ($parts.Length - 1); $i++) {
            $cells += $parts[$i].Trim()
        }

        if ($cells.Count -eq 9) {
            $newCells = @($cells[0], $cells[1], $cells[2], $cells[3], $cells[4], '', $cells[5], $cells[6], '', $cells[7], $cells[8])
            $out.Add('| ' + ($newCells -join ' | ') + ' |')
            continue
        }
    }

    $out.Add($line)
}

Set-Content -Path $path -Value $out -Encoding ascii
