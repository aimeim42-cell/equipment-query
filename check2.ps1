$token = "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"
$headers = @{"Authorization" = "token $token"}

try {
    $r = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query" -Method Get -Headers $headers
    Write-Host "Repository: OK"
    Write-Host "Name:" $r.name
    Write-Host "Updated:" $r.updated_at
} catch {
    Write-Host "Error:" $_.Exception.Message
}

# Check pages
try {
    $p = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/pages" -Method Get -Headers $headers
    Write-Host "Pages Status:" $p.status
} catch {
    Write-Host "Pages Error:" $_.Exception.Message
}
