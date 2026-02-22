---
title: "群星联机优化指南（Ubuntu 22.04 版）"
date: 2026-02-22
description: "基于 Ubuntu 22.04 64 位的 OpenVPN 虚拟局域网搭建教程"
categories:
  - "网络"
  - "游戏"
tags:
  - "群星"
  - "Stellaris"
  - "OpenVPN"
  - "联机"
  - "虚拟局域网"
  - "Ubuntu"
  - "网络配置"
draft: true
slug: "stellaris-lan-openvpn-ubuntu"
---

本文为 **Ubuntu 22.04 64 位** 系统下的群星联机节点搭建指南，内容待补充。

---

## 大纲（待撰写）

1. **引言与准备**
   - 方案简介（OpenVPN TAP、去加密、带宽与延迟）
   - 你需要准备：VPS（Ubuntu 22.04）、WinSCP、SSH 终端

2. **服务器准备与基础环境**
   - 服务器选购建议（带宽、地理位置、配置）
   - 安装必要组件：`apt update`、`unzip`、`openvpn`
   - OpenVPN 版本检查与兼容性说明（2.5/2.6 的 data-ciphers、verify-client-cert）
   - 开放防火墙端口：3074 (UDP)、3075 (TCP)（ufw 或 iptables）
   - 云厂商安全组配置
   - 特殊情况：共享型 VPS 的端口转发（NAT 映射）

3. **服务端文件部署与配置**
   - 下载并解压 server.zip（原作者教程包）
   - 使用 WinSCP 上传与解压到 `/etc/openvpn/`
   - 赋予 `checkpsw.sh` 执行权限
   - 修改 TCP/UDP 配置文件（auth none、data-ciphers none、verify-client-cert none 等）
   - 设置 `psw-file` 账号密码

4. **服务启动与开机自启**
   - 手动启动测试（TCP/UDP）、查看日志
   - 使用 systemd 配置开机自启（替代 rc.local）

5. **客户端配置与联机实测**
   - UsbEAm LAN Party 下载与 TAP 驱动安装
   - 编辑 customize.ini（IP、端口、账号密码）
   - 连接测试与 UDP 模式说明

6. **总结**
   - 使用步骤回顾

---

_请在上方各节中补充具体命令、截图与说明。配图请放在 `static/images/stellaris-lan-setup/`，与 CentOS 版共用，文中引用路径为 `/images/stellaris-lan-setup/xxx.png`。_
