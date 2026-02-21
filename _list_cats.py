import io, sys, re
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

for md in sorted(Path("content/post").rglob("index.md")):
    text = md.read_text(encoding="utf-8", errors="ignore")
    fm = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not fm: continue
    in_cats = False
    cats = []
    for line in fm.group(1).splitlines():
        if re.match(r"^categories\s*:", line): in_cats = True; continue
        if re.match(r"^\S", line) and ":" in line: in_cats = False
        if in_cats and re.match(r"^\s+-\s+", line):
            cats.append(line.strip().lstrip("- ").strip('"'))
    if cats:
        print(f"{md.parent.name}: {cats}")
