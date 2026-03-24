$token = "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"
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

# Create repository
$repoData = @{
    name = "equipment-query"
    description = "设备运维查询系统"
    private = $false
    auto_init = $true
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $repoData
Write-Host "Repository created:" $response.full_name
Write-Host "Repo URL:" $response.html_url
