$token = "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"
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

# Read files and upload to repo
$files = @("运维管理系统.html", "报修入口.html", "工单查询.html")
$baseUrl = "https://api.github.com/repos/aimeim42-cell/equipment-query/contents"

foreach ($file in $files) {
    $content = Get-Content "C:\Users\lenovo\.openclaw\workspace\$file" -Raw -Encoding UTF8
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
    $base64 = [Convert]::ToBase64String($bytes)
    
    $body = @{
        message = "Upload $file"
        content = $base64
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/$file" -Method Put -Headers $headers -Body $body
    Write-Host "Uploaded: $($response.content.name)"
}
