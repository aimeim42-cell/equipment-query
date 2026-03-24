$token = "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"
$headers = @{"Authorization" = "token $token"}
$f = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Headers $headers
$c = Get-Content "C:\Users\lenovo\.openclaw\workspace\admin_new.html" -Raw -Encoding UTF8
$b = [Text.Encoding]::UTF8.GetBytes($c)
$base = [Convert]::ToBase64String($b)
$body = @{message="v16 fresh";content=$base;sha=$f.sha} | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Put -Headers $headers -Body $body
Write-Host "Done"
