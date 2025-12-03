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

