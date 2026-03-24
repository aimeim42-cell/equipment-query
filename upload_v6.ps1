$token = "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"
$h = @{"Authorization" = "token $token"}

$f = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Get -Headers $h

$c = Get-Content "C:\Users\lenovo\.openclaw\workspace\admin_v6.html" -Raw -Encoding UTF8
$b = [System.Text.Encoding]::UTF8.GetBytes($c)
$base = [Convert]::ToBase64String($b)

$body = @{
    message = "Update v6"
    content = $base
    sha = $f.sha
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Put -Headers $h -Body $body
Write-Host "Done"
