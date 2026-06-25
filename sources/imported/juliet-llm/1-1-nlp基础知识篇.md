---

source_id: juliet-llm

source_file: "居丽叶LLM体系知识搭建.docx"

source_section: "1 nlp基础知识篇"

generated: true

---



# 1 nlp基础知识篇

## 1.1 自注意力

### 1.1.1 前言

每次输入不一样（数目、长度等）的时候怎么处理？输入是一堆向量（一个sequence），例如一句话，语音，图，图片（RGB图视为3个向量）

输出有三种可能性

每个向量对应一个label ，每个label可能是一个数值，那就是regression的问题；如果每个label是一个class，那就是一个classification的问题。例如词性标注，语音识别，每个人的购买意向

![原文图片](assets/47efd7fb9236.png)

整个sequence对应一个label 。例如情感分析，判断一个分子是否是亲水性

![原文图片](assets/0020521baf91.png)

机器自己决定应该要输出多少个label ，也就是seq2seq，输入和输出都是sequence且长度不固定

![原文图片](assets/195975cb6743.png)

seq2seq通过encoder-decoder结构实现。seq2seq的问题是，长sequence中为了计算两个距离较远的单词之间的关系，采用梯度的形式导致的梯度爆炸和消失。使用self-attenion能解决这一问题。

分析第一种情况，也被称为sequence labeling，在这种场景下怎么考虑上下文呢？下例中两个saw明显词性不同，分别丢给 FC 却输出一样，所以需要考虑上下文，把这一个向量前后几个向量都串起来，一起丢到FC。

但是当一个任务需要 考虑整个sequence 时，开太大的window导致FC参数量过大且容易过拟合，这需要self- attention机制。

![原文图片](assets/f45d78dcbfb7.png)

### 1.1.2 self-attention原理

self-attention是一种 将单个序列的不同位置关联起来以计算同一序列的表示的注意机制 。可以把self-attention理解为感受野可以自学习的CNN，CNN是self-attention的特例。self-attention在数据量大时表现优于CNN。

全局建模能力对比

自注意力 : 在全局建模能力上，自注意力机制具有明显的优势，因为它可以显式地捕捉序列中 任意两个元素之间的关系 ，无论它们之间的距离。这使得自注意力机制在处理长距离依赖和全局信息方面非常强大。

CNN : CNN在 局部特征提取方面非常有效 ，但在全局建模能力上可能不如自注意力机制。然而，通过设计特定的网络结构(如使用全局池化层或多尺度卷积)，CNN也可以在一定程度上捕捉全局信息

self attention会 考虑一整个sequence的上下文 ，输入几个vector（向量）就输出几个vector。self-attention可以与 FC(全连接层) 叠加使用，self-attention处理整个sequence的上下文，FC处理某个vector。

![原文图片](assets/c5c5b516cb4a.png)

运作原理：

输入是一个sequence，可能是网络输入或者隐藏层的输出，输出的b是考虑了整个sequence的结果。

![原文图片](assets/1c179b929ca1.png)

怎么产生b1向量？

找出这个sequence里面a1相关的其他向量。关联程度用 【公式开始】\alpha 【公式结束】 表示，将两个向量作为输入，常见计算方式有：

点积 （transformer使用）：a1和a2乘两个矩阵 【公式开始】W^q 【公式结束】 和 【公式开始】W^k 【公式结束】 ,得到q和k，再作点积

Additive ：将q和k串起来放入激活函数

怎么把上面生成的 【公式开始】\alpha 【公式结束】 套用在self attention里面？

【公式开始】\alpha_{1,1}=q^1 \dot k^1 【公式结束】 ,经过softmax进行normalize，（q k对应query和key， 【公式开始】q^1 k^2 【公式结束】 表示第二个向量对第一个向量的影响）

![原文图片](assets/ccd5a64abc31.png)

![原文图片](assets/53064072d875.png)

转化成矩阵格式，带学习的参数只 【公式开始】W^q W^k W^v 【公式结束】 ，注意 A'就是注意力矩阵 ，乘以V得到self-attention的输出O。

![原文图片](assets/8df66a09d9e4.png)

![原文图片](assets/0f8cd4ce6c24.png)

除以 【公式开始】\sqrt{d_k} 【公式结束】 是为了平滑softmax的结果，防止进入了softmax的饱和区，导致梯度值太小而难以训练。

总结下self-attention 与 RNN/LSTM的对比：

引入Self Attention后会 更容易捕获句子中长距离的相互依赖的特征 。 RNN或者LSTM虽然也能捕获长距离的特征，但是对于远距离的相互依赖的特征，要经过若干时间步步骤的信息累积才能将两者联系起来，而距离越远，有效捕获的可能性越小。

self-attention和RNN都能处理时序数据，每个向量都考虑了整个sequence，但RNN需要按顺序计算，无法并行； self-attention可以并行计算 。

### 1.1.3 self-attention改进

位置编码 ：Self-Attention虽然考虑了所有的输入向量，但没有考虑到向量的位置信息。可以通过位置编码(Positional Encoding)来解决这个问题，就是把 位置信息添加到输入序列中，让输入数据本身就带有位置信息 。

上面的a是无序的，需要对a加上位置向量e，e可以通过多种方法产生（ sinusodial、position embedding、floater、rnn 等）。

![原文图片](assets/82b2d494429c.png)

多头注意力 ：把输入序列投影为多组不同的Query，Key，Value，并行分别计算后，再把各组计算的结果合并作为最终的结果。类似CNN中的多个channel，生成多个 【公式开始】W^q W^k W^v 【公式结束】 。（V,K,Q）三个矩阵通过h个线性变换，分别得到h组（V,K,Q）矩阵，每一组（V,K,Q）经过Attention计算， 得到h个Attention Score并进行拼接（Concat），最后通过一个线性变换得到输出 ，其维度与输入词向量的维度一致，其中h就是多头注意力机制的“头数”。

![原文图片](assets/b19ab7f4c6c4.png)

### 1.1.4 self-attention代码

Python
import torch.nn as nn
import numpy as np
import torch
import math
# 多头注意力 
class MHA(nn.Module):
 def __init__(self, num_head, dimension_k, dimension_v, d_k, d_v, d_o):
 # d_k表示head dimension，d_k * num_head 就是embedding的长度
 super().__init__()
 self.num_head = num_head
 self.d_k = d_k
 self.d_v = d_v
 self.d_o = d_o
 self.fc_q = nn.Linear(dimension_k, num_head * d_k)
 self.fc_k = nn.Linear(dimension_k, num_head * d_k)
 self.fc_v = nn.Linear(dimension_v, num_head * d_v)
 self.fc_o = nn.Linear(num_head * d_v, d_o)
 self.softmax = nn.Softmax(dim=2)
 
 
 def forward(self, q, k, v, mask):
 
 batch, n_q, dimension_q = q.size()
 batch, n_k, dimension_k = k.size()
 batch, n_v, dimension_v = v.size()
 
 q = self.fc_q(q)
 k = self.fc_k(k)
 v = self.fc_v(v)
 q = q.view(batch, n_q, self.num_head, self.d_k).permute(2, 0, 1, 3).contiguous().view(-1, n_q, self.d_k)
 k = k.view(batch, n_k, self.num_head, self.d_k).permute(2, 0, 1, 3).contiguous().view(-1, n_k, self.d_k)
 v = v.view(batch, n_v, self.num_head, self.d_v).permute(2, 0, 1, 3).contiguous().view(-1, n_v, self.d_v)
 
 attention = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(self.d_k)
 mask = mask.repeat(self.num_head, 1, 1)
 attention = attention + mask
 attention = self.softmax(attention)
 
 output = torch.matmul(attention, v)
 output = output.view(self.num_head, batch, n_q, self.d_v).permute(1, 2, 0, 3).contiguous().view(batch, n_q, -1)
 output = self.fc_o(output)
 return attention, output
# Multi query attention
class MQA(nn.Module):
 def __init__(self, num_head, dimension_k, dimension_v, d_k, d_v, d_o):
 super().__init__()
 self.num_head = num_head
 self.d_k = d_k
 self.d_v = d_v
 self.d_o = d_o
 self.fc_q = nn.Linear(dimension_k, num_head * d_k)
 self.fc_k = nn.Linear(dimension_k, d_k)
 self.fc_v = nn.Linear(dimension_v, d_v)
 self.fc_o = nn.Linear(num_head * d_v, d_o)
 self.softmax = nn.Softmax(dim=2)
 
 
 def forward(self, q, k, v, mask):
 
 batch, n_q, dimension_q = q.size()
 batch, n_k, dimension_k = k.size()
 batch, n_v, dimension_v = v.size()
 
 q = self.fc_q(q)
 k = self.fc_k(k)
 v = self.fc_v(v) 
 q = q.view(batch, n_q, self.num_head, self.d_k).permute(2, 0, 1, 3).contiguous().view(-1, n_q, self.d_k) 
 k = k.repeat(self.num_head, 1, 1)
 v = v.repeat(self.num_head, 1, 1)
 
 attention = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(self.d_k)
 mask = mask.repeat(self.num_head, 1, 1)
 attention = attention + mask
 attention = self.softmax(attention)
 
 output = torch.matmul(attention, v)
 output = output.view(self.num_head, batch, n_q, self.d_v).permute(1, 2, 0, 3).contiguous().view(batch, n_q, -1)
 output = self.fc_o(output)
 return attention, output

