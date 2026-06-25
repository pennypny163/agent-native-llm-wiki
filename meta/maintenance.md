---
title: 知识库维护方法
aliases: [Agentic Wiki 工作流]
type: how-to
domain: knowledge-management
status: canonical
sources: []
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: []
related: []
---

# 知识库维护方法

本知识库采用“来源层 → 规范知识层 → 导航与行动层”的编译流程。

## 导入不等于整理

`make build_wiki` 会重建来源层、本地检索索引并运行验证。导入结果可能包含
重复、过时内容甚至错误，因此不能直接视为 canonical knowledge。

日常来源更新使用 `make apply_updates`。它只生成影响报告，不会擅自改写 canonical 页面。

## 整理一个主题

1. 在 `sources/imported/` 搜索主题及其别名。
2. 比较不同来源的定义、论证、示例和发布日期。
3. 确定页面类型，不在一篇页面里混合完整教程和参数手册。
4. 写出当前最佳表述，并在元数据中列出来源章节。
5. 把不确定、冲突或待验证的内容明确写出。
6. 更新相应 `maps/` 页面并执行 `make verify_wiki`。

## 什么时候拆页

- 页面同时回答“是什么”“为什么”“怎么做”，且任一部分已经较长；
- 页面包含多个可以独立复用的概念；
- 信息的更新频率明显不同；
- 一个章节需要被多个学习路径或操作指南复用。

不要为了“原子化”把完整论证拆成缺乏上下文的碎片。

## 版本控制

- Markdown、脚本、规范和来源层文本进入 Git；
- 原始 Word 与导出的图片不进入普通 Git 历史；
- 每次提交只表达一个知识或维护目的；
- Pull Request / diff 用于复核观点变化、来源变化和链接影响；
- 自动检查必须通过后再合并。
