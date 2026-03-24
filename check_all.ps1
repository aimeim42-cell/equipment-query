$urls = @(
    "https://aimeim42-cell.github.io/equipment-query/admin.html",
    "https://aimeim42-cell.github.io/equipment-query/repair.html",
    "https://aimeim42-cell.github.io/equipment-query/query.html"
)

foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
        $filename = $url.Split('/')[-1]
        Write-Host "$filename - Status:" $response.StatusCode
    } catch {
        $filename = $url.Split('/')[-1]
        Write-Host "$filename - Error:" $_.Exception.Message
    }
}
