---
title: "用本地 Codex 并行开发同一个项目"
date: 2026-07-31
description: "记录如何使用本地 Codex 将同一项目拆分为多个可并行推进的开发任务，并完成集成与验收。"
categories:
  - "开发"
tags:
  - "Codex"
  - "AI 编程"
  - "并行开发"
  - "本地开发"
  - "Git"
draft: true
slug: "codex-parallel-development"
---

本文演示如何借助本地 Codex 和 Git 工作树，让多个对话同时推进同一个项目中的不同任务。关键在于：先划分清楚每个任务的改动范围，再分别开发和合并。

## 1. 创建第一个工作树

首先新建一个对话。

<a href="images/2026-07-31-21-53-02.png" target="_blank"> <img src="images/2026-07-31-21-53-02.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后将本地环境切换到一个新的工作树。

<a href="images/2026-07-31-21-53-26.png" target="_blank"> <img src="images/2026-07-31-21-53-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

接下来，为第一个工作树分配任务。随后重复创建新对话和新工作树的过程，就可以让多个对话并行修改同一个项目。

在开始前，建议明确划分每个任务负责的模块和文件范围。例如，一个任务负责接口实现，另一个任务负责测试，第三个任务负责前端页面。避免多个工作树同时修改同一批文件，否则后续合并时很容易出现冲突。

<a href="images/2026-07-31-21-57-50.png" target="_blank"> <img src="images/2026-07-31-21-57-50.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

多个任务并行执行后的效果如下：
<a href="images/2026-07-31-22-01-38.png" target="_blank"> <img src="images/2026-07-31-22-01-38.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 2. 要求每个任务完成收尾

当某个工作树中的任务完成后，可以向对应对话发送下面这段提示，确保它在提交前完成必要的检查：

```text
请停止继续扩展范围，完成当前任务的收尾：

1. 运行本任务相关测试、Ruff、Python 编译和 git diff --check。
2. 只提交你自己修改的文件，不要更新 docs/任务书.md、docs/完成记录.md。
3. 创建一个清晰的 Git 提交。
4. 回复提交哈希、修改文件列表、测试结果和已知风险。
```

这样可以使每个并行任务都产出独立、可审查的提交，也便于后续定位问题。

## 3. 将各工作树的改动合并到主线

当各工作树完成 Git 提交后，在主工作区的终端中按依赖关系依次执行 `cherry-pick`。例如：

```powershell
git cherry-pick <A 的提交哈希>
git cherry-pick <C 的提交哈希>
git cherry-pick <E 的提交哈希>
git cherry-pick <D 的提交哈希>
```

这些命令会将各工作树中的提交复制到主分支。每次执行 `cherry-pick` 后，都应检查当前工作区状态和补丁格式：

```powershell
git status --short
git diff --check
```

如果发生冲突，应停留在主工作区统一处理，不要回到原工作树反复修改同一处代码。处理完成后继续执行 `cherry-pick`，并在所有提交合并完成后运行完整测试。

## 4. 小结

使用本地 Codex 并行开发的重点不在于同时开启多少个对话，而在于任务边界清晰、每项改动独立提交，并在主工作区集中完成合并与验证。这样既能提升并行效率，也能控制集成风险。
