---

source_id: agent-from-zero

source_file: "大模型AI Agent知识从0-1笔记-万字详解版本！ .docx"

source_section: "8. Agent实战案例与代码实现"

generated: true

---



# 8. Agent实战案例与代码实现

## 8.1 案例一：智能客服Agent

需求分析

Python
场景：电商平台的客服系统

功能要求：
回答常见问题（FAQ）
查询订单状态
处理退换货
转人工客服（复杂问题）
技术挑战：
需要访问数据库（订单系统）
需要记忆上下文（多轮对话）
需要情感识别（判断用户情绪）

完整实现

Python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
import sqlite3

# 1. 定义工具

def query_order(order_id: str) -> str:
 """查询订单状态"""
 conn = sqlite3.connect('ecommerce.db')
 cursor = conn.cursor()
 
 cursor.execute(
 "SELECT status, items, total FROM orders WHERE order_id = ?",
 (order_id,)
 )
 result = cursor.fetchone()
 conn.close()
 
 if result:
 status, items, total = result
 return f"订单状态：{status}，商品：{items}，总金额：{total}元"
 else:
 return "未找到该订单"

def search_faq(question: str) -> str:
 """搜索FAQ知识库"""
 faq_db = {
 "退货": "退货政策：7天无理由退货，商品需保持完好...",
 "发货": "发货时间：工作日下单当天发货，节假日顺延...",
 "支付": "支付方式：支持微信、支付宝、信用卡...",
 }
 
 # 简单的关键词匹配
 for key, answer in faq_db.items():
 if key in question:
 return answer
 
 return "未找到相关FAQ，建议转人工客服"

def detect_emotion(text: str) -> str:
 """检测用户情绪"""
 negative_words = ["生气", "不满意", "糟糕", "差", "垃圾"]
 
 for word in negative_words:
 if word in text:
 return "negative"
 
 return "neutral"

# 2. 创建工具列表

tools = [
 Tool(
 name="QueryOrder",
 func=query_order,
 description="查询订单状态。输入订单号，返回订单详情。"
 ),
 Tool(
 name="SearchFAQ",
 func=search_faq,
 description="搜索常见问题答案。输入问题关键词。"
 ),
 Tool(
 name="DetectEmotion",
 func=detect_emotion,
 description="检测用户情绪。输入用户消息文本。"
 ),
]

# 3. 创建客服Agent

llm = ChatOpenAI(model="gpt-4", temperature=0.7)

memory = ConversationBufferMemory(
 memory_key="chat_history",
 return_messages=True
)

customer_service_prompt = """
你是一个友好、专业的电商客服AI助手。

你的职责：
1. 热情回答用户问题
2. 查询订单信息
3. 处理退换货问题
4. 如遇复杂问题，建议转人工客服

重要原则：
- 始终保持礼貌和耐心
- 如果用户情绪不好，先安抚情绪
- 准确查询信息，不要编造数据
- 不确定时建议转人工

可用工具：
{tools}

对话历史：
{chat_history}

用户问题：{input}
{agent_scratchpad}
"""

agent = create_react_agent(llm, tools, customer_service_prompt)

agent_executor = AgentExecutor(
 agent=agent,
 tools=tools,
 memory=memory,
 verbose=True,
 max_iterations=5,
)

# 4. 使用示例

def chat_with_customer(user_input):
 result = agent_executor.invoke({"input": user_input})
 return result["output"]

# 对话流程
print("客服：您好！我是AI客服小助手，很高兴为您服务~")

# 第一轮
user1 = "我想查一下订单号12345的状态"
response1 = chat_with_customer(user1)
print(f"客服：{response1}")

# Agent思考过程（verbose=True会显示）：
# Thought: 用户想查询订单，我需要使用QueryOrder工具
# Action: QueryOrder
# Action Input: "12345"
# Observation: 订单状态：已发货，商品：iPhone 15，总金额：5999元
# Thought: 我现在知道订单信息了
# Final Answer: 您的订单12345已经发货啦！...

# 第二轮（记忆上下文）
user2 = "什么时候能到？"
response2 = chat_with_customer(user2)
print(f"客服：{response2}")

# Agent会记得在讨论订单12345

增强版：处理情绪和转人工

