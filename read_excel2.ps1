$desktopPath = [Environment]::GetFolderPath("Desktop")
$files = Get-ChildItem -Path $desktopPath -Filter "报修*.xlsx" | Sort-Object LastWriteTime -Descending

foreach($f in $files) {
    Write-Host "Found: $($f.Name) - Size: $($f.Length) - Date: $($f.LastWriteTime)"
}

$latestFile = $files[0]
Write-Host "Using: $($latestFile.FullName)"

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

try {
    $wb = $excel.Workbooks.Open($latestFile.FullName)
    $ws = $wb.Sheets.Item(1)
    $usedRange = $ws.UsedRange
    $rows = $usedRange.Rows.Count
    $cols = $usedRange.Columns.Count
    
    Write-Host "TotalRows:$rows"
    Write-Host "TotalCols:$cols"
    
    for($i=1; $i -le [Math]::Min($rows, 100); $i++) {
        $row = ""
        for($j=1; $j -le $cols; $j++) {
            $cell = $ws.Cells.Item($i, $j).Text
            $row += $cell + "|"
        }
        Write-Host $row
    }
}
catch {
    Write-Host "Error: $_"
}
finally {
    if($wb) { $wb.Close($false) }
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
}
