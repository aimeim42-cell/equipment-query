$ErrorActionPreference = 'SilentlyContinue'

# Collect installed apps from registry
$paths = @(
 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
 'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*'
)
$apps = Get-ItemProperty -Path $paths |
 Where-Object { $_.DisplayName -and ($_.SystemComponent -ne1) -and ($_.ReleaseType -ne 'Security Update') -and ($_.ParentKeyName -notmatch '^{') } |
 Select-Object DisplayName, DisplayVersion, Publisher, InstallLocation, UninstallString |
 Sort-Object DisplayName

# Save raw list
$apps | ConvertTo-Json -Depth5 | Set-Content -Encoding UTF8 'installed-apps.json'

# Heuristics for removable candidates (conservative; excludes Office/Chrome/OneDrive)
$candidates = @()
foreach ($a in $apps) {
 $name = [string]$a.DisplayName
 $pub = [string]$a.Publisher
 $n = $name.ToLowerInvariant()
 $p = $pub.ToLowerInvariant()

 # Exclusions (keep)
 if ($n -match 'microsoft office|microsoft365|office' -or
 $n -match 'google chrome' -or
 $n -match 'edge' -or
 $n -match 'onenote|outlook|teams|excel|word|powerpoint' -or
 $p -match '^microsoft' -or
 $p -match '^google') { continue }

 $reason = $null

 if ($n -match 'updater|auto.?update|update service|update manager|installer service|assistant|helper|toolbox|service hub|support assistant|oem|manager') {
 $reason = '第三方更新/助手/工具箱'
 }
 elseif ($n -match 'toolbar|plugin|extension pack' -or $p -match 'baidu|2345|hao123') {
 $reason = '工具条/插件类'
 }
 elseif ($n -match 'flash|silverlight|shockwave') {
 $reason = '过时组件（可卸载）'
 }
 elseif ($n -match 'java|jre|runtime environment' -and -not ($n -match 'jdk')) {
 $reason = '旧版 Java运行时（如无需要可卸载）'
 }
 elseif ($p -match 'lenovo|dell|hp|asus|acer' -and $n -match 'assistant|service|optimizer|hotkey|experience|cloud|toolbox') {
 $reason = 'OEM预装助手/服务，可酌情卸载'
 }
 elseif ($p -match '360|qihu|qq|tencent|kingsoft|baidu' -and $n -match 'security|safe|guard|管家|安全|杀毒') {
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

$candidates | ConvertTo-Json -Depth5 | Set-Content -Encoding UTF8 'uninstall-candidates.json'

# Short text summary
$summary = "Apps total: " + ($apps | Measure-Object).Count + ", candidates: " + ($candidates | Measure-Object).Count
$summary | Set-Content -Encoding UTF8 'uninstall-summary.txt'
