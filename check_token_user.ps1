$headers = @{"Authorization" = "token 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"}
$user = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
Write-Host "Token user:" $user.login

# 检查这个用户创建的gists
$gists = Invoke-RestMethod -Uri "https://api.github.com/gists" -Headers $headers
Write-Host "User gists count:" $gists.Count
