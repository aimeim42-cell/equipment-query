$token = "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"
$headers = @{"Authorization" = "token $token"}

# Check file status
$f = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Get -Headers $headers
Write-Host "File SHA:" $f.sha
Write-Host "Size:" $f.size "bytes"

# Check pages
$p = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/pages" -Method Get -Headers $headers
Write-Host "Pages Status:" $p.status

# List all files
$files = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents" -Method Get -Headers $headers
Write-Host "`nAll files:"
foreach ($file in $files) {
    Write-Host " -" $file.name "(" $file.size "bytes)"
}
