$token = "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"
$headers = @{"Authorization" = "token $token"}

# Get current file SHA
$file = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Get -Headers $headers
Write-Host "Current SHA:" $file.sha

# Re-upload the file
$content = Get-Content "C:\Users\lenovo\.openclaw\workspace\admin_v2.html" -Raw -Encoding UTF8
$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
$base64 = [Convert]::ToBase64String($bytes)

$body = @{
    message = "Re-upload admin"
    content = $base64
    sha = $file.sha
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Put -Headers $headers -Body $body
Write-Host "Re-uploaded successfully!"
