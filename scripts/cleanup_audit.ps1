$ErrorActionPreference = 'SilentlyContinue'

function SizeMB($p) {
 if (Test-Path -LiteralPath $p) {
 $sum = (Get-ChildItem -LiteralPath $p -Force -Recurse -ErrorAction SilentlyContinue |
 Where-Object { -not $_.PSIsContainer } |
 Measure-Object -Property Length -Sum).Sum
 if ($sum) { return [math]::Round(($sum /1MB),2) } else { return0 }
 } else { return0 }
}

function Safe-ClearFolder($p) {
 if (Test-Path -LiteralPath $p) {
 Get-ChildItem -LiteralPath $p -Force -Recurse -ErrorAction SilentlyContinue |
 Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
 }
}

$targets = [ordered]@{}
$targets.UserTemp = $env:TEMP
$targets.LocalAppDataTemp = Join-Path $env:LOCALAPPDATA 'Temp'
$targets.NpmCache = Join-Path $env:APPDATA 'npm-cache'
$targets.EdgeCache = Join-Path $env:LOCALAPPDATA 'Microsoft/Edge/User Data/Default/Cache'
$targets.ChromeCache = Join-Path $env:LOCALAPPDATA 'Google/Chrome/User Data/Default/Cache'
$targets.WindowsTemp = 'C:/Windows/Temp'
$targets.WinUpdate = 'C:/Windows/SoftwareDistribution/Download'

$before = @{}
foreach ($k in $targets.Keys) { $before[$k] = SizeMB $targets[$k] }
$freeBeforeGB = ((Get-PSDrive -Name C).Free /1GB)

# Recycle bin
try { Clear-RecycleBin -Force -ErrorAction SilentlyContinue } catch {}

# Clear folders (no services stop; best-effort user-level)
foreach ($k in $targets.Keys) { Safe-ClearFolder $targets[$k] }

Start-Sleep -Milliseconds300

$after = @{}
foreach ($k in $targets.Keys) { $after[$k] = SizeMB $targets[$k] }
$freeAfterGB = ((Get-PSDrive -Name C).Free /1GB)

# Light audit
$paths = @(
 'HKLM:Software/Microsoft/Windows/CurrentVersion/Uninstall/*',
 'HKLM:Software/WOW6432Node/Microsoft/Windows/CurrentVersion/Uninstall/*',
 'HKCU:Software/Microsoft/Windows/CurrentVersion/Uninstall/*'
)
$apps = Get-ItemProperty $paths | Where-Object { $_.DisplayName } |
 Select-Object DisplayName, DisplayVersion, Publisher | Sort-Object DisplayName

$startup = Get-CimInstance Win32_StartupCommand |
 Select-Object Name, Command, Location, User

$services = Get-Service | Where-Object { $_.Status -eq 'Running' -or $_.StartType -in @('Automatic','AutomaticDelayedStart') } |
 Select-Object Name, DisplayName, StartType | Sort-Object DisplayName

# Build result
$result = [ordered]@{}
$beforeTotal = (($before.GetEnumerator() | ForEach-Object { $_.Value }) | Measure-Object -Sum).Sum
$afterTotal = (($after.GetEnumerator() | ForEach-Object { $_.Value }) | Measure-Object -Sum).Sum
$result.FreedMB = [math]::Round(($beforeTotal - $afterTotal),2)
$result.FreeSpaceGB_Before = [math]::Round($freeBeforeGB,2)
$result.FreeSpaceGB_After = [math]::Round($freeAfterGB,2)
$result.Details = @{}
foreach ($k in $targets.Keys) { $result.Details[$k] = @{ BeforeMB = [math]::Round($before[$k],2); AfterMB = [math]::Round($after[$k],2) } }
$result.AppCount = ($apps | Measure-Object).Count
$result.StartupCount = ($startup | Measure-Object).Count
$result.ServiceCount = ($services | Measure-Object).Count

$result | ConvertTo-Json -Depth6 | Set-Content -Encoding UTF8 'cleanup-report.json'
$apps | ConvertTo-Json -Depth6 | Set-Content -Encoding UTF8 'installed-apps.json'
$startup | ConvertTo-Json -Depth6 | Set-Content -Encoding UTF8 'startup-items.json'
$services | ConvertTo-Json -Depth6 | Set-Content -Encoding UTF8 'services-auto-running.json'
