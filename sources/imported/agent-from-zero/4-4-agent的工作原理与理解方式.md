---

source_id: agent-from-zero

source_file: "大模型AI Agent知识从0-1笔记-万字详解版本！ .docx"

source_section: "4. Agent的工作原理与理解方式"

generated: true

---



# 4. Agent的工作原理与理解方式

## 4.1 ReAct框架深度解析

ReAct（Reasoning + Acting）是目前最主流的Agent工作框架，由Google Brain研究团队提出。

ReAct的核心循环

![原文图片](assets/07c6df2373bf.png)

完整的ReAct示例

任务：「2024年哪个国家赢得了最多的奥运金牌？这个国家的首都是哪里？」

Agent的完整思考过程：

YAML
=== 第一轮循环 ===

Thought 1:
"我需要找到2024年奥运会的金牌榜信息。这需要搜索最新的数据。"

Action 1:
Tool: WebSearch
Input: "2024奥运会金牌榜"

Observation 1:
"2024年巴黎奥运会，美国队以40枚金牌位居榜首，中国队38枚金牌第二..."

=== 第二轮循环 ===

Thought 2:
"好的，美国赢得了最多的金牌。现在我需要确认美国的首都。虽然我知道是华盛顿D.C.，但为了确保准确性，我应该验证一下。"

Action 2:
Tool: WebSearch
Input: "美国首都"

Observation 2:
"美国的首都是华盛顿哥伦比亚特区（Washington, D.C.）..."

=== 完成 ===

Thought 3:
"我已经获得了所有需要的信息，可以回答了。"

Final Answer:
"2024年巴黎奥运会，美国赢得了最多的金牌（40枚）。美国的首都是华盛顿哥伦比亚特区（Washington, D.C.）。"

ReAct的代码实现

Python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

# 1. 定义ReAct的提示词模板
react_prompt = PromptTemplate.from_template("""
你是一个AI助手，通过推理和行动来解决问题。

可用工具：
{tools}

使用以下格式：

Question: 需要回答的问题
Thought: 你应该思考该做什么
Action: 要采取的行动，必须是[{tool_names}]之一
Action Input: 行动的输入
Observation: 行动的结果
... (这个Thought/Action/Action Input/Observation可以重复N次)
Thought: 我现在知道最终答案了
Final Answer: 原始问题的最终答案

开始！

Question: {input}
Thought: {agent_scratchpad}
""")

# 2. 创建工具
def search(query):
 # 简化的搜索实现
 if "金牌" in query:
 return "2024年巴黎奥运会美国队40枚金牌第一"
 elif "首都" in query:
 return "美国首都是华盛顿D.C."

search_tool = Tool(
 name="Search",
 func=search,
 description="搜索互联网信息"
)

# 3. 创建Agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_react_agent(
 llm=llm,
 tools=[search_tool],
 prompt=react_prompt
)

agent_executor = AgentExecutor(
 agent=agent,
 tools=[search_tool],
 verbose=True, # 显示详细过程
 max_iterations=5 # 最多5轮循环
)

# 4. 执行任务
result = agent_executor.invoke({
 "input": "2024年哪个国家赢得了最多的奥运金牌？这个国家的首都是哪里？"
})

print(result["output"])

## 4.2 其他Agent工作模式

除了ReAct，还有其他几种重要的工作模式：

模式1：Chain of Thought (CoT) - 纯推理

![原文图片](assets/0cb65f5a7792.png)

特点：

只有思考，没有行动

适合纯逻辑推理问题

Token消耗少

示例：

Python
问题："如果一个房间有3只猫，每只猫前面有2只猫，那一共有多少只猫？"

CoT推理：
思考1：题目说"每只猫前面有2只猫"
思考2：这意味着猫排成一排
思考3：但只有3只猫，所以是循环的或者交叉的排列
思考4：实际上还是3只猫
答案：3只猫

模式2：Plan-and-Execute - 先计划后执行

![原文图片](assets/327277d0be22.png)

特点：

先一次性规划，再按计划执行

可以并行执行任务

适合流程明确的复杂任务

代码示例：

Bash
#1. 规划阶段
planner_prompt = """
将任务分解为子任务：
任务：{task}

请输出JSON格式的任务列表：
[
 {"id": 1, "description": "...", "dependencies": []},
 {"id": 2, "description": "...", "dependencies": [1]},
 ...
]
"""

plan = llm.invoke(planner_prompt.format(
 task="分析竞争对手的产品策略"
))

# 2. 执行阶段
for task in plan:
 if all_dependencies_completed(task):
 result = execute_task(task)
 store_result(task.id, result)

模式3：Self-Ask - 自问自答

![原文图片](assets/56da82cbcf45.png)

示例：

Python
主问题："iPhone 15的屏幕比iPhone 14大多少？"

Agent自问自答：
Q1: "iPhone 15的屏幕尺寸是多少？"
→ 搜索得到：6.1英寸

Q2: "iPhone 14的屏幕尺寸是多少？"
→ 搜索得到：6.1英寸

Q3: "6.1英寸 - 6.1英寸 = ?"
→ 计算得到：0英寸

最终答案："iPhone 15和iPhone 14的屏幕尺寸相同，都是6.1英寸。"

## 4.3 理解Agent的三种视角

视角1：把Agent看作「员工」

Python
你（老板）：「帮我准备明天的演讲PPT」

Agent（员工）：
理解需求（演讲主题、目标听众）
搜索资料（行业数据、案例）
设计大纲（结构规划）
制作PPT（使用工具）
审核优化（自我检查）
交付成果（PPT文件）

这个视角帮助你：

设计Agent的职责范围

定义输入输出格式

考虑错误处理

视角2：把Agent看作「循环系统」

Python
输入 → [感知 → 思考 → 决策 → 行动 → 观察] → 输出
 ↑_______________________________|
 反馈循环

这个视角帮助你：

优化循环次数

设置终止条件

调试中间过程

视角3：把Agent看作「大脑+工具」

Python
大脑（LLM）：
 理解语言
 推理规划
 生成文本

↕ 通信

工具箱：
 搜索引擎
 计算器
 API接口
 数据库

这个视角帮助你：

扩展Agent能力（添加新工具）

优化工具选择（描述要精确）

提升执行效率（工具要快）
