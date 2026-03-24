$ErrorActionPreference = 'SilentlyContinue'

# Collect installed apps from registry
$paths = @(
 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
 'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*'
)
$apps = Get-ItemProperty -Path $paths |
 Where-Object { $_.DisplayName -and ($_.SystemComponent -ne1) } |
 Select-Object DisplayName, DisplayVersion, Publisher, InstallLocation, UninstallString |
 Sort-Object DisplayName

# Save full list
$apps | ConvertTo-Json -Depth4 | Set-Content -Encoding UTF8 'installed-apps.json'

# Helper: safe lower
function ToLower($s) { if ([string]::IsNullOrWhiteSpace($s)) { return '' } else { return $s.ToString().ToLowerInvariant() } }

$candidates = @()
foreach ($a in $apps) {
 $name = ToLower $a.DisplayName
 $pub = ToLower $a.Publisher
 if ([string]::IsNullOrWhiteSpace($name)) { continue }

 # Exclusions to KEEP
 if ($name.Contains('google chrome') -or $name.Contains('microsoft office') -or $name.Contains('microsoft365') -or $name.Contains('onenote') -or $name.Contains('outlook') -or $name.Contains('teams') -or $name.Contains('excel') -or $name.Contains('word') -or $name.Contains('powerpoint')) { continue }
 if ($pub.StartsWith('microsoft') -or $pub.StartsWith('google')) { continue }

 $reason = $null
 if ($name.Contains('updater') -or $name.Contains('auto update') -or $name.Contains('update service') -or $name.Contains('assistant') -or $name.Contains('helper') -or $name.Contains('toolbox') -or $name.Contains('service hub') -or $name.Contains('support assistant') -or $name.Contains('manager')) {
 $reason = '第三方更新/助手/工具箱'
 } elseif ($name.Contains('toolbar') -or $name.Contains('plugin') -or $name.Contains('extension')) {
 $reason = '工具条/插件类'
 } elseif ($name.Contains('flash') -or $name.Contains('silverlight') -or $name.Contains('shockwave')) {
 $reason = '过时组件（可卸载）'
 } elseif ($name.Contains('java') -and -not $name.Contains('jdk')) {
 $reason = '旧版 Java运行时（如无需要可卸载）'
 } elseif (($pub.Contains('lenovo') -or $pub.Contains('dell') -or $pub.Contains('hp') -or $pub.Contains('asus') -or $pub.Contains('acer')) -and ($name.Contains('assistant') -or $name.Contains('service') -or $name.Contains('optimizer') -or $name.Contains('hotkey') -or $name.Contains('experience') -or $name.Contains('cloud') -or $name.Contains('toolbox'))) {
 $reason = 'OEM预装助手/服务（可酌情卸载）'
 } elseif (($pub.Contains('360') -or $pub.Contains('qihu') -or $pub.Contains('tencent') -or $pub.Contains('kingsoft') -or $pub.Contains('baidu')) -and ($name.Contains('security') -or $name.Contains('safe') -or $name.Contains('guard') -or $name.Contains('管家') -or $name.Contains('安全') -or $name.Contains('杀毒'))) {
 $reason = '第三方安全/管家（可能与系统安全重复）'
 }
 if ($reason) {
 $obj = [ordered]@{
 DisplayName = $a.DisplayName
 DisplayVersion = $a.DisplayVersion
 Publisher = $a.Publisher
 Reason = $reason
 UninstallString = $a.UninstallString
 }
 $candidates += (New-Object psobject -Property $obj)
 }
}

$candidates | ConvertTo-Json -Depth4 | Set-Content -Encoding UTF8 'uninstall-candidates.json'

# summary
("Apps total: " + ($apps | Measure-Object).Count + ", candidates: " + ($candidates | Measure-Object).Count) | Set-Content -Encoding UTF8 'uninstall-summary.txt'
