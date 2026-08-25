---
title: "2026-08-25 AI 知识库日报"
date: 2026-08-25T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 27 条对话,提炼 27 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(27/27 条有效)。
> 信息来源分布:DeepSeek Harness(27条)

## 今日知识要点

### 如何配置 WireGuard 以实现内网流量不走代理

**核心结论**：
- 连上 v2rayN 后，内网流量（如局域网地址、路由器管理页面）会直接通过本地网卡，不走代理。
- 使用 v2rayN 的“绕过大陆”路由预设，可以实现内网流量直连，国外流量走隧道。

**关键要点**：
1. **配置 v2rayN 节点**：
   - 地址：VPS 公网 IP
   - 端口：51820
   - 本地IP：10.0.0.2/24
   - 私钥：VPS 上 `cat /etc/wireguard/client_private.key` 的内容
   - 公钥：VPS 上 `cat /etc/wireguard/server_public.key` 的内容
   - 允许的IP：0.0.0.0/0
   - 预共享密钥：留空
   - Reserved：0,0,0
   - MTU：1420

2. **验证内网流量直连**：
   - 打开 v2rayN，访问路由器管理页面（如 `http://192.168.1.1`）。
   - 查看 v2rayN 日志页，出现 `[socks -> direct]` 行，证明流量直连。

3. **注意事项**：
   - 不要将路由模式切换为“全局”，以免国外/国内流量都走代理。
   - 不要同时运行官方 WireGuard 客户端和 v2rayN，避免握手冲突。

**信息来源**：DeepSeek 网页

### WireGuard 部署与排查

**核心结论**：
- WireGuard 部署需要生成密钥对，并配置服务器和客户端。
- 排查问题时，需确认隧道握手成功、流量是否正常流动。

**关键要点**：
1. **生成密钥对**：
   - 服务器密钥生成：
     ```bash
     cd /etc/wireguard
     sudo umask 077
     sudo sh -c 'umask 077 && wg genkey | tee server_private.key | wg pubkey > server_public.key'
     ```
   - 客户端密钥生成：
     ```bash
     cd /etc/wireguard && sudo sh -c 'umask 077
     wg genkey > client_private.key && wg pubkey < client_private.key > client_public.key
     SERVER_PRIV=$(cat server_private.key)
     CLIENT_PUB=$(cat client_public.key)
     cat > wg0.conf <<EOF
     [Interface]
     Address = 10.0.0.1/24
     ListenPort = 51820
     PrivateKey = $SERVER_PRIV
     PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
     PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

     [Peer]
     PublicKey = $CLIENT_PUB
     AllowedIPs = 10.0.0.2/32
     EOF
     chmod 600 wg0.conf'
     ```

2. **排查问题**：
   - 确认服务器能否访问外部网络：
     ```bash
     curl -I --max-time 5 https://www.google.com
     echo "---"
     curl -I --max-time 5 https://www.baidu.com
     ```
   - 确认流量是否到达服务器：
     ```bash
     sudo wg show
     ```
   - 确认客户端能否访问外部网络：
     ```bash
     curl -I --max-time 5 https://www.google.com
     ```

3. **常见问题及解决方法**：
   - DNS 问题：
     - 修改客户端配置中的 DNS 服务器：
       ```ini
       DNS = 8.8.8.8, 223.5.5.5
       ```
   - MTU 问题：
     - 在客户端配置 `[Interface]` 下加一行：
       ```ini
       MTU = 1420
       ```

**信息来源**：DeepSeek 网页

### SSH 密钥登录配置与排查

- **核心结论**：SSH 密钥登录配置完成后，v2rayN 不需要额外修改配置，但需确保防火墙开放相应端口。
- **关键要点**
  - SSH 和 WireGuard 是两个独立的服务，密钥登录只影响 SSH。
  - 防火墙配置检查：确保 `51820/udp` 端口开放。
  - 生成密钥对：使用 `ssh-keygen` 命令生成密钥对。
  - 传公钥到 VPS：使用 `ssh` 命令将公钥传到 VPS。
  - 验证免密登录：使用 `ssh` 命令验证免密登录。
  - 密钥登录配置：修改 SSH 配置文件，禁用密码登录。
- **信息来源**：DeepSeek Harness

### SSH 客户端安装与排查

- **核心结论**：`ssh-keygen` 命令找不到说明 OpenSSH 客户端未安装或 PATH 未更新。
- **关键要点**
  - 安装 OpenSSH 客户端：使用 PowerShell 命令 `Add-WindowsCapability` 安装。
  - 检查文件路径：使用 `Test-Path` 命令检查文件路径。
  - 修复 PATH：使用 `SetEnvironmentVariable` 命令修复 PATH。
  - 使用 Git 自带的 ssh-keygen：使用 Git 安装的 `ssh-keygen` 命令。
- **信息来源**：DeepSeek Harness

### 生成与配置密钥对

- **核心结论**：生成 SSH 密钥对并配置免密登录。
- **关键要点**
  - 生成密钥对：使用 `ssh-keygen` 命令生成密钥对。
  - 传公钥到 VPS：使用 `ssh` 命令将公钥传到 VPS。
  - 验证免密登录：使用 `ssh` 命令验证免密登录。
- **信息来源**：DeepSeek Harness

### 具体操作步骤

- **生成密钥对**：
  ```powershell
  ssh-keygen -t ed25519 -N "" -f $env:USERPROFILE\.ssh\id_ed25519
  ```

- **传公钥到 VPS**：
  ```powershell
  type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh -p 10086 用户名@VPS_IP "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
  ```

- **验证免密登录**：
  ```powershell
  ssh -p 10086 用户名@VPS_IP
  ```

- **修改 SSH 配置文件**：
  ```bash
  sudo nano /etc/ssh/sshd_config
  ```
  修改 `PasswordAuthentication` 为 `no`，保存后：
  ```bash
  sudo sshd -t && sudo systemctl restart ssh
  ```

- **修复 PATH**：
  ```powershell
  [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Windows\System32\OpenSSH", "User")
  ```

- **重新安装 OpenSSH 客户端**：
  ```powershell
  Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
  ```

- **使用 Git 自带的 ssh-keygen**：
  ```powershell
  & "C:\Program Files\Git\usr\bin\ssh-keygen.exe" -t ed25519 -N "" -f $env:USERPROFILE\.ssh\id_ed25519
  ```

- **检查文件路径**：
  ```powershell
  Test-Path C:\Windows\System32\OpenSSH\ssh-keygen.exe
  ```

- **验证版本号**：
  ```powershell
  ssh -V
  ```

> **注意**：具体操作步骤需根据实际情况调整。

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(bash)
```bash
# Ubuntu 20.04+ / Debian 11+ 直接装，内核 5.6+ 已内置 WireGuard 模块
sudo apt update
sudo apt install -y wireguard

# 检查模块是否可用（有输出即正常）
modprobe wireguard && echo OK
```
### 片段 2(bash)
```bash
cd /etc/wireguard
sudo umask 077
sudo sh -c 'umask 077 && wg genkey | tee server_private.key | wg pubkey > server_public.key'
```
### 片段 3(bash)
```bash
sudo nano /etc/wireguard/wg0.conf
```
### 片段 4(ini)
```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <SERVER_PRIVATE_KEY>
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <CLIENT_PUBLIC_KEY>
AllowedIPs = 10.0.0.2/32
```
### 片段 5(bash)
```bash
echo 'net.ipv4.ip_forward = 1' | sudo tee /etc/sysctl.d/99-wireguard.conf
sudo sysctl -p /etc/sysctl.d/99-wireguard.conf

# 如果启用了 ufw
sudo ufw allow 51820/udp
```
### 片段 6(bash)
```bash
sudo sh -c 'umask 077 && cd /etc/wireguard && wg genkey | tee client_private.key | wg pubkey > client_public.key'
sudo cat /etc/wireguard/client_public.key   # 把输出填回 wg0.conf 的 [Peer] PublicKey
```
### 片段 7(bash)
```bash
sudo systemctl enable --now wg-quick@wg0
sudo wg show   # 应能看到 wg0 和 peer 信息
```
### 片段 8(ini)
```ini
[Interface]
PrivateKey = <CLIENT_PRIVATE_KEY>
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = <SERVER_PUBLIC_KEY>
Endpoint = <YOUR_VPS_IP>:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```
### 片段 9(bash)
```bash
# 服务器上
sudo wg show          # 客户端连上后会显示 latest handshake
```
### 片段 10(bash)
```bash
sudo cat /etc/wireguard/server_private.key
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
