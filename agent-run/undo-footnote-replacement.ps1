$dir = 'c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\nibbana-the-mind-stilled'
$files = Get-ChildItem -Path $dir -Filter '*-en.md'
$utf8 = [System.Text.Encoding]::UTF8
$win1252 = [System.Text.Encoding]::GetEncoding(1252)
# Reverse the footnote replacement
$footnotePattern = '\[\^(\d+)\](?!\:)'
$footnoteReplace = '[[$1\]](https://seeingthroughthenet.net/wp-content/uploads/2018/03/Mind-Stilled_HTML.htm#_edn$1)'

foreach ($file in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    # Step 1: Read current file bytes as UTF-8 to get corrupted string
    $corrupted = $utf8.GetString($bytes)
    # Step 2: Re-encode the corrupted string to Windows-1252 bytes
    $originalBytes = $win1252.GetBytes($corrupted)
    # Step 3: Decode those bytes as UTF-8 to recover original text
    $recovered = $utf8.GetString($originalBytes)
    # Step 4: Reverse footnote replacement
    $final = $recovered -replace $footnotePattern, $footnoteReplace
    # Write back as UTF-8
    [System.IO.File]::WriteAllBytes($file.FullName, $utf8.GetBytes($final))
    Write-Output ('Undone: ' + $file.Name)
}
