---
name: initialize-blog-article
description: Initialize a new blog article from this repository's supported templates and writing conventions. Use when the user asks to create, initialize, scaffold, or start a new article, topic guide, or project documentation page.
---

# 初始化博客文章

## 目标

只负责初始化文章模板和目录结构，不代替用户编写正文。必须遵循仓库现有规范，不要发明新的文章结构。

## 开始前必须读取

在创建、拆分或重构文章前，完整读取以下文件：

- `docs/文章模板.md`
- `docs/分类标签规范.md`
- `docs/AI辅助写作指南.md`
- `templates/README.md`

然后根据 `docs/文章模板.md` 的决策规则，只选择一种模板：

1. 普通单篇文章：复制 `templates/standard-article/`。
2. 专题总分架构：复制 `templates/topic-guide/`，包含公开主指南和可搜索的隐藏子文章。
3. 项目介绍文档：复制 `templates/project-docs/`，包含 `_index.md` 和多个有序子页面。

不要混用三种模板，也不要自行创建第四种结构。

## 需要确认的信息

优先从用户请求和仓库上下文中推断；只有无法安全推断时才询问。初始化至少需要：

- 文章或项目标题
- 文章类型；如果用户未指定，按 `docs/文章模板.md` 的决策规则判断
- 内容分类
- 文章目录名或 slug
- 文章涉及的标签

目录路径必须使用英文目录名；Front Matter 中的 `categories` 使用规范中的中文分类名。slug 只使用适合 URL 的英文小写字母、数字和连字符。

## 初始化流程

1. 先运行 `git status --short`，识别并保护用户已有改动。
2. 根据模板选择结果确定目标目录：
   - 普通单篇文章：`content/post/<分类目录>/<文章目录>/index.md`
   - 专题主指南：`content/post/<分类目录>/<专题目录>/guide/index.md`
   - 专题子文章：`content/post/<分类目录>/<专题目录>/<子文章目录>/index.md`
   - 项目介绍文档：`content/post/projects/<项目分类>/<项目目录>/`
3. 检查目标路径是否已存在。已有文件不得覆盖；如目标已存在，应报告冲突并停止写入该目标。
4. 从 `templates/` 复制对应模板文件，保持模板结构和字段顺序。
5. 将已知信息填入 Front Matter：标题、日期、描述、分类、标签、`draft: true`、slug 以及该模板要求的其他字段。
6. 创建专题子文章时，必须同步更新同一专题的 `guide/index.md`：按用户任务或问题类型将子文章链接加入合适的小节。链接文本应使用文章标题或能区分该问题的简洁描述；不得只设置子文章的 `guide` 字段而遗漏主指南入口。
7. 项目介绍文档必须保留 `_index.md`、`getting-started.md`、`daily-use.md`、`faq.md` 的结构；按需创建 `images/` 目录。不要把项目文档改成多个 `index.md` page bundle。
8. 普通文章和专题文章的图片放在文章目录下的 `images/`；小型附件放在文章 page bundle 的 `files/`，文件名只使用英文、数字和连字符。
9. 不主动填写用户未提供的正文事实。可以保留模板占位内容，但应明确告诉用户哪些内容仍待补充。
10. 不修改分类统计，不改变其他已有文章，不自动提交 Git。

## 图片和正文约定

初始化阶段不要替用户插入图片。需要图片的位置保留纯文字占位，或保留模板原有占位内容。后续用户粘贴图片后，遵循 `docs/AI辅助写作指南.md` 中的图片引用规范。

正文标题从 `##` 开始；按钮、选项名称使用加粗；命令、路径和文件名使用行内代码。初始化时不得删除或改写用户已有内容。

## 完成后检查

至少检查：

- 目标目录结构符合所选模板。
- Front Matter 包含模板要求的字段。
- `draft` 保持为 `true`，除非用户明确要求发布。
- 如果创建的是专题子文章，`guide/index.md` 已增加指向该子文章的链接，且子文章的 `guide` 指回同一个主指南。
- 分类和标签符合 `docs/分类标签规范.md`。
- 没有覆盖已有文件。
- 运行 `git diff --check`。
- 条件允许时运行 `hugo --gc --minify`，确认构建没有错误。

## 输出格式

完成后用中文简要报告：

1. 选择的模板类型及判断理由。
2. 创建或修改的绝对路径。
3. 已填入的 Front Matter 信息。
4. 仍待用户补充的正文、图片或附件内容。
5. 执行过的检查及结果。

如果因为目标已存在、信息不足或构建失败而未完成，明确说明原因，不要假装初始化成功。
