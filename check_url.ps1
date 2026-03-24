$url = "https://aimeim42-cell.github.io/equipment-query/admin.html"
try {
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
    Write-Host "Status:" $response.StatusCode
    Write-Host "Content length:" $response.Content.Length
} catch {
    Write-Host "Error:" $_.Exception.Message
}
