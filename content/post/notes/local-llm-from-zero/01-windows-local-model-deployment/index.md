---
title: "从零开始玩转本地模型（一）：Windows 本地部署流程"
date: 2026-07-30
description: "从零开始在 Windows 上部署本地模型，完成运行环境、模型与基础工具的准备。"
slug: "windows-local-model-deployment"
image:
categories:
  - "笔记"
tags:
  - "Windows"
  - "本地模型"
  - "大语言模型"
  - "LLM"
  - "环境配置"
draft: false
---

首先确认系统配置
LM Studio 官方建议 Windows 电脑至少配备 16GB 内存和 4GB 独立显存
准备硬盘空间

建议至少预留：

20GB
虽然单个 4B 量化模型不会占这么多，但后续你可能还会下载：

Qwen3.5-4B；
Qwen3.5-9B；
不同量化版本；
微调后导出的模型。

模型最好放在空间比较充足的 D 盘或其他固态硬盘上。

二、下载安装 LM Studio

进入 LM Studio 官方下载页面 https://lmstudio.ai/download，选择：

<a href="images/2026-07-31-01-12-10.png" target="_blank"> <img src="images/2026-07-31-01-12-10.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

下载后运行安装程序，按照默认选项安装即可。LM Studio 官方支持 Windows x64，x64 电脑要求处理器支持 AVX2；近些年的 Intel 和 AMD 桌面处理器通常都支持。

安装完成后打开 LM Studio。
选给全部用户安装有可能会莫名其妙终止安装，选为自己安装即可

前面让你下载一个模型，可以选择跳过，

接下来的设置如图设置，1. Turn on Developer Mode

即开启开发者模式。2. Start local LLM service on login

即：

每次登录 Windows 时，自动在后台启动 LM Studio 的本地模型服务。

<a href="images/2026-07-31-01-23-15.png" target="_blank"> <img src="images/2026-07-31-01-23-15.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

LM Studio 支持简体中文界面。

进入左下角：

Settings
<a href="images/2026-07-31-01-24-11.png" target="_blank"> <img src="images/2026-07-31-01-24-11.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>
找到：

在 General

选择：

简体中文
<a href="images/2026-07-31-01-28-11.png" target="_blank"> <img src="images/2026-07-31-01-28-11.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>
对，目前汉化并不完整，不是你设置错了。

接下来点击右侧下载模型

<a href="images/2026-07-31-01-30-41.png" target="_blank"> <img src="images/2026-07-31-01-30-41.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

以我 5070 8gb 为例 可以下载 qwen/qwen3.5-4b — GGUF — Q4_K_M
Qwen3.5-4B 的 LM Studio 推荐量化文件约 3.75GB，支持中文、多模态图片输入和推理模式；模型本身是 4B 参数，官方页面标注最低系统内存需求为 4GB。它不会把你的 8GB 显存全部吃满，还能给上下文缓存和桌面显示留出空间。

搜索，点击下载第一个

<a href="images/2026-07-31-01-33-42.png" target="_blank"> <img src="images/2026-07-31-01-33-42.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

当然如果有大把空闲时间让电脑下载，可以多下几个，比如稍微勉强一点的 9b 模型，还有解限版

<a href="images/2026-08-01-00-53-54.png" target="_blank"> <img src="images/2026-08-01-00-53-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

在右上角的下载列表可以看到更详细的下载进度

<a href="images/2026-07-31-01-55-18.png" target="_blank"> <img src="images/2026-07-31-01-55-18.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

设置 → Hardware（硬件）

<a href="images/2026-08-01-00-47-41.png" target="_blank"> <img src="images/2026-08-01-00-47-41.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

这三项全部开启，他们的作用是 xxxx

<a href="images/2026-08-01-00-48-14.png" target="_blank"> <img src="images/2026-08-01-00-48-14.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

点击选择要加载的模型

<a href="images/2026-08-01-00-55-15.png" target="_blank"> <img src="images/2026-08-01-00-55-15.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

勾选手动选择模型参数，然后选择最基础的第一个试试能不能行

<a href="images/2026-08-01-00-57-01.png" target="_blank"> <img src="images/2026-08-01-00-57-01.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

上下文长度：8192，保持不变。
GPU 卸载：32，已经拉到最右边，代表全部层尽量放进显卡，保持不变。
预计显存占用 3.73GB
勾选 Remember settings for qwen3.5-4b，以后加载这个模型不用重复设置。
Show advanced settings 更加详尽的设置，目前只是测试能不能成功运行，暂时不用开启。
设置好后点击加载模型

<a href="images/2026-08-01-01-00-34.png" target="_blank"> <img src="images/2026-08-01-01-00-34.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如果没有选择成功，就点击上面这个再选一下

<a href="images/2026-08-01-01-01-55.png" target="_blank"> <img src="images/2026-08-01-01-01-55.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后发一句话试试：请用中文介绍你自己，并说明你能完成哪些任务。可以看到成功运行

<a href="images/2026-08-01-01-03-11.png" target="_blank"> <img src="images/2026-08-01-01-03-11.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如果要运行更大的模型比如 9b 的这个，就要适当的拉低一些设置，比如上下文改为 4096，打开拓展设置，Max Concurrent Predictions：4 → 1
这是同时生成回答的数量个人聊天只需要 1，

评估批处理大小：2048 → 512
2048 对 9B＋8GB 显存过于激进。先设 512，稳定后可以尝试 1024。
Physical Batch Size：512 → 256

<a href="images/2026-08-01-01-10-35.png" target="_blank"> <img src="images/2026-08-01-01-10-35.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>
