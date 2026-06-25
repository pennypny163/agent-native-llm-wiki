---

source_id: juliet-llm

source_file: "居丽叶LLM体系知识搭建.docx"

source_section: "4 Agent篇"

generated: true

---



# 4 Agent篇

## 4.1 Agent 概述

大模型存在的固有问题： 无法主动更新自己的知识，导致出现事实幻觉 。RAG可以一定程度上缓解这个问题，让大模型先在本地知识库中进行搜索，检查一下提示中的信息的真实性，如果真实，再进行输出；如果不真实，则进行修正。但如果本地知识库找不到相应的信息，就应该调用工具进行外部搜索，这就需要使用 Agent（Agent 能调用的工具不止外部搜索，还包括数学工具、编程工具等等）。

Agent （智能体）是一种能够自主决策、采取行动以达到某种目标的实体。在人工智能领域，Agent 是基于大模型技术构建的智能实体， 能够感知和理解环境，并采取行动以完成特定任务 。

从结构上来说，一个Agent包括三个部分，如下图所示：

Perception（输入）： Agent通过文字输入、传感器、摄像头、麦克风等等，建立起对外部世界或环境的感知。

Brain（大脑）： 大脑是Agent最重要的部分，包括信息存储、记忆、知识库、规划决策系统。

Action（行动）： 基于Brain给出的决策进行下一步行动，对于Agent来说，行动主要包括对外部工具的API 调用，或者对物理控制组件的信号输出。

![原文图片](assets/47739667e178.png)

从功能的角度来看，Agent 就像一个多功能的接口，它能够接触并使用一套工具。根据用户的输入，Agent会规划出一条解决用户问题的路线，决定其中需要调用哪些工具，并调用这些工具。 Agent = 大语言模型+规划+记忆+工具使用 ，具备以下关键能力：

规划（Planning） ：最核心最关键的部分，负责 拆解复杂任务为可执行的子任务 ，并规划执行任务的流程。同时Agent还会对任务执行的过程进行思考和反思，决定是否继续执行任务，并 改进决策策略 。

任务分解 ：将复杂任务分解为可执行的子任务，让大模型逐步解决，例如将订外卖分解为选择餐厅+选择菜品两步。关键技术例如CoT、LLM+P等。

反思 ：Agent 通过完善过去的行动决策和纠正以前的错误来不断改进。关键技术例如React、Reflexion等。

记忆（Memory） ：包括短期记忆和长期记忆，用于存储会话上下文和业务数据等信息，来优化未来行为。

短时记忆 ：即上下文学习， 由于受到Transformer上下文窗口长度的限制，它是短暂的和有限的 。

长期记忆 ：则可对应为 外部的向量数据存储 ，Agent 可在查询时引用，并可通过快速检索进行访问。

工具使用（Tools） ：通过调用外部工具（如API、插件）扩展Agent的能力，如 文档解析、代码编译 等。

![原文图片](assets/c736478b339b.png)

Agent开发框架概览

低代码框架： 无需代码就能在线完成Agent开发，

扣子coze（字节）： https://www.coze.cn

通义千问（阿里）： https://tongyi.aliyun.com/qianw en

文心智能体（百度）： https://agents.baidu.com/center

元器智能体（腾讯）： https://yuanqi.tencent.com/agent-shop

Dify: https://dify.ai/zh

Fastgpt: https://fastgpt.cn

基础框架 ：利用大模型原生能力进行Agent开发

function calling： https://platform.openai.com/docs/guides/function-calling

代码框架 ：

Langchain： https://www.langchain.com/

LangGraph： https://langchain.ac.cn/langgraph

LlamaIndex： https://docs.llamaindex.ai/en/stable/

多智能体框架 ：

CrewAI： https://www.crewai.com/

Swarm： https://github.com/openai/swarm

MegaGPT： https://github.com/openai/swarm

开放式问题：谈谈你对Agent的理解 ？

这个问题准确来说，应该是谈谈你对基于大模型的Agent的理解（之前在介绍强化学习时，也有Agent的概念，本章中讲的Agent特指基于LLM的Agent）。

在Agent诞生之前，有两种方式能使机器智能化：

基于规则的方法 ：将 人类指令转化成机器能理解的规则符号 ，这需要有丰富经验的人类专家，并且容错很低。

基于强化学习的方法 ：构建策略模型和奖励模型， 需要大量的数据进行训练 。

随着大模型的诞生，人类利用其在逻辑推理、工具应用、策略规划等方面的能力，构建以大模型为核心的Agent系统，极大的提升了机器的智能化程度。当然，为了进一步提升Agent的性能，还提出了CoT等规划方法、引入记忆和工具模块，使得Agent越来越 逼近人类的思考方式 。

从人机合作的角度出发，Agent 改变了人机合作的方式。截至现在，主要有三种模式：

人类主导 ：代表是 SaaS+AI模式 ，人类完成大多数工作，而AI只负责完成特定任务。例如AI只负责实现人脸识别、OCR等能力，嵌入到人类操作的SaaS软件中，其他功能AI不参与。

AI作为人类助手 ：代表是 Copilot模式 ，AI可以随时辅助人类完成各种任务，不再局限于特定的功能。

AI主导 ：代表 Agent模式 ，人类只负责提出需求，在AI负责完成的过程中，可能需要人类进行进一步的描述需求、点评AI生成内容质量、矫正AI理解等。而Agent正式通往AGI（Artificial General Intelligence）的必经之路。

| 对比维度 | 传统对话式 AI | 基于 LLM 的 AI Agent |
| --- | --- | --- |
| 交互方式 | 单轮或有限多轮对话 | 支持多轮交互，任务持续性强 |
| 能力边界 | 仅限于预设回复、有限理解 | 可动态调用工具，灵活执行复杂任务 |
| 知识更新 | 静态（训练时固定） | 可实时联网，获取最新信息 |
| 执行复杂任务能力 | 很弱 | 强，支持规划、执行、反馈、修正的闭环流程 |

## 4.2 Agent 分类

按照工作模型可以分为单Agent、多Agent和混合Agent三种。

单Agent ：

特点 ： 由一个独立的智能体构成 ，所有的决策和执行都集中在一个智能体上，没有与其他智能体的协调和通信需求，适用于单一任务或相对简单的任务。

优点 ： 不需要处理多个智能体之间的协调问题，也不需要额外的资源来管理多个智能体 。

缺点 ：难以处理复杂、多变的环境， 并且如果Agent出现故障，整个系统都将瘫痪 。

应用场景 ：比如专门用于进行市场分析调研的Agent。

多Agent ：

定义 ： 多个Agent协同工作 ，相互交流信息，共同完成更复杂的任务或目标。多个智能体在分布式环境中独立运行，每个智能体可以自主决策，需要处理智能体之间的通信、协调和竞争等问题。

优点 ： 能够处理复杂、动态和多变的环境 ，可以完成单个智能体难以完成的任务。多个智能体之间可以相互协作，即使部分智能体出现故障系统仍然可以正常工作， 鲁棒性强 。能根据环境和任务需求动态调整，具有 可拓展性。

缺点 ： 需要大量的通信和协调 来确保智能体之间的同步和协作。

应用场景 ：比如一家公司就可以视为一个多Agent系统，由Agent来扮演产品经理、UI设计师、研发工程师、测试人员、项目经理等角色。

例子 ：斯坦福小镇

混合Agent：

定义 ： Agent系统和人类共同参与决策过程 ，交互合作完成任务，强调的是人机协作的重要性和互补性。这种系统通常包含一个或多个智能体，以及与人类用户的交互接口。

优点 ：通过人类的参与，混合Agent系统可以更好地处理复杂和多变的任务，提高任务完成的质量和效率， 灵活地调整人类和智能体的角色和任务分配 ，提供更个性化和人性化的服务。

缺点 ：开发难度和复杂度较高。

应用场景： 医生和Agent可以共同进行病情诊断，Agent负责快速分析病人的医疗记录、影像资料等，提供初步的诊断建议；而医生则可以基于Agent的分析结果和自己的专业知识和经验，做出最终的诊断决定。

## 4.3 Planning

智能体会把大型任务 分解为子任务 ，并规划执行任务的流程；智能体会对任务执行的过程进行 思考和反思 ，从而决定是继续执行任务，或判断任务完结并终止运行。目前Agent大部分的planning逻辑，是通过提示词（ prompt ），手动告诉 LLM 它该怎么思考、怎么分步执行的。 实际系统里常常先通过 人工/程序硬编码 固定主干流程以及有严格要求的核心业务，再在需要模型能力的节点中（例如创新、总结、标注、推理等任务），通过 Prompt 来让模型做局部规划或执行，从而在灵活和可控之间找到平衡 。

Prompt 更像“指导”或“原则” ，让模型在这些原则内自由思考、制定和执行流程，适合需要 灵活应变 、 创造性 或 自动化 程度高的场景。

人工/程序硬编码的流程 ，适合高度 可控、可预测、合规、安全 的任务；这些场景往往我们不希望模型自由发挥。

举个例子，比如在电商系统中，身份信息验证不能出错，售后政策有明确规定，这些都适合人工编码。而智能客服则可以通过prompt指导LLM来进行回复。

什么时候用 Prompt 让 LLM 来决定或规划

需要模型自行推理或发挥创造力时

问题不确定、场景复杂 ：例如，你需要一个解决方案，但并不清楚最佳方案是什么，需要模型自己做大量推断。

希望模型能灵活应对多变场景 ：场景可能临时发生变化，或者问题本身没有“标准化”的解决流程；这时借助 LLM 自主推理和生成方案更高效。

需要模型产生更多可能性 ：尤其在创意、撰写文案、构思初稿等需要发散思维的任务中，你希望模型做不同尝试、给出多种备选方案。

人力成本/维护成本高

不要人为写死过多逻辑 ：有时业务频繁变化，如果完全硬编码，会导致需要经常改程序。通过 Prompt 动态让模型来生成、优化策略或流程，可减少手动维护的成本。

辅助决策或自动化

你只需要告诉模型“目标”或“限制条件”，让模型自己“分解”并“规划”下一步操作，而非固定给出所有步骤。

什么时候要用人为定义/硬编码

流程固定，可控性要求高

强流程化/标准化 ：如某些业务流程、法务流程、风控流程等，规定必须走固定的若干步骤、检查点。例如KYC（实名认证）等合规步骤，这种就适合在业务代码里“写死”或严格定义。

合规或安全要求高 ：不能容忍模型输出违反规定的内容；需要可解释、可审计。人工定义好的流程更可控，审计上也更简单。

不需要太多“模型推理”

简单稳定的逻辑 ：比如根据用户选择，进入下一个固定页面或固定问答，不需要模型判断或发挥创造力。手动硬编码更加直接、高效。

高准确度要求 + 可预期 ：有些核心业务关键性很高（例如金融交易的步骤），一旦出错会造成损失，这时往往宁可牺牲灵活度，也要保证流程的绝对稳定和可验证。

需要结合大量外部系统或特定算法

与数据库、API 或传统程序强绑定 ：如果中间步骤牵涉到很多传统逻辑（比如数据库查询、多层调用），而这些逻辑又必须严格按某个顺序走，这种更适合在编程逻辑里“定死”流程，而不是让模型自由调度。

将人为定义和LLM规划相结合

实际系统里常常“先在人为代码中固定主干流程”，再在需要模型能力的节点中，通过 Prompt 来让模型做局部规划或执行，从而在灵活和可控之间找到平衡。

大框架“定死”，关键节点用 Prompt ：先用人工代码或流程图固定好业务主流程，在需要创造力或不确定性强的地方，让模型根据 Prompt 来规划或填充内容。

在 Prompt 中嵌入关键信息和限制条件 ：比如你可以在 Prompt 里告诉模型“这里要先检查一下输入是否合法，否则直接返回失败”，再让模型自己决定在什么条件下执行具体动作。

