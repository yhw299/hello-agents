import re
import random
import sys

# Fix encoding issues on Windows terminals
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 定义规则库:模式(正则表达式) -> 响应模板列表
rules = {
    r'I need (.*)': [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?"
    ],
    r'Why don\'t you (.*)\?': [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?"
    ],
    r'Why can\'t I (.*)\?': [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?"
    ],
    r'I am (.*)': [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?"
    ],
    r'.* mother .*': [
        "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?"
    ],
    r'.* father .*': [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?"
    ],
    r'.*': [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?"
    ]
}

# 基于上下文的回复模板
context_responses = [
    "Earlier you talked about {0}. Can you tell me more about that?",
    "How does what you just said relate to {0}?",
    "Before we move on, let's go back to {0} for a moment.",
]

# 上下文记忆：保存最近的对话历史
context = {
    "last_input": "",
    "last_response": "",
    "history": []  # 保存 (user_input, response) 对，最多 5 轮
}

MAX_HISTORY = 5

# 定义代词转换规则
pronoun_swap = {
    "i": "you", "you": "i", "me": "you", "my": "your",
    "am": "are", "are": "am", "was": "were", "i'd": "you would",
    "i've": "you have", "i'll": "you will", "yours": "mine",
    "mine": "yours"
}


def swap_pronouns(phrase):
    """
    对输入短语中的代词进行第一/第二人称转换
    """
    words = phrase.lower().split()
    swapped_words = [pronoun_swap.get(word, word) for word in words]
    return " ".join(swapped_words)


def respond(user_input):
    """
    根据规则库和上下文生成响应
    """
    # 先尝试匹配具体规则
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            captured_group = match.group(1) if match.groups() else ''
            swapped_group = swap_pronouns(captured_group)
            response = random.choice(responses).format(swapped_group)
            # 更新上下文
            context["last_input"] = user_input
            context["last_response"] = response
            context["history"].append((user_input, response))
            if len(context["history"]) > MAX_HISTORY:
                context["history"].pop(0)
            return response

    # 默认回复：偶尔引用之前聊过的话题
    context["last_input"] = user_input
    if context["history"] and random.random() < 0.4:
        old_topic = random.choice(context["history"])[0]
        response = random.choice(context_responses).format(old_topic)
    else:
        response = random.choice(rules[r'.*'])

    context["last_response"] = response
    context["history"].append((user_input, response))
    if len(context["history"]) > MAX_HISTORY:
        context["history"].pop(0)
    return response


# 主聊天循环
if __name__ == '__main__':
    print("Therapist: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Therapist: Goodbye. It was nice talking to you.")
            break
        response = respond(user_input)
        print(f"Therapist: {response}")
