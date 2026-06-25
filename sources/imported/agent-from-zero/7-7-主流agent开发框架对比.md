---

source_id: agent-from-zero

source_file: "大模型AI Agent知识从0-1笔记-万字详解版本！ .docx"

source_section: "7. 主流Agent开发框架对比"

generated: true

---



# 7. 主流Agent开发框架对比

## 7.1 框架总览对比

点击图片可查看完整电子表格

## 7.2 LangChain深度解析

核心概念

Python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

# 1. LLM：大脑
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 2. Tools：工具
tools = [
 Tool(
 name="Search",
 func=search_function,
 description="搜索互联网信息"
 ),
 Tool(
 name="Calculator",
 func=calculator_function,
 description="执行数学计算"
 ),
]

# 3. Prompt：指令模板
prompt = PromptTemplate.from_template("""
你是一个AI助手。使用以下工具来回答问题：
{tools}

格式：
Question: {input}
Thought: 思考过程
Action: 工具名称
Action Input: 工具输入
Observation: 工具输出
... (重复)
Thought: 我现在知道答案了
Final Answer: 最终答案

Question: {input}
{agent_scratchpad}
""")

# 4. Agent：组装
agent = create_react_agent(llm, tools, prompt)

# 5. Executor：执行器
agent_executor = AgentExecutor(
 agent=agent,
 tools=tools,
 verbose=True,
 max_iterations=5,
)

# 6. 执行
result = agent_executor.invoke({"input": "2024年AI Agent市场规模是多少？"})

LangChain的优势

Python
#优势1：丰富的集成
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader

#一站式RAG方案
loader = WebBaseLoader("https://example.com/article")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
chunks = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(
 documents=chunks,
 embedding=OpenAIEmbeddings()
)

#优势2：灵活的链式组合
from langchain.chains import LLMChain

chain = (
 prompt
 | llm
 | output_parser
)

#优势3：强大的记忆管理
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=5) # 保留最近5轮对话

## 7.3 AutoGen多Agent协作

AutoGen的特色

Python
from autogen import ConversableAgent, GroupChat, GroupChatManager

#定义多个Agent
product_manager = ConversableAgent(
 name="PM",
 system_message="你是产品经理，负责需求分析和产品规划。",
 llm_config={"model": "gpt-4"},
)

engineer = ConversableAgent(
 name="Engineer",
 system_message="你是工程师，负责技术实现。",
 llm_config={"model": "gpt-4"},
)

designer = ConversableAgent(
 name="Designer",
 system_message="你是设计师，负责UI/UX设计。",
 llm_config={"model": "gpt-4"},
)

#创建群聊
group_chat = GroupChat(
 agents=[product_manager, engineer, designer],
 messages=[],
 max_round=10,
)

#管理者
manager = GroupChatManager(
 groupchat=group_chat,
 llm_config={"model": "gpt-4"},
)

#开始协作
product_manager.initiate_chat(
 manager,
 message="我们需要开发一个AI聊天应用，大家讨论一下方案。",
)

#输出示例：
#PM: "我建议使用WebSocket实现实时通信..."
#Engineer: "技术上可行，我可以用FastAPI+WebSocket实现..."
#Designer: "UI应该简洁，参考Slack的设计..."
#PM: "同意，我们先做MVP..."
#...

AutoGen的并行执行

Python
#多个Agent同时工作
from autogen import UserProxyAgent

user_proxy = UserProxyAgent(
 name="User",
 human_input_mode="NEVER", # 不需要人工输入
 code_execution_config={"work_dir": "workspace"},
)

#并行任务
tasks = [
 "搜索2024年AI发展趋势",
 "分析主要竞争对手",
 "设计产品架构",
]

import asyncio

async def parallel_execution():
 results = await asyncio.gather(*[
 agent.a_generate_reply({"content": task})
 for task in tasks
 ])
 return results

## 7.4 CrewAI角色扮演框架

CrewAI的团队概念

Python
from crewai import Agent, Task, Crew

#定义角色
researcher = Agent(
 role="Research Analyst",
 goal="发现AI Agent领域的最新趋势",
 backstory="你是一个经验丰富的AI研究分析师...",
 tools=[search_tool],
 verbose=True,
)

writer = Agent(
 role="Content Writer",
 goal="撰写吸引人的技术文章",
 backstory="你是一个技术作家，擅长将复杂概念简化...",
 tools=[],
 verbose=True,
)

#定义任务
task1 = Task(
 description="研究2024年AI Agent的市场趋势",
 agent=researcher,
 expected_output="详细的市场分析报告",
)

task2 = Task(
 description="基于研究结果撰写一篇博客文章",
 agent=writer,
 expected_output="1500字的博客文章",
)

#组建团队
crew = Crew(
 agents=[researcher, writer],
 tasks=[task1, task2],
 verbose=True,
 process="sequential", # 顺序执行
)

#启动
result = crew.kickoff()

## 7.5 Dify可视化平台

Dify的工作流编排

Python
[用户输入]
 ↓
[LLM节点: 理解意图]
 ↓
[条件分支]
 ├─ 需要搜索 → [搜索节点] → [LLM节点: 总结]
 └─ 不需要搜索 → [LLM节点: 直接回答]
 ↓
[输出节点]

Dify的优势：

✅ 拖拽式设计，无需代码

✅ 内置RAG、Agent、工作流模板

✅ 可视化调试和监控

✅ 一键部署API

适用场景：

快速原型验证

业务人员使用

低代码场景

## 7.6 框架选择指南

Python
def choose_framework(scenario):
 if scenario == "学习和探索":
 return "LangChain - 生态最完善，教程最多"
 elif scenario == "多Agent协作":
 return "AutoGen - 专为多Agent设计"
 elif scenario == "团队流程模拟":
 return "CrewAI - 角色扮演最自然"
 elif scenario == "快速原型":
 return "Dify - 可视化，上手快"
 elif scenario == "国内部署":
 return "LazyLLM - 中文优化，商汤支持"
 elif scenario == "生产级应用":
 return "LangChain + 自定义优化"
 else:
 return "LangChain - 最保险的选择"
