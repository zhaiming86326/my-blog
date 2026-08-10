# 轻量抓包: 只记录 DeepSeek 流量(网页版 + API)
#
# 特点:
#   - 无需 v2rayN / VPN(DeepSeek 国内直连)
#   - PAC 只让 deepseek.com 走代理, 其他应用流量完全直连, 不受影响
#   - 退出(Ctrl+C)自动还原系统代理
#
# 用法:
#   1. 首次: 管理员运行 scripts\install-cert.ps1 装证书
#   2. .\scripts\run-deepseek.ps1
# 数据写入 .capture\capture.db (已 gitignore)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$addon = Join-Path $scriptDir "capture\addon.py"
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings"

if (-not (Get-Command mitmdump -ErrorAction SilentlyContinue)) {
    Write-Host "[!] 未找到 mitmdump, 请先执行: pip install mitmproxy" -ForegroundColor Red
    exit 1
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
    return "DIRECT"; // 其他所有流量直连, 不受影响
}
"@
Set-Content -Path $pacFile -Value $pacContent -Encoding UTF8

# 托管 PAC(端口 18081, file:// 在 Windows 上不可靠)
$pacServer = Start-Process python -ArgumentList "-m", "http.server", "18081", "--bind", "127.0.0.1", "--directory", $captureDir -WindowStyle Hidden -PassThru
Start-Sleep -Milliseconds 800
$pacUrl = "http://127.0.0.1:18081/ai-proxy-deepseek.pac"

try {
    Set-ItemProperty -Path $regPath -Name AutoConfigURL -Value $pacUrl
    Set-ItemProperty -Path $regPath -Name ProxyEnable -Value 1
    Remove-ItemProperty -Path $regPath -Name ProxyServer -ErrorAction SilentlyContinue
    Write-Host "[*] 已启用 DeepSeek 专用 PAC (仅 deepseek.com 走代理)" -ForegroundColor Green
} catch {
    Stop-Process -Id $pacServer.Id -Force -ErrorAction SilentlyContinue
    Write-Host "[!] 设置 PAC 失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# ---- 设置用户级代理环境变量 ----
# CLI/工具(Python requests / Node fetch / curl 等)不读 Windows 系统代理,
# 只认 HTTP_PROXY/HTTPS_PROXY。设为用户级变量, 新启动的工具进程自动继承。
[Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://127.0.0.1:8080", "User")
[Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://127.0.0.1:8080", "User")
[Environment]::SetEnvironmentVariable("NO_PROXY", "127.0.0.1,localhost", "User")
Write-Host "[*] 已设置 HTTP_PROXY/HTTPS_PROXY 环境变量 (新启动的工具将走代理)" -ForegroundColor Green
Write-Host "[*] 注意: 调用 DeepSeek 的工具需重新启动(从新终端/重新打开应用)才能生效" -ForegroundColor Yellow

Write-Host "[*] 启动抓包代理: 127.0.0.1:8080 (按 Ctrl+C 退出自动还原)" -ForegroundColor Green

try {
    & mitmdump -s $addon -p 8080 --set console_eventlog_verbosity=info
} finally {
    Stop-Process -Id $pacServer.Id -Force -ErrorAction SilentlyContinue
    # 清除用户级代理环境变量
    [Environment]::SetEnvironmentVariable("HTTP_PROXY", $null, "User")
    [Environment]::SetEnvironmentVariable("HTTPS_PROXY", $null, "User")
    [Environment]::SetEnvironmentVariable("NO_PROXY", $null, "User")
    try {
        Remove-ItemProperty -Path $regPath -Name AutoConfigURL -ErrorAction SilentlyContinue
        Set-ItemProperty -Path $regPath -Name ProxyEnable -Value 0
        Write-Host "`n[*] 已还原系统代理设置" -ForegroundColor Green
    } catch {
        Write-Host "[!] 还原代理设置失败: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}
