---
title: "Codex 使用指南：配置、工作流与问题排查"
date: 2026-08-05
description: "按使用目标汇总 Codex 相关文章，涵盖 API 与模型配置、模型能力扩展、开发工作流，以及桌面端常见问题排查。"
categories:
  - "开发"
tags:
  - "Codex"
  - "CC Switch"
  - "DeepSeek"
  - "API"
  - "AI 编程"
  - "专题指南"
draft: false
slug: "codex-guide"
related_group: "codex"
content_richness: 100
---

本指南按照读者实际要完成的任务组织内容。先判断你是准备接入 API、扩展模型能力、改进开发工作流，还是解决 Codex 桌面端的异常现象，再进入对应文章。

## 1. API 接入与模型配置

适合首次配置 Codex、自定义 API 服务或更换模型来源的场景。

- [使用 CC Switch 在 Codex 中接入 Faro API](/p/codex-faroapi-api/)
- [使用 CC Switch 在 Codex 中接入 DeepSeek API](/p/codex-deepseek-api/)

## 2. 模型能力扩展

适合基础模型已经可以使用，但还需要补充图片识别等额外能力的场景。

- [让 Codex 中的 DeepSeek 支持看图：本地视觉代理接入指南](/p/codex-deepseek-vision/)

## 3. 开发与任务工作流

适合已经能够正常使用 Codex，希望进一步改进任务拆分、并行开发或任务交接方式的场景。

- [用本地 Codex 并行开发同一个项目](/p/codex-parallel-development/)
- [在 Codex 新任务中迁移上下文](/p/codex-new-task-context-handoff/)

## 4. 桌面端问题排查

适合 Codex 已完成配置，但界面、模型列表或功能表现不符合预期的场景。

- [Codex 桌面端自定义模型列表为空的修复方法](/p/codex-desktop-custom-model-list-empty/)
- [Codex 切换简体中文界面无效的解决方法](/p/codex-zh-cn-language-fix/)

## 5. 仍未解决

如果现有文章无法解决问题，请根据问题类型提供对应信息：

- API 或模型问题：Codex 版本、接入方式、模型名称、脱敏后的配置和报错日志。
- 模型能力问题：使用的模型、代理程序、请求流程和失败时的日志。
- 工作流问题：任务目标、工作区状态、Git 状态和已经执行的步骤。
- 桌面端问题：操作系统、Codex 版本、异常现象、复现步骤和截图。
