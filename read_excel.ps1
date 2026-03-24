$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

try {
    $wb = $excel.Workbooks.Open("C:\Users\lenovo\Desktop\报修单(20260302171532).xlsx")
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
finally {
    $wb.Close($false)
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
}
