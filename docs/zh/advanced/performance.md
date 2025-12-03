# 性能优化

## 目录

- [概述](#概述)
- [目标读者](#目标读者)
- [前置条件](#前置条件)
- [性能优化的维度](#性能优化的维度)
- [提示优化最佳实践](#提示优化最佳实践)
- [响应速度优化](#响应速度优化)
- [输出质量优化](#输出质量优化)
- [成本优化](#成本优化)
- [性能测试方法](#性能测试方法)
- [基准测试](#基准测试)
- [实际案例分析](#实际案例分析)
- [相关资源](#相关资源)
- [下一步](#下一步)

---

## 概述

本文档提供全面的性能优化指南，帮助您提高 Claude 的响应速度、输出质量和成本效益。性能优化不仅仅是技术问题，更是在多个目标之间找到最佳平衡点的艺术。

性能优化的三个核心维度：
- **速度**：减少响应时间
- **质量**：提高输出准确性和相关性
- **成本**：降低 API 调用费用

---

## 目标读者

本文档适合以下人群：

- **应用开发者**：需要优化生产环境中的 AI 性能
- **产品经理**：需要平衡性能、质量和成本
- **系统架构师**：设计高效的 AI 集成方案
- **高级用户**：追求最佳的提示工程实践

---

## 前置条件

在阅读本文档前，您应该：

- 完成教程的核心章节（第 1-9 章）
- 有实际的提示工程经验
- 了解基本的性能指标概念
- 熟悉您的应用场景和需求

---

## 性能优化的维度

### 1. 响应时间（Latency）

**定义**：从发送请求到收到完整响应的时间。

**影响因素**：
- 提示长度
- 输出长度（max_tokens）
- 模型选择
- 网络延迟
- 服务器负载

**优化目标**：
- 交互式应用：< 2 秒
- 批处理任务：可接受更长时间
- 实时应用：< 500ms

### 2. 输出质量（Quality）

**定义**：输出满足需求的程度。

**衡量指标**：
- 准确性：事实正确性
- 相关性：与任务的相关程度
- 完整性：是否包含所有必要信息
- 一致性：多次调用的稳定性
- 可用性：输出格式是否易于使用

**优化目标**：
根据应用场景设定具体标准。

### 3. 成本效益（Cost）

**定义**：完成任务所需的 API 费用。

**计费因素**：
- 输入 tokens 数量
- 输出 tokens 数量
- 模型选择（Haiku < Sonnet < Opus）
- 调用频率

**优化目标**：
在满足质量要求的前提下最小化成本。

### 4. 性能权衡三角

```
        质量
         /\
        /  \
       /    \
      /      \
     /________\
  速度        成本
```

**关键洞察**：
- 提高质量通常需要更长的提示或更强大的模型（增加成本和时间）
- 提高速度可能需要简化提示（可能降低质量）
- 降低成本可能需要使用更小的模型（可能影响质量）

**优化策略**：
根据应用场景确定优先级，找到最佳平衡点。

---

## 提示优化最佳实践

### 1. 提示长度优化

**原则**：提供足够的信息，但避免冗余。

**优化技巧**：

**技巧 1：移除冗余信息**
```python
# ❌ 冗余
PROMPT = """
请帮我分析这个文本。我需要你仔细阅读，然后告诉我主要观点。
请确保你的分析是准确的。谢谢你的帮助。

<text>
[文本内容]
</text>

再次强调，请给我一个详细的分析。
"""

# ✅ 简洁
PROMPT = """
分析以下文本，提取主要观点：

<text>
[文本内容]
</text>
"""
```

**技巧 2：使用引用而非重复**
```python
# ❌ 重复
PROMPT = """
<document>
[很长的文档]
</document>

请总结上面的文档。
然后基于上面的文档回答：文档的主要论点是什么？
最后，根据上面的文档，列出关键证据。
"""

# ✅ 引用
PROMPT = """
<document>
[很长的文档]
</document>

基于上述文档：
1. 总结主要内容
2. 提取主要论点
3. 列出关键证据
"""
```

**技巧 3：精简示例**
```python
# ❌ 过多示例
PROMPT = """
[10 个相似的示例]

现在处理：[实际任务]
"""

# ✅ 精选示例
PROMPT = """
[3 个代表性示例，涵盖不同情况]

现在处理：[实际任务]
"""
```

### 2. 指令清晰度优化

**原则**：清晰的指令减少迭代和错误。

**优化技巧**：

**技巧 1：使用具体动词**
```python
# ❌ 模糊
PROMPT = "处理这个数据"

# ✅ 具体
PROMPT = "计算这个数据集的平均值、中位数和标准差"
```

**技巧 2：明确输出格式**
```python
# ❌ 不明确
PROMPT = "给我一些建议"

# ✅ 明确
PROMPT = """
提供 3 条建议，每条包含：
- 建议标题
- 详细说明（2-3 句话）
- 预期效果

格式：编号列表
"""
```

**技巧 3：预填充引导**
```python
# 使用预填充跳过不必要的前言
messages = [
    {"role": "user", "content": "列出三种编程语言"},
    {"role": "assistant", "content": "1."}  # 预填充
]
# Claude 直接输出列表，节省 tokens
```

### 3. 上下文管理优化

**原则**：只提供必要的上下文。

**优化技巧**：

**技巧 1：分段处理长文档**
```python
# ❌ 一次处理全部
PROMPT = f"""
<document>
[100 页的文档]
</document>

总结这个文档
"""

# ✅ 分段处理
for section in document_sections:
    summary = get_completion(f"""
    <section>
    {section}
    </section>
    
    总结这一部分的要点（2-3 句话）
    """)
    summaries.append(summary)

# 最后合并总结
final_summary = get_completion(f"""
以下是各部分的总结：
{summaries}

综合这些总结，提供整体概述
""")
```

**技巧 2：使用摘要而非全文**
```python
# 对于多轮对话，保存摘要而非完整历史
conversation_summary = "用户询问了产品价格，我们提供了报价..."
current_prompt = f"""
<conversation_context>
{conversation_summary}
</conversation_context>

<current_question>
{new_question}
</current_question>

基于对话上下文回答当前问题
"""
```


### 4. 模型选择优化

**原则**：为任务选择合适的模型。

**模型对比**：

| 模型 | 速度 | 成本 | 能力 | 适用场景 |
|------|------|------|------|----------|
| Claude 3 Haiku | 最快 | 最低 | 良好 | 简单任务、高频调用 |
| Claude 3 Sonnet | 中等 | 中等 | 优秀 | 平衡性能和成本 |
| Claude 3 Opus | 较慢 | 最高 | 最强 | 复杂任务、高质量要求 |

**选择策略**：

**策略 1：任务分层**
```python
# 简单任务用 Haiku
def classify_sentiment(text):
    return call_claude_haiku(f"这段文本的情感是正面还是负面？{text}")

# 复杂任务用 Opus
def analyze_legal_document(doc):
    return call_claude_opus(f"深入分析这份法律文件：{doc}")
```

**策略 2：级联调用**
```python
# 先用 Haiku 快速筛选
candidates = []
for item in large_dataset:
    if call_claude_haiku(f"这个项目是否相关？{item}") == "是":
        candidates.append(item)

# 再用 Opus 深入分析筛选后的项目
for candidate in candidates:
    detailed_analysis = call_claude_opus(f"详细分析：{candidate}")
```

**策略 3：动态选择**
```python
def smart_call(prompt, complexity):
    if complexity == "simple":
        return call_claude_haiku(prompt)
    elif complexity == "medium":
        return call_claude_sonnet(prompt)
    else:
        return call_claude_opus(prompt)
```

---

## 响应速度优化

### 1. 减少输入长度

**技巧 1：提取关键信息**
```python
# ❌ 发送整个网页
PROMPT = f"总结这个网页：{entire_html}"

# ✅ 提取文本内容
text_content = extract_text_from_html(html)
PROMPT = f"总结以下内容：{text_content}"
```

**技巧 2：使用摘要**
```python
# 对于长文档，先生成摘要
summary = generate_summary(long_document)
# 后续任务基于摘要
result = process_with_summary(summary)
```

### 2. 控制输出长度

**技巧 1：设置合理的 max_tokens**
```python
# ❌ 过大的 max_tokens
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=4096,  # 可能生成很长的响应
    messages=[{"role": "user", "content": "用一句话回答：什么是AI？"}]
)

# ✅ 根据需求设置
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,  # 足够一句话
    messages=[{"role": "user", "content": "用一句话回答：什么是AI？"}]
)
```

**技巧 2：在提示中限制长度**
```python
PROMPT = "用不超过 50 字总结这篇文章：[文章]"
```

### 3. 并行处理

**技巧 1：批量并行调用**
```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=API_KEY)

async def process_item(item):
    message = await client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        messages=[{"role": "user", "content": f"处理：{item}"}]
    )
    return message.content[0].text

async def process_batch(items):
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)

# 并行处理多个项目
results = asyncio.run(process_batch(items))
```

**技巧 2：流式输出**
```python
# 使用流式 API 获得更快的首字节时间
with client.messages.stream(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### 4. 缓存策略

**技巧 1：缓存常见查询**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_response(prompt):
    return call_claude(prompt)

# 相同的提示会返回缓存结果
result1 = get_cached_response("什么是机器学习？")
result2 = get_cached_response("什么是机器学习？")  # 从缓存返回
```

**技巧 2：预计算常见任务**
```python
# 预先生成常见问题的答案
FAQ_CACHE = {
    "产品价格": "我们的产品价格从 $99 起...",
    "配送时间": "标准配送需要 3-5 个工作日...",
    # ...
}

def answer_question(question):
    # 先检查缓存
    if question in FAQ_CACHE:
        return FAQ_CACHE[question]
    # 否则调用 Claude
    return call_claude(question)
```

---

## 输出质量优化

### 1. 提高准确性

**技巧 1：提供充分上下文**
```python
# ❌ 缺少上下文
PROMPT = "这个决策对吗？"

# ✅ 提供完整上下文
PROMPT = """
<situation>
公司正在考虑进入新市场。
当前资源：100 万预算，10 人团队
市场规模：预计 500 万潜在客户
竞争：3 个主要竞争对手
</situation>

<decision>
立即进入市场，投入全部预算
</decision>

评估这个决策的合理性，考虑风险和机会。
"""
```

**技巧 2：使用思维链**
```python
PROMPT = """
计算：(15 + 23) * 4 - 18 / 3

请逐步计算：
1. 先计算括号内
2. 再计算乘除
3. 最后计算加减
4. 给出最终答案
"""
```

**技巧 3：要求引用来源**
```python
PROMPT = """
<document>
[文档内容]
</document>

回答问题：文档中提到的主要风险是什么？

要求：
- 直接引用文档中的相关句子
- 使用引号标注引用
- 如果文档中没有相关信息，明确说明
"""
```

### 2. 提高一致性

**技巧 1：使用系统提示**
```python
SYSTEM_PROMPT = """
你是一个客户服务助手。在所有回复中：
- 使用礼貌、专业的语气
- 提供具体的解决方案
- 如果不确定，建议联系人工客服
- 始终以"感谢您的咨询"结尾
"""

# 所有调用使用相同的系统提示
response = call_claude(user_question, system=SYSTEM_PROMPT)
```

**技巧 2：使用模板**
```python
RESPONSE_TEMPLATE = """
基于提供的信息：

分析：
[分析内容]

建议：
[具体建议]

风险：
[潜在风险]

下一步：
[行动步骤]
"""

PROMPT = f"""
分析以下情况：
{situation}

请按照以下格式输出：
{RESPONSE_TEMPLATE}
"""
```

**技巧 3：设置 temperature = 0**
```python
# 对于需要一致性的任务
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    temperature=0.0,  # 最大化一致性
    messages=[{"role": "user", "content": prompt}]
)
```

### 3. 提高相关性

**技巧 1：明确任务范围**
```python
# ❌ 范围不明确
PROMPT = "告诉我关于 Python 的信息"

# ✅ 明确范围
PROMPT = """
针对初学者，解释 Python 的以下方面：
1. 什么是 Python
2. 为什么学习 Python
3. 如何开始学习
4. 推荐的学习资源

每个方面用 2-3 句话说明。
"""
```

**技巧 2：使用约束**
```python
PROMPT = """
推荐 5 本编程书籍。

约束：
- 只推荐 2020 年后出版的书
- 适合中级程序员
- 涵盖不同编程语言
- 每本书包含：书名、作者、简短推荐理由
"""
```

---

## 成本优化

### 1. Token 使用优化

**理解计费**：
- 输入 tokens：提示中的所有文本
- 输出 tokens：Claude 生成的文本
- 不同模型有不同的价格

**优化策略**：

**策略 1：减少不必要的 tokens**
```python
# ❌ 浪费 tokens
PROMPT = """
你好！我希望你能帮我一个忙。我有一个问题想要问你。
这个问题是关于编程的。具体来说，是关于 Python 的。
我想知道如何在 Python 中读取文件。你能告诉我吗？
谢谢你的帮助！我真的很感激！
"""

# ✅ 简洁高效
PROMPT = "如何在 Python 中读取文件？"
```

**策略 2：重用结果**
```python
# 一次生成，多次使用
summary = call_claude("总结这篇文章：[文章]")

# 基于总结进行多个任务
task1 = call_claude(f"基于这个总结，提取关键词：{summary}")
task2 = call_claude(f"基于这个总结，生成标题：{summary}")
# 比每次都发送完整文章更经济
```

### 2. 模型选择优化

**成本对比**（相对价格）：
- Haiku：1x（基准）
- Sonnet：3x
- Opus：15x

**优化策略**：

**策略 1：任务分类**
```python
def choose_model(task_complexity):
    if task_complexity == "simple":
        return "claude-3-haiku-20240307"  # 最经济
    elif task_complexity == "medium":
        return "claude-3-sonnet-20240229"
    else:
        return "claude-3-opus-20240229"  # 最强大但最贵
```

**策略 2：先筛选后分析**
```python
# 用 Haiku 快速筛选（便宜）
relevant_items = []
for item in all_items:
    if is_relevant_haiku(item):  # 使用 Haiku
        relevant_items.append(item)

# 用 Opus 深入分析筛选后的项目（贵但必要）
for item in relevant_items:
    detailed_analysis = analyze_with_opus(item)
```

### 3. 批处理优化

**策略 1：合并请求**
```python
# ❌ 多次调用
for item in items:
    result = call_claude(f"处理：{item}")

# ✅ 批量处理
batch_prompt = "处理以下项目，每个项目单独输出：\n"
for i, item in enumerate(items):
    batch_prompt += f"{i+1}. {item}\n"

results = call_claude(batch_prompt)
```

**策略 2：增量处理**
```python
# 对于大型任务，增量处理而非重新开始
processed_so_far = []
for chunk in data_chunks:
    result = call_claude(f"""
    已处理：{processed_so_far}
    新数据：{chunk}
    继续处理新数据
    """)
    processed_so_far.append(result)
```


---

## 性能测试方法

### 1. 建立基准

**步骤 1：定义测试用例**
```python
test_cases = [
    {
        "name": "简单分类",
        "prompt": "这段文本的情感是正面还是负面？{text}",
        "expected_quality": "高",
        "max_latency": 1.0  # 秒
    },
    {
        "name": "复杂分析",
        "prompt": "深入分析这份报告：{report}",
        "expected_quality": "非常高",
        "max_latency": 5.0
    }
]
```

**步骤 2：测量性能指标**
```python
import time

def measure_performance(prompt, model):
    start_time = time.time()
    
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    end_time = time.time()
    
    return {
        "latency": end_time - start_time,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "response": response.content[0].text
    }
```

**步骤 3：记录结果**
```python
results = []
for test_case in test_cases:
    result = measure_performance(test_case["prompt"], "claude-3-haiku-20240307")
    results.append({
        "test": test_case["name"],
        "latency": result["latency"],
        "tokens": result["input_tokens"] + result["output_tokens"],
        "meets_requirements": result["latency"] <= test_case["max_latency"]
    })
```

### 2. A/B 测试

**比较不同提示版本**：
```python
def ab_test(prompt_a, prompt_b, test_data, n_runs=10):
    results_a = []
    results_b = []
    
    for _ in range(n_runs):
        for data in test_data:
            # 测试版本 A
            result_a = measure_performance(prompt_a.format(**data), model)
            results_a.append(result_a)
            
            # 测试版本 B
            result_b = measure_performance(prompt_b.format(**data), model)
            results_b.append(result_b)
    
    # 比较平均性能
    avg_latency_a = sum(r["latency"] for r in results_a) / len(results_a)
    avg_latency_b = sum(r["latency"] for r in results_b) / len(results_b)
    
    print(f"版本 A 平均延迟: {avg_latency_a:.2f}s")
    print(f"版本 B 平均延迟: {avg_latency_b:.2f}s")
    
    return results_a, results_b
```

### 3. 质量评估

**自动化质量检查**：
```python
def evaluate_quality(response, expected_format, expected_content):
    checks = {
        "format_correct": check_format(response, expected_format),
        "content_complete": check_completeness(response, expected_content),
        "factually_accurate": check_accuracy(response),
        "relevant": check_relevance(response)
    }
    
    quality_score = sum(checks.values()) / len(checks)
    return quality_score, checks

def check_format(response, expected_format):
    """检查输出格式是否符合预期"""
    if expected_format == "json":
        try:
            json.loads(response)
            return True
        except:
            return False
    # 其他格式检查...
    return True
```

### 4. 负载测试

**测试高并发场景**：
```python
import concurrent.futures

def load_test(prompt, n_concurrent=10, n_requests=100):
    def make_request():
        return measure_performance(prompt, model)
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_concurrent) as executor:
        futures = [executor.submit(make_request) for _ in range(n_requests)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_latency = sum(r["latency"] for r in results) / len(results)
    throughput = n_requests / total_time
    
    print(f"总时间: {total_time:.2f}s")
    print(f"平均延迟: {avg_latency:.2f}s")
    print(f"吞吐量: {throughput:.2f} 请求/秒")
    
    return results
```

---

## 基准测试

### 1. 不同模型的性能对比

**测试设置**：
- 任务：情感分析
- 输入：100 条产品评论
- 评估指标：准确性、速度、成本

**结果示例**：

| 模型 | 准确率 | 平均延迟 | 总成本 | 综合评分 |
|------|--------|----------|--------|----------|
| Haiku | 92% | 0.8s | $0.50 | ⭐⭐⭐⭐ |
| Sonnet | 96% | 1.5s | $1.50 | ⭐⭐⭐⭐⭐ |
| Opus | 98% | 2.5s | $7.50 | ⭐⭐⭐⭐ |

**结论**：
- Haiku：最适合高频、简单任务
- Sonnet：最佳性价比
- Opus：需要最高准确性时使用

### 2. 提示优化前后对比

**优化前**：
```python
PROMPT_V1 = """
请帮我分析一下这个客户反馈。我需要知道客户是否满意，
以及他们提到了哪些具体的问题。请给我一个详细的分析报告。
谢谢！

客户反馈：{feedback}
"""
```

**优化后**：
```python
PROMPT_V2 = """
分析客户反馈，提供：
1. 满意度（满意/不满意）
2. 提到的具体问题（列表）

<feedback>
{feedback}
</feedback>
"""
```

**性能对比**：

| 指标 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| 平均延迟 | 2.1s | 1.3s | ⬇️ 38% |
| 输入 tokens | 85 | 45 | ⬇️ 47% |
| 输出 tokens | 150 | 80 | ⬇️ 47% |
| 成本 | $0.015 | $0.007 | ⬇️ 53% |
| 格式一致性 | 75% | 98% | ⬆️ 31% |

### 3. 批处理 vs 单独处理

**场景**：处理 100 个项目

**方法 1：单独处理**
```python
for item in items:
    result = call_claude(f"处理：{item}")
# 总时间：100 * 1.5s = 150s
# 总成本：100 * $0.01 = $1.00
```

**方法 2：批处理**
```python
batch_prompt = "处理以下项目：\n" + "\n".join(f"{i}. {item}" for i, item in enumerate(items))
result = call_claude(batch_prompt)
# 总时间：8s
# 总成本：$0.15
```

**对比**：
- 速度提升：18.75x
- 成本降低：85%
- 权衡：批处理可能降低单个项目的处理质量

---

## 实际案例分析

### 案例 1：客户服务聊天机器人

**场景**：
- 每天 10,000 次对话
- 平均每次对话 5 轮
- 需要快速响应（< 2 秒）

**初始方案**：
- 模型：Claude 3 Opus
- 每次都发送完整对话历史
- 月成本：约 $15,000

**优化方案**：
1. **模型分层**：
   - 简单问题（FAQ）：Haiku
   - 复杂问题：Sonnet
   - 仅在必要时升级到 Opus

2. **上下文管理**：
   - 保存对话摘要而非完整历史
   - 只发送最近 3 轮对话

3. **缓存常见问题**：
   - 预生成 FAQ 答案
   - 使用语义搜索匹配

**优化结果**：
- 平均响应时间：从 2.5s 降至 1.2s
- 月成本：从 $15,000 降至 $3,500（节省 77%）
- 用户满意度：从 85% 提升至 92%

### 案例 2：文档分析系统

**场景**：
- 分析法律合同（平均 50 页）
- 提取关键条款和风险
- 需要高准确性

**初始方案**：
- 一次性发送整个文档
- 经常超出 token 限制
- 处理时间：5-10 分钟

**优化方案**：
1. **分段处理**：
   ```python
   # 步骤 1：分段总结
   summaries = []
   for section in document.sections:
       summary = call_haiku(f"总结这一部分：{section}")
       summaries.append(summary)
   
   # 步骤 2：综合分析
   analysis = call_opus(f"基于这些总结，分析风险：{summaries}")
   ```

2. **两阶段分析**：
   - 第一阶段（Haiku）：快速扫描，识别重要部分
   - 第二阶段（Opus）：深入分析重要部分

**优化结果**：
- 处理时间：从 7 分钟降至 2 分钟
- 成本：从 $2.50/文档降至 $0.80/文档
- 准确性：保持在 95% 以上

### 案例 3：内容审核系统

**场景**：
- 每小时审核 50,000 条用户评论
- 需要实时处理
- 预算有限

**初始方案**：
- 模型：Claude 3 Sonnet
- 每条评论单独调用
- 无法满足实时要求

**优化方案**：
1. **规则预筛选**：
   ```python
   # 使用简单规则过滤明显安全的内容
   if simple_rule_check(comment):
       return "approved"
   # 只有可疑内容才调用 Claude
   return call_claude_haiku(f"审核：{comment}")
   ```

2. **批处理**：
   - 每 10 秒收集一批评论
   - 批量发送给 Claude

3. **缓存相似内容**：
   - 使用向量相似度检测重复内容
   - 相似内容使用缓存结果

**优化结果**：
- API 调用减少 80%
- 成本从 $5,000/月降至 $800/月
- 处理延迟从 3 秒降至 0.5 秒
- 准确性保持在 98%

---

## 相关资源

### 官方文档
- [Anthropic API 定价](https://www.anthropic.com/pricing)
- [性能最佳实践](https://docs.anthropic.com/claude/docs/best-practices)
- [API 参考文档](https://docs.anthropic.com/claude/reference/)

### 性能监控工具
- **Anthropic Console**：查看 API 使用情况和成本
- **Langfuse**：LLM 应用性能监控
- **Helicone**：API 调用追踪和分析
- **Weights & Biases**：实验追踪和对比

### 相关文档
- [设计原理](design-principles.md)：理解优化背后的原理
- [问题排查](troubleshooting.md)：解决性能问题
- [API 参考](../user-guide/api-reference.md)：API 使用详情

### 社区资源
- [Anthropic Discord](https://discord.gg/anthropic)：与其他开发者交流
- [GitHub Cookbook](https://github.com/anthropics/anthropic-cookbook)：实用示例
- [性能优化案例集](https://community.anthropic.com/performance)

---

## 下一步

掌握性能优化后，您可以：

1. **实施优化**：
   - 在您的应用中应用本文档的技巧
   - 建立性能监控系统
   - 定期评估和优化

2. **深入学习**：
   - [问题排查](troubleshooting.md)：解决常见性能问题
   - [设计原理](design-principles.md)：理解深层原理
   - [常见问题](faq.md)：查找具体问题的答案

3. **持续改进**：
   - 建立性能基准
   - A/B 测试新方法
   - 记录和分享最佳实践

4. **扩展应用**：
   - 探索高级功能（工具使用、提示链）
   - 集成到生产系统
   - 优化用户体验

5. **参与社区**：
   - 分享您的优化经验
   - 学习他人的最佳实践
   - 贡献开源项目

---

**上一步**：[设计原理](design-principles.md)  
**下一步**：[问题排查](troubleshooting.md)

**相关文档**：
- [完整使用手册](../user-guide/user-guide.md)
- [API 参考](../user-guide/api-reference.md)
- [常见问题](faq.md)

