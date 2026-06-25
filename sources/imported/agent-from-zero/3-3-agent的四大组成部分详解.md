---

source_id: agent-from-zero

source_file: "大模型AI Agent知识从0-1笔记-万字详解版本！ .docx"

source_section: "3. Agent的四大组成部分详解"

generated: true

---



# 3. Agent的四大组成部分详解

## 3.1 组成部分总览

![原文图片](assets/bb043fb9054c.png)

## 3.2 组成部分一：大语言模型（LLM Brain）

作用与地位

LLM是Agent的「大脑」，负责：

理解用户意图

生成推理过程

决策选择工具

综合信息输出

当前主流选择

点击图片可查看完整电子表格

实际代码示例

Python
from langchain_openai import ChatOpenAI

# 初始化LLM作为Agent的大脑
llm = ChatOpenAI(
 model="gpt-4",
 temperature=0, # 降低随机性，提高推理稳定性
)

# LLM的推理能力展示
response = llm.invoke(
 "你需要查找2024年奥运会金牌榜，然后比较中美两国的金牌数。请分步思考如何完成这个任务。"
)
print(response.content)

# 输出示例：
# 思考步骤：
# 1. 首先需要调用搜索工具查找"2024奥运会金牌榜"
# 2. 从搜索结果中提取中国和美国的金牌数
# 3. 进行数值比较
# 4. 生成比较结果

关键点：

temperature=0：让Agent在推理时更稳定、更可预测

提示词需要引导「分步思考」，这是CoT（Chain of Thought）的核心

## 3.3 组成部分二：规划模块（Planning）

为什么需要规划？

举个例子：如果任务是「帮我准备一场技术分享会」，没有规划的Agent会：

不知道从哪开始

可能遗漏重要步骤

浪费大量token重复思考

有规划的Agent会：

Python
确定主题和目标听众
搜索相关技术资料
设计PPT大纲
准备演示Demo
生成演讲稿

两种主流规划方法

方法一：ReAct框架（边想边做）

![原文图片](assets/7423c19105f6.png)

ReAct特点：

✅ 灵活：可以根据中间结果调整计划

✅ 适合探索性任务

❌ Token消耗大：每一步都要调用LLM

方法二：Plan-and-Execute（先计划后执行）

![原文图片](assets/0a4c5e280a20.png)

Plan-and-Execute特点：

✅ 高效：只需调用一次LLM规划

✅ 可并行执行多个任务

❌ 不灵活：难以根据中间结果调整

实际代码对比

ReAct实现：

Python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# 定义工具
search_tool = Tool(
 name="Search",
 func=search_function,
 description="搜索互联网信息"
)

# 创建ReAct Agent
agent = create_react_agent(llm, [search_tool])
agent_executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True)

# 执行任务
result = agent_executor.invoke({
 "input": "找出DeepSeek-R1的训练成本，并与GPT-4对比"
})

# 输出过程（verbose=True会显示）：
# Thought: 我需要搜索DeepSeek-R1的信息
# Action: Search("DeepSeek-R1 training cost")
# Observation: [搜索结果]
# Thought: 接下来需要搜索GPT-4的成本
# Action: Search("GPT-4 training cost")
# Observation: [搜索结果]
# Thought: 现在可以进行对比了
# Final Answer: [对比结果]

Plan-and-Execute实现：

Python
from langchain.agents import Plan, Execute

# 第一步：规划
planner = create_planner(llm)
plan = planner.plan("分析2024年AI Agent市场趋势")

# 输出的计划：
# Task 1: 搜索2024年AI Agent市场报告
# Task 2: 提取市场规模数据
# Task 3: 识别主要参与者
# Task 4: 总结趋势和预测

# 第二步：执行
executor = create_executor(tools)
results = executor.execute(plan) # 按计划依次执行

选择建议

探索性任务（不知道中间会遇到什么）→ 用ReAct

流程明确的任务（步骤固定）→ 用Plan-and-Execute

复杂混合任务 → 两者结合

## 3.4 组成部分三：记忆模块（Memory）

为什么记忆很重要？

想象你在和一个朋友聊天：

没有记忆：每次对话都是新的，对方完全不记得你之前说过什么

有记忆：对方记得你的喜好、之前的讨论，对话更流畅

