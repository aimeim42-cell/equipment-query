$content = [System.IO.File]::ReadAllText("C:\Users\lenovo\.openclaw\workspace\admin_v17.html", [System.Text.Encoding]::UTF8)
Write-Host "File length: $($content.Length)"

Write-Host "`n=== Checking key functions ==="
$functions = @('renderDashboard', 'showPage', 'renderVendors', 'getCurrentUser', 'getAccounts', 'getGistId', 'saveGistId', 'renderDashboard', 'uploadToCloud', 'syncFromCloud')
foreach ($fn in $functions) {
    $idx = $content.IndexOf("function $fn")
    Write-Host "$fn : $(if($idx -ge 0){'FOUND at '+$idx}else{'MISSING'})"
}

Write-Host "`n=== Checking for '待分配' ==="
$idx = $content.IndexOf('待分配')
Write-Host "待分配 found at: $idx"

Write-Host "`n=== Checking upload button near sync ==="
$idx = $content.IndexOf('syncFromCloud')
if ($idx -gt 0) {
    Write-Host "syncFromCloud found at: $idx"
    Write-Host "Context: $($content.Substring([Math]::Max(0,$idx-300), 500))"
}

Write-Host "`n=== Last 100 chars ==="
Write-Host $content.Substring([Math]::Max(0, $content.Length - 100))
