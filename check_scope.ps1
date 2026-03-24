$headers = @{"Authorization" = "token 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"}
$user = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
Write-Host "User:" $user.login
Write-Host "Token scopes:" $user.Scopes
