# 停止 AI 抓包服务并还原系统代理/环境变量
$ErrorActionPreference = "Continue"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$captureDir = Join-Path $scriptDir ".capture"
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings"

# 杀 mitmdump
Get-Process mitmdump -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "[*] mitmdump 已停止"

# 杀 PAC 托管服务
$pidFile = Join-Path $captureDir "pac_server.pid"
if (Test-Path $pidFile) {
    $pid = (Get-Content $pidFile).Trim()
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Remove-Item $pidFile -ErrorAction SilentlyContinue
    Write-Host "[*] PAC 托管已停止"
}
# 兜底: 杀 18081 监听
Get-NetTCPConnection -LocalPort 18081 -State Listen -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
# 兜底: 杀 8080 监听 (mitmdump 实际由 python.exe 承载, 只杀 shim 会遗留孤儿进程占端口)
Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

# 还原系统代理
Remove-ItemProperty -Path $regPath -Name AutoConfigURL -ErrorAction SilentlyContinue
Set-ItemProperty -Path $regPath -Name ProxyEnable -Value 0
Write-Host "[*] 系统代理已还原"

# 清除用户级环境变量
[Environment]::SetEnvironmentVariable("HTTP_PROXY", $null, "User")
[Environment]::SetEnvironmentVariable("HTTPS_PROXY", $null, "User")
[Environment]::SetEnvironmentVariable("NO_PROXY", $null, "User")
Write-Host "[*] 代理环境变量已清除"

Write-Host "[*] AI 抓包服务已停止"
