$token = "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"
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

# Check GitHub Pages status
$pages = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/pages" -Method Get -Headers $headers
Write-Host "GitHub Pages URL:" $pages.html_url
Write-Host "Pages Status:" $pages.status

# List files in repo
$files = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents" -Method Get -Headers $headers
Write-Host "`nFiles in repo:"
foreach ($f in $files) {
    Write-Host " -" $f.name
}