Python
class EnhancedCustomerServiceAgent:
 def __init__(self):
 self.agent = agent_executor
 self.human_agent_queue = []
 def handle_message(self, user_input):
 # 1. 检测情绪
 emotion = detect_emotion(user_input)
 if emotion == "negative":
 # 情绪不好，优先安抚
 comfort_msg = "非常抱歉给您带来不好的体验，我会尽快帮您解决问题..."
 print(f"客服：{comfort_msg}")
 # 2. Agent处理
 try:
 response = self.agent.invoke({"input": user_input})
 result = response["output"]
 # 3. 判断是否需要转人工
 if self._need_human_agent(result):
 return self._transfer_to_human(user_input)
 return result
 except Exception as e:
 # 出错时转人工
 return self._transfer_to_human(user_input)
 def _need_human_agent(self, agent_response):
 # 检测关键词
 keywords = ["转人工", "不能解决", "复杂问题"]
 return any(kw in agent_response for kw in keywords)
 def _transfer_to_human(self, user_input):
 self.human_agent_queue.append({
 "user_input": user_input,
 "timestamp": datetime.now(),
 })
 return "我为您转接人工客服，请稍等..."

#使用
enhanced_agent = EnhancedCustomerServiceAgent()
response = enhanced_agent.handle_message("我的订单有问题，很生气！")

## 8.2 案例二：代码生成Agent

需求分析

Python
功能：根据自然语言描述生成代码

流程：
 理解需求
 设计方案
 生成代码
 测试代码
 修复bug（如果有）
 添加注释和文档

实现

Python
from langchain.agents import Tool
import subprocess
import tempfile
import os

class CodeGenerationAgent:
 def init(self):
 self.llm = ChatOpenAI(model="gpt-4", temperature=0)
 
 # 定义工具
 self.tools = [
 Tool(
 name="GenerateCode",
 func=self._generate_code,
 description="生成Python代码"
 ),
 Tool(
 name="TestCode",
 func=self._test_code,
 description="测试代码是否可以运行"
 ),
 Tool(
 name="FixBug",
 func=self._fix_bug,
 description="修复代码中的bug"
 ),
 ]
 
 def _generate_code(self, requirement: str) -> str:
 """生成代码"""
 prompt = f"""
 请根据以下需求生成Python代码：
 
 需求：{requirement}
 
 要求：
 1. 代码要清晰、可读
 2. 添加必要的注释
 3. 包含错误处理
 4. 包含使用示例
 
 请输出完整的可运行代码。
 """
 
 response = self.llm.invoke(prompt)
 code = self._extract_code(response.content)
 return code
 
 def _test_code(self, code: str) -> dict:
 """测试代码"""
 # 创建临时文件
 with tempfile.NamedTemporaryFile(
 mode='w',
 suffix='.py',
 delete=False
 ) as f:
 f.write(code)
 temp_file = f.name
 
 try:
 # 运行代码
 result = subprocess.run(
 ['python', temp_file],
 capture_output=True,
 text=True,
 timeout=5
 )
 
 if result.returncode == 0:
 return {
 "success": True,
 "output": result.stdout,
 }
 else:
 return {
 "success": False,
 "error": result.stderr,
 }
 
 except subprocess.TimeoutExpired:
 return {
 "success": False,
 "error": "代码执行超时"
 }
 
 finally:
 os.unlink(temp_file)
 
 def _fix_bug(self, code: str, error: str) -> str:
 """修复bug"""
 prompt = f"""
 以下代码有错误：
 
 代码：
 ```python
 {code}
 ```
 
 错误信息：
 {error}
 
 请修复这个bug并返回完整的正确代码。
 """
 
 response = self.llm.invoke(prompt)
 fixed_code = self._extract_code(response.content)
 return fixed_code
 
 def _extract_code(self, text: str) -> str:
 """从回复中提取代码"""
 # 提取```python...```之间的内容
 import re
 pattern = r"```python\n(.*?)```"
 match = re.search(pattern, text, re.DOTALL)
 
 if match:
 return match.group(1).strip()
 else:
 return text.strip()
 
 def generate(self, requirement: str, max_attempts=3):
 """完整的代码生成流程"""
 print(f"📝 需求：{requirement}\n")
 
 # 步骤1：生成代码
 print("1️⃣ 生成代码...")
 code = self._generate_code(requirement)
 print(f"生成的代码：\n{code}\n")
 
 # 步骤2：测试代码
 print("2️⃣ 测试代码...")
 
 for attempt in range(max_attempts):
 test_result = self._test_code(code)
 
 if test_result["success"]:
 print("✅ 测试通过！")
 print(f"输出：{test_result['output']}")
 
 # 步骤3：添加文档
 print("\n3️⃣ 添加文档...")
 documented_code = self._add_documentation(code)
 
 return documented_code
 
 else:
 print(f"❌ 测试失败（尝试{attempt+1}/{max_attempts}）")
 print(f"错误：{test_result['error']}\n")
 
 # 修复bug
 print("🔧 修复bug...")
 code = self._fix_bug(code, test_result['error'])
 print(f"修复后的代码：\n{code}\n")
 
 # 所有尝试都失败
 return {
 "success": False,
 "message": f"经过{max_attempts}次尝试仍无法生成可运行的代码",
 "last_code": code,
 }
 
 def _add_documentation(self, code: str) -> str:
 """添加文档字符串"""
 prompt = f"""
 为以下代码添加详细的文档字符串（docstring）和使用说明：
 
 ```python
 {code}
 ```
 
 要求：
 1. 每个函数都有docstring
 2. 包含参数说明
 3. 包含返回值说明
 4. 包含使用示例
 """
 
 response = self.llm.invoke(prompt)
 return self._extract_code(response.content)

