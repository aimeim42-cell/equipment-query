$headers = @{"Authorization" = "token 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"; "Content-Type" = "application/json"}
$body = @{
    description = "工单数据备份"
    public = $false
    files = @{
        "workorders.json" = @{content = '{"workorders":[],"updateTime":"2026-03-23"}'}
    }
} | ConvertTo-Json -Depth 3

$r = Invoke-RestMethod -Uri "https://api.github.com/gists" -Method POST -Headers $headers -Body $body
Write-Host "Gist ID:" $r.id
Write-Host "URL:" $r.html_url
