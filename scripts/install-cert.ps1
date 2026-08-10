# 安装 mitmproxy CA 证书到当前用户受信任根 (需管理员运行)
# 用法: 以管理员身份执行  powershell -ExecutionPolicy Bypass -File scripts\install-cert.ps1
# 之后浏览器/客户端即可解密 HTTPS 流量

$ErrorActionPreference = "Stop"

$certPath = Join-Path $env:USERPROFILE ".mitmproxy\mitmproxy-ca-cert.cer"
if (-not (Test-Path $certPath)) {
    Write-Host "[!] 证书不存在: $certPath" -ForegroundColor Red
    Write-Host "[!] 请先运行 scripts\run-capture.ps1 让 mitmproxy 生成证书, 再回来装。" -ForegroundColor Red
    exit 1
}

$store = New-Object System.Security.Cryptography.X509Certificates.X509Store(
    "Root", "CurrentUser")
$store.Open("ReadWrite")

$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($certPath)
$store.Add($cert)
$store.Close()

Write-Host "[*] 证书已安装到 当前用户/受信任的根证书颁发机构: $certPath" -ForegroundColor Green
Write-Host "[*] 关闭代理后记得通过 设置->证书 或 certmgr.msc 删除该证书以恢复干净环境。" -ForegroundColor Yellow
