---
title: "ChatGPT 频繁「正在重新连接」？开启 Clash TUN 模式即可解决"
date: 2026-07-13
description: "ChatGPT 工作时反复显示正在重新连接，重试多次后才正常输出？原因是 WebSocket 未走代理退化为 HTTP，开启 Clash TUN 模式即可解决"
categories:
  - "开发"
tags:
  - "ChatGPT"
  - "Clash"
  - "Clash Verge"
  - "TUN"
  - "代理"
  - "问题排查"
  - "网络配置"
draft: false
slug: "chatgpt-clash-tun-mode-fix"
---

## 1. 问题现象

使用 ChatGPT 时，界面顶部频繁弹出 **正在重新连接**，往往连续重试四五次，看起来已经无法正常使用了。但稍等片刻后，回复又会突然正常输出。

这种「先失败、后恢复」的表现容易让人误以为是网络波动或 ChatGPT 服务端不稳定。

## 2. 原因分析

问题通常出在代理配置上，而非 ChatGPT 本身。

ChatGPT 优先通过 **WebSocket** 与服务器保持长连接，以实现流式输出。在仅开启系统代理、未启用 TUN 模式的情况下，Clash 往往只能接管浏览器走 HTTP 代理的那部分流量，**WebSocket 连接不一定能稳定经过代理**，于是反复握手失败，界面便不断显示「正在重新连接」。

多次重试之后，客户端会 **降级为普通 HTTP 请求** 拉取回复。HTTP 走代理通常没有问题，所以最终又能看到正常输出——给人一种「快放弃了又好了」的错觉。

## 3. 解决方案：开启 Clash TUN 模式

TUN 模式在系统网络层接管全部流量，WebSocket 与 HTTP 都会经过 Clash 路由，长连接不再频繁中断。

### 3.1. 操作步骤

以 Clash Verge 为例：

1. 打开 Clash Verge，确保代理已正常运行
2. 进入 **设置**，找到 **TUN 模式**（或 **虚拟网卡模式**）
3. 开启 **TUN 模式**，按提示授予管理员权限（Windows 首次开启需要）
4. 重新打开 ChatGPT 页面，发起一次对话验证

<a href="images/Clash%20TUN%20模式开启截图.png" target="_blank"> <img src="images/Clash%20TUN%20模式开启截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

> 若使用其他 Clash 客户端（如 Clash for Windows、Clash Meta 等），同样在设置中开启 TUN / 增强模式即可，名称可能略有不同。

## 4. 总结

| 现象                 | 原因                   | 解决                |
| -------------------- | ---------------------- | ------------------- |
| 频繁「正在重新连接」 | WebSocket 未稳定走代理 | 开启 Clash TUN 模式 |
| 重试多次后又能用     | 客户端降级为 HTTP      | 同上，无需额外操作  |

开启 TUN 模式后，ChatGPT 的 WebSocket 长连接可以稳定经代理转发，流式输出不再反复断连。
