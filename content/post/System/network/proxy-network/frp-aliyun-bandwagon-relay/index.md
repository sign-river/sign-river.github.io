---
title: "国内中转绕开网络封锁：阿里云 + 搬瓦工 FRP 完整教程"
date: 2026-08-12
description: "通过阿里云大陆服务器作为入口，使用 FRP 反向隧道转发搬瓦工 VLESS+Reality 节点，绕开本机对海外 IP 的网络封锁。"
categories:
  - "系统"
tags:
  - "FRP"
  - "frps"
  - "frpc"
  - "阿里云"
  - "搬瓦工"
  - "VLESS"
  - "Reality"
  - "Clash Verge"
draft: false
slug: "frp-aliyun-bandwagon-relay"
related_group: "proxy-network"
hidden: true
searchable: true
guide: "/p/proxy-network-guide/"
guide_title: "自建节点教程与国内中转绕网指南"
---

## 写在前面

本方案解决"本机网络封锁国外 IP，直连自建节点（搬瓦工 VLESS+Reality）出不去"的问题：用一台**国内大陆服务器**作为入口，搬瓦工通过 **FRP 反向隧道**主动连回国内服务器，把搬瓦工上现有的节点端口（443）映射到国内服务器的公网端口。这样本机只需要连接国内服务器 IP，实际流量经"国内服务器 → FRP 隧道 → 搬瓦工节点 → 国外"转发。

**为什么选 FRP 而不是 socat / 中转客户端？** 实测结论：

- socat 裸转发对 VLESS+Reality 不兼容（握手后数据流被掐）；
- 在本次环境中观察到阿里云到搬瓦工的直连存在**握手后数据异常**（握手能过、真实代理数据不稳定）；阿里云主动连、mihomo 直连、FRP 隧道都实际测试过，最终只有 FRP 反向隧道稳定。这个结论是本线路的实测结果，不代表所有阿里云与搬瓦工线路都存在同样策略：隧道由搬瓦工主动发起并长期保持，数据在既有连接上双向流动，因此绕开了直连路径上的异常；
- 出口仍是**搬瓦工 IP**，因此 Steam、Google 等服务都能正常识别使用。

如果你还没有节点，请先阅读[搬瓦工搭建 VLESS+Reality 节点完整教程](/p/bandwagon-vless-reality-setup/)；

**前置条件：**

- 已有一台阿里云大陆服务器（本文以阿里云轻量为例）
- 已有可正常使用的搬瓦工 VLESS+Reality 节点
- 本机已装 Clash Verge（Windows）
- 会使用 SSH 登录服务器

## 1. 方案原理

```
本机 Clash ──▶ 阿里云:443 (frps) ──FRP隧道──▶ 搬瓦工:443 (frpc → 本机 VLESS节点) ──▶ 国外
```

| 组件       | 位置   | 作用                                                           |
| ---------- | ------ | -------------------------------------------------------------- |
| frps       | 阿里云 | 监听 7000 控制端口 + 443 映射端口                              |
| frpc       | 搬瓦工 | 主动连接阿里云 7000，保持反向隧道；把本机 443 节点端口映射出去 |
| 本地 Clash | 本机   | 只连阿里云 443，参数与搬瓦工节点一致                           |

## 2. 准备服务器

购买阿里云轻量服务器（就近地域、Ubuntu 24.04、月付试水），设置 root 密码并用 SSH 登录（密码登录）。详细选购步骤可参考《[国内中转绕开网络封锁：阿里云 + 一元机场完整教程](/p/network-ip-block-china-relay/)》。

## 3. 下载并安装 frp

frps（阿里云）和 frpc（搬瓦工）都需要 frp 程序。推荐**本机下载后 scp 上传**（国内服务器直连 GitHub 可能超时）：

**① 本机下载**（PowerShell）：

```powershell
curl.exe -L -f -sS --ssl-no-revoke -o "$env:USERPROFILE\Downloads\frp.tar.gz" "https://github.com/fatedier/frp/releases/download/v0.63.0/frp_0.63.0_linux_amd64.tar.gz"
```

**② 上传到两台服务器**：

```powershell
scp "$env:USERPROFILE\Downloads\frp.tar.gz" root@<阿里云IP>:/root/frp.tar.gz
scp "$env:USERPROFILE\Downloads\frp.tar.gz" root@<搬瓦工IP>:/root/frp.tar.gz
```

**③ 两台服务器分别解压安装**：

```bash
cd /root && tar -xzf frp.tar.gz
cp frp_0.63.0_linux_amd64/frps /usr/local/bin/frps
cp frp_0.63.0_linux_amd64/frpc /usr/local/bin/frpc
chmod +x /usr/local/bin/frps /usr/local/bin/frpc
mkdir -p /etc/frp
frps -v
frpc -v
```

