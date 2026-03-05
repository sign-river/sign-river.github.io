---
title: "Markdown 语法指南"
date: 2026-02-10
description: "Markdown 从基础到进阶的完整语法参考手册"
image:
categories:
  - "开发"
tags:
  - "Markdown"
  - "写作效率"
  - "语法"
  - "参考手册"
draft: false
slug: "markdown-syntax-guide"
---

## 1. 前言

Markdown 是一种轻量级标记语言，让你可以用纯文本格式编写文档，然后转换成格式丰富的 HTML 页面。本文将系统介绍 Markdown 的各种语法。

## 2. 基础语法

### 2.1. 标题

使用 `#` 符号创建标题，数量表示标题级别：

```markdown
# 一级标题

## 二级标题

### 三级标题

#### 四级标题

##### 五级标题

###### 六级标题
```

### 2.2. 段落和换行

**段落**：段落之间用空行分隔

```markdown
这是第一段内容。

这是第二段内容。
```

**换行**：在行末添加两个空格或使用 `<br>`

```markdown
第一行内容
第二行内容（注意上一行末尾有两个空格）

或者使用 HTML 标签：
第一行内容<br>
第二行内容
在代码段和图片间添加空行更适合用第二种方法
```

**效果**：
第一行内容
第二行内容

或者：<br>
第一行内容<br>
第二行内容

### 2.3. 强调

```markdown
_斜体_ 或 _斜体_
**粗体** 或 **粗体**
**_粗斜体_** 或 **_粗斜体_**
~~删除线~~
```

**效果**：

- _斜体_
- **粗体**
- **_粗斜体_**
- ~~删除线~~

## 3. 列表

### 3.1. 无序列表

使用 `-`、`+` 或 `*` 加空格：

```markdown
- 第一项
- 第二项
  - 嵌套项 1
  - 嵌套项 2
- 第三项
```

**效果**：

- 第一项
- 第二项
  - 嵌套项 1
  - 嵌套项 2
- 第三项

### 3.2. 有序列表

使用数字加点加空格：

```markdown
1. 第一项
2. 第二项
   1. 嵌套项 1
   2. 嵌套项 2
3. 第三项
```

**效果**：

1. 第一项
2. 第二项
   1. 嵌套项 1
   2. 嵌套项 2
3. 第三项

### 3.3. 任务列表

```markdown
- [x] 已完成任务
- [ ] 未完成任务
- [ ] 待办事项
```

**效果**：

- [x] 已完成任务
- [ ] 未完成任务
- [ ] 待办事项

## 4. 链接和图片

### 4.1. 链接

**普通链接**：

```markdown
[链接文本](https://example.com)
[带标题的链接](https://example.com "鼠标悬停时显示")
```

**效果**：

