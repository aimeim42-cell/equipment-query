$headers = @{"Authorization" = "token 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"}
$user = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
Write-Host "User:" $user.login
Write-Host "Token scopes:" $user.Scopes