> 也可以直接使用挂载的安装脚本：[frp-install.sh](files/frp-install.sh)（上传后 `bash frp-install.sh`，自动下载并安装）。

> **注意：frps 和 frpc 版本必须配套**（都装 0.63.0 即可）。

## 4. 阿里云部署 frps（服务端）

创建配置（可用挂载模板 [frps.toml](files/frps.toml) 修改后上传，或直接 heredoc）：

```bash
cat > /etc/frp/frps.toml <<'EOF'
bindPort = 7000
auth.method = "token"
auth.token = "<设置一个和frpc一致的token>"
EOF
```

注册为开机自启服务：

```bash
cat > /etc/systemd/system/frps.service <<'EOF'
[Unit]
Description=frps
After=network.target

[Service]
ExecStart=/usr/local/bin/frps -c /etc/frp/frps.toml
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now frps
ss -tlnp | grep ':7000'
```

**放行防火墙**（阿里云控制台）：**TCP 7000** 和 **TCP 443**。

## 5. 搬瓦工部署 frpc（客户端）

创建配置（可用挂载模板 [frpc.toml](files/frpc.toml) 修改后上传，或直接 heredoc）：

```bash
cat > /etc/frp/frpc.toml <<'EOF'
serverAddr = "<阿里云公网IP>"
serverPort = 7000
auth.method = "token"
auth.token = "<设置一个和frps一致的token>"

[[proxies]]
name = "bandwagon-443"
type = "tcp"
localIP = "127.0.0.1"
localPort = 443
remotePort = 443
EOF
```

注册为开机自启服务：

```bash
cat > /etc/systemd/system/frpc.service <<'EOF'
[Unit]
Description=frpc
After=network.target

[Service]
ExecStart=/usr/local/bin/frpc -c /etc/frp/frpc.toml
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now frpc
systemctl status frpc --no-pager | head -8
```

## 6. 验证隧道

**① 搬瓦工日志**确认连接成功：

```bash
journalctl -u frpc --no-pager -n 15
```

应看到 `login to server success` 和 `start proxy success`。

**② 阿里云确认映射端口监听**：

```bash
ss -tlnp | grep -E ':(7000|443)'
```

`443` 出现说明 frpc 已上线、隧道建立（frpc 未连接时 frps 不会监听 443）。

**③ 阿里云本机做端到端测试**（连本地 443 → 隧道 → 搬瓦工节点 → 目标）：

```bash
curl -k -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 10 --resolve gateway.icloud.com:443:127.0.0.1 https://gateway.icloud.com/
```

返回 `400`（或其他 HTTP 码）说明隧道数据已能到达搬瓦工节点，链路正常。

## 7. 本地 Clash 配置

在 Clash Verge 配置里新增一个节点——**就是搬瓦工节点本身，只是 `server` 改成阿里云 IP、`port` 改成 443**：

```yaml
proxies:
  - name: "FRP-搬瓦工"
    type: vless
    server: <阿里云公网 IP>
    port: 443
    uuid: <与搬瓦工节点链接一致的 UUID>
    network: tcp
    tls: true
    udp: true
    servername: gateway.icloud.com
    client-fingerprint: chrome
    reality-opts:
      public-key: <与搬瓦工节点链接一致的 pbk>
      short-id: <与搬瓦工节点链接一致的 sid>
```

> **⚠️ 最容易犯的错：节点参数必须和搬瓦工面板导出的 vless 链接完全一致**（尤其是 `uuid`、`public-key`、`short-id`、`servername`）。任何一处不一致都会导致握手失败/秒超时。建议直接从搬瓦工面板复制链接逐字段核对。

> **实测排错记录：UUID 必须以国外 Xray 当前入站配置为准。** 本方案曾出现“TCP 已建立、约 0.3 秒后断开”的现象，最终原因是客户端复用了旧的 3x-ui UUID，而国外服务器当前 `/usr/local/x-ui/bin/config.json` 中的 `inbounds[].settings.clients[].id` 已经变化。FRP 只负责转发 TCP，不会校验 VLESS 身份；请在国外服务器执行 `sudo grep -n '"id"' /usr/local/x-ui/bin/config.json`，把实际 UUID 同步到 Clash 配置。

保存后选中 `FRP-搬瓦工` 节点测速，绿色延迟即成功；然后打开系统代理（或 TUN）实际浏览验证。

## 8. 常见错误提醒

