---

source_id: agent-from-zero

source_file: "大模型AI Agent知识从0-1笔记-万字详解版本！ .docx"

source_section: "6. 多Agent协同系统设计"

generated: true

---



# 6. 多Agent协同系统设计

## 6.1 为什么需要多Agent？

单个Agent的局限性：

Python
假设你要开发一个完整的软件产品：

单Agent模式：
Agent：「我既要写需求文档，又要写代码，还要测试，还要设计UI...」
→ 能力有限
→ 容易出错
→ 效率低下

多Agent模式：
产品经理Agent：负责需求分析
架构师Agent：负责系统设计
开发Agent：负责编写代码
测试Agent：负责质量保证
UI设计Agent：负责界面设计

→ 专业分工
→ 并行工作
→ 质量更高

## 6.2 多Agent系统架构

![原文图片](assets/b753f02680db.png)

## 6.3 多Agent协作模式

模式1：层级结构（Hierarchical）

![原文图片](assets/4537b559254a.png)

特点：

有明确的上下级关系

管理者负责任务分配和结果整合

适合层次清晰的任务

代码实现：

Python
from langchain.agents import Agent
from langchain_openai import ChatOpenAI

class ManagerAgent:
 def init(self):
 self.llm = ChatOpenAI(model="gpt-4")
 self.workers = {
 "researcher": ResearcherAgent(),
 "analyst": AnalystAgent(),
 "writer": WriterAgent(),
 }
 
 def delegate(self, task):
 # 分析任务，分配给合适的worker
 plan = self.llm.invoke(f"""
 任务：{task}
 
 请将任务分解并分配给以下worker：
 - researcher: 负责搜集信息
 - analyst: 负责数据分析
 - writer: 负责内容创作
 
 输出JSON格式的任务分配：
 [
 {{"worker": "researcher", "subtask": "..."}},
 {{"worker": "analyst", "subtask": "..."}},
 ...
 ]
 """)
 
 # 分配任务
 results = {}
 for subtask in plan:
 worker_name = subtask["worker"]
 worker = self.workers[worker_name]
 results[worker_name] = worker.execute(subtask["subtask"])
 
 # 整合结果
 return self.integrate_results(results)
 
 def integrate_results(self, results):
 # 让LLM整合各个worker的结果
 combined = self.llm.invoke(f"""
 请整合以下各部分的结果：
 
 研究结果：{results['researcher']}
 分析结果：{results['analyst']}
 创作结果：{results['writer']}
 
 输出最终完整的报告。
 """)
 return combined

# 使用
manager = ManagerAgent()
result = manager.delegate("分析2024年AI Agent市场趋势并撰写报告")

模式2：平等协作（Collaborative）

![原文图片](assets/4177f258b16f.png)

特点：

Agents地位平等

可以相互协商和讨论

适合需要多角度思考的复杂问题

代码实现（AutoGen风格）：

Python
from autogen import ConversableAgent

# 定义三个平等的Agent
researcher = ConversableAgent(
 name="Researcher",
 system_message="你是一个研究员，负责收集和验证信息。",
 llm_config={"model": "gpt-4"},
)

critic = ConversableAgent(
 name="Critic",
 system_message="你是一个评论家，负责质疑和改进方案。",
 llm_config={"model": "gpt-4"},
)

writer = ConversableAgent(
 name="Writer",
 system_message="你是一个作家，负责组织和表达信息。",
 llm_config={"model": "gpt-4"},
)

# Agents之间的对话
def collaborative_work(task):
 # Round 1: Researcher提供初步信息
 research_result = researcher.generate_reply(
 messages=[{"role": "user", "content": task}]
 )
 
 # Round 2: Critic评价和建议
 critique = critic.generate_reply(
 messages=[
 {"role": "user", "content": task},
 {"role": "assistant", "content": research_result},
 ]
 )
 
 # Round 3: Writer整合并输出
 final_output = writer.generate_reply(
 messages=[
 {"role": "user", "content": task},
 {"role": "assistant", "content": research_result},
 {"role": "assistant", "content": critique},
 ]
 )
 
 return final_output

result = collaborative_work("设计一个AI Agent产品的营销策略")

模式3：流水线（Pipeline）

![原文图片](assets/ff0615621635.png)

特点：

固定的处理顺序

每个Agent专注于流程中的一个阶段

适合有明确步骤的任务

实际案例：内容创作流水线

Python
class ContentPipeline:
 def init(self):
 self.stages = [
 ResearchAgent(), # 阶段1：研究
 OutlineAgent(), # 阶段2：大纲
 DraftAgent(), # 阶段3：草稿
 EditorAgent(), # 阶段4：编辑
 SEOAgent(), # 阶段5：SEO优化
 ]
 
 def process(self, topic):
 data = {"topic": topic}
 
 for stage in self.stages:
 print(f"执行阶段：{stage.name}")
 data = stage.execute(data)
 print(f"输出：{data[:100]}...\n")
 
 return data

# 定义各阶段的Agent
class ResearchAgent:
 name = "Research"
 def execute(self, data):
 # 搜索相关资料
 sources = search(data["topic"])
 data["sources"] = sources
 return data

class OutlineAgent:
 name = "Outline"
 def execute(self, data):
 # 基于sources生成大纲
 outline = generate_outline(data["sources"])
 data["outline"] = outline
 return data

