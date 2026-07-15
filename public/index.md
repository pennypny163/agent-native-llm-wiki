---
title: 知源编译系统
---

<section class="story-hero" markdown>
<div class="story-hero-copy" markdown>

<span class="story-label">面向人和 Agent 的 LLM/RAG/Agent 知识管理系统</span>

<div class="story-subtitle">
  <strong>知源编译系统</strong>
  <span>面向人和 Agent 的 AI 知识基础设施。</span>
</div>

# 收藏≠学习：信息焦虑后，我开始构建自己的AI知识体系

刚开始考虑转行AI产品经理，我的收集癖就犯了：先购入一大堆“一站式AI产品经理学习指南”等教程。公众号收藏的文章、小红书上买来的面经、学长学姐整理的飞书文档、技术社区的分享长文和Leetcode题库，很快塞满了各平台文件夹。前后花了¥1000+，换得短暂的安慰——资料已经在手里，只待有时间去学。

真正开始准备面试，理想化的假设不攻自破。我能想起“看过”，却找不到出处；能复述LLM名词，却讲不清它适合什么场景；同一个问题在不同资料中检索到互相冲突的答案，我无法判断该信哪一个。

重新定义问题：我缺的不是资料，也不只是点对点ima式的RAG搜索，缺的是“自我演进的判断逻辑”。我没有选择再做一个静态的“第二大脑”，而是为自己和未来的 Agent助手，构建了一个具备结构、记忆、证据与代谢能力的知识操作系统。这个网站就是我做出的第一版解决方案。目前它已经接入约 91.2 万字，以后还会继续生长。

