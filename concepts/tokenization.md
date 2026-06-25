---
title: Tokenization
aliases: [Tokenizer, 分词, 子词切分]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#1.3
  - juliet-llm#1.3.1
  - juliet-llm#1.3.2
  - juliet-llm#1.3.3
  - juliet-llm#7.3.1
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: []
related: [text-embeddings, pretraining, decoding-strategies]
---

# Tokenization

Tokenization 把文本转换为有限词表中的 token ID 序列，是文本进入模型和模型输出文本的接口。

## 粒度取舍

- 词级词表语义单位大，但词表庞大且难处理未登录词；
- 字符或字节级覆盖稳定，但序列更长；
- 子词方法在词表大小、覆盖能力和序列长度之间折中。

常见训练方法包括 BPE、Byte-level BPE、WordPiece 和 Unigram；SentencePiece 提供了不依赖语言空格
规则的训练与编码方式。

## 为什么 tokenizer 影响模型

- 决定同一文本占用多少上下文和计算；
- 影响数字、代码、多语言和领域术语的表示；
- 词表大小决定输入 embedding 与输出 head 的规模；
- 不同 tokenizer 下的 loss 和 perplexity 不宜直接比较。

## 修改词表的风险

新增 token 会改变切分路径和 embedding 矩阵。继续预训练时，应验证旧文本是否仍按预期编码，并为
新增 embedding 设计初始化和训练方案。不能把“扩词表”当作无副作用的配置修改。