batch = 10
num_head = 8
n_q, n_k, n_v = 2, 4, 4 # sequence 长度
dimension_q, dimension_k, dimension_v = 128, 128, 64 # embedding的长度
d_k, d_v, d_o = 16, 16, 8
q = torch.randn(batch, n_q, dimension_q)
k = torch.randn(batch, n_k, dimension_k)
v = torch.randn(batch, n_v, dimension_v)
mask = torch.full((batch, n_q, n_k), -np.inf) 
mask = torch.triu(mask)
mha = MHA(num_head, dimension_k, dimension_v, d_k, d_v, d_o)
attention, output = mha(q, k, v, mask)
print(attention.size(), output.size())

mqa = MQA(num_head, dimension_k, dimension_v, d_k, d_v, d_o)
attention, output = mqa(q, k, v, mask)
print(attention.size(), output.size())

## 1.2 transformer

![原文图片](assets/7c0e5558510e.png)

### 1.2.1 Embedding

由 输入的 embedding 和位置编码相加 得到，后面的文章详细介绍。

输入的embedding可以通过 word2Vec，bert，OpenAI Embedding API 等方式获取，目的是 将文本映射到连续的向量空间（把文本变成模型能处理的向量）。

位置编码是为了 捕捉输入中token的顺序信息 ，常用的有 rope ，绝对位置编码等

### 1.2.2 Encoder

上图中红色部分就是encoder，由 Multi-Head Attention, Add & Norm, Feed Forward, Add & Norm 组成。输入为矩阵 【公式开始】X \in R^{n \times d} 【公式结束】 ，n是输入的长度，d是embedding的维度（简单理解为embedding会把一个token转成一个d维向量），每一个encoder block都会输出一个矩阵 【公式开始】X \in R^{n \times d} 【公式结束】 。最终encoder的输出就是编码信息矩阵。

Add & Norm

有两次layer normalization（对 每个样本的特征维度 进行归一化，可以加速训练过程和提高模型的泛化性能）和残差操作，分别是：

![原文图片](assets/4f747a78d4f5.png)

这种normalization被称为 post-norm ，本文后面会详细介绍。

Feed Forward

两个简单的全连接层。

![原文图片](assets/dc85f6dced9b.png)

### 1.2.3 Decoder

上图中绿色部分就是decoder，其中第一个多头注意力使用了 掩码矩阵 。第二个多头注意力使用了 cross-attention 。decoder之后会有一个softmax层用来预测下一个文本。

掩码矩阵

如下图所示，解码过程中会 把将之前预测的输出作为当前预测的输入 ，通过掩码矩阵可以防止第 i 个文本知道 i+1 个文本之后的信息。

![原文图片](assets/25d12d17c0a6.png)

掩码矩阵在自注意力中的softmax之前使用 。

![原文图片](assets/9f00a728be89.png)

![原文图片](assets/382f65f29ef7.png)

cross-attention

这里的K和V矩阵是由encoder的编码信息矩阵计算得到的，Q是由上一个decoder block计算得到的。

![原文图片](assets/cdbb4d7cf824.png)

softmax

由于之前使用了掩码矩阵，第i个单词的预测只包含了前i个单词的信息。softmax会输出一个长度为m的向量（m是词表长度），其中 元素加和为1 ，每个元素表示预测这个单词的概率。然后根据decoding方法（后面的文章详细介绍）确定输出哪个单词。

transformer总结：

优点：支持并行计算（RNN需要顺序计算），有一定捕获长距离语义的能力，已经衍生出了大量的模型。

缺点：计算复杂度 【公式开始】O(n^2) 【公式结束】 ，需要大量数据进行训练。

### 1.2.4 pre-norm和post-norm的区别？

pre-norm 和 post-norm 分别指的是把normalization操作放在残差连接之前和之后。

![原文图片](assets/7f0bfe57819b.jpeg)

先说结论：Pre-Norm结构往往更容易训练，但最终效果通常不如Post-Norm 。 参考文献是 《Understanding the Difficulty of Training Transformers》 和 《RealFormer: Transformer Likes Residual Attention》 。

这里指的是post-norm在最优设置下的性能是优于pre-norm的，而不是在相同配置下，因为post-norm更难训练，需要一些额外的操作（比如需要添加学习率warmup）。

pre-norm效果为什么更差？

对于pre-norm迭代可以得到：

![原文图片](assets/00ee720a880d.jpeg)

其中每一项都是同一量级的（苏剑林认为这一说法并不准确，这是一个基于直觉的判断，即为了追求稳定的梯度，认为每一层的更新量都比较接近），那么有 【公式开始】x_{t+1}=O(t+1) 【公式结束】 ，也就是说第t+1层跟第t层的差别就相当于t+1与t的差别， 当t较大时， 【公式开始】x_{t+1}和x_t 【公式结束】 的相对差别是很小的 ，因此就有：

![原文图片](assets/c2b826f6bf00.jpeg)

这个公式的意思是由于 【公式开始】x_{t+1}和x_t 【公式结束】 的相对差别小， 【公式开始】F_{t+1}(Norm(x_{t+1})) 和 F_{t+1}(Norm(x_{t})) 【公式结束】 很接近，原本是一个t层的模型与t+1层拼接， 近似等效于一个更宽的t层模型 。在Pre-Norm中多层叠加的结果更多是增加宽度而不是深度，层数越多，这个层就越“虚”。而 对于深度学习模型，深度比宽度更重要 。

post-norm为什么更难训练

先说结论：post-norm严重削弱了残差的恒等分支，所以反而失去了残差“易于训练”的优点，通常要warmup并设置足够小的学习率才能使它收敛。

假设初始状态的x和F(x)的方差均为1，假设这二者相互独立，normalization操作为了将方差降为1，这样初始阶段的post-norm相当于：

![原文图片](assets/754ad01fa973.jpeg)

迭代下去就得到了：

![原文图片](assets/4b1022161be5.jpeg)

残差的本意是为了给前面的层添加一个快速通道，保障梯度快速回传，而post-norm削弱了这个快速通道，残差名存实亡，容易导致梯度消失，难以训练。

梯度消失指的是在深度网络的反向传播阶段，梯度在从输出层向输入层传播的过程中逐渐变小，最终趋于接近零 。前面的层梯度较小乃至不更新，会导致后面层的输入质量变低，从而导致模型准确率降低。为了缓解梯度消失，就可以采用残差连接，补 上一个梯度为常数的项 。

梯度消失在微调模型时是优点 。因为微调希望优先调整后面的层，而前面的层少调整，避免破坏预训练学到的知识。梯度消失正好对前面的层调整较弱。所以，预训练好的Post-Norm模型，往往比Pre-Norm模型有更好的微调效果。

再插入个知识，为什么adam优化器比SGD优化器更容易收敛（受梯度消失影响小）？

Adam优化器的更新公式如下：

![原文图片](assets/68b0f62cb431.jpeg)

Adam每一轮的更新量是 【公式开始】O(\eta) 【公式结束】 量级的 ，理论上只要梯度的绝对值大于随机误差，那么对应的参数都会有常数量级的更新量；而 SGD的更新量正比于梯度 ，梯度过小会导致参数不更新，因此受梯度消失影响更严重。

与之对比的 pre-norm保留了完整的快速通道 ：

![原文图片](assets/01eb0d7771e5.jpeg)

warmup学习率对post-norm的作用

warmup学习率指 学习率随着轮数逐渐增长到目标学习率 。如果不进行warmup学习率，那么后面的层学习会很快，但由于前面的层梯度消失，学习的并不好，导致后面的层是建立在糟糕的输入上的。这会导致模型陷入局部最优，最坏的情况下， 前面的层学习效果过于差，后面层每轮的更新变成了随机常数，loss发散成NAN。

而使用warmup，就留给模型足够多的时间进行“预热”，在这个过程中，主要是抑制了后面的层的学习速度，并且给了前面的层更多的优化时间，以促进每个层的同步优化。

deepnorm

对输入乘上一个 【公式开始】\alpha > 1 【公式结束】 ，保障快速通道的系数能保持比较大。

