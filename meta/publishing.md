# 发布 MkDocs Wiki

## 本地预览

建议使用独立虚拟环境：

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install -r requirements-docs.txt
make docs-serve
```

浏览器访问 `http://127.0.0.1:8000`。

发布视图由 `scripts/prepare_mkdocs.py` 生成到 `.cache/public-docs/`。它只复制 canonical、Evergreen、
解释、指南、参考和学习路径，不把原始 Word 与完整来源档案发布到网站。

## 严格构建

```bash
make docs-build
```

任何无效内部链接或 MkDocs 警告都会使构建失败。

## 发布到 GitHub Pages

1. 在 GitHub 创建空仓库。
2. 在 `mkdocs.yml` 中取消 `repo_url` 注释并填写真实地址。
3. 添加远程仓库并推送：

```bash
git remote add origin https://github.com/<username>/<repository>.git
git push -u origin main
```

4. `.github/workflows/deploy-wiki.yml` 会验证并把网站部署到 `gh-pages` 分支。
5. 在 GitHub 仓库的 **Settings → Pages** 中选择从 `gh-pages` 分支发布。

默认地址通常为：

```text
https://<username>.github.io/<repository>/
```

## 发布边界

- Markdown 知识页是事实源；
- `.cache/public-docs/` 和 `site/` 是可重建产物；
- MkDocs 只负责展示与搜索；
- 来源层保留在仓库或本地，用于审计，不进入公开导航；
- 更新知识后运行 `make verify_wiki` 和 `make docs-build`。

