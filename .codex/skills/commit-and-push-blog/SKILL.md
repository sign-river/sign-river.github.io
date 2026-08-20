---
name: commit-and-push-blog
description: Validate, commit, and push intentional blog changes to the configured Git remote. Use when the user explicitly asks to submit, commit, push, publish, or sync the current blog changes to GitHub.
---

# 提交并推送博客改动

## 目标

将用户明确要求发布的博客改动安全地检查、提交并推送到当前 Git 远程仓库。只处理本次任务相关的文件，不覆盖或顺手提交无关改动。

## 执行前检查

1. 运行 `git status --short`，确认当前分支、未提交文件和是否存在未跟踪文件。
2. 查看 `git diff --stat`、`git diff --check`，必要时查看完整 diff。
3. 识别无关改动、用户未完成的编辑、生成物、密钥和敏感信息。无关文件不得加入本次提交。
4. 运行适合本仓库的检查：
   - 至少运行 `git diff --check`。
   - 内容或配置改动时运行 `hugo --gc --minify`。
   - 如用户指定了额外检查，优先执行指定检查。
5. 检查当前分支和远程：

   ```powershell
   git branch --show-current
   git remote -v
   ```

6. 不进行 `git reset --hard`、强制推送、删除分支或覆盖用户文件。

## 提交流程

1. 向用户简要说明将要提交的文件、检查结果和建议的 commit message。
2. 只有用户明确要求提交或推送时，才执行写操作；单独要求“检查”时不得提交。
3. 只暂存本次任务相关的明确文件，例如：

   ```powershell
   git add -- path/to/file1 path/to/file2
   ```

   不要使用未经检查的 `git add .`。
4. 再次检查暂存区：

   ```powershell
   git diff --cached --stat
   git diff --cached --check
   ```

5. 使用简洁、准确的提交信息。优先使用中文描述，例如：

   ```text
   docs: 初始化文章模板技能
   docs: 优化项目文章图片引用
   ```

6. 执行 `git commit -m "提交信息"`。
7. 提交成功后，确认当前分支有对应远程跟踪分支，再执行：

   ```powershell
   git push
   ```

   如果没有跟踪分支，先报告远程名、当前分支和拟执行的完整命令；不要擅自推送到错误分支。
8. 推送失败时保留本地提交，报告错误原文和下一步建议，不要自动强制推送。

## 发布前注意事项

- 文章发布前确认 Front Matter 中的 `draft` 已按用户意图设置；不要仅因为用户要求推送就自动把草稿改成正式文章。
- 项目文档的站内 `website` 地址应使用站内相对路径，例如 `/p/project-slug/getting-started/`，不要写死 GitHub Pages 域名。
- 不提交 `.env`、密钥、访问令牌、私人 IP 或其他敏感信息。
- 不修改分类统计，除非本次任务明确包含更新分类统计。

## 完成后的报告

用中文报告：

- 实际提交的文件
- 使用的 commit message
- commit SHA
- 推送到的远程和分支
- Hugo 或其他检查结果
- 如果未提交或未推送，明确说明原因