Agent也一样。记忆分为两类：

短期记忆（Short-term Memory）

作用：保存当前任务的上下文

存储内容：

当前对话历史

中间步骤的结果

临时变量和状态

技术实现：

Python
from langchain.memory import ConversationBufferMemory

# 创建对话记忆
memory = ConversationBufferMemory(
 memory_key="chat_history",
 return_messages=True
)

# Agent执行时自动记录
agent_executor = AgentExecutor(
 agent=agent,
 tools=tools,
 memory=memory, # 添加记忆
 verbose=True
)

# 第一轮对话
agent_executor.invoke({"input": "我叫张三，在北京工作"})

# 第二轮对话（Agent会记得上下文）
agent_executor.invoke({"input": "帮我推荐北京的餐厅"})
# Agent会知道你在北京，直接推荐北京的餐厅

短期记忆的挑战：

📊 Token限制：GPT-4有128K token限制，长对话会超出

💰 成本问题：每次调用都要把整个历史发送给LLM

解决方案：

Python
from langchain.memory import ConversationSummaryMemory

# 使用摘要记忆：自动总结历史对话
summary_memory = ConversationSummaryMemory(
 llm=llm,
 max_token_limit=2000 # 超过限制时自动总结
)

# 效果：
# 原始历史（5000 tokens）→ 总结后（500 tokens）
# "用户是张三，在北京工作，偏好川菜，预算500元以内"

长期记忆（Long-term Memory）

作用：存储可复用的知识和经验

存储内容：

用户的个人信息和偏好

历史任务的成功经验

领域知识库

工具使用的最佳实践

技术实现：使用向量数据库

Python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# 1. 创建向量数据库（长期记忆）
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
 collection_name="agent_memory",
 embedding_function=embeddings
)

# 2. 存储经验
vectorstore.add_texts([
 "用户张三偏好川菜，预算500元",
 "北京最佳川菜馆：川办、巴国布衣",
 "搜索餐厅时应该考虑：位置、评分、价格、口味"
])

# 3. Agent执行任务时检索相关记忆
query = "帮张三推荐餐厅"
relevant_memories = vectorstore.similarity_search(query, k=3)

# 4. 将记忆注入到prompt中
prompt = f"""
相关记忆：
{relevant_memories}

用户请求：{query}

请根据记忆中的信息给出推荐。
"""

记忆架构图

![原文图片](assets/442dc5acc12d.png)

记忆模块的高级技巧

技巧1：自动清理不重要的记忆

Python
#基于重要性评分的记忆管理
def should_store_in_long_term(message):
 # 让LLM判断是否重要
 importance = llm.predict(f"这条信息的重要性（1-10）：{message}")
 return int(importance) >= 7 # 只存储重要度>=7的信息

技巧2：记忆的时效性管理

Python
#给记忆加上时间戳
from datetime import datetime, timedelta

memory_item = {
 "content": "用户偏好川菜",
 "timestamp": datetime.now(),
 "expiry": datetime.now() + timedelta(days=30) # 30天后过期
}

# 检索时过滤过期记忆
def get_valid_memories():
 return [m for m in memories if m["expiry"] > datetime.now()]

## 3.5 组成部分四：工具集（Tools）

工具是Agent的「超能力」

如果说LLM是Agent的大脑，那工具就是Agent的「手脚」和「超能力」。通过工具，Agent可以：

🔍 搜索互联网

💻 执行代码

📊 操作数据库

🔧 调用API

🖥️ 控制电脑

工具的定义与实现

一个工具的标准结构：

Python
from langchain.tools import Tool

def calculate(expression: str) -> str:
 """执行数学计算"""
 try:
 result = eval(expression) # 实际生产中不要用eval
 return f"计算结果：{result}"
 except Exception as e:
 return f"计算错误：{str(e)}"

# 定义工具
calculator_tool = Tool(
 name="Calculator", # 工具名称（Agent会看到）
 func=calculate, # 工具函数
 description="""
 用于数学计算。
 输入：数学表达式字符串，如 "2 + 2" 或 "sqrt(16)"
 输出：计算结果
 何时使用：当需要进行精确数学计算时
 """ # 描述很重要！Agent通过描述来决定是否使用该工具
)

关键要素：

清晰的名称：Agent通过名称快速识别工具

