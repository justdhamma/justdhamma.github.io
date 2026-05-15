$transcriptDir = "_transcripts"
$converted = 0

Get-ChildItem -Path $transcriptDir -Filter "*.md" -Recurse | ForEach-Object {
    $filepath = $_.FullName
    $content = Get-Content -Path $filepath -Encoding UTF8 -Raw
    
    if (-not $content.StartsWith("---")) {
        return
    }
    
    $parts = $content -split "^---`n|`n---`n", 3
    if ($parts.Count -lt 3) {
        return
    }
    
    $frontMatter = $parts[1]
    $newFrontMatter = $frontMatter -replace "episode:\s*['\`"](\d+)['\`"]", "episode: `$1"
    
    if ($newFrontMatter -ne $frontMatter) {
        $newContent = "---`n$newFrontMatter`n---`n$($parts[2])"
        Set-Content -Path $filepath -Value $newContent -Encoding UTF8
        $converted++
        Write-Host "Updated: $filepath"
    }
}

Write-Host "`nResult: $converted files converted"
Write-Host "All episodes are now integers!"
