---

source_id: agent-from-zero

source_file: "大模型AI Agent知识从0-1笔记-万字详解版本！ .docx"

source_section: "2. Agent核心架构深度剖析"

generated: true

---



# 2. Agent核心架构深度剖析

## 2.1 Agent整体架构图

让我们先看一张完整的Agent架构图，理解各个组件如何协同工作：

![原文图片](assets/d852ac74e525.png)

## 2.2 架构分层解析

这个架构可以分为四个核心层：

第一层：感知层（Perception Layer）

作用：接收并理解用户输入

组件：用户输入 → 大语言模型理解

类比：就像人的耳朵和眼睛

第二层：认知层（Cognition Layer）

作用：分析、推理、规划

组件：LLM Brain + 规划模块 + 推理引擎

类比：就像人的大脑

第三层：执行层（Execution Layer）

作用：调用各种工具完成任务

组件：工具集（搜索、代码、API等）

类比：就像人的手脚

第四层：记忆层（Memory Layer）

作用：存储和检索信息

组件：短期记忆 + 长期记忆

类比：就像人的记忆系统

## 2.3 数据流转过程

让我用一个具体例子说明数据如何在架构中流转：

任务：「找出2024年诺贝尔物理学奖获得者，并总结他们的主要贡献」

SQL
步骤1: 用户输入
 → 进入规划模块：识别需要「搜索」和「总结」两个步骤

步骤2: 规划完成
 → 进入推理引擎（ReAct框架）

步骤3: 第一轮思考-行动-观察循环
 Thought: "我需要搜索2024年诺贝尔物理学奖获得者"
 Action: 调用搜索工具search("2024 Nobel Prize Physics")
 Observation: 获得搜索结果→ "John Hopfield和Geoffrey Hinton"

步骤4: 第二轮思考-行动-观察循环
 Thought: "我需要了解他们的贡献"
 Action: 调用搜索工具search("Hopfield Hinton 神经网络贡献")
 Observation: 获得详细信息→ "人工神经网络和机器学习基础"

步骤5: 综合信息
 → LLM整合所有观察结果
 → 生成结构化答案
 → 存入记忆模块（长期记忆）

步骤6: 输出结果
 → 返回完整答案给用户

这个过程中，Agent不是一次性生成答案，而是通过多轮思考-行动-观察的循环，逐步接近最终答案。这就是Agent比传统LLM强大的地方。
