$token = "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"
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

$files = @{
    "admin.html" = "C:\Users\lenovo\.openclaw\workspace\admin.html"
    "repair.html" = "C:\Users\lenovo\.openclaw\workspace\repair.html"
    "query.html" = "C:\Users\lenovo\.openclaw\workspace\query.html"
}

$baseUrl = "https://api.github.com/repos/aimeim42-cell/equipment-query/contents"

foreach ($file in $files.GetEnumerator()) {
    $content = Get-Content $file.Value -Raw -Encoding UTF8
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
    $base64 = [Convert]::ToBase64String($bytes)
    
    $body = @{
        message = "Upload $file.Key"
        content = $base64
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/$($file.Key)" -Method Put -Headers $headers -Body $body
        Write-Host "Uploaded: $($file.Key)"
    } catch {
        Write-Host "Error uploading $($file.Key): $_"
    }
}
