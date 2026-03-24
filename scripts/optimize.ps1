$ErrorActionPreference = 'SilentlyContinue'

#1) Backup + disable risky HKCU Run entries (non-essential updaters/assistants)
$runKey = 'HKCU:Software\Microsoft\Windows\CurrentVersion\Run'
$backupKey = 'HKCU:Software\OpenClaw\DisabledRunBackup'
if (Test-Path $runKey) {
 if (-not (Test-Path $backupKey)) { New-Item -Path $backupKey -Force | Out-Null }
 $props = (Get-ItemProperty -Path $runKey) | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
 foreach ($name in $props) {
 $val = (Get-ItemProperty -Path $runKey -Name $name).$name
 if (-not [string]::IsNullOrWhiteSpace($val)) {
 $lower = $val.ToString().ToLowerInvariant()
 $nLower = $name.ToString().ToLowerInvariant()
 $isUpdater = ($lower -match 'update|updater|autoupdate|assistant|helper|agent') -or ($nLower -match 'update|updater|assistant|helper|agent')
 $isProtected = ($lower -match 'onedrive') -or ($nLower -match 'onedrive') -or ($lower -match 'ime|input') -or ($nLower -match 'ime|input') -or ($lower -match 'lenovo') -or ($nLower -match 'lenovo') -or ($lower -match 'google\\chrome')
 if ($isUpdater -and -not $isProtected) {
 # backup and remove
 New-ItemProperty -Path $backupKey -Name $name -Value $val -PropertyType String -Force | Out-Null
 Remove-ItemProperty -Path $runKey -Name $name -Force -ErrorAction SilentlyContinue
 }
 }
 }
}

#2) Disable common third-party updater scheduled tasks (safe subset)
$disableTasks = @(
 '\\Adobe Acrobat Update Task',
 '\\Adobe Flash Player Updater',
 '\\Java Update Scheduler',
 '\\Apple\\AppleSoftwareUpdate',
 '\\Microsoft\\Office\\Office Automatic Updates',
 '\\Microsoft\\Office\\OfficeTelemetryAgentFallBack' # telemetry-ish
)
foreach ($t in $disableTasks) {
 schtasks /Change /TN $t /DISABLE1>$null2>$null
}

# Do NOT touch Edge/Chrome/OneDrive updaters by default

#3) Enable Storage Sense (best-effort)
New-Item -Path 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense' -Force | Out-Null
New-Item -Path 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy' -Force | Out-Null
New-ItemProperty -Path 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense' -Name 'AllowStorageSenseGlobal' -PropertyType DWord -Value1 -Force | Out-Null
# StoragePolicy '01' => Enable Storage Sense, other keys can be tuned later
New-ItemProperty -Path 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy' -Name '01' -PropertyType DWord -Value1 -Force | Out-Null

#4) Visual effects: performance-friendly
New-Item -Path 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced' -Force | Out-Null
New-ItemProperty -Path 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced' -Name 'VisualFXSetting' -PropertyType DWord -Value2 -Force | Out-Null

#5) Light cache cleanup (again best-effort)
$targets = @(
 $env:TEMP,
 (Join-Path $env:LOCALAPPDATA 'Temp'),
 'C:/Windows/Temp'
)
foreach ($p in $targets) {
 if (Test-Path -LiteralPath $p) {
 Get-ChildItem -LiteralPath $p -Force -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
 }
}

# Write a small log
$log = @()
$log += "Disabled HKCU Run entries backed up under: $backupKey"
$log += "Disabled tasks (best-effort):"; $log += ($disableTasks -join ', ')
$log += "Storage Sense enabled (AllowStorageSenseGlobal=1, StoragePolicy01=1)"
$log += "VisualFXSetting set to2 (performance)"
$log -join [Environment]::NewLine | Set-Content -Encoding UTF8 'optimize-log.txt'