LLM 生成“初步规划”，再由人工/代码做校验或修订 ：例如让模型生成一个方案，然后可以通过代码或人工来审核它，如果不符合要求，再让模型重新迭代或直接由人来修正最终执行流程。

一些关键考量点

是否允许模型发挥主观创造力或灵活应对

如果需要，倾向于多用 Prompt，让 LLM 自行规划。

如果不行（必须“100% 按照规定”），就多在程序里硬编码。

可控性 / 风险承受度

重要环节、合规要求极高场景 → 人工+程序严格定义

容错度高或创新、探索场景 → 让模型自由生成

维护成本

需求变化频繁，需要经常改 → 用 Prompt 可能更灵活

需求相对稳定 → 硬编码也没问题

可解释性 / 审计要求

模型生成的内容难以完全审计或解释 → 重要核心部分需人工定义

非关键部分，可以让 LLM 去生成

总结

固定 & 硬编码 ：

常见于需要 高可控性、固定逻辑 或 合规要求 的部分，或对 数据处理、权限管理 、 业务规则 等有严格要求的场景。

其优势是：结果可预期、容易审计、维护简单。

劣势是：缺乏灵活性，不易处理未知变化或新需求。

Prompt & LLM ：

适合对 自然语言处理 、 创造性或不确定性 较高的任务，或 需要做推理/归纳/总结 时。

优势是：可以减少人工或传统编程的复杂度，快速给出多种方案或文案，能适应变化的场景。

劣势是：输出可能有不确定性，需要一定的验证或控制策略。

### 4.3.1 基础方法

CoT

思维链 将复杂的问题分解为更简单的任务 ，逐步解决问题，使用CoT能在算数、常识和推理任务都提高了性能。但这会增加推理的时间。CoT可以分为Few-Shot 和Zero-Shot（Zero-Shot 只需要在prompt中加入“让我们一步步的思考”）两种。使用Langchain可以轻松的实现CoT：

Python
# 创建聊天模型
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0)
# 设定 AI 的角色和目标
role_template = "你是一个xx工作的AI助手,目标是xx"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template = """
请你按部就班的思考，先理解用户需求，再进行信息检索，再做出决策
一些示例:xx
"""
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template)

# 用户的询问
human_template = "{human_input}"
human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# 将以上所有信息结合为一个聊天提示
chat_prompt = ChatPromptTemplate.from_messages([system_prompt_role, system_prompt_cot, human_prompt])
prompt = chat_prompt.format_prompt(human_input="xx").to_messages()

# 接收用户的询问，返回回答结果
response = llm(prompt)
print(response)

ToT

在需要多步骤推理的任务中，引导语言模型搜索一棵由连贯的语言序列（解决问题的中间步骤）组成的思维树，而不是简单地生成一个答案。ToT框架的核心思想是： 让模型生成和评估其思维的能力 ，并将其与 搜索算法 （如广度优先搜索和深度优先搜索）结合起来，进行系统性地探索和验证。 对于每个任务，将其分解为多个步骤，为每个步骤提出多个方案，在多条思维路径中搜寻最优的方案。

![原文图片](assets/40389d83e9fe.png)

LLM+P

大型语言模型 不擅长解决长期规划问题 。相反，一旦以一种规范的方式给出问题，传统的规划方法就能够运用有效的搜索算法快速找到正确的，甚至是最优的解决方案。LLM+P把这两者的优势结合起来，接收一个用自然语言描述的规划问题，将语言描述转化为一个用 规划领域定义语言（PDDL） 编写的文件，然后利用传统规划方法快速找到解决方案，最后将找到的解决方案翻译回自然语言。

PDDL包含领域定义和问题定义两部分：

领域定义 ：描述可能的动作、动作前提条件、和导致结果。

问题定义 ：描述一个具体的规划问题，包含初始状态和目标状态

![原文图片](assets/79f8f46fd2e0.png)

ReAct

ReAct: Synergizing Reasoning and Acting in Language Models （不是前端哪个react框架）。其实现了 “行动”和“推理”之间的协同作用 ，使得大模型能够作为智能代理， 生成推理痕迹和任务特定行动来实现更大的协同作用 。

ReAct的任务解决轨迹是 Thought-Action-Observation ， 可以简化为模型按照 Reasoning-Acting 框架。 Reasoning包括了对当前环境和状态的观察，并生成推理轨迹 。这使模型能够诱导、跟踪和更新操作计划，甚至处理异常情况。ReAct的每一个推理过程都会被详细记录在案，这也改善大模型解决问题时的可解释性和可信度； Acting在于指导大模型采取下一步的行动 ，比如与外部源（如知识库或环境）进行交互并且收集信息，或者给出最终答案。

与仅仅使用CoT不同的是，这会导致模型存在幻觉，没有与外部工具交互的功能。而将ReAct框架与CoT结合，就能够 让大模型在推理过程同时使用内部知识和获取到的外部信息 ，提升模型的可解释性和可信度。

![原文图片](assets/048b99883da2.png)

langchain实现了ReAct框架：

