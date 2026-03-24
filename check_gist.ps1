$headers = @{"Authorization" = "token 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"}
try {
    $r = Invoke-RestMethod -Uri "https://api.github.com/gists/0a760e133e65feba23cd29b5f22805cd" -Headers $headers
    Write-Host "Gist exists, files:" $r.files.PSObject.Properties.Name
} catch {
    Write-Host "Error:" $_.Exception.Message
}
