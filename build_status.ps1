$token = "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"
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

# Get pages build status
$response = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/pages/builds/latest" -Method Get -Headers $headers
Write-Host "Status:" $response.status
Write-Host "Commit:" $response.commit
