$t = "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"
$h = @{"Authorization" = "token $t"}

# Test token
try {
    $user = Invoke-RestMethod -Uri "https://api.github.com/user" -Method Get -Headers $h
    Write-Host "Token valid for user:" $user.login
} catch {
    Write-Host "Token error:" $_.Exception.Message
}

# Get file SHA
$f = Invoke-RestMethod -Uri "https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html" -Method Get -Headers $h
Write-Host "File SHA:" $f.sha