<div class="story-actions" markdown>
[问题定义](#problem-definition){ .story-button .primary }
[检查项目实现](#evidence){ .story-button }
[直接进入 Wiki](#wiki-entry){ .story-button }
</div>

</div>

<aside class="story-note" markdown>
<span>我最后把问题写成了这句话</span>

怎样让一批散落、冲突、还会过期的资料，稳定地变成我能复用、Agent 也能核验的判断？

这比“选哪个笔记软件”难得多，也更值得长期做。
</aside>
</section>

<section class="story-metrics" markdown>
<div><strong>91.2w</strong><span>目前接入的资料，还在增加</span></div>
<div><strong>5</strong><span>已经登记的 Word 来源</span></div>
<div><strong>67</strong><span>经过整理的知识页面</span></div>
<div><strong>186</strong><span>可以被检索的 Markdown 页面</span></div>
<div><strong>5</strong><span>Agent可调用的封装MCP</span></div>
</section>

## 打破“占有即学习”的幻觉 {#problem-definition}

<section class="turning-route" markdown>
<div class="route-item" markdown>
<span>01</span>
### 错把认知差距，降维成信息差

从商科跨界到 AI 产品，面对不熟悉的LLM体系和工程约束，我的第一反应是疯狂囤资料。可技术盲区不是靠多读文章就能填平的。判断力的养成需要先构建出知识体系。
</div>

<div class="route-item" markdown>
<span>02</span>
### 关键词检索，替代不了权衡与决策

准备面试时，真正卡住我的不是“某个技术的定义在哪”，而是实际的权衡：为什么在这个场景选 RAG 而不用微调？效果和成本怎么取舍？普通的搜索只能捞出教科书式的定义，给不了在实际场景的深度思考。
</div>

<div class="route-item" markdown>
<span>03</span>
### 借用wiki：把资料先编译一遍

在腾讯实习时接触到 Karpathy 的 LLM Wiki 思路，本质上是一套人机分工：原始材料用来保留证据，人工提炼的页面用来记录核心判断，Agent 负责跑腿检索。资料不该直接去喂 AI，得先经过清洗和结构化。
</div>

<div class="route-item" markdown>
<span>04</span>
### 范式转变：把知识库当成产品来设计

不再一味充实知识库，而是构建动态的维护体系：解决信息从哪来、怎么形成当前结论、新证据进来后怎么触发更新。只有让人和 Agent 都能轻松调用，知识才能真正产生复利。
</div>
</section>

## 技术选型：从产品架构视角，设计知识编译流水线 {#system-evolution}

首先调研Github上现有的知识管理方法论：PARA 适合安置资料，却不负责判断一页内容是否可靠；Diátaxis 能区分解释、教程、操作和参考；Evergreen Notes 适合保存会被新证据修正的长期判断；Docs-as-Code 则提供纯文本、版本记录和自动检查。RAG 与 MCP 被放在最外层，只负责找到和调用知识。我的决策是：抛弃纯粹的语义搜索依赖。真正的事实源，必须是人和 Agent 都能轻松阅读、版本化管理（Docs-as-Code）且能追溯证据链的 Markdown 页面。我希望用确定性的结构，去对抗大模型幻觉的不确定性。

<section class="compiler-mini" aria-label="知识编译流水线">
  <div class="mini-flow">
    <div class="mini-node">
      <span>Input</span>
      <strong>原始资料流</strong>
      <small>公众号 / 小红书 / Word</small>
    </div>
    <div class="mini-action">
      <span>清洗与溯源</span>
      <small>Source Tracing</small>
    </div>
    <div class="mini-node">
      <span>Compile</span>
      <strong>Canonical Knowledge</strong>
      <small>重写成可判断页面</small>
    </div>
    <div class="mini-action">
      <span>时效代谢</span>
      <small>Freshness Check</small>
    </div>
    <div class="mini-node">
      <span>Connect</span>
      <strong>Learning Maps</strong>
      <small>主题地图 / 关联网络</small>
    </div>
    <div class="mini-action">
      <span>人机共用</span>
      <small>接口化调用</small>
    </div>
    <div class="mini-node">
      <span>Use</span>
      <strong>Public Wiki & MCP Tools</strong>
      <small>人阅读，Agent 核验</small>
    </div>
  </div>
  <p>核心取舍：Markdown 是事实源，RAG / MCP 只是进入和调用知识的接口。</p>
</section>

<section class="evolution-map" markdown>
<div class="evolution-stage raw" markdown>
<span>01 · 保留证据</span>
### 原文先入来源层

Word 不直接变成“正确答案”。它先被导入、分段并登记来源，原文保持可回查。

**Why**：发生分歧时，我需要看到作者究竟说了什么。
</div>

<div class="evolution-stage methods" markdown>
<span>02 · 形成答案</span>
### 围绕问题重写

我不沿着某份资料的目录抄笔记，而是把多个来源整理成 concept、explanation、how-to 或 reference 页面。

**Why**：一页只承担一种任务，内容才容易读，也容易维护。
</div>

<div class="evolution-stage system" markdown>
<span>03 · 建立关系</span>
### 用地图连接，而不是靠记忆寻找

Canonical 页面、主题地图、学习路径和 Evergreen 判断通过链接组成网络。

**Why**：人需要看到上下文，Agent 也需要沿着关系继续读取。
</div>

<div class="evolution-stage agent" markdown>
<span>04 · 阅读与调用</span>
### Wiki 给人，MCP 给 Agent

人从网站阅读；Agent 可以搜索页面、读取正文、追溯来源、寻找关联，并检查哪些内容可能过期。

**Why**：Markdown 保存事实，RAG 只是入口。检索结果不能取代事实源。
</div>
</section>

## 人机共生：知识的“代谢”与“推理”

系统最核心的产品思考，是回答：

如果一个知识库在未来要被 Agent 频繁调用，它应该具备什么特征？

我的设计哲学是：它必须满足三位不同的“读者”——当下的我、未来的我、Agent助手。

我希望的 Agent-Native，目的不止是“把资料变好看”，而是让知识具备结构、记忆、证据和生命周期。

<section class="philosophy-grid" markdown>
<div markdown>
### 当下的我：迅速建立问题地图

准备面试时，我需要从一个问题看见它的前置概念、常见方案和判断边界。主题地图和学习路径负责带路，正文负责把问题讲透。
</div>

<div markdown>
### 未来的我：认知可能固化，旧观点未更新

知识代谢机制（Metabolism）：强制标注 `last_verified`（最后验证时间）与 `conflicts`（冲突标记），对抗人的认知遗忘与滞后。
</div>

<div markdown>
### Agent：对抗传统 flat chunks 所缺乏的上下文推理能力

可推理的知识结构（Reasoning）：页面间保留强关联（link-following），提供完整的上下文、来源溯源（Source Tracing），让 Agent 能够“遍历和判断证据是否充分”，而不是瞎猜。
</div>

<div markdown>
### 共同的底线：只维护一份事实

人从页面和地图进入，Agent 从 MCP 和搜索进入，最后都回到同一份 Markdown。与其期待模型每次都记住边界，我更愿意把边界写进结构里。
</div>
</section>

## 临近秋招，我的 AI PM 认知飞轮

临近互联网公司的 AI 产品经理秋招，我正在直接拿真实问题来测试这套结构。

<section class="interview-use" markdown>
<div markdown>
### 从实际问题向下追溯

遇到“RAG 为什么失败”，我会从主题地图进入失败模式、检索链路和评估页面，再回到来源核对。缺哪一层，一眼就能看见。
</div>

<div markdown>
### 从技术事实向上做产品判断

从 LLM、RAG 到 Agent 与 Reasoning，所有的技术名词不再是孤立的散点，而是顺着网络拓扑结构（Theme Topology）自然呈现的业务解法。
</div>

<div markdown>
### 把每一次卡壳写回系统

模拟面试里讲不顺的地方，会变成一次具体更新：补来源、改页面、增加关联，或者承认当前证据还不够。复盘不再只是一份很快被遗忘的记录。
</div>

<div markdown>
### 让框架经得起检阅

从导入脚本、内容模型到 Git 历史和 MCP 工具，关键产品设计都有实现可以检查。
</div>
</section>

## 持续升值的“第二大脑”

底层的演进逻辑已经确立，未来不论是加入公司后的核心项目复盘，还是更深度的行业研究与职业决策，它们都将顺着这套“收集 → 溯源 → 抽象 → 织网 → 代谢”的编译流程无缝接入。

它允许我带着商科、产品、AI、面试、实习等不同的视角进入同一个系统，并在这个系统里，看着我的知识库像赛博生物一样，持续健康地进化。

## 你可以沿着这条链路检查它 {#evidence}

<section class="evidence-wall">
<a class="evidence-card" href="https://github.com/pennypny163/agent-native-llm-wiki/blob/main/evidence/sources.yml">
<span>Source Registry</span>
<strong>资料从哪里来</strong>
<span class="evidence-description">查看目前 5 份来源、资料类型、使用边界和登记方式。</span>
</a>

<a class="evidence-card" href="https://github.com/pennypny163/agent-native-llm-wiki/blob/main/scripts/import_docx.py">
<span>Import Pipeline</span>
<strong>原始材料如何进入系统</strong>
<span class="evidence-description">查看 DOCX 导入、章节识别和图片保留逻辑。</span>
</a>

<a class="evidence-card" href="https://github.com/pennypny163/agent-native-llm-wiki/blob/main/meta/content-model.md">
<span>Content Model</span>
<strong>一条知识应该写成什么</strong>
<span class="evidence-description">查看页面类型、元数据要求，以及内容职责如何被划分。</span>
</a>

<a class="evidence-card" href="https://github.com/pennypny163/agent-native-llm-wiki/blob/main/mcp_server/server.py">
<span>MCP Server</span>
<strong>Agent如何调用该系统</strong>
<span class="evidence-description">查看搜索、正文读取、来源追溯、关联发现和过期检查工具。</span>
</a>

<a class="evidence-card" href="maps/ai-product-management/">
<span>AI PM Map</span>
<strong>技术理解如何转化成产品判断</strong>
<span class="evidence-description">查看指标、PRD、功能评估、产品形态和面试准备之间的关系。</span>
</a>

<a class="evidence-card" href="evergreen/ai-pm-own-the-gap-between-model-capability-and-user-value/">
<span>Evergreen Claim</span>
<strong>长期持有的观点</strong>
<span class="evidence-description">模型有能力，不等于用户能获得价值；产品工作发生在两者之间。</span>
</a>
</section>

## 试阅现有内容，从这里开始 {#wiki-entry}

<div class="grid cards wiki-entry-grid" markdown>

-   :material-brain: **LLM Engineering**

    ---

    从 Tokenizer、Transformer 到训练、对齐、推理与部署。

    [进入 LLM 主题地图](maps/llm.md)

-   :material-database-search: **RAG Systems**

    ---

    从检索链路到评估：理解 RAG 为什么有效，又为什么失灵。

    [进入 RAG 主题地图](maps/rag.md)

-   :material-robot: **Agent Architecture**

    ---

    查看 Planning、Memory、Tool Use、ReAct 与可靠性设计。

    [进入 Agent 主题地图](maps/agent.md)

-   :material-account-tie: **AI Product Management**

    ---

    把技术边界、产品形态、指标体系和面试表达连起来。

    [进入 AI PM 主题地图](maps/ai-product-management.md)

</div>
