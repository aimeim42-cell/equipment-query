$headers = @{"Authorization" = "token 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"; "Content-Type" = "application/json"}
$body = @{
    description = "test"
    public = $false
    files = @{
        "workorders.json" = @{content = '{"workorders":[]}'}
    }
} | ConvertTo-Json

try {
    $r = Invoke-RestMethod -Uri "https://api.github.com/gists/0a760e133e65feba23cd29b5f22805cd" -Method PATCH -Headers $headers -Body $body
    Write-Host "Success! Updated gist"
} catch {
    Write-Host "Error:" $_.Exception.Message
}