详细的描述：告诉Agent什么时候用、怎么用

标准的输入输出：保证工具能被正确调用

常用工具类型与实现

搜索工具

Python
from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

search_tool = Tool(
 name="WebSearch",
 func=search.run,
 description="搜索互联网获取最新信息。适用于需要实时数据的场景。"
)

# 使用示例
result = search.run("2024年诺贝尔物理学奖")

代码执行工具

Python
def python_executor(code: str) -> str:
 """执行Python代码"""
 import io
 import sys
 from contextlib import redirect_stdout
 
 f = io.StringIO()
 try:
 with redirect_stdout(f):
 exec(code)
 return f.getvalue()
 except Exception as e:
 return f"错误：{str(e)}"

code_tool = Tool(
 name="PythonExecutor",
 func=python_executor,
 description="执行Python代码。适用于数据处理、计算、可视化等任务。"
)

# Agent可以这样用：
# code_tool.run("""
# import pandas as pd
# data = [1, 2, 3, 4, 5]
# print(f"平均值：{sum(data)/len(data)}")
# """)

API调用工具

Python
import requests

def weather_api(city: str) -> str:
 """查询天气"""
 # 假设调用某个天气API
 response = requests.get(f"https://api.weather.com/{city}")
 return response.json()

weather_tool = Tool(
 name="WeatherAPI",
 func=weather_api,
 description="查询指定城市的天气信息。输入城市名，返回温度、湿度等信息。"
)

数据库工具

Python
import sqlite3

def query_database(sql: str) -> str:
 """查询数据库"""
 conn = sqlite3.connect('my_database.db')
 cursor = conn.cursor()
 try:
 cursor.execute(sql)
 results = cursor.fetchall()
 return str(results)
 except Exception as e:
 return f"查询错误：{str(e)}"
 finally:
 conn.close()

db_tool = Tool(
 name="DatabaseQuery",
 func=query_database,
 description="执行SQL查询。适用于需要从数据库获取数据的场景。"
)

工具组合的实际案例

案例：构建一个数据分析Agent

Python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI

# 1. 准备工具集
tools = [
 search_tool, # 搜索数据
 code_tool, # 数据处理
 db_tool, # 数据库查询
]

# 2. 创建Agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_react_agent(llm, tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 3. 执行复杂任务
result = agent_executor.invoke({
 "input": """
 帮我分析一下：
 1. 从数据库中查询2024年的销售数据
 2. 搜索行业平均增长率
 3. 用Python计算我们的增长率
 4. 对比并给出结论
 """
})

# Agent的执行过程：
# Thought: 需要先从数据库获取数据
# Action: DatabaseQuery("SELECT * FROM sales WHERE year=2024")
# Observation: [...数据...]
# 
# Thought: 需要搜索行业数据
# Action: WebSearch("2024年销售行业平均增长率")
# Observation: [...行业数据...]
# 
# Thought: 现在可以计算了
# Action: PythonExecutor("
# our_growth = (current - previous) / previous * 100
# industry_avg = 15.2
# print(f'我们的增长率：{our_growth}%，行业平均：{industry_avg}%')
# ")
# Observation: 我们的增长率：18.5%，行业平均：15.2%
# 
# Thought: 可以给出结论了
# Final Answer: [完整分析报告]

工具使用的最佳实践

实践1：工具描述要精确

❌ 不好的描述：

Python
description="一个搜索工具"

✅ 好的描述：

Python
description="""
搜索互联网获取最新信息。
- 输入：搜索关键词（字符串）
- 输出：相关网页内容摘要
- 适用场景：需要实时数据、最新新闻、当前事件
- 不适用场景：历史数据、个人信息、数学计算
"""

实践2：工具要有错误处理

Python
def safe_tool(input_data):
 try:
 # 工具的实际逻辑
 result = process(input_data)
 return result
 except Exception as e:
 # 返回友好的错误信息，帮助Agent调整策略
 return f"工具执行失败：{str(e)}。建议：尝试其他方法或简化输入。"

实践3：工具要有使用日志

Python
import logging

def logged_tool(input_data):
 logging.info(f"工具被调用，输入：{input_data}")
 result = execute(input_data)
 logging.info(f"工具执行完成，输出：{result}")
 return result
