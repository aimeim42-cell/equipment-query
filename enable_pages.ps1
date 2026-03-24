$token = "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"
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

# Enable GitHub Pages with correct syntax
$body = @{
    source = @{
        branch = "main"
        path = "/"
    }
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/pages" -Method Post -Headers $headers -Body $body
Write-Host "GitHub Pages enabled!"
Write-Host "URL:" $response.html_url