![原文图片](assets/0920aa65dfff.jpeg)

总结：

Post-Norm ：适合 较浅 的 Transformer 网络，或者任务不太复杂时，它可以取得更好的准确性。

Pre-Norm ：对于 深层 Transformer 模型，它的梯度更加稳定，收敛性有保障，因此通常在深度模型中表现得更好。

## 1.3 Tokenizer

这一节中的图都出自 《大语言模型LLM基础之Tokenizer完全介绍》 ，视频讲解的非常清晰。

![原文图片](assets/a9028b7fb004.jpeg)

### 1.3.1 Word-based Tokenizer

将文本划分为一个个词 ，缺点是将相同意思的词划为不同的token，且词表巨大。巨大的词表意味着需要学习巨大的embedding matrix，会导致空间复杂度和时间复杂的的大幅增加。

### 1.3.2 Character-based Tokenizer

将文本划分为一个个字符 ，缺点是相较于word-based，信息量很低，模型性能差，且Token序列很长。

### 1.3.3 Subword-based Tokenizer

以上两者的折中。 对于高频的字符串片段（比如常用词、词根、词缀），将其作为一个整体的token，而不是再继续细分为更小的单位。 具体分为以下几种 ：

Byte Pair Encoding Tokenizer(BPE)

BPE的输入是一个语料库corpus，以英文举例包括很多的单词，初始的词表采用Character-based Tokenizer的词表。迭代地进行词频统计和词表合并两步，直到达到合并次数上限。

词频统计 ：统计词中相邻token共同出现的词频

词表合并 ：将最常出现的相邻token加入到词表中

![原文图片](assets/287d36819333.jpeg)

![原文图片](assets/cebe1a54638b.jpeg)

![原文图片](assets/972fa1797b2e.jpeg)

Byte-level BPE(BBPE)

BPE的缺点在于其初始词表很大， B BPE用两个字节表示一个token的unicode码 ，将unicode码作为基础token。

![原文图片](assets/62685bb588f6.jpeg)

WordPiece Tokenization

与BPE的思路基本一样，区别在于合并的规则不同。

![原文图片](assets/7caf7144a113.jpeg)

Unigram Tokenization

先初始化一个很大的词表（包含字母、所有字词）。

![原文图片](assets/1e5ceb56565b.jpeg)

Unigram 算法假设每个词都是独立出现的，因此整个单词出现的概率就是其中每个词概率的乘积。 计算出corpus中每个单词出现的最大概率，作为该单词的分词方式。

![原文图片](assets/9ed1164a8f4c.jpeg)

每一轮删除一个子词， 该子词满足删除后负对数似然变得最小 。如果每个子词删除后负对数似然大小一样，则随即删除一个。删去p%loss最小的token。

![原文图片](assets/dc6495287607.jpeg)

SentencePiece（使用BBPE或Unigram）

![原文图片](assets/4c6a12de92d4.jpeg)

最后总结一下以上分词方法对应的常见模型：

![原文图片](assets/e7209664f33d.jpeg)

在transformers库中使用tokenizer

Python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("uer/roberta-base-finetuned-dianping-chinese")
sen = "弱小的我也有大梦想!"
inputs = tokenizer(sen, padding="max_length", max_length=15)
print(inputs)
# {
# "input_ids": [101, 2483, 2207, 4638, 2769, 738, 3300, 1920, 3457, 2682, 106, 102, 0, 0, 0], 
# "token_type_ids": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# "attention_mask": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
# }
# inputs_ids 对应embedding，
# token_type_ids表示属于第几个句子，
# attention_mask表示embedding中哪部分是真实有效的。

## 1.4 位置编码

卷积具有局部性，天然地注意到了元素之间的相对位置。而基于自注意力的 transformer模型则对位置不敏感 ，因此必须要把元素的位置信息加入到embedding中。

### 1.4.1 绝对位置编码

绝对位置编码 直接将位置信息加到文本的embedding 中，被早期的BERT、GPT2等模型中使用。绝对位置编码又可以分为可学习的和固定的两种。

可学习绝对位置编码 ：直接对不同的位置随机初始化一个 postion embedding，加到文本的embedding 上输入给模型， 作为参数进行训练 。这种方法引入了大量的可学习参数，需要大量的数据才能训练。

固定的绝对位置编码 ：代表是《Attention is all you need.》论文中的三角位置编码。

位置 pos 对应的位置向量在偶数位和奇数位的值分别为：

![原文图片](assets/a6e24aba5d24.jpeg)

其中 【公式开始】d_{model} 【公式结束】 是位置编码的长度， 【公式开始】i \in [0,1,...,(d_{model} - 1) / 2] 【公式结束】 。采用这种设计， pos+k位置的位置编码可以用pos位置的位置编码线性表示，体现了其相对位置关系。

这里的相对位置关系指的是两个token之间的，但是 绝对位置编码每个位置的编码是固定的 ，而 相对位置编码直接考虑两个token之间的相对位置。

证明：需要用到三角公式，定义 【公式开始】w_i = \frac{1}{10000^{2i / d_{model}}} 【公式结束】

![原文图片](assets/611bfdecf3ef.jpeg)

![原文图片](assets/5af84ef9b864.jpeg)

为了计算pos+k和pos之间的距离，可以通过计算他们之间的内积

![原文图片](assets/059568161e67.jpeg)

可以看到pos+k和pos之间的内积随着相对距离的增加而减小，符合文本中token之间一般距离越远关系越弱的原理。但是由于相对距离的对称性， 三角位置编码无法区分方向 ，即pos+k与pos和pos-k与pos之间的距离使用一样的。实现三角位置编码的代码如下：

Python
class PositionalEncoding(nn.Module):
 def __init__(self, d_model, dropout, max_len=5000):
 super().__init__() 
 self.dropout = nn.Dropout(p=dropout) # 初始化dropout层
 
 # 计算位置编码并将其存储在pe张量中
 pe = torch.zeros(max_len, d_model) # 创建一个max_len x d_model的全零张量
 # 生成0到max_len-1的整数序列，并添加一个维度
 position = torch.arange(0, max_len).unsqueeze(1) 
 # 计算div_term，用于缩放不同位置的正弦和余弦函数
 div_term = torch.exp(torch.arange(0, d_model, 2) *
 -(math.log(10000.0) / d_model))
 
 # 对于d_model的偶数索引，使用正弦函数；对于奇数索引，使用余弦函数。
 pe[:, 0::2] = torch.sin(position * div_term)
 pe[:, 1::2] = torch.cos(position * div_term)
 pe = pe.unsqueeze(0) # 在第一个维度添加一个维度，以便进行批处理
 
 # 定义前向传播函数
 def forward(self, x):
 # 将输入x与对应的位置编码相加
 x = x + self.pe[:, : x.size(1)]
 # 应用dropout层并返回结果
 return self.dropout(x)

总结： 绝对位置编码实现简单，存在以下缺点：

尽管能包含一定的相对位置信息，但是这种信息仅仅保存在位置编码内部， 在计算自注意力时，这种位置信息就被破坏了。

一个token的位置编码是什么由其在句子中的绝对位置决定，但是 真正重要的往往不是绝对位置，而是它与其他token之间的关系。

对输入的长度敏感 ，一旦输入变化则需要重新调整。

### 1.4.2 相对位置编码

相对位置编码将两个token的相对位置信息添加到对应的attention值中。

Attention with linear biases enables input length extrapolation（ALiBi）

在计算attention时，对前边位置的分数进行惩罚，如图所示：

![原文图片](assets/e9b3aca9aa72.png)

传统的绝对位置编码在训练时会为每个位置分配一个固定的向量，模型可能会过度拟合这些特定长度的模式。而 ALiBi通过在注意力分数计算中直接使用线性偏置，减少了模型对特定序列长度的依赖，从而提高了对未见过的序列长度的泛化能力 。

ALiBi的位置偏差随距离线性增长 ，这种设计让模型在处理不同长度的序列时，可以自然地根据距离调整注意力权重，无需显式学习位置编码的复杂周期性结构。

由于线性偏置的引入直接与序列中元素的位置相关，没有固定大小的编码矩阵限制，理论上模型可以更容易地处理任意长度的序列，从而展现出良好的长度外推性能。

通过直接在注意力分数上施加与距离相关的线性惩罚， ALiBi鼓励模型关注更近的位置，同时不完全排除远处的依赖 ，从而在一定程度上平衡了局部和全局依赖的学习，这对于处理长序列尤其有利。

XLNET

三角位置编码在计算attention时的表示如下：

![原文图片](assets/f9ec1dce388d.png)

从绝对位置编码出发：

![原文图片](assets/efae3d1efe49.png)