class DraftAgent:
 name = "Draft"
 def execute(self, data):
 # 基于outline写草稿
 draft = write_draft(data["outline"])
 data["draft"] = draft
 return data

class EditorAgent:
 name = "Editor"
 def execute(self, data):
 # 润色和改进草稿
 edited = edit_content(data["draft"])
 data["final_content"] = edited
 return data

class SEOAgent:
 name = "SEO"
 def execute(self, data):
 # 优化SEO
 optimized = add_seo_keywords(data["final_content"])
 data["seo_content"] = optimized
 return data

# 使用流水线
pipeline = ContentPipeline()
article = pipeline.process("AI Agent的商业应用")

## 6.4 多Agent的实战案例

案例：智能软件开发团队

Python
class SoftwareDevelopmentTeam:
 def init(self):
 # 定义团队成员
 self.agents = {
 "pm": ProductManagerAgent(), # 产品经理
 "architect": ArchitectAgent(), # 架构师
 "frontend": FrontendAgent(), # 前端开发
 "backend": BackendAgent(), # 后端开发
 "tester": TesterAgent(), # 测试工程师
 "reviewer": CodeReviewerAgent(), # 代码审查
 }
 
 self.coordinator = CoordinatorAgent()
 
 def develop(self, requirement):
 """完整的开发流程"""
 
 # 步骤1：产品经理分析需求
 print("📋 产品经理分析需求...")
 prd = self.agents["pm"].analyze_requirement(requirement)
 
 # 步骤2：架构师设计系统
 print("🏗️ 架构师设计系统...")
 architecture = self.agents["architect"].design_system(prd)
 
 # 步骤3：前后端并行开发
 print("💻 开发中...")
 from concurrent.futures import ThreadPoolExecutor
 
 with ThreadPoolExecutor(max_workers=2) as executor:
 frontend_future = executor.submit(
 self.agents["frontend"].develop,
 architecture["frontend_spec"]
 )
 backend_future = executor.submit(
 self.agents["backend"].develop,
 architecture["backend_spec"]
 )
 
 frontend_code = frontend_future.result()
 backend_code = backend_future.result()
 
 # 步骤4：代码审查
 print("🔍 代码审查...")
 review_result = self.agents["reviewer"].review({
 "frontend": frontend_code,
 "backend": backend_code,
 })
 
 if not review_result["passed"]:
 print("⚠️ 代码审查未通过，需要修改...")
 # 递归修改，直到通过
 return self.develop(requirement) # 简化示例
 
 # 步骤5：测试
 print("🧪 测试中...")
 test_result = self.agents["tester"].test({
 "frontend": frontend_code,
 "backend": backend_code,
 })
 
 if not test_result["passed"]:
 print("❌ 测试失败，修复bug...")
 # 修复并重新测试
 return self.develop(requirement) # 简化示例
 
 # 步骤6：部署
 print("✅ 开发完成！")
 return {
 "prd": prd,
 "architecture": architecture,
 "code": {
 "frontend": frontend_code,
 "backend": backend_code,
 },
 "test_report": test_result,
 }

# 使用
team = SoftwareDevelopmentTeam()
result = team.develop("开发一个AI聊天机器人网站")

# 输出示例：
# 📋 产品经理分析需求...
# 🏗️ 架构师设计系统...
# 💻 开发中...
# 🔍 代码审查...
# 🧪 测试中...
# ✅ 开发完成！

## 6.5 多Agent的关键挑战

挑战1：通信开销

多个Agent之间需要频繁通信：

Python
#问题：每次通信都要调用LLM
Agent1 → LLM → Agent2 → LLM → Agent3
成本和延迟都很高

# 解决：使用结构化消息
class Message:
 def init(self, sender, receiver, content, message_type):
 self.sender = sender
 self.receiver = receiver
 self.content = content # 结构化数据，不需要LLM理解
 self.type = message_type # "task", "result", "question"
 
 def to_dict(self):
 return {
 "from": self.sender,
 "to": self.receiver,
 "content": self.content,
 "type": self.type,
 }

# Agent直接处理结构化消息，只在必要时调用LLM

挑战2：死锁和循环依赖

Python
#问题：两个Agent互相等待
Agent1：等待Agent2的结果...
Agent2：等待Agent1的结果...
→ 死锁

# 解决：超时和fallback机制
class AgentCommunicator:
 def send_and_wait(self, target_agent, message, timeout=30):
 start_time = time.time()
 
 # 发送消息
 target_agent.receive(message)
 
 # 等待响应
 while time.time() - start_time < timeout:
 if target_agent.has_response():
 return target_agent.get_response()
 time.sleep(0.1)
 
 # 超时处理
 return {"error": "Timeout", "fallback": "使用默认值"}

挑战3：结果冲突

Python
#问题：不同Agent给出不同的答案
Agent1: "这个方案可行"
Agent2: "这个方案有风险"
Agent3: "这个方案成本太高"

# 解决：投票或仲裁机制
class ConflictResolver:
 def resolve(self, opinions):
 # 方法1：投票
 votes = {"agree": 0, "disagree": 0}
 for opinion in opinions:
 if opinion["stance"] == "positive":
 votes["agree"] += opinion["confidence"]
 else:
 votes["disagree"] += opinion["confidence"]
 
 if votes["agree"] > votes["disagree"]:
 return "采纳方案"
 else:
 return "否决方案"
 
 # 方法2：专家仲裁
 expert = ExpertAgent()
 final_decision = expert.judge(opinions)
 return final_decision
