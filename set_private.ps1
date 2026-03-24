$body = @{
    private = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri 'https://api.github.com/repos/aimeim42-cell/equipment-query' -Method PATCH -Headers @{
    'Authorization' = 'token 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'
    'Content-Type' = 'application/json'
} -Body $body
