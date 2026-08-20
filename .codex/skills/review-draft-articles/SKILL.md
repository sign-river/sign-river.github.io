---
name: review-draft-articles
description: Inspect and summarize all draft blog articles in this repository. Use when the user asks to view, list, check, review, or summarize draft articles, unpublished posts, or content with draft enabled.
---

# 查看所有草稿文章

## 目标

只读检查仓库中的草稿文章，不修改文章内容、不修改 `draft` 状态、不提交 Git。

## 检查流程

1. 先运行 `git status --short`，记录工作区状态，但不要修改已有改动。
2. 在仓库根目录运行：

   ```powershell
   hugo list drafts
   ```

3. 如果 Hugo 命令无法提供足够信息，再使用仓库文件扫描作为补充，检查 Markdown Front Matter 中明确写有 `draft: true` 的文件。
4. 同时关注未来文章：如用户要求“所有未发布文章”，补充运行 `hugo list future`，避免遗漏日期尚未生效的内容。
5. 不把 `draft: false` 的正常文章列为草稿；不要仅凭文件名或目录位置判断文章状态。

## 输出内容

用中文按表格或分组报告：

- 文章标题
- 文件绝对路径
- 文章类型或所在结构（普通文章、专题主指南、专题子文章、项目文档）
- 分类、标签（能够可靠读取时）
- 日期
- 是否属于未来文章
- 当前是否已发布（以 Front Matter 和 Hugo 列表结果为准）

如果没有草稿，明确报告“当前没有检测到草稿文章”。如果命令失败，说明失败原因，并使用文件扫描结果标注不确定性。

## 额外检查

用户要求“检查草稿质量”时，才进一步检查：

- Front Matter 是否完整
- 分类和标签是否符合 `docs/分类标签规范.md`
- 目录结构是否符合 `docs/文章模板.md`
- 图片和附件引用是否存在
- 是否缺少描述、slug 或必要页面

仅要求“查看所有草稿”时，不要擅自修改或扩写任何文件。
