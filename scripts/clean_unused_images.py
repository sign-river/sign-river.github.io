# -*- coding: utf-8 -*-
"""
遍历 Hugo 博客 content 目录，找出 images/image 文件夹中未被引用的图片。

支持的目录结构：
- 普通单篇文章：<文章目录>/index.md + images/
- 专题合集：<专题目录>/guide/index.md + 各子文章 index.md（都是 leaf bundle）
- 项目文档：<项目目录>/_index.md + getting-started.md / daily-use.md / faq.md 等
  多页共享同一 images/ 目录，脚本会先聚合该目录下所有 .md 的引用再判断。

安全设计：
- 默认只试运行（dry-run），不会删除任何文件；
- 只有显式加 --delete 才会实际删除，删除前会要求输入 yes 确认（可用 --yes 跳过）；
- 引用匹配按文件名（大小写不敏感）在各自 bundle 内进行，不会跨目录误删；
- 同一 bundle 目录下所有 .md（含 _index.md、README.md）的引用都会计入，宁可漏删也不误删。

用法（在项目根目录执行）：
  python scripts/clean_unused_images.py                  # 试运行，只打印
  python scripts/clean_unused_images.py --dry-run        # 同上（显式指定）
  python scripts/clean_unused_images.py --delete         # 实际删除（需输入 yes 确认）
  python scripts/clean_unused_images.py --delete --yes   # 实际删除（跳过确认）
"""

import io
import re
import sys
from pathlib import Path
from urllib.parse import unquote

# 强制 stdout 使用 UTF-8，避免 Windows 乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── 可配置项 ──────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico"}
IMAGE_DIRS = {"images", "image"}
DELETE = "--delete" in sys.argv
SKIP_CONFIRM = "--yes" in sys.argv
# 安全优先：--dry-run 存在时始终不删除；默认（什么都不加）也是试运行
DRY_RUN = DELETE is False or "--dry-run" in sys.argv
# ─────────────────────────────────────────────────────────

# Markdown 图片：![alt](path)
RE_MD_IMAGE = re.compile(r'!\[.*?\]\(([^)]+)\)')
# HTML src/href 属性：src="..." 或 src='...'
RE_HTML_ATTR = re.compile(r'(?:src|href)\s*=\s*["\']([^"\']+)["\']')
# YAML front matter 字段（image / thumbnail / cover 等常见封面字段）
RE_YAML_IMAGE = re.compile(
    r'^(?:image|thumbnail|cover|featured_image|banner)\s*:\s*(.+)$',
    re.MULTILINE | re.IGNORECASE,
)


def extract_referenced_images(md_text: str) -> set[str]:
    """从 md 文本中提取所有引用的图片文件名（仅文件名，不含路径）。"""
    refs: set[str] = set()

    # Markdown 语法
    for m in RE_MD_IMAGE.finditer(md_text):
        refs.add(unquote(Path(m.group(1).strip()).name))

    # HTML 属性
    for m in RE_HTML_ATTR.finditer(md_text):
        path = m.group(1).strip()
        if Path(path).suffix.lower() in IMAGE_EXTENSIONS:
            refs.add(unquote(Path(path).name))

    # YAML front matter 封面字段
    for m in RE_YAML_IMAGE.finditer(md_text):
        path = m.group(1).strip().strip('"\'')
        if path and not path.startswith('#'):
            refs.add(unquote(Path(path).name))

    return refs


def iter_bundle_dirs():
    """返回 (目录, 该目录下所有 .md 文件列表) 的生成器。

    只处理 Hugo 会渲染页面、且带图片目录的 bundle：
    - index.md 存在 → leaf bundle（普通文章 / 合集主指南 / 子文章）
    - _index.md 存在 → section / 项目文档（多页共享 images/）
    - 两者都没有 → 跳过（如纯 README 目录、静态资源目录）
    聚合该目录下所有 .md 的引用，宁可漏删也不误删。
    """
    for d in sorted(CONTENT_DIR.rglob("*")):
        if not d.is_dir():
            continue
        if not any((d / n).is_dir() for n in IMAGE_DIRS):
            continue
        index_md = d / "index.md"
        section_md = d / "_index.md"
        if index_md.is_file() or section_md.is_file():
            pages = sorted(d.glob("*.md"))
            if pages:
                yield d, pages


def process_bundle(bundle_dir: Path, pages: list[Path], dry_run: bool) -> tuple[int, int]:
    """处理一个 bundle，返回 (检查图片数, 删除图片数)。"""
    referenced: set[str] = set()
    for page in pages:
        md_text = page.read_text(encoding="utf-8", errors="ignore")
        referenced |= extract_referenced_images(md_text)
    referenced_lower = {name.lower() for name in referenced}

    checked = deleted = 0
    for img_dir_name in IMAGE_DIRS:
        img_dir = bundle_dir / img_dir_name
        if not img_dir.is_dir():
            continue
        for img_file in sorted(img_dir.iterdir()):
            if not img_file.is_file():
                continue
            if img_file.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            checked += 1
            if img_file.name.lower() not in referenced_lower:
                rel = img_file.relative_to(CONTENT_DIR.parent)
                if dry_run:
                    print(f"  [将删除] {rel}")
                else:
                    img_file.unlink()
                    print(f"  [已删除] {rel}")
                deleted += 1
    return checked, deleted


def main():
    if not CONTENT_DIR.is_dir():
        print(f"错误：找不到 content 目录：{CONTENT_DIR}")
        sys.exit(1)

    if DRY_RUN:
        mode = "试运行，不会实际删除（如需删除请加 --delete）"
    else:
        mode = "将实际删除文件"

    print(f"=== Hugo 博客冗余图片清理工具（{mode}）===\n")

    if not DRY_RUN and not SKIP_CONFIRM:
        answer = input("即将删除上方扫描出的冗余图片，输入 yes 确认：").strip()
        if answer.lower() != "yes":
            print("已取消，未删除任何文件。")
            sys.exit(0)

    total_bundles = total_checked = total_deleted = 0
    for bundle_dir, pages in iter_bundle_dirs():
        checked, deleted = process_bundle(bundle_dir, pages, DRY_RUN)
        if checked > 0:
            rel = bundle_dir.relative_to(CONTENT_DIR.parent)
            page_tag = f"{len(pages)} 页" if len(pages) > 1 else "单页  "
            tag = f"删除 {deleted} 张" if deleted else "无冗余  "
            print(f"[{tag:^8}] {rel}  （{page_tag}，共 {checked} 张）")
        total_bundles += 1
        total_checked += checked
        total_deleted += deleted

    action = "将删除" if DRY_RUN else "已删除"
    print(
        f"\n扫描完毕：共 {total_bundles} 个 bundle，"
        f"检查 {total_checked} 张图片，"
        f"{action} {total_deleted} 张冗余图片。"
    )


if __name__ == "__main__":
    main()