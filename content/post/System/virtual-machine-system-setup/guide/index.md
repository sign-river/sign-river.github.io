---
title: "虚拟机系统部署指南"
date: 2026-08-16
description: "汇总在 Windows 上使用 VMware Workstation 和 VirtualBox 部署 macOS、SteamOS 测试虚拟机的完整实践。"
categories:
  - "系统"
  - "专题"
tags:
  - "虚拟机"
  - "VMware Workstation"
  - "VirtualBox"
  - "macOS"
  - "SteamOS"
draft: false
slug: "virtual-machine-system-setup-guide"
related_group: "virtual-machine-system-setup"
content_richness: 100
---

本专题汇总在 Windows 宿主机上部署不同操作系统测试虚拟机的实践文章。根据目标系统和虚拟化软件选择对应教程；两篇文章均保留独立搜索入口，便于按系统名称、虚拟化软件或具体步骤查找。

## 1. 使用 VMware 部署 macOS

- [在 Windows 的 VMware 中安装 macOS Sequoia](/p/macos-sequoia-vmware-setup/)：使用 Apple BaseSystem Recovery、VMware Workstation 和两块 VMDK，从零安装可启动的 macOS Sequoia 虚拟机。

## 2. 使用 VirtualBox 部署 SteamOS

- [在 VirtualBox 中部署 SteamOS 测试虚拟机](/p/steamos-virtualbox-setup/)：把 Steam Deck Recovery 镜像转换为 VirtualBox 虚拟机，并完成分辨率、关机和 Steam 启动配置。

## 3. 仍未解决

如果部署过程中仍有问题，请提供使用的虚拟化软件版本、宿主机系统版本、完整错误文字、出错步骤，以及相关日志或截图。