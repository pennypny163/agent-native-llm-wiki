---

source_id: juliet-llm

source_file: "居丽叶LLM体系知识搭建.docx"

source_section: "3 RAG篇"

generated: true

---



# 3 RAG篇

## 3.1 RAG

RAG（检索增强生成） 是一种结合 信息检索 和 文本生成 的技术，旨在通过引入外部知识库提升生成模型的事实准确性、相关性和多样性。其核心思想是： 在生成答案前，先从大规模文档库中检索相关上下文，再基于检索结果生成最终输出 。RAG就像是让大模型开卷考试，不必再死记硬背所有知识，而是根据用户问题先去查参考书，然后再进行回复。

下图参考： RAG From Scratch

![原文图片](assets/152555587ee9.jpeg)

RAG有哪些好处？

提升生成内容的准确性 ：通过引入外部知识库的信息，能够在生成文本时补充模型自身的知识缺陷，提高生成内容的准确性和可靠性。尤其是在特定领域中，RAG可能检索到相比模型训练时更丰富的知识。

即时更新知识 ：RAG模型具备检索库的更新机制，可以实现知识的即时更新，无需重新训练模型，从而提供与最新信息相关的回答。

增强可解释性 ：由于RAG模型的答案直接来自检索库，其回复具有很强的可解释性，用户可以核实答案的准确性，从信息来源中获取支持。

缓解幻觉问题： 让大模型避免对不了解的内容进行胡说八道。

本地数据的隐私性 ：很多企业数据是不能上传云端，或者进行模型训练的。

RAG对比模型微调：

| 特性 | RAG技术 | 模型微调 |
| --- | --- | --- |
| 知识更新 | 实时更新检索库，适合动态数据，无需频繁重训 | 存储静态信息，更新知识需要重新训练 |
| 外部知识 | 高效利用外部资源，适合各类数据库 | 可对齐外部知识，但对动态数据源不够灵活 |
| 数据处理 | 数据处理需求低 | 需构建高质量数据集，数据限制可能影响性能 |
| 模型定制化 | 专注于信息检索和整合，定制化程度低 | 可定制行为，风格及领域知识 |
| 可解释性 | 答案可追溯，解释性高 | 解释性相对低 |
| 计算资源 | 需要支持检索的计算资源，维护外部数据源 | 需要训练数据集和微调资源 |
| 减少幻觉 | 基于实际数据，幻觉减少 | 通过特定域训练可减少幻觉，但仍然有限 |

### 3.1.1 基本步骤

Indexing：建库

数据收集与处理 ：系统从各种数据源（如文本文件、PDF、网站、数据库或API）中收集数据，并 转换成统一的纯文本格式 。

数据分割 ：将处理后的文本 分割成适当大小的块 ，以便于后续的检索和管理，常用分割方法有 固定长度分块、重叠分块 等，此过程可以省略，详见 Chunking-free RAG篇。

向量化表示 ：使用预训练的模型（如BERT、BGE等）将文本块转换为 向量表示 ，这些向量捕获了文本的语义信息，详见 embedding篇 。

索引构建 ：将这些向量存储在专门的数据库中，构建 索引结构 （如倒排索引或向量索引），以便快速检索，详见 向量索引篇。

indexing阶段可以 离线运行，不参与与用户的实时交互。

Retrieval：检索

查询编码 ：当用户提交查询时，使用 相同的编码器 将查询转换为向量表示。

相似性计算 ：计算查询向量与索引中的文档向量之间的 相似度 ，常用的相似性度量方法包括余弦相似度和欧氏距离。

排序与选择 ：根据相似度得分对文档进行排序，并选取 排名最高的前K个文档或 文档片段作为与查询最相关的文档。

查询优化 ：进行 重新排序或过滤 ，以提高检索结果的质量，详见 ReRank篇 。

Generation：生成

上下文整合 ：将检索到的文档片段与用户的原始查询结合，形成一个连贯的提示（ prompt ），为生成模型提供丰富的上下文信息。

生成响应 ：生成llm模型基于这些 上下文信息和原始查询生成最终的回答 。生成的文本不仅利用了检索到的信息，还结合了模型的语言生成能力，以确保回答的准确性和流畅性。

输出优化 ：在生成阶段，可能会加入后处理步骤，如答案的 置信度评估 、 多候选答案筛选 、 格式解析 等，以确保生成的答案是相关且准确的。

Retrieval和Generation阶段 在线运行，对每个用户查询都会实时执行 ，确保系统能够利用最新的知识库信息提供准确回答。

下图描述了RAG的基本流程，文档存储在向量数据库中，新的用户查询进来之后，首先向量数据库中检索相关的文档，将检索到的文档加到prompt中，由大模型负责生成回复。

![原文图片](assets/49afa27ca63e.png)

RAG的核心优化方法主要有两方面 ：

如何根据用户查询检索到所有最相关的知识

如何根据知识生成准确的回复，并且支持多轮交互

### 3.1.2 query translation

属于rag pipeline的第一阶段，目的是为了将question变成 更容易检索的形式 ，提升retrieval的效果。

![原文图片](assets/9acdd0567389.jpeg)

Multi Query

将question 从多个角度重写（例如同义词替换、相似语义拓展、删除冗余词、纠正错误和标准化表述等） ，再每个question上都retrieval， 查询结果取并集 ，获取更全面的文档集合。

Python
def get_unique_union(documents: list[list]): 
 """ Unique union of retrieved docs """ 
 flattened_docs = [dumps(doc) for sublist in documents for doc in sublist] 
 # 获取唯一文档 
 unique_docs = list(set(flattened_docs)) 
 return [loads(doc) for doc in unique_docs]

![原文图片](assets/4d322a701ec0.png)

RAG Fusion

对于检索到的文档做相互排名（Reciprocal Rank Fusion，RRF）， 通过加权各个question在文档中的查询结果，得到一个综合排名，并取前几名

Python
def reciprocal_rank_fusion(results: list[list], k=60): 
 # k: 参数，默认值为60。用于平滑排名得分，使得较高的排名对得分的影响更大，但不会过于极端。 """ 
 # 存储每个唯一文档的融合得分 
 fused_scores = {} 
 for docs in results: 
 for rank, doc in enumerate(docs): 
 doc_str = dumps(doc) 
 if doc_str not in fused_scores: 
 fused_scores[doc_str] = 0 
 previous_score = fused_scores[doc_str] 
 # 使用RRF公式更新文档的得分 
 fused_scores[doc_str] += 1 / (rank + k) 
 # 根据融合得分对文档进行降序排序: 
 reranked_results = [ (loads(doc), score) 
 for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True) ] 
 return reranked_results

![原文图片](assets/9cdac5a4df1d.png)

Decomposition

将原始query拆解成多个子问题，主要有两种实现方式：

每个子问题都会影响后续子问题的提问和解答过程，类似 逐步推理 。

![原文图片](assets/5a98640bf75c.png)

Python
q_a_pairs = "" 
for q in questions: 
 rag_chain = ( 
 {"context": itemgetter("question") | retriever, 
 "question": itemgetter("question"), 
 "q_a_pairs": itemgetter("q_a_pairs")} 
 | decomposition_prompt 
 | llm 
 | StrOutputParser())
 answer = rag_chain.invoke({"question":q,"q_a_pairs":q_a_pairs}) 
 q_a_pair = format_qa_pair(q,answer) 
 q_a_pairs = q_a_pairs + "\n---\n"+ q_a_pair 
 # 通过累积`q_a_pairs`，之前的问题和答案不断地加入到背景信息中，
 # 使得LLM在处理当前问题时能参考之前 问答的内容

每个子问题互相不影响 ，最后合并答案。

![原文图片](assets/e29ce492a4a6.png)

Python
def format_qa_pairs(questions, answers):
 formatted_string = ""
 for i, (question, answer) in enumerate(zip(questions, answers), start=1):
 formatted_string += f"Question {i}: {question}\nAnswer {i}: {answer}\n\n"
 return formatted_string.strip()
context = format_qa_pairs(questions, answers)

Step Back

从一个具体的问题出发，通过给一些few-shot的方式，生成一个 更高层次、更抽象的问题 ，以便于检索到相关文档。例如从问某人的学习成绩到问对某人的评价。

HyDE（hypothetical_document_embeddings）

与以上不同，HyDE根 据用户输入的question生成一些假设的doc ，这些doc与文档更接近，利用这些doc检索相关的知识。这样做的直觉是：由模型生成的回答会包含与查询语义相关的词汇和信息，可以作为查询的丰富语义表示，从而找到那些没有直接关键词匹配但语义相关的文档。

HyDE大致可以分为三个步骤：

首先使用一个生成式语言模型（如GPT）根据输入查询生成一篇内容丰富的 假设性回答文档 （即使这个文档在知识库中并不存在）；

然后将生成的假设文档 输入编码器生成嵌入向量表示 ；

最后利用该向量 去检索知识库中与之 语义相似 的真实文档。

HyDE的优点 ：

对于专业领域或长尾问句，直接基于关键词的匹配效果可能不佳，而通过生成一个“理想答案”再去搜索，能显著提高召回的相关性和丰富度。在没有大规模标注数据的情况下， HyDE 属于一种 零样本 的增强检索策略 ，对垂直领域（金融、医疗等）的长尾问题尤其有效。

样例 ：用户查询“保险销售技巧”。传统检索可能只针对“销售”或“保险”检索，结果不一定全面。应用 HyDE 时，我们先让 LLM 根据这一查询生成一段 假设回答 ，例如：“保险销售技巧包括了解客户需求、建立信任、提供专业建议”，假设回答丰富了查询关键词，有更大概率找到相关的文档。

Python
def hyde_retrieval(query: str, embed_model, doc_embeddings, doc_ids):
 # 1. 使用LLM生成假设文档
 prompt = f"请针对以下问题给出详细的回答：{query}"
 response = openai.ChatCompletion.create(
 model="gpt-3.5-turbo",
 messages=[{"role": "user", "content": prompt}]
 )
 hypo_doc = response["choices"][0]["message"]["content"]

 # 2. 将生成的文档进行向量化
 query_vector = embed_model.encode(hypo_doc)

 # 3. 在向量空间中检索相似文档
 # （这里假设已有知识库文档向量 doc_embeddings 和对应的 doc_ids 列表）
 # 计算与所有文档向量的余弦相似度，并选取最高的若干
 import numpy as np
 sims = np.dot(doc_embeddings, query_vector)
 top_idx = sims.argsort()[-5:][::-1] # 取前5个相似度最高的文档索引
 results = [(doc_ids[i], sims[i]) for i in top_idx]
 return results

![原文图片](assets/784e9bbb9ea0.png)

### 3.1.3 Routing

属于RAG pipeline的第二个阶段，目的是 根据question查到正确的数据源 ，实际是一个分类任务。首先要根据用户问题做意图识别：

基于规则的方法 ：使用预先定义的关键词或模式来判断意图。 根据领域知识，列出与各类意图相关的关键词集合，匹配用户 query 中出现的词来分类。 此方法实现简单直接，对已知意图效果好。缺点是对未包含的表达方式鲁棒性差，需人工维护规则库。

例子：如果用户 query 中包含“ 报销”“费用” 等关键词，判定为 报销流程查询 ；如果包含 “销售”“技巧” 等词，判定为 保险产品销售技巧 。

基于机器学习的方法 ：收集大量的意图识别的样本， 对预训练的模型（如BERT）继续微调。 相比规则方法，ML 模型对同义表达更鲁棒，能捕获上下文语义特征。缺点是需要标注数据进行训练。

基于特征工程的方法 ： 通过精心设计的Prompt直接让大模型判断意图类别。 可以提供若干意图类别描述，让模型选择最适合的类别。此方法不需要额外训练数据，在零样本或少样本场景下效果好。

识别出意图之后，就可以将用户问题route到最相关的资源库中进行查询。

Logical routing

拥有多个资源库，将用户查询route到最 相关的资源库 中进行查询。

![原文图片](assets/0954b27658b7.png)

Semantic routing

通过 语义相似度 进行路由， 一种特别有用的技术是使用embeddings将query路由到最相关的prompt。

![原文图片](assets/567481ee9118.png)

### 3.1.4 Query Construction

Query Construction是RAG pipeline的第三个阶段，利用命名实体识别等技术将 自然语言question转成合适的搜索和过滤参数 ，根绝关键词从数据库中的中进行搜索。

用户query：how to use multi-modal models in an agent, only videos under 5 minutes

输出：

content_search: multi-modal models agent

title_search: multi-modal models agent

max_length_sec: 300

![原文图片](assets/bc60d209f537.png)

![原文图片](assets/f9f88c76191e.png)

### 3.1.5 Indexing

Rag pipeline的第四阶段， 将文档拆成vector形式，建立索引 。

Chunking

分块（chunking）是将 大块文本分解成小段 的过程，直接影响系统的检索质量和生成效果：

检索精度和相关性 ：合理的切分能 保证每个chunk的语义完整性 ，更准确的匹配用户意图，降低不相关内容被一同检索的可能性。

向量表示与相似度计算 ： 能产生更精确的语义向量表示，使相似度计算更加准确 ，并且可以加速相似度计算和索引查找过程

生成质量优化 ：合理的切分能在不超过模型最大输入限制的情况下提供足够上下文，提高输入给模型的信息密度和质量， 减轻模型幻觉

实际应用考量 ：不同领域可能有不同的切分策略， 保留和添加适当的元数据可以提升检索效果。

现有的一些分块方案：

FastGPT、Langchian-Chat、 Baidu千帆知识库、星火知识库、Jina

基于 Langchain 的分块方案：

Character ：按固定字符数分割。 可以设置重叠字符来保持上下文

Recursive ：Langchain的默认文本分割器，它按不同的字符递归地分割文档（默认使用[“\n\n” ,"\n" ," ",""]），按照顺序逐个遍历列表中的分隔符直到块足够小为止，可以实现结构化的文档切分。 可以设置重叠字符来保持上下文。

Token ：按照token数量进行分块。常用的分词器有BPE、tiktoken等

Document ：使用特定的分隔符或规则进行分割，如markdown中的标题符号、Python代码中的类和函数等。

Semantic ：通过计算句子间embedding距离，把具有相似主题或内容的句子分为一块。

Agentic ：最高级别的chunking方法，通过LLM做决策，将文本分块为独立的命题。

分块时应该考虑的因素：

被索引内容的性质是什么 ? 是处理较长的文档(如文章或书籍)，还是处理较短的内容(如微博或即时消息)？

使用的是哪种Embedding模型 ？例如，sentence-transformer模型在单个句子上工作得很好，但像 text- embedt-ada -002 这样的模型在包含256或512个tokens的块上表现得更好。

对用户查询的长度和复杂性有什么期望 ？用户输入的问题文本是简短而具体的还是冗长而复杂的？这也直接影响到我们选择分组内容的方式，以便在嵌入查询和嵌入文本块之间有更紧密的相关性。

如何使用检索结果 ？ 例如，它们是否用于语义搜索、问答、摘要或其他目的？

一个比较好的文档解析

统一文档解析与OCR改进 ： 构建通用的解析模块，针对不同格式分别处理：

PDF解析： 优先使用文本层提取（如pdfplumber或PyMuPDF读取），保持读取顺序；对于扫描PDF或嵌入的图片，调用OCR引擎（如 Tesseract 或 PaddleOCR）。特别地，OCR时针对表格区域采用专门处理（例如先检测表格边框或使用表格OCR算法），确保按单元格顺序输出文本；对于代码块图片，可设置OCR保持换行和空格格式。（这里推荐Marker和 MinerU ）

PPT解析： 利用幻灯片结构提取标题和文本框内容。每页幻灯片输出时保留其标题，项目符号列表作为子内容。对于包含图片的幻灯片，可对图片执行OCR（如截图后OCR）以提取其中的文字说明。

纯文本解析： 直接按行/段读取，识别格式中的特殊标记（例如Markdown的 代码 块或表格格式）加以处理。确保代码块保留缩进和换行，表格按行列分隔保存。

视频解析： 先通过语音识别得到逐句字幕，再按时间戳或内容语义将字幕合并成段落。可以利用现有ASR工具获取准确的转录文本，并根据视频内容结构（章节或PPT同步内容）对转录文本分段。

智能Chunk切分（规则 + 语义融合） ：在得到完整文本后，按照文档的自然结构和语义连贯性进行分块：

基于规则的切分 ：利用文档格式特征，如章节标题、段落换行、列表项、表格边界等作为切分点。一旦检测到新的章节点或列表起始，就结束当前Chunk开启新Chunk。对于表格和代码块，整段内容视为一个Chunk，避免中途截断。

语义连贯的调整 ：在规则初切分后，检查相邻Chunks的内容连贯性。如果发现某Chunk过短且与前后段落语义上紧密相关（例如上一个Chunk以冒号结尾或内容未完结），则可以和相邻Chunk合并，确保信息完整。例如跨页的段落，如果下页开头并非新章标题，则应与前页末尾合并为同一Chunk。再如表格跨越多页时，将各页片段合成为一个整体表格Chunk。通过简单的NLP或embedding相似度检测，也可判断段落主题是否延续，辅助决定是否合并或继续切分。

长度和平衡 ：在保证语义完整的前提下控制Chunk长度，使其适合向量检索和后续模型处理（例如不超过512字或一定token数）。过长则适当按语义次级节点再拆分，过短则与相邻补充。最终每个Chunk都应是自含意义明确的一段内容。

层级结构与标签管理 ：为每个Chunk附加丰富的元数据标签，保留其在原文档中的位置和语境：

章节层级标签 ：在解析阶段捕获文档的层次结构（例如章节编号/标题、二级标题等）。实现方式可以是依据格式（PPT的标题框、PDF文本的字体大小/序号）识别标题行，并维护一个层级栈。例如检测到“1 总则”属于一级标题、“1.1 范围”属于二级标题等。分块时，将当前Chunk所属的所有上级标题作为一个层级列表存入标签。如此每个Chunk都带有类似“总则 > 范围”的层级路径。检索时可以将这些标题一起参与索引，提高召回率（例如用户搜索某章节名时也能匹配相关Chunk）。

内容类别标签 ：标注Chunk的内容类型和主题类别。例如标记Chunk是否为“表格”、“代码块”或普通文本，“政策条例”还是“操作指南”等。这可通过解析时的内容特征判断（如检测到多列文本则标记表格，包含代码格式则标记代码段）。也可以结合业务定义的类别（如财务制度、销售策略）作为标签。这些标签在检索时可用于过滤或作为额外特征提高准确匹配度。

引用与来源 ：每个Chunk还应记录来源文档名、页码或幻灯片编号等，以便命中后追溯原文。同时这些信息可在生成答案时用于引用出处。

Multi-representation indexing

将 用于答案生成的文档与用于检索的参考文档解耦 。

建库时建立一个包含完整文档的 docstore ，再利用llm做对文档做总结，建立一个 vectorstore 用于检索。对于输入的question，先与每个文档的总结进行相似度匹配，再根据匹配到的总结在完整的docstore中查询。

![原文图片](assets/721dc298029f.png)

该方法特别适用于 图像和表格 ，解决了直接嵌入表格或图像（多模态嵌入）的挑战，使用总结作基于文本相似性搜索。

RAPTOR

"低层次"的query，指那些只需要单一文档就可以回答的query；"高层次"的问题，指那些需要多个文档结合才会回答的query。此时，典型的kNN检索可能并不适用，因为kNN检索只能检索有限数量的文档块。

通过创建捕捉更高层次概念的文档摘要来解决这个问题。嵌入并聚类文档，然后总结每个聚类。以 递归 的方式这样做，产生一个包含越来越高层次概念的 摘要树 。摘要和起始文档一起被索引，覆盖用户query的范围。

![原文图片](assets/985289e11f68.png)

ColBERT

文档和问题都先被分解成一个个词（Tokens），然后分别对每个词进行嵌入，得到词级别的嵌入向量。对于问题中的每个词的嵌入，分别与文档中每个词的嵌入进行相似度计算，找到与问题中每个词嵌入最相似的文档词嵌入，并记录下它们之间的最大相似度。 然后，每个文档的得分是问题嵌入与文档嵌入中任何一个最大相似度的总和：

![原文图片](assets/a1be92c3c33c.jpeg)

### 3.1.6 Retrieval

混合索引

检索模块要根据用户查询，从索引中召回最相关的文档片段。首先使用Indexing阶段相同的embedding模型将用户查询向量化，然后计算用户查询与向量库中文档的相似度，选取排名最高的前K个文档或文档片段作为与查询最相关的文档。检索之后还可以进行重新排序，以提高检索结果的质量。

基础的检索算法有稀疏检索和密集检索两种： 向量语义检索擅长捕捉语义相似度，能找到包含同义表述的相关文档，但可能忽略精确的关键词匹配；而BM25等传统关键词检索对匹配查询关键词的文档非常有效。

稀疏检索

代表算法BM25，是一种基于关键词的检索算法，通过计算查询词与文档中的关键词匹配程度来评估文档的相关性。它使用TF-IDF（词频-逆文档频率）权重来衡量关键词的重要性。

词频（TF） ： 一个词在文档中出现的频率 。一个词在文档中出现的次数越多，它就越重要：

【公式开始】TF(t, d) = \frac{词汇t再文档d中出现的次数}{文档d中的总词数} 【公式结束】

逆文档频率（IDF） ：反映了 一个词在整个文档集合中有多罕见 。如果一个词在很多文档中都出现，那么它的重要性就低；反之，如果它在少数文档中出现，则它的重要性就高。

【公式开始】IDF(t) = log(\frac{文档总数}{包含词汇t的文档数量}) 【公式结束】

TF-IDF ： 【公式开始】TF-IDF(t,d)=TF(t,d)×IDF(t) 【公式结束】

BM25的核心思想是计算 查询词项和文档词项之间的相关性得分 ，然后综合这些得分来评估整个文档的相关性:

![原文图片](assets/e22cc87c8cb5.png)

![原文图片](assets/94872b9fd166.jpeg)

BM25的优点在于其简单性和有效性，它能够 快速 计算文档与查询的相关性得分，并且通常在实际应用中表现良好。然而，BM25也有局限性，例如它 不考虑词语的顺序和语义 。

密集检索

计算用户 查询向量与文档 之间的相似性，代表性指标有：

![原文图片](assets/9f601e8b0131.jpeg)

提供一个比较好的混合检索方案 ：

意图识别与路由 ： 通过简单的规则或训练分类模型对查询进行分类 。如果检测到查询是流程/制度类问题（通常包含“制度”、“流程”等关键词），则可以对BM25检索给予更高权重；如果是开放性思考类问题（包含“如何”、“怎么办”等），则侧重向量检索结果。此前置步骤保证不同查询走最合适的检索路径。

BM25检索 ：构建文档的关键词 倒排索引 （可使用Elasticsearch或其他搜索库），检索出Top N候选文档片段。BM25根据查询词在文档中的频率、文档长度等打分。 对于短查询，可直接采用BM25结果；对于长查询，BM25结果可作为补充 。

向量检索 ：利用Embedding模型将查询编码成向量，在Milvus向量数据库中进行近邻搜索，获取Top N候选片段。 向量检索能找出语义相关的内容，即使字面不匹配。

结果合并与去重 ：将两种检索的候选列表合并。由于BM25分数和向量相似度分值不在同一量纲，需进行 归一化 处理。例如，可将BM25分数归一到0-1区间，向量相似度天然在0-1（如余弦相似度）。然后按一定策略融合，如线性加权组合或者直接取两者结果集的并集。在组合过程中处理重复文档（相同chunk多次出现）以避免干扰。

提高召回率 ：混合检索确保潜在相关结果进入候选集。尤其在 只用向量或只用BM25无法检索到某些答案时，另一种方式可以补充，使真正相关的片段不被漏掉 。

Embedding模型训练

参考：《 Fine-Tune Embedding: The Secret to Improve Response Rates | iWeaver AI 》

预训练的Embedding模型可能在下游任务上表现不佳，体现在以下方面：

语义理解偏差 ： 模型可能将一般语境下相似的词判为相关，但在下游领域可能意义不同 （例如“保费” vs “费用”）。

同义词识别 ： 领域内常见的不同表述（如“推广”与“推销”）需要模型识别为相似。

重点概念强化 ：通过训练让模型强调领域高频概念，从而 在嵌入空间上将相关主题的文档聚类更紧密 ，提升召回 准确率 和 召回率 。

为了解决以上问题，可以收集大量下游任务的数据，特别收集用户问题和答案对作为正样本。再选择对Embedding模型进行 有监督微调、继续预训练或Cross-Encoder蒸馏 。

有监督微调 ：使用领域 问答对或相关性标注的数据 ，通过 度量学习 损失函数（如 Triplet Loss 或 MultipleNegativesRankingLoss 等）训练模型，使得相似问句-文档对的向量距离更近，不相关对更远。

继续预训练 ：将Embedding模型（如BGE）在大量 无监督文本 上继续训练（如通过 Masked Language Model 任务或者 对比学习 ），让模型嵌入空间更贴合领域分布。

Cross-Encoder蒸馏 ：用一个强大的 交叉编码器 （如一个微调后的BERT问答模型）生成query-doc相关性得分，然后 微调bi-encoder的Embedding模型去拟合这些得分，实现知识蒸馏。

Rerank

经过混合检索得到的文档可能只有部分与问题相关（这一过程也被称为粗排），这就需要进行rerank精排。常用的rerank模型是 Cross-Encoder 架构： 将查询和候选段落拼接输入一个Transformer模型，直接输出一个相关性分数，然后根据分数对候选段落排序。 由于Cross-Encoder在编码时考虑到了查询和文档之间的双向交互（Attention），相关性判断更准确，但计算成本较高，只适合对少量候选做精排。

更详细介绍见 3.4 Rerank 篇。

检索评估指标

参考：《 Evaluation Metrics for Search and Recommendation Systems | Weaviate 》

MRR（Mean Reciprocal Rank，平均倒数排名） ： 关注第一个相关结果出现的位置，反映用户是否能很快找到答案 。MRR是所有查询 Reciprocal Rank 的平均值，其中每个查询的 Reciprocal Rank = 1/(相关结果的排名)。如果相关结果总是排在第一，MRR=1；如果相关结果平均排在第三位，MRR≈0.33。MRR适合评估问答场景下 第一个正确答案 的易得性。

NDCG（Normalized Discounted Cumulative Gain，归一化折损累计增益） ： 考察整个排名列表的质量 ，包括多个相关结果的贡献 。它考虑结果的相关性等级和排名次序，通过折损因子（如1/log2(rank+1)）给排名靠后的相关结果降低权重。NDCG进行归一化以便不同查询间可比，值在0到1之间，1表示理想排序。 NDCG@K通常用于评估Top K结果的综合相关性排序。

Precision@K（P@K，前K精度） ： 衡量在返回的前K个结果中，有多少比例是相关的。 例如Precision@5 = 前5个结果中相关结果数量/5。它直接反映用户看前K条结果能找到多少正确答案， 不考虑顺序 （非rank-aware指标）。常和 Recall@K （在所有相关文档中前K找到多少）一起使用。

Recall@K（召回率） ： 相关文档中有多大比例在前K结果里。 由于问答系统往往每问只需一两个相关片段即可回答，有时Precision和MRR更受关注，但在多文档综合场景下Recall也重要。

总结以上的方法：

混合检索 ：结合 BM25 和 向量相似度 ，弥补单一检索缺陷，确保不同类型查询都能召回相关文档 。

Embedding模型微调 ： 在下游语料上微调Embedding ，使模型更懂领域语言，提高语义匹配效果。

结果重排 ：采用 Cross-Encoder对候选段落重新打分排序 ，显著提升相关结果排名靠前的概率。

评估指标 ：用 MRR、NDCG、P@K 等指标验证召回和排序效果的提升，指导迭代优化。

混合检索和模型微调侧重 提高召回率 ，重排序侧重 提升准确率

### 3.1.7 Generation

将检索到的相关文档与原始查询合并，形成更丰富的上下文信息，作为生成模型的输入，生成连贯、准确且信息丰富的回答或文本。

Python
from langchain.prompts import ChatPromptTemplate
# 一个参考模板
template = """你是一个xx领域的专家，请结合从知识库中检索到的相关文档，回答用户问题：
### 问题: 
{question} 
### 上下文: 
{context} 
### 答案:
"""
prompt = ChatPromptTemplate.from_template(template)

生成阶段面临的问题：

多轮对话的语义连贯性不足 ：在用户多轮提问时，如果新问题是对上一轮回答的跟进（例如用户问：“这个怎么申请？”），系统需要理解“这个”指代什么。缺少对话上下文的关联可能导致LLM误解提问，给出不相关或幻觉的答案。

多模态知识的利用困难 ：金融保险领域的知识库包含PDF手册、PPT演示、文本说明、视频讲解等多种形式。如果不对这些不同格式的数据进行预处理和结构化，检索时可能遗漏关键信息，导致答案不全面。

缺少来源引用降低可解释性 ：用户希望了解答案出处以建立信任。如果生成的答案没有标注来源，用户无法追溯信息真实性。特别是从长文档提取内容时，不注明具体出处会降低答案的可信度和可检查性。

针对以上问题，解决方案如下：

维护对话上下文，确保连贯 ：在每次用户提问时， 检测问题是否包含代词或省略（如“这个”“它”等）以判断是否为跟进问答 。如果是跟进问题，将 之前的相关问答摘要 或 关键术语 添加到当前查询中。 一种常见做法是 问题重写 ：将用户的新问题与上下文合并重写成完整问题，再送入检索和LLM 。与此同时，系统应维护一个对话历史状态，让LLM参考之前的问答或已检索的知识，避免因缺少背景造成误解。

整合多模态知识，提高答案全面性 ： 预先对PDF、PPT、文本、视频等资料进行解析和结构化处理，存入统一的向量数据库以便检索。 比如：

PDF/PPT ：提取文字内容，保留章节标题、表格数据等结构信息，将长文档按段落或页面切分成知识片段（chunks），并为每个片段添加文档名称、页码/幻灯片编号等元数据。

视频 ：对讲解视频执行语音转文本（ASR），获得字幕稿。根据时间戳将字幕稿切分成短段，并存储视频ID和时间段元数据。必要时可结合视频说明文字或关键帧截图的文字说明。

将不同模态的数据转换为统一的文本嵌入向量，以便用同一种检索方式获取相关片段（例如使用同一嵌入模型表示文本和语音转文本）。或者采用 多模态检索 策略：分别在文本库、图像/视频库中检索，再融合结果。

在生成答案时，允许LLM综合多个来源的片段。例如同时引用保单PDF中的条款和培训视频中的说明，以形成完整答案。

3. 在答案中加入来源引用，增强可解释性 ： 设计提示（Prompt）要求LLM在给出答案时 标注信息来源 。例如，让模型在句末用括号注明来源文档名称或索引编号。实现方法可以是：在将检索到的文档片段传递给LLM时，附加标记（如【1】、【2】）或者直接提供“引用格式”的文本，让模型仿照引用格式回答。对于长文档的引用，如果答案来自同一资料的不同部分，可以拆分引用为【文档A，第10页】、【文档A，第15页】等，精确指明出处。生成策略上， 可以使用RAG的 引用增强模式 ，即模型严禁脱离提供的知识片段编造答案，确保每句都有据可依。 最终答案输出时，将源文件名称或链接映射为用户可查看的引用，以便用户点开核实内容。这种动态插入引用的方式保证了答案的可溯源性，减少幻觉，增加用户信任。

### 3.1.8 RAG面临的问题

![原文图片](assets/fbfa5177589d.png)

内容缺失 ： 知识库中缺失上下文 ，rag只能提供不精确、甚至是错误的答案。

解决方案：可以通过 数据清洗 和 prompt优化 （比如在prompt中加入“如果你不确定答案是什么，就告诉我你不知道”的提示，防止模型胡说八道）缓解。

错过排名靠前的文档 ：由于 检索时缺乏上下文，导致检索到的关键的文档排名靠后 ，没有返回给用户。

解决方案：可以通过 chunk_size 和 similarity_top_k 平衡计算效率和质量，以及采用 Rerank算法 。

不在上下文中 ：无法将检索到的文档全部放在输入模型的上下文中，尤其是检索到大量文档时。

解决方案：使用 长上下文 的方法，例如需要对文档进行合并、插值等。

未提取 ：LLM倾向于检索近似值而不是精确值，导致 包含很多不相关的甚至互相矛盾的信息 ，可能因为这些噪音损害响应质量。

解决方案： 数据清洗，压缩prompt ，避免 中部丢失问题 （模型对输入上下文开头和结尾的信息理解能力更强，应避免将关键的信息放在中部）。

格式错误 ： LLM 忽视了 提取特定格式 的信息（如表格或列表）的指令。

解决方案：prompt中给出 示例 ，简化清晰prompt，对 输出进行解析 。

特异度不正确 ：输出的粒度与输入不一致，比如用户问题很具体，模型回答很宏观；或者用户问题包含详细的上下文，模型生成简短的回复。

解决方案：改进检索策略，如从 小到大检索、句子窗口检索、递归检索； 在prompt中引导模型生成特定粒度的内同。

不完整 ： 输出只回答了输入的部分问题 。

解决方案：之前RAG的文章中提到的一些方法，如 routing 到最相关的文档库， 用户查询重写 和 分解成子问题 。

### 3.1.9 RAG 效果评估

可以从以下角度进行评估。

准确率/召回率评估

评估RAG系统回答问题的正确性和检索相关性，更多指标详见 3.1.6 Retrieval 检索评估指标 。主要包括：

答案准确率 ： 比较生成的答案与标准答案的匹配程度 ，可使用自然语言处理中的评价指标如 BLEU （衡量n元语法匹配程度）、 ROUGE （衡量召回的n元语法覆盖率）等来量化答案与参考答案的相似度。

检索召回率 ： 评估检索模块是否找到了包含正确答案的文档。 例如计算 Top-k召回率 （正确答案所在文档是否出现在前k个检索结果中）以及 MRR（平均倒数排名）、NDCG（归一化折损累计增益） ，以衡量正确文档在检索结果中的位置（MRR越高表示相关文档排名越靠前）。

可信度评估

衡量生成的答案在多大程度上有文档支持，以及答案内容和检索到的文档是否一致、可靠。具体包括：

答案与支持文档匹配度 ： 验证生成答案中的关键信息是否能在检索文档中找到。 可以计算答案和支持文档之间的相似度或重合率，例如关键词重叠度。

文档覆盖率 ： 检查检索到的文档是否覆盖了回答所需的所有要点。 如果答案涉及多个要点，评估这些要点是否均能在提供的文档集合中找到依据。

响应速度评估

评估RAG系统处理查询的速度，包括：

平均响应时间 ：系统处理单个查询的平均用时。

P95/P99 延迟 ：95%和99%的请求在多少时间内完成（尾部延迟）， 用于评估最慢响应的情况 。

整体响应分布 ：可以绘制响应时间分布图（如直方图）来了解大部分查询的延迟范围。

可扩展性评估

测试RAG系统在不同数据规模和负载下的性能表现 ，包括：

数据规模扩展 ：增大知识库或文档集规模，观察检索和生成性能的变化（如 响应时间是否随数据量线性增长，检索准确率是否保持稳定 ）。

吞吐量 ：衡量系统 每秒可处理的查询数（QPS） ，以及在高并发情况下的性能表现。

用户体验评估

系统给用户带来的主观感受和易用性，包括：

人工满意度评价 ：通过 人工评估或用户反馈 来打分，衡量用户对答案的满意度。例如收集用户评分（1-5分）或对答案是否解决问题的二元反馈，以计算平均满意度分或满意率。

答案可读性 ： 评价生成答案表述的清晰易懂程度 。可以使用 可读性评分 （如基于句子长度和词汇复杂度的指标）来定量分析答案文本的可读性，确保答案语言简洁明了，便于用户理解。

### 3.1.10 RAG 加速

想要实现RAG系统加速，也就是提升首字响应速度，就要首先找到消耗时间最长的步骤，并对其进行加速。RAG的时间占用主要分为4个部分：

查询向量embedding

向量检索

构建上下文

infra时间 ，包括网络 / 队列 / I/O等。

Embedding阶段

假设此阶段调用openAI API实现。

存在问题：

| 问题 | 加速手段 |
| --- | --- |
| 网络往返多、一次只算一条 | 批量请求 (batch) |
| I/O 等待 | 异步并发 (asyncio + semaphore) |
| 重复文本反复算 | Redis/KV 缓存 |
| 模型本身推理慢 | 小模型 / 量化 / 本地部署 |

批量Embedding ：可以把 待嵌入的多个查询或文本段组合成数组传入单次API调用，避免逐条请求所带来的网络开销 。 请求不能超出最大token限制。

并发调用与异步处理： 异步非阻塞调用能让CPU空闲时间用于处理其它任务 ， 从而提升整体吞吐。 通过Python的 asyncio 等异步框架，可以在等待一个Embedding结果时并行触发其他请求 。实践中OpenAI对并发请求有一定限制，过高并发可能引起排队延迟，一般将并发控制在个位数，并监控接口返回的速率限制信息。

缓存Embedding结果： 对于常见问题或频繁查询，可以在首次获取Embedding后将 query->embedding 键值对存入内存或Redis缓存。下次遇到相同查询时直接复用缓存向量，跳过API调用，从而显著降低延迟。 需要设计缓存键（可用查询字符串或其哈希）并考虑到语义相近但不完全相同的查询不会命中缓存的情况。 对于文档语料， 尽量预先计算并存储Embedding ，避免在查询时现算 。

Python
pip install openai redis tiktoken
import os, json, asyncio, hashlib, redis, tiktoken, openai
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL, DIM = "text-embedding-3-small", 1536
enc = tiktoken.encoding_for_model(MODEL)
redis_cli = redis.Redis(host="localhost", decode_responses=True)
def _key(text):
 return "emb:" + hashlib.sha1(" ".join(text.split()).lower().encode()).hexdigest()
async def _embed_batch(batch):
 resp = await openai.Embedding.acreate(model=MODEL, input=batch)
 return [d["embedding"] for d in resp["data"]]
async def embed(texts, concurrency=5, token_cap=8191):
 # ① 批量分组
 batch, cur, out, sem = [], 0, [], asyncio.Semaphore(concurrency)
 async def run(b): # ② 异步 + 并发
 async with sem: return await _embed_batch(b)
 async def push(): # 发起单批
 nonlocal batch, cur; out.extend(await run(batch)); batch, cur = [], 0
 tasks = []
 for txt in texts:
 if (vec := redis_cli.get(_key(txt))): # ③ 缓存命中
 out.append(json.loads(vec)); continue
 tok = len(enc.encode(txt))
 if cur + tok > token_cap and batch: tasks.append(asyncio.create_task(push()))
 batch.append(txt); cur += tok
 if batch: tasks.append(asyncio.create_task(push()))
 await asyncio.gather(*tasks)
 # ④ 把新算的结果写缓存
 for t, v in zip(texts, out):
 redis_cli.set(_key(t), json.dumps(v), ex=86400)
 return out

向量检索阶段

假设采用Milvius数据库。

| 痛点 | 加速手段 |
| --- | --- |
| 全库暴力扫 | ANN 索引（HNSW / IVF） |
| 海量数据串行查 | 批量 search + 多副本加载 |
| query 多但每次只看少量数据 | 分区 / 过滤 |
| CPU 饱和 | GPU or 水平扩容 |

优化索引 ： 采用近似最近邻算法构建索引，例如 IVF 、 HNSW 等 ，以大幅提升检索速度。IVF索引可调节细分簇数量( nlist )和查询探测范围( nprobe )，HNSW可调节每层节点数 efConstruction 。

批量查询与并发连接： Milvus支持在一次请求中执行 批量搜索 （即传入多个查询向量一起检索），这相比逐一查询能减少网络开销和调度开销，适用于需要同时回答多子问题或多用户批量请求的场景。对于并发请求量高的系统，可 在客户端维护连接池或使用多线程/协程并发查询Milvus 。Milvus 2.x的无锁架构对并发查询有良好支持，但仍需确保后端资源充足（CPU/内存不成为瓶颈）。如果QPS需求特别高，可以增加检索副本：Milvus允许在内存中加载数据的多个副本来提高并行查询能力。通过在 Collection.load() 时设置 replica_number>1 ，可以启用多副本使查询负载分摊到不同Query Node，从而提升整体吞吐。例如，将副本数设为4可显著提高QPS上限。同样，需要搭配增加Milvus后端的QueryNode实例数和计算资源，以充分利用副本带来的并行度。

优化数据分片与过滤： 利用Milvus的分区和过滤功能缩小检索范围，从而减少每次查询需要遍历的向量数量。如果先验知道查询只涉及某部分语料（例如按来源、时间分区的数据），可 将向量集合按属性切分成分区，查询时指定相应分区检索，避免全库扫描 。 对于规模超大的向量集合，合理分片（sharding）有助于降低单机内检索延迟 。同时剔 除过期或低相关的向量（例如对知识库定期清理无用数据）可减小索引规模 ，使查询更高效。

系统配置与硬件加速： 调整Milvus的配置以匹配性能需求。例如，在保证召回的前提下将搜索参数 efSearch （对HNSW）或 nprobe （对IVF）设为较小值以加快查询。确保在查询前调用 collection.load() 将数据加载至内存，并设置合适的 cache_config （Milvus会将常用数据页缓存在内存）。如果数据规模巨大或需要亚毫秒级查询延迟，可考虑GPU加速：使用Milvus的GPU版本或将向量数据托管到支持GPU的向量引擎上，以利用GPU的并行计算能力执行向量点积运算。不过GPU方案需要权衡部署成本，通常在超大规模或低延迟（如实时推荐）场景才需要。总体而言，充分利用Milvus的并行和内存特性。

Python
# pip install pymilvus==2.3.4
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

connections.connect(host="127.0.0.1", port="19530")

fields = [
 FieldSchema("id", DataType.INT64, is_primary=True, auto_id=True),
 FieldSchema("vec", DataType.FLOAT_VECTOR, dim=DIM),
 FieldSchema("txt", DataType.VARCHAR, max_length=1024)
]
col = Collection("rag_docs", CollectionSchema(fields))
# ① HNSW 索引（只建一次）
if not col.indexes: 
 col.create_index("vec", {"index_type":"HNSW", "metric_type":"IP",
 "params":{"M":16, "efConstruction":128}})

# ② 把向量加载到内存，并开 4 副本
col.load(replica_number=4) 

def search(vecs, k=5, ef=64):
 p = {"metric_type":"IP", "params":{"ef":ef}}
 res = col.search(vecs, "vec", p, k=k, output_fields=["txt"])
 return [[hit.entity.txt for hit in hits] for hits in res]

系统层级优化

异步架构与并发设计： 采用异步非阻塞架构以充分利用服务器资源，提高整体吞吐量。例如使用Python的 asyncio 或多线程池， 让Embedding计算、向量检索、LLM生成等步骤能够流水线并行或重叠执行，同时处理多个用户请求，在生成回答的同时预取下次检索 。针对高并发的场景，可引入任务队列（如RabbitMQ、Kafka）和工作进程批量处理请求。例如 积攒一定数量的查询统一进行Embedding或检索操作，以摊薄单次处理开销。 同时，可以部署 多实例LLM服务 （如果使用自托管模型）或使用 OpenAI多API Key分流 ，请求端做负载均衡以避免单点瓶颈。

引入缓存层（Redis等）： 在系统中增加缓存机制，用空间换时间，避免重复计算开销。缓存可存在多个层次： （1）Embedding缓存： 缓存常见查询文本的向量表示，下次出现直接复用；缓存文档向量同样重要，静态语料库可以离线算好全部向量并存入Milvus或KV存储 。 （2）检索结果缓存 ： 对于经常被查询的问题，其检索到的文档列表往往相同，可缓存这些文档ID列表 ，下次查询时直接使用缓存结果而无需访问向量库。 （3）答案缓存 ： 对于高度重复且答案固定的提问（如FAQ），可以直接缓存上一次的完整回答文本 。下次相同提问立即返回缓存答案，实现近乎零延迟响应。需要注意对于有时效性的数据（如新闻、股价），缓存过久可能失准，需设置适当TTL或在数据更新时主动清除相关缓存 。 使用Redis这类内存KV存储可以提供毫秒级的读取性能，适合做共享缓存层。同时通过哈希key（例如将query字符串规范化后哈希）索引缓存内容，并采用LRU等策略淘汰冷门条目。总之，缓存系统的引入能大幅减少重复调用OpenAI API和向量库的次数，从架构上加快响应。

Python
# Embedding缓存
EMB_TTL = timedelta(days=30) # 静态文档可更长

async def get_embed_cached(text: str):
 key = f"emb:{_hash(text)}"
 if (vec := _get(key)):
 return vec # 命中缓存
 vec = (await embed([text]))[0]
 _set(key, vec, EMB_TTL)
 return vec

# 检索结果缓存
SEARCH_TTL = timedelta(days=1) # 语料相对稳定，可按需调整

def search_cached(question: str, q_vec, k=3):
 key = f"srch:{_hash(question)}:{k}"
 if (hits := _get(key)):
 return hits
 hits = search([q_vec], k=k)[0] # 调 Milvus
 _set(key, hits, SEARCH_TTL)
 return hits

# 答案缓存
ANS_TTL = timedelta(days=7) # FAQ 可更长；时效数据可减小

async def answer_cached(question: str):
 key = f"ans:{_hash(question)}"
 if (ans := _get(key)):
 return ans # 秒级返回

 # —— 缓存未命中：正常 RAG 流程 ——
 q_vec = await get_embed_cached(question)
 docs = search_cached(question, q_vec, k=3)
 prompt = build_prompt(question, docs)

 # 不需要流式时可直接用 openai.ChatCompletion
 chunks = []
 async for tok in stream_chat(prompt): # 自行实现 yield token
 chunks.append(tok)
 answer = "".join(chunks)

 _set(key, answer, ANS_TTL)
 return answer

## 3.2 Chunking-free RAG

参考论文：《BGE Landmark Embedding: A Chunking-Free Embedding Method For Retrieval Augmented Long-Context Large Language Models》

RAG从大规模语料库中检索相关信息，将长文本压缩成简洁、关键的输入形式，以在不直接修改模型的情况下扩展上下文。为了提高检索效率， RAG在建库的时候需要将长文本拆成小块 ，为每个块生成embedding，通过比较用户查询和文档之间的embedding的相似度来检索最相关的块并作为输入。

分块带来了严重的问题：

破坏上下文连贯性 ：即长文本被切割成不连续的部分（为了尽可能保证连续性，每一块可以有一些 重复 的），会破坏上下文的完整性。当模型需要理解段落中的复杂关系或连续语义时，分块会使得这些语义信息被分散，导致嵌入表示的准确性降低。

信息不完整 ：检索系统容易选择显著性较高的块，然而其他重要但不显著的块可能会被忽略。这样一来，模型可能 无法获取完整的背景信息 ，影响检索的完整性。

为了解决分块带来的问题，提出了一种 Landmark Embedding 的方法，在chunking-free的情况下实现RAG。

![原文图片](assets/cf2108902b16.jpeg)

### 3.2.1 基础知识

大模型生成的过程可以用 【公式开始】max ( log LLM(x_t | q, ctx, X_{<t})) 【公式结束】 表示，即 根据用户query，context以及已经生成的文生成下一个词 。在上下文很长的情况下，传统的基于检索的方法将上下文分块，选择top k相关的作为上下文，但是分块会导致上下文连关系破坏以及信息不完整的问题。

Landmark Embedding提出一种不需要分块的检索方法 【公式开始】\gamma'(\cdot) 【公式结束】 ， 直接在一个完整的上下文内生成对查询最有帮助的信息表示 ：

【公式开始】C*: \{c_1,...,c_k\} <- \gamma'(q, ctx) 【公式结束】

【公式开始】c_i 【公式结束】 表示细粒度单元（例如句子）。拥有了完整的上下文信息，每个细粒度单元的语义信息都能被完整保留，这能保障对用户query进行精确的检索。

### 3.2.2 Chunking-Free架构

假设原始的上下文由n个句子组成： 【公式开始】\{c_1,...,c_n \} 【公式结束】 ，周期每个句子的末尾添加一个特殊的标记 landmark（LMK） ，用来 捕捉对应句子的底层语义 。 LMK和句子以及邻居上文一起编码 ，编码结果LE，被用来表示整个句子。

采用大语言模型（LLaMA-2-7B）对LMK和用户query进行编码，表示为：

![原文图片](assets/b5f4dc15a9d7.jpeg)

基于上述结果，用户query和每个句子之间的相关性表示为两个嵌入的 内积 ： 【公式开始】<E_q, LE_{i}> 【公式结束】 。如果进行编码时，输入比大模型的的上下文窗口大，采用 滑动窗口 的方式处理，如下图：

![原文图片](assets/9201bd2d677a.jpeg)

![原文图片](assets/a6701b9a0e67.jpeg)

### 3.2.3 位置感知目标函数（Position-Aware Objective）

LMK通过 对比学习 得到，对用户query有用的信息往往 聚集在连续的句子中 【公式开始】c_{z-m,..,c_z} 【公式结束】 。为保证检索到的信息尽可能完整，提出了一种位置感知的目标函数：

![原文图片](assets/d1df976b86ff.jpeg)

连续信息的处理 ：长文本中的信息通常是由多个连续句子共同传达的。不同于传统的“正样本”赋予等同权重的做法， Landmark Embedding为每个句子赋予不同的权重，权重值随着句子位置的接近性而递增 ，以确保文本信息的完整性。

位置权重 ：通过引入一个基于位置的权重函数，将句子的重要性随着它离信息“边界”的远近调整， 使最靠近边界的句子得到更高的权重 。具体地，目标函数会 通过对比学习方式训练Landmark嵌入 ，使得查询与其相关句子的嵌入相似度更高。

### 3.2.4 多阶段学习

提出了一个多阶段的训练方法，利用不同的数据来源来提升Landmark Embedding的嵌入质量，使 1)基本的 语义区分能力 、2) 上下文表示能力， 这两种能力能够在适当的训练数据之上逐步建立。LE初始化为 通用的句子级别的embedding model ，然后，将其增强为上下文表示模型，可以为其包含的句子生成判别嵌入。包含以下三个阶段：

远程监督 。首先，利用 MS MARCO 中的成对训练数据，基于此模型可以初始化为一个基本的 句子嵌入器 。在这里，Landmark Embedding采取特殊形式， 只有一个单独的LMK附加在答案上下文的末尾 ： 【公式开始】LE_a ← LLM(answer; LMK).embed[−1] 【公式结束】 。第一阶段训练遵循 密集检索 的基本训练形式，为每个query检索15个难负样本和批次内负样本

弱监督 。对成对训练数据进行了简单修改，模型被训练以 在长上下文中生成有区分性的句子嵌入 。具体来说， 随机打乱不同用户query的答案，并将它们合并为一个伪长文档 。第i个答案的嵌入可以生成为： 【公式开始】LE_{a_i} ← LLM(aj≠i, ..., ai; LMK).embed[−1] 【公式结束】 . 第二阶段仍然依赖于批次内负样本，其中来自其他答案的Landmark嵌入 【公式开始】LE{a_{j≠i}} 【公式结束】 被用作负样本。

微调 。 利用合成数据进行最终阶段的微调 。在这一步中，利用维基百科（Foundation）的真实长文档。对于每个长文档，随机采样一系列文本跨度，通过 提示LLM生成伪查询 。此外，它可能与真实世界数据分布不同。因此，只有少量合成数据被生成用于最终训练阶段。然而，得益于前两个阶段建立的基本能力，Landmark Embedding在适度微调后可以实现卓越性能。

## 3.3 向量索引

上一章介绍Indexing中提到，要将这些embedding后的向量存储在专门的数据库中，构建索引结构（如倒排索引或向量索引），以便快速检索。这就需要用到 向量数据库 了。向量数据库是一种专门用于存储、索引、查询和检索高维向量数据的数据库系统。它特别适合处理非结构化数据，如图像、音频和文本，能够实现传统数据库难以完成的高级分析和相似性搜索， 具备高效存储和处理高维向量数据的能力。

如何选择向量数据库？

常见的向量数据库包含 milvus、Elasticsearch、Faiss、Chroma 等，选择时可以考虑的因素有：

数据规模和速度需求 ：考虑你的数据量大小以及查询速度的要求。一些向量数据库在处理大规模数据时更加出色，而另一些在低延迟查询中表现更好。

持久性和可靠性 ：根据你的应用场景，确定你是否需要数据的高可用性、备份和故障转移功能。

易用性和社区支持 ：考虑向量数据库的学习曲线、文档的完整性以及社区的活跃度。

成本 ：考虑总体拥有成本，包括许可、硬件、运营和维护成本。

特性 ：考虑你是否需要特定的功能，例如多模态搜索等。

安全性 ：确保向量数据库符合你的安全和合规要求。

| 向量数据库 | Milvus | Elasticsearch | Faiss | Chroma |
| --- | --- | --- | --- | --- |
| 类型 | 分布式向量数据库 | 全文检索引擎（支持向量插件） | 向量搜索库 | 轻量级向量数据库 |
| 核心用途 | 大规模向量相似性搜索 | 混合搜索（文本+向量） | 高效向量相似性计算 | 快速原型开发和小规模向量存储 |
| 开源协议 | Apache 2.0 | Elastic License（部分功能商业限制） | MIT License | Apache 2.0 |
| 分布式支持 | ✅ 原生支持 | ✅ 原生支持 | ❌ 需自行扩展 | ❌ 单机为主 |
| 存储能力 | 支持持久化存储 | 支持结构化数据+向量 | ❌ 仅内存或需外部存储 | ✅ 内置轻量级持久化 |
| 索引类型 | IVF、HNSW、ANNOY 等 | HNSW、Flat | IVF、HNSW、PQ 等 | HNSW、IVF-PQ |
| 查询性能 | 高吞吐、低延迟（分布式优化） | 中等（适合混合查询） | 极高（纯内存计算） | 中等（适合小规模） |
| 易用性 | 中等（需配置集群） | 复杂（需调优索引和插件） | 低（API简单，但需集成存储和分布式） | 高（API简单，开箱即用） |
| 扩展性 | ✅ 水平扩展 | ✅ 水平扩展 | ❌ 需手动分片 | ❌ 有限 |
| 多模态支持 | ✅ 支持文本、图像、视频等向量 | ✅ 结合文本和向量 | ❌ 仅向量 | ✅ 支持文本和向量 |
| 社区生态 | 活跃（企业支持：Zilliz） | 极大（商业+社区） | 活跃（Meta维护） | 新兴（GrowingFast维护） |
| 典型场景 | 大规模推荐系统、图像检索 | 混合搜索（电商、日志分析） | 嵌入到应用中的相似性搜索 | 本地开发、小规模AI应用 |
| 优点 | 高扩展性、丰富索引算法、云原生支持 | 全文+向量混合搜索、成熟生态 | 极致性能、低延迟、易集成 | 简单轻量、快速部署 |
| 缺点 | 部署复杂、资源占用高 | 向量性能弱于专用库、商业功能限制 | 无原生存储和分布式支持 | 功能有限、不适合大规模数据 |

接下来深入探讨Milvus所支持的几种主要向量索引的原理：

### 3.3.1 ANNS

在处理高维数据时， 最近邻搜索 （NNS, Nearest Neighbor Search）是一个常见且重要的任务。NNS旨在通过给定的查询向量，快速找到数据集中最相似的若干个向量。这在图像检索、推荐系统、语音识别等应用中具有广泛的需求。然而，随着数据规模的增大，精确的最近邻检索通常会变得非常耗时和资源密集。因此， 近似最近邻搜索 （ANNS, Approximate Nearest Neighbor Search）应运而生。

ANNS的核心思想是在可接受的精度范围内，牺牲部分准确性，换取更高的检索效率。相比于精确检索，ANNS只需要 找到目标向量的近似邻居 ，而不是完全精确的邻居，从而在大规模数据集上大幅提升查询速度。Milvus 支持的向量索引类型大多采用ANNS算法，常见的索引类型的划分如下图所示：

![原文图片](assets/0563fc3ac3b8.png)

### 3.3.2 FLAT

这是最简单的索引方式，进行 暴力搜索（brute-force） ，可以保证精确度，但效率低，尤其在数据量大时。

适合场景：在小型、百万级数据集上寻求完全精确的搜索结果。

### 3.3.3 IVF_FLAT

IVF_FLAT 是一种基于 倒排 的索引方法，广泛用于在大规模数据集上实现高效的近似最近邻搜索。它适用于在精度和查询速度之间寻求平衡的场景。IVF_FLAT本身并没有进行量化操作，因此在精度和存储开销上相对保守，但能够提供较快的搜索速度。

![原文图片](assets/c2817e857f0c.png)

核心原理

聚类 ：IVF_FLAT通过 聚类算法（如k-means）将高维空间中的向量划分为多个子空间（簇） 。每个簇包含一组相似的向量，并且每个簇会有一个代表向量，通常是簇的中心点。

倒排索引 ：为每个簇创建倒排索引。 每个向量会被映射到它所属的簇 ，这样在查询时，系统只需关注与查询向量相似的簇，而不需要搜索整个高维空间，从而显著降低搜索的时间复杂度。

查询处理 ：

查询时，IVF_FLAT首先将查询向量分配到距离 最近的簇中心 （即子空间）。

然后在该簇内执行精确的 线性搜索 ，从而查找与查询向量相似的向量。

为了优化查询，IVF_FLAT使用一个参数 nprobe 来控制搜索的簇数。 nprobe 控制搜索时考虑的簇的数量，从而平衡查询精度和查询速度：

增大 nprobe 可以搜索更多簇 ，返回更多候选向量，提高结果的精确度，但查询时间也会增加。

减少 nprobe 可以缩小搜索范围 ，降低计算时间，查询速度更快，但可能会牺牲一些精度。

降低搜索成本 ：由于IVF_FLAT 通过划分子空间来限制搜索范围 ，它能够显著减少传统线性搜索所带来的高维数据中的计算开销，从而提高查询效率。与传统的暴力搜索方法相比，IVF_FLAT的时间复杂度大大降低，尤其适合在大规模数据集上使用。

适用场景：

IVF_FLAT适用于需要平衡精度和查询速度的场景，尤其是在大规模、高维数据集上，可以有效减少查询时间。它适合那些要求较高精度但能容忍一定查询延迟的应用。

### 3.3.4 IVF_SQ8

IVF_SQ8 是在 IVF_FLAT 基础上增加了 量化 步骤的一种索引方法，其核心思想与 IVF_FLAT 类似，但通过量化技术将存储和计算资源的消耗大大降低，尤其在磁盘、内存、CPU 和 GPU 资源的使用上节省了 70%-75%。IVF_SQ8通过 标量量化 （Scalar Quantization）将 每个维度的 4 字节浮点数表示压缩为 1 字节整数 表示。

核心原理

标量量化 ：IVF_SQ8 通过标量量化将每个向量的每个维度从 4 字节（通常是浮点数）压缩为 1 字节。量化的过程是将原始的浮点数值映射到一个较小的整数范围。例如，假设一个维度的原始值范围是 [0.0, 1.0]，通过量化后，该维度的数值会被压缩为整数值，这样可以显著节省存储空间并加速计算。

Quantized Vectors ：量化后的向量使用 整数 （如 uint8）来表示每个维度的值。通过量化，向量的存储空间大大减少，同时查询时计算量也降低。量化后的整数表示会根据原始值的分布划分为若干个区间。

倒排索引与聚类 ：与 IVF_FLAT 类似，IVF_SQ8 使用 聚类算法 （如 k-means）将高维空间中的向量划分为多个簇。每个簇内的向量都通过量化后的表示存储和检索。查询时，系统会将查询向量分配到与其最接近的簇中心，然后在该簇内执行快速的线性搜索。

![原文图片](assets/352d3a645e32.png)

### 3.3.5 IVF_PQ

IVF_PQ 是一种结合了 倒排文件和乘积量化 （Product Quantization, PQ）的高效索引方法，旨在加速大规模高维数据集的检索过程。它主要用于高维向量的近似最近邻搜索，通过将向量空间划分为更小的子空间并进行量化，显著降低了存储开销和计算复杂度。

倒排文件

倒排文件是一种高效的索引结构，用于存储和检索向量。在IVF_PQ中，数据集中的 每个向量被分配到一个或多个倒排表中 ，每个表包含了对应向量的标识符。查询时，我们首先在倒排文件中找到候选的向量集合，从而大大减少了搜索空间。 倒排文件特别适合于高维空间 ，因为它允许我们仅搜索与查询向量相似的部分数据，而不是遍历整个数据集。

乘积量化（PQ）

乘积量化是一种 将高维向量压缩为低维表示的技术 。它通过将向量划分为多个子空间，并对每个子空间进行独立的量化，生成一个 代码本 （codebook）。这样，原始的高维向量可以由多个子空间的量化表示组合而成，从而降低存储需求并加速检索。

在IVF_PQ中，乘积量化应用于IVF的聚类过程。每个簇的中心点会被进一步量化，原始的查询向量和数据向量在计算距离时，不是直接与每个簇中心进行计算，而是 与每个子空间的量化中心进行计算 。这种方法不仅降低了存储开销，还减少了计算距离时的运算量。

IVF_PQ的结合

IVF_PQ将倒排文件和乘积量化结合在一起，利用两者的优势来加速高维向量检索。具体流程如下：

量化与聚类 ：首先，数据集中的每个向量会被分为多个子空间，每个子空间进行乘积量化。接着，通过倒排文件将数据按簇组织。

查询流程 ：

查询时，首先 根据查询向量找到相应的倒排表 （即查询向量属于哪个簇）。

然后，在该簇内，使用乘积量化后的 代码本 来进行相似度计算，找到与查询向量最相似的向量。

这样，通过倒排文件限制搜索范围，并通过乘积量化精简计算过程，IVF_PQ大大提高了大规模数据集上相似向量检索的效率。

![原文图片](assets/f83d45983ee6.png)

### 3.3.6 HNSW

HNSW （Hierarchical Navigable Small World Graph）是一种基于图的索引算法，采用 分层结构和小世界图理论 ，旨在高效地进行近似最近邻搜索。它通过构建一个 多层次的图结构 ，其中每一层的节点连接关系不同，逐层精细化，从而提高高维数据集的搜索效率。

图的结构

HNSW的图结构结合了两种技术： 跳表 （Skip List）和 可导航小世界 （NSW）图。

跳表 特点：

多层链表 ：跳表的底层是一个完整的 有序链表，存储所有元素 。上层链表是下层链表的“抽象版”，包含部分元素，随着层数增加变得更加稀疏。

逐层查找 ：查询时， 从最上层开始查找，如果当前层无法找到目标元素，则跳到下一层继续查找，直到最底层。

![原文图片](assets/43339a4f7786.png)

可导航小世界（NSW） 特点：

邻接列表 ：每个节点连接若干相似节点，称为邻接节点。 每个节点都保存一个邻接列表。

遍历过程 ：从随机选定的入口节点开始，通过图的边 逐步找到最接近查询向量的节点 。

HNSW的工作原理

HNSW将跳表的层次化结构与NSW的小世界理论结合起来，形成了一个高效的近似最近邻搜索算法。其工作分为两个主要阶段：索引构建和查询过程。

索引构建

图的层次结构 ：HNSW构建一个 多层图 ，每一层代表不同的搜索精度和速度。最上层图的节点较少，提供粗粒度的搜索；而底层节点则提供更精细的搜索，逐层提升搜索精度。

连接邻居 ：每个新加入的节点会选择 若干个近邻节点进行连接 ，从而形成一个局部的小世界结构。通过选择性地建立邻接关系，确保了图的稀疏性和高效搜索。

查询过程

逐层搜索 ：查询从最上层图开始，逐层向下进行。每一层会根据相似度从当前节点跳到相邻节点，逐步逼近目标位置。此时，查询会通过图中的边，利用 跳表 的方式，逐步接近查询向量。

局部优化 ：在最底层，HNSW通过 局部搜索策略 ，遍历当前节点的邻接节点，找到最接近查询向量的结果。

![原文图片](assets/5199eeb12e57.png)

### 3.3.7 DiskANN

DiskANN是一种 基于磁盘的高性能向量近邻搜索算法 ，旨在解决大规模向量数据检索中的内存消耗问题。通过将轻量级的索引结构置于内存中，而将海量的原始数据和构建好的图结构存放在磁盘上，DiskANN能够在保持高召回率和低时延的同时，大幅减少对内存资源的依赖。

DiskANN的优势：

与基于内存的算法相比 ：如HNSW和IVF，DiskANN在资源消耗和可扩展性上有明显优势，能够在更低的资源消耗下提供相似的查询性能。

与基于聚类压缩的算法相比 ：如IVF_PQ，DiskANN在召回率和性能上保持高效，同时避免了因压缩而导致的召回率降低

### 3.3.8 总结与建议

向量索引技术在大规模、高维度的非结构化数据检索中扮演了至关重要的角色。通过多种创新算法，不同场景中的检索效率得到了显著提升。这些索引技术有效解决了传统方法在处理海量数据时的局限，支持了高效的近似最近邻（ANN）搜索，尤其在LLM、推荐系统、多模态搜索等领域表现出巨大的应用潜力。

选择合适的向量检索方式依赖于具体的应用需求和数据特性，需要在性能和效率之间取得平衡，下图是一些建议：

![原文图片](assets/580eaf766f66.png)

## 3.4 ReRank

Rerank作为RAG模型中在retrieve和generation之间的一个重要环节，主要负责在大范围检索完成后对候选文档进行再 精排 序，从而提升最终大模型生成结果的质量和关联性。

![原文图片](assets/30833fd55e85.png)

rerank的作用：

提升检索结果相关性： RAG粗排返回的文档质量和相关性可能较差，rerank采用更精细的语义匹配模型，过滤掉与用户问题相关性较低的文档，以及噪声和不相关的信息。

复杂语义理解： rerank能帮助大模型更好地理解和利用检索到的信息，强化相关文档的影响，从而提升生成结果的相关性和准确性。

降低生成模型负担： RAG检索到的文档数量较多，通过Rerank能较少输入文档数量，缩短上下文长度。

## 3.4.1综述

首先从一遍综述《Large Language Models for Information Retrieval: A Survey》，来了解学术界ReRank的做法：

现有的涉及LLM的重排方法大致可以分为三类： 监督式重排 ， 无监督式重排 ，以及 利用LLM做训练数据的增强 。

监督式重排

由于在LLM 预训练阶段缺少rerank意识 ，因此需要在任务相关的排序数据集上进行微调（例如MS MARCO passage ranking dataset ，这种数据集针对每个条目都包含了相关和不相关的信息），使其能够更好地衡量查询与文档之间的相关性，并理解重排任务的要求。

Encoder

使用基于编码器（encoder）的LLMs进行文档重排。将查询和文档拼接为一个序列，例如“[CLS] query [SEP] document [SEP]”，通过 计算“[CLS]”位置的表示向量，输入到线性层中，得到相关性分数 。使用交叉熵损失函数进行优化，以学习用户查询与文档之间的相关性。

代表方法 ：monoBERT。

优点 ：利用现有的预训练模型（如BERT），通过简单的微调即可应用于重排任务，简单高效。

Encoder-Decoder

使用基于编码器-解码器（encoder-decoder）的LLMs进行文档重排。一般作为 生成任务 训练，将查询和文档作为输入，训练模型生成一个特定的标记（如“true”或“false”）来表示文档的相关性。在推理阶段，通过计算生成标记的logits，使用 softmax函数 计算相关性分数。

代表方法 ：monoT5、DuoT5、RankT5。

优点 ：能够通过生成任务的形式来学习查询与文档之间的复杂语义关系。

Decoder

使用基于解码器（decoder-only）的LLMs进行文档重排，通过 解码器的最后一层 表示向量计算相关性分数。也可以利用现有的ranking 算法（Cohere等）来辅助训练重排模型。

代表方法 ：RankLLaMA 、TSARankLLM 、Q-PEFT 、PE-Rank。

优点： 解码器模型在生成任务上表现优异，能够生成高质量的相关性标记。

无监督重排

随着大模型参数量的激增，微调大模型也变得困难。可以通过 prompt工程 来提升rerank效果，不依赖标注数据，而是直接利用LLM的语言能力来评估查询与文档的相关性，通过prompt引导模型生成相关性评分。这种方法可以分为三种： pointwise, listwise, pairwise。

![原文图片](assets/25bc0f8a984d.png)

Pointwise

Pointwise方法通过评估单个文档与查询的相关性来对文档进行重排。这些方法可以进一步细分为两类： 相关性生成（Relevance Generation）和查询生成（Query Generation） 。

relevance generation方法直接要求LLM输出“真”或“假”标签。基于 生成的标签计算相关性分数 ，通常使用softmax函数计算“是”和“否”的概率。query-document的相关性分数为：

![原文图片](assets/ea0ab9a27461.jpeg)

【公式开始】S_Y和S_N 【公式结束】 表示“真”或“假”的log-likelihood分数

query generation 基于document生成一个预测query ，然后基于生成查询的log-likelihood计算相关性分数：

![原文图片](assets/3401b5f011e3.jpeg)

其中|q|表示query的token数，d表示document，P表示预测prompt。

举例： Discrete Prompt Optimization via Constrained Generation for Zero-shot Re-ranker

定义 【公式开始】ρ* 【公式结束】 作为指导LLM生成最接近于用户query的prompt：

![原文图片](assets/6ffdda0edfaa.jpeg)

其中D包含了所有的用户query和其对应的检索到的相关document。为了解决寻找最优prompt 【公式开始】ρ* 【公式结束】 的问题，本文用 基于鉴别器的条件生成方法 解决，该方法遵循 贝叶斯公式 ：

![原文图片](assets/dd193d402b02.jpeg)

其中 【公式开始】M_D 【公式结束】 是zero-shot的重排器作为鉴别器， 【公式开始】M_G 【公式结束】 作为decoder-only的大模型作为生成器， 【公式开始】D_s 【公式结束】 为数据集D的子集。

鉴别器 【公式开始】M_D 【公式结束】 用于 衡量prompt能否指导大模型生成好的query ， 【公式开始】P_{M_D}(D_s| ρ) 【公式结束】 表示query-document对 ( 【公式开始】q_i, d_i 【公式结束】 )之间的相关性期望:

![原文图片](assets/1ffef8b26c24.jpeg)

由于直接计算公式3中词表中所有的token耗时过长，因而生成器 【公式开始】M_G 【公式结束】 只从鉴别器衡量过的prompt进行采样 。生成器采用beam search的方式选取每一轮的token。整体训练如下：

![原文图片](assets/30753cf95d87.jpeg)

Listwise

LLM的输入是用户query和一些检索到的document， 要求LLM对其进行排序 。由于LLM的上下文长度有限，这里也会采用一些Longcentext的方法（例如 滑动窗口、分批次排序 ）。能够同时考虑多个文档的相关性，生成更全局的重排结果，使用GPT-4做LLM的方法取得了比较好的性能。

缺点：

只有在使用很大的模型（例如GPT4）才能取得良好的性能

对document在prompt中的 顺序敏感 ，当document随机时，其效果甚至差于BM25。

滑动窗口大小限制了一次能排序的文档数量，相邻窗口之间的依赖限制了 并行推理

举例： Zero-Shot Listwise Document Reranking with a Large Language Model

作者提出使用如下prompt来让LLM实现document的重排，方括号后生成一系列按相关性重新排序后的passage id。为了解决输入长度的限制，作者采用滑动窗口的方法。

![原文图片](assets/fa9e68eb83b0.png)

Pairwise

pairwise方法利用了大模型天生擅长做对比的特点，输入为用户查询和和文档对，生成一个表示哪个文档更相关的标记。

举例： Large Language Models are Effective Text Rankers with Pairwise Ranking Prompting

本文提出的pairwise ranking prompting (PRP)支持 生成式 和 打分式 的输出，但是生成式可能生成无关内容，所以主要讨论生成式。PRP的输入为入为 【公式开始】u(q, d_1, d_2) 【公式结束】 的三元组形式，并且利用 LLM对输入顺序敏感的特点 ，同一个三元组会变换顺序输入到模型两次， 若两次结果相反，则认为两个document得分一样 。

![原文图片](assets/e5dd814dea3a.png)

基于PRP，本文还提出三种变体：

PRP-Allpair ：对所有的document都进行比较，缺点是时间复杂度 【公式开始】O(N^2) 【公式结束】

PRP-Sorting :使用快排或者堆排等算法，时间复杂度 【公式开始】O(NlogN) 【公式结束】

PRP-Sliding-K :类似于冒泡排序，但是由于rerank只关心top K的文档，这里K比较小，总体复杂度 【公式开始】O(KlogN) 【公式结束】

利用LLM做训练数据的增强

训练数据增强的目标是通过生成额外的训练样本来扩充有限的标注数据集，从而提高模型的泛化能力和性能。ExaRanker使用GPT-3.5生成检索数据库的解释，然后利用query-document对的解释来训练seq2seq排序模型来生成相关性标签。 InPars-Light提出利用prompt要求大模型基于document生成query，ChatGPT-RetrievalQA提出基于用户query合成document。此外还有方法提出将gpt的ranking能力迁移到小模型，利用gpt生成ranking列表来训练较小的模型。

### 3.4.2 Rerank与Embedding

首先分辨一下rerank模型和embedding模型的异同：

embedding模型（例如 bi-encoder ）的目的是将文本转化成向量表示，以便直接用于计算用户问题和文档之间的相似度。使用bi-encoder进行向量搜索时， 在创建document文档时 就完成了所有繁重的transformer计算。当用户发起查询时， 只需要运行一个Transformer计算生成查询向量 ，在计算用户查询和document之间的相似度，效率极高。

embedding模型存在的问题

embedding模型只是将文本信息压缩为固定长度的向量，可能会导致 语义信息丢失 、 理解多义词困难 、 长文本语义平均化 等问题。

因为 在用户提出问题之前就已经为文档创建了嵌入，无法理解用户问题的上下文信息。

embedding模型计算整个查询和文档之间的相似度，难以捕捉 捕捉词级、句级或精确语义关系 。

![原文图片](assets/f541f01c1dc6.png)

rerank（例如 cross-encoder ）是在初步检索的基础上进行进一步的排序，在 用户提出查询时 才运行，这让我们能够针对具体查询分析文档的含义，而非仅生成一个泛化的、平均化的含义。缺点是要对用户查询和相关的多个文档一起运行Transformer推理，消耗更长的时间

![原文图片](assets/45b6219f94dd.png)

为什么Rerank精度更高？

reranker不进行预计算，而是 将用户查询和一个文档一起输入到transformer 中，能更好的捕捉两者之间语义和上下文信息。

embedding模型将用户查询和文档 压缩到低维向量 中，可能丢失细粒度语义。

总结 ：rerank模型的精度要更高，但其开销也更大。所以一般是用embedding模型作初步筛选，再做rerank，也被称为Two-Stage Retrieval。

### 3.4.3 传统Rerank模型

编码器模型（Bert）

参考：PASSAGE RE-RANKING WITH BERT

将 Bert-LARGE 模型作为一个分类模型，即使用 BERT 中的 [CLS] 标记 ，通过单层神经网络输入从而获取概率输出，根据这些概率对文本进行重排序，类似于 Cross-Encoder（将用户查询和单个文档一起交给一个bert模型，直接计算二者的相似度，不产生embedding）。输入格式类似于：

Python
Input: [CLS] query_token_ids [SEP] doc_token_ids [SEP]

这里限制query最长64token，整个输入最长512个token。模型的输出是相关性打分。将预训练好的bert模型进行微调，使用的损失函数为：

![原文图片](assets/6245ca401d5d.png)

实现代码：

Python
# https://github.com/nyu-dl/dl4marco-bert/blob/master/convert_msmarco_to_tfrecord.py
def write_to_tf_record(writer, tokenizer, query, docs, labels,
 ids_file=None, query_id=None, doc_ids=None):
 query = tokenization.convert_to_unicode(query)
 # 转化 query token id，在前面添加了 [CLS] 
 query_token_ids = tokenization.convert_to_bert_input(
 text=query, max_seq_length=FLAGS.max_query_length, tokenizer=tokenizer, 
 add_cls=True)

 query_token_ids_tf = tf.train.Feature(
 int64_list=tf.train.Int64List(value=query_token_ids))

 for i, (doc_text, label) in enumerate(zip(docs, labels)):
 # 转换为 doc token ids， 没有添加 [CLS] 
 doc_token_id = tokenization.convert_to_bert_input(
 text=tokenization.convert_to_unicode(doc_text),
 max_seq_length=FLAGS.max_seq_length - len(query_token_ids),
 tokenizer=tokenizer,
 add_cls=False)

 doc_ids_tf = tf.train.Feature(
 int64_list=tf.train.Int64List(value=doc_token_id))
 
 # 数据集标签 labels_tf = tf.train.Feature(
 int64_list=tf.train.Int64List(value=[label]))
 
 features = tf.train.Features(feature={
 'query_ids': query_token_ids_tf,
 'doc_ids': doc_ids_tf,
 'label': labels_tf,
 })

解码器模型（GPT）

参考：SGPT: GPTSentence Embeddings for Semantic Search

SGPT Cross-Encoder

通过 GPT 实现 Cross-Encoder 交叉编码器。具体的方法是将 query 和 document 拼接起来一起编码，然后基于获取的对数概率 (log probabilities) 来计算分数。

![原文图片](assets/2fdf962c86a1.png)

给定用户查询q，文档集合D，目标是查询最相关的文档d*，基于贝叶斯公式有：

![原文图片](assets/d369b40c8dfa.jpeg)

这里边P(q)是固定值，P(d)变化量比较小。这里限制了模型输出的query长度和原始用户query长度一样，并对过长的document进行了裁剪，由于用户query长度是固定的，比较P(q|d)也更容易。

实现代码：

Python
## https://github.com/Muennighoff/sgpt/blob/main/README.md#asymmetric-semantic-search-ce
prompt = 'Documents are searched to find matches with the same content.\nThe document "{}" is a good search result for "'
for query in queries:
 print(f"Query: {query}")
 for doc in docs:
 context = prompt.format(doc)

 context_enc = tokenizer.encode(context, add_special_tokens=False)
 continuation_enc = tokenizer.encode(query, add_special_tokens=False)
 ## 拼接 query 和 document 
 model_input = torch.tensor(context_enc+continuation_enc[:-1])
 continuation_len = len(continuation_enc)
 input_len, = model_input.shape

 ## 获取对数概率 
 logprobs = torch.nn.functional.log_softmax(model(model_input)[0], dim=-1).cpu()
 logprobs = logprobs[input_len-continuation_len:]
 ## Gather the log probabilities of the continuation tokens -> [continuation_len] 
 logprobs = torch.gather(logprobs, 1, torch.tensor(continuation_enc).unsqueeze(-1)).squeeze(-1)
 score = torch.sum(logprobs)
 ## The higher (closer to 0), the more similar 
 print(f"Document: {doc[:20] + '...'} Score: {score}")

### 3.4.4 ReRank模型盘点

为了衡量检索系统的有效性，主要依赖两个指标:、

命中率 （Hit rate）：计算在前k个检索文档中 找到正确答案的查询比例 。简单来说，它是关于我们的系统在前几次猜测中正确的频率。

平均倒数排名 （MRR）：对于每个查询，MRR通过查看排 名最高的相关文档的排名来评估系统的准确性。 具体来说，它是所有查询中这些秩的倒数的平均值。因此，如果第一个相关文档是顶部结果，则倒数排名为1;如果是第二个，倒数是1/2，以此类推。

现有Embedding和ReRank模型的测评效果：

![原文图片](assets/6eb79ce50add.png)

cohere-reranker-v3.5

这是个闭源模型，也是采用two-stage retrieval，在第二阶段的rerank采用llm计算用户问题和文档之间的相关性得分。

![原文图片](assets/6ef2e0e92aa3.png)

实现代码：

Python
import cohere
co = cohere.Client("{apiKey}")
results = co.rerank(query=query, documents=documents, top_n=3, 
 model="rerank-multilingual-v2.0")

BGE Re-Ranker v2.0

https://huggingface.co/BAAI/bge-reranker-v2-m3

如下图所示，系统会首先借助 向量模型 （BGE-M3-Dense）与 稀疏检索模型 （BGE-M3-Sparse）分别从向量数据库与倒排索引中初步获取 粗粒度的候选文档 （coarse-grained candidates）。紧接着，系统会进一步利用 排序模型 （BGE Re-Ranker）进一步过滤候选集，并最终获得 精细的文档集 （fine-grained candidates）。

![原文图片](assets/f45cfa270c1c.png)

BGE Re-Ranker v2.0 系列排序模型采用了两种不同尺寸的模型基座，基座模型都在多语言数据上训练得到，并且通过引入由CLIP模型生成的vision token，具有文本+图片混合建模能力：

BGE Re-Ranker v2-LLM： 基于 MiniCPM-2B，Gemma-2B 等性能卓越的轻量化大语言模型。

BGE Re-Ranker v2-M3 ：基于性能出色、参数量更小的 BGE-M3-0.5B 速度更快。

BGE Re-Ranker v2.0 采取了 分层自蒸馏 训练策略，用适度的计算开销换取显著的性能收益（下图 （C））。具体而言， 模型最终排序得分（S(0)）被用作教师信号，利用知识蒸馏的方式，模型的各中间层也被学习并赋予了排序能力 。在实际应用中，用户可以基于具体场景的算力条件及时延限制灵活选择排序模型的层数。

![原文图片](assets/7bb98835e35b.png)

BGE Re-Ranker v2.0是由BGE-M3等embedding模型作为 基座训练而来， 由于BGE Re-Rank没有发表对应的论文，因此 接下来介绍BGE最著名的模型 BGE M3的《BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation》论文。

BGE-M3由北京智源研究院（BAAI）开发，基于Bi-Encoder架构，使用预训练的Transformer模型（ XLM-RoBERTa ）对用户查询和文档进行联合编码，直接输出二者的相关性分数。该模型支持多语言、文本+图片检索方式和更长的文本长度。

混合检索

M3-Embedding统一了密集检索、词汇（稀疏）检索和多向量检索。

密集检索 ：用户查询首先经过一个encoder转换成 隐层状态 【公式开始】H_q 【公式结束】 ，其中 【公式开始】H_q[0] 【公式结束】 表示整个句子的向量，也就是 [CLS] 标记 ，使用 [CLS] 标记的归一化向量表示文本，通过内积计算相似度：

![原文图片](assets/5a83e4730417.jpeg)

稀疏检索 ：定义 词级权重 为：

![原文图片](assets/6d9efc2cb808.jpeg)

如果一个单词出现了多次，则只统计最大的权重。相似度计算为共现词权重的乘积和：

![原文图片](assets/dfc115234bca.jpeg)

多向量检索 ：使用整个输出嵌入 【公式开始】H_q 【公式结束】 来表示用户查询和文档，通过跨 token 交互计算相似度，其中N和M分别是用户查询和文档的长度：

![原文图片](assets/256fe00b7543.jpeg)

最终查询时将这三个损失加权求和。

自蒸馏

embedding模型的目的是区分出 正样本和负样本 ，给正样本评分更高，负样本评分更低。对于以上三种检索方法，可以计算出3种 InfoNCE损失 ：

![原文图片](assets/100dfa41a1a3.jpeg)

其中p*和P'分别表示对于用户查询q来说的正负样本（相关文档和不相关文档），s()表示以上三种相似度的一种。

由于三种检索方式可能存在一定的冲突，为了统一三种损失，作者提出了 自蒸馏 的方法。将三种检索分数加权求和作为教师信号：

![原文图片](assets/1668250b72df.jpeg)

对每个检索方法，使用教师信号指导其损失计算：

![原文图片](assets/36c34261ac2f.jpeg)

其中p()表示softmax函数， 【公式开始】s_* 【公式结束】 表示三种检索的相似性之一，然后将三种损失函数加权求和，

![原文图片](assets/1b8eb33f489b.jpeg)

总损失函数为： 【公式开始】\mathcal{L}_{final} = (\mathcal{L}+\mathcal{L'})/2 【公式结束】 。

BGD-M3的训练流程如下图所示:

先在适应 RetroMAE 方法的 XLM-RoBERTa 模型上进行无监督预训练（RetroMAE的介绍详见Embedding篇），其中只有密集检索采用对比学习的形式。

利用自蒸馏微调embedding模型，在这阶段采用了有标签数据和合成数据。

![原文图片](assets/6c86391bdfd7.png)

高效批处理

embedding模型需要保持 batch-size足够大 才能充分学习文本之间的差异（也就是in-batch中包含足够多的负样本），传统的将长文本分块方法不适用于BGE-M3，因为本模型需要同时学习长文本和短文本。

为了从不同粒度的输入中学习，并保持大批量大小，作者提出了以下方法：

在训练数据预处理时就 根据序列长度进行分组 ，每个batch的数据都来自于同一个组，以减少padding并充分利用GPU。

为不同的GPU进行数据采样时，采用 固定的种子 ，保证负载均衡。

处理长序列数据时，将batch进一步 细分成sub-batch ，使用 梯度检查点 （Gradient Checkpointing）以降低显存，逐个sub-batch编码后合并结果。此外该方法能有效 扩大batch-size ，长文本（如 8192 token）批次大小提升 20 倍以上

跨 GPU 广播编码结果 ，扩大负样本规模。

总结 BGE-M3 的特点：

多语言统一表示 ：通过大规模跨语言数据构建，支持 100+ 语言的语义对齐。

多功能检索集成 ：首次在单一模型中实现密集、稀疏、多向量检索的统一。

自知识蒸馏框架 ：通过集成不同检索功能的教师信号，显著提升模型鲁棒性。

高效训练优化 ：创新的批处理策略，显著提升长文本训练效率。

Jina Reranker v2

https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual

jina-Reranker-v2支持多语言，表格搜索，代码检索和函数调用，具有以下特点：

是一种 跨编码器（cross-encoder） 模型，只有278M 参数，轻量高效。

该模型能够处理多达 524,288 个token的序列，同时保持出色的速度。为了使模型能够处理超过 1024 个token的长文本，该模型使用 滑动窗口方法 将输入文本分块为较小的部分，并分别重新排列每个块。

使用 flash attention 进行快速推理，吞吐量比其前代产品高出 6 倍

Jina Reranker v2训练pipeline

英文数据准备： 我们仅使用英语数据训练骨干模型，准备了第一个版本，包括配对数据（对比训练）或三元组（查询、正确响应、错误响应）、查询-函数模式配对和查询-表模式配对。

添加跨语言数据： 在下一阶段，我们添加了跨语言配对和三元组数据集，专门改进骨干模型在检索任务上的多语言能力。

添加 所有 多语言数据： 在这个阶段，我们主要专注于确保模型能看到最大量的数据。我们使用来自 100 多种低资源和高资源语言的所有配对和三元组数据集对第二阶段的模型检查点进行微调。

使用挖掘的困难负样本进行微调： 在观察第三阶段的重排序性能后，我们通过添加更多三元组数据进行微调，特别是为现有查询添加更多困难负样本的例子——那些表面上看起来与查询相关，但实际上是错误的响应。

jina-Reranker-v2是在Jina Embeddings v2的基础上采用Cross Encoder， 但没有发表专门的jina-Reranker-v2技术报告，因此 以下介绍Jina Embeddings v2。

预训练Bert

在修改的Bert模型上预训练，上下文扩展到8192个token。模型细节：

Attention with Linear Biases（ALiBi） ： ALiBi在每个注意力层的注意力分数矩阵中引入一个常数偏置项来编码位置信息 。 与原始的方法不同，使用了 对称encoder模型和双向自注意力 ，其中 【公式开始】m_i 【公式结束】 的计算为：

![原文图片](assets/1da424c808df.jpeg)

![原文图片](assets/fdbbab6b51e7.jpeg)

Gated Linear Units（GLU） ： 对于small模型和base模型，使用GEGLU（GELU激活函数）；对于large模型，使用ReGLU（ReLU激活函数），以提高训练稳定性。

Layer Normalization（LN） ：采用post-norm的LN。

预训练过程要点 ：

采用 MLM 任务训练，随机掩盖输入词元的30%，使用全词掩盖策略，并让模型推断这些被掩盖的词元。被掩盖的词元中，80%被替换为[MASK]，10%被替换为随机词元，剩余10%保持不变。

预训练阶段序列长度限制在512以内，每个批次的全局批量大小为4096，由于序列长度不同，计算损失时每个批次包含的被掩盖词元数量也不同。

采用 AdamW 优化器和 FP16 动态混合精度训练

微调

为了微调文本embedding模型，额外添加了一个 平均池化层 ，平均文本中的token embedding以将将各token的嵌入向量平均合并为单个向量，无需额外可训练参数。该过程分为两个主要阶段： 基于文本对的微调 和 结合困难负样本的微调 。

基于文本对的微调：

数据来源 ：约40种不同的数据源，包括标题-摘要对（提升聚类任务性能）。采用 一致性过滤 （Consistency Filtering）提升文本对质量。批次构建时，随机选择数据源并填充批次，不同数据源的采样率根据质量和数量动态调整。

训练损失 ：采用 InfoNCE 损失，并且同时计算查询到目标（q→p）和目标到查询（p→q）的损失，增强对称性。

结合困难负样本的微调

针对 检索任务 （如MSMarco、Natural Questions），每个批次包含一个正样本和15个 困难负样本 （通过检索模型筛选出的相似但无关的文档）。

针对 非检索任务 （如Natural Language Inference），负样本随机选择。

损失函数还是采用对称的形式，并且引入了更多 难负样本 ：

![原文图片](assets/be8b420f9f60.jpeg)

对于embedding模型的训练来说，InfoNCE损失依赖批次内所有样本的对比，一般 批次越大，对比信息越丰富，模型性能越好 。但大的batch-size会导致显存资源吃紧，Jina Reranker v2采用了以下显存优化技术：

FP16混合精度训练

deepspeed

梯度检查点

Jina Reranker v2的优点

多语言支持 ：覆盖 100+ 种语言，打造真正无界的全球化搜索体验。

结构化数据处理 ：支持表格搜索和函数调用，为 Agentic RAG 强势助力。

顶级性能 ：在包括跨语言问答、英文信息检索、Text-to-SQL 等多个基准测试中表现非常出色。

速度为王 ：性能较前代提升了 6 倍，搜索响应时间减半。

轻量高效 ：仅用 278M 参数即达到顶尖性能，体积是同类模型的一半，大幅降低资源消耗。

mGTE

阿里巴巴通义实验室推出的GTE-Multilingual系列模型，具备高性能、长文档支持、多语言处理及弹性向量表示等特性，显著提升了RAG系统的检索与排序效果。mGTE构建了两阶段RAG的训练流程：

首先利用 RoPE和unpadding 方法训练的编码器，该编码器经过两阶段 MLM 预训练得到

基于编码器训练用于检索的 混合文本表示模型 （TRM）用作第一阶段粗排，和 rerank模型 用作第二阶段精排。

![原文图片](assets/420953c58029.png)

文本编码器

对BERT模型采用了如下的改进：

用 RoPE 代替绝对位置编码

用 GLU 代替FFN

为了加速模型训练，padding后的embedding长度都是64的整数倍。通过 xFormers 框架实现 变长注意力 计算，减少填充（padding）带来的冗余计算，提升训练效率

![原文图片](assets/b51b7abadb95.jpeg)

预训练阶段采用 MLM 任务，掩盖30%的token，采用 AdamW 优化器，学习率线性预热与衰减，混合精度训练（ BF16 ）。为了保障多语言能力，提升数据少的语言的训练效果，从所有语言中根据概率采样某种语言的数据，其中 【公式开始】n_i 【公式结束】 表示语言i的文档数量。

![原文图片](assets/d30659cfb730.jpeg)

采用两阶段学习：

MLM-2048 ：在2048 tokens上下文上预训练，RoPE基值设为10,000。

MLM-8192 ：扩展至8192 tokens，RoPE基值调整为160,000，以适应更长的序列。

文本表示模型

包含两个阶段：

对比学习预训练： 使用encoder输出中提取的[CLS]隐层表示计算余弦相似度，训练损失函数为InfoNCE。batch-size设置为16384，每个batch采用公式（1）中的采样策略。该阶段采用无监督数据集。

对比学习微调 ：采用了 弹性嵌入（Matryoshka嵌入）策略 ， 降低存储与搜索成本；采用 稀疏表示 提升长文本检索效果。损失函数为以上两者的相加。该阶段采用有监督数据集，根据文本长度分组，不同长度采用不同批次大小（如短文本批次大，长文本批次小）。采用激活检查点（activation checkpointing）减少显存占用。

文本重排序模型

采用Cross-Encoder模型， 每个正样本搭配6个困难负样本和4个随机负样本 ，增强模型区分能力。

输入格式：拼接查询与文档为 [CLS] query [SEP] document 。

输出：通过[CLS]标记的隐藏状态预测相关性分数。

总结下ReRank模型的一些技术特点：

使用 Cross-Encoder ，将用户查询和文档拼接起来，交给Transformer编码器，能更好的建模两者之间的语义关系。

一般都采用 多阶段训练 的方式，逐步扩充上下文长度。

损失函数大多采用 InfoNCE 损失，并在对比学习中加入 难负样本 ，增强模型的鲁棒性。

为了加速训练和节省显存，可能采用deepspeed、混合精度训练、激活检查点、动态批次划分等技术。

在性能上，使用了Rerank模型后的精度往往更高

## 3.5 Long context

Long context，也就是长上下文，通过 增加模型直接处理的文本长度来维持更多的上下文信息 ，需要通过模型训练来逐步拉升大模型能够接纳的输入文本长度。一般来说，把接受4K-8K输入token的LLM，算作普通的LLM。能够接受10K~200K甚至数百万的LLM，叫做长上下文大模型。

现实中的如文档摘要、多轮对话等任务，需要llm理解长文本序列，否则模型的perplexity将显著上升。但是长上下文将增加计算成本，且对显存需求更高。

![原文图片](assets/1c230667aca8.png)

上图摘自论文《Beyond the Limits: A Survey of Techniques to Extend the Context Length in Large Language Models 》， 将长上下文方法分为5类：

Length Extrapolation ，长度外推，即"Train Short, Test Long"。如 位置编码外推、上下文窗口分割和prompt压缩 ，也是本章节介绍的重点。

Attention Approximation ，注意力近似。旨在降低注意力依赖计算的复杂度，比如 低秩分解和稀疏注意 力。降低复杂度后，在有限资源的情况下可以输入更多的token。

Attention-free Transformer ，在不依赖于传统注意力机制的情况下提供token之间依赖信息的计算方法，如 基于RNN的状态空间模型SSM ，最近比较火的 Mamba 。

模型压缩 ：压缩模型减小参数量和计算量，进而可以处理更长的上下文。例如 模型量化、剪枝 。

硬件感知的Transformer ：主要从I/O、资源管理和多设备等方面提高计算效率，如 FlashAttention 。

### 3.5.1 位置外推

位置外推通过调整与输入token相关的位置嵌入(position embedding)的技术，从而修改这些token在模型体系结构中的定位和解释方式，从而在推理时能处理超过其训练序列长度的输入序列。

最直接的外推即在训练时预留多几维设置为0，推理时再改为其他值，但是这些维度没有被训练过，会导致推理时性能严重下降。

通过位置编码外推的方法已经在 1.4 位置编码 介绍了，在这里不再赘述。

### 3.5.2 插值

将推理时的位置索引进行 下采样或缩放 ，就是把2k的位置编码对应到1k。通过这种方式， 推理时的位置索引被映射回了模型训练时的范围内 ，从而帮助模型更好地处理这些原本超出其处理能力的输入序列。

线性内插

比如通过除以2，将4位转成3位，导致的结果是 最后一位更加拥挤 ，相邻数字的差距变成了0.5。虽然经过微调后效果不会明显下降，但是当处理范围进一步增大时，相邻数字差异更小，并且相邻差异只集中在个位数，其他位相邻差异仍是1，导致 维度之间分布不一样 ，增大模型学习难度。

![原文图片](assets/d6033c0666c9.png)

进制转换

可以通过 进制转换 ，既不用新增维度，也可以保持相邻间距。比如采用16进制取代10进制。

![原文图片](assets/eac90e26601f.png)

重新思考RoPE

首先给出苏神的定义： 位置m的旋转位置编码(RoPE)，本质上就是数字m的 【公式开始】\beta 【公式结束】 进制编码。

举个例子：给定一个10进制的数字m，求其 【公式开始】\beta 【公式结束】 进制的从右往左数的第n位数字，采用如下公式：

【公式开始】\lfloor(\frac{m}{\beta^{n-1}} ) \rfloor \space mod \space \beta 【公式结束】

又知道RoPE的定义中有以下cos序列（sin也同理）： 【公式开始】[cos \space m\theta_0, cos \space m\theta_1,..., cos \space m\theta_{d/2-1}] 【公式结束】

![原文图片](assets/56388ee160fa.jpeg)

【公式开始】cos(\frac{m}{10000^{2i/d}}) = cos(\frac{m}{10000^{(2/d)*i}}) = cos(\frac{m}{\beta^i}), \beta = 10000^{(2/d)} 【公式结束】

cos序列就可以表示为： 【公式开始】[cos \space \frac{m}{\beta^0}, cos \space \frac{m}{\beta^1},..., cos \space \frac{m}{\beta^{d/2-1}}] 【公式结束】 ，将其翻转过来： 【公式开始】[cos \space \frac{m}{\beta^{d/2-1}},..., cos \space \frac{m}{\beta^1}, cos \space \frac{m}{\beta^0}] 【公式结束】 。

至于 模运算，它的最重要特性是周期性 ，cos刚好也是周期函数。所以，除掉取整函数这个无关紧要的差异外，RoPE其实就是数字m的 【公式开始】\beta 【公式结束】 进制编码！

基于以上结论，后续介绍的 内插就是将m换成m/k，k是推理时需要扩大的倍数；NTK插值则是将10000换成10000k。

位置插值

参考文章：Extending context window of large language models via positional interpolation

PI通过 直接将位置索引缩小 ，这对于RoPE等位置编码更合适，并且可能需要较少的训练，因为 没有添加可训练参数 ，使得最大位置索引与预训练阶段的上下文窗口限制相匹配。其本质就是 在相邻的整数位置上插值位置索引 ，因为位置索引可以应用在非整数的位置上(而非在训练位置外进行外推)。

区别于线性内插，PI仍保留了4096个位置索引，只不过索引之间距离变成0.5，而前者只有2048个索引，多出来的索引被压缩到了最后一位。

![原文图片](assets/664321657e67.png)

使用PI后，位置m缩放成了 【公式开始】\frac{mL}{L'} 【公式结束】 ，L是训练的上下文长度(2048)，L'是推理时需要扩展到的长度(4096)，对应的q和k计算时变成了 【公式开始】f(x, \frac{mL}{L'}) 【公式结束】 。使用PI后的微调只需要少量用例且对用例不敏感，原因在于 模型在微调阶段仅适应新的上下文窗口 ，从良好的初始化开始，而不是获取新的知识。 只需要进行1000步对微调就能显著降低ppl。

![原文图片](assets/b09b4eb011c0.png)

位置插值法存在的问题

与RoPE一起使用时，RoPE中的每个维度 【公式开始】sin \space m\theta_j, \theta_j = 10000^{-\frac{2j}{d}}, j \in [0,1,...,d/2-1] 【公式结束】 ，其周期为 【公式开始】\frac{2\pi}{m}10000^{\frac{2j}{d}} 【公式结束】 ， 对于维度较低的j，其对应的周期比较小，频率较高。对于这种维度，插值后会变得很拥挤 （本来一个周期包含10个值，但是内插之后能包含20个值）。

NTK-aware插值

核心思想是：高频外推，低频内插。

对于 【公式开始】[cos \space \frac{m}{\beta^0}, cos \space \frac{m}{\beta^1},..., cos \space \frac{m}{\beta^{d/2-1}}]，\beta = 10000^{(2/d)} 【公式结束】 ，将最后面的 低频项 引入 【公式开始】\lambda 【公式结束】 变成 【公式开始】\frac{m}{(\beta \lambda)^{d/2-1}} 【公式结束】 ，为了与内插法一致（内插就是将n换成n/k，其中k是要扩大的倍数），有 【公式开始】\frac{m}{(βλ)^{d/2−1}}=\frac{m/k}{β^{d/2−1}} 【公式结束】 ，解得 【公式开始】\lambda = k^{2/(d-2)} 【公式结束】 。（即上文提到的“NTK插值则是将10000换成10000k”）

而对于最 高频项 【公式开始】cos \space \frac{m}{\beta} 【公式结束】 ，引入 【公式开始】\lambda 【公式结束】 变成 【公式开始】\frac{m}{\beta \lambda} 【公式结束】 ，但由于d一般很大，λ很接近于1，所以还是接近于 【公式开始】\frac{m}{\beta} 【公式结束】 ，基本等价于外推。

NTK插值存在的问题

由于它不仅仅是一种插值方案，一些维度被轻微 外推 到“超出边界”的值，因此使用“NTK-aware”插值进行微调的结果不如PI。

此外，由于存在“越界”值， 理论尺度因子 k 并不能准确描述真实的上下文扩展尺度 。在实践中，对于给定的上下文长度扩展，尺度值 k 必须设置得高于预期尺度

NTK-by-parts插值

波长 ：维度d上嵌入的RoPE，执行完整 旋转 ( 【公式开始】2\pi 【公式结束】 )所需的token长度：

【公式开始】\lambda_d = \frac{2\pi}{\theta_d} = 2\pi b^{\frac{2d}{D}}, \theta_d = 10000^{-\frac{2d}{D}} 【公式结束】

“盲”插值方法 不关心不同维度对应的不同波长，比如像PI和“NTK-aware”插值，对所有RoPE维度的没有做针对性的处理(因为它们对网络有相同的影响)，而其他方法(如 YaRN )，定义为 “有针对性的”插值方法 。

对RoPE有以下观察：

给定上下文大小L， 有一些维数d的波长长于预训练期间看到的最大上下文长度( 【公式开始】\lambda > L 【公式结束】 )，这表明 一些维数的嵌入可能在旋转域中不均匀分布 。 当波长很长时 ，这些维度上的嵌入几乎不变，可以认为 它们保持了绝对位置信息，即每个位置的嵌入不因相对位置变化而变化 ；当 波长较短时 ，嵌入会在较短的距离内完成多次旋转，这使得这些维度上的嵌入反映的是相对位置信息，即 它们可以捕捉到标记之间的相对距离变化 。

采用RoPE进行拉伸时，所有的token变得更彼此接近，因为 【公式开始】a \cdot b = ||a|| \space ||b|| cos(\theta) 【公式结束】 ， 【公式开始】\theta 【公式结束】 减小会导致两个向量的内积变大，变得更加接近 。从而损害模型处理邻近token位置时的性能。

为了解决以上问题，对高频率的维度不插值，对更低频率的维度插值。

如果波长 λ 比上下文长度 L 小得多，此时不插值

如果波长 λ 等于或大于上下文长度 L ，此时只做插值，不做任何外推

两者之间的维数可以兼备

定义比率 【公式开始】r_d = \frac{L}{\lambda_d} 【公式结束】 ，且维数为d时，比率 r 以如下方式依赖于 d：

![原文图片](assets/2f70f3f19e7c.jpeg)

| 对比维度 | 位置插值（PI） | NTK-aware 插值 | NTK-by-parts 插值 |
| --- | --- | --- | --- |
| 基本原理 | 线性缩放位置编码的索引，将超出训练长度的位置压缩到模型支持的范围内。 | 基于神经正切核（NTK）理论，非线性调整位置编码的基频，平衡高频和低频分辨率。 | 将位置编码的频率范围划分为不同部分，对不同频段分别进行插值（如高频保留、低频缩放）。 |
| 是否需要微调 | 通常需要少量微调（如 1000 步）以稳定模型性能。 | 一般无需微调，可直接推理使用。 | 部分实现需要少量微调（如 YaRN 变体），但少于 PI。 |
| 处理长上下文能力 | 中等：缩放因子较小时效果较好，但扩展倍数较大时性能下降明显。 | 较高：通过非线性调整支持更大扩展倍数（如 8 倍以上），性能衰减较慢。 | 最高：通过分频段优化，在极大扩展倍数（如 16 倍）下仍能保持较好性能。 |
| 高频信息保留 | 较差：线性缩放导致高频位置分辨率下降，影响模型细节理解能力。 | 较好：通过调整基频参数，保留更多高频信息。 | 最好：单独处理高频部分，避免高频信号丢失。 |
| 实现复杂度 | 简单：仅需线性缩放位置索引。 | 中等：需计算非线性基频参数，但公式固定。 | 复杂：需划分频段并分别处理，可能引入额外超参数。 |
| 主要优点 | 实现简单，资源消耗低，适合快速扩展小倍数上下文。 | 无需微调，支持更大扩展倍数，高频信息保留优于 PI。 | 在极端扩展倍数下性能最优，尤其适合超长文本（如 100k tokens 以上）。 |
| 主要缺点 | 扩展倍数受限，高频信息丢失严重，需额外微调。 | 理论复杂，需手动调整基频参数（如 alpha），可能影响低频分辨率。 | 实现复杂，分频策略依赖经验设置，调试成本高。 |

动态插值

固定缩放因子s可能会导致，模型在长度小于 L 时可能出现性能折扣，当序列长度大于 L′ 时可能出现突然退化。因此提出动态缩放， 在每次前向传递中，位置嵌入更新缩放因子 s=max(1,l′/L)，其中 l′ 是当前序列的序列长度。

yarn插值

在对logits进行softmax操作之前引入 温度 可以统一地影响困惑度，无论数据样本和扩展上下文窗口上的token位置如何。具体来说，将注意力计算修改为： 【公式开始】softmax(\frac{q_m^T k_n}{t\sqrt D}) 【公式结束】 。这样在计算RoPE时，可以 根据上下文长度动态调整温度：

短上下文 ： t 较小，插值强度低，保持原始位置编码特性。

长上下文 ： t 增大，增强低频段的插值强度，避免位置编码碰撞。

在训练和推理时没有引入额外的开销，结合NTK-by-parts插值就得到了Yarn插值。

LongRoPE

非均匀位置插值： LongRoPE中发现，有效的位置编码插值应考虑两种非均匀性：不同的RoPE维度（ 【公式开始】\theta_i中的i 【公式结束】 ）和不同的token位置（ 【公式开始】cos(m\theta_i)中的m 【公式结束】 ）。低维和初始token位置存储着关键信息，因此需要进行更少程度的插值。相比之下， 高维存储的信息相对较为稀疏，可进行较大程度的插值 。通过搜索RoPE每个维度以及不同token位置的旋转角度缩放因子，有效地保留了原始 RoPE 位置编码中的信息。这种方法最大程度地减小了位置插值引起的信息损失，从而为微调提供了更好的初始化。

上下文渐进式扩展： LongRoPE首先在 预训练的LLM上进行256k长度的微调 ，然后对微调后的模型进行第二次位置插值，以实现 2048k的上下文窗口 。

短上下文窗口性能恢复： 在扩展到2048k上下文窗口后，LongRoPE通过调整RoPE位置插值因子来恢复短上下文窗口的性能 。LongRoPE在扩展后的大模型上对8K长度内的RoPE缩放因子进行了重新搜索 ，以鼓励在较短上下文长度上进行较少的位置插值。在推理过程中，大模型可根据输入长度动态调整相应的 RoPE 缩放因子。

![原文图片](assets/d5e33746be3c.jpeg)

### 3.5.3 上下文窗口分割

通过 将上下文分割成段，并采用滑动窗口方法来处理上下文。

子序列恢复算法(Parallel context windows for large language models)

LLM的输入分为 上下文token （上下文文档或者检索到的文档）和 任务token （要分类的句子或者问题本身）。

PCW使用的是 Decoder框架 ，输入和输出都在Decoder侧。

位置编码：LLM的上下文窗口长度为N，任务token长度为T，上下文的窗口长度为C=N-T。对于要处理的长上下文，将其分割为B段，每一段长度为C，总的长度为BC+T。PCW位置编码为：

![原文图片](assets/f0995e226b0a.png)

在 解码时丢弃了上下文多段文本之间的位置关系 ，解码时只知道上下文多段文本都是在解码器之前，但无法区分文本之间的位置。不过因为上下文每段文本复用了相同的位置编码，因此位置编码的长度大幅降低，也就降低了对位置编码外推性的需求。

注意力矩阵：基于PCW编码，在执行注意力计算时， 每个窗口内部进行自回归 ， 然后将结果进行拼接，各个窗口复用同一个位置编码 。 任务token和所有上下文中的token都计算注意力。

PCW需要的 计算复杂度正比于并行上下文数量B ，但注意力矩阵很稀疏，多窗口并行的效率很高。

![原文图片](assets/7dc5d2953afd.png)

PCW的缺点：

但是在 长文本QA 问题上表现比较一般，当上下文存在多段文本且无明显关系时，正确答案中会混杂很多无关的文本变短。

PCW是在输入层就开始对超长上文进行Attention，因为不同上文的位置编码相同，一定程度上会让解码注意力变得非常分散，导致 注意力的熵值变高，解码的不确定性变大 ，更容易出现乱码。

NBCE

假设T是要生成的token序列，S1,S2,⋯,Sn是 相对独立的Context集合 （比如n个不同的段落，至少不是一个句子被分割为两个片段那种），假设它们的总长度已经超过了训练长度，而单个Sk加T还在训练长度内。我们需要根据S1,S2,⋯,Sn生成T，即估计p(T|S1,S2,⋯,Sn)。

基于独立假设的贝叶斯公式，即 朴素贝叶斯 ：

![原文图片](assets/349faa66dbe8.png)

这里 【公式开始】P(S_1,S_2,...,S_n) 【公式结束】 是1所以被省略，由独立假设可以进一步得到：

![原文图片](assets/4f933ad55d39.png)

![原文图片](assets/d018bfd52ec6.png)

另外根据贝叶斯公式：

![原文图片](assets/366cd5341702.png)

![原文图片](assets/bfa547201be5.png)

![原文图片](assets/470349235899.png)

这里的p(T|Sk)和p(T)都可以直接用现有的LLM进行计算,且不涉及长文本。

记 【公式开始】\beta = n - 1 【公式结束】 , 且

![原文图片](assets/4571bc2dd8c6.png)

就可以得到：

![原文图片](assets/f2432f6a1067.png)

在阅读理解场景中Max Pooling配合β=0.25，用Greedy Search总体表现比较好，然而Random Sample出来的结果基本不可读。Random Sample是“按照分布采样”，它的效果差说明Max Pooling的结果不是一个合理的分布；而 Greedy Search只关心最大概率者，而不关心分布的合理性 ，它的效果好告诉我们 概率最大的token正确性较高。

【公式开始】\bar{log p(T|S)} 【公式结束】 本质是在做 Average Pooling ，也可以换成其他的Pooling方法：

![原文图片](assets/d92526f283e3.png)

概率越大说明结果的不确定性越低， 将Pooling方式改为直接输出不确定性最低的那个分布 ，就得到了NBCE。

![原文图片](assets/89daff720ae4.png)

NBCE中不同Context的预测结果通过方法P聚合（或者说投票）在一起（权重为β+1），并减去无Context的预测结果（权重为β）。之所以要减去无Context预测结果，是为了 让模型更加倾向于结合Context而不是纯粹根据自身知识储备来回答。

![原文图片](assets/93fca607aa58.png)

NBCE 存在的问题：

与PCW类似，当上下文增加时，输出的结果不准确，具体表现为主题相关，但是作为问题的答案来说是错误的。并且由于 无法识别Context输入顺序 ，在故事续写等场景表现欠佳。

PCW大致上就是Average Pooling版的NBCE，实测也发现它跟Average Pooling版的NBCE有着相似的缺点。

streaming-LLM

![原文图片](assets/9132b49268da.png)

a) 密集注意力 ：时间复杂度为O( 【公式开始】T^2 【公式结束】 ),当推理文本超过预训练长度时，困惑度大幅度上升

b) 窗口注意力 ：只 维护最近的L个token的KV ，但是当序列长度超过缓存大小时， 失去第一个token的KV，会导致困惑度增加。

c) 滑动窗口与重新计算 ：为每个新的token重建最近token的KV状态（这样一直保持有初始token）。虽然它在长文本上表现良好，但它的 【公式开始】O(T L^2) 【公式结束】 复杂性(源于 上下文重新计算中的二次注意力 )使得它相当慢。

d） streaming-LLM ：保留 attention sink (注意力汇聚，汇聚在初始的几个tokens) 与最近的token结合，用于稳定的注意力计算。

作者观察到 大量的注意力得分被分配给初始的token ，即使它们与任务的相关性不高（即 模型重视初始tokens的绝对位置，而不是它们的语义价值 ）。主要原因是因为 Softmax操作 ，要求所有上下文token的注意力分数总和为1。因此，即使当前任务和许多先前的token不匹配，模型仍然需要在某个地方分配这些不需要的注意力分数，使得分数总和为1。 由于初始token对几乎所有后续token都是可见的，所以这些额外的注意力都汇聚在初始的token上。

StreamingLLM将注意力汇聚的 前4个初始token和滑动窗口 的KV结合在一起，可以有效地推广到无限长的序列长度。

![原文图片](assets/0a8ef99f1723.png)

StreamingLLM在确定 相对距离和添加位置信息 时， 关注缓存中的位置而非原文 ，以保障模型的效率。 例如，如果当前高速缓存具有token[0，1，2，3，6，7，8]并且正在解码第9个token的过程中，则分配的位置是[0,1,2,3,4,5,6,7]。而不是原始文本中的位置，即不是[0,1,2,3,6,7,8,9]。

为了避免模型 过度关注初始的token：

引入一个 全局可训练的注意力汇聚token 。

修改softmax函数：不再使用真实的权重概率向量, 允许所有位置的attention值都很低 。

![原文图片](assets/3cecbe3b34fb.png)

| 维度 | PCW | NBCE | Streaming-LLM |
| --- | --- | --- | --- |
| 核心思想 | 将超长文本分割成多个固定大小的窗口，每个窗口独立编码，然后在解码时对所有窗口的输出进行融合 | 基于朴素贝叶斯假设，对超长文本进行分段，对每段上文进行独立编码，在输出层对每个Step预测token的概率矩阵进行融合 | 利用注意力汇聚点，仅保留少量初始token的KV作为注意力汇聚点，结合滑动窗口的KV进行注意力计算 |
| 上下文长度 | 短（如512 tokens） | 长（如数万tokens） | 中等（依赖缓存策略） |
| 计算效率 | 高 | 中等（稀疏注意力优化） | 高（实时性优先） |
| 缺点 | 无法区分不同窗口之间的位置关系， 解码时注意力可能分散，影响解码合理性 | 无法区分不同窗口之间的位置关系， 当Context数据增加时，输出结果可能不够准确 | 历史信息可能被丢弃，影响长期依赖建模 |
| 适用场景 | 短文本任务 | 长文档处理、代码生成 | 实时对话、流式输入 |

### 3.5.4 提示压缩

对于LLM，越详细的prompt，往往效果越好。但是当prompt(在下图的Rag场景中，上下文一般指prompt)长度过长时，一方面耗时更长；另一方面由于检索到的很多内容可能与答案无关，LLM需要结合context对rerank重新排名后的context进行理解并生成答案，当context长度过长时效果较差。

如下图所示，右下角的prompt提示压缩能有效解决这些问题，只保留prompt中有价值的token。

![原文图片](assets/280aff554883.png)

prompt压缩主要可以分为以下几类：

基于信息熵（information entropy）/ 困惑度（perplexity）：使用小模型计算原始prompt中每个token的困惑度，删除困惑度较低的标记。例如Selective Context、LLMLingua 和 LongLLMLingua。

基于 soft prompt tuning ：引入一组可学习的连续向量（通常称为"soft prompts"），在下游领域对LLM进行微调，但不能应用于黑盒LLM。如AutoCompressor。

基于数据蒸馏：先进行数据蒸馏，再训练模型生成可解释性强的摘要，适用于黑盒LLM。如LLMLingua-2 和 RECOMP

Selective Context

作者观察到即使缺失了部分包含非关键信息的上下文，大模型依然能对用户查询进行准确作答。Selective Context 建立在这种思想之上。

Selective Context 策略采用小型语言模型（SLM），来 计算给定上下文中各个词汇单元（比如句子、短语或词语）的 自信息值（（self-information）进一步） 。然后，基于这些自信息值评估各单元的信息含量。通过仅保留自信息值较高的内容，Selective Context 为大语言模型（LLM）提供了更为简洁、高效的 context representation 。

自信息量 ： 量化事件传达的信息量 ，设随机变量X的概率密度函数为p(X)，对于 【公式开始】X=x 【公式结束】 这件事的信息量为：

【公式开始】I(x)=−log_2p(x) 【公式结束】

越罕见的事件，由于包含了更多新颖的信息，传达的信息越多。

训练流程：

使用小型语言模型（SLM） 计算出上下文中每一个 token 的自信息值 。

接着 将token合并成句子/短语 ，合并后句子/短语的自信息量为每个token的和。

之后将句子/短语按照信息量降序分布，只保留包含前p%信息量的句子/短语，从而达到优化的目的。

Selective Context存在的问题 ：

只根据自信息量选择关键信息，可能无法完全捕捉关键信息，并且 忽略了压缩后上下文内容之间的连接性 ，可能对模型预测造成影响。

没有考虑 大模型与压缩prompt的小模型 的相关性。

计算自信息量会导致一定的 计算开销 。

LLMLingua

![原文图片](assets/7148b1a02c59.png)

问题定义 ： 【公式开始】\hat{x} 【公式结束】 和x分别表示压缩后和压缩前的prompt， 【公式开始】\hat{x_G} 【公式结束】 和 【公式开始】x_G 【公式结束】 分别表示压缩后和压缩前的LLM的输出。 训练目标是最小化压缩前输出和压缩后输出分布之间的差距 ：

![原文图片](assets/b7a4268ef1b5.png)

LLMLingua 采用 预算控制器 为原始提示的各个组成部分（例如指令instruction、演示demonstration（其实就是样例）和问题query）动态分配不同的压缩比。LLMLingua执行粗粒度、演示级压缩，即使在高压缩比下也能保持语义完整性。此外，LLMLingua 引入了用于 细粒度提示压缩的令牌级迭代算法 。

B udget Controller预算控制器

为原始prompt的不同部分动态分配不同的压缩率。

用户查询和系统指令 要保持较高的信息密度，用 较低的压缩比率 ，确保核心信息的完整留存

演示样例 部分可实施 更高比率的压缩 ，剔除不必要的冗余信息。

之所以要采用粗粒度、演示级压缩用于demonstration的压缩，是因为一方面 过多冗余的demonstration会占据instruction和query的位置 ，后者对生成答案的影响更大。另一方面 token级别的压缩可能导致prompt过于琐碎 。

训练流程 如下：

计算演示样例的 压缩比例

利用小型语言模型（如 GPT-2 或 LLaMA）计算原始演示样例集合中每个演示样例的 困惑度 （perplexity），按perplexity进行排序。

迭代选取演示样例加入集合D。

压缩演示样例后， 剩余的budget 加到系统指令和用户查询中。

![原文图片](assets/623f1eb77208.png)

ITPC迭代令牌级提示压缩

存在问题 : 上一阶段按照困惑度（perplexity）进行压缩，依赖于token之间的 独立性假设 （也就是n-gram，假设token之间是彼此独立的，其出现概率只跟其前面的n-1个token有关，而跟其他token无关）。这一假设忽略了token之间复杂的关系，这种关系对于理解上下文和保持语义的完整性至关重要。

目的 ：对prompt进行进一步的细颗粒度的压缩，得到 最终的输出prompt。

ITPC算法 ：在压缩期间更精确地评估每个标记的重要性，通过迭代处理提示中的每个片段并考虑当前上下文中每个标记的条件概率来实现这一点。这种方法有助于更好地保留令牌之间的依赖关系。

将Budget Controller输出的 【公式开始】x' = (x^{ins}, x^D, x^{que}) 【公式结束】 分成几段 【公式开始】S = {s_1, ...,s_m} 【公式结束】 ，用小模型 【公式开始】M_s 【公式结束】 计算每一段的困惑度。 假设组内的分布具有独立性， 采取阈值或比例的方式进行压缩；每次压缩完前一组后，再计算后一组的困惑度进行压缩，即 组间的分布不具有独立性 。

![原文图片](assets/242ee1c3ac58.png)

可以根据每一段的 压缩率和困惑度 分布计算阈值 【公式开始】\gamma_j 【公式结束】 ，每一段的压缩率可以总结为：

![原文图片](assets/60022fc9c426.png)

每一段中每个困惑度大于阈值 【公式开始】\gamma_j 【公式结束】 的token被保留

![原文图片](assets/9c0b0e8a842f.png)

Distribution Alignment

用于 消除压缩用的小模型 【公式开始】M_s 【公式结束】 与用于回答用户问题的大模型之间的分布gap 。利用大模型生成的数据（指令-回答对）来对 【公式开始】M_s 【公式结束】 进行 指令微调 ，微调目标为：

![原文图片](assets/66cbd11d85d2.png)

LongLLMLingua

LLMLingua 在压缩过程中 没有考虑用户查询 ，可能会保留不相关的信息。LongLLMLingua通过将用户问题纳入压缩过程来解决这个问题。再LLMLingua的基础上，做了以下的改进：

![原文图片](assets/3869194b33a5.jpeg)

基于问题的粗粒度压缩

通过找到一个指标 【公式开始】r_k 【公式结束】 来衡量每个document的重要性，并只保留重要性高的document。计算文档级的perplexity 【公式开始】p(x_k^{doc}|x^{que}) 【公式结束】 效果不好，因为 文档中包含了大量的无关信息，每个document的困惑度值都很高 。

因此这篇文章用 【公式开始】p(x_k^{que}|x^{doc}) 【公式结束】 来衡量困惑度，并且在 【公式开始】x^{que} 【公式结束】 添加了一句“ We can get the answer to this question in the given documents ”来 增强用户查询和文档之间的联系 ，并减轻幻觉。

![原文图片](assets/9b2b8f36f6f8.png)

基于问题的细粒度压缩

为了 消除文档自身信息熵 的影响，使用不带查询的上下文困惑度与带查询的上下文困惑度之间的差作为当前token的“重要性”，来对文档进行细粒度压缩。本文使用 对比困惑度 ， 如果问题加入进来以后，某个词困惑度大幅度下降，则说明这个词于问题高度相关 ：

![原文图片](assets/d30a3897b2ea.png)

实验证明 高对比困惑度的token与question更相关 。

文档重新排序

实验结果表明，LLM倾向于使用 提示开头和结尾的内容 ，而忽略中间的内容。因此 将粗粒度压缩后的结果按照 【公式开始】r_k 【公式结束】 进行排序 ，按照分数从前到后降序排列：

![原文图片](assets/b5fa77a440b5.png)

动态压缩比

LLMLingua对所有document使用同样的压缩比。LongLLMLingua 使用粗粒度压缩的重要性分数来指导细粒度压缩期间的预算分配 。

首先使用 LLMLingua 的预算控制器设置保留文档的初始预算。然后，在细粒度压缩阶段， 动态地将压缩预算分配给每个文档 。LongLLMLingua 实施了一种 线性调度方法 ，这种分配 基于文档重要性得分的排名指数 【公式开始】I(r_k) 【公式结束】 ，该得分是在粗粒度压缩阶段确定的。

![原文图片](assets/3fdc4dad4e08.jpeg)

保证关键信息完整

在细粒度压缩过程中，可能会压缩一些关键名词，比如2009被压缩成209，导致生成的答案有问题。本文提出 子序列恢复算法：

遍历大语言模型(LLM)响应内容中的每一个词元（token） 【公式开始】y_l 【公式结束】 ，从中选取在压缩提示词 【公式开始】\hat x 【公式结束】 中出现的最长子序列 【公式开始】\hat y_{key,l} 【公式结束】 ；

在原始提示词 x 内，寻找与 \hat y_{key,l} 匹配的最大公共最短子序列（maximum common shortest subsequence） 【公式开始】x_{i,j} 【公式结束】 ；

将大语言模型(LLMs)响应内容中的相应词元 【公式开始】\hat y_{key,l} 【公式结束】 替换为原始的 【公式开始】x_{i,j} 【公式结束】 。

![原文图片](assets/cc88411101de.png)

AutoCompressor

通过增加词汇量和利用"summary tokens"和"summary vectors"来提炼大量上下文信息，进而精调现有的模型结构。具体来说，通过 递归生成 summary vectors 来处理长文档， 这些 summary vectors 作为 软提示词（soft prompts） 被传递给后续的所有文档片段。

![原文图片](assets/a3d31696fab3.png)

训练流程 ：

词汇扩展 ：在这一步骤中，我们将 “summary tokens” 加入到模型现有的词汇库中。这些 tokens 的作用是 帮助模型将庞大的信息量压缩成更紧凑的向量表征 。

文档分割 ：待处理的文档被切割成若干小段， 每一小段后都会附加有 summary tokens 。这些 tokens 不仅携带了本段的信息， 还包含了前面所有段落的摘要信息 ，实现了摘要信息的连续积累（ summary accumulation ）。

微调训练 ：采用 无监督训练 的方式，根据当前片段前的 tokens 序列以及之前片段的摘要向量（summary vectors），预测下一个单词。

反向传播 ：AutoCompressor 在每个文档片段上运用 backpropagation through time (BPTT)（对于每一个时间步，BPTT 都会计算损失函数关于当前时间步和所有之前时间步参数的梯度，然后将这些梯度反向传播回网络，以更新参数。详见《 https://zhuanlan.zhihu.com/p/129336512 》） 和 gradient checkpointing 。反向传播针对整个文档进行，使得模型能够全面理解并学习到整个上下文之间存在的关联。

LLMLingua-2

基于困惑度的方法存在以下问题 ：

(1) 用来计算困惑度的小型语言模型与 提示词压缩的实际目标 不一致，也就是小模型能力不足。

(2) 这一方法仅依赖于 单向的上下文信息 ，而这或许无法覆盖提示词压缩所需的所有必要信息。

针对第一个问题，LLMLingua-2 引入了 数据蒸馏 流程。该流程从大语言模型中提取知识，在不丢失关键信息的情况下压缩提示词。同时，它还构建了一个 extractive text compression dataset， 从原始文本中挑选出最重要的句子、短语或词汇 ，直接组成一个较短的版本，以保留原文的主要信息和意义。在这样的数据集上进行训练，有助于小型语言模型更精准地对齐提示词压缩的需求。

面对第二个问题，LLMLingua-2 采取了一种创新策略 ------ 将提示词压缩转化为 token分类任务 。这一策略确保了压缩后的提示词能忠实地反映原始提示词的意图。它选用 transformer 的 编码器 作为底层架构，能够充分利用完整的 双向上下文信息（bidirectional context） ，捕捉到进行提示词压缩所需的全部必要细节。

![原文图片](assets/f0a7612b283c.png)

数据蒸馏

目的是 从大语言模型（比如 GPT-4）中抽取知识 ，以便在不丢失基本信息的情况下实现有效压缩提示词。作者精心设计了一个提示词（提示词的设计也就是 提示工程 ），指导模型在不向生成文本中引入新词汇的前提下，剔除原始文本中的冗余词汇，从而实现文本的压缩。

![原文图片](assets/89e731a8cd72.png)

观察到在处理非常长的文本时，GPT-4 倾向于采取高比例的压缩策略，可能是因为其处理长文本的能力有限。这种激进的压缩策略往往伴随着大量信息的流失，可能严重影响接下来的任务执行效果。为了解决这个问题，LLMLingua-2 引入了一种 分块压缩（chunk compression） 技术，即先将长文本拆解为若干个不超过 512 tokens 的小文本块，再分别对每一小文本块进行压缩处理，由 GPT-4 来完成这一过程。

数据标注

由于 GPT-4生成的结果需要与原始文本“对应上”，才能构建token级别分类模型 。因此数据标注的目的就是为原始文本里的每个 token 标上一个二元标签，以此判断压缩后该字符是否应该被保留。LLMLingua-2 采取了 滑动窗口策略（sliding window） ，以此来限定搜索范围。同时，还引入了 模糊匹配技术（fuzzy matching） ，有效处理了 GPT-4 在提示词压缩过程中对原始词汇可能做出的细微改动。

质量控制

质量控制环节采用了两个关键指标来评估通过 GPT-4 蒸馏生成的压缩文本，以及自动标注标签的优劣：

Variation Rate （VR）：衡量压缩后的文本与原始文本相比，有多少比例的词汇发生了改变。

Alignment Gap （AG），衡量自动标注的标签的精准程度。

压缩器训练

本质上就是做 二元分类问题 ，预测每个token保留或者丢弃的概率。模型采用transformer 编码器（例如 bert ）+ 一个分类层， 将每个token输出的logits作为其“保留”的概率，只保留大于阈值的token 。

RECOMP

RECOMP[10]是一个建模在RAG场景中的模型压缩方案。其主要核心是3个部分+2个模型： 抽取型压缩器 擅长 从已检索的文档中精挑细选出有价值的部分 ；而 概括型压缩器 则通过 融合多篇文档的精华，自动生成摘要 。

![原文图片](assets/ac37b19cd3e8.png)

抽取型压缩器 ：采用 双编码器模型 （bi-encoder），将文档和用户查询都转换成固定长度的向量，计算每个文档和查询之间的内积来衡量文档和查询之间的相似度，筛选召回的文档。

概括型压缩器 ：采用 Encoder-Decode r模型，对用户查询和筛选后的文档进行摘要。

总结以上介绍的长上下文方法 ：

| 方法 | 位置外推（Positional Extrapolation） | 插值（Interpolation） | 上下文窗口分割（Chunking） | 提示压缩（Prompt Compression） |
| --- | --- | --- | --- | --- |
| 核心原理 | 通过修改位置编码或注意力机制，使模型支持超出训练长度的序列 | 将原始位置编码缩放到更长的上下文窗口 | 将长文本分割为多个短块，分别处理后合并结果 | 通过摘要、关键词提取或模型压缩原始提示信息 |
| 是否需要微调模型 | 通常无需微调（如ALiBi） | 需要微调以适应缩放后的位置编码 | 无需修改模型 | 需要训练压缩模型（如摘要模型） |
| 是否修改模型结构 | 修改注意力机制或位置编码设计（如RoPE扩展） | 调整位置编码参数（如调整旋转基频） | 无需修改模型结构 | 通常不修改主模型，需额外压缩模块 |
| 处理长文本能力 | 支持连续长文本，但末端位置可能精度下降 | 支持连续长文本，性能较稳定 | 分块处理，跨块依赖关系可能丢失 | 保留关键信息，但细节可能损失 |
| 计算复杂度 | 低（仅修改注意力计算） | 中（需微调模型参数） | 低（分块独立处理） | 中（需额外压缩步骤） |
| 优点 | 1. 无需重新训练 2. 实现简单 | 1. 上下文连贯性较好 2. 性能稳定 | 1. 兼容所有模型 2. 资源消耗低 | 1. 减少计算成本 2. 适配固定窗口模型 |
| 适用场景 | 需快速扩展上下文（如对话历史） | 需要稳定处理2-4倍原始长度的场景（如长文档分析） | 资源受限的实时系统（如边缘设备） | 输入冗余度高且需降本（如法律文本处理） |

## 3.6 GraphRAG

RAG为llm提供了从某些数据源检索到的信息，作为其生成答案的依据。也就是将根据上下文相关信息进行检索，基于检索到的知识指导llm进行生成。

RAG能一定程度上缓解大模型面临的问题：

幻觉 ：通过检索 相关的文档 ，减少生成内容幻觉，提供更多的可解释性。

知识实时更新 ：RAG模型的非参数化记忆可以轻松更新，以反映当下世界的知识变化， 无需对模型重新训练 。

数据隐私 ：RAG通过本地化部署私有知识库，限定模型仅访问相关内部数据，从而有效 防止敏感信息外泄。

但是基于RAG的大模型应用面临的问题：

平面检索 : RAG 将每个文档作为一个独立的信息 。想象一下，阅读单独的书页，却不知道它们之间是如何连接的。这种方法错过了不同信息片段之间更深层次的关系。

语境缺陷 : 如果不理解关系和语境，人工智能可能会提供不连贯的反应。这就像有一个图书管理员，他知道在哪里可以找到书，但是却不知道书中的故事之间的联系。

可伸缩性问题: 随着信息量的增长，寻找正确的文档变得越来越慢 ，也越来越复杂，就像试图在不断扩展的库中找到一本特定的书一样。

全局语义理解 ：RAG在 对大型数据集进行总结和理解 的任务上表现不佳，难以把握全局语义。

GraphRAG 不使用非结构化的文本，而是利用 知识图谱 ，利用图结构捕捉数据中的实体、关系及复杂依赖，从而更高效地检索相关信息并生成准确答案。GraphRAG 的一大特色是利用图机器学习算法针对数据集进行 语义聚合和层次化分析 ，因而可以回答一些相对高层级的抽象或总结性问题, 这一点恰好是常规 RAG 系统的短板(例如：用户提问一个问题，需要全局搜索整个数据集，而不是搜索相似性片段，在这种场景下rag性能比较差)。

GraphRAG 基本步骤为：

将输入语料库切分为一系列文本单元，利用LLM创建对源数据中所有 实体和关系 的引用，然后使用这些引用来创建 LLM 生成的知识图谱。

通过图算法检测 社区结构 （进行创建自下而上的聚类），构建分层结构。使用 LLM 为每个社区生成自然语言 摘要 ，帮助全面理解数据集。

在用户查询时，可以进行 局部搜索 或者 全局搜索 。

![原文图片](assets/d44caff4e3f8.png)

GraphRAG总结

基于图的检索 ：传统的 RAG 方法使用向量相似性进行检索，而 GraphRAG 引入了 知识图谱 来捕捉 实体、关系 及其他重要元数据，从而更有效地进行推理。

层次聚类 ：GraphRAG 使用 Leiden 等技术进行 层次聚类 ，将实体及其关系进行组织，提供更丰富的上下文信息来处理复杂的查询。

多模式查询 ：支持多种查询模式：

全局搜索 ：通过利用 社区摘要 来进行全局性推理。

局部搜索 ：通过 扩展相关实体的邻居和关联 概念来进行具体实体的推理。

DRIFT 搜索 ： 结合局部搜索和社区信息 ，提供更准确和相关的答案。

Prompt 调优 ：GraphRAG通过prompt调优能显著提升性能，通过 描述图拓扑结构、限制检索范围、注入结构化信息 等方式，能实现精准的图语义对齐、检索效率提高和更高质量的回复。

### 3.6.1 建立知识图谱索引

知识图谱是真实实体及其之间关系的结构化表示。回忆数据结构的知识，图是由节点和边构成的：

实体（节点） ：表示关键的概念。

关系（边） ：表示实体之间的关系。

知识图谱的构建流程：

输入文档 ：GraphRAG 将一组文本文档的chunking作为输入，这些输入一般存储在 图形数据库 中。

常见的图数据库 ：

Neo4j ：最流行的属性图数据库，具有“无索引邻接”特性，每个顶点维护着指向其邻接顶点的直接引用，图导航操作代价与图大小无关，仅与图的遍历范围成正比。支持ACID事务，适用于多种应用场景，包括社交网络、推荐系统、生物信息学等。

ArangoDB ：多模型数据库，支持图、文档和键值存储。允许在单个数据库中同时使用多种数据模型，适用于各种不同的应用场景。

TigerGraph ：高性能的分布式图数据库，支持复杂的图查询和分析，以及内置的图算法库。适用于处理大规模的图数据。

实体和语义关系提取 : LLM 用于从输入文档中自动提取实体(人、地点、概念)以及它们之间的关系。这是使用 命名实体识别 和 关系提取 等自然语言技术完成的。

知识图谱生成 : 利用提取的实体和关系构造知识图谱数据结构，通过 知识融合 对数据进行逻辑归属和冗杂/错误过滤。

分层社区检测 : 使用图算法（例如Leiden），找出紧密相关的实体群体形成的 社区 。这些社区代表了跨越多个文档的主题或主题。社区 按等级组织 ，高层次社区包含低层次的子社区。

生成信息摘要 ：利用LLM 为每个社区生成摘要 ，包括社区中的实体、关系。此外再将 社区的分层结构保留在分层摘要 中。

### 3.6.2 检索增强生成

主要有两种检索方式：

局部检索 : 局部搜索旨在理解和回答关于特定实体及其相关概念的详细问题。将用户查询与社区摘要进行匹配，以 查找最相关的社区 ，向该实体的 邻居（即相关实体）扩展搜索。

全局检索 : 全局搜索是为了理解和回答关于整个文档集的综合性问题，如“数据中的前N个主题是什么？”这类需要跨文档聚合信息的查询。利用知识图的分层结构对 整个数据集进行搜索 ，以查找回答查询所需的特定实体、关系和信息。这包括了遍历知识图谱和组合来自多个社区的信息，可以提供全面的响应。

### 3.6.3 局部检索

当用户提出关于特定 实体（如人名、地点、组织等）的问题时，应该采用局部搜索的方法，如下图所示：

![原文图片](assets/9b4bc9ca4e43.png)

用户查询 ：首先，系统接收用户查询，这可能是一个简单的问题或更复杂的查询。

搜索相似实体 ：系统从知识图中识别出与用户输入语义相关的一组 实体。这些 实体 作为进入知识图谱的入口点。这一步骤中使用像 Milvus 这样的向量数据库 进行 文本相似性搜索 。

实体-文本单元映射 ：提取的文本单元被映射到相应的 实体，移除原始的文本信息。

实体-关系提取 ：这一步提取关于 实体 及其相应关系 的特定信息。

实体-协变量（Covariate）映射 ：这一步将 实体 映射到它们的协变量，这可能包括 统计数据或其他相关属性 。

实体-社区 摘要映射 ：社区摘要被整合到搜索结果中，纳入一些 全局信息 。

利用对话历史 ：如果有对话历史，系统使用对话历史来更好地 理解用户的意图和上下文 。

生成响应 ：最后，系统根据前几步生成的经过过滤和排序的数据生成并响应用户查询。

### 3.6.4 全局检索

参考：《 https://arxiv.org/pdf/2404.16130 》

针对用户提出的需要全局搜索整个数据集的全局性问题，提出了一种基于GraphRAG的回复方法，大致分为6个步骤：

源文档 → 文本块

粒度 ：将源文档的 文本分割成块 。

权衡 ：更长的块需要更少的 LLM 调用，但可能因为 较长的上下文窗口而降低召回率。

示例 ：在 HotPotQA 数据集上，600 token的块大小提取的实体引用几乎是 2400 token块大小的两倍。

文本块 → 元素实例

目标 ：从文本块中识别和提取 图节点和边 。使用 LLM 提示识别实体和关系，输出限定元组。

定制化 ：可以通过为LLM提供少量领域特定的 示例 来定制提示, 以适应不同的知识领域(如科学、医学、法律等)。

协变量提取 : 支持二级提取提示,用于提取与提取的节点实例相关的其他协变量,如 实体相关的声明、主题、对象、类型、描述、源文本范围以及开始和结束日期 。

多轮提取 ：在不牺牲块大小的情况下检测到更多实体。

元素实例 → 元素摘要

摘要 ：LLM 抽象并总结文本中的实体、关系和声明。

处理重复 ：LLM可能无法始终以统一的格式提取同一实体的引用,可能会产生 重复的实体元素 。但由于检测到密切相关的实体及其摘要，加上LLM可以理解多种名称变体对应的共同实体, 只要这些变体与一组密切相关的实体有足够的连接性, 整体方法就能够应对这种变体。

元素摘要 → 图社区

图建模 ：创建一个 无向加权图 ，其中节点是实体，边是关系。

社区检测 ：使用 Leiden 算法 将图分割成 层次化社区 ，将具有较强内部连接的节点划分为社区, 实现高效的全局摘要。

图社区 → 社区摘要

摘要创建 ：为每个 社区生成报告式摘要 。

实用性 ：摘要有助于 理解数据集的全局结构和语义 ，辅助回答全局查询。用户可以浏览不同层级的社区摘要, 寻找感兴趣的一般主题, 然后深入到较低层级的摘要以获取更多细节。

社区摘要 → 社区回答 → 全局回答

查询社区摘要 ：首先定位用户查询 需要那一层级的社区摘要进行回复 ，然后在这一层级检索相关的社区摘要。

社区摘要处理 ： 社区摘要被随机打乱并划分为预设大小的块 。这确保相关信息分布在各个块中, 而不是集中(并可能丢失)在单个上下文窗口中。

社区回答映射 ：为每一块社区摘要并行生成社区回答，利用LLM 生成 有用程度分数 。

归纳全局回答 ：按照有用程度得分降序对中间社区答案进行排序, 并迭代地添加到新的上下文窗口中, 直到达到token限制。

![原文图片](assets/9c92bd98ca8c.png)

参考：

《 https://blog.csdn.net/m0_56255097/article/details/144033101 》

《 https://xie.infoq.cn/article/18ca7cd7702fc0f03baa02b01 》

《 https://arxiv.org/pdf/2404.16130 》

《 https://microsoft.github.io/graphrag/ 》

GraphRAG 的主要优点有：

结构化知识表示 : GraphRAG 使用 知识图谱 来表示信息、捕获实体、关系和层次结构，更准确的理解上下文语义

高效处理 : 在知识图谱中将数据预处理可以降低计算成本，并且与传统的 RAG 方法相比，可以 更快地检索 。

多方面查询处理 : GraphRAG 可以通过 综合来自知识图谱多个部分的相关信息 来处理复杂的多方面查询。

可解释性 : 与大模型的黑盒输出相比，GraphRAG 中的结构化知识表示提供了更高的透明度和可解释性。

| 特点 | 局部搜索（Local Search） | 全局搜索（Global Search） |
| --- | --- | --- |
| 目的 | 理解和回答关于特定实体及其相关概念的详细问题 | 理解和回答关于整个文档集的综合性问题。 |
| 优化原理 | 在特定的子图或领域内进行搜索，聚焦于相关节点和边，查找与当前查询最相关的信息 | 在整个图谱或大范围的图谱中进行搜索，利用由大型语言模型（LLM）生成的社区报告，这些报告预先总结了数据集的语义结构 |
| 搜索范围 | 限于局部子图，可能只包含少数几个节点和关系 | 涉及整个知识图谱，搜索范围广泛，信息全面 |
| 效率 | 搜索范围较小，通常速度更快，计算量较低 | 搜索范围大，可能需要更多的时间和计算资源，但信息更为全面 |
| 信息相关性 | 聚焦于与查询最相关的局部信息，减少不相关信息的干扰 | 涉及更多的信息，可能包含一些冗余信息，信息覆盖面广，但可能含有不相关部分 |
| 适用场景 | 需要理解文档中提到的特定实体的问题，例如“牛顿运动定律如何影响其他研究？” | 需要跨文档聚合信息的查询，例如“这篇文章的主要主题是什么？” |

### 3.6.5 graphrag库实现GraphRAG

首先安装graphrag库，并初始化项目

Python
!pip install graphrag
# 项目初始化
!graphrag init --root ./graphrag
# 创建输入数据文件夹，并上传文档，目前支持.txt和.csv格式的文档
!mkdir -p ./graphrag/input

接下来在settings.yaml中配置default_chat_model和default_embedding_model

![原文图片](assets/8cdb14f0c00d.jpeg)

调用API进行索引

Python
from pathlib import Path
from pprint import pprint
import pandas as pd
import graphrag.api as api
from graphrag.config.load_config import load_config
from graphrag.index.typing.pipeline_run_result import PipelineRunResult
PROJECT_DIRECTORY = "./graphrag"

graphrag_config = load_config(Path(PROJECT_DIRECTORY))
# 构建索引，index_result 是一个包含索引流水线各个工作流的列表，每个工作流代表一次索引构建过程。
index_result: list[PipelineRunResult] = await api.build_index(config=graphrag_config)

接下来读取索引数据，包括实体、社区和社区摘要

Python
entities = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/entities.parquet")
communities = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/communities.parquet")
community_reports = pd.read_parquet(
 f"{PROJECT_DIRECTORY}/output/community_reports.parquet"
)

检索，支持global_search、local_search和drift_search。

Python
# response 是 GraphRAG 返回的查询结果，context 包含关于查询过程的详细元数据，包括：
# 查询过程中检索到的数据信息
# 被用于构建上下文的文本片段
# 其他元数据
response, context = await api.global_search(
 config=graphrag_config,
 entities=entities,
 communities=communities,
 community_reports=community_reports,
 community_level=2, #核心实体向外扩展的社区层级范围
 dynamic_community_selection=False,# 禁用动态社群选择。
 response_type="Multiple Paragraphs", # 设置返回的查询结果为多段落格式。
 query="对比LoRA微调和QLoRA微调的优劣势",
)

## 3.7 Agentic RAG

参考：《AGENTIC RETRIEVAL-AUGMENTED GENERATION: A SURVEY ON AGENTIC RAG》

Agentic RAG 将AI Agent融入了 RAG， 采用了Agent中的思想，例如Reflection、planning、工具使用、多智能体协作等 ，在以下方面都表现出卓越的性能：

多领域知识检索。

以文档为中心的实时工作流程。

可扩展、自适应且合乎道德的 AI 系统。

![原文图片](assets/745d95a68421.png)

### 3.7.1 RAG 发展历程

Naive RAG

Naive RAG 是最基础的一种架构，用于结合检索和生成来处理复杂的任务。下图中的示例依赖于基于关键词的检索技术，如 TF-IDF 和 BM25 ，从静态数据集中获取文档，用于增强模型的生成能力。（Naive RAG也支持向量检索）

![原文图片](assets/75fb31919047.png)

Naive RAG容易实现， 适用于简单的事实查询或上下文复杂性低的任务 ，但存在以下缺陷：

缺乏上下文意识 ：由于 依赖词汇匹配而非语义理解 ，检索到的文档往往 无法捕捉查询的语义细微差别

输出碎片化 ：缺乏 数据预处理 或 上下文 整合，往往导致 回答不连贯或过于通用

可扩展性问题 ： 基于关键词的检索技术在处理大型数据集时存在困难 ，往往无法识别最相关的信息

Advanced RAG

Advanced RAG 融入语义理解和增强的检索技术。使用 密集检索模型（如 Dense Passage Retrieval，DPR） 和 神经排序算法 来提高检索精度。

![原文图片](assets/55ad83366204.png)

Advanced RAG 的核心特性包括：

密集向量搜索 ： 查询和文档以高维向量空间表示 ，从而实现用户查询和检索到的文档之间更好的语义对齐

上下文重新排序 ： 神经模型重新对检索到的文档进行排序 ，以优先考虑最相关的上下文信息

迭代检索 ：Advanced RAG 引入了 多跳检索机制 ，使得在复杂查询中可以跨多个文档进行推理

Advanced RAG 适用于 需要高精度和细致理解的应用 ，例如研究综述和个性化推荐。然而，仍然存在一些挑战，比如 计算开销和有限的可扩展性，特别是在处理大型数据集或多步查询时。

Modular RAG

Modular RAG 强调 灵活性 和 定制性 。 将检索和生成流程分解为独立、可重用的组件，从而实现领域特定的优化和任务适应性 。下图展示了 Modular RAG 的架构，展示了混合检索策略、可组合的流程和外部工具集成。

![原文图片](assets/8f05fd129026.png)

Modular RAG 的关键创新包括：

混合检索策略 ： 将稀疏检索方法 （例如 稀疏编码器-BM25） 与密集检索技术 （例如 DPR - Dense Passage Retrieval）相结合 ，准确性更高（就是bge里的混合检索）。

工具集成 ：将外部 API、数据库、计算工具等功能纳入系统， 用于处理特定任务， 如实时数据分析或领域特定计算

可组合的流程 ：Modular RAG 使得检索器、生成器和其他组件可以独立替换、增强或重新配置，从而 实现对特定用例的高度适应性

例如，一个专为金融分析设计的 Modular RAG 系统可以通过 API 获取实时股票价格，利用密集检索分析历史趋势，并通过定制的语言模型生成可操作的投资见解。这种模块化和定制性使得 Modular RAG 非常 适合处理复杂的、多领域的任务，既具有可扩展性又具有精确性 。

Graph RAG

Graph RAG整合基于图的数据结构扩展了传统的检索增强生成系统， 利用图数据中的关系和层次结构，增强了多跳推理和上下文丰富性 。通过引入基于图的检索，Graph RAG能够实现更丰富、更准确的生成输出，特别是在需要 关系理解的任务 中。

![原文图片](assets/306699d0097d.png)

Graph RAG的特点包括：

节点连接性 ： 捕获并推理实体之间的关系 。

层次知识管理 ：通过 基于图的层次结构处理结构化和非结构化数据 。

上下文丰富 ：通过利用基于图的路径 添加关系理解 。

然而，Graph RAG也有一些局限性：

可扩展性有限 ：依赖图结构可能会 限制可扩展性，特别是在数据源广泛时。

数据依赖性 ：高质量的图数据对于有意义的输出至关重要， 限制了其在非结构化或注释不佳的数据集中的适用性 。

集成复杂性 ：将图数据与非结构化检索系统集成 增加了设计和实现的复杂性。

Graph RAG适用于医疗诊断、法律研究等需要对结构化关系进行推理的应用领域。更详细描述见 3.6 GraphRAG。

传统RAG面临的问题

上下文整合 ：通常难以将RAG检索到的内容其无缝地融入生成的响应中，检索是静态的，缺乏上下文意识，导致输出结果零散、不一致或者过于通用。

多步推理 ：复杂的查询需要多步查询和推理，传统的 RAG 系统往往无法根据中间洞察或用户反馈来优化检索，导致响应不完整或不连贯。

可拓展性和高延迟 ：随着数据源的增多，查询将需要更大的计算资源，导致了显著的延迟。

Agentic RAG

Agentic RAG 引入了具有动态决策能力和工作流优化能力的自主代理，实现了范式转变。与静态系统不同，Agentic RAG 采用 迭代改进 和 自适应检索策略 来应对复杂、实时和多领域查询。这种范式 利用了检索和生成过程的模块化，同时引入了基于代理的自治性 。

Agentic RAG 的关键特性包括：

自主决策 ：代理 根据查询的复杂性独立评估和管理检索策略

迭代改进 ：引入 反馈循环 以提高检索准确性和响应相关性

工作流优化 ： 动态编排任务 ，实现实时应用的高效性

Agentic RAG 面临的挑战：

协调复杂性 ：管理代理之间的交互需要复杂的 编排机制

计算开销 ：使用多个代理增加了复杂工作流的 资源需求

可扩展性限制 ：虽然具有可扩展性，但系统的动态性可能会对高查询量的 计算资源 造成压力

Agentic RAG 在客户支持、金融分析和自适应学习平台等领域表现出色，其中动态适应性和上下文精确性至关重要。

| 类型 | 检索方式 | 核心创新 | 适用场景 |
| --- | --- | --- | --- |
| Naive RAG | 关键词匹配 | 初步结合检索与生成 | 简单事实问答 |
| Advanced RAG | 密集向量+神经排序 | 语义对齐与多跳推理 | 研究分析、推荐系统 |
| Modular RAG | 混合检索+模块化 | 灵活定制与工具集成 | 跨领域复杂任务 |
| Graph RAG | 图结构推理 | 关系与层次化知识管理 | 医疗诊断、法律研究 |
| Agentic RAG | 动态Agent协作 | 自主决策与迭代优化 | 实时交互场景（如客服） |

### 3.7.2 Agentic 样式

Agent通常由四部分组成：

LLM ：作为代理的主要 推理引擎和对话接口 ，负责解释用户查询，生成响应，并保持连贯性

记忆（短期和长期） ：在交互过程中捕捉上下文和相关数据。 短期记忆跟踪即时对话状态，而长期记忆存储积累的知识和代理经验

规划（反思和自我批评） ：通过反思、查询路由或自我批评指导代理的迭代推理过程，确保有效地拆分复杂任务

工具（向量搜索、网络搜索、API 等） ：扩展代理的能力，使其不仅限于文本生成，还能够 访问外部资源、实时数据或专门的计算

更多关于Agent的知识见 4 Agent篇

![原文图片](assets/5c3face813a1.png)

Reflection

代理迭代地评估和改进其输出，以识别和解决错误、不一致性和改进空间，提高在代码生成、文本生成和问题回答等任务中的性能。 在实际应用中，反思涉及促使代理对其输出进行正确性、风格和效率的批判，并将这些反馈纳入后续的迭代中。 外部工具如单元测试或网络搜索，可以进一步增强这个过程，验证结果并突出差距。

通过不断地迭代精炼，可以提高多步骤推理任务的准确性。在多代理系统中， 反思可以涉及不同的角色，例如一个代理生成输出，而另一个代理对其进行批判，促进协作改进（类似强化学习的Actor-Critic算法） 。例如，在法律研究中，代理可以通过重新评估检索到的案例法来迭代地改进回答，确保准确性和全面性。

Planning

规划使代理能够自主地 将复杂任务分解为更小、可管理的子任务，创建结构化的工作流程和任务序列，高效地解决问题。 目标在于通过分解任务促进多步骤推理，通过优化任务优先级减少计算开销。例如，一个财务分析系统规划数据检索任务，以评估风险并提供建议。 与反思等确定性工作流程相比，规划可能产生较不可预测的结果。

Tool Use

代理与外部工具、API和知识库互动来扩展其能力。 目标在于将系统功能扩展到预训练知识之外，通过集成外部资源实现特定领域的应用。通过将工具动态集成到工作流程中，代理可以适应复杂任务并提供更准确和与上下文相关的输出。例如，法务助理代理人从合同数据库中检索条款，并应用特定领域的规则进行合规性分析。

![原文图片](assets/27efe317be5e.jpeg)

Multi-Agent

多个代理协同工作以解决复杂任务 ，代理之间进行通信和共享中间结果，确保整体工作流程高效和连贯。 通过将子任务分配给专门的代理，这种模式提高了复杂工作流程的可扩展性和适应性。 每个代理都有自己的记忆和工作流程，可以包括使用工具、反思或规划，实现动态和协作的问题解决。例如，在软件开发中，不同代理分别负责前端、后端、测试、算法。

![原文图片](assets/26a5297beba0.jpeg)

提升Agentic性能的方法

Prompt Chaining ： 将复杂任务分解为多个步骤，每个步骤都建立在前一个步骤的基础上 。这种结构化方法通过在继续前进之前简化每个子任务来提高准确性。然而，由于顺序处理，它可能会增加延迟。该方法适用于逐步推理，每个子任务都对最终输出有贡献的场景，例如数学推理。

Routing ： 对输入进行分类，并将其引导到适当的专门提示或处理过程。 这种方法确保不同的查询或任务被单独处理，提高了效率和响应质量。适合不同类型的输入需要不同处理策略的场景，确保每个类别的最佳性能，例如智能客服。

Parallelization ： 并行化将一个任务分解为同时运行的独立的进程，从而减少延迟并提高吞吐量 。它可以分为分段（ 独立子任务 ）和投票（ 多个输出以提高准确性 ）两种类型，例如内容审核。

Orchestrator-Workers ： 利用中央协调模型动态地将任务分解为子任务，分配给专门的工作模型 ，并编译结果。与并行化不同，它 能够适应不同的输入复杂性 。

Evaluator-Optimizer ： 评估器-优化器工作流程通过生成初始输出并根据评估模型的反馈进行改进 ，迭代地提高内容质量。例如Actor-Critic算法。

### 3.7.3 Agentic RAG分类

Single-Agent Agentic RAG

Single-Agent Agentic RAG 作为一个集中的决策系统， 负责管理信息的检索、路由和整合 ，适用于有限工具或数据源的设置，可扩展性有限，对于多步推理或大型数据集表现较差。

举例：《Search-o1: Agentic Search-Enhanced Large Reasoning Models》

![原文图片](assets/5b33f7f8c152.jpeg)

Multi-Agent Agentic RAG

Multi-Agent Agentic RAG 通过利用多个专门的代理来处理复杂的工作流程和多样化的查询类型。该系统不再依赖于单个代理来管理所有任务（推理、检索和响应生成），而是 将责任分配给多个代理，每个代理针对特定的角色或数据源进行了优化。 对于分布式、多步骤任务的性能更好，增加模块化和可扩展性。

举例：《Agentic Retrieval-Augmented Generation for Time Series Analysis》

![原文图片](assets/196609fa52e8.png)

一个电商场景下的实际案例：

![原文图片](assets/06894c405886.png)

上图案例的回复：

“您的美国仓直发羽绒服目前仍处于运输中（物流单号：US20240715-001，预计 3 天后抵达您所在城市）。根据《跨境电商退货管理办法》第三章第五条规定，未签收商品可申请物流拦截退货，国际段运费（$50）将从退款中扣除，关税部分需您在退货时提供原始报关单照片（上传入口：订单详情页> 退货申请 > 关税材料）。

如需立即处理，可点击此处申请物流拦截 <操作链接>，拦截成功后系统将自动生成退货单（无需签收商品）。退款预计在仓库确认商品状态无误后 15 个工作日内原路返回，关税退还流程同步启动（预计额外 3 个工作日）。

如需人工复核或修改地址，可直接回复 “转接客服”，当前客服专员已获取您的订单详情，将优先为您处理。”

这是一个电商场景的案例。

用户query ：“美国仓羽绒服未签收，退货关税怎么处理？”

意图识别 模块判定为“跨境未签收退货”场景。

Router Agent 分配任务：

给 跨境政策Agent ：检索《跨境电商退货管理办法》第5条（关税退还条件）。

给 物流Agent ：调用DHL API获取包裹状态（运输中，可拦截）。

给 财务Agent ：查询ERP系统中“未签收退货的关税计算规则”。

不做 ：不直接处理政策文本内容、物流JSON数据或财务公式计算，仅决定“谁该做什么”。

数据集成 ：三个Agent返回的数据格式不同（政策PDF段落、物流API的JSON、财务系统的SQL结果），由独立的 数据集成模块 统一为：

Plaintext
{ 
 "政策依据": "第三章第五条 未签收商品关税需凭报关单申请", 
 "物流状态": "运输中，可申请拦截（链接：XXX）", 
 "关税计算": "国际运费$50从退款扣除，关税需上传报关单" 
}

LLM合成 ：根据上述结构化数据，LLM生成自然语言response，Router Agent不参与内容生成，仅确保数据按正确顺序输入LLM。

在本案例中，Agentic RAG的 优点 在于： 用户获得的不再是 “碎片化政策条款”，而是 “包含具体操作路径的解决方案”；系统不再是 “被动响应查询”，而是 “主动诊断场景并提供最优路径”。

不过Agentic RAG并非尽善尽美，依据最近阅读的论文：Why Do Multi-Agent LLM Systems Fail? 分析一下本案例可能会存在的实际 问题 ：

不遵守任务规范

问题 ：Agent未严格遵循用户查询的具体要求，导致解决方案偏离核心需求。

若用户明确要求“提供未签收商品的关税退还流程”，但 跨境政策Agent 错误引用“已签收商品退货政策”，导致回复中包含“需先签收再申请”的错误步骤，违反用户对“未签收场景”的任务规范。

不遵守角色规范

问题 ：Agent越权或混淆角色职责，破坏分工协作逻辑。

财务Agent 本应负责运费计算，却越权调用物流API获取包裹状态，导致 物流Agent 的职责被架空，流程混乱（如财务Agent错误判断“包裹已签收”，错误计算关税）。

步骤重复

问题 ：Agent重复执行已完成的任务，浪费计算资源并延长响应时间。

案例映射 ： 物流Agent 已返回“包裹运输中，可拦截”，但 协调Agent 未记录状态，再次触发 物流Agent 重复查询同一包裹状态，导致响应延迟10秒以上。

对话历史丢失

问题 ：Agent在多轮对话中丢失关键上下文，导致逻辑断裂。

案例映射 ：用户补充“退货时需要保留原包装吗？”，但Agent因丢失前期“未签收拦截”的对话历史，错误引用“已签收退货需保留包装”的政策，导致回复矛盾。

……

诸如此类的问题仅通过改进Prompt（如更明确的角色定义）只能部分缓解，但无法根治，需要一些结构性策略（如标准化通信协议、强化验证机制）。

分层 Agentic RAG

分层Agentic RAG系统采用结构化的 多层次方法进行信息检索和处理， 代理按层次结构组织，高级代理监督和指导低级代理。这种结构实现了多级决策，确保查询由最合适的资源处理。

![原文图片](assets/07e32b12f932.png)

Agentic Corrective RAG

Corrective RAG 引入了 自我纠正检索结果的机制 ，迭代地改进上下文文档和响应，最小化错误并最大化相关性。

举例：《Agentic AI-Driven Technical Troubleshooting for Enterprise Systems: A Novel Weighted Retrieval-Augmented Generation Paradigm》《Corrective RAG (CRAG)》

![原文图片](assets/f82733df4b11.jpeg)

Adaptive Agentic RAG

其思想在于 根据任务需求动态调整检索策略和工作流程 。工作流程为：代理评估查询及其上下文->基于可用数据和用户需求实时调整检索策略->使用动态工作流程合成响应。

![原文图片](assets/5e547088960f.jpeg)

Graph-Based Agentic RAG

将图知识库与非结构化文档检索相结合。通过结合结构化和非结构化数据源，利用图知识库和反馈循环动态分配任务给专业代理，提高了 RAG 系统的推理和检索准确性。

例子：《Agent-G: An Agentic Framework for Graph Retrieval Augmented Generation》

![原文图片](assets/c2e9a740021d.jpeg)

Agentic文档工作流

Agentic Document Workflows 通过实现端到端的知识工作自动化，扩展了传统的 RAG 范式。这些工作流程协调 以文档为中心的复杂过程，集成了文档解析、检索、推理和结构化输出，并与智能代理结合 。

![原文图片](assets/48a74e9e7446.png)

| 特征 | 传统 RAG | 代理 RAG | 代理文档工作流 （ADW） |
| --- | --- | --- | --- |
| 重点 | 独立的检索和生成任务 | 多智能体协作和推理 | 以文档为中心的端到端工作流程 |
| 上下文维护 | 有限 | 通过内存模块启用 | 在多步骤工作流中维护状态 |
| 动态适应性 | 极小 | 高 | 为文档工作流程量身定制 |
| 工作流编排 | 无 | 协调多代理任务 | 集成多步骤文档处理 |
| 使用外部工具/API | 基本集成（例如，检索工具） | 通过 API 和知识库等工具进行扩展 | 深度集成业务规则和特定领域的工具 |
| 可扩展性 | 仅限于小型数据集或查询 | 可针对多代理系统进行扩展 | 适用于多领域企业工作流 |
| 复杂推理 | 基本（例如，简单的 Q&A） | 使用代理进行多步骤推理 | 跨文档的结构化推理 |
| 主要应用 | QA 系统、知识检索 | 多领域知识和推理 | 合同审查、发票处理、索赔分析等以文档为中心的任务 |
| 优势 | 简单、快速设置 | 高准确率、协作推理 | 端到端自动化，特定领域的智能 |
| 挑战 | 对上下文的理解不佳 | 协调复杂性 | 资源开销、域标准化 |

### 3.7.4 Agentic RAG 工具和数据集

这里只介绍我使用过的工具，更多工具请参考原论文

LangChain 和 LangGraph

LLamaIndex

Hugging Face Transformers 和 Qdrant

RAG评估数据集：

![原文图片](assets/8561c43b037c.png)

Agentic RAG实战项目详见《 https://github.com/asinghcsu/AgenticRAG-Survey?tab=readme-ov-file#implementation-of-rag-agentic-taxonomy-techniques-and-tools 》
