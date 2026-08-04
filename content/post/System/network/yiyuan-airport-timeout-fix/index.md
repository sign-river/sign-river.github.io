---
title: "Clash Verge 开启 TUN 后一元机场节点全部超时的解决办法"
date: 2026-08-04
description: "解决 Clash Verge 开启 TUN 后订阅能更新但一元机场节点全部超时的问题，核心是 TUN 堆栈与 DNS 覆写配置"
categories:
  - "系统"
tags:
  - "Clash Verge"
  - "一元机场"
  - "代理"
  - "TUN"
  - "XHTTP"
  - "网络配置"
  - "问题排查"
draft: false
slug: "clash-verge-yiyuan-airport-timeout-fix"
---

本文记录 Windows 电脑端 Clash Verge 开启 TUN 后，一元机场节点全部超时的排查与解决过程：订阅能正常更新、自建节点也能使用，唯独机场节点在 TUN 模式下几乎全部 `Timeout`。最终根因与 TUN 堆栈、DNS、IPv6 以及机场节点的 XHTTP 传输方式共同相关。

## 1. 故障现象

使用环境：Windows + Clash Verge 2.5.2 + Mihomo v1.19.29，规则模式，TUN 虚拟网卡接管，机场节点为 VLESS + TLS + XHTTP（`stream-up` 模式，端口 443）。

故障表现：

1. Clash Verge 正常启动，机场订阅正常更新，流量、到期时间正常显示，节点完整加载。
2. 代理页面测速时几乎所有节点都显示 `Timeout` 或 `Error`，自动选择与故障转移也无法找到可用节点。
3. 同一订阅在朋友电脑上正常；同一台电脑使用自建节点则正常。

由此可排除：机场整体宕机、订阅链接过期、流量耗尽、节点全部失效、账号被封、客户端版本差异。

节点测速页面截图

## 2. 关键判断：问题出在 TUN 接管后的链路

订阅更新与节点连接是两条独立的网络路径：能更新订阅只说明订阅服务器可访问，不代表节点能连上。

初步验证时关闭 TUN、改用系统代理（同时关闭 IPv6）后，日本、香港等大量节点立刻恢复延迟。这说明：

- 机场节点并没有失效，账号和订阅参数基本正常；
- 电脑可以直接连接机场服务器；
- 故障主要出现在 TUN 接管流量之后，集中在 TUN 堆栈、路由、DNS 劫持、IPv6 或虚拟网卡环节。

自建节点在 TUN 下正常而机场节点超时也不矛盾：机场 XHTTP 节点同时涉及主连接域名和 `download-settings` 中的下载域名，需要维持多条 TCP/TLS/XHTTP 长连接，对 TUN 协议栈和 DNS 解析的敏感度远高于普通自建节点。

## 3. 解决办法

### 3.1. 先用系统代理验证问题范围

将设置调整为：

- TUN 虚拟网卡模式：关闭
- 系统代理：开启
- IPv6：关闭
- DNS 覆写：关闭
- 代理模式：规则

如果节点恢复延迟，即可确认故障在 TUN 接管链路，而不是节点或账号问题。

### 3.2. 将 TUN 堆栈切换为 Mixed

Clash Verge 的 TUN 设置中有三种堆栈：

- **GVisor**：TCP 和 UDP 都由 Mihomo 内置的用户态协议栈处理
- **System**：TCP 和 UDP 都走 Windows 原生协议栈
- **Mixed**：TCP 走 Windows 原生协议栈，UDP 走 GVisor 用户态协议栈

机场 XHTTP 的 TLS 长连接主要依赖 TCP，从 **GVisor** 切换为 **Mixed** 后，TCP 连接改由 Windows 原生协议栈处理，兼容性更好。

> 注意：仅切换堆栈只是短暂恢复，一段时间后节点会再次全部超时，说明根因不只是协议栈，还需要配合下一步修正 DNS 配置。

### 3.3. 修正 DNS 覆写配置（核心）

原 DNS 覆写配置存在几个问题：

1. 主设置已关闭 IPv6，但 DNS 覆写中 `ipv6: true` 且配置了 IPv6 DNS，DNS 返回 AAAA 记录后 Mihomo 尝试走不稳定的 IPv6 出口，导致连接超时。
2. `default-nameserver` 混用 `system`、阿里 DNS、Google DNS、IPv6 DNS，不同来源解析结果不一致。
3. `proxy-server-nameserver` 使用 DoH 域名，解析链路复杂。
4. `listen: ':53'` 可能与 TUN 的 `dns-hijack: any:53` 或 Windows 上其他占用 53 端口的服务冲突。

修正要点：

- `ipv6: false`，去掉 IPv6 DNS 条目
- `listen` 改为 `0.0.0.0:1053`，避开 53 端口
- `default-nameserver` 统一为国内公共 DNS（如 `223.5.5.5`）
- 开启 `use-hosts` 和 `use-system-hosts`
- `fake-ip-filter` 保留本地域名、NTP 和系统连通性探测域名

将 DNS 覆写配置整体替换为：

```yaml
dns:
  enable: true
  listen: '0.0.0.0:1053'
  enhanced-mode: 'fake-ip'
  fake-ip-range: '198.18.0.1/16'
  fake-ip-range6: 'fdfe:dcba:9876::1/64'
  fake-ip-filter-mode: 'blacklist'
  prefer-h3: false
  respect-rules: false
  use-hosts: true
  use-system-hosts: true
  ipv6: false
  fake-ip-filter:
    - '*.lan'
    - '*.local'
    - '*.arpa'
    - 'time.*.com'
    - 'ntp.*.com'
    - '+.market.xiaomi.com'
    - 'localhost.ptlogin2.qq.com'
    - '*.msftncsi.com'
    - 'www.msftconnecttest.com'
  default-nameserver:
    - '223.5.5.5'
    - '119.29.29.29'
  nameserver:
    - 'https://doh.pub/dns-query'
    - 'https://dns.alidns.com/dns-query'
  direct-nameserver-follow-policy: false
  fallback-filter:
    geoip: true
    geoip-code: 'CN'
    ipcidr:
      - '240.0.0.0/4'
      - '0.0.0.0/32'
    domain:
      - '+.google.com'
      - '+.facebook.com'
      - '+.youtube.com'
  fallback: []
  proxy-server-nameserver:
    - '223.5.5.5'
    - '119.29.29.29'
  direct-nameserver:
    - 'https://doh.pub/dns-query'
    - 'https://dns.alidns.com/dns-query'
```

## 4. 验证结果

按上述步骤调整后（TUN 开启、堆栈 **Mixed**、IPv6 关闭、DNS 覆写使用修正后的配置），一元机场节点恢复稳定延迟，TUN 模式下可正常访问网络。

## 5. 总结

遇到"订阅能更新、节点却全部超时"时，不要急着怀疑节点失效，按以下顺序排查：

1. 关闭 TUN、开启系统代理验证，确认问题是否出在 TUN 接管链路。
2. 将 TUN 堆栈切换为 **Mixed**，让 TCP 走 Windows 原生协议栈，改善 XHTTP 长连接兼容性。
3. 修正 DNS 覆写：关闭 IPv6、统一 `default-nameserver`、监听端口避开 53、开启 hosts 支持。

机场的 XHTTP 节点链路复杂，对 TUN 堆栈和 DNS 解析更敏感，以上三项需要配合调整才能彻底解决。



