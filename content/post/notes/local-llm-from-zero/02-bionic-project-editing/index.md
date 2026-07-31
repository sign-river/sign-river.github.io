---
title: "从零开始玩转本地模型（二）：用 Bionic 修改项目文件"
date: 2026-08-01
description: "了解 LM Studio 的聊天边界，并通过 Bionic 将本地模型用于读取、修改和验证项目代码。"
slug: "bionic-project-editing"
image:
categories:
  - "笔记"
tags:
  - "Windows"
  - "本地模型"
  - "大语言模型"
  - "LLM"
  - "Bionic"
  - "AI 编程"
draft: false
---

> [待补充：承接上一篇，说明已完成 LM Studio 和本地模型部署；本文将把本地模型从聊天工具扩展为可协助修改项目的开发工具。]

## 一、LM Studio 的聊天边界

在 LM Studio 中，本地模型可以回答问题、解释代码和生成代码片段，但默认只能在聊天窗口中输出内容，无法直接读取或修改电脑上的项目文件。

Bionic 可以作为本地模型与项目文件之间的工作界面：将项目目录交给工具后，模型便可以基于项目上下文协助分析和修改代码。

## 三、下载并安装 Bionic

进入 Bionic 官方下载页面https://lmstudio.ai/download，选择适合当前系统的安装包。

<a href="images/[待补充：填写官方下载地址，并插入下载页面截图。].png" target="_blank"> <img src="images/[待补充：填写官方下载地址，并插入下载页面截图。].png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>


下载完成后运行安装程序，按提示完成安装。

这里注意，Bionic无法和LM Studio一同运行，在安装Bionic前先彻底关闭LM Studio

## 四、连接本地模型

打开 Bionic 后，将它连接到上一篇已经启动的本地模型服务。

<a href="images/2026-08-01-01-43-47.png" target="_blank"> <img src="images/2026-08-01-01-43-47.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

连接成功后，打开一个用于测试的项目目录。建议从可回退的小项目或独立分支开始，不要直接在唯一的生产副本上尝试。

### 1. 打开项目目录

[待补充：说明如何在 Bionic 中选择项目文件夹，以及首次读取项目时需要确认的权限。]

### 2. 描述修改需求

给模型的指令应包含修改目标、涉及范围和验收方式。例如：

```text
[待补充：填写一条实际的项目修改指令。]
```

### 3. 审查并应用改动

[待补充：说明如何查看模型提出的文件改动、确认或拒绝修改，以及如何用 Git 检查差异。]

```powershell
git status --short
git diff --check
git diff
```

## 六、使用建议与注意事项

[待补充：说明本地模型的能力边界、模型大小与硬件要求、敏感文件处理、提交前测试，以及使用 Git 分支或备份的重要性。]

## 七、总结

[待补充：总结从 LM Studio 聊天到 Bionic 项目修改的工作流，并为后续进阶内容埋下方向。]