XLNET将 【公式开始】p_j 【公式结束】 替换成相对位置向量 【公式开始】R_{i-j} 【公式结束】 ， 【公式开始】p_i 【公式结束】 替换成可训练的向量u和v，

![原文图片](assets/c0b47096f9b4.png)

![原文图片](assets/92049934f64f.png)

T5

（7）式中的每一项可以理解为“输入-输入”、“输入-位置”、“位置-输入”、“位置-位置”四项注意力的组合，由于 输入信息与位置信息应该是独立（解耦） 的，它们不应该有过多的交互，所以“输入-位置”、“位置-输入”两项Attention可以删掉，“位置-位置”实际上是一个依赖于（s,）的一个标量。

此外，通过固定的桶函数 b(t-s) ，将 t-s 从 [−128,128] 压缩至 [0,31] ，再对每个 b(t-s) 训练对应的偏移量 【公式开始】r_{b(t-s)} 【公式结束】

![原文图片](assets/6e349775e707.png)

DeBERTa

与T5相反， 扔掉“位置-位置”一项只保留剩下三项 ，通过通过 【公式开始】δ(t,s) 【公式结束】 将 t−s 直接截断在区间 (−k,k] 内

![原文图片](assets/748fff6a4a5e.png)

DeBERTa在softmax时校正系数为 【公式开始】\sqrt{3d} 【公式结束】 ，不是默认的 【公式开始】\sqrt{d} 【公式结束】 。此外，指出NLP的大多数任务可能都只需要相对位置信息，但确实有些场景下绝对位置信息更有帮助，于是它将整个模型分为两部分来理解。以Base版的MLM预训练模型为例，它一共有13层，前11层只是用相对位置编码，这部分称为Encoder，后面2层加入绝对位置信息，这部分它称之为Decoder；至于下游任务的微调截断，则是使用前11层的Encoder加上1层的Decoder来进行。

### 1.4.3 旋转位置编码RoPE

RoPE实现了绝对位置编码和相对位置编码的统一，它 通过绝对位置编码的形式，实现了相对位置编码的效果 。

RoPE将输入序列的位置信息通过 旋转操作 嵌入到self-attention的计算中 ，不同位置的 token 可以有不同的旋转角度，从而嵌入位置信息，从而增强模型对长序列和相对位置的处理能力。 RoPE的频率（base）是可学习的 ，在自注意力公式中结合了明确的相对位置依赖性。

