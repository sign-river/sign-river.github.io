---
title: "PyTorch 基础入门"
date: 2026-02-10
description: "PyTorch 的基本概念和环境配置"
image: 
categories:
    - "学习笔记"
    - "深度学习"
tags:
    - "PyTorch"
    - "深度学习"
    - "机器学习"
draft: true
---

## 前言

开始学习 PyTorch，记录基础知识和学习心得。

## PyTorch 简介

PyTorch 是一个基于 Python 的科学计算包，主要用于：
- 替代 NumPy，利用 GPU 加速
- 提供灵活的深度学习研究平台

## 环境配置

### 安装 PyTorch

```bash
pip install torch torchvision torchaudio
```

### 验证安装

```python
import torch
print(torch.__version__)
print(torch.cuda.is_available())
```

## 基本概念

### Tensor（张量）

Tensor 是 PyTorch 中的核心数据结构，类似于 NumPy 的 ndarray。

```python
import torch

# 创建张量
x = torch.tensor([1, 2, 3])
print(x)

# 创建随机张量
y = torch.randn(3, 3)
print(y)
```

## 总结

待补充...

## 参考资料

- [PyTorch 官方文档](https://pytorch.org/docs/stable/index.html)
- [PyTorch 官方教程](https://pytorch.org/tutorials/)
