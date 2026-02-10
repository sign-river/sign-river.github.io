# Hugo 服务器管理指南

本文档记录了在本地开发博客时，如何启动、查看和关闭 Hugo 服务器的常用命令。

---

## 📦 环境信息

- **Hugo 版本**：Extended v0.155.3
- **安装路径**：`C:\Users\32173\scoop\apps\hugo-extended\`
- **项目路径**：`d:\project\blogs\sign-river.github.io\`
- **本地预览地址**：<http://localhost:1313>

---

## 🚀 启动 Hugo 服务器

在项目根目录下打开 PowerShell 或命令行，执行：

```powershell
hugo server -D
```

**参数说明：**

- `server`：启动本地开发服务器
- `-D`：显示草稿文章（draft: true 的文章也会显示）

**启动成功标志：**

```
Web Server is available at http://localhost:1313/
Press Ctrl+C to stop
```

**访问方法：**
在浏览器中打开 <http://localhost:1313> 即可实时预览博客。

**热更新：**
服务器启动后，修改任何文章或配置文件都会自动重新加载，无需手动刷新。

---

## 🔍 查找 Hugo 进程

如果不确定 Hugo 服务器是否在运行，可以使用以下命令查询：

```powershell
Get-Process hugo
```

**输出示例：**

```
Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
    234      18    38420      51836       1.25   1234   1 hugo
```

**状态判断：**

- ✅ 如果显示进程信息，说明 Hugo 正在运行
- ❌ 如果显示错误 `Get-Process : Cannot find a process with the name "hugo"`，说明没有运行

---

## 🛑 关闭 Hugo 服务器

### 方法一：正常关闭（推荐）

如果 Hugo 是在当前终端前台运行的，直接按：

```
Ctrl + C
```

服务器会优雅地停止运行。

### 方法二：强制关闭

如果 Hugo 在后台运行或无法正常停止，使用以下命令强制终止：

```powershell
Stop-Process -Name hugo -Force
```

**参数说明：**

- `-Name hugo`：指定要关闭的进程名称
- `-Force`：强制终止，不等待进程正常退出

**执行后验证：**
再次运行 `Get-Process hugo`，如果显示找不到进程，说明已成功关闭。

---

## 📝 使用 VS Code 任务

本项目已配置 VS Code 任务，可以通过以下方式快速启动：

1. 按 `Ctrl + Shift + P` 打开命令面板
2. 输入 `Tasks: Run Task`
3. 选择 `Serve Drafts` 或 `Build`

**任务说明：**

- **Serve Drafts**：启动开发服务器（等同于 `hugo server -D`）
- **Build**：构建静态网站到 `public/` 目录（等同于 `hugo`）

---

## ⚠️ 常见问题

### Q1: 端口被占用怎么办？

如果看到错误：`Error: listen tcp :1313: bind: Only one usage of each socket address`

**原因**：1313 端口已被占用（通常是之前的 Hugo 进程没有正常关闭）

**解决方法**：

```powershell
# 方法 1：关闭 Hugo 进程
Stop-Process -Name hugo -Force

# 方法 2：使用其他端口启动
hugo server -D --port 1314
```

### Q2: 修改配置文件后没有生效？

**原因**：某些配置文件修改需要重启服务器

**解决方法**：

1. 按 `Ctrl + C` 停止服务器
2. 再次运行 `hugo server -D`

### Q3: 启动后浏览器显示空白？

**检查步骤**：

1. 确认终端是否显示 "Web Server is available"
2. 检查 URL 是否正确：<http://localhost:1313（注意是> http 不是 https）
3. 尝试清除浏览器缓存或使用无痕模式

---

## 🎯 最佳实践

1. **开发时**：始终使用 `hugo server -D` 进行实时预览
2. **发布前**：执行 `hugo` 命令构建生产版本，检查 `public/` 目录内容
3. **多任务**：如果同时运行多个 Hugo 项目，记得指定不同端口
4. **结束工作**：养成习惯用 `Ctrl + C` 正常关闭服务器

---

**最后更新时间**：2026 年 2 月 9 日
