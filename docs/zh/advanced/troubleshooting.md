# 问题排查

## 目录

- [概述](#概述)
- [目标读者](#目标读者)
- [问题诊断流程](#问题诊断流程)
- [常见问题分类](#常见问题分类)
- [API 和连接问题](#api-和连接问题)
- [提示和输出问题](#提示和输出问题)
- [性能问题](#性能问题)
- [质量问题](#质量问题)
- [成本问题](#成本问题)
- [调试技巧和工具](#调试技巧和工具)
- [获取帮助](#获取帮助)
- [相关资源](#相关资源)

---

## 概述

本文档提供系统化的问题排查指南，帮助您快速识别和解决使用 Claude 时遇到的各种问题。无论是 API 错误、输出质量问题还是性能瓶颈，您都能在这里找到解决方案。

---

## 目标读者

本文档适合以下人群：

- **开发者**：遇到技术问题需要快速解决
- **系统管理员**：维护生产环境中的 AI 应用
- **测试人员**：验证和调试 AI 功能
- **所有用户**：遇到任何使用问题

---

## 问题诊断流程

### 系统化诊断方法

```
1. 识别问题
   ↓
2. 收集信息
   ↓
3. 隔离变量
   ↓
4. 测试假设
   ↓
5. 实施解决方案
   ↓
6. 验证修复
   ↓
7. 记录经验
```

### 问题识别清单

在开始排查前，明确以下问题：

- [ ] 问题是什么？（具体症状）
- [ ] 何时开始出现？（时间点）
- [ ] 是否能稳定复现？（频率）
- [ ] 影响范围？（所有请求还是特定情况）
- [ ] 最近有什么变化？（代码、配置、数据）
- [ ] 错误信息是什么？（完整的错误日志）

### 信息收集

**必要信息**：
```python
# 记录请求详情
debug_info = {
    "timestamp": datetime.now(),
    "model": "claude-3-haiku-20240307",
    "prompt_length": len(prompt),
    "max_tokens": 1024,
    "temperature": 0.0,
    "error_message": str(error),
    "request_id": response.headers.get("request-id")
}
```

---

## 常见问题分类

### 问题类型概览

| 类型 | 常见症状 | 紧急程度 |
|------|----------|----------|
| API 错误 | 请求失败、超时 | 🔴 高 |
| 输出质量 | 结果不准确、格式错误 | 🟡 中 |
| 性能问题 | 响应慢、超时 | 🟡 中 |
| 成本问题 | 费用超预期 | 🟢 低 |
| 配置问题 | 认证失败、权限错误 | 🔴 高 |

---

## API 和连接问题

### 问题 1：认证失败

**症状**：
```
anthropic.AuthenticationError: Invalid API key
```

**原因**：
- API 密钥错误或过期
- API 密钥格式不正确
- 环境变量未正确设置

**解决方案**：

**步骤 1：验证 API 密钥**
```python
# 检查 API 密钥格式
API_KEY = "sk-ant-..."  # 应该以 sk-ant- 开头

# 测试 API 密钥
import anthropic

try:
    client = anthropic.Anthropic(api_key=API_KEY)
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )
    print("✅ API 密钥有效")
except anthropic.AuthenticationError:
    print("❌ API 密钥无效")
```

**步骤 2：检查环境变量**
```bash
# 查看环境变量
echo $ANTHROPIC_API_KEY

# 设置环境变量
export ANTHROPIC_API_KEY="your_api_key_here"
```

**步骤 3：重新生成密钥**
- 访问 [Anthropic Console](https://console.anthropic.com/)
- 生成新的 API 密钥
- 更新应用配置

### 问题 2：请求超时

**症状**：
```
requests.exceptions.Timeout: Request timed out
```

**原因**：
- 网络连接不稳定
- 提示过长导致处理时间长
- 服务器负载高

**解决方案**：

**方案 1：增加超时时间**
```python
client = anthropic.Anthropic(
    api_key=API_KEY,
    timeout=60.0  # 增加到 60 秒
)
```

**方案 2：使用重试机制**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_claude_with_retry(prompt):
    return client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
```

**方案 3：优化提示长度**
```python
# 如果提示过长，考虑分段处理
if len(prompt) > 10000:
    # 分段或总结
    prompt = summarize_prompt(prompt)
```

### 问题 3：速率限制

**症状**：
```
anthropic.RateLimitError: Rate limit exceeded
```

**原因**：
- 请求频率超过限制
- 并发请求过多
- Token 使用超过配额

**解决方案**：

**方案 1：实现速率限制**
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests_per_minute=50):
        self.max_requests = max_requests_per_minute
        self.requests = deque()
    
    def wait_if_needed(self):
        now = time.time()
        # 移除 1 分钟前的请求记录
        while self.requests and self.requests[0] < now - 60:
            self.requests.popleft()
        
        # 如果达到限制，等待
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0])
            time.sleep(sleep_time)
        
        self.requests.append(now)

limiter = RateLimiter(max_requests_per_minute=50)

def call_claude_with_limit(prompt):
    limiter.wait_if_needed()
    return client.messages.create(...)
```

**方案 2：使用指数退避**
```python
import time

def call_with_backoff(prompt, max_retries=5):
    for i in range(max_retries):
        try:
            return client.messages.create(...)
        except anthropic.RateLimitError:
            if i == max_retries - 1:
                raise
            wait_time = 2 ** i  # 1, 2, 4, 8, 16 秒
            print(f"速率限制，等待 {wait_time} 秒...")
            time.sleep(wait_time)
```

### 问题 4：网络连接错误

**症状**：
```
requests.exceptions.ConnectionError: Failed to establish connection
```

**原因**：
- 网络不稳定
- 防火墙阻止
- DNS 解析问题
- 代理配置问题

**解决方案**：

**方案 1：检查网络连接**
```bash
# 测试连接
ping api.anthropic.com

# 测试 HTTPS 连接
curl -I https://api.anthropic.com
```

**方案 2：配置代理**
```python
import os

# 设置代理
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.example.com:8080'

# 或在客户端中配置
import httpx

client = anthropic.Anthropic(
    api_key=API_KEY,
    http_client=httpx.Client(proxies="http://proxy.example.com:8080")
)
```

**方案 3：使用备用 DNS**
```bash
# 修改 /etc/hosts (Linux/Mac)
# 或 C:\Windows\System32\drivers\etc\hosts (Windows)
# 添加：
# 8.8.8.8 api.anthropic.com
```

### 问题 5：AWS Bedrock 特定问题

**症状**：
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**解决方案**：

**步骤 1：配置 AWS 凭证**
```bash
aws configure
# 输入 Access Key ID
# 输入 Secret Access Key
# 输入 Region (如 us-east-1)
```

**步骤 2：验证凭证**
```bash
aws sts get-caller-identity
```

**步骤 3：检查 Bedrock 访问权限**
```bash
aws bedrock list-foundation-models --region us-east-1
```

**步骤 4：请求模型访问**
- 访问 AWS Console
- 进入 Bedrock 服务
- 请求 Claude 模型访问权限

---

## 提示和输出问题

### 问题 6：输出被截断

**症状**：
- 响应突然结束
- 句子不完整
- 缺少预期内容

**原因**：
- `max_tokens` 设置过小
- 输出超过模型限制

**解决方案**：

**方案 1：增加 max_tokens**
```python
# ❌ 太小
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,  # 可能不够
    messages=[{"role": "user", "content": "写一篇文章..."}]
)

# ✅ 合理设置
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=2048,  # 根据需求调整
    messages=[{"role": "user", "content": "写一篇文章..."}]
)
```

**方案 2：检查 stop_reason**
```python
response = client.messages.create(...)

if response.stop_reason == "max_tokens":
    print("⚠️ 输出被截断，需要增加 max_tokens")
elif response.stop_reason == "end_turn":
    print("✅ 输出完整")
```

**方案 3：分段生成**
```python
# 对于长内容，分段生成
sections = ["引言", "主体", "结论"]
full_content = ""

for section in sections:
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"写文章的{section}部分：{full_content}"
        }]
    )
    full_content += response.content[0].text
```

### 问题 7：输出格式不一致

**症状**：
- 有时返回 JSON，有时返回文本
- 格式不符合预期
- 包含不必要的前言

**解决方案**：

**方案 1：使用预填充**
```python
messages = [
    {"role": "user", "content": "列出三种水果"},
    {"role": "assistant", "content": "{"}  # 强制 JSON 格式
]
```

**方案 2：明确格式要求**
```python
PROMPT = """
分析以下文本，以 JSON 格式输出。

<text>
{text}
</text>

输出格式（不要包含任何其他文字）：
{{
  "sentiment": "positive/negative/neutral",
  "keywords": ["keyword1", "keyword2"]
}}
"""
```

**方案 3：后处理验证**
```python
import json
import re

def extract_json(response_text):
    # 尝试直接解析
    try:
        return json.loads(response_text)
    except:
        pass
    
    # 尝试提取 JSON 部分
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            pass
    
    raise ValueError("无法提取有效的 JSON")

response_text = response.content[0].text
data = extract_json(response_text)
```

### 问题 8：Claude 不遵循指令

**症状**：
- 输出与要求不符
- 忽略某些约束
- 添加不必要的内容

**解决方案**：

**方案 1：使用更清晰的指令**
```python
# ❌ 模糊
PROMPT = "分析这个文本"

# ✅ 清晰
PROMPT = """
分析以下文本，只提供以下信息：
1. 主题（一句话）
2. 情感（正面/负面/中性）
3. 关键词（3-5个）

不要包含其他内容。

<text>
{text}
</text>
"""
```

**方案 2：使用系统提示强化**
```python
SYSTEM_PROMPT = """
你必须严格遵循用户的指令。
- 只输出要求的内容
- 不要添加解释或前言
- 严格按照指定格式输出
"""
```

**方案 3：使用预填充**
```python
messages = [
    {"role": "user", "content": "列出三种水果，不要其他内容"},
    {"role": "assistant", "content": "1."}  # 引导直接输出
]
```

### 问题 9：输出包含幻觉

**症状**：
- 编造不存在的事实
- 虚构引用或数据
- 对不确定的信息表现得很确定

**解决方案**：

**方案 1：提供完整上下文**
```python
# ❌ 依赖模型记忆
PROMPT = "总结《XYZ报告》的主要发现"

# ✅ 提供实际内容
PROMPT = """
总结以下报告的主要发现：

<report>
[报告全文]
</report>

只基于上述内容进行总结，不要添加报告中没有的信息。
"""
```

**方案 2：要求引用来源**
```python
PROMPT = """
回答问题并引用文档中的具体内容：

<document>
{document}
</document>

问题：{question}

要求：
- 直接引用文档中的相关句子
- 使用引号标注引用
- 如果文档中没有相关信息，明确说明"文档中未提及"
"""
```

**方案 3：要求承认不确定性**
```python
SYSTEM_PROMPT = """
在回答时：
- 如果不确定，明确说"我不确定"
- 区分事实和推测
- 不要编造信息
- 承认知识的局限性
"""
```

---

## 性能问题

### 问题 10：响应时间过长

**症状**：
- 请求需要很长时间才能完成
- 超过预期的响应时间

**诊断步骤**：

**步骤 1：测量各部分时间**
```python
import time

start_time = time.time()

# 网络时间
request_start = time.time()
response = client.messages.create(...)
request_end = time.time()

# 处理时间
process_start = time.time()
result = process_response(response)
process_end = time.time()

print(f"网络时间: {request_end - request_start:.2f}s")
print(f"处理时间: {process_end - process_start:.2f}s")
print(f"总时间: {time.time() - start_time:.2f}s")
```

**解决方案**：

**方案 1：优化提示长度**
```python
# 减少输入 tokens
prompt = optimize_prompt(original_prompt)
```

**方案 2：使用更快的模型**
```python
# Haiku 比 Opus 快得多
model = "claude-3-haiku-20240307"  # 而不是 opus
```

**方案 3：使用流式输出**
```python
# 获得更快的首字节时间
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**方案 4：并行处理**
```python
# 对于多个独立请求，并行处理
import asyncio

async def process_batch(items):
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)
```

### 问题 11：Token 使用超出预期

**症状**：
- API 费用高于预期
- Token 计数与预期不符

**诊断**：

```python
response = client.messages.create(...)

print(f"输入 tokens: {response.usage.input_tokens}")
print(f"输出 tokens: {response.usage.output_tokens}")
print(f"总 tokens: {response.usage.input_tokens + response.usage.output_tokens}")

# 估算成本（以 Haiku 为例）
input_cost = response.usage.input_tokens * 0.00025 / 1000
output_cost = response.usage.output_tokens * 0.00125 / 1000
total_cost = input_cost + output_cost
print(f"估算成本: ${total_cost:.4f}")
```

**解决方案**：

**方案 1：优化提示**
- 移除冗余内容
- 使用更简洁的表达
- 避免重复信息

**方案 2：控制输出长度**
```python
# 设置合理的 max_tokens
response = client.messages.create(
    max_tokens=500,  # 而不是 4096
    ...
)
```

**方案 3：使用缓存**
```python
# 缓存常见查询的结果
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_response(prompt):
    return call_claude(prompt)
```

---

## 质量问题

### 问题 12：输出质量不稳定

**症状**：
- 相同提示产生不同质量的输出
- 有时好有时差

**原因**：
- temperature 设置过高
- 提示不够明确
- 缺少示例

**解决方案**：

**方案 1：设置 temperature = 0**
```python
response = client.messages.create(
    temperature=0.0,  # 最大化一致性
    ...
)
```

**方案 2：提供更明确的指令**
```python
PROMPT = """
严格按照以下格式输出：

格式：
- 第一行：标题
- 第二行：摘要（不超过50字）
- 第三行开始：详细内容

示例：
标题：示例标题
摘要：这是一个示例摘要，不超过五十字。
详细内容从这里开始...
"""
```

**方案 3：使用少样本学习**
```python
PROMPT = """
示例1：
输入：{example1_input}
输出：{example1_output}

示例2：
输入：{example2_input}
输出：{example2_output}

现在处理：
输入：{actual_input}
输出：
"""
```

### 问题 13：输出不够准确

**症状**：
- 事实错误
- 逻辑错误
- 理解偏差

**解决方案**：

**方案 1：使用思维链**
```python
PROMPT = """
请逐步分析：

1. 理解问题
2. 识别关键信息
3. 逐步推理
4. 得出结论
5. 验证答案

问题：{question}
"""
```

**方案 2：提供更多上下文**
```python
PROMPT = """
<context>
{relevant_context}
</context>

<question>
{question}
</question>

基于上述上下文回答问题。
"""
```

**方案 3：使用更强大的模型**
```python
# 对于复杂任务，使用 Opus
model = "claude-3-opus-20240229"
```

---

## 成本问题

### 问题 14：成本超出预算

**症状**：
- API 费用高于预期
- 成本增长过快

**诊断**：

```python
# 追踪每个请求的成本
def track_cost(response, model):
    # Haiku 价格（示例）
    prices = {
        "claude-3-haiku-20240307": {
            "input": 0.00025 / 1000,
            "output": 0.00125 / 1000
        },
        # 其他模型...
    }
    
    input_cost = response.usage.input_tokens * prices[model]["input"]
    output_cost = response.usage.output_tokens * prices[model]["output"]
    
    return {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost
    }
```

**解决方案**：

**方案 1：使用更经济的模型**
```python
# 对于简单任务，使用 Haiku
model = "claude-3-haiku-20240307"  # 最便宜
```

**方案 2：优化提示长度**
- 移除不必要的内容
- 使用摘要而非全文
- 批量处理

**方案 3：实施成本控制**
```python
class CostController:
    def __init__(self, daily_budget=10.0):
        self.daily_budget = daily_budget
        self.daily_cost = 0.0
        self.last_reset = datetime.now().date()
    
    def check_budget(self, estimated_cost):
        # 检查是否需要重置
        if datetime.now().date() > self.last_reset:
            self.daily_cost = 0.0
            self.last_reset = datetime.now().date()
        
        # 检查预算
        if self.daily_cost + estimated_cost > self.daily_budget:
            raise Exception("超出每日预算")
        
        self.daily_cost += estimated_cost
```

---

## 调试技巧和工具

### 1. 启用详细日志

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 记录请求详情
logger = logging.getLogger(__name__)

def call_claude_with_logging(prompt):
    logger.info(f"发送请求，提示长度: {len(prompt)}")
    
    try:
        response = client.messages.create(...)
        logger.info(f"收到响应，tokens: {response.usage.input_tokens + response.usage.output_tokens}")
        return response
    except Exception as e:
        logger.error(f"请求失败: {str(e)}")
        raise
```

### 2. 使用调试包装器

```python
class DebugClient:
    def __init__(self, client):
        self.client = client
        self.requests = []
    
    def messages_create(self, **kwargs):
        # 记录请求
        request_info = {
            "timestamp": datetime.now(),
            "model": kwargs.get("model"),
            "prompt_length": len(str(kwargs.get("messages"))),
            "max_tokens": kwargs.get("max_tokens")
        }
        
        try:
            response = self.client.messages.create(**kwargs)
            request_info["success"] = True
            request_info["tokens"] = response.usage.input_tokens + response.usage.output_tokens
            return response
        except Exception as e:
            request_info["success"] = False
            request_info["error"] = str(e)
            raise
        finally:
            self.requests.append(request_info)
    
    def get_stats(self):
        total_requests = len(self.requests)
        successful = sum(1 for r in self.requests if r["success"])
        failed = total_requests - successful
        
        return {
            "total_requests": total_requests,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total_requests if total_requests > 0 else 0
        }

# 使用
debug_client = DebugClient(client)
response = debug_client.messages_create(...)
print(debug_client.get_stats())
```

### 3. 提示调试工具

```python
def debug_prompt(prompt):
    """分析提示的潜在问题"""
    issues = []
    
    # 检查长度
    if len(prompt) > 10000:
        issues.append("⚠️ 提示过长，可能影响性能")
    
    # 检查是否包含明确指令
    if "请" not in prompt and "输出" not in prompt:
        issues.append("⚠️ 缺少明确的指令动词")
    
    # 检查是否有格式说明
    if "格式" not in prompt and "JSON" not in prompt:
        issues.append("💡 考虑添加输出格式说明")
    
    # 检查是否有示例
    if "示例" not in prompt and "例如" not in prompt:
        issues.append("💡 考虑添加示例以提高质量")
    
    return issues

# 使用
issues = debug_prompt(my_prompt)
for issue in issues:
    print(issue)
```

### 4. 响应验证工具

```python
def validate_response(response, expected_format=None, required_fields=None):
    """验证响应是否符合预期"""
    validation_results = {
        "valid": True,
        "issues": []
    }
    
    text = response.content[0].text
    
    # 检查是否被截断
    if response.stop_reason == "max_tokens":
        validation_results["valid"] = False
        validation_results["issues"].append("响应被截断")
    
    # 检查格式
    if expected_format == "json":
        try:
            data = json.loads(text)
            
            # 检查必需字段
            if required_fields:
                for field in required_fields:
                    if field not in data:
                        validation_results["valid"] = False
                        validation_results["issues"].append(f"缺少字段: {field}")
        except json.JSONDecodeError:
            validation_results["valid"] = False
            validation_results["issues"].append("不是有效的 JSON")
    
    return validation_results

# 使用
validation = validate_response(
    response,
    expected_format="json",
    required_fields=["sentiment", "keywords"]
)

if not validation["valid"]:
    print("验证失败:")
    for issue in validation["issues"]:
        print(f"  - {issue}")
```

### 5. 性能分析工具

```python
import time
from collections import defaultdict

class PerformanceProfiler:
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def profile(self, name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                
                self.metrics[name].append(end_time - start_time)
                return result
            return wrapper
        return decorator
    
    def report(self):
        for name, times in self.metrics.items():
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"{name}:")
            print(f"  平均: {avg_time:.2f}s")
            print(f"  最小: {min_time:.2f}s")
            print(f"  最大: {max_time:.2f}s")
            print(f"  调用次数: {len(times)}")

# 使用
profiler = PerformanceProfiler()

@profiler.profile("claude_call")
def call_claude(prompt):
    return client.messages.create(...)

# 执行多次调用
for prompt in prompts:
    call_claude(prompt)

# 查看报告
profiler.report()
```

### 6. 推荐的第三方工具

**监控和分析**：
- **Langfuse**：LLM 应用性能监控
- **Helicone**：API 调用追踪和分析
- **Weights & Biases**：实验追踪

**开发工具**：
- **Jupyter Notebook**：交互式开发和调试
- **Postman**：API 测试
- **curl**：命令行 API 测试

**日志和错误追踪**：
- **Sentry**：错误追踪
- **Datadog**：应用监控
- **CloudWatch**：AWS 环境监控

---

## 获取帮助

### 1. 自助资源

**官方文档**：
- [Anthropic 文档](https://docs.anthropic.com/)
- [API 参考](https://docs.anthropic.com/claude/reference/)
- [最佳实践](https://docs.anthropic.com/claude/docs/best-practices)

**本项目文档**：
- [设计原理](design-principles.md)
- [性能优化](performance.md)
- [常见问题](faq.md)
- [完整使用手册](../user-guide/user-guide.md)

### 2. 社区支持

**Anthropic 社区**：
- [Discord 服务器](https://discord.gg/anthropic)
- [社区论坛](https://community.anthropic.com/)
- [GitHub Discussions](https://github.com/anthropics/anthropic-sdk-python/discussions)

**提问技巧**：
1. 提供完整的错误信息
2. 包含最小可复现示例
3. 说明已尝试的解决方案
4. 描述预期行为和实际行为

### 3. 技术支持

**Anthropic 支持**：
- 企业客户：通过 Anthropic Console 提交工单
- 技术问题：support@anthropic.com
- 安全问题：security@anthropic.com

**AWS Bedrock 支持**：
- AWS Support Center
- AWS 论坛
- AWS 文档

### 4. 报告问题

**提交 Bug 报告时包含**：
```
环境信息：
- 操作系统：
- Python 版本：
- SDK 版本：
- 模型：

问题描述：
[详细描述问题]

复现步骤：
1. 
2. 
3. 

预期行为：
[描述预期结果]

实际行为：
[描述实际结果]

错误信息：
```
[完整的错误日志]
```

最小可复现代码：
```python
[最简单的能复现问题的代码]
```
```

---

## 相关资源

### 官方资源
- [Anthropic 官网](https://www.anthropic.com/)
- [Claude API 文档](https://docs.anthropic.com/claude/)
- [Anthropic Console](https://console.anthropic.com/)
- [状态页面](https://status.anthropic.com/)

### 开发资源
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)
- [Cookbook](https://github.com/anthropics/anthropic-cookbook)

### 学习资源
- [提示工程指南](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [最佳实践](https://docs.anthropic.com/claude/docs/best-practices)
- [示例项目](https://github.com/anthropics/anthropic-cookbook)

### 相关文档
- [设计原理](design-principles.md)：理解问题背后的原理
- [性能优化](performance.md)：提高性能和降低成本
- [常见问题](faq.md)：快速查找答案
- [API 参考](../user-guide/api-reference.md)：API 详细说明

---

**上一步**：[性能优化](performance.md)  
**下一步**：[常见问题](faq.md)

**相关文档**：
- [完整使用手册](../user-guide/user-guide.md)
- [安装指南](../getting-started/installation.md)
- [快速开始](../getting-started/quickstart.md)


