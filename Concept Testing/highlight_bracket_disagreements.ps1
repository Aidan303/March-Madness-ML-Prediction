$path = '2026_Production_Model_Comparison.md'
$lines = Get-Content $path
$out = New-Object System.Collections.Generic.List[string]

$inBracketSection = $false

function HighlightSingle([string]$text) {
    return '<span style="background-color:#b91c1c;color:#ffffff;padding:0 4px;border-radius:2px;font-weight:700;">' + $text + '</span>'
}

function HighlightAll([string]$text) {
    return '<span style="background-color:#92400e;color:#ffffff;padding:0 4px;border-radius:2px;font-weight:700;">' + $text + '</span>'
}

function StripHighlight([string]$text) {
    $clean = $text -replace '<span style="background-color:#b91c1c;color:#ffffff;padding:0 4px;border-radius:2px;font-weight:700;">(.*?)</span>', '$1'
    $clean = $clean -replace '<span style="background-color:#92400e;color:#ffffff;padding:0 4px;border-radius:2px;font-weight:700;">(.*?)</span>', '$1'
    return $clean
}

foreach ($line in $lines) {
    if ($line.StartsWith('| Slot | Round | Matchup |')) {
        $inBracketSection = $true
        $out.Add($line)
        continue
    }

    if ($inBracketSection -and $line.StartsWith('## Bracket Differences')) {
        $inBracketSection = $false
        $out.Add($line)
        continue
    }

    if ($inBracketSection -and $line -match '^\|\s*R\d') {
        $parts = $line -split '\|'
        $cells = @()
        for ($i = 1; $i -lt ($parts.Length - 1); $i++) {
            $cells += $parts[$i].Trim()
        }

        if ($cells.Count -ge 13) {
            # Normalize any existing highlights so reruns are idempotent.
            $cells[2] = StripHighlight $cells[2]
            $cells[3] = StripHighlight $cells[3]
            $cells[4] = StripHighlight $cells[4]
            $cells[5] = StripHighlight $cells[5]
            $cells[8] = StripHighlight $cells[8]
            $cells[11] = StripHighlight $cells[11]

            # Matchup discrepancy highlighting (only when all three matchup columns are populated).
            $mu = $cells[2]
            $mo = $cells[3]
            $mw = $cells[4]

            if (($mu -ne '') -and ($mo -ne '') -and ($mw -ne '')) {
                if (($mu -eq $mo) -and ($mo -ne $mw)) {
                    $cells[4] = HighlightSingle $mw
                } elseif (($mu -eq $mw) -and ($mu -ne $mo)) {
                    $cells[3] = HighlightSingle $mo
                } elseif (($mo -eq $mw) -and ($mu -ne $mo)) {
                    $cells[2] = HighlightSingle $mu
                } elseif (($mu -ne $mo) -and ($mu -ne $mw) -and ($mo -ne $mw)) {
                    $cells[2] = HighlightAll $mu
                    $cells[3] = HighlightAll $mo
                    $cells[4] = HighlightAll $mw
                }
            }

            # Winner discrepancy highlighting.
            $u = $cells[5]
            $o = $cells[8]
            $w = $cells[11]

            if (($u -eq $o) -and ($o -ne $w)) {
                $cells[11] = HighlightSingle $w
            } elseif (($u -eq $w) -and ($u -ne $o)) {
                $cells[8] = HighlightSingle $o
            } elseif (($o -eq $w) -and ($u -ne $o)) {
                $cells[5] = HighlightSingle $u
            } elseif (($u -ne $o) -and ($u -ne $w) -and ($o -ne $w)) {
                $cells[5] = HighlightAll $u
                $cells[8] = HighlightAll $o
                $cells[11] = HighlightAll $w
            }
        }

        $out.Add('| ' + ($cells -join ' | ') + ' |')
        continue
    }

    $out.Add($line)
}

Set-Content -Path $path -Value $out -Encoding ascii
