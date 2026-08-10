# 启动 AI 流量抓包代理 (mitmproxy), 与 v2rayN/Clash 类 VPN 共存
#
# 网络拓扑:
#   AI 域名:   浏览器 -> PAC -> mitmproxy(8080, 抓包) -> v2rayN(10809, 翻墙) -> ChatGPT/Grok
#   其他流量:  浏览器 -> PAC -> v2rayN(10809) -> v2rayN 规则分流(国内直连/国外翻墙)
#
# 前提: v2rayN 已开启本地 HTTP 端口(默认 10809) —— 参数设置 -> 本地监听端口 -> 勾选 Http
# 顺序: 先开 v2rayN, 再运行本脚本(脚本会覆盖系统代理为 PAC, 指向 v2rayN 与 mitmproxy)
#
# 用法:
#   1. 确保 v2rayN 运行且 Http 端口(10809)已开启
#   2. 首次运行前: 用管理员 PowerShell 执行 scripts\install-cert.ps1 安装 CA 证书
#   3. 运行:  .\scripts\run-capture.ps1
#      端口不同时:  .\scripts\run-capture.ps1 -ProxyPort 7890  (Clash)
#   4. 结束: 按 Ctrl+C 退出, 自动还原系统代理
# 数据写入 .capture\capture.db (已 gitignore, 不进 git)

param(
    [int]$ProxyPort = 10809  # v2rayN 本地 HTTP 端口 / Clash 混合端口
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$addon = Join-Path $scriptDir "capture\addon.py"
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings"

if (-not (Get-Command mitmdump -ErrorAction SilentlyContinue)) {
    Write-Host "[!] 未找到 mitmdump, 请先执行: pip install mitmproxy" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "$env:USERPROFILE\.mitmproxy\mitmproxy-ca-cert.cer")) {
    Write-Host "[!] 尚未生成 CA 证书。首次启动会生成, 之后请用管理员运行 scripts\install-cert.ps1 安装。" -ForegroundColor Yellow
}

# ---- 检查 v2rayN http 端口是否可用 ----
$vpnUp = Get-NetTCPConnection -LocalPort $ProxyPort -State Listen -ErrorAction SilentlyContinue
if (-not $vpnUp) {
    Write-Host "[!] 未检测到 $ProxyPort 端口监听! 请确认 v2rayN 已开启 HTTP 端口:" -ForegroundColor Red
    Write-Host "    v2rayN -> 参数设置 -> 本地监听端口 -> 勾选 Http (默认 10809) -> 重启 v2rayN" -ForegroundColor Red
    exit 1
}

# ---- 生成 PAC 文件并托管到本地 HTTP (file:// PAC 在 Windows 上常加载失败) ----
$captureDir = Join-Path $scriptDir ".capture"
New-Item -ItemType Directory -Path $captureDir -Force | Out-Null
$pacFile = Join-Path $captureDir "ai-proxy.pac"
$pacContent = @"
function FindProxyForURL(url, host) {
    // 本地/内网地址一律直连, 防止回环
    if (isPlainHostName(host) || host === "127.0.0.1" || host === "localhost"
        || shExpMatch(host, "127.*") || shExpMatch(host, "10.*")
        || shExpMatch(host, "192.168.*") || shExpMatch(host, "172.1[6-9].*")
        || shExpMatch(host, "172.2[0-9].*") || shExpMatch(host, "172.3[0-1].*")) {
        return "DIRECT";
    }
    var AI_DOMAINS = [
        "deepseek.com", "chatgpt.com", "openai.com",
        "grok.com", "x.ai"
    ];
    var h = host.toLowerCase();
    for (var i = 0; i < AI_DOMAINS.length; i++) {
        var d = AI_DOMAINS[i];
        if (h === d || h.endsWith("." + d)) {
            return "PROXY 127.0.0.1:8080";
        }
    }
    return "PROXY 127.0.0.1:$ProxyPort"; // 其他流量走 v2rayN, 由其规则分流
}
"@
Set-Content -Path $pacFile -Value $pacContent -Encoding UTF8

# 用 python http.server 托管 PAC(端口 18080), 退出时自动清理
$pacServer = Start-Process python -ArgumentList "-m", "http.server", "18080", "--bind", "127.0.0.1", "--directory", $captureDir -WindowStyle Hidden -PassThru
Start-Sleep -Milliseconds 800
$pacUrl = "http://127.0.0.1:18080/ai-proxy.pac"

# ---- 开启 PAC 系统代理 ----
try {
    Set-ItemProperty -Path $regPath -Name AutoConfigURL -Value $pacUrl
    Set-ItemProperty -Path $regPath -Name ProxyEnable -Value 1
    Remove-ItemProperty -Path $regPath -Name ProxyServer -ErrorAction SilentlyContinue
    Write-Host "[*] 已启用 PAC 分流: $pacUrl" -ForegroundColor Green
    Write-Host "[*] AI -> mitmproxy:8080 -> v2rayN:$ProxyPort, 其他 -> v2rayN:$ProxyPort" -ForegroundColor Green
} catch {
    Stop-Process -Id $pacServer.Id -Force -ErrorAction SilentlyContinue
    Write-Host "[!] 设置 PAC 失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

$upstream = "upstream:http://127.0.0.1:$ProxyPort"
Write-Host "[*] 启动抓包代理: 127.0.0.1:8080 (上游 $upstream, 按 Ctrl+C 退出自动还原)" -ForegroundColor Green

try {
    & mitmdump --mode $upstream -s $addon -p 8080 --set console_eventlog_verbosity=info
} finally {
    # ---- 退出后还原系统代理设置并停掉 PAC 托管服务 ----
    Stop-Process -Id $pacServer.Id -Force -ErrorAction SilentlyContinue
    try {
        Remove-ItemProperty -Path $regPath -Name AutoConfigURL -ErrorAction SilentlyContinue
        Set-ItemProperty -Path $regPath -Name ProxyEnable -Value 0
        Write-Host "`n[*] 已还原系统代理设置 (PAC 已清除, 代理已关闭)" -ForegroundColor Green
    } catch {
        Write-Host "[!] 还原代理设置失败: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}
