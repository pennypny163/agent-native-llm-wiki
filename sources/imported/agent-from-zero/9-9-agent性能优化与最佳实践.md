---

source_id: agent-from-zero

source_file: "大模型AI Agent知识从0-1笔记-万字详解版本！ .docx"

source_section: "9. Agent性能优化与最佳实践"

generated: true

---



# 9. Agent性能优化与最佳实践

## 9.1 提示词工程优化

技巧1：Few-Shot Examples

Python
#❌ 不好的提示词
prompt = "请分析这段代码"

# ✅ 好的提示词（包含示例）
prompt = """
请分析代码的时间复杂度。

示例1：
代码：
for i in range(n):
 print(i)

分析：时间复杂度 O(n)，因为循环执行n次。

示例2：
代码：
for i in range(n):
 for j in range(n):
 print(i, j)

分析：时间复杂度 O(n²)，因为嵌套循环执行n*n次。

现在请分析以下代码：
{code}
"""

技巧2：Chain of Thought

Python
#❌ 直接要求答案
prompt = "2024年哪个国家GDP最高？"

# ✅ 引导逐步思考
prompt = """
请回答：2024年哪个国家GDP最高？

请按以下步骤思考：
1. 首先，我需要搜索2024年全球GDP排名
2. 然后，找到排名第一的国家
3. 最后，验证这个信息的可靠性

现在开始：
"""

技巧3：角色扮演

Python
#❌ 通用指令
prompt = "帮我写代码"

#✅ 明确角色
prompt = """
你是一个资深的Python工程师，有10年开发经验。
你的代码特点：
清晰易读
注重性能
考虑边界情况
包含完整的错误处理
现在请帮我写一个函数...
"""

## 9.2 工具调用优化

优化1：工具描述标准化

Python
class ToolDescriptionTemplate:
 """标准化的工具描述模板"""
 @staticmethod
 def create_description(
 purpose: str,
 input_format: str,
 output_format: str,
 use_cases: list,
 limitations: list,
 ):
 return f"""
工具目的：{purpose}

输入格式：{input_format}
输出格式：{output_format}

适用场景：
{chr(10).join(f"- {case}" for case in use_cases)}

不适用场景：
{chr(10).join(f"- {limit}" for limit in limitations)}

示例：
输入："example_input"
输出："example_output"
"""

使用
search_tool_desc = ToolDescriptionTemplate.create_description(
 purpose="搜索互联网获取最新信息",
 input_format="字符串（搜索查询）",
 output_format="字符串（搜索结果摘要）",
 use_cases=[
 "需要最新数据（新闻、事件）",
 "查找具体信息（人物、地点）",
 "验证事实",
 ],
 limitations=[
 "不用于数学计算",
 "不用于代码执行",
 "不用于个人隐私信息",
 ],
)

优化2：工具调用缓存

Python
from functools import lru_cache
import hashlib

class CachedToolExecutor:
 def init(self):
 self.cache = {}
 self.cache_hits = 0
 self.cache_misses = 0
 
 def execute(self, tool_name: str, tool_input: str):
 # 生成缓存key
 cache_key = hashlib.md5(
 f"{tool_name}:{tool_input}".encode()
 ).hexdigest()
 
 # 检查缓存
 if cache_key in self.cache:
 self.cache_hits += 1
 print(f"✅ Cache hit! (命中率: {self.hit_rate:.2%})")
 return self.cache[cache_key]
 
 # 执行工具
 self.cache_misses += 1
 result = self._actual_execute(tool_name, tool_input)
 
 # 存入缓存
 self.cache[cache_key] = result
 return result
 
 @property
 def hit_rate(self):
 total = self.cache_hits + self.cache_misses
 return self.cache_hits / total if total > 0 else 0

## 9.3 成本优化策略

策略1：智能Token管理

Python
class TokenOptimizer:
 def __init__(self, max_tokens=4000):
 self.max_tokens = max_tokens
 def compress_context(self, messages: list) -> list:
 """压缩上下文"""
 total_tokens = sum(len(m["content"].split()) for m in messages)
 if total_tokens <= self.max_tokens:
 return messages
 # 保留最近的和最重要的
 recent_messages = messages[-3:] # 最近3条
 important_messages = self._extract_important(messages[:-3])
 return important_messages + recent_messages
 def _extract_important(self, messages):
 """提取重要消息"""
 # 使用关键词识别重要性
 important_keywords = ["重要", "关键", "必须", "注意"]
 important = []
 for msg in messages:
 if any(kw in msg["content"] for kw in important_keywords):
 important.append(msg)
 return important[:2] # 最多保留2条

策略2：批量处理

