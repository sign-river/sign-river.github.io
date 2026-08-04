# 🌊 Sign River's Blog

我的个人技术博客，使用 Hugo + Stack 主题搭建，托管在 GitHub Pages。

🔗 **在线访问**：[https://ysy.fan](https://ysy.fan)

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

本站固定使用三种文章模板体系：

1. **普通单篇文章**：一个 `index.md` 完整承载内容
2. **专题总分架构**：一篇公开主指南聚合多篇可搜索的隐藏子文章
3. **项目介绍文档**：一个 `_index.md` 配合多个带导航的项目子页面

新建文章前必须先阅读 [文章模板体系](docs/文章模板.md)，按其中的判断规则选择一种，并复制 `templates/` 下的对应模板。

选定模板后：

1. 在 `content/post/` 的对应分类下创建内容
2. 图片放在内容同级的 `images/` 文件夹中
3. 按模板的发布前清单检查并运行 `hugo`
4. 提交并推送到 GitHub，由 GitHub Actions 自动构建部署

详细教程见：[GitHub 个人博客搭建教程](https://ysy.fan/p/github-blog-tutorial/)

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
