$path = '2026_Production_Model_Comparison.md'
$lines = Get-Content $path

$origCsv = Import-Csv 'Model Creation\Results\Production\2026_bracket_predictions.csv'
$weightedCsv = Import-Csv 'Model Creation Weighted Points\Results\Production\2026_bracket_predictions_weighted_points.csv'

$lateRoundSlots = @('R4W1','R4X1','R4Y1','R4Z1','R5WX','R5YZ','R6CH')
$origMatchupBySlot = @{}
$weightedMatchupBySlot = @{}

foreach ($s in $lateRoundSlots) {
    $or = $origCsv | Where-Object { $_.Slot -eq $s }
    $wr = $weightedCsv | Where-Object { $_.Slot -eq $s }
    if ($or) { $origMatchupBySlot[$s] = "$($or.TeamA_name) vs $($or.TeamB_name)" }
    if ($wr) { $weightedMatchupBySlot[$s] = "$($wr.TeamA_name) vs $($wr.TeamB_name)" }
}

$out = New-Object System.Collections.Generic.List[string]
$inBracketTable = $false

foreach ($line in $lines) {
    if ($line.StartsWith('| Slot | Round | Matchup |')) {
        $inBracketTable = $true
        $out.Add('| Slot | Round | Matchup | Original Matchup (R4-R6) | Weighted Matchup (R4-R6) | <span style="background-color:#0b6bcb;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Updated Winner</span> | <span style="background-color:#0b6bcb;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Updated Win Prob</span> |  | <span style="background-color:#1f2937;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Original Winner</span> | <span style="background-color:#1f2937;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Original Win Prob</span> |  | <span style="background-color:#b45309;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Weighted Winner</span> | <span style="background-color:#b45309;color:#ffffff;padding:2px 8px;border-radius:0;font-weight:700;display:inline-block;">Weighted Win Prob</span> |')
        continue
    }

    if ($inBracketTable -and $line -eq '|---|---:|---|---|---:|:---:|---|---:|:---:|---|---:|') {
        $out.Add('|---|---:|---|---|---|---|---:|:---:|---|---:|:---:|---|---:|')
        continue
    }

    if ($inBracketTable -and $line.StartsWith('## Bracket Differences')) {
        $inBracketTable = $false
        $out.Add($line)
        continue
    }

    if ($inBracketTable -and $line -match '^\|\s*R\d') {
        $parts = $line -split '\|'
        $cells = @()
        for ($i = 1; $i -lt ($parts.Length - 1); $i++) {
            $cells += $parts[$i].Trim()
        }

        if ($cells.Count -eq 11) {
            $slot = $cells[0]
            $origMatch = ''
            $weightMatch = ''
            if ($origMatchupBySlot.ContainsKey($slot)) { $origMatch = $origMatchupBySlot[$slot] }
            if ($weightedMatchupBySlot.ContainsKey($slot)) { $weightMatch = $weightedMatchupBySlot[$slot] }

            $newCells = @(
                $cells[0], $cells[1], $cells[2],
                $origMatch, $weightMatch,
                $cells[3], $cells[4], $cells[5], $cells[6], $cells[7], $cells[8], $cells[9], $cells[10]
            )
            $out.Add('| ' + ($newCells -join ' | ') + ' |')
            continue
        }
    }

    $out.Add($line)
}

Set-Content -Path $path -Value $out -Encoding ascii
