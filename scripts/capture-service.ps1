# AI 抓包服务脚本 —— 由 Windows 登录任务自动启动(开机即跑)
# 作用: 生成 PAC -> 起 PAC 托管(18081) -> 起 mitmdump(8080) -> 设置系统代理/环境变量
# 停止: 运行 scripts\stop-capture.ps1

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$addon = Join-Path $scriptDir "capture\addon.py"
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings"

# 已运行则退出
if (Get-Process mitmdump -ErrorAction SilentlyContinue) {
    Write-Host "[*] mitmdump 已在运行, 跳过"
    exit 0
}

# ---- 生成 DeepSeek 专用 PAC ----
$captureDir = Join-Path $scriptDir ".capture"
New-Item -ItemType Directory -Path $captureDir -Force | Out-Null
$pacFile = Join-Path $captureDir "ai-proxy-deepseek.pac"
$pacContent = @"
function FindProxyForURL(url, host) {
    if (isPlainHostName(host) || host === "127.0.0.1" || host === "localhost"
        || shExpMatch(host, "127.*") || shExpMatch(host, "10.*")
        || shExpMatch(host, "192.168.*") || shExpMatch(host, "172.1[6-9].*")
        || shExpMatch(host, "172.2[0-9].*") || shExpMatch(host, "172.3[0-1].*")) {
        return "DIRECT";
    }
    var h = host.toLowerCase();
    if (h === "deepseek.com" || h.endsWith(".deepseek.com")) {
        return "PROXY 127.0.0.1:8080";
    }
    return "DIRECT"; // 其他所有流量直连
}
"@
Set-Content -Path $pacFile -Value $pacContent -Encoding UTF8

# ---- 起 PAC 托管服务(18081)----
$pacServer = Start-Process python -ArgumentList "-m", "http.server", "18081", "--bind", "127.0.0.1", "--directory", $captureDir -WindowStyle Hidden -PassThru
$pacServer.Id | Out-File (Join-Path $captureDir "pac_server.pid") -Encoding ascii
Start-Sleep -Milliseconds 800

# ---- 设置系统代理(PAC)----
try {
    Set-ItemProperty -Path $regPath -Name AutoConfigURL -Value "http://127.0.0.1:18081/ai-proxy-deepseek.pac"
    Set-ItemProperty -Path $regPath -Name ProxyEnable -Value 1
    Remove-ItemProperty -Path $regPath -Name ProxyServer -ErrorAction SilentlyContinue
} catch {
    Write-Host "[!] 设置 PAC 失败: $($_.Exception.Message)" -ForegroundColor Red
}

# ---- 设置用户级代理环境变量(供 CLI/工具使用)----
[Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://127.0.0.1:8080", "User")
[Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://127.0.0.1:8080", "User")
[Environment]::SetEnvironmentVariable("NO_PROXY", "127.0.0.1,localhost", "User")

# ---- 启动 mitmdump(后台, 隐藏窗口)----
$mitmdump = (Get-Command mitmdump -ErrorAction SilentlyContinue).Source
if (-not $mitmdump) {
    $mitmdump = "$env:LOCALAPPDATA\Programs\Python\Python311\Scripts\mitmdump.exe"
}
$pidFile = Join-Path $captureDir "mitmdump.pid"
Start-Process $mitmdump -ArgumentList "-s", "`"$addon`"", "-p", "8080", "--set", "console_eventlog_verbosity=info" -WindowStyle Hidden -PassThru | ForEach-Object {
    $_.Id | Out-File $pidFile -Encoding ascii
}

Start-Sleep -Seconds 2
if (Get-Process mitmdump -ErrorAction SilentlyContinue) {
    Write-Host "[*] AI 抓包服务已启动: mitmdump(8080) + PAC(18081)"
} else {
    Write-Host "[!] mitmdump 启动失败" -ForegroundColor Red
}
