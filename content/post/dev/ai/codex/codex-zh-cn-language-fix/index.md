---
title: "Codex 切换简体中文界面无效的解决方法"
date: 2026-08-13
description: "Codex 桌面版把语言切换为简体中文后界面仍是英文？本文记录通过彻底退出 Codex 并在 Clash Verge 中开启全局模式后解决问题的步骤。"
categories:
  - "开发"
tags:
  - "Codex"
  - "AI 编程"
  - "Clash Verge"
  - "代理"
  - "语言设置"
  - "问题排查"
draft: true
slug: "codex-zh-cn-language-fix"
related_group: "codex"
hidden: true
searchable: true
guide: "/p/codex-guide/"
guide_title: "Codex 使用指南"
---

在 Codex 桌面版的设置中把语言切换为简体中文后，重启应用界面仍然显示英文，语言切换看起来"没有效果"。

## 1. 问题现象

在 Codex 设置中将语言切换为简体中文并重启后，界面仍是英文，简体中文设置未生效。

## 2. 解决方法

1. **彻底关闭 Codex**：不要只关闭窗口，而是完全退出应用（如通过系统托盘右键退出，或在任务管理器中结束 Codex 相关进程）。
2. **开启 Clash Verge 全局模式**：打开 Clash Verge，将代理模式由规则模式切换为**全局模式**。
3. **重新打开 Codex**：等待代理生效后重新启动 Codex，简体中文界面即可正常加载。

## 3. 验证结果

重新打开 Codex 后，界面显示为简体中文，之前切换的语言设置生效。