| 现象                                                                       | 原因与解决                                                                                   |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| frpc 日志 `connect to server error: dial tcp <阿里云IP>:7000: i/o timeout` | 阿里云防火墙 7000 未放行，或 frps 没启动。放行后重启 frpc                                    |
| frpc 日志 `login to the server failed: token ...`                          | frps 与 frpc 的 `auth.token` 不一致，改成相同值                                              |
| 阿里云 `ss` 看不到 443 监听                                                | frpc 尚未成功上线（看 frpc 日志是否 `start proxy success`）                                  |
| 本地节点秒超时 / `REALITY authentication failed`                           | ① 节点参数（uuid/pbk/sid/sni）与搬瓦工链接不一致；② 搬瓦工面板"最低客户端版本"未设为 `1.0.0` |
| 本地 TCP 能连 443 但握手后断                                               | 检查搬瓦工节点本身是否正常（先用直连确认）；若直连正常而经隧道断，多为参数问题               |
| frps/frpc 版本不一致导致异常                                               | 两台都用同一版本（0.63.0）                                                                   |

## 9. 配置备份与 token 轮换

修改 FRP 配置前先备份。阿里云服务器执行：

```bash
sudo mkdir -p /root/relay-backup
sudo cp -a /etc/frp/frps.toml /root/relay-backup/frps.toml
sudo cp -a /etc/mihomo /root/relay-backup/mihomo
sudo chmod -R 700 /root/relay-backup
```

生成新 token（不要把真实值发布到文章、工单或聊天中）：

```bash
openssl rand -hex 32
```

将同一个 token 写入两端时，可以用 `sed` 自动替换，避免手动编辑出错。先在阿里云修改并验证：

```bash
NEW_TOKEN='替换为刚生成的token'; sudo sed -i -E "s|^auth\.token = .*|auth.token = \"$NEW_TOKEN\"|" /etc/frp/frps.toml; unset NEW_TOKEN
sudo /usr/local/bin/frps verify -c /etc/frp/frps.toml
```

再在搬瓦工执行相同替换（填入完全相同的 token）并验证：

```bash
NEW_TOKEN='替换为刚生成的同一个token'; sudo sed -i -E "s|^auth\.token = .*|auth.token = \"$NEW_TOKEN\"|" /etc/frp/frpc.toml; unset NEW_TOKEN
sudo /usr/local/bin/frpc verify -c /etc/frp/frpc.toml
```

两端验证通过后，先重启阿里云 `frps`，再重启搬瓦工 `frpc`：

阿里云执行：

```bash
sudo systemctl restart frps
sudo systemctl status frps --no-pager
```

搬瓦工执行：

```bash
sudo systemctl restart frpc
sudo systemctl status frpc --no-pager
```

搬瓦工日志应出现 `login to server success`、`proxy added` 和 `start proxy success`。如果看到 `token in login doesn't match token from configuration`，说明两端 token 不一致；可先用备份恢复阿里云配置，再重新同步。

如果修改后无法登录搬瓦工，可在阿里云恢复备份并重启 `frps`：

```bash
sudo cp -a /root/relay-backup/frps.toml /etc/frp/frps.toml
sudo /usr/local/bin/frps verify -c /etc/frp/frps.toml
sudo systemctl restart frps
```

注意：把 token 直接写在命令行会进入当前 shell 的历史记录；正式环境应清理相关历史，或使用交互式编辑器/受保护的部署工具输入 token。不要把真实 token 提交到博客仓库。

## 10. 端口与 UDP 能力边界

阿里云安全组至少需要放行 `TCP 7000`（仅供搬瓦工 `frpc` 连接）和 `TCP 443`（供本机 Clash 访问）。稳定后可将 `7000/tcp` 来源限制为搬瓦工公网 IP；`7890` 等公网 SOCKS5 端口不使用时应关闭，使用时也应限制来源。

本教程的 FRP 映射是 `TCP 443 -> TCP 443`。Clash 节点中的 `udp: true` 只表示客户端协议能力，**不代表这条 FRP TCP 隧道提供原生 UDP**。网页、Steam 登录和下载等 TCP 流量可以正常工作；具体游戏是否需要 UDP，必须通过实际匹配、组队和对局验证。只有在游戏出现无法进房、语音异常或频繁掉线时，才需要另行设计 UDP/TUN/WireGuard 方案。

## 11. 大流量验证

先验证出口 IP：

```powershell
curl.exe -x socks5h://127.0.0.1:7897 https://api.ipify.org
```

应返回搬瓦工公网 IP。再用 HTTP/1.1 下载一个已知大小的测试文件，确认中途不断流且文件完整：

```powershell
curl.exe --http1.1 --retry 3 --retry-all-errors -L `
  --proxy socks5h://127.0.0.1:7897 `
  -o "$env:TEMP\test.bin" `
  https://proof.ovh.net/files/100Mb.dat
Get-Item "$env:TEMP\test.bin" | Select-Object Length
```

完整文件大小应为 `104857600` 字节。首次测试若只在 TLS 收尾阶段提示 `missing close_notify`，但文件大小完整，不应直接判定为 FRP 断流；可用上述 `--http1.1` 命令复测。
