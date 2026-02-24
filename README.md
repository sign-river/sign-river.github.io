# 🌊 Sign River's Blog

我的个人技术博客，使用 Hugo + Stack 主题搭建，托管在 GitHub Pages。

🔗 **在线访问**：[https://sign-river.github.io](https://sign-river.github.io)

---

## 📝 关于本博客

这里记录我的：

- 💻 技术学习笔记
- 🛠️ 实用工具分享
- 📚 项目开发经验
- ✍️ 个人思考与总结

## 🏗️ 技术栈

- **静态网站生成器**：[Hugo](https://gohugo.io/)
- **主题**：[Hugo Theme Stack](https://github.com/CaiJimmy/hugo-theme-stack)
- **托管平台**：GitHub Pages
- **自动部署**：GitHub Actions
- **评论系统**：Giscus

## 📂 项目结构

```
.
├── config/           # 配置文件
│   └── _default/     # 默认配置
├── content/          # 文章内容
│   └── post/         # 博客文章
│       ├── tutorial/ # 教程类
│       ├── tools/    # 工具类
│       ├── projects/ # 项目类
│       ├── notes/    # 笔记类
│       ├── tech/     # 技术类
│       └── ...       # 其他分类
├── static/           # 静态资源
├── docs/             # 项目文档
└── public/           # 构建输出（自动生成）
```

## 🚀 本地运行

### 前置要求

- Git
- Hugo Extended (推荐最新版本)

### 运行步骤

1. **克隆仓库**

```bash
git clone https://github.com/sign-river/sign-river.github.io.git
cd sign-river.github.io
```

1. **启动本地服务器**

```bash
hugo server -D
```

1. **访问博客**
   打开浏览器访问 `http://localhost:1313`

## ✍️ 写作流程

1. 在 `content/post/分类/` 下创建文章文件夹
2. 创建 `index.md` 作为文章主文件
3. 图片放在同级的 `images/` 文件夹中
4. 提交并推送到 GitHub
5. GitHub Actions 自动构建部署

详细教程见：[GitHub 个人博客搭建教程](https://sign-river.github.io/p/github-blog-tutorial/)

## 🔄 更新主题

手动更新 Stack 主题：

```bash
hugo mod get -u github.com/CaiJimmy/hugo-theme-stack/v3
hugo mod tidy
```

## 📊 SEO 优化

- ✅ 已配置 sitemap.xml
- ✅ 已接入 Google Search Console
- ✅ 支持 robots.txt
- ✅ 每篇文章包含 meta description

## 📄 开源协议

本博客内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 协议。

代码部分遵循仓库原有协议。

---

**感谢 [Hugo](https://gohugo.io/) 和 [Stack 主题](https://github.com/CaiJimmy/hugo-theme-stack) 的开发者！** 🙏