Python
def batch_process_with_cost_tracking(tasks, batch_size=10):
 """批量处理并跟踪成本"""
 results = []
 total_cost = 0
 
 for i in range(0, len(tasks), batch_size):
 batch = tasks[i:i+batch_size]
 
 # 批量处理
 batch_prompt = create_batch_prompt(batch)
 response = llm.invoke(batch_prompt)
 
 # 计算成本
 tokens_used = count_tokens(batch_prompt) + count_tokens(response.content)
 batch_cost = calculate_cost(tokens_used)
 total_cost += batch_cost
 
 print(f"批次{i//batch_size + 1}: {len(batch)}个任务, 成本${batch_cost:.4f}")
 
 # 解析结果
 batch_results = parse_batch_response(response.content)
 results.extend(batch_results)
 
 print(f"\n总成本: ${total_cost:.4f}")
 print(f"平均每任务: ${total_cost/len(tasks):.4f}")
 
 return results

## 9.4 可靠性增强

技巧1：重试机制

Python
import time
from functools import wraps

def retry_with_exponential_backoff(
 max_retries=3,
 initial_delay=1,
 exponential_base=2,
):
 """指数退避重试装饰器"""
 def decorator(func):
 @wraps(func)
 def wrapper(*args, **kwargs):
 delay = initial_delay
 
 for attempt in range(max_retries):
 try:
 return func(*args, **kwargs)
 except Exception as e:
 if attempt == max_retries - 1:
 raise
 
 print(f"⚠️ 尝试{attempt+1}失败: {e}")
 print(f"等待{delay}秒后重试...")
 time.sleep(delay)
 delay *= exponential_base
 
 return wrapper
 return decorator

# 使用
@retry_with_exponential_backoff(max_retries=3)
def call_llm(prompt):
 return llm.invoke(prompt)

技巧2：健康检查

Python
class AgentHealthMonitor:
 def init(self):
 self.metrics = {
 "total_requests": 0,
 "successful_requests": 0,
 "failed_requests": 0,
 "total_latency": 0,
 }
 
 def record_request(self, success: bool, latency: float):
 self.metrics["total_requests"] += 1
 self.metrics["total_latency"] += latency
 
 if success:
 self.metrics["successful_requests"] += 1
 else:
 self.metrics["failed_requests"] += 1
 
 def get_health_status(self):
 total = self.metrics["total_requests"]
 if total == 0:
 return "UNKNOWN"
 
 success_rate = self.metrics["successful_requests"] / total
 avg_latency = self.metrics["total_latency"] / total
 
 if success_rate >= 0.95 and avg_latency < 2:
 return "HEALTHY"
 elif success_rate >= 0.8:
 return "DEGRADED"
 else:
 return "UNHEALTHY"
 
 def get_report(self):
 total = self.metrics["total_requests"]
 if total == 0:
 return "暂无数据"
 
 return f"""
健康状态：{self.get_health_status()}

统计信息：
- 总请求数：{total}
- 成功率：{self.metrics["successful_requests"]/total:.2%}
- 平均延迟：{self.metrics["total_latency"]/total:.2f}秒
"""

## 9.5 调试与监控

调试技巧

Python
class DebugAgent:
 def init(self, agent, debug_mode=True):
 self.agent = agent
 self.debug_mode = debug_mode
 self.execution_log = []
 
 def execute(self, task):
 if self.debug_mode:
 print("\n" + "="*50)
 print("🔍 调试模式")
 print("="*50)
 print(f"任务：{task}\n")
 
 start_time = time.time()
 
 try:
 # 记录每一步
 result = self._execute_with_logging(task)
 
 if self.debug_mode:
 self._print_execution_summary(time.time() - start_time)
 
 return result
 
 except Exception as e:
 if self.debug_mode:
 self._print_error_details(e)
 raise
 
 def _execute_with_logging(self, task):
 # 钩子：记录每次工具调用
 original_tool_call = self.agent.tool_executor.call
 
 def logged_tool_call(tool_name, tool_input):
 self.execution_log.append({
 "type": "tool_call",
 "tool": tool_name,
 "input": tool_input,
 "timestamp": time.time(),
 })
 
 result = original_tool_call(tool_name, tool_input)
 
 self.execution_log.append({
 "type": "tool_result",
 "tool": tool_name,
 "result": result,
 "timestamp": time.time(),
 })
 
 if self.debug_mode:
 print(f"\n🔧 工具调用：{tool_name}")
 print(f"输入：{tool_input}")
 print(f"输出：{result[:100]}...")
 
 return result
 
 self.agent.tool_executor.call = logged_tool_call
 
 return self.agent.execute(task)
 
 def _print_execution_summary(self, duration):
 print("\n" + "="*50)
 print("📊 执行总结")
 print("="*50)
 print(f"总耗时：{duration:.2f}秒")
 print(f"工具调用次数：{len([l for l in self.execution_log if l['type']=='tool_call'])}")
 print(f"执行步骤：{len(self.execution_log)}")
