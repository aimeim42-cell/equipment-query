$token = "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"
$headers = @{"Authorization" = "token $token"; "Accept" = "application/vnd.github.v3+json"}

# Check GitHub Pages status
try {
    $pages = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/pages" -Method Get -Headers $headers
    Write-Host "GitHub Pages Status:" $pages.status
    Write-Host "URL:" $pages.html_url
} catch {
    Write-Host "Pages check error:" $_.Exception.Message
}

# List files
$files = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents" -Method Get -Headers $headers
Write-Host "`nFiles in repo:"
foreach ($f in $files) { Write-Host " -" $f.name }
