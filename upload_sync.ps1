$t = "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"
$h = @{"Authorization" = "token $t"}
$f = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Get -Headers $h
$c = Get-Content "C:\Users\lenovo\.openclaw\workspace\admin_sync.html" -Raw -Encoding UTF8
$b = [System.Text.Encoding]::UTF8.GetBytes($c)
$base = [Convert]::ToBase64String($b)
$body = @{message="Sync v2";content=$base;sha=$f.sha} | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Put -Headers $h -Body $body
Write-Host "Done"
