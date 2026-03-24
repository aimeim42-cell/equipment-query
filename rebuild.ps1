$token = "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"
$headers = @{"Authorization" = "token $token"}

# Trigger build
try {
    $body = @{source = @{branch = "main"; path = "/"}} | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/pages" -Method Post -Headers $headers -Body $body
    Write-Host "Build triggered"
} catch {
    Write-Host "Build trigger error:" $_.Exception.Message
}
