// AI 流量分流 PAC(配合 v2rayN/Clash 共存) —— 参考文件, 实际由 run-capture.ps1 动态生成
//   AI 服务域名   → mitmproxy(127.0.0.1:8080, 抓包记录) → 上游 v2rayN 翻墙
//   本地/内网地址 → DIRECT(防回环)
//   其他流量      → v2rayN 本地 HTTP 端口(默认 10809), 由其规则分流
function FindProxyForURL(url, host) {
    if (isPlainHostName(host) || host === "127.0.0.1" || host === "localhost"
        || shExpMatch(host, "127.*") || shExpMatch(host, "10.*")
        || shExpMatch(host, "192.168.*") || shExpMatch(host, "172.1[6-9].*")
        || shExpMatch(host, "172.2[0-9].*") || shExpMatch(host, "172.3[0-1].*")) {
        return "DIRECT";
    }
    var AI_DOMAINS = [
        "deepseek.com",
        "chatgpt.com",
        "openai.com",
        "grok.com",
        "x.ai"
    ];
    var h = host.toLowerCase();
    for (var i = 0; i < AI_DOMAINS.length; i++) {
        var d = AI_DOMAINS[i];
        if (h === d || h.endsWith("." + d)) {
            return "PROXY 127.0.0.1:8080";
        }
    }
    return "PROXY 127.0.0.1:10809"; // v2rayN 默认 http 端口; Clash 改 7890
}