RoPE保持了序列长度的灵活性、随相对距离的增加而衰减的token间依赖性。其原理如下图，针对词嵌入维度 【公式开始】d_{model} 【公式结束】 为2的情况， 【公式开始】x_m^{'} 【公式结束】 表示经过RoPE后的结果：

![原文图片](assets/263a6eb4891d.jpeg)

从内积的角度推导：

![原文图片](assets/f56faa085141.jpeg)

![原文图片](assets/ad30db3b46a3.jpeg)

![原文图片](assets/65fc8571b181.jpeg)

上图中第四行中间矩阵应该是【 【cos(n-m)θ, -sin(n-m)θ】, 【sin(n-m)θ, cos(n-m)θ】 】

对于多维的旋转位置编码，可以简化为以下形式：

![原文图片](assets/56388ee160fa.jpeg)

结合代码来看，在chatglm中，因为内积计算与顺序无关，巧妙地将所有负数和正数分开

![原文图片](assets/f9f03eac79c1.png)

从公式的角度推理：

要计算m和n之间的距离，假设query 【公式开始】q_m 【公式结束】 和key 【公式开始】k_n 【公式结束】 之间的内积可以用函数 【公式开始】g(x_m', x_n', m-n) 【公式结束】 表示，函数 【公式开始】g(x_m', x_n', m-n) 【公式结束】 的定义如下：

![原文图片](assets/616a92a8f05b.jpeg)

总结下RoPE的流程： 首先计算得到q和k矩阵，然后对q和k向量的元素按顺序，两两一组应用RoPE ，例如：

![原文图片](assets/654b3feee129.png)

那么对于m和n之间的考虑位置距离的注意力就是：

![原文图片](assets/32f2b224fc4a.png)

得到的注意力随m与n之间的距离增大而减小， 注意对v矩阵不需要应用RoPE 。

改进：xPOS

RoPE能扩展到任意长度，但其外推性能较差：虽然RoPE可以拓展到任意长度，但对于语言建模等生成任务，无法在测试长序列性能时，维持其在训练长度序列上的表现。 xPos在旋转的基础上，在旋转角度向量的每个维度上都包含了独特的指数衰减因子 ，以及blockwise causal attention，让模型忽略相距较远的语义：

![原文图片](assets/a4afba183d0e.jpeg)

## 1.5 Decoding

经过一系列self-attention操作后，需要将一个token对应的d维向量映射到词库维的向量，然后经过softmax输出对这个token的预测向量。Decoding就是根据预测向量选择这个token对应的单词的过程

### 1.5.1 Greedy Search

迭代的预测每个token时，每次都 选择概率最大的单词 ，将选中的token添加到序列中，继续预测下一个token，速度非常快。

面临问题：一旦有一个错误，就会影响后续的预测； 生成的文本会比较单调 ，因为 容易陷入局部最优 ，很难找到最优解。可以通过惩罚重复的字段进行缓解。

应用场景：适用于对推理速度要求高、对文本质量要求不高的场景。

### 1.5.2 Beam Search

beam search是对贪心策略一个改进，在每一个时间步，不再只保留当前分数最高的1个输出，而是 保留num_beams个 。当num_beams=1时集束搜索就退化成了贪心搜索 。是一种启发式图搜索算法，通常用在图的解空间比较大的情况下， 为了减少搜索所占用的空间和时间，在每一步深度扩展的时候，剪掉一些质量比较差的结点 ，保留下一些质量较高的结点。这样减少了空间消耗，并提高了时间效率。通常选择概率最高的完整序列作为最终输出。

面临问题：有可能存在潜在的最佳方案被丢弃，因此Beam Search算法是不完全的，一般用于解空间较大的系统中；计算成本比贪心更高

![原文图片](assets/331486ad3291.png)

### 1.5.3 Top k 抽样

思路：从 tokens 里选择 k 个作为候选， 然后根据它们的 likelihood scores 来采样模型从最可能的"k"个选项中随机选择一个 ，如果k=3，模型将从最可能的3个单词中随机选择一个。

面临问题： 在分布陡峭的时候仍会采样到概率小的单词，或者在分布平缓的时候只能采样到部分可用单词 ；k不太好选：k设置越大，生成的内容可能性越大；k设置越小，生成的内容越固定；设置为1时，和 greedy decoding 效果一样。

### 1.5.4 Top p抽样/核采样

思路 ： 候选词列表是动态的， 从 tokens 里按百分比选择候选词，模型从累计概率大于或等于“p”的最小集合中随机选择一个 ，如果p=0.9，选择的单词集将是概率累计到0.9的那部分。

top-P采样方法往往与top-K采样方法结合使用，每次选取两者中最小的采样范围进行采样，可以减少预测分布过于平缓时采样到极小概率单词的几率。如果k和p都启用，则p在k之后起作用。

top-P越高，候选词越多，多样性越丰富。top-P越低，候选词越少，越稳定

面临问题：采样概率p设置太低模型的输出太固定，设置太高，模型输出太过混乱。

### 1.5.5 Temperature

![原文图片](assets/b4e3c9055bcd.png)

思路：通过温度，在采样前调整每个词的概率分布。 温度越低，概率分布差距越大，越容易采样到概率大的字。温度越高，概率分布差距越小，增加了低概率字被采样到的机会。

参数temperature(取值范围：0-1)设的越高，生成文本的自由创作空间越大，更具多样性。温度越低，生成的文本越偏保守，更稳定。

一般来说，prompt 越长，描述得越清楚，模型生成的输出质量就越好，置信度越高，这时可以适当调高 temperature 的值；反过来，如果 prompt 很短，很含糊，这时再设置一个比较高的 temperature 值，模型的输出就很不稳定了。

### 1.5.6 联合采样（top-k & top-p & Temperature）

top-k、top-p、Temperature都是属于 随机采样 的方法，即在采样的过程中加入了一定的随机性，这可能会导致生成的句子容易不连贯，上下文比较矛盾。为了缓解这种随机性，将 top-k、top-p、Temperature 联合起来使用。使用的先后顺序是 temperature - top-k-/top-p。

## 1.6 Normalization

normalization，即归一化，旨在 将数据的数值范围缩放到正态分布 ，通常是为了消除不同特征之间的量纲差异，使得数据更加适合进行后续的分析和处理，保证网络的稳定性。对于有很多层的深度模型，如果数据分布在某一层出现明显的偏移误差，随着网络的加深这一问题会加剧 （ 内部协变量偏移，internal covariate shift，ICS ） 。 通过使用normalization，可以减轻内部协变量偏移，稳定训练过程，避免出现梯度消失和爆炸；使数据远离Sigmoid激活函数的饱和区，加速模型收敛；避免模型对某些数据的过拟合，提升模型的泛化能力。

对于nlp任务来说，最常用的是Layer Normalization和 RMSNorm

### 1.6.1 Batch Normalization（BN）

在神经网络的每一层中，对 每个mini-batch 的输入进行归一化处理。

优点：加速网络训练、防止梯度问题、优化正则化效果、降低学习率要求，并有助于缓解过拟合，从而显著提升神经网络的性能和稳定性。

缺点：BN对batch-size的大小敏感；要求数据长度一致；受离群数据的影响很严重。

### 1.6.2 Layer Normalization（LN）

在神经网络的每一层中，对每个样本的 所有特征通道 进行归一化处理。

![原文图片](assets/9123731fdd25.jpeg)

优点： 在训练样本较小、样本间相互影响较大的情况下更稳定，主要应用于RNN。

Python
class LayerNorm(nn.Module):
 # features: (bsz, max_len, hidden_dim)
 def __init__(self, features, eps=1e-6):
 super(LayerNorm, self).__init__()
 self.a_2 = nn.Parameter(torch.ones(features))
 self.b_2 = nn.Parameter(torch.zeros(features))
 self.eps = eps
 def forward(self, x):
 # 就是在统计每个样本所有维度的值，求均值和方差，所以就是在hidden dim上操作
 # 相当于变成[bsz*max_len, hidden_dim], 然后再转回来, 保持是三维
 mean = x.mean(-1, keepdim=True) # mean: [bsz, max_len, 1]
 std = x.std(-1, keepdim=True) # std: [bsz, max_len, 1]
 # 注意这里也在最后一个维度发生了广播
 return self.a_2 * (x - mean) / (std + self.eps) + self.b_2

### 1.6.3 Instance Normalization（IN）

对 每个样本的每个特征通道 进行归一化。

优点： 更适用于图像生成等任务中，每个样本的特征通道独立于其他样本的情况。

### 1.6.4 Group Normalization（GN）

IN和LN的融合，在神经网络的每一层中， 将特征分成若干组，对每个组的特征进行归一化处理。

优点： 适用于样本较小、样本间相互影响较大，但又不需要对整个mini-batch进行归一化的情况。

总结：

Batch Normalization 对batch的维度去做归一化，也就是针对不同样本的同一特征做操作， Layer Normalization 对hidden的维度去做归一化，也就是针对单个样本的不同特征做操作。

Batch Normalization 是对这批样本的同一维度特征（每个神经元）做归一化， Layer Normalization 是对这单个样本的所有维度特征做归一化。

Instance Normalization 是在每个通道的维度进行归一化，Group Normalization是IN和LN的融合。

下图很好的总结了以上介绍的几种Normalization的示意。

![原文图片](assets/2f8434c44237.png)

### 1.6.5 RMSNorm

LayerNorm每次都需要计算均值和方差，而RMSNorm去中心化的操作，只有缩放的操作， 只需要计算方差计算量更小 。这也是Llama模型使用的Normalization方法。

对于给定的输入 【公式开始】X 【公式结束】 (其中 【公式开始】 X 【公式结束】 是一个 【公式开始】n\times d 【公式结束】 的矩阵， 【公式开始】n 【公式结束】 是批次大小， 【公式开始】d 【公式结束】 是特征维度)，RMSNorm 的计算可以表示为:

首先计算每个样本的特征平方的均方根（均值的平方根）：

【公式开始】\mu = \frac{1}{d} \sum_{i=1} ^d x_i^2 【公式结束】

接着计算均方根的倒数，同时加上一个小的常数 【公式开始】\sigma 【公式结束】 以避免除以零：

【公式开始】RMS = \sqrt {\frac{1}{\mu +\sigma}} 【公式结束】

最后，使用得到的 RMS 值对输入 【公式开始】X 【公式结束】 进行归一化，并乘以可学习的权重参数 【公式开始】w 【公式结束】 :

【公式开始】Y = X * RMS * w 【公式结束】

Python
class RMsNorm(torch.nn.Module):
 def __init__(self, dim:int, eps:float =1e-6):
 super()._init_()
 self.eps=eps
 self.weight =nn.Parameter(torch.ones(dim))
 def _norm(self，x):
 return x*torch.rsqrt(x.pow(2).mean(-1,keepdim=True)+ self.eps)
 def forward(self，x):
 output =self._norm(x.float()).type_as(x)
 return output* self.weight

RMSNorm对比LayerNorm的优点

RMSNorm 不计算均值 ， 计算效率更高 ，更适合大规模数据计算。

RMSNorm 减轻了内部协变量偏移的影响 ，仅对输入的均方根值进行归一化，受异常特征值导致的梯度不稳定影响更小，训练更加稳定。

RMSNorm 可以 加快模型收敛速度 ，降低了训练初期模型需要调整的幅度

| 维度 | Batch Normalization | Layer Normalization | RMSNorm |
| --- | --- | --- | --- |
| 归一化维度 | 沿 Batch 维度（对每个通道单独归一化） | 沿 特征维度（对每个样本单独归一化） | 沿 特征维度（无均值中心化） |
| 计算开销 | 高（需统计Batch维度均值/方差） | 中（统计特征维度均值/方差） | 低（仅统计特征维度方差） |
| Batch依赖 | 强（Batch Size小效果差） | 无 | 无 |
| 优点 | 加速训练，提升泛化能力 | 对变长序列友好，适合小Batch训练 | 计算高效，训练稳定性与LN相当 |
| 缺点 | 依赖Batch Size，对动态网络不友好 | 对特征维度敏感，可能抑制表达能力 | 无均值中心化，可能损失部分信息 |

## 1.7 Embedding

embedding中文名是嵌入，目的是将tokenizer之后的词转化成向量矩阵，也就是词向量。本节介绍一些传统的embedding方法，和近些年提出的方法。

### 1.7.1 静态编码

独热编码

将的单词表示为一个长度为V的向量， 其中只有一个位置是1，其他位置都是0 。V是语料库的大小。

缺点：独热编码无法表示单词之间语义的相似度，因为不同词之间的相似度都是一样的；独热编码很稀疏，会浪费空间。

Word2Vec

包括Skip-Gram（SG）和CBOW。 SG模型需要根据target来预测上下文的词 （即target左右的词，称为context）；而 CBOW相反，需要根据context来预测target ，准确来说，是使用规定窗口范围内的context的平均（或求和）来预测target。

| SG | CBOW |
| --- | --- |
|  |  |

二者存在以下区别：

训练的速度不同 。 从训练集的样本数量来说， CBOW的样本数量比SG样本数量少得多 。假设有n个target，窗口大小为w（target左右取w个context word），那么SG的样本数量接近2 ∗ w ∗ n ，而CBOW的样本数量近似为n.

训练的效果不同 。SG适用于相对少量的训练数据，对于稀有词的效果更好（可以得到表征能力很好的embedding）。 CBOW比SG的训练速度快了几倍 ， 并且因为CBOW的中对context取平均，模型会预测更经常出现的单词，常用词的表征的效果要比SG好一点。

![原文图片](assets/4b49fb4db9dc.png)

Word2Vec的缺点和解决方法：

针对高频但意义不大的Stop Word（例如The）充斥训练样本，可以通过设置在训练原始文本中遇到的每一个单词，它们按照一定概率保留，保留的概率与单词的频率成反相关。

在Word2Vec预测的时候， 输出的是预测目标词的概率 ，也就是说每一次预测最后的SoftMax层都要基于全部的词表进行计算，这无疑会带来很大的时间开销。为了加快训练速度，提出了Hierarchical softmax和Negative Sampling。

Hierarchical softmax ：使用树的层级结构替代扁平化的标准Softmax，在计算P(y = j)时，只需要计算一条路径上所有节点的概率值。树的结构是根据类别的频数构造的 霍夫曼树 。

Negative Sampling ：每次随机选择k个出现概率高的negative word（即预测错误的词）和positive word（预测正确的词）进行计算，k一般为2-20。

FastText

word2vec将每个单词作为最小单位，为每个单词生成一个向量，这忽略了单词内部的形态特征（如 apple 和 apples）。

介绍FastText之前，先介绍n-gram。基本思想是将文本内容按照字节顺序进行大小为N的 滑动窗口 操作，最终形成长度为N的字节片段序列。利用 n-gram 可以构建许多文本特征，例如当n=3时，即trigram，“apple”可以构建出：

【公式开始】<ap, app, ppl, ple, le> 【公式结束】

<表示前缀，>表示后缀。利用这些trigram来表示“apple”这个单词，进一步，我们可以用这5个trigram的embedding和apple本身的embedding叠加来表示“apple”的词向量。这样的好处是：

对于低频词生成的词向量效果会更好 。因为它们的n-gram可以和其它词共享。

对于训练词库之外的单词，仍然可以构建它们的词向量 。我们可以叠加它们的字符级n-gram向量。

FastText和CBOW一样，也包含输入层、隐含层、输出层，输入都是多个经向量表示的单词，输出都是一个特定的target，隐含层都是对多个词向量的叠加平均。不同的是， FastText的输入是上下文单词和n-gram的embedding，CBOW只有上下文单词。FastText使用了分层softmax。

FastText除了用来训练词向量，还可以用来做文本分类。

Glove

根据语料库构建一个共现矩阵，矩阵中的每一个元素 【公式开始】X_{ij} 【公式结束】 代表 单词 i 和上下文单词 j 在特定大小的上下文窗口内共同出现的次数 。然后使用神经网络来拟合共现矩阵，目标函数如下：

![原文图片](assets/fe8ed8c2d14c.png)

![原文图片](assets/c8c27b25762e.png)

【公式开始】x_{max} = 100, \alpha = 0.75 【公式结束】 。向量v是要学习的参数，本质上 与 监督学习 的训练方法一样 ，采用了AdaGrad的梯度下降算法，对矩阵X中的所有非零元素进行随机采样，学习曲率（learning rate）设为0.05，在vector size小于300的情况下迭代了50次，其他大小的vectors上迭代了100次，直至收敛。最后我们对于一个词w的target embedding和context embedding，就是它对应的 【公式开始】v_i 【公式结束】 和 【公式开始】v_j 【公式结束】 求和。

Glove对比Word2vec

word2vec是局部语料库训练的， 其特征提取是基于滑窗的；而 glove的滑窗是为了构建共现 matrix ，是基于全局语料的，可见glove需要事先统计共现概率；因此，word2vec可以进行在线学习，glove则需要统计固定语料信息。并且 Glove训练时收敛更快 。

word2vec是无监督学习，同样由于不需要人工标注；glove通常被认为是无监督学习，但实际上glove还是有label的，即共现次数log(Xij)。

word2vec损失函数实质上是带权重的 交叉熵 ，权重固定；glove的损失函数是 最小平方损失函数 ，权重可以做映射变换。

Glove可拓展性好 ，对于很小或很大的corpus都可以有效地训练；另外，对于 限制embedding维度更低的情况，Glove也表现很好。

### 1.7.2 动态编码

静态编码的每个单词都只能学出一个词向量，但在nlp工作中，单词再不同上下文中更可能有不同的意义。这就需要动态编码，也就是 一个单词可以学出多个词向量 。以下方法预训练阶段是无监督的，下游任务一般是有监督的。

Elmo

事先用语言模型学好一个单词的Word Embedding，此时多义词无法区分。在实际使用Word Embedding的时候，单词已经具备了特定的上下文了，这个时候根据上下文单词的语义去调整单词的Word Embedding表示，这样经过调整后的Word Embedding更能表达在这个上下文中的具体含义，自然也就解决了多义词的问题了。

ELMO采用了典型的两阶段过程， 第一个阶段是利用语言模型进行预训练；第二个阶段是在做下游任务时，从预训练网络中提取对应单词的网络各层的Word Embedding作为新特征补充到下游任务中。

![原文图片](assets/31ee6488b8d8.png)

预训练采用 双层双向 LSTM，训练任务是根据上下文预测目标单词。左端的前向双层LSTM代表正方向编码器，输入的是从左到右顺序的除了预测单词外的上文Context-before；右端的逆向双层LSTM代表反方向编码器，输入的是从右到左的逆序的句子下文Context-after；每个编码器的深度都是两层LSTM叠加。采用这样的网络，可以得到三个embedding，分别是 最底层单词的embedding，句法特征的embedding和语义特征的embedding。

第二个阶段，比如下游任务是QA任务，将用户query和回复的三个embedding 加权整合 ，作为补充的新特征给下游任务，然后再进行下游任务的训练。ELMO给下游提供的是每个单词的特征形式，所以这一类预训练的方法被称为“ Feature-based Pre-Training ”。

缺点：LSTM的特征提取能力弱于Transformer；ELMO采取双向拼接这种融合特征的能力可能比Bert一体化的融合特征方式弱。

GPT

![原文图片](assets/9c9d3221dd18.png)

也是采用两阶段训练。区别是采用了transformer，特征提取能力强于LSTM； 并且 预训练是单向训练，即只用上文不用下文 。在微调阶段，GPT的损失函数要考虑语言模型的损失（即decoder利用前k-1个词预测第k个词的最大对数似然估计，对 【公式开始】k \in [1, n] 【公式结束】 求和）以及具体任务的损失。此外，Elmo可以用其他任务的模型，而 GPT要求所有的任务都用自身的框架 ，在此基础上进行微调，对于不同的任务会有不同的处理方法：

![原文图片](assets/5546813201f0.png)

在序列前后增加两个特殊token——”start”和”extract”，分别表示开始和结束；而如果输入是两个序列，那么在它们中间增加一个特殊的token “delim”。比如Entailment，输入是Premise和Hypothesis，输出是3个分类标签中的一个。 如果是相似度计算，因为对称性，我们把它们交换顺序，然后输入两个Transformer。如果是多选题，比如给定一个问题和N个答案，那么我们可以把问题和N个答案分别输入N个Transformer。

Bert

Bert采用与GPT一样的训练方式，区别是采用双向语言模型，用MLM和NSP任务预训练。

MLM ：Mask language model，随机mask掉15%的单词，让语言模型去预测这个单词。为了弥补预训练和下游任务的差距（下游任务没有mask），这些mask的单词有10%的概率替换成随机的一个词，10%的概率替换成它本身，这样就能强迫模型在编码当前时刻的时候不能太依赖于当前的词，而要考虑它的上下文，甚至更加上下文进行”纠错”。

NSP ： Next Sentence Prediction，输入是A和B两个句子，判断B是否是A后面的句子。

Bert模型的输入包含三部分： 词embedding，位置编码embedding和segment （为了将多个句子区分，属于第一个句子的用0，第二个句子用1）

![原文图片](assets/a395f7b0d759.png)

Bert对不同的下游任务也有格式转换方法：

![原文图片](assets/68eded2af682.png)

对比emlo、GPT和bert

模型架构： elmo采用LSTM，GPT和bert采用transformer 。GPT利用transformer的decoder部分，bert利用encoder部分。

单向双向： elmo和bert都是双向语言模型，GPT是单向的，只能看到前边部分 。elmo实际上是两个单向语言模型（方向相反）的拼接，这种融合特征的能力比bert一体化融合特征方式弱。

下游任务： elmo采用feature-based的方式 ，抽取预训练模型的hidden states作为下游任务的额外的特征，与下游任务的embedding结合起来，能适用于所有下游任务。 GPT和bert都是微调方式 ，预训练模型直接作为下游任务的网络架构，下游任务需要做格式转换以适应预训练模型的输入格式。

### 1.7.3 常用编码方法

embedding模型常见架构

在RAG框架中，常见的两种用于doc召回的embedding模型是双编码器（Bi-Encoder）和稀疏嵌入模型（Sparse Embedding Models）。

双编码器（Bi-Encoder）

双编码器的基本思想是使用 两个相同的encoder来分别处理query和doc （或候选doc），然后将它们嵌入到相同的向量空间中。在检索阶段，query和doc会被转化为固定长度的向量表示，然后通过计算 query向量和doc向量之间的相似度 来进行匹配。

工作方式 ：query和doc分别通过两个相同的encoder处理，每个编码器将输入转化为一个embedding。这两个embedding向量在同一个向量空间中表示它们的语义信息，之后根据相似度（例如余弦相似度）来判断查询与文档之间的相关性。

优点 ：这种方法的优势在于它具有较高的计算效率，因为 查询和文档的编码是独立 进行的，适合用于大规模数据集。通常，使用双编码器进行检索时，检索过程会非常快速。

![原文图片](assets/95cb66b63396.jpeg)

稀疏嵌入模型（Sparse Embedding Model）

稀疏嵌入模型则是一种不同于密集嵌入（dense embedding）的模型，通常基于传统的词袋模型（如TF-IDF）或稀疏编码技术。这些模型生成的嵌入是稀疏的，意味着嵌入向量中 大多数元素的值是零 ，仅有少量非零元素。

工作方式 ：在稀疏嵌入模型中，文本的表示通常不是通过密集的向量（如BERT生成的嵌入向量）来表示，而是通过一种稀疏表示，其中很多维度的值为零，只在少数维度上有较高的值。这种稀疏表示通常是通过词频或其他特征的权重计算得到的，常见的实现包括基于词频的向量化方法（如 TF-IDF、bm25 ）和一些稀疏编码方法（如 LDA 等）。

优点 ：稀疏嵌入模型往往计算效率较高，并且可以避免高维密集向量所带来的 计算开销 ，特别是在大型文档库的检索中。此外，稀疏表示有时能捕捉到 更加显著的词汇特征 ，适用于特定的检索任务，如关键词匹配等。

以下介绍两个经典的bi-encoder embedding模型

bge v1

BGE，全称BAAI General Embedding，是智源研究院提出的开源通用向量模型，在过去短短一年时间内，在huggingface上总下载量已超数亿次，是目前下载量最多的国产AI系列模型。

论文：C-Pack: Packed Resources For General Chinese Embeddings

bge训练的3个阶段：

（1） 预训练 ：用Wudao纯文本语料训练，利用了RetroMAE，重建污染的编码向量；

（2） 弱监督学习 ：用C-MTP无标签数据集训练，对比学习从负样本学习中如何区分出成对的文本；

（3） 有监督微调 ：用C-MTP有监督数据集训练，由于标签数据是多任务的，所以加入了指令微调实现多任务下的微调。

BGE v1由6个模型组成，每种语言有'large', 'base'和'small'三款不同规模的模型。用户可根据需求平衡挑选更大能力更强的模型，或更小速度更快的模型。

![原文图片](assets/5d1b6b0c627b.jpeg)

后面又出了v1.5版本，主要缓解了相似度分布问题，并提升无指令情况下的检索能力。

下面分别对训练的每个阶段做详细的分析：

## 一、预训练

预训练阶段用的是2022年EMNLP上提出的RetroMAE。RetroMAE由两个主要部分组成： Encoder和Decoder 。首先，输入文本经过掩码处理后被送入Encoder部分，由bert组成(12层 transformer 的encoder构成。Encoder使用 BERT结构 来处理输入并获取最终的 [CLS] 标记对应的隐层表示，这个表示作为整个句子的向量（绿色小方块）。然后，Decoder接收两个输入： 一是经过掩码的句子，二是从Encoder中提取的 [CLS] 隐层表示 ，作为句子向量。Decoder部分是一个单层的Transformer， 用于根据掩码输入和句子向量进行重建 。

在训练过程中，模型的损失函数由两部分组成：一是 Encoder的MLM （Masked Language Modeling）损失，负责通过掩码预测来学习语言的语法和语义；二是 Decoder的重建损失 ，负责根据掩码的输入和Encoder的句子向量来恢复原始句子。整个模型的优化目标是同时最小化这两种损失。

![原文图片](assets/6552d67f0362.jpeg)

工作流程如下：

![原文图片](assets/d93e60943f11.jpeg)

通过三步构建了一个逐步细化的自监督学习框架：

首先 通过Encoder获取句子的 嵌入表示

然后 通过Decoder利用该句子表示来 重建掩码部分

最后 通过增强编码阶段进一步利用上下文信息和句子嵌入进行 全局恢复 。

为了进一步提升性能，作者对Decoder进行了优化。具体来说，作者认为每个掩码token基于相同的上下文进行重建过于单一，因此引入了 双流自注意力 （two-stream self-attention）和 位置关注掩码 （position-specific attention mask）。简单来说，Q（查询）和KV（键值）分别处理不同的上下文信息， 去掉cross attention，直接将encoder中的sentence的编码融入self-attention中 。在transformer的decoder中，通过cross-attention模块将source sentence的信息融入target sentence中，而在enhanced decoder中，通过改变Q、K和V，而改变信息融合的方式(详情见上图的part (c)部分)：在enchanted decoder中，Q，K，V为：

![原文图片](assets/89a5aca07d54.png)

在enhanced decoder中，除了第一行， 每个token都可以看见第一个元素和随机采样的词 ，对角线位置也是一定会被mask掉的，最后得到每个token的context vector。在计算attention时， 通过mask机制使得每个掩码token能够使用不同部分的上下文 。这样做的目的是增加模型的复杂度，并提升其 泛化能力 。如下图所示：

![原文图片](assets/8b776e754820.jpeg)

Q：为什么编码器和解码器是非对称的？

A： 从论文创新的角度来看，这种设计是经过深思熟虑的。传统上，BERT主要用于 MLM （Masked Language Modeling）和 NSP （Next Sentence Prediction）任务，通过获取 [CLS] 向量或最后一层隐层的输出，能捕捉一定的语义信息，作为语义嵌入用于文本检索等任务。自监督学习除了MLM，还包括对比学习和自编码器等方法，但对比学习的应用较多，并且对负采样有较高要求。现在， RetroMAE的创新点在于将自编码器的思想引入BERT，利用自编码器作为特征表征学习的方式，进而提升模型的性能。

BERT本身作为一个强大的编码器，而通过加一个解码器，采用自编码的方式去牵引原本的BERT模型，使得特征表征能更好地学习和优化，相当于为原有的BERT任务添加了一个新的学习目标——即“ 重建掩码输入 ”。这本质上是一个 多任务学习 的问题，其中一个任务是学习有效的语义嵌入，另一个任务则是通过解码器恢复原始输入，从而强化特征表征的学习。

从掩码率和模型的尺寸上，我们可以看到对解码器的要求非常严格，解码器的设计较为紧凑。通过这种方式，RetroMAE强迫编码器学习更高质量的特征表征，因为解码器的学习任务相对复杂，它要求编码器提供更精准的表示来进行有效的重建。因此，整个模型设计是为了迫使 编码器在学习过程中更加注重语义表征的精度 。

总的来说，RetroMAE将编码器和解码器设计为非对称结构，正是为了通过多任务学习的方式，提升模型的表征学习能力。需要注意的是，最终的embedding（如BGE）主要来自于Encoder的 [CLS] 标记的最后隐层表示。

## 二、弱监督学习

在对比学习中，我们的目标是通过无标签数据集让模型学习区分正负样本的能力。具体来说，给定一个正文本对 p 和 q，以及一个负样本 q′，我们希望通过一个损失函数使得正文本对的相似度高于负样本对的相似度，从而提升模型的区分能力。这个目标的损失函数可以表示为：

【公式开始】\mathcal{L} = - \log \frac{\exp(\text{sim}(e_p, e_q) / \tau)}{\exp(\text{sim}(e_p, e_q) / \tau) + \exp(\text{sim}(e_p, e_{q'}) / \tau)}【公式结束】

其中：

【公式开始】\text{sim}(e_p, e_q) 【公式结束】 表示正样本对 p 和 q 的相似度，通常使用点积或余弦相似度来计算；

【公式开始】\tau【公式结束】 是温度参数，控制平滑程度；

【公式开始】e_p【公式结束】 和 【公式开始】e_q【公式结束】 分别是正样本 p 和 q 的嵌入向量。

从抽象的角度来看，这个损失函数与 softmax 类似，正文本对的相似度占所有文本对相似度之和的比例越大，损失越小。温度参数 【公式开始】\tau【公式结束】 的作用是调节这种比例的平滑程度：当 【公式开始】\tau【公式结束】 越大时，概率分布越平滑，这会降低正样本对之间的区分度，帮助提升模型的泛化能力，减少过拟合。

难负样本采样

在对比学习中，负样本采样的质量对模型性能至关重要。特别是 难负样本 的采样非常重要，因为如果所有负样本都很容易区分，那么模型的损失会很小，梯度也会很小，导致模型收敛慢，且在复杂语义场景下，学习到的表示可能无法有效地区分正样本和难负样本。

然而，在本研究中，作者并未专门设计难负样本采样方法，而是采用了 in-batch负采样 （in-batch negative sampling）。具体来说，假设一个batch中有 m 条文本，作者为每条文本 p配对了一个正样本 q，即相关文本。这样，在一个batch中，除了正样本对 (p, q) 外，其他文本都与 p 无关，因此可以作为负样本 q' 来参与训练。这样一来，负样本集合就是这个batch中所有不与 p 相关的文本。

为了增加难负样本被包含的概率，作者使用了一个较大的batch size，设定为 19200，这样可以增加batch中包含难负样本的可能性。通过这种 in-batch负采样 方式，模型能够在每个batch中同时学习正样本和负样本，且由于batch size较大，能够确保难负样本得到有效利用，从而提升模型的区分能力并加速收敛。

## 三、有监督微调

由于标签数据含有不同有监督任务的数据，所以加入了指令微调实现多任务下的微调。具体做法是在query前加入指令做微调，比如：指令“search relevant passages for the query” + query。此外，除了in-batch负采样，还采用ANN-style采样策略从给定任务的原始语料中挖掘难负样本。具体来说，ANN索引（近似最近邻索引）被用来找到与正样本相似度较高但仍属于负样本的文档，从而进一步增加负样本的难度，帮助模型更好地区分正负样本，提升训练效果。

Conan-Embedding

最近在C_MTEB霸榜的embedding模型，该工作来自腾讯。

论文：Conan-embedding: General Text Embedding with More and Better Negative Samples

![原文图片](assets/3c3014dc3ee9.jpeg)

训练过程主要分为两个阶段： 弱监督预训练 和 有监督微调

![原文图片](assets/eadc7fcb5329.jpeg)

## 一、弱监督预训练

在预训练阶段，收集了7.5亿的文本对，参考了Internlm2.5中描述的标准数据过滤方法，通过以下四步进行过滤：

1、通过文档提取和语言识别进行 格式化处理 ；

2、在基于规则的阶段，文本会经过 规范化和启发式过滤 ；

3、通过 MinHash方法进行去重 ；在安全过滤阶段，执行域名阻止、毒性分类和色情内容分类；

4、在质量过滤阶段，文本会经过 广告分类和流畅度分类 ，以确保输出文本的高质量。

通过过滤，筛选了约 4.5 亿对数据，留存率约60%。

然后使用bge-large-zh-v1.5对数据进行评分，过滤掉得分低于0.4的低质量数据，最终筛选出4亿对数据。

预训练的方法和bge类似，采用 InfoNCE loss ，将in-batch内的其他文本对作为负样本进行训练。

## 二、有监督微调

在这个阶段针对不同的下游任务进行微调，将训练数据分为retrieval（非对称型）和STS（对称型）两种任务类型，其中 retrieval任务使用InfoNCE loss，STS任务使用CoSENT loss 。

这个阶段还使用了两种优化技巧： 动态难负例挖掘训练 、 跨GPU的Batch均衡训练

动态难负例挖掘训练 （Dynamic Hard Negative Mining，Dynamic-HNM）

Embedding模型的训练通常依赖 对比学习 ，其关键在于正负例的选择质量。难负例（Hard Negatives）是与Query有一定相关性但与正例的区分较难的负例，能有效提高模型的对比损失效率。

传统的负例挖掘多在数据预处理阶段完成，这意味着负例是固定的。随着训练的进行，模型的 权重更新 可能导致这些固定负例对模型来说变得不再困难，从而降低训练效率。

为解决上述问题，Dynamic-HNM在训练过程中动态调整负例，主要步骤如下：

基于Teacher模型初始化难负例 ：

使用预训练Teacher模型为Query选择初始负例，这些负例需满足“有一定相关性但区分度低”的条件。

动态更新机制 ：

在每次权重更新后，记录当前负例与Query的相似性得分（例如Cosine相似度）。

每隔一定迭代步数（如100步），根据以下规则检测负例是否需要替换：

若负例与Query的相似性得分的1.15倍小于初始得分，且绝对值低于0.8，则判定该负例“不再困难”。

替换规则：使用最新的模型权重重新挖掘负例。

负例替换方案 ：

每次替换使用区间中的案例（如第 【公式开始】(i-1) \times n+10【公式结束】 到 【公式开始】i \times n+10【公式结束】 个案例），确保负例质量与多样性。其中i表示第次替换，n表示每次使用的难负例数

低成本实现 ：

通过简单的Score更新与筛选逻辑，动态挖掘的成本仅相当于一个训练Step的计算代价。

下图展示了Dynamic-HNM和Standard-HNM的正负例相似性得分随训练步数的变化曲线：

Standard-HNM ：负例得分在早期下降后趋于震荡，表明模型已“学会”这些负例。

Dynamic-HNM ：在负例学习完成后自动替换新负例，使负例得分继续下降。

![原文图片](assets/e5775dfdf82d.jpeg)

跨GPU的Batch均衡训练 （Cross-GPU Batch Balancing, CBB）

这个优化点主要是通过优化任务训练流程和样本利用率，从而提高训练稳定性和模型性能。

将训练数据分为两种任务类型：

Retrieve任务：检索任务， 通过对比学习优化Query和正/负样本的表示关系 。使用InfoNCE loss。

STS任务：语义文本相似性任务， 通过监督学习训练模型 ，使其能够量化句子对之间的语义相似性。使用CoSENT loss。

传统的做法通常是在 顺序随机任务训练 中，每个训练Step只处理一个任务（如iter0处理STS任务，iter1处理Retrieve任务）。这种任务分配方式存在以下问题：

单任务优化方向不一致 ：单次优化方向可能与Embedding模型的全局优化目标偏离，导致梯度震荡和收敛困难。

负样本利用不足 ：Retrieve任务中，负样本数量受单GPU计算能力限制，无法充分挖掘更多难负例。

针对这两个问题CBB策略主要从以下两方面优化：

跨任务均衡

每个训练Step同时引入所有任务的Loss，确保优化方向与全局目标更一致。在单次Forward-Loss-Backward-Update中，计算所有任务的Loss并合并。

例如：Retrieve任务，从多个GPU中收集负样本，计算对比损失；STS任务，在另一个GPU上计算STS任务的Loss。最后将所有Loss汇总，计算全局梯度并更新模型权重。

跨GPU负例共享

多个GPU共享相同的Query和正样本（确保一致性），但每个GPU有不同的负样本。例如：4个GPU分别处理不同的负样本集，并计算对应的对比Loss，汇总后，整合所有负样本信息，提高训练效率和样本利用率。

loss函数如下：

![原文图片](assets/3961335904c4.jpeg)

【公式开始】s(q, y)【公式结束】 ：Query和样本之间的相似性评分函数，通常为余弦相似度。

【公式开始】\tau【公式结束】 ：温度缩放参数，控制对高相似性样本的敏感度。

【公式开始】N【公式结束】 ：Query q和正样本共享的GPU数量。

【公式开始】\beta【公式结束】 ：权重因子，控制两个任务在总Loss中的占比（经验值为0.8）。

下图展示了CBB策略的具体流程，包括：

多个GPU如何分配负样本。

各任务如何在单次Iter中计算Loss并合并。

![原文图片](assets/230ae5c30ae1.jpeg)

如何选择合适的embedding模型

语言支持和性能 ：大部分开源向量模型只支持单一或者有限的文本语言，所以需要确保 Embedding 模型支持的语言种类。多语言模型如 OpenAI Embedding 和 bge-m3 等模型能够处理多种语言。bge-m3 支持 100 多种语言，适合多语言需求的场景。另外，某些模型在主要语言（如中文）中的表现较好，但在处理较少使用的语言时可能会表现不佳。因此，需要评估模型在所有必需语言中的准确性，以确保一致的性能。

处理长文本的能力 ：切分的文本片段后续需要通过 Embedding 模型进行向量化，所以必须考虑向量模型对输入文本块的 tokens 长度限制，超出这个限制则会导致模型对文本进行截断，从而丢失信息，影响下游任务的性能。不同的 Embedding 模型对文本块长度的支持能力不同。比如，BERT 及其变体通常支持最多 512 个tokens，处理长文本时则需要将文本分成更小的块，意味着需要更加精细化的分块策略。而 Jina AI 的 Embedding 模型和 bge-m3 模型则支持 8K 的 tokens 输入，适合处理长文本块。

模型在特定领域的表现 ：通用 Embedding 模型在特定垂直领域（如医学、法律和金融等）可能不如专用模型有效。这些领域通常需要专门训练 Embedding 模型来捕捉特定的专业术语和语境。为特定业务需求优化的 Embedding 模型能够显著提升检索和生成的质量。例如，通过结合向量检索和重排序（reranking）技术，可以进一步优化结果。

存储和内存等资源需求 ：高维向量需要更多的存储空间，这可能会带来长期成本。例如，较高维度的模型如 text-embedding-ada-002 需要更多的存储资源。另外，较大的模型可能会占用更多内存，因此不适合内存有限的设备。

模型响应时间 ： Embedding 模型的处理速度在实时应用中尤为关键。例如，intfloat/e5-base-v2 模型在处理速度上表现优异，但需要在 GPU上 运行以达到最佳性能。在选择模型时，需要评估其在嵌入和检索过程中的延迟。例如，OpenAI 的 Embedding 模型在许多基准测试中显示出较高的性能和较低的延迟。

通用的 Embedding 模型通常是在大规模、多样化的数据集上训练的，可能不完全适合特定领域的任务，比如医学、法律等专业领域，它们无法很好的理解一些专有词汇。如果模型在业务数据集上表现不能满足预期，可以通过微调，让模型学习到特定领域的词汇和概念，使其在特定应用场景中表现更佳。