- [GitHub 官网](https://github.com)
- [带标题的链接](https://github.com "这是鼠标悬停时的提示")

**自动链接**：

```markdown
<https://example.com>
<email@example.com>
```

**效果**：

- <https://github.com>
- <example@email.com>

**引用式链接**：

```markdown
这是 [链接][1] 和 [另一个链接][link-ref]

[1]: https://example.com
[link-ref]: https://another-example.com
```

**效果**：
这是 [GitHub][1] 和 [VS Code][link-ref]

[1]: https://github.com
[link-ref]: https://code.visualstudio.com

### 4.2. 图片

**基本语法**：

```markdown
![图片描述](图片路径。jpg)
![带标题的图片](图片路径。jpg "鼠标悬停标题")
```

**调整图片大小（需要 HTML）**：

```html
<img src="图片路径。jpg" alt="描述" width="300" />
```

**示例**：

```html
<img src="images/example.jpg" alt="示例图片" width="400" />
```

**引用式图片**（与引用式链接类似）：

```markdown
![图片][image-ref]

[image-ref]: 图片路径。jpg
```

## 5. 引用

### 5.1. 基本引用

```markdown
> 这是一句引用
>
> 可以包含多个段落
```

**效果**：

> 这是一句引用
>
> 可以包含多个段落

### 5.2. 嵌套引用

```markdown
> 第一层引用
>
> > 第二层引用
> >
> > > 第三层引用
```

**效果**：

> 第一层引用
>
> > 第二层引用
> >
> > > 第三层引用

### 5.3. 引用中使用其他元素

```markdown
> ## 引用中的标题
>
> - 列表项 1
> - 列表项 2
>
> **粗体文本**
```

**效果**：

> ## 引用中的标题
>
> - 列表项 1
> - 列表项 2
>
> **粗体文本** 和 _斜体文本_

## 6. 代码

### 6.1. 行内代码

使用反引号包裹：

```markdown
这是一段包含 `代码` 的文本。
```

**效果**：这是一段包含 `代码` 的文本。

### 6.2. 代码块

#### 6.2.1. 方式一：使用三个反引号

````markdown
```python
def hello():
    print("Hello, World!")
```
````

#### 6.2.2. 方式二：缩进四个空格

```markdown
    def hello():
        print("Hello, World!")
```

#### 6.2.3. 指定语言以启用语法高亮

````markdown
```python
print("Python 代码")
```

```javascript
console.log("JavaScript 代码");
```

```bash
echo "Shell 脚本"
```
````

**效果**：

```python
def greet(name):
    print(f"Hello, {name}!")
```

```javascript
function greet(name) {
  console.log(`Hello, ${name}!`);
}
```

```bash
#!/bin/bash
echo "Hello, World!"
```

## 7. 表格

### 7.1. 基本表格

```markdown
| 左对齐 | 居中对齐 |   右对齐 |
| :----- | :------: | -------: |
| 内容 1 |  内容 2  |   内容 3 |
| 长内容 |    短    | 中等内容 |
```

**效果**：

| 左对齐 | 居中对齐 |   右对齐 |
| :----- | :------: | -------: |
| 内容 1 |  内容 2  |   内容 3 |
| 长内容 |    短    | 中等内容 |

**对齐方式**：

- `:---` 左对齐
- `:---:` 居中
- `---:` 右对齐

## 8. 分隔线

使用三个或更多的 `-`：

```markdown
---
```

**效果**：

第一条分隔线：

## 9. 转义字符

使用反斜杠 `\` 转义特殊字符：

```markdown
\* 不是斜体
\# 不是标题
\[ 不是链接
```

**效果**：

- \* 这不会变成列表
- \# 这不会变成标题
- \[这不是链接、]

**可转义的字符**：

```
\ ` * _ { } [ ] ( ) # + - . !
```

## 10. 进阶语法

### 10.1. 脚注

```markdown
这是一段包含脚注的文本 [^1]。

[^1]: 这是脚注内容。
```

**效果**：
这是一段包含脚注的文本 [^1]，还有另一个脚注 [^2]。

[^1]: 这是第一个脚注的内容。

[^2]: 这是第二个脚注的内容。

### 10.2. 定义列表

```markdown
术语
: 定义内容
: 可以有多个定义

另一个术语
: 另一个定义
```

**效果**：

Markdown
: 一种轻量级标记语言
: 由 John Gruber 创建

HTML
: 超文本标记语言

### 10.3. 缩略语

```markdown
_[HTML]: Hyper Text Markup Language
_[CSS]: Cascading Style Sheets

HTML 和 CSS 是 Web 开发的基础。
```

## 11. HTML 支持

Markdown 支持内嵌 HTML 标签：

```html
<div align="center">
  <h2>居中标题</h2>
  <p style="color: red;">红色文字</p>
</div>

<details>
  <summary>点击展开</summary>
  隐藏的内容
</details>
```

**效果**：

<div align="center">
  <h3>这是居中的标题</h3>
  <p style="color: red;">这是红色的文字</p>
</div>

<details>
  <summary>点击展开查看更多</summary>

这里是隐藏的内容

- 可以包含列表
- 也可以包含其他 Markdown 语法
- **甚至是粗体**

</details>

## 12. 数学公式

使用 LaTeX 语法（需要支持）：

**行内公式**：

```markdown
这是行内公式 $E = mc^2$
```

**效果**：
这是行内公式 $E = mc^2$，还有勾股定理 $a^2 + b^2 = c^2$

**块级公式**：

```markdown
$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$
```

**效果**：

$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$

$$
\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

## 13. 常用技巧

### 13.1. 空行和空格

```markdown
<!-- 强制空行（HTML 注释不显示） -->

&nbsp;

<!-- 空格 -->

使用&nbsp; 添加不间断空格
```

**效果**：

第一段文字

&nbsp;

第二段文字（上方有空行）

这里有&nbsp;&nbsp;&nbsp; 三个空格&nbsp;&nbsp;&nbsp; 的效果

### 13.2. 文本居中

```html
<div align="center">居中的内容</div>
```

**效果**：

<div align="center">
  <p><strong>这段文字是居中的</strong></p>
  <p>可以包含多行内容</p>
</div>

### 13.3. 折叠内容

```html
<details>
  <summary>点击展开</summary>

  这里是折叠的内容 可以包含任何 Markdown 语法
</details>
```

**效果**（上文 HTML 支持部分已展示）

### 13.4. 颜色文字

```html
<span style="color: red;">红色文字</span>
<span style="color: blue;">蓝色文字</span>
```

**效果**：

<span style="color: red;">这是红色文字</span>
<span style="color: blue;">这是蓝色文字</span>
<span style="color: green;">这是绿色文字</span>
<span style="color: orange;">这是橙色文字</span>

## 14. VS Code 快捷键（Markdown All in One）

| 功能         | 快捷键             |
| ------------ | ------------------ |
| 加粗         | `Ctrl + B`         |
| 斜体         | `Ctrl + I`         |
| 删除线       | `Alt + S`          |
| 切换标题级别 | `Ctrl + Shift + ]` |
| 预览         | `Ctrl + K V`       |

## 15. 常见问题

### 15.1. Q: 如何在列表中添加多个段落？

A: 在段落前添加 4 个空格或 1 个 Tab：

```markdown
1. 第一项

   这是第一项的第二段。

   这是第一项的第三段。

2. 第二项
```

**效果**：

1. 第一项

   这是第一项的第二段内容。

   这是第一项的第三段内容。

2. 第二项

### 15.2. Q: 如何在表格中换行？

A: 使用 `<br>` 标签：

```markdown
| 列 1             | 列 2 |
| ---------------- | ---- |
| 第一行<br>第二行 | 内容 |
```

**效果**：

| 列 1                 | 列 2     |
| -------------------- | -------- |
| 第一行<br>第二行     | 内容     |
| 多行<br>内容<br>演示 | 这是单行 |

### 15.3. Q: 图片太大怎么办？

A: 使用 HTML 指定宽度：

```html
<img src="image.jpg" alt="描述" width="400" />
```

## 16. 在线工具推荐

- **StackEdit**：在线 Markdown 编辑器
- **Dillinger**：支持实时预览
- **Typora**：所见即所得编辑器
- **Markdown Preview Enhanced**：VS Code 插件

## 17. 参考资料

- [Markdown 官方语法](https://daringfireball.net/projects/markdown/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [CommonMark 规范](https://commonmark.org/)

---

最后更新：2026-02-10
