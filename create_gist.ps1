$headers = @{"Authorization" = "token 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"; "Content-Type" = "application/json"}
$body = @{
    description = "工单数据备份"
    public = $false
    files = @{
        "workorders.json" = @{content = '{"workorders":[],"updateTime":"2026-03-23"}'}
    }
} | ConvertTo-Json -Depth 3

try {
    $r = Invoke-RestMethod -Uri "https://api.github.com/gists" -Method POST -Headers $headers -Body $body
    Write-Host "SUCCESS! Gist created"
    Write-Host "Gist ID:" $r.id
    Write-Host "URL:" $r.html_url
} catch {
    Write-Host "Error:" $_.Exception.Message
    $err = $_.Exception.Response
    if($err) {
        $stream = $err.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $reader.BaseStream.Position = 0
        Write-Host "Response:" $reader.ReadToEnd()
    }
}
