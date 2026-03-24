$token = "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"
$headers = @{"Authorization" = "token $token"}
# Upload as backup file
$content = Get-Content "C:\Users\lenovo\.openclaw\workspace\admin_v16_backup.html" -Raw -Encoding UTF8
$bytes = [Text.Encoding]::UTF8.GetBytes($content)
$base64 = [Convert]::ToBase64String($bytes)
$body = @{message="Backup v16";content=$base64} | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin_v16_backup.html" -Method Put -Headers $headers -Body $body
Write-Host "Backup saved"
