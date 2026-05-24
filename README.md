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

  效果演示：

  You: I feel sad
  Therapist: How long have you been sad?

  You: not sure, maybe a week
  Therapist: Earlier you talked about I feel sad. Can you tell me more about that?

  这样就实现了对话不会完全像失忆一样，偶尔会回头追问之前聊过的话题。