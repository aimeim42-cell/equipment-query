$token = "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"
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

# Read the HTML file and convert to Base64
$content = Get-Content "C:\Users\lenovo\.openclaw\workspace\equipment-query.html" -Raw -Encoding UTF8
$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
$base64 = [Convert]::ToBase64String($bytes)

$body = @{
    message = "Upload equipment query page"
    content = $base64
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/index.html" -Method Put -Headers $headers -Body $body
Write-Host "File uploaded:" $response.content.name
Write-Host "Download URL:" $response.content.download_url
