$headers = @{"Authorization" = "token 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"}
# 尝试直接访问
try {
    $r = Invoke-WebRequest -Uri "https://api.github.com/user" -Headers $headers
    Write-Host "Status:" $r.StatusCode
    Write-Host "Content:" $r.Content
} catch {
    Write-Host "Error:" $_.Exception.Message
}
