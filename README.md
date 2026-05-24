weather-test.py

能处理分步任务的智能旅行助手

chatbot.py

构建基于规则的聊天机器人
不正面回答问题或提供信息，
而是通过识别用户输入中的关键词，
然后应用一套预设的转换规则，将用户的陈述转化为一个开放式的提问
增加了一个上下文记忆
  1. 上下文存储（第 58-65 行）
  用一个 context 字典保存最近 5 轮的 (输入, 回复) 对话历史。
  2. 上下文感知的回复模板（第 51-56 行）
  当没有匹配到具体规则时，机器人有 40% 的概率从历史里随机挑一句用户之前说过的话，套用模板追问，比如 "Earlier you talked
  about {0}. Can you tell me more about that?"
  3. respond() 函数更新
每次生成回复后自动把当前对话追加到 context["history"] 中，超出 5 轮就丢掉最早的。
这样就实现了对话不会完全像失忆一样，偶尔会回头追问之前聊过的话题。

Transformer.py

各模块作用
  1. PositionalEncoding（第10-36行）
  作用：给词嵌入向量注入位置信息。因为 Self-Attention
  本身不关心词的顺序，所以需要用 sin/cos 函数生成位置编码，直接加到输入向量上。    
     - 偶数维度用 sin，奇数维度用 cos
     - 注册为 buffer（非参数张量），随模型一起移动到 GPU
  2. MultiHeadAttention（第38-95行）
  作用：Transformer 的核心——多头自注意力机制。让每个词都能"看到"序列中所有其他词， 
  计算它们之间的关联权重。
    关键步骤：
    1. W_q/W_k/W_v 线性层：将输入投影到 Q（查询）、K（键）、V（值）空间
    2. split_heads：将 d_model 维拆成 num_heads 个头，每个头独立计算注意力
    3. scaled_dot_product_attention：计算 softmax(QK^T / √d_k) × V，得出加权表示     
    4. combine_heads：把所有头拼回 d_model 维
    5. W_o：最终线性变换输出
  其中 mask 用于屏蔽某些位置（如 padding 或解码时屏蔽未来词）。
  3. PositionWiseFeedForward（第97-115行）
  作用：位置前馈网络。对每个位置独立地做两次线性变换 + ReLU 激活。
     - 结构：Linear(d_model → d_ff) → ReLU → Dropout → Linear(d_ff → d_model)
     - 作用是增加模型的非线性和表达能力
  4. EncoderLayer（第119-136行）
  作用：编码器的单层，使用 残差连接 + LayerNorm 将两个子层串起来：
  x → Self-Attention → Dropout → 残差相加 → LayerNorm
    → FeedForward   → Dropout → 残差相加 → LayerNorm
     - norm1：注意力子层后的 LayerNorm
     - norm2：前馈网络子层后的 LayerNorm
  5. DecoderLayer（第139-163行）
  作用：解码器的单层，比编码器多一个交叉注意力子层：
  x → Masked Self-Attention → Dropout → 残差相加 → LayerNorm       (norm1)
    → Cross-Attention(Q=x, K/V=encoder_output) → 残差相加 → LayerNorm  (norm2)     
    → FeedForward → 残差相加 → LayerNorm                             (norm3)       
  - Masked Self-Attention：用 tgt_mask 防止当前位置"偷看"未来的词

BPE.py
这是 BPE 子词分词算法的核心演示，用于将单词拆分为更小的子词单元。
原始词表 → 统计相邻符号对频率 → 合并最高频词对 → 更新词表 → 重复 N 次
  get_stats(vocab)（第3-10行）
  统计当前词表中所有相邻符号对的出现频率。符号之间用空格分隔，遍历每个词中相邻的两 
  个符号，累加它们的频率。

  merge_vocab(pair, v_in)（第12-20行）
  将指定的符号对合并为一个整体。用正则匹配词中独立的 a
  b（两边是空格或边界），替换为 ab。
  
