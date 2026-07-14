# 页面元数据规范

规范知识页使用 YAML front matter。必填字段：

| 字段 | 含义 |
|---|---|
| `title` | 人类可读标题 |
| `aliases` | 中英文别名和常见写法 |
| `type` | concept / evergreen / explanation / how-to / reference / learning-path / tutorial / map |
| `domain` | llm / rag / agent / ai-pm / knowledge-management |
| `status` | draft / canonical / deprecated |
| `sources` | `source-id#section` 列表 |
| `last_verified` | 最近验证日期，格式 YYYY-MM-DD |
| `freshness` | low / medium / high |
| `confidence` | low / medium / high |
| `prerequisites` | 前置页面 slug |
| `related` | 相关页面 slug |

`sources: []` 只允许用于导航、流程和本知识库自身的说明页面。

Evergreen 页面还必须包含：

| 字段 | 含义 |
|---|---|
| `maturity` | seedling / growing / evergreen |
| `claim` | 页面持续维护的核心判断 |
| `review_triggers` | 哪些证据或变化会触发复核 |