# 使用示例
agent = CodeGenerationAgent()

result = agent.generate("""
写一个函数，计算列表中所有数字的平方和。
要求：
- 输入是一个数字列表
- 返回平方和
- 包含错误处理（如果输入不是数字）
""")

print("\n" + "="*50)
print("最终代码：")
print("="*50)
print(result)

# 输出示例：
# 📝 需求：写一个函数，计算列表中所有数字的平方和...
# 
# 1️⃣ 生成代码...
# 生成的代码：
# def sum_of_squares(numbers):
# total = 0
# for num in numbers:
# total += num ** 2
# return total
# 
# 2️⃣ 测试代码...
# ✅ 测试通过！
# 
# 3️⃣ 添加文档...
# 
# ==================================================
# 最终代码：
# ==================================================
# def sum_of_squares(numbers):
# """
# 计算列表中所有数字的平方和。
# 
# 参数：
# numbers (list): 数字列表
# 
# 返回：
# int/float: 所有数字的平方和
# 
# 示例：
# >>> sum_of_squares([1, 2, 3])
# 14
# """
# ...

## 8.3 案例三：数据分析Agent

需求

Python
场景：自动分析Excel数据

功能：
 读取Excel文件
 数据清洗和预处理
 统计分析（均值、中位数等）
 生成可视化图表
 输出分析报告

实现（完整代码过长，展示关键部分）

Python
import pandas as pd
import matplotlib.pyplot as plt

class DataAnalysisAgent:
 def analyze(self, file_path: str, question: str):
 """
 分析数据并回答问题
 参数：
 file_path: Excel文件路径
 question: 分析问题
 """
 # 1. 读取数据
 print("📊 读取数据...")
 df = pd.read_excel(file_path)
 print(f"数据形状：{df.shape}")
 print(f"列名：{df.columns.tolist()}\n")
 # 2. 让Agent分析应该做什么
 print("🤔 分析问题...")
 analysis_plan = self._plan_analysis(df, question)
 print(f"分析计划：\n{analysis_plan}\n")
 # 3. 执行分析
 print("⚙️ 执行分析...")
 results = self._execute_analysis(df, analysis_plan)
 # 4. 生成报告
 print("📝 生成报告...")
 report = self._generate_report(results, question)
 return report
 def _plan_analysis(self, df, question):
 """制定分析计划"""
 prompt = f"""
 数据集信息：
 - 形状：{df.shape}
 - 列名：{df.columns.tolist()}
 - 前5行数据：
 {df.head().to_string()}
 问题：{question}
 请制定分析计划（JSON格式）：
 {{
 "steps": [
 {{"action": "统计描述", "columns": ["..."]}}，
 {{"action": "分组分析", "group_by": "...", "agg": "..."}},
 {{"action": "可视化", "chart_type": "...", "x": "...", "y": "..."}}
 ]
 }}
 """
 response = self.llm.invoke(prompt)
 return json.loads(response.content)
 def _execute_analysis(self, df, plan):
 """执行分析步骤"""
 results = {}
 for step in plan["steps"]:
 action = step["action"]
 if action == "统计描述":
 results["统计"] = df[step["columns"]].describe()
 elif action == "分组分析":
 results["分组"] = df.groupby(step["group_by"]).agg(step["agg"])
 elif action == "可视化":
 self._create_chart(df, step)
 results["图表"] = "已生成"
 return results

#使用
agent = DataAnalysisAgent()
report = agent.analyze(
 "sales_data.xlsx",
 "分析各地区的销售情况，找出销售最好的3个地区"
)
