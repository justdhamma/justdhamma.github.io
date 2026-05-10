$dir = 'c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\nibbana-the-mind-stilled'
$files = Get-ChildItem -Path $dir -Filter '*-en.md'
# Match: [[N\]](https://seeingthroughthenet.net/.../Mind-Stilled_HTML.htm#_ednN)
# Replace with: [^N]
$pattern = '\[\[(\d+)\\\]\]\(https://seeingthroughthenet\.net/wp-content/uploads/2018/03/Mind-Stilled_HTML\.htm#_edn\d+\)'
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $newContent = $content -replace $pattern, '[^$1]'
    if ($content -ne $newContent) {
        [System.IO.File]::WriteAllText($file.FullName, $newContent)
        Write-Output ('Updated: ' + $file.Name)
    } else {
        Write-Output ('No changes: ' + $file.Name)
    }
}
