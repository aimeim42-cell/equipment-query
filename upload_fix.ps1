$t = "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"
$h = @{"Authorization" = "token $t"}
$f = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Get -Headers $h
$c = Get-Content "C:\Users\lenovo\.openclaw\workspace\admin_final_v2.html" -Raw -Encoding UTF8
$b = [System.Text.Encoding]::UTF8.GetBytes($c)
$base = [Convert]::ToBase64String($b)
$body = @{message="Fix sync";content=$base;sha=$f.sha} | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Put -Headers $h -Body $body
Write-Host "Done"
