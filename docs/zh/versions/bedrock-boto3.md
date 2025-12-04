# Bedrock Boto3 版本文档

## 目录

- [概述](#概述)
- [目标读者](#目标读者)
- [版本特点](#版本特点)
- [前置条件](#前置条件)
- [安装指南](#安装指南)
- [配置说明](#配置说明)
- [使用示例](#使用示例)
- [Boto3 高级功能](#boto3-高级功能)
- [最佳实践](#最佳实践)

---

## 概述

Bedrock Boto3 版本使用 AWS 原生的 Boto3 SDK 通过 Amazon Bedrock 访问 Claude 模型。这是最底层、最灵活的实现方式，适合需要完全 AWS 原生体验和细粒度控制的场景。

**版本标识**：🟨 Bedrock Boto3

**目录位置**：`AmazonBedrock/boto3/`

## 目标读者

- 深度使用 AWS 服务的企业开发者
- 已经使用 Boto3 管理 AWS 资源的团队
- 需要完全 AWS 原生体验的项目
- 需要更细粒度请求控制的高级用户

## 版本特点

### 核心优势

✅ **AWS 原生**
- 完全的 AWS 原生体验
- 与其他 AWS 服务无缝集成
- 统一的 Boto3 API 风格

✅ **细粒度控制**
- 更底层的 API 访问
- 完全控制请求和响应
- 灵活的配置选项

✅ **统一管理**
- 使用 Boto3 管理所有 AWS 资源
- 统一的错误处理
- 一致的认证机制

✅ **企业级功能**
- 完整的 AWS 企业功能
- IAM 精细权限控制
- CloudWatch 深度集成

### 适用场景

- 🏢 **AWS 原生应用**：深度集成 AWS 生态系统
- 🔧 **现有 Boto3 项目**：已使用 Boto3 的项目
- 🎛️ **高级控制**：需要细粒度 API 控制
- 📊 **企业级应用**：大规模 AWS 部署
- 🔗 **多服务集成**：与多个 AWS 服务交互

### 不适用场景

- ❌ 不熟悉 AWS 和 Boto3
- ❌ 希望简化的 API 接口
- ❌ 快速原型开发
- ❌ 不使用 AWS 的项目

## 前置条件

### 1. AWS 账户和 Bedrock 访问

与 Bedrock Anthropic SDK 版本相同，您需要：

- 有效的 AWS 账户
- 启用 Amazon Bedrock 服务
- 请求并获得 Claude 模型访问权限

详细步骤请参考 [Bedrock Anthropic SDK 版本文档](./bedrock-anthropic.md#前置条件)。

### 2. AWS 凭证配置

配置 AWS 访问凭证：

```bash
aws configure
```

或使用环境变量：

```bash
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

### 3. IAM 权限

确保具有以下权限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-*"
    }
  ]
}
```

### 4. Python 环境

- Python 3.7 或更高版本
- pip 包管理器
- Jupyter Notebook

## 安装指南

### 步骤 1：克隆仓库

```bash
git clone https://github.com/anthropics/prompt-eng-interactive-tutorial.git
cd prompt-eng-interactive-tutorial
```

### 步骤 2：进入 Bedrock Boto3 目录

```bash
cd AmazonBedrock/boto3
```

### 步骤 3：安装依赖

```bash
pip install -U pip
pip install -r ../requirements.txt
```

**依赖列表**：
```
awscli==1.32.74
boto3==1.34.74
botocore==1.34.74
pickleshare==0.7.5
```

**注意**：此版本不需要 `anthropic` 包，完全使用 Boto3。

### 步骤 4：配置 AWS 凭证

```bash
aws configure
```

### 步骤 5：启动 Jupyter Notebook

```bash
jupyter notebook
```

### 步骤 6：运行初始化 Notebook

打开 `00_Tutorial_How-To.ipynb` 并运行：

```python
import boto3

# 获取当前区域
session = boto3.Session()
AWS_REGION = session.region_name
print("AWS Region:", AWS_REGION)

MODEL_NAME = "anthropic.claude-3-haiku-20240307-v1:0"

# 存储变量
%store MODEL_NAME
%store AWS_REGION
```

### 步骤 7：验证安装

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)

def get_completion(prompt):
    body = json.dumps({
        "anthropic_version": '',
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "top_p": 1,
        "system": ''
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId=MODEL_NAME
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body.get('content')[0].get('text')

# 测试
print(get_completion("Hello, Claude!"))
```

如果看到 Claude 的回复，说明配置成功！

## 配置说明

### 客户端初始化

#### 基本配置

```python
import boto3

# 使用默认配置
bedrock = boto3.client('bedrock-runtime')

# 指定区域
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
```

#### 使用特定凭证

```python
import boto3

# 使用显式凭证
bedrock = boto3.client(
    'bedrock-runtime',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='us-east-1'
)
```

#### 使用 Session

```python
import boto3

# 创建 session
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='us-east-1'
)

# 从 session 创建客户端
bedrock = session.client('bedrock-runtime')
```

#### 高级配置

```python
import boto3
from botocore.config import Config

# 自定义配置
config = Config(
    region_name='us-east-1',
    signature_version='v4',
    retries={
        'max_attempts': 3,
        'mode': 'adaptive'
    },
    connect_timeout=5,
    read_timeout=60
)

bedrock = boto3.client('bedrock-runtime', config=config)
```

### 模型选择

Bedrock 中的 Claude 模型 ID：

```python
# Claude 3 系列
MODEL_ID = "anthropic.claude-3-opus-20240229-v1:0"    # 最强大
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"  # 平衡性能
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"   # 最快速（教程默认）

# Claude 2 系列
MODEL_ID = "anthropic.claude-v2:1"
MODEL_ID = "anthropic.claude-v2"
MODEL_ID = "anthropic.claude-instant-v1"
```

### 请求体结构

Boto3 版本需要手动构建 JSON 请求体：

```python
import json

# 基本请求体
request_body = {
    "anthropic_version": "",  # 可选，留空使用默认版本
    "max_tokens": 2000,       # 必需
    "messages": [             # 必需
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ],
    "temperature": 0.0,       # 可选，默认 1.0
    "top_p": 1.0,            # 可选，默认 1.0
    "top_k": 250,            # 可选
    "stop_sequences": [],     # 可选
    "system": ""             # 可选，系统提示
}

# 转换为 JSON 字符串
body = json.dumps(request_body)
```

### API 调用

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# 调用模型
response = bedrock.invoke_model(
    modelId="anthropic.claude-3-haiku-20240307-v1:0",
    body=json.dumps({
        "anthropic_version": "",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 0.0
    })
)

# 解析响应
response_body = json.loads(response['body'].read())
text = response_body['content'][0]['text']
```

## 使用示例

### 示例 1：基本对话

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def get_completion(prompt: str, model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"):
    body = json.dumps({
        "anthropic_version": "",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "top_p": 1
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body.get('content')[0].get('text')

# 使用
result = get_completion("解释什么是提示工程")
print(result)
```

### 示例 2：使用系统提示

```python
def get_completion_with_system(prompt: str, system: str = ""):
    body = json.dumps({
        "anthropic_version": "",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "system": system
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId="anthropic.claude-3-haiku-20240307-v1:0"
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

# 使用
system_prompt = "你是一位专业的 Python 编程导师"
result = get_completion_with_system(
    "如何使用列表推导式？",
    system_prompt
)
print(result)
```

### 示例 3：多轮对话

```python
def chat(messages: list, system: str = ""):
    body = json.dumps({
        "anthropic_version": "",
        "max_tokens": 2000,
        "messages": messages,
        "temperature": 0.0,
        "system": system
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId="anthropic.claude-3-haiku-20240307-v1:0"
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

# 构建对话
conversation = [
    {"role": "user", "content": "什么是机器学习？"}
]

response1 = chat(conversation)
print("Claude:", response1)

# 添加到历史
conversation.append({"role": "assistant", "content": response1})
conversation.append({"role": "user", "content": "能举个例子吗？"})

response2 = chat(conversation)
print("Claude:", response2)
```

### 示例 4：流式响应

```python
def stream_completion(prompt: str):
    body = json.dumps({
        "anthropic_version": "",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    })
    
    response = bedrock.invoke_model_with_response_stream(
        body=body,
        modelId="anthropic.claude-3-haiku-20240307-v1:0"
    )
    
    stream = response.get('body')
    if stream:
        for event in stream:
            chunk = event.get('chunk')
            if chunk:
                chunk_data = json.loads(chunk.get('bytes').decode())
                
                if chunk_data['type'] == 'content_block_delta':
                    if chunk_data['delta']['type'] == 'text_delta':
                        print(chunk_data['delta']['text'], end='', flush=True)
    
    print()  # 换行

# 使用
stream_completion("写一首关于云计算的短诗")
```
### 示例 5：响应元数据

```python
def get_completion_with_metadata(prompt: str):
    body = json.dumps({
        "anthropic_version": "",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId="anthropic.claude-3-haiku-20240307-v1:0"
    )
    
    # 获取响应元数据
    response_metadata = response['ResponseMetadata']
    print(f"请求 ID: {response_metadata['RequestId']}")
    print(f"HTTP 状态码: {response_metadata['HTTPStatusCode']}")
    
    # 解析响应体
    response_body = json.loads(response['body'].read())
    
    # 获取使用信息
    usage = response_body.get('usage', {})
    print(f"输入 tokens: {usage.get('input_tokens', 0)}")
    print(f"输出 tokens: {usage.get('output_tokens', 0)}")
    
    return response_body['content'][0]['text']

# 使用
result = get_completion_with_metadata("解释量子计算")
print(f"\n回复: {result}")
```

### 示例 6：与其他 AWS 服务集成

```python
import boto3
import json

# 初始化多个 AWS 服务客户端
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def process_document_from_s3(bucket: str, key: str):
    """从 S3 读取文档，使用 Claude 处理，保存结果到 DynamoDB"""
    
    # 从 S3 读取
    s3_response = s3.get_object(Bucket=bucket, Key=key)
    document_text = s3_response['Body'].read().decode('utf-8')
    
    # 使用 Claude 处理
    prompt = f"请总结以下文档：\n\n{document_text}"
    body = json.dumps({
        "anthropic_version": "",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    })
    
    bedrock_response = bedrock.invoke_model(
        body=body,
        modelId="anthropic.claude-3-haiku-20240307-v1:0"
    )
    
    response_body = json.loads(bedrock_response['body'].read())
    summary = response_body['content'][0]['text']
    
    # 保存到 DynamoDB
    table = dynamodb.Table('DocumentSummaries')
    table.put_item(
        Item={
            'document_key': key,
            'summary': summary,
            'timestamp': int(time.time())
        }
    )
    
    return summary

# 使用
summary = process_document_from_s3('my-bucket', 'documents/report.txt')
print(summary)
```

## Boto3 高级功能

### 1. 分页器（Paginator）

虽然 Bedrock 的 `invoke_model` 不使用分页，但在列出模型时可以使用：

```python
import boto3

bedrock = boto3.client('bedrock', region_name='us-east-1')

# 使用分页器列出所有基础模型
paginator = bedrock.get_paginator('list_foundation_models')
page_iterator = paginator.paginate()

for page in page_iterator:
    for model in page['modelSummaries']:
        if 'anthropic' in model['modelId'].lower():
            print(f"模型: {model['modelId']}")
            print(f"  提供商: {model['providerName']}")
            print(f"  输入模态: {model.get('inputModalities', [])}")
            print(f"  输出模态: {model.get('outputModalities', [])}")
            print()
```

### 2. 等待器（Waiter）

用于等待异步操作完成：

```python
import boto3

bedrock = boto3.client('bedrock', region_name='us-east-1')

# 等待模型访问被授予（如果有相应的 waiter）
# 注意：Bedrock 可能没有所有操作的 waiter
try:
    waiter = bedrock.get_waiter('model_customization_job_complete')
    waiter.wait(jobIdentifier='job-id')
    print("任务完成")
except Exception as e:
    print(f"等待器不可用或出错: {e}")
```

### 3. 资源（Resource）

Boto3 资源提供更高级的接口（Bedrock 主要使用客户端）：

```python
import boto3

# S3 资源示例（与 Bedrock 配合使用）
s3 = boto3.resource('s3')

# 上传文件
bucket = s3.Bucket('my-bucket')
bucket.upload_file('local_file.txt', 'remote_file.txt')

# 下载文件
bucket.download_file('remote_file.txt', 'downloaded_file.txt')
```

### 4. 会话管理

```python
import boto3
from botocore.session import Session

# 创建自定义会话
botocore_session = Session()
botocore_session.set_credentials(
    access_key='YOUR_ACCESS_KEY',
    secret_key='YOUR_SECRET_KEY'
)

# 从 botocore session 创建 boto3 session
boto3_session = boto3.Session(botocore_session=botocore_session)

# 创建客户端
bedrock = boto3_session.client('bedrock-runtime', region_name='us-east-1')
```

## 最佳实践

### 1. 错误处理

```python
import boto3
import json
import time
from botocore.exceptions import ClientError, BotoCoreError

def robust_invoke_model(prompt: str, max_retries: int = 3):
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    for attempt in range(max_retries):
        try:
            body = json.dumps({
                "anthropic_version": "",
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0
            })
            
            response = bedrock.invoke_model(
                body=body,
                modelId="anthropic.claude-3-haiku-20240307-v1:0"
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            if error_code == 'ThrottlingException':
                wait_time = (2 ** attempt) + (random.randint(0, 1000) / 1000)
                print(f"速率限制，等待 {wait_time:.2f}s...")
                time.sleep(wait_time)
            
            elif error_code == 'ModelTimeoutException':
                print("模型超时，重试...")
                time.sleep(2)
            
            elif error_code == 'ModelNotReadyException':
                print("模型未就绪，等待...")
                time.sleep(5)
            
            elif error_code == 'ValidationException':
                print(f"验证错误: {error_message}")
                raise
            
            elif error_code == 'AccessDeniedException':
                print(f"访问被拒绝: {error_message}")
                raise
            
            elif error_code == 'ResourceNotFoundException':
                print(f"资源未找到: {error_message}")
                raise
            
            else:
                print(f"未知错误 ({error_code}): {error_message}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    raise
        
        except BotoCoreError as e:
            print(f"Boto3 核心错误: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                raise
        
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            raise
        
        except Exception as e:
            print(f"未预期的错误: {e}")
            raise
    
    raise Exception("达到最大重试次数")
```

### 2. 连接池配置

```python
import boto3
from botocore.config import Config

# 配置连接池
config = Config(
    region_name='us-east-1',
    max_pool_connections=50,  # 最大连接数
    retries={
        'max_attempts': 3,
        'mode': 'adaptive'
    }
)

bedrock = boto3.client('bedrock-runtime', config=config)
```

### 3. 超时配置

```python
from botocore.config import Config

config = Config(
    connect_timeout=5,   # 连接超时（秒）
    read_timeout=60,     # 读取超时（秒）
    retries={
        'max_attempts': 3
    }
)

bedrock = boto3.client('bedrock-runtime', config=config)
```

### 4. 日志配置

```python
import boto3
import logging

# 配置 Boto3 日志
boto3.set_stream_logger('boto3.resources', logging.INFO)
boto3.set_stream_logger('botocore', logging.DEBUG)

# 或使用标准 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('boto3')
logger.setLevel(logging.DEBUG)
```

### 5. 成本优化

```python
import boto3
import json

def cost_aware_completion(prompt: str, max_cost_per_request: float = 0.01):
    """带成本控制的请求"""
    
    # 估算输入 tokens（粗略估计：1 token ≈ 4 字符）
    estimated_input_tokens = len(prompt) // 4
    
    # Claude 3 Haiku 定价（示例，请查看最新定价）
    input_price_per_1k = 0.00025  # $0.25 per 1M tokens
    output_price_per_1k = 0.00125  # $1.25 per 1M tokens
    
    # 估算最大输出 tokens
    max_output_tokens = 2000
    
    # 估算成本
    estimated_cost = (
        (estimated_input_tokens / 1000) * input_price_per_1k +
        (max_output_tokens / 1000) * output_price_per_1k
    )
    
    if estimated_cost > max_cost_per_request:
        raise ValueError(f"预估成本 ${estimated_cost:.4f} 超过限制 ${max_cost_per_request}")
    
    # 执行请求
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    body = json.dumps({
        "anthropic_version": "",
        "max_tokens": max_output_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId="anthropic.claude-3-haiku-20240307-v1:0"
    )
    
    response_body = json.loads(response['body'].read())
    
    # 计算实际成本
    usage = response_body.get('usage', {})
    actual_input_tokens = usage.get('input_tokens', 0)
    actual_output_tokens = usage.get('output_tokens', 0)
    
    actual_cost = (
        (actual_input_tokens / 1000) * input_price_per_1k +
        (actual_output_tokens / 1000) * output_price_per_1k
    )
    
    print(f"实际成本: ${actual_cost:.6f}")
    
    return response_body['content'][0]['text']
```

### 6. 批量处理

```python
import boto3
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def batch_process(prompts: list, max_workers: int = 5):
    """并发处理多个提示"""
    
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    def process_one(prompt: str):
        body = json.dumps({
            "anthropic_version": "",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0
        })
        
        response = bedrock.invoke_model(
            body=body,
            modelId="anthropic.claude-3-haiku-20240307-v1:0"
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_prompt = {
            executor.submit(process_one, prompt): prompt 
            for prompt in prompts
        }
        
        for future in as_completed(future_to_prompt):
            prompt = future_to_prompt[future]
            try:
                result = future.result()
                results.append({'prompt': prompt, 'result': result, 'error': None})
            except Exception as e:
                results.append({'prompt': prompt, 'result': None, 'error': str(e)})
    
    return results

# 使用
prompts = ["提示1", "提示2", "提示3"]
results = batch_process(prompts, max_workers=3)

for item in results:
    if item['error']:
        print(f"错误: {item['error']}")
    else:
        print(f"结果: {item['result'][:100]}...")
```
