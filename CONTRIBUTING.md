# 贡献与评审流程

## 修改知识

1. 从主题地图进入现有页面，优先修改而不是重复创建。
2. 更新来源、`last_verified`、相关链接和必要的冲突记录。
3. Evergreen 页面应直接重写为当前最佳理解，并在提交说明中解释观点变化。
4. 执行 `make verify_wiki`。

## 更新 Word 来源

1. 替换根目录中的上游 Word 文件。
2. 执行 `make apply_updates`。
3. 阅读 `meta/update-report.md` 中的受影响页面。
4. 更新相关 canonical / evergreen 页面。
5. 执行 `make verify_wiki`。

## 提交建议

- `source:` 上游资料变化；
- `concept:` 定义或边界变化；
- `explain:` 原理解释变化；
- `howto:` 操作流程变化；
- `reference:` 参数或检查表变化；
- `infra:` 构建、检索或检查工具变化。

大型 Word、导出图片、缓存和临时报告不进入普通 Git 提交。