Python
llm = ChatOpenAI(model=os.environ["LLM_MODELEND"], temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(
 tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run(prompt)

React+CoT的训练流程如下，注意之前每轮的输出会加入prompt作为后续轮次模型的输入。

![原文图片](assets/f33a69997c6d.png)

总结以上算法：

| 算法 | 结构特点 | 核心优势 | 主要局限 | 典型场景 |
| --- | --- | --- | --- | --- |
| CoT | 线性分步推理 | 可解释性强，适用广泛 | 单一路径，计算成本高 | 数学推理、代码生成 |
| ToT | 树状多路径搜索 | 多方案探索，动态调整 | 复杂度高，实现难度大 | 开放域问题、复杂规划 |
| LLM+P | 符号逻辑结合 | 严格约束处理，可验证 | 依赖预定义规则，泛化弱 | 结构化流程、合规检查 |
| ReAct | 推理-行动循环 | 动态交互，工具扩展性 | 工具依赖性，步骤冗余 | 实时交互、工具调用任务 |

### 4.3.2 规划

ReWoo

ReAct 提示词结构是 Thought→ Action→ Observation, React每一轮思考都要将之前所有的响应加入prompt，会消耗大量的token 。ReWoo将推理过程与外部观察分离，将 Observation 隐式地嵌入到下一步的执行单元中了，即由 下一步骤的执行器自动去 observe 上一步执行器的输出 ，从而显著减少了token消耗。

ReWoo包含三个部分：

Planner负责 将用户问题分解为子任务并确定执行顺序 ，每个子任务都分配给Worker；

Worker 利用工具检索外部知识 提供证据；

Solver负责综合所有任务和证据， 生成最终答案 。

![原文图片](assets/508528b89972.png)

如下图所示，React每一轮的都要将上下文、示例和之前轮次的相应输入到LLM中，带来大量的冗余，并且可能需要调用LLM很多次； ReWoo中Planner负责生成一个子任务列表，并调用Worker从工具中获取证据，根据列表循环执行完成任务，避免了将prompt中一样的内容反复交给LLM ，这个过程只调用了 两次LLM（Planner和Solver各一次） 。ReWoo的另一个优点是简化微调过程，由于Planner不依赖于工具的输出，因此可以在不实际调用工具的情况下对Planner进行微调。

![原文图片](assets/9c3fbc96f1ef.png)

Plan and solve

这个方法在 零样本思维链 的基础上进行优化。Zero-shot-CoT知识简单的在prompt中加入“让我们逐步思考”，面临着 计算错误、缺失步骤错误和语义误解错误 等三个问题。Plan and solve解决了缺失步骤错误，先制定计划将任务分解为子任务，再按照计划执行子任务。

这个方法整体感觉偏向提示工程。prompt应该满足以下条件：

引导LLMs确定子任务并完成这些子任务,

指导LLMs更加关注计算和中间结果，并尽可能确保它们的正确执行 。

最终的prompt格式为：“Q: [X]. A: Let’s first understand the problem，extract relevant variables and their corresponding numerals, and devise a plan.Then let's carryout the plan, calculate intermediate results(pay attention to calculation and common sense), solve the problem step by step, and show the answer.”

Plan-and-solve的思想的一大应用就是Plan-and-Execute。Plan-and-Execute相比ReWOO，最大的不同就是加入了 Replan 机制，整体的思考流程如下图。Planner负责生成任务列表， replanner负责当完成一个子任务时进行重新思考 ，并将原有计划和已经完成的步骤加入prompt中，更新任务列表。

![原文图片](assets/bda2bf89f757.jpeg)

LLMCompiler

这个方法的主要思想是通过 并行function call来提高效率 ，比如询问微软的市值需要增长多少才能超过苹果的市值，可以并行的查询微软市值和苹果市值。主要包含4个模块：

函数调用规划器 ：负责理解用户输入， 拆分成可执行的子任务，并确定它们之间的依赖关系，形成任务依赖的有向无环图（DAG） 。该部分需要用到大模型， 最好用户为规划器提供一些上下文示例 。

任务获取单元 ：根据 贪婪策略 ，将可以执行的任务发给执行器， 并用执行后的输出替换后续任务的占位符 。无需LLM

执行器 ：多个执行器 并发执行 ，可以调用用户提供的工具。

动态重规划 ：对于复杂的任务，可能需要 根据中间结果进行重新规划，由函数调用规划器生成新的子任务和它们之间的依赖关系。

函数调用规划器负责生成一个 包含任务及其相互依赖关系的 DAG(有向无环图) 。然后，任务获取单元根据任务的依赖关系将这些任务并行调度到执行器。在本例中 ，任务 $1 和 $2 被同时获取，以并行执行两个独立的搜索任务 。每个任务执行完成后，结果将被转发给任务获取单元， 用实际值替换其占位符变量，同时解除被依赖任务的阻塞（例如，任务 $3 中依赖 $1 和 $2） 。所有任务执行完成后，最终答案将被传递给用户。

![原文图片](assets/8b66af04dcf3.png)

![原文图片](assets/027f963deb01.png)

总结以上的方法：

| 特性 | ReWOO | Plan & Solve | LLMCompiler |
| --- | --- | --- | --- |
| 原理 | 将推理过程与使用外部工具的过程分离，通过规划器生成一次性使用的完整工具链，然后由执行器调用工具获取证据，最后由合并器整合证据形成最终答案。 | 先由规划器生成一个多步计划来完成一个大任务，然后由执行器根据计划调用工具完成任务，过程中可以根据任务的完成情况进行重新规划。 | 将输入查询翻译成一系列具有相互依赖关系的任务，并通过并行函数调用来提高推理效率。 |
| 核心目标 | 减少Token消耗，提升鲁棒性 | 动态调整计划，增强容错性 | 并行执行任务，提升效率 |
| LLM调用次数 | 2次（Planner + Solver） | 多次（Planner + Replanner） | 多次（Planner + Joiner） |
| 执行方式 | 串行执行任务 | 串行执行 + 动态重规划 | 并行执行DAG任务 |
| 适用场景 | 工具调用稳定、需低Token消耗的任务 | 适用于需要详细规划和执行的任务场景，擅长处理复杂动态环境下的长周期任务 | 适用于需要高效推理和处理大量任务的场景 |
| 主要缺点 | 非常依赖于规划器的规划能力，如果规划有误，则后续所有的执行都会出现错误，对于复杂任务，很难在初始阶段就制定合理且完备的计划清单 | 规划和执行过程可能较为复杂，需要较多的计算资源和时间；对规划器的性能要求较高。 | 对任务的依赖关系处理较为复杂，需要精心设计任务的并行执行策略；对模型的性能和资源要求较高。 |

### 4.3.3 反思

Reflexion

Reflexion 采用了强化学习的方法， Reflexion代理在生成每一个轨迹后，进行 启发式评估 ，生成 反思文本 并保留在记忆缓冲区中，以诱导在随后的尝试中做出更好的决策 。首先介绍基本概念：

启发式函数： 用于确定轨迹是否效率低下或包含幻觉应当停止。

效率低下 ： 长时间未成功完成的轨迹 。

幻觉 ：定义为 一系列连续相同的行动 ，这些行动导致在环境中观察到相同的结果。

Reflexion包含三个不同的模型：

执行者 （Actor）用 【公式开始】M_a 【公式结束】 表示，它 生成文本和动作 。利用llm根据状态观察生成文本和动作，采用类似 强化学习 的设置，从策略采样行动，并从环境接受观察，生成轨迹，可以采用React框架。

评估者模型 （Evaluator），由 【公式开始】M_e 【公式结束】 表示，它对 【公式开始】M_a 【公式结束】 产生的输出进行打分， 评估行动的价值 ，将轨迹作为输入，计算奖励分数。

自我反思模型 （Self-Reflection model），用 【公式开始】M_{sr} 【公式结束】 表示，它协助执行者自我提升。 通过生成 自我反思来为未来的尝试提供有价值的反馈，存储到记忆中。 Memory 存储短期记忆和长期记忆。在推理时，Actor根据短期和长期记忆做出决策， 轨迹历史作为短期记忆 ，而 Self-Reflection模型的输出则存储在长期记忆中 。

在提示词方面，要求让大模型针对问题在回答前进行反思和批判性思考，反思包括 有没有漏掉(missing)或者重复(Superfluous) ，然后回答问题，回答之后再有针对性的 修改(Revise)

![原文图片](assets/83cc72f2412d.png)

Self DisCover

Self-discover 的核心是让大模型 在更小粒度上 task 本身进行反思 ，比如前文中的 Plan&Slove 是反思 task 是不是需要补充，而 Self-discover 是对 task 本身进行反思。

本方法主要分为两个阶段： 利用SELF-DISCOVER 构建了 任务特定的推理结构 ， 应用推理结构解决问题 。其中第一步又可以分为以下三个操作：

![原文图片](assets/7972ee43a023.jpeg)

选择 ：模型从一组 原子推理模块 （例如“批判性思维”和“逐步思考”） 中选择对于解决特定任务有用的模块。模型通过一个元提示来引导选择过程，这个元提示结合了任务示例和原子模块描述。 选择过程的目标是确定哪些推理模块对于解决任务是有助的。

适应 ：一旦选定了相关的推理模块，下一步是调整这些模块的描述使其更适合当前任务。这个过程将一般性的推理模块描述， 转化为更具体的任务相关描述 。 例如对于算术问题，“分解问题”的模块可能被调整为“按顺序计算每个算术操作” 。同样， 这个过程使用元提示和模型来生成适应任务的推理模块描述 。

实施 ：在适应了推理模块之后，Self-Discover框架将这些适应后的推理模块描述转化为一个 结构化的可执行计划 。这个计划以键值对的形式呈现，类似于JSON，以便于模型理解和执行。这个过程不仅包括元提示， 还包括一个人类编写的推理结构示例，帮助模型更好地将自然语言转化为结构化的推理计划 。

![原文图片](assets/979d633414a7.jpeg)

LATS

LATS算法《Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models》融合了 ToT、React、Plan&solve、Reflection和强化学习 等思想，作为对以上算法的总结。

预备知识

给定自然语言x和y，模型 【公式开始】p_\theta(x) 【公式结束】 的任务是推理出最接近y的答案，通常prompt和x一起作为输入，生成过程可以表示为 【公式开始】y = p_\theta(prompt_{IO}(x)) 【公式结束】 。

React框架引入了外部环境的交互，定 义行动空间 【公式开始】a \in A 【公式结束】 和 CoT的推理路径 【公式开始】z \in Z 【公式结束】 ，将两者合并为最后的行动空间 【公式开始】\hat{A} = A ∪ Z 【公式结束】 ，外部环境的观察定义为o。给定观察o，下一个行动的生成表示为

![原文图片](assets/b06695c0f159.jpeg)

CoT、ToT和React框架面临着以下问题：1） CoT和React的自回归训练会忽略特定状态的潜在连续名词 2） CoT和ToT只依赖LLM自有的能力，可能造成幻觉 。3） 以上方法无法利用过去的经验 。

蒙特卡洛树搜索 是一种决策树算法， 树的结点表示状态，边表示行动 。从初始状态根节点出发，每轮训练包含2个步骤：1） 从当前状态p中探索多个子状态s，并采样n个动作 。2）采取 上致信度（UCT） 最高的动作，定义为：

![原文图片](assets/7279d4252ade.jpeg)

V(s)表示节点s的期望value，N(s)表示访问节点s的次数，w是权重参数。 当一个episode结束时，进行反向传播 ，用奖励r更新路径上的每个节点的value值：

![原文图片](assets/b863fce907f5.jpeg)

LATS方法

本文提出的LATS遵循 React 框架的Thought-Action-Observation流程，参照 蒙特卡洛树 ， 每轮采样n个行动产生多个轨迹，以克服LLM的随机性并扩大探索域，从而找到最优轨迹。

LATS包含以下图中的6个步骤，并循环迭代，直到采样了k个轨迹后任务完成或者计算资源限制。其中 【公式开始】p_\theta 【公式结束】 同时作为agent，value function和反馈生成器，充分利用LLM的表征能力。

selection ： 根据蒙特卡洛树选择UCT值最大的下一个节点 。

expansion ： 从当前状态p采样n个行动 ，与环境交互得到n个子节点。

evaluation ：为每个子节点计算value值，参考ToT，通过提示工程 将 【公式开始】p_\theta 【公式结束】 作为一个评估值函数 ，并且这里还引入了环境反馈。还引入了基于 self-consistency 的启发， 认为选择次数更多的action更精确 ：

![原文图片](assets/8625f30ffddb.jpeg)

simulation： 重复之前的过程直到到达终点状态，如果达到最优解就直接结束，反之进行 Backpropagation和reflection。

backpropagation ： 更新蒙特卡洛树中轨迹上的每一个节点 ， 【公式开始】N(s_i) = N(s_{i-1}) + 1, V(s_i) = \frac{V(s_{i-1}N(s_{i-1})) + r}{N(s_i)} 【公式结束】 ，其中r是奖励。

reflection ：通过提示工程，让 【公式开始】p_\theta 【公式结束】 根据轨迹和奖励进行self-relection， 总结推理过程中的错误 ，并选择更好的选项。 将错误的轨迹和relection存储在记忆中 ，在随后的迭代中，这些被加入到agent和value函数的上下文。

![原文图片](assets/3aa7c1cabb38.jpeg)

![原文图片](assets/1e6cef9172c4.jpeg)

| 维度 | Reflexion | Self-Discover | LATS |
| --- | --- | --- | --- |
| 原理 | 由参与者（Actor）、评估者（Evaluator）和自我反思（Self-Reflection）三个部分组成。参与者根据状态观测量生成文本和动作，评估者对参与者的输出进行评价，自我反思模型利用奖励信号、当前轨迹和其持久记忆生成具体且相关的反馈，并存储在记忆组件中。 | Self-discover 的核心是让大模型在更小粒度上对任务本身进行反思，通过 Selector 从众多的反省方式中选择合适的反省方式，Adaptor 使用选择的反省方式进行反省，Implementor 反省后进行重新 Reasoning。 | 融合了 Tree Search、ReAct、Plan & Execute、Reflexion 的能力。它使用蒙特卡罗树搜索（MCTS）算法，通过平衡探索和利用，找到最优决策路径，并结合来自语言模型的反馈，以判断推理中是否存在错误并提出替代方案。 |
| 核心目标 | 通过语言反馈优化试错学习 | 动态构建任务专属推理逻辑 | 多路径搜索与全局优化 |
| 关键技术 | 强化学习、自我反思 | 原子模块选择与适应 | 蒙特卡洛树搜索+强化学习 |
| 适用场景 | 编程、决策等需迭代改进的任务 | 复杂推理任务（如数学问题） | 高复杂度决策任务 |
| 主要缺点 | 长期记忆容量有限 | 依赖预定义推理模块 | 计算资源消耗大 |

介绍两个近期比较火的规划方法：BabyAGI和AutoGPT

BabyAGI 使用一个“ Task List ”来管理所有待办任务。它有三个主要组件：

Task Creation Agent : 根据当前任务、执行结果，不断新建子任务。

Task Prioritization Agent : 对现有任务重新排序，决定执行顺序。

Execution Agent : 真正去执行当前的任务（通常是调用LLM/工具等）。

循环流程

从 “ Task List ” 中取出最高优先级的任务。

调用 Execution Agent 去执行。

把执行结果（Result）交给 Task Creation Agent ，是否需要生成新的子任务？

把更新后的任务列表给 Task Prioritization Agent ，排序并循环。

AutoGPT 也有一个任务/目标管理系统，也能生成子任务并执行。它侧重更丰富的“工具”支持，如联网、读取/写入文件、执行代码等，包含以下模块：

AI Config : 存放 AI 的角色、名称、目标等基础信息。

Memory : 把过去的重要信息存下来，供下一步参考。

Planner （或类似角色）: 生成下一步要干啥。

Command Executor : 解析 LLM 返回的命令，然后在外部执行相应操作。

## 4.4 Memory

正文开始之前先放一个吴恩达老师对Agent的理解图，其中的很多方法已经介绍过了：

任务分解 是指借助LLM 将任务拆解为若干个子任务，并依次对每个子任务进行规划 。可以分为先分解后规划（HuggingGPT，plan and solve）和边分解边规划（COT，react，pal）两个思路

多方案选择 是指大型语言模型深入“思考”， 针对特定任务提出多种可能的方案 。接着，利用针对性的任务搜索机制，从中挑选一个最合适的方案来实施。例如ToT，GoT，LAT

外部模块辅助规划 。该策略专门设计用于 引入外部规划器，以增强规划过程的效率和计划的可行性 ，同时大型语言模型主要负责将任务规范化。分为符号规划器（LLM+P）和神经规划器（利用强化学习训练深度学习模型，作为决策模型）

反思与优化 。这种策略着重于通过 自我反思 和细节完善来增强规划能力。它激励大型语言模型Agent应用在遭遇失败后进行深入反思，并据此优化规划方案。例如Reflexion，critic

记忆增强规划 。该策略通过引入一个附加的记忆组件来提升规划能力，该组件中存储了各种宝贵信息，包括 基本常识、历史经验、领域专业知识等 。 在进行规划时，这些信息会被调取出来，充当辅助提示，以增强规划的效果 。分为RAG记忆（即接下来要介绍的Memory）和嵌入式记忆（将RAG知识通过微调嵌入到模型参数里）

![原文图片](assets/23e23b161b5f.png)

记忆模块是智能体存储内部日志的关键组成部分，负责存储过去的思考、行动、观察以及与用户的互动。

短期记忆 关注于 当前情境的上下文信息 ，是短暂且有限的，通常通过上下文窗口限制的学习实现。

长期记忆 储存智能体的历史行为和思考，通过 外部向量存储 实现，以便快速检索重要信息。

混合记忆 -通过整合短期和长期记忆，不仅优化了智能体对当前情境的理解，还加强了对过去经验的利用，从而提高了其长期推理和经验积累的能力。

长期记忆存储到外部存储器中，最常见的做法是将记忆的embedding存储到支持快速的最大内积搜索（MIPS）的向量存储数据库中。不只是文本，图像、音视频等非结构化数据也可以存储为结构化向量，降低了存储和计算的成本，同时加速了检索效率。

参考： A Survey on the Memory Mechanism of Large Language Model based Agents

### 4.4.1 基本概念

任务 ：agent 要实现的目标 ，例如订一个机票，下面用 【公式开始】\mathcal{T} 【公式结束】 表示一个问题。

环境 ：agent为了完成任务需要与环境交互， 环境包含了可能改变agent决策的上下文信息 。

trail ： agent采取行动，并从环境获得行动的反馈，基于此反馈再采取行动，循环持续直到任务完成，这一过程被称为trail 。一个长度为T的trail可以表示为 【公式开始】ξ_T = {a_1, o_1, ...,.a_T, o_T} 【公式结束】 ，其中 【公式开始】a 和 o 【公式结束】 分别是行动和环境。每一轮agent与环境的交互被称为一个step。 每个任务可能有多个trail，即为了完成一个任务可能做很多尝试。

memory ：狭义上的memory指同一个trail中的历史信息。给定一系列任务 【公式开始】\{\mathcal{T}_1,...,\mathcal{T_k}\} 【公式结束】 ，对于任务 【公式开始】\mathcal{T_k} 【公式结束】 在第t步时，广义的memory来自3个方面：

| 1）同一个trail之前的历史信息，记为：<br>2）任务k之前的任务的trail，以及任务k之前尝试的trail（记为k'）：<br>3）外部知识，比如通过RAG查询到的知识，表示为： | 【公式开始】D_t^k 【公式结束】 |
| --- | --- |
|  |  |

### 4.4.2 Memory-based agent

agent在与环境交互的过程可以分为3个阶段。

1） 智能体从环境中感知信息，并将其存储到记忆中 。

2） 智能体对存储的信息进行处理，使其更加可用 ；

3） 智能体根据处理后的记忆信息采取下一步行动 。

对应了三个agent memory的三个操作：

写记忆： 此操作旨在 将从环境的原始观察结果投射到实际存储的记忆内容中 ，这些内容更具信息量和简洁。这一操作可以表示为 【公式开始】m_t^k = W(\{ a_t^k, o_t^k \}) 【公式结束】 ，W表示映射函数， 【公式开始】m_t^k 【公式结束】 是最终写入memory的内容，可以以自然语言的形式或者参数化的形式。

记忆管理： 使得记忆信息更加高效，例如 总结高级的概括性概念以使得agent更具有泛化性，合并相似信息以降低冗余性，忘记不重要信息避免造成负面影响 。这一操作表示为 【公式开始】M_t^k = P(M_{t-1}^k, m_t^k) 【公式结束】 ， 【公式开始】m_t^k 【公式结束】 是第t轮的记忆， 【公式开始】M_{t-1}^k 【公式结束】 表示之前处理过的记忆，P是迭代处理存储的记忆信息的函数。对于广义的记忆， 这一操作会跨trail跨任务执行，并且会随着外部知识的变化而执行。

读记忆： 从memory获取信息以采取下一次行动 ， 【公式开始】\hat{M_t^k} = R(M_t^k, c_{t+1}^k) 【公式结束】 ， 【公式开始】c_{t+1}^k 【公式结束】 表示下一个行动的上下文，R是计算相似度的函数， 【公式开始】\hat{M_t^k} 【公式结束】 表示计算得到的最相似的记忆内容，会被加入下一轮agent的prompt中。

基于以上操作，就可以得到agent做决策的统一表示，下图展示了agent完成一个任务的工作流程。

![原文图片](assets/a7187ff90456.jpeg)

![原文图片](assets/e5d97017ec46.jpeg)

为什么要使用Memory-based agent

从认知心理学角度 ：对于人类的认知来说，记忆重要的模块，agent想要替代人类完成一些任务，就要 表现的像人类 ，为agent设置代理模块。

从自我进化角度 ：在完成任务的过程中， agent也需要在与环境交互时自我进化 。记忆能帮助agent积累经验、探索更多的环境、抽象出概括性信息以增强泛化性。

从agent应用角度 ： 在很多应用中记忆是不可取代的 ，例如chatgpt、虚拟角色。

### 4.4.3 如何实现Memory-based agent

![原文图片](assets/46758c367e36.png)

记忆来源

如之前介绍的，memory来源主要包含3部分： 同一个trial ， 跨trail跨任务 ， 外部知识 。前两部分都来自agent与环境交互，外部知识来自任务以外的环境。代表工作有这些：

![原文图片](assets/f224829d68b4.png)

同一个trial ： 同一个trial中的历史步骤是最相关最有信息量的信息，与agent的任务高度相关 。这部分信息不仅包括代理环境交互，还包含交互上下文，例如时间和位置信息。

跨trial跨任务 ：在环境中多次试验所积累的信息也是记忆的重要组成部分，通 常包括成功和失败的操作及其见解，例如失败的原因、成功的常见行动模式等 ，基于过去的经验，agent可以根据整个过程的整体反馈调整其行为。代表工作是Planning篇介绍的Reflexion。 同一个trial的可以视为短期记忆，跨trial跨任务的则是长期记忆。

外部知识 ： 根据任务需求实时动态访问各种工具的 API 来获取 ，例如搜索维基百科，扩展agent的知识边界。代表工作是Planning篇介绍的React。

记忆形式

记忆一般有两种形式： 文本和参数化形式 。代表工作有这些：

![原文图片](assets/8a99d65004b3.png)

文本形式 是目前表示记忆内容的主流方法，具有可解释性更好、更容易实现、读写效率更快的特点。过去的研究主要分为4个方向：

（1） 完整的agent-环境交互： 计算成本和推理时间都会大幅增加，并且推理容易不鲁棒，因为文本在长上下文中的位置会极大地影响它们的利用率 ，长上下文提示中的记忆不能得到平等和稳定的处理。

（2） 最近的agent-环境交互： 会遗忘遥远的记忆，对于长期任务可能导致关键信息缺失，并且如何确定缓存窗口也比较困难 。

（3） 检索到的agent-环境交互： 根据记忆内容的相关性进行检索，在记忆读取时，会 为每个记忆条目计算匹配分数，并选取 top-K 条目 。在记忆写入时生成embedding作为记忆的索引，以辅助信息检索。检索需要额外的计算成本。

（4） 外部知识： 通过 调用工具获取外部知识（如维基百科） ，可能会涉及检索、重排等多个计算过程，如何将外部知识和内部决策过程融合值得研究。

参数化形式 的记忆存储在模型的参数中，不受 LLM 上下文长度限制的限制。现有方法主要分为两类：微调方法和记忆编辑方法。

（1）微调方法： 通过有监督微调将外部知识整合到代理的记忆中，能显著提升模型在特定领域的能力 。只能应用在离线场景。面临着微调通用的问题，灾难性遗忘，过拟合，需要大量数据，计算成本高等。

（2）记忆编辑方法： 直接修改Transformer模型的权重, 以实现对模型记忆的精确编辑。记忆编辑只针对需要修改的事实，更适合小规模的记忆调整，适合在线场景。

对比文本形式记忆和参数化形式记忆：

有效性： 文本记忆存储有关agent与环境交互的原始信息 ，这些信息更全面、更详细。然而，它 受到 prompt中token上限的限制 ，这使得agent难以存储大量信息。相比之下， 参数记忆不受提示长度的限制 ， 但在将文本转换为参数时可能会遭受信息丢失 ，复杂的记忆训练会带来额外的挑战。

效率： 对于文本记忆，每次 LLM 推理都需要将记忆整合到上下文提示中，这会导致 更高的成本和更长的处理时间 。相比之下，对于参数记忆，信息可以集成到 LLM 的参数中，从而消除了这些上下文的额外成本。然而， 将参数记忆写入模型的需要额外的成本 ，但文本记忆更容易写作，尤其是对于少量数据。简而言之， 文本记忆在写作方面更有效率，而参数记忆在阅读方面更有效率。

可解释性： 文本记忆通常比参数记忆更易于解释 ，因为自然语言是人类理解的最自然、最直接的策略，而参数记忆通常以潜在空间表示。然而，这种 可解释性是以信息密度为代价的 。这是因为 文本记忆中的单词序列以离散空间表示，而离散空间不像参数记忆中的连续空间那样密集。

总之文本记忆更适合对话和特定上下文的场景，并且上下文内容不太多。参数化记忆适合有大量知识需要写入模型记忆的场景。

记忆操作

如上文所述，对记忆的操作主要有写记忆，记忆管理，读记忆。

![原文图片](assets/e95f274baaf1.png)

写记忆 ：识别哪些信息应该写入记忆至关重要，并且应该 对原始信息中的噪声进行处理 。此外， 环境可能会提供各种形式的反馈 ，如何从这些反馈中提取有效信息（可能涉及多模态）也至关重要。

记忆管理 ： 通过不断的反思来管理 ，以生成更高级的记忆，合并多余的记忆条目，并忘记不重要的早期记忆。

读记忆 ：对于文本形式的记忆，可以采用 文本相似度 来筛选记忆。而对于参数化的记忆，模型 直接用更新后的模型进行推理，这可以视为隐式的阅读过程 。

### 4.4.4 如何评估Memory-based agent

本文将评估方法分为两类：（1）直接评估， 独立测量记忆模块的能力 。（2）间接评估， 通过端到端代理任务评估记忆模块 。

直接评估 ：又可以分为人的主观评价和客观指标评价两种

主观评价 ：主要从回答的 连贯性 ，即检索到的记忆应该与当前情景匹配，以及 合理性 ，即检索到的以及应该包含正确的信息。

客观评价 ：常见指标包括预测标签 准确率 ，检索到的记忆的 F1值 ， 计算和推理时长 ， GPU占用量

间接评估 ：如果代理能完成高度依赖记忆的任务，那就证明记忆模块是有效的。代表性任务有：

对话任务 ：记忆保留与用户对话的上下文， agent的回复应该与上下文一致，不能出现自相矛盾的情况 。还可以 通过用户的参与度来衡量agent回复的质量和吸引力 。

多源问答 ： 综合评估之前提到的多个来源的记忆信息 ，即同一个trial、跨trail和外部知识， 测试agent对不同内容和来源的记忆的整合能力 。同时检测 多信息源导致的记忆矛盾和知识更新问题 。

长文本应用 ：采用文本形式的记忆会一般都会导致比较长的上下文，需要 评估agent能否充分理解长文本 ，并从中检索出对给定问题有用的内容。

![原文图片](assets/9766e43fd6f1.png)

### 4.4.5 Agent记忆机制示例

![原文图片](assets/7b21c17efc45.png)

在上图的例子中，Agent有两个任务：

(A) 为Alice在2024年5月1日至5月3日期间在北京制定旅行计划，Agent需要 (i) 购买往返机票，(ii) 根据Alice的偏好确定几个景点，(iii) 安排这些景点的参观顺序 。

(B) 在2024年5月10日为Alice推荐一部电影，Agent需要 (i) 确定Alice有空看电影的时间，(ii) 根据Alice的观看偏好选择一部电影 。对于每个任务，在下面展示一个可能的试验：

对于任务(A)，试验是：

[步骤 1] Agent：我需要通过在线票务办公室预订2024年5月1日从上海到北京的航班，以及5月3日从北京返回上海的航班。环境（在线票务办公室）：订单已确认。出发航班上午9:00起飞，您的票号是EK240501SX9021。返程航班下午4:30起飞，您的票号是LG240503FN6317。请准时到达机场搭乘您的航班。

[步骤 2] Agent：我已经从《北京景点》杂志获取了外部知识。它显示长城、故宫和颐和园都很有名。根据爱丽丝的偏好，我认为她更喜欢古代建筑，所以我确定故宫和颐和园作为目的地。环境（Alice）：做得好！

[步骤 3] Agent：现在，我需要为Alice安排参观顺序。根据上面的信息，我建议她一到北京就参观颐和园，因为那里适合整个下午游玩并观看日落。然后，她第二天可以去故宫，这样会给她足够的时间。

最后，她可以在第三天返回上海休息。环境（Alice）：我喜欢这个计划。谢谢！

对于任务(B)，试验是：

[步骤 1] Agent：根据我以前为Alice推荐电影的经验，她更喜欢在晚上9:00开始看电影，因为那时她已经完成工作。我应该问问Alice那个时间她是否有空。环境（Alice）：当然，这是个好时间！

[步骤 2] 智能体：现在，我需要找到一些Alice在Netflix上标记为“想看”的电影。环境（Netflix）：Alice的想看列表：《星际穿越》、《恐怖星球》和《鬼吹灯》。

[步骤 3] Agent：由于Alice晚上从不观看恐怖电影，《星际穿越》对她来说更合适。现在，我需要与爱丽丝确认这部电影。环境（Alice）：太棒了！我喜欢它！

### 4.4.6 Langchain实现Memory-based agent

langchain中使用memory的例子：创建一个简单的自定义代理，该代理可以访问搜索工具并使用 ConversationBufferMemory 类。首先定义搜索工具

Python
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain
from langchain_core.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_openai import ChatOpenAI
import os
os.environ["SERPAPI_API_KEY"] = (
 "Your serpapi key"
)
search = SerpAPIWrapper()
from langchain.agents import load_tools
llm = ChatOpenAI(model=os.environ["LLM_MODELEND"], temperature=0)
tools = load_tools(["serpapi"], llm=llm)

接下来定义一个prompt， prompt中的的chat_history需要与ConversationBufferMemory的key对应 ，存储对话记录。

Python
prefix = """Have a conversation with a human, answering the following questions as 
 best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
 tools,
 prefix=prefix,
 suffix=suffix,
 input_variables=["input", "chat_history", "agent_scratchpad"],
)
memory = ConversationBufferMemory(memory_key="chat_history")

接下来创建一个LLMChain，然后 将momory加入到agent中 。

Python
llm_chain = LLMChain(llm = llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
 agent=agent, tools=tools, verbose=True, memory=memory
)

agent_chain.run(input="How many people live in canada?")
agent_chain.run(input="what is their national anthem called?")

langchain中为我们实现了多种记忆，常见的有：

ConversationBufferMemory ： 所有聊天记录都被存入chat_history中 ，导致下一轮的prompt很长

ConversationBufferWindowMemory ： 只保留最近几次人类与AI的互动 ，只适应短对话。

ConversationSummaryMemory ：在回答新问题的时候， 对之前的问题进行了总结性的重述 ，再传递给chat_history 参数，这种基于总结的方法能避免过度使用token，适合长对话。总结由LLM完成，虽然最初使用的 Token 数量较多，但随着对话的进展，汇总方法的增长速度会减慢；并且，总结的过程中并没有区分近期的对话和长期的对话（通常情况下近期的对话更重要）。

ConversationSummaryBufferMemory ： 总结较早的对话，保留近期的对话原始内容 。

### 4.4.7 Milvus向量数据库实现记忆

Mem0是一个为AI应用设计的智能记忆层，旨在通过保留用户偏好并随时间不断适应，提供个性化且高效的交互体验。特别适合聊天机器人和AI驱动的工具，Mem0能够创建无缝、上下文感知的体验。

下面将通过介绍Mem0记忆管理的基本操作来做一个Agent持有记忆的简单demo，同时使用Milvus，一个高性能、开源的向量数据库，它 能够支持高效的存储和检索 。以下代码完成了基础记忆操作，帮助用户使用Mem0和Milvus构建个性化的AI交互。

Python
! pip install mem0ai pymilvus

配置Mem0与Milvus

Python
import os
os.environ["OPENAI_API_KEY"] = "sk-***********"

现在，我们可以配置Mem0使用Milvus作为向量存储。

Python
# Define Config
from mem0 import Memory

config = {
 "vector_store": {
 "provider": "milvus",
 "config": {
 "collection_name": "quickstart_mem0_with_milvus",
 "embedding_model_dims": "1536",
 "url": "./milvus.db", # Use local vector database for demo purpose
 },
 },
 "version": "v1.1",
}

m = Memory.from_config(config)

添加记忆

add函数 将非结构化文本作为记忆存储在Milvus中，并将其与特定用户和可选元数据关联 。

在这里，将Alice的记忆“working on improving my tennis skills”连同相关metadata一起添加到Milvus中。

Python
# Add a memory to user: Working on improving tennis skills
res = m.add(
 messages="I am working on improving my tennis skills.",
 user_id="alice",
 metadata={"category": "hobbies"},
)

res

输出结果：

{'results': [{'id': '77162018-663b-4dfa-88b1-4f029d6136ab',

'memory': 'Working on improving tennis skills',

'event': 'ADD'}],

'relations': []}

搜索记忆

可以使用搜索功能来寻找与用户最相关的记忆。

让我们从为Alice添加另一个记忆开始。

Python
new_mem = m.add(
 "I have a linear algebra midterm exam on November 20",
 user_id="alice",
 metadata={"category": "task"},
)

现在，调用 get_all 函数并指定 user_id 来验证我们确实为用户alice保存了2条记忆记录。

Python
m.get_all(user_id="alice")

输出结果：

{'results': [{'id': '77162018-663b-4dfa-88b1-4f029d6136ab',

'memory': 'Likes to play tennis on weekends',

'hash': '4c3bc9f87b78418f19df6407bc86e006',

'metadata': None,

'created_at': '2024-11-01T19:33:44.116920-07:00',

'updated_at': '2024-11-01T19:33:47.619857-07:00',

'user_id': 'alice'},

{'id': 'aa8eaa38-74d6-4b58-8207-b881d6d93d02',

'memory': 'Has a linear algebra midterm exam on November 20',

'hash': '575182f46965111ca0a8279c44920ea2',

'metadata': {'category': 'task'},

'created_at': '2024-11-01T19:33:57.271657-07:00',

'updated_at': None,

'user_id': 'alice'}]}

可以进行搜索，通过提供查询内容和用户ID来寻找与用户最相关的记忆。默认情况下，使用 L2度量（欧几里得距离）来进行相似度搜索 ，因此，得分越小意味着相似度越高。

Python
m.search(query="What are Alice's hobbies", user_id="alice")

输出结果：

{'results': [{'id': '77162018-663b-4dfa-88b1-4f029d6136ab',

'memory': 'Likes to play tennis on weekends',

'hash': '4c3bc9f87b78418f19df6407bc86e006',

'metadata': None,

'score': 1.2807445526123047,

'created_at': '2024-11-01T19:33:44.116920-07:00',

'updated_at': '2024-11-01T19:33:47.619857-07:00',

'user_id': 'alice'},

{'id': 'aa8eaa38-74d6-4b58-8207-b881d6d93d02',

'memory': 'Has a linear algebra midterm exam on November 20',

'hash': '575182f46965111ca0a8279c44920ea2',

'metadata': {'category': 'task'},

'score': 1.728922724723816,

'created_at': '2024-11-01T19:33:57.271657-07:00',

'updated_at': None,

'user_id': 'alice'}]}

## 4.5 Tool

Agent 与大模型的一大区别在于能够使用外部工具拓展模型能力。在获取到每一步子任务的工作后，Agent 都会判断是否需要通过调用外部工具来完成该子任务，并在完成后获取该外部工具返回的信息提供给 LLM，进行下一步子任务的工作。

### 4.5.1 Function call

Function Call 是一种实现大型语言模型连接外部工具的机制。通过 API 调用 LLM 时， 调用方可以描述函数，包括函数的功能描述、请求参数说明、响应参数说明，让 LLM 根据用户的输入，合适地选择调用哪个函数 ，同时理解用户的自然语言，并转换为调用函数的请求参数（通过 JSON 格式返回 ）。调用方使用 LLM 返回的函数名称和参数， 调用函数并得到响应 。最后，如果 需要 ， 把函数的响应传给 LLM，让 LLM 组织成自然语言回复用户 。

![原文图片](assets/0456f952f838.png)

### 4.5.2 MRKL

MRKL（Modular Reasoning, Knowledge and Language）即模块化推理、知识和语言系统，是一种旨在改进现有大规模语言模型的自主代理的架构。MRKL系统旨在包含一系列“专家”模块，而 LLM作为路由器，将查询引导至最合适的专家模块 。 这些专家模块既可以是大模型，也可以是符号的 （例如数学计算器、货币转换器、天气API）。

MRKL 提供一个 Prompt 模板 ，其中包括：

工具列表 ：每个工具的功能描述。

主要指令 ：告诉 LLM “你可以思考后调用工具，拿到结果后继续思考”。

对话或任务上下文 ：让 LLM 结合上下文做决策。

![原文图片](assets/112845953688.png)

### 4.5.3 Toolformer

训练了一个 用于决定何时调用哪些API、传递什么参数以及如何最佳地将结果进行分析的大模型 。这一过程通过 微调 的方法来训练大模型，仅需要每个API几个示例即可, 训练所用的数据集根据新增的 API 调用注释是否能够提高模型输出的质量而进行扩展。该工作集成了一系列工具，包括计算器、问答系统、搜索引擎、翻译系统和日历。

![原文图片](assets/14f05ac42ba1.png)

### 4.5.4 HuggingGPT

HuggingGPT是由大型语言模型（LLM）驱动的，设计用来自主处理一系列复杂的人工智能任务。HuggingGPT融合了 ChatGPT 与 HuggingFace 。具体来说，LLM在这里扮演着大脑的角色，一方面 根据用户请求拆解任务 ，另一方面 依据任务描述选择适合的模型执行任务 。通过执行这些模型并 将结果整合到计划的任务中 ，HuggingGPT能自主完成复杂的用户请求。下图展示了从任务规划到模型选择，再到任务执行，最后是响应生成的完整流程：

首先，HuggingGPT利用ChatGPT 分析用户的请求以理解他们的意图 ，并将其分解为可能的解决方案。

接下来，它会选择Hugging Face上托管的、最适合执行这些任务的专家模型。每个 选定的模型被调用并执行 ，其结果将反馈给ChatGPT。

最终，ChatGPT将所有 模型的预测结果集成起来，为用户生成响应。

![原文图片](assets/8febc0b9ad94.png)

HuggingGPT的这种工作方式不仅扩展了传统单一模式处理的能力，而且通过其智能的模型选择和任务执行机制，在跨领域任务中提供了高效、准确的解决方案。从本质上来说，HuggingGPT是一个 使用ChatGPT作为任务规划器 的框架，ChatGPT 可根据模型的描述 选择 HuggingFace 平台中可用的模型 ，使其能够处理来自不同模态的输入，并根据执行结果总结响应结果。

总结：

| 维度 | Function Call | MRKL | Toolformer | HuggingGPT |
| --- | --- | --- | --- | --- |
| 核心思想 | 通过 API 调用外部工具或服务，实现与外部系统的交互，扩展 LLM 的能力。 | 将神经网络模型与外部知识库和符号专家系统相结合，通过路由模块根据问题匹配合适的专家系统，实现推理和知识利用。 | 允许语言模型自主学习和调用工具，通过在训练过程中插入工具调用，使模型能够在生成文本时自动调用相关工具。 | 基于 HuggingFace 上的不同模型，通过任务规划、模型选择、执行任务和响应汇总四个步骤，完成复杂任务。 |
| 技术实现 | 1. 定义函数描述 2. 模型生成JSON调用参数 | 1. 设计专家模块（工具） 2. LLM选择工具路由 | 1. 自监督学习插入API调用token 2. 微调LLM | 1. 解析任务需求 2. 选择Hugging Face模型 3. 整合结果 |
| 工具管理方式 | 预定义API集合 | 模块化工具库（如计算器、数据库） | 预定义API集合 | Hugging Face模型池（文本、图像、语音等） |
| 优点 | 1. 实现简单 2. 低延迟 | 1. 模块化扩展性强 2. 可解释性高 | 1. 自动化学习调用时机 2. 减少人工干预 | 1. 多模态支持 2. 利用现成模型生态 |
| 典型应用场景 | 简单工具调用（如天气查询、日历管理） | 需要多专家协作的任务（如财务分析） | 自动化API调用（如翻译、摘要） | 复杂多模态任务（如图文生成、视频理解） |

## 4.6 多智能体 为什么失败

谈谈我对多智能体的理解

人类受限于自身知识的和生产效率有限性，人类协作可以让每个人发挥自己的长处并且提高生产效率。

多智能体与人类协作不一样，大模型一直在往通用化方向发展，单纯按照任务类型去给多个agent分配任务（比如分别做前端、后端、算法），效果可能不如都交给一个agent做（多智能体对任务理解不同，会因为沟通彼此之间的思路、数据格式、具体代码等浪费很多时间，效率反而可能不如单agent）。

MAS （Multi Agent System） 更适合于群体智能场景，也就是多agent做的事情基本一致，比如多个agent互相对抗（狼人杀），互相启发（共同审阅一篇论文）。

论文：《Why Do Multi-Agent LLM Systems Fail》

### 4.6.1 背景介绍

MAS定义 ：LLM-based 智能体定义为一个具有提示规范（初始状态）、对话记录（状态）以及与环境交互能力（动作）的实体。 多智能体系统（MAS） 由多个智能体组成，通过编排实现协作，以实现集体智能。

研究背景 ：MAS允许多个 LLM 智能体协作完成任务，理论上能比单个智能体取得更好的效果（将复杂任务拆解，每个Agent只完成其中一部分，理论上肯定比一个Agent全包好）。但 现实中MAS却在基准测试上的性能提升仍然微乎其微 ，下图中主流的MAS框架ChatDev在某些任务中的正确率低至25%。

![原文图片](assets/13f73e278cbd.jpeg)

论文贡献 ：

分析了五种流行的 MAS 框架，涉及 150 多个任务，每个轨迹平均超过15,000行文本。提出多智能体系统失败分类法（ Multi-Agent System Failure Taxonomy，MAST ）将失败模式分为3类，总共14种范式：

角色规范和系统设计问题 ：比如 任务的定义不够清晰 ， 角色定义不明确 ， 或者 系统流程设计本身存在缺陷 。这个问题很普遍，不止出现在多agent场景。

举例：分工不明确，导致不同agent之间有权责重叠。

智能体之间的不协调 ：比如不同 智能体之间的目标不一致 ， 信息隐瞒 ，或者它们 可能忽略关键信息 。

举例：一个团队写代码（包括leader、产品、程序员），沟通的时候大部分时间 都在讨论不重要的东西 ，写出来的代码质量很低。

任务验证和终止问题 ：比如系统 无法正确判断任务是否完成 ，或者 验证不完整不正确 。

举例：大模型生成的内容可能会存在错误，这种错误不仅来自幻觉， 也来自于搜索时无法过滤掉低质量网页和资料 ，这一问题在多智能体中被放大了，从而无法验证自己生成的内容是否正确，以及何时终止生成。

为了验证分类的准确性，邀请三组专家对失败模式进行分析， Cohen's Kappa 得分为 0.88，证明分类结果非常可信。

此外，论文将 MAS 与“大语言模型作为裁判”（ LLM-as-a-Judge ）结合在一起，使用gpt-o1以支持高效的评估，通过与三个人类专家对10个轨迹的注释进行交叉验证，Cohen's Kappa 得分为 0.77。

失败模式需要更复杂的解决方案， 单纯的清晰智能体角色或者优化智能体协作模式无法彻底解决以上问题 。

不要把失败模式全甩锅给LLM自身的局限性，许多MAS失败源于智能体之间的交互挑战，而不是单个智能体的局限性。

### 4.6.2 失败模式分类

这部分不做重点讨论，只简要介绍。

采用Grounded Theory（GT）方法，通过理论抽样、开放式编码、持续比较分析、备忘录和理论化等步骤，迭代地收集和分析多智能体系统（MAS）的执行轨迹。

通过理论抽样确保所选MAS和任务的多样性，选择代表系统预期的典型任务，包括HyperAgent,AppWorld, AG2, ChatDev, MetaGPT。

通过持续比较分析，注释者识别失败模式，并将其与现有代码进行比较，确保代码的准确性和一致性。直到达到理论饱和，即额外数据不再提供新见解。

进行一轮初步分类和两轮优化分类， Cohen's Kappa 达到0.84

为实现自动化注释，实现了 LLM-as-a-Judge ，few-shot形式gpt-o1的 Cohen's Kappa 达到0.77。

![原文图片](assets/b81831f35309.jpeg)

Cohen's Kappa：一种衡量分类一致性的指标

定义 【公式开始】p_o 【公式结束】 ：评估者之间观察到的相对一致性， 【公式开始】p_e 【公式结束】 ：机会一致的假设概率

【公式开始】kappa = (p_o - p_e) / (1 - p_e) 【公式结束】

计算示例：

| 用户1/<br>用户2 | Yes | No |
| --- | --- | --- |
| Yes | 25 | 10 |
| No | 15 | 20 |

计算 【公式开始】p_o 【公式结束】 :

【公式开始】p_o 【公式结束】 =（都说是 + 都说不是）/（总分）

【公式开始】p_o 【公式结束】 = (25 + 20) / (70) = 0.6429

计算 【公式开始】p_e 【公式结束】 ：

用户1说“是”的总次数除以响应总数*用户2说“是”的总次数 + 用户1说“否”的总次数除以响应总数*用户2说“否”的总次数

P(“是”) = ((25+10)/70) * ((25+15)/70) = 0.285714

P(“否”) = ((15+20)/70) * ((10+20)/70) = 0.214285

【公式开始】p_e 【公式结束】 = 0.285714 + 0.214285 = 0.5

计算Kappa, Kappa值越大说明一致性越强，一般Kappa>0.8就认为标注标准清晰可靠。

【公式开始】kappa = (p_o - p_e) / (1 - p_e) = 0.2857 【公式结束】

### 4.6.3 失败模式分析

![原文图片](assets/a6747d465e79.jpeg)

规范与系统设计问题

这类失败源于系统设计本身的缺陷、会话管理糟糕、任务指令的不明确、或者智能体未能遵循其角色和职责。

Disobey task specification（违反任务、规范） ： 未能遵守给定任务的指定约束或要求， 导致次优或错误的结果。

例子 ：开发国际象棋游戏时，输入应该遵循国际象棋记谱法（如'Ke8', 'Qd4'），而最终生成的游戏却要求输入棋子移动前后的坐标 (x1, y1), (x2, y2)。

Disobey role specification（违反角色规范） ： 未能遵守分配角色的既定责任和约束 ，智能体1越俎代庖做其他智能体2的活。

例子 ：在ChatDev的需求分析阶段，CPO（首席产品官）智能体有时会越权，承担CEO的角色，自行定义产品愿景并做出最终决策。

Step repetition（步骤重复） ： 不必要地重复先前已完成的步骤 ，可能导致任务完成的延迟或错误，通常是因为死板的轮次设置。

例子 ：HyperAgent中的“导航员”智能体为了实现Line3D类而反复尝试，即使已经实现了。

Loss of conversation history（会话历史丢失） ： 上下文意外截断，导致 智能体忽略最近的交互历史并恢复到先前的对话状态。

例子 ：HyperAgent在解决一个编程bug时，一开始决定用scikit-learn模型替换所需的lightgbm库，但在后续交互中，它似乎忘记了这个决定，又回过头来尝试安装lightgbm。

Unaware of termination conditions（不知道终止条件） ： 智能体不知道何时应该结束交互 ，导致不必要的对话持续。

例子 ：在AG2解决一个数学问题时，即使已经给出了正确的答案，或者问题无法解决，智能体仍然反复要求继续进行。

智能体之间的不协调

这类失败发生在智能体之间的沟通和协作环节，存在无效沟通、行为冲突、偏离初始任务、互相误解等问题。

Conversation reset（会话重置）： 对话意外或无端的重启 ，可能导致上下文和交互中取得的进展丢失。

例子 ：同Step repetition。

Fail to ask for clarification（未能请求澄清）： 面对不清楚或不完整的数据时没有请求更多信息，而是基于猜测行动 ，可能导致错误的操作。

例子 ：AppWorld 中的“主管”智能体指示“电话”智能体使用电子邮箱ID作为用户名。电话智能体在阅读文档后发现正确的用户名应为电话号码，但仍继续使用错误的邮箱ID，导致出现错误。

Task derailment（任务偏离）： 偏离给定任务的预期目标或重点 ，可能导致无关或无效的操作。

例子 ：AG2在解决一个数学问题时，可能中途被某个计算细节带偏，开始解决一个完全不同的问题，或者在找到正确答案后又继续进行不相关的计算。

（Information withholding）信息隐瞒： 未分享智能体自身拥有的重要数据或见解 。

例子 ：HyperAgent 的“导航员”有时找到了潜在解决方案，但没有将其完整传达给“planner”，导致后者无法做出正确决策。

Ignored other agent’s input（忽略其他智能体的输入）： 忽视或未能充分考虑系统中其他智能体提供的输入或建议。

例子 ：在Multi-Agent Peer Review系统中，智能体1收到了智能体2对其数学解题过程的正确反馈，智能体1口头上承认了反馈，但没有发现其解决方案与其自身解决方案之间存在矛盾，在最终答案中仍然坚持自己最初的错误结果。

Reasoning-action mismatch（推理-行动不匹配）： 智能体的逻辑推理过程与其实际行动之间存在差异 .

例子 ：HyperAgent 的“导航员”已经发现了正确答案，但告诉“planner”是无关的建议。

任务验证与终止失败

这类失败发生在任务验证阶段，包括由于过早执行终止而导致的故障，以及缺乏保证交互、决策和结果的准确性、完整性和可靠性的机制。

Premature termination（过早终止）： 在交换所有必要信息或实现目标之前结束对话、交互或任务。

例子 ：HyperAgent 的“编辑器”智能体声称已经完成了对代码的修改，但实际上并没有执行修改操作，却提前结束了自己的任务环节，导致后续依赖该修改的步骤失败。

No or incomplete verification（无或不完整验证）： 系统缺少验证步骤，或者验证步骤未能覆盖所有关键方面 ，导致错误或不一致被遗漏。

例子 ：AG2 系统中把鱼的数量和它们的成本搞混了，但没有验证。

Incorrect verification（验证错误）： 存在验证步骤，但 验证本身是错误的或无效的， 未能发现实际存在的问题。

例子 ：MetaGPT 在实现棋类游戏时，单元测试可能只覆盖了最基本的情况（如兵的移动），没有覆盖非兵棋子的复杂移动规则，却错误地认为验证通过。

MAS失败模式的一些观察

这些失败模式分布相对均匀，没有单一错误类别主导失败发生。

失败模式可能具有连锁效应。

虽然验证是最后一道防线，但 并非所有问题都由验证不足引起 。

MAS的失败模式违反了核电站、航空管制等 高可靠性组织（HRO） 的规则，如“不遵从角色规范" (FM-1.2) 违反了 "极端层级分化"，”未能请求澄清" (FM-2.2) 违反了 "尊重专业知识" 。

### 4.6.4 设计更好的多智能体系统

作者将其分为战术性方法和结构性策略两类，前者针对特定失败模式进行的直接小修小补，后者涉及对整个系统结构进行修改，从基础架构层面提升 MAS 的鲁棒性和可靠性。

战术性方法

提示词优化 ：明确提示词中的任务和每个智能体的角色，并 鼓励智能体之间进行主动对话，如果存在不一致，智能体应能够重试任务。

自我验证 ：通过 重新陈述解决方案、检查条件并测试错误 ，智能体可以发现潜在问题。

模块化设计 ：采用模块化方法， 使用简单且定义明确的智能体，而不是复杂的多任务智能体。

交叉验证 ： 不同智能体可以提出多种解决方案，并通过交叉验证确保结果的准确性。

结构性策略

加强验证 ：验证是抵抗模式失败的最后一道防线， 不充分的验证机制是MAS失败的重要原因之一 。

标准化通信协议 ：基于大语言模型的智能体主要通过 无结构的文本 进行通信，这可能导致歧义。 通过明确定义意图和参数，可以提高智能体之间的对齐度，并在互动过程中进行正式的连贯性检查 。

强化学习 ： 奖励任务相关行为并惩罚低效行为 。

概率置信度 ： 当智能体的置信度低于某个阈值时，它们可以暂停以获取更多信息，从而避免错误决策 。

记忆和状态管理 ： 增强上下文理解并减少交流中的歧义。

## 4.7 MCP

### 4.7.1 从 Function calling 到 MCP

Function calling

能调用外部工具，是大模型进化为智能体Agent的关键，如果不能使用外部工具，大模型就只能是个简单的聊天机器人，甚至连查询天气都做不到。 Function calling 就是解决这一问题的， 作为大模型和外部工具之间的中介，使得大模型能间接的调用外部工具。根据用户的问题判定何时需要调用外部工具，并以结构化 JSON 输出调用信息，外部系统据此执行相应操作，再将结果回传给模型，最终由模型基于真实数据生成回答。

![原文图片](assets/f84acc119e2c.png)

接下来结合Qwen模型介绍Function call的流程，首先定义了一个查询当前天气的函数：

JSON
{
 "type": "function",
 "function": {
 "name": "get_current_weather",
 "description": "当你想查询指定城市的天气时非常有用。",
 "parameters": {
 "type": "object",
 "properties": {
 "location": {
 "type": "string",
 "description": "城市或县区，比如北京市、杭州市、余杭区等。",
 }
 },
 "required": ["location"]
 }
 }
}

工具调用判定

大模型会在生成回答时判断用户需求是否超出自身知识范围，若需调用工具便会 输出特殊标记 （ 如 <tool_call> ）来表明需要调用函数。现有大模型经过微调，需要用工具时能够较高概率地正确调用，能正确的生成特殊标记。

生成函数调用

在 <tool_call> 标记后，模型输出严格遵循预先提供的 JSON Schema，包含 name 和 arguments 字段，描述要调用的函数名及参数 。

Bash
<tool_call>
{"name": "get_current_weather", "arguments": {"city":"北京"}}
</tool_call>

在Qwen的系统信息中就包含JSON Schema格式的函数定义，通过提示词要求大模型返回包含函数名和参数的JSON对象，并放在 <tool_call> ... </tool_call> 标签内 。并且 模型也进行了函数调用的微调 ，保证模型能按格式生成调用。

工具执行

外部调度器（Orchestrator）解析模型输出的 JSON 调用请求，将其映射到实际的工具/函数实现，并传入相应参数执行 。具体流程为：

输出解析 ：通过正则表达式匹配所有Json串，并反序列化为Python对象。

函数运行 ：根据函数名映射到对应的函数，并将 arguments 中的字段作为参数，并调用对应的函数。

模型输出

工具执行结果被封装成 <tool_response> ... </tool_response> 消息，追加到对话历史中，供模型下一轮生成时参考 。Qwen会将工具响应作为用户信息插入对话，因为希望模型将工具响应作为新的信息源，让模型基于此再回答：

Python
{
 'role': 'user',
 'content': '<tool_response>
 {"weather": [..气温信息..]}
 </tool_response>'
}

最后， 再次调用大模型 读取 <tool_response> 中的信息，生成准确的最终答案。

MCP

2024 年 11 月，Claude 母公司 Anthropic 正式推出了 MCP（Model Context Protocol）。这一技术协议旨在 为Agent开发建立统一规范 ，通过约定共同遵守的技术标准，大幅提升多人协作开发Agent的效率。

MCP 着力解决智能体开发中一个核心痛点 —— 外部工具调用的技术门槛过高问题 。由于大型语言模型自身缺乏与外部工具直接通信的能力，传统开发中只能依赖 "函数调用"（Function calling）作为中介桥梁，由大模型间接触发外部函数执行：

![原文图片](assets/f84acc119e2c.png)

编写Function calling函数工作量很大 （随便一个函数就要100+行代码），并且为了让大模型理解这个函数，需要用Json Schema格式编写功能说明，并设计提示词模板。

JSON
JSON Schema 是一种用于描述和验证JSON数据结构的标准化格式，在Function calling中扮演函数接口说明书
的角色。其核心作用是为大模型提供精准的函数调用规范，确保模型生成的参数格式正确。下面的例子中，指明了
Function名字和功能，以及入参类型、参数可选值、是否必须和参数描述等信息。
{
 "name": "get_weather",
 "description": "查询指定地点的天气信息",
 "parameters": {
 "type": "object",
 "properties": {
 "location": {
 "type": "string",
 "description": "城市名称，如'北京'"
 },
 "unit": {
 "type": "string",
 "enum": ["celsius", "fahrenheit"],
 "description": "温度单位"
 }
 },
 "required": ["location"]
 }
}

Markdown
提示词模板是预定义的结构化指令框架，用于引导大模型准确触发函数调用。其本质是通过工程化设计，
将自然语言指令转化为机器可解析的逻辑流。例如：

你是一个智能天气助手，请按以下步骤响应用户：
1. **意图识别**：判断用户是否在询问天气
2. **参数提取**：
 - 若需查询天气，提取地点(location)和单位(unit)
 - 若未明确单位，默认使用摄氏制
3. **函数调用**：严格按JSON格式返回调用指令：
 {
 "function": "get_weather",
 "arguments": {"location": "北京", "unit": "celsius"}
 }

![原文图片](assets/ffd1ffa5f953.jpeg)

MCP统一了Function calling的运行规范：

首先是先统一名称，MCP把大模型运行环境称作 MCP Client ，也就是MCP客户端，同时，把外部函数运行环境称作 MCP Server ，也就是MCP服务器。

然后，统一MCP客户端和服务器的运行规范， 并且要求MCP客户端和服务器之间，也统一按照某个既定的提示词模板进行通信 。

![原文图片](assets/21eb469f7f29.jpeg)

使用MCP的好处在于可以 避免外部函数重复编写 。 像查询天气、网页爬取、查询本地MySQL数据库这种通用的需求，只需要开发一个服务器就好，后续的开发者可以直接调用服务而不用重新实现。MCP开发工具支持Python、TS和Java等多种语言。想要使用MCP服务器就要构建MCP客户端（支持任意本地和在线大模型，甚至是Cursor）。而如果没有所需要的MCP服务器，就要自己开发，下面的代码给出了一个简单的服务器示例

Python
# server.py
from mcp.server.fastmcp import FastMCP
# Create an MCP server
mcp = FastMCP("Demo")
# Add an addition tool
@mcp.tool()
def add(a:int,b:int)-> int:
 """Add two numbers"""
 return a+ b
# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get greeting(name:str)->str:
 """Get a personalized greeting"""
 return f"Hello, {name}!"

MCP针对agent的tools模块，目前不涉及memory和planning模块。

下图形象的对比了Function calling调用API和使用MCP的差异，MCP就像转接口，将多种多样的API封装成统一格式的mcp server，允许client端的大模型调用。

MCP是一种更底层的Agent开发框架，与之前介绍的 Agent开发框架 不冲突。

### 4.7.2 MCP客户端

uv环境管理

uv 是一个 Python 依赖管理工具 ，类似于pip 和 conda ，但它更快、更高效，并且可以更好地管理 Python 虚拟环境和依赖项。它的核心目标是替代 pip 、 venv 和 pip-tools ，提供更好的性能和更低的管理开销。

uv 的特点 ：

1. 速度更快 ：相比 pip ， uv 采用 Rust 编写，性能更优。

2. 支持 PEP 582 ：无需 virtualenv ，可以直接使用 pypackages 进行管理。

3. 兼容 pip ：支持 requirements.txt 和 pyproject.toml 依赖管理。

4. 替代 venv ：提供 uv venv 进行虚拟环境管理，比 venv 更轻量。

5. 跨平台 ：支持 Windows、macOS 和 Linux。

Python
# 安装uv
pip install uv
# 安装 Python 依赖，等效于pip install requests
uv pip install pandas
# 创建虚拟环境，等效于python -m venv myenv
uv venv myenv
# 激活虚拟环境
source myenv/bin/activate
# 安装所需的包，等效于pip install -r requirements.txt
uv pip install -r requirements.txt
# 运行 python 项目，等效于python script.py
uv run python script.py

MCP客户端搭建

Python
# 创建目录
uv init mcp-client 
cd mcp-client
# 创建虚拟环境并激活
uv venv
source .venv/bin/activate
# 安装 MCP SDK 
uv add mcp

创建一个简单的MCP客户端，核心功能有：

初始化 MCP 客户端

提供一个命令行交互界面

模拟 MCP 服务器连接

支持用户输入查询并返回「模拟回复」

支持安全退出

Python
import asyncio # 让代码支持异步操作 
from mcp import ClientSession # MCP 客户端会话管理 
from contextlib import AsyncExitStack # 资源管理（确保客户端关闭时释放资源）

class MCPClient:
 def __init__(self):
 """初始化 MCP 客户端"""
 # 核心概念：会话，可以获取外部工具列表，保存当前会话状态等功能，暂时不链接MCP服务器
 self.session = None
 # 异步通信资源管理器
 self.exit_stack = AsyncExitStack()
 async def connect_to_mock_server(self):
 """模拟 MCP 服务器的连接（暂不连接真实服务器）"""
 print("✅ MCP 客户端已初始化，但未连接到服务器")
 async def chat_loop(self):
 """运行交互式聊天循环"""
 print("\nMCP 客户端已启动！输入 'quit' 退出")
 while True:
 try:
 query = input("\nQuery: ").strip()
 if query.lower() == 'quit':
 break
 print(f"\n🤖 [Mock Response] 你说的是：{query}")
 except Exception as e:
 print(f"\n⚠️ 发生错误: {str(e)}")
 async def cleanup(self):
 """清理资源"""
 await self.exit_stack.aclose() # 关闭资源管理器
async def main(): 
 client = MCPClient() # 创建 MCP 客户端 
 try: 
 await client.connect_to_mock_server() # 连接（模拟）服务器 
 await client.chat_loop() # 进入聊天循环 
 finally: 
 await client.cleanup() # 确保退出时清理资源
if __name__ == "__main__":
 asyncio.run(main())

接入在线模型

Python
import asyncio
import os
from openai import OpenAI
from dotenv import load_dotenv
from contextlib import AsyncExitStack
# 加载 .env 文件，确保 API Key 受到保护，需要在.env文件中写入：
 # BASE_URL="https://ai.devtool.tech/proxy/v1"
 # MODEL=gpt-4o
 # OPENAI_API_KEY="your_api_key"
load_dotenv()
class MCPClient:
 def __init__(self):
 """初始化 MCP 客户端"""
 self.exit_stack = AsyncExitStack()
 self.openai_api_key = os.getenv("OPENAI_API_KEY") # 读取 OpenAI API Key
 self.base_url = os.getenv("BASE_URL") # 读取 BASE YRL
 self.model = os.getenv("MODEL") # 读取 model
 if not self.openai_api_key:
 raise ValueError("❌ 未找到 OpenAI API Key，请在 .env 文件中设置OPENAI_API_KEY")
 self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)
 async def process_query(self, query: str) -> str:
 """调用 OpenAI API 处理用户查询"""
 messages = [{"role": "system", "content": "你是一个智能助手，帮助用户回答问题。"},
 {"role": "user", "content": query}]
 try:
 # 调用 OpenAI API,将 OpenAI API 变成异步任务，防止程序卡顿。
 response = await asyncio.get_event_loop().run_in_executor(
 None,
 lambda: self.client.chat.completions.create(
 model=self.model,
 messages=messages
 )
 )
 return response.choices[0].message.content
 except Exception as e:
 return f"⚠️ 调用 OpenAI API 时出错: {str(e)}"
 async def chat_loop(self):
 """运行交互式聊天循环"""
 print("\n🤖 MCP 客户端已启动！输入 'quit' 退出")
 while True:
 try:
 query = input("\n你: ").strip()
 if query.lower() == 'quit':
 break
 response = await self.process_query(query) # 发送用户输入到 OpenAI API
 print(f"\n🤖 OpenAI: {response}")
 except Exception as e:
 print(f"\n⚠️ 发生错误: {str(e)}")
 async def cleanup(self):
 """清理资源"""
 await self.exit_stack.aclose()
async def main():
 client = MCPClient()
 try:
 await client.chat_loop()
 finally:
 await client.cleanup()
if __name__ == "__main__":
 asyncio.run(main())

部署本地模型

使用vllm库部署QwQ-32B

模型比较大，采用huggingface担心网络不稳定，可以用modelscope下载模型

Plaintext
pip install modelscope
modelscope download --model Qwen/QwQ-32B --local_dir ./QwQ-32B

安装vllm库

Plaintext
pip install vllm

开启vllm

Plaintext
vllm serve ./QwQ-32B --max-model-len 32768 # 32k上下文单卡
CUDA_VISIBLE_DEVICES=0,1 vllm serve ./QwQ-32B --tensor-parallel-size 2 # 128k上下文双卡

在jupyter中运行以下代码：

Plaintext
from openai import OpenAI
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
 api_key=openai_api_key,
 base_url=openai_api_base,
)
prompt = "在单词\"strawberry\"中，总共有几个R？"
messages = [
 {"role": "user", "content": prompt}
]
response = client.chat.completions.create(
 model="QWQ-32B/",
 messages=messages,
)

print(response.choices[0].message.content)

后端接收到以下请求：

![原文图片](assets/0be32b1e2d97.jpeg)

### 4.7.3 MCP服务器端

Server端可以提供以下三种标准能力：

Resources： 资源，类似于文件数据读取，可以是文件资源或是API响应返回的内容。

Tools： 工具，第三方服务、功能函数，通过此可控制LLM可调用哪些函数。

Prompts： 提示词，为用户预先定义好的完成特定任务的模板。

通信机制

MCP目前支持两种传输方式：

标准输入输出（stdio） ：用于本地通信的传输方式。在这种模式下，MCP 客户端会将服务器程序作为子进程启动，双方通过标准输入（stdin）和标准输出（stdout）进行数据交换。这种方式适用于客户端和服务器在同一台机器上运行的场景，确保了高效、低延迟的通信。

HTTP+SSE ：适用于客户端和服务器位于不同物理位置的场景。在这种模式下，客户端和服务器通过 HTTP 协议进行通信，利用 SSE 实现服务器向客户端的实时数据推送。

天气查询服务器搭建

![原文图片](assets/4ae69fb16556.jpeg)

搭建了一个提供天气查询的工具的server，通过http请求查询天气。

Plaintext
uv add httpx

Python
import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(" .env")

# 初始化 MCP 服务器
mcp = FastMCP("weatherServer")

# OpenWeather API 配置
OPENWEATHER_API_BASE = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("OpenWeather_API_KEY") # 请替换为你自己的 OpenWeather API Key
USER_AGENT = "weather-app/1.0"

# 异步获取天气数据
async def fetch_weather(city: str) -> dict[str, Any] | None:
 """
 从 OpenWeather API 获取天气信息。
 :param city: 城市名称（需使用英文，如 Beijing）
 :return: 天气数据字典，若出错返回包含 error 信息的字典
 """
 params = {
 "q": city,
 "appid": API_KEY,
 "units": "metric",
 "lang": "zh_cn"
 }
 headers = {"User-Agent": USER_AGENT}
 # 使用 httpx.AsyncClient() 发送异步 GET 请求到 OpenWeather API。
 async with httpx.AsyncClient() as client:
 try:
 response = await client.get(OPENWEATHER_API_BASE, params=params, headers=headers, timeout=30.0)
 response.raise_for_status()
 return response.json() # 返回字典类型
 except httpx.HTTPStatusError as e:
 return {"error": f"HTTP 错误: {e.response.status_code}"}
 except Exception as e:
 return {"error": f"请求失败: {str(e)}"}

# 天气数据格式化
def format_weather(data: dict[str, Any] | str) -> str:
 """
 将天气数据格式化为易读文本。
 :param data: 天气数据（可以是字典或 JSON 字符串）
 :return: 格式化后的天气信息字符串
 """
 # 如果传入的是字符串，则先转换为字典
 if isinstance(data, str):
 try:
 data = json.loads(data)
 except Exception as e:
 return f"无法解析天气数据: {e}"

 # 如果数据中含错误信息，直接返回错误提示
 if "error" in data:
 return f"{data['error']}"

 # 提取数据做容错处理
 city = data.get("name", "未知")
 country = data.get("sys", {}).get("country", "未知")
 temp = data.get("main", {}).get("temp", "N/A")
 humidity = data.get("main", {}).get("humidity", "N/A")
 wind_speed = data.get("wind", {}).get("speed", "N/A")

 # weather 是一个列表，因此此处用 [{}] 前先提供默认字典
 weather_list = data.get("weather", [{}])
 description = weather_list[0].get("description", "未知")

 return (
 f"🌍 {city}, {country}\n"
 f"🌡️ 温度: {temp}°C\n"
 f"💧 湿度: {humidity}%\n"
 f"🌬️ 风速: {wind_speed} m/s\n"
 f"☁️ 天气: {description}\n"
 )

@mcp.tool()
async def query_weather(city: str) -> str:
 """
 输入指定城市的英文名称，返回今日天气查询结果。
 :param city: 城市名称（需使用英文）
 :return: 格式化后的天气信息
 """
 data = await fetch_weather(city)
 return format_weather(data)

if __name__ == "__main__":
 # 以标准 I/O 方式运行 MCP 服务器，也就是本地进程间通信IPC，服务器作为子进程运行，
 # 并通过标准输入输出(stdin/stdout)进行数据交换
 mcp.run(transport='stdio')

接下来实现一个与调用这个server的client端，以与大模型对话的形式呈现，只有问天气查询的问题时调用工具，否则就是与大模型对话。

Python
import asyncio
import os
import json
import sys
from typing import Optional
from contextlib import AsyncExitStack

from openai import OpenAI
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 加载环境变量
load_dotenv()

class MCPClient:
 def __init__(self):
 """初始化 MCP 客户端"""
 self.exit_stack = AsyncExitStack()# 统一管理异步上下文（如 MCP 连接）的生命周期。可以在退出（ cleanup ）时自动关闭
 self.openai_api_key = os.getenv("OPENAI_API_KEY")
 self.base_url = os.getenv("BASE_URL")
 self.model = os.getenv("MODEL")
 
 if not self.openai_api_key:
 raise ValueError("✕ 未找到 OpenAI API Key，请在 .env 文件中设置 OPENAI_API_KEY")
 
 self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)
 self.session: Optional[ClientSession] = None # 用于保存 MCP 的客户端会话，默认是 None ，稍后通过 connect_to_server 进行连接

 async def connect_to_server(self, server_script_path: str):
 """连接到 MCP 服务器并列出可用工具"""
 is_python = server_script_path.endswith('.py')
 is_js = server_script_path.endswith('.js')

 if not (is_python or is_js):
 raise ValueError("服务器脚本必须是 .py 或 .js 文件")
 # 判断服务器脚本是 Python 还是 Node.js，选择对应的运行命令。
 command = "python" if is_python else "node"
 server_params = StdioServerParameters(
 command=command,
 args=[server_script_path],
 env=None
 )

 # 启动服务器连接
 stdio_transport = await self.exit_stack.enter_async_context(
 stdio_client(server_params)
 )
 self.stdio, self.write = stdio_transport
 self.session = await self.exit_stack.enter_async_context(
 ClientSession(self.stdio, self.write)
 )# 发送初始化消息给服务器，等待服务器就绪。

 await self.session.initialize()

 # 列出可用工具
 response = await self.session.list_tools()
 print("\n已连接到服务器，支持以下工具:", [tool.name for tool in response.tools])

 async def process_query(self, query: str) -> str:
 """使用大模型处理查询并调用工具"""
 messages = [{"role": "user", "content": query}]
 response = await self.session.list_tools()

 # 构建可用工具列表
 available_tools = [
 {
 "type": "function",
 "function": {
 "name": tool.name, # 工具的名字
 "description": tool.description, # 外部函数的描述
 "parameters": tool.inputSchema # 如果要调用这个函数，需要的json_schema说明
 }
 } for tool in response.tools
 ]

 # 第一次模型调用
 response = self.client.chat.completions.create(
 model=self.model,
 messages=messages,
 tools=available_tools
 )

 content = response.choices[0]
 # 如何是需要使用工具，就解析工具
 if content.finish_reason == "tool_calls":
 tool_call = content.message.tool_calls[0]
 tool_name = tool_call.function.name
 tool_args = json.loads(tool_call.function.arguments)

 # 执行工具调用
 print(f"\n\n[调用工具 {tool_name}，参数 {tool_args}]\n")
 result = await self.session.call_tool(tool_name, tool_args)
 
 # 将模型返回的调用哪个工具数据和工具执行完成后的数据都存入messages中
 messages.append(content.message.model_dump())
 messages.append({
 "role": "tool",
 "content": result.content[0].text,
 "tool_call_id": tool_call.id
 })
 # 将工具调用的结果再返回给大模型用于生产最终的结果
 response = self.client.chat.completions.create(
 model=self.model,
 messages=messages
 )
 return response.choices[0].message.content
 
 return content.message.content

 async def chat_loop(self):
 """运行交互式聊天循环"""
 print("\n客户端已启动！输入 'quit' 退出")

 while True:
 try:
 query = input("\n你: ").strip()
 if query.lower() == 'quit':
 break

 response = await self.process_query(query)
 print(f"\nopenAI: {response}")

 except Exception as e:
 print(f"\n发生错误: {str(e)}")

 async def cleanup(self):
 """清理资源"""
 await self.exit_stack.aclose()

async def main():
 if len(sys.argv) < 2:
 print("用法: python client.py <服务端脚本路径>")
 sys.exit(1)

 client = MCPClient()
 try:
 await client.connect_to_server(sys.argv[1])
 await client.chat_loop()
 finally:
 await client.cleanup()

if __name__ == "__main__":
 asyncio.run(main())

Plaintext
uv run client.py server.py

MCPClient 的主要职责 ：

启动 MCP 服务器 （通过 StdioServerParameters ）

建立 MCP 会话 ，列出可用工具

处理用户输入 ，将其发送给 OpenAI 模型

如果模型想调用 MCP 工具（Function Calling） ，就执行 call_tool

将结果重新发给模型 ，并返回最终回答

测试服务器

Anthropic提供了一个非常便捷的debug工具：Inspector。借助Inspector，我们能够非常快捷的调用各类server，并测试其功能。

Plaintext
mcp dev xx.py

在线服务器导航 ：

MCP官方服务器合集： https://github.com/modelcontextprotocol/servers

MCP Github热门导航： https://github.com/punkpeye/awesome-mcp-servers

https://mcp.so/

https://mcpservers.cn/

https://smithery.ai/

以cursor举例，将mcp server的功能添加到大模型之中。

![原文图片](assets/1958b3b60003.jpeg)

将对应的json配置信息添加到mcp.json文件中，在上面页面刷新，变绿即添加成功。

![原文图片](assets/bb9f794a5bf2.jpeg)

调用大模型时要选择agent模式

![原文图片](assets/c5c20bf2b585.jpeg)

用MCP实现秒回功能

视频： https://mp.weixin.qq.com/s/0EILiRUgHlNtPrCdDJm28g

代码： https://github.com/saintGeorge13/wx-mcp/tree/main
