# Repository instructions

Before creating, splitting, moving, or restructuring any article, read `docs/文章模板.md` completely.

This repository has exactly three supported article templates:

1. Standard single article
2. Topic guide with a visible main article and searchable hidden child articles
3. Project documentation with `_index.md` and `type: "project-docs"`

Choose exactly one template using the decision rules in `docs/文章模板.md`. Reuse files under `templates/` and do not invent a fourth content structure without updating the canonical guide, templates, and validation rules first.

Also follow `docs/分类标签规范.md` for taxonomy and `docs/AI辅助写作指南.md` when assisting with article writing.

## Attaching small files to articles

To attach small files (config templates, scripts, archives) to an article:

- Put the file in the article's page bundle under `files/` (e.g. `content/post/<category>/<article>/files/example.conf`).
- Reference it from the article body with a relative path: `[download example.conf](files/example.conf)` (works for Markdown links and `<a href="files/...">`).
- Hugo automatically publishes bundle files to `/p/<slug>/files/<filename>`.
- For files shared across the whole site, put them in `static/files/` and reference `/files/<filename>`.
- Name files with English letters, digits and hyphens only; do not mix Chinese/English and do not use spaces (avoids `%20` in URLs).
- Do not commit secrets (IPs, keys); redact them in published files.
- GitHub Pages limits: single file <= 100 MB, site total ~1 GB.