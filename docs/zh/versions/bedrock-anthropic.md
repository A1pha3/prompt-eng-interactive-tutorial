# Bedrock Anthropic SDK 版本文档

## 概述

Bedrock Anthropic SDK 版本通过 Amazon Bedrock 平台使用 Anthropic SDK 访问 Claude 模型。这个版本结合了 Anthropic SDK 的易用性和 AWS Bedrock 的企业级功能，是从 Anthropic 1P 迁移到 AWS 的理想选择。

**版本标识**：🟧 Bedrock Anthropic SDK

**目录位置**：`AmazonBedrock/anthropic/`

## 目标读者

- 使用 AWS 基础设施的企业开发者
- 需要 AWS 企业功能的团队
- 从 Anthropic 1P 迁移到 AWS 的用户
- 希望保持 Anthropic SDK API 风格的开发者

## 版本特点

### 核心优势

✅ **熟悉的 API**
- 与 Anthropic 1P 相似的 API 接口
- 最小化迁移成本
- 保持代码一致性

✅ **AWS 集成**
- 完整的 AWS 生态系统集成
- IAM 权限管理
- CloudWatch 监控和日志
- VPC 和网络安全

✅ **企业级功能**
- AWS 企业支持和 SLA
- 合规性和审计功能
- 数据驻留控制
- 成本管理和优化

✅ **简化的认证**
- 使用 AWS 凭证
- 支持 IAM 角色
- 无需管理额外的 API 密钥

### 适用场景

- 🏢 **企业应用**：需要企业级功能和支持
- 🔐 **安全合规**：严格的安全和合规要求
- 🔗 **AWS 集成**：与其他 AWS 服务集成
- 📊 **统一管理**：在 AWS 中统一管理资源
- 🔄 **平滑迁移**：从 Anthropic 1P 迁移

### 不适用场景

- ❌ 不使用 AWS 的项目
- ❌ 需要最底层 AWS 控制的场景
- ❌ 预算非常有限的个人项目
- ❌ 不熟悉 AWS 的初学者

## 前置条件

### 1. AWS 账户

您需要一个有效的 AWS 账户并启用 Amazon Bedrock 服务。

**创建 AWS 账户**：
1. 访问 [AWS 注册页面](https://aws.amazon.com/)
2. 按照指引创建账户
3. 配置支付方式

**启用 Amazon Bedrock**：
1. 登录 AWS 控制台
2. 搜索并打开 Amazon Bedrock 服务
3. 在支持的区域启用服务
4. 请求访问 Claude 模型（如需要）

### 2. AWS 凭证配置

您需要配置 AWS 访问凭证。

**方式 1：AWS CLI 配置**（推荐）

```bash
# 安装 AWS CLI
pip install awscli

# 配置凭证
aws configure
```

输入以下信息：
- AWS Access Key ID
- AWS Secret Access Key
- Default region name（如 `us-east-1`）
- Default output format（如 `json`）

**方式 2：环境变量**

```bash
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

**方式 3：IAM 角色**（EC2、Lambda 等）

在 AWS 服务中运行时，可以使用 IAM 角色自动获取凭证。

### 3. Bedrock 权限

确保您的 IAM 用户或角色具有以下权限：

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

### 4. 支持的 AWS 区域

Amazon Bedrock 在以下区域提供 Claude 模型（持续更新）：

- `us-east-1` (美国东部 - 弗吉尼亚北部)
- `us-west-2` (美国西部 - 俄勒冈)
- `ap-southeast-1` (亚太地区 - 新加坡)
- `ap-northeast-1` (亚太地区 - 东京)
- `eu-central-1` (欧洲 - 法兰克福)

查看最新区域支持：[Bedrock 区域](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html#bedrock-regions)

### 5. Python 环境

- Python 3.7 或更高版本
- pip 包管理器
- Jupyter Notebook（用于运行教程）

## 安装指南

### 步骤 1：克隆仓库

```bash
git clone https://github.com/anthropics/prompt-eng-interactive-tutorial.git
cd prompt-eng-interactive-tutorial
```

### 步骤 2：进入 Bedrock Anthropic 目录

```bash
cd AmazonBedrock/anthropic
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
anthropic==0.21.3
pickleshare==0.7.5
```

### 步骤 4：配置 AWS 凭证

如果尚未配置，运行：

```bash
aws configure
```

### 步骤 5：启动 Jupyter Notebook

```bash
jupyter notebook
```

### 步骤 6：运行初始化 Notebook

打开 `00_Tutorial_How-To.ipynb` 并运行所有单元格：

1. 安装依赖（如果需要）
2. 重启内核
3. 设置区域和模型名称
4. 测试连接

```python
import boto3

# 自动获取当前区域
session = boto3.Session()
AWS_REGION = session.region_name
print("AWS Region:", AWS_REGION)

MODEL_NAME = "anthropic.claude-3-haiku-20240307-v1:0"

# 存储变量
%store MODEL_NAME
%store AWS_REGION
```

### 步骤 7：验证安装

运行测试代码：

```python
from anthropic import AnthropicBedrock

client = AnthropicBedrock(aws_region=AWS_REGION)

def get_completion(prompt, system=''):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt}
        ],
        system=system
    )
    return message.content[0].text

# 测试
print(get_completion("Hello, Claude!"))
```

如果看到 Claude 的回复，说明配置成功！

## 配置说明

### 客户端初始化

#### 基本配置

```python
from anthropic import AnthropicBedrock

# 使用默认凭证和区域
client = AnthropicBedrock()

# 指定区域
client = AnthropicBedrock(aws_region="us-east-1")
```

#### 使用特定凭证

```python
import boto3
from anthropic import AnthropicBedrock

# 创建自定义 session
session = boto3.Session(
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY",
    region_name="us-east-1"
)

# 使用自定义 session
client = AnthropicBedrock(aws_session=session)
```

#### 使用 IAM 角色

```python
from anthropic import AnthropicBedrock

# 在 EC2、Lambda 等环境中自动使用 IAM 角色
client = AnthropicBedrock(aws_region="us-east-1")
```

### 模型选择

Bedrock 中的 Claude 模型使用特定的模型 ID：

```python
# Claude 3 系列（Bedrock 模型 ID）
MODEL_NAME = "anthropic.claude-3-opus-20240229-v1:0"    # 最强大
MODEL_NAME = "anthropic.claude-3-sonnet-20240229-v1:0"  # 平衡性能
MODEL_NAME = "anthropic.claude-3-haiku-20240307-v1:0"   # 最快速（教程默认）

# Claude 2 系列
MODEL_NAME = "anthropic.claude-v2:1"
MODEL_NAME = "anthropic.claude-v2"
MODEL_NAME = "anthropic.claude-instant-v1"
```

**注意**：Bedrock 模型 ID 与 Anthropic 1P 不同，需要添加 `anthropic.` 前缀和版本后缀。

### API 参数配置

```python
message = client.messages.create(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    max_tokens=2000,        # 最大输出 token 数
    temperature=0.0,        # 温度（0-1）
    messages=[
        {"role": "user", "content": "Your prompt here"}
    ],
    system="Optional system prompt",  # 系统提示
    stop_sequences=["\n\n"]  # 停止序列
)
```

API 参数与 Anthropic 1P 版本基本相同，保持了良好的兼容性。

## 使用示例

### 示例 1：基本对话

```python
from anthropic import AnthropicBedrock

client = AnthropicBedrock(aws_region="us-east-1")

def get_completion(prompt: str, system: str = ''):
    message = client.messages.create(
        model="anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens=2000,
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt}
        ],
        system=system
    )
    return message.content[0].text

# 使用
response = get_completion("解释什么是提示工程")
print(response)
```

### 示例 2：使用系统提示

```python
system_prompt = "你是一位专业的 Python 编程导师，擅长用简单的语言解释复杂概念。"

response = get_completion(
    "如何使用列表推导式？",
    system=system_prompt
)
print(response)
```

### 示例 3：多轮对话

```python
def chat(messages: list, system: str = ''):
    message = client.messages.create(
        model="anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens=2000,
        temperature=0.0,
        messages=messages,
        system=system
    )
    return message.content[0].text

# 构建对话
conversation = [
    {"role": "user", "content": "什么是机器学习？"},
]

response1 = chat(conversation)
print("Claude:", response1)

conversation.append({"role": "assistant", "content": response1})
conversation.append({"role": "user", "content": "能举个例子吗？"})

response2 = chat(conversation)
print("Claude:", response2)
```


### 示例 4：流式响应

```python
def stream_completion(prompt: str):
    with client.messages.stream(
        model="anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens=2000,
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()

# 使用
stream_completion("写一首关于云计算的短诗")
```

### 示例 5：与 AWS 服务集成

```python
import boto3
from anthropic import AnthropicBedrock

# 初始化客户端
bedrock_client = AnthropicBedrock(aws_region="us-east-1")
s3_client = boto3.client('s3')

# 从 S3 读取提示
def get_prompt_from_s3(bucket: str, key: str) -> str:
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response['Body'].read().decode('utf-8')

# 使用 Claude 处理
prompt = get_prompt_from_s3('my-bucket', 'prompts/analysis.txt')
result = get_completion(prompt)

# 将结果保存到 S3
s3_client.put_object(
    Bucket='my-bucket',
    Key='results/output.txt',
    Body=result.encode('utf-8')
)
```

## AWS 集成功能

### 1. CloudWatch 监控

#### 启用 CloudWatch 日志

```python
import logging
import boto3

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 CloudWatch 日志客户端
logs_client = boto3.client('logs', region_name='us-east-1')

def log_to_cloudwatch(log_group: str, log_stream: str, message: str):
    try:
        logs_client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': message
                }
            ]
        )
    except Exception as e:
        logger.error(f"CloudWatch 日志错误: {e}")

# 使用
def monitored_completion(prompt: str):
    start_time = time.time()
    
    try:
        response = get_completion(prompt)
        duration = time.time() - start_time
        
        log_to_cloudwatch(
            '/aws/bedrock/claude',
            'completions',
            f"成功 | 耗时: {duration:.2f}s | Prompt: {prompt[:50]}..."
        )
        
        return response
    
    except Exception as e:
        log_to_cloudwatch(
            '/aws/bedrock/claude',
            'errors',
            f"错误: {str(e)} | Prompt: {prompt[:50]}..."
        )
        raise
```

#### 查看 CloudWatch 指标

```python
import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

def get_bedrock_metrics():
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/Bedrock',
        MetricName='Invocations',
        Dimensions=[
            {'Name': 'ModelId', 'Value': 'anthropic.claude-3-haiku-20240307-v1:0'}
        ],
        StartTime=datetime.now() - timedelta(hours=1),
        EndTime=datetime.now(),
        Period=300,
        Statistics=['Sum']
    )
    
    return response['Datapoints']

# 查看调用次数
metrics = get_bedrock_metrics()
for point in metrics:
    print(f"{point['Timestamp']}: {point['Sum']} 次调用")
```

### 2. IAM 权限管理

#### 创建最小权限策略

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockInvokeModel",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
      ]
    }
  ]
}
```

#### 使用临时凭证

```python
import boto3
from anthropic import AnthropicBedrock

# 使用 STS 获取临时凭证
sts = boto3.client('sts')
response = sts.assume_role(
    RoleArn='arn:aws:iam::123456789012:role/BedrockAccessRole',
    RoleSessionName='claude-session'
)

credentials = response['Credentials']

# 创建 session
session = boto3.Session(
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],
    region_name='us-east-1'
)

# 使用临时凭证
client = AnthropicBedrock(aws_session=session)
```

### 3. VPC 端点

在 VPC 中使用 Bedrock 以提高安全性：

```python
import boto3
from anthropic import AnthropicBedrock

# 配置 VPC 端点
config = boto3.session.Config(
    region_name='us-east-1',
    signature_version='v4',
    retries={
        'max_attempts': 3,
        'mode': 'standard'
    }
)

# 创建使用 VPC 端点的客户端
session = boto3.Session()
client = AnthropicBedrock(
    aws_session=session,
    aws_region='us-east-1'
)
```

### 4. 成本管理

#### 使用 AWS Cost Explorer

```python
import boto3
from datetime import datetime, timedelta

ce = boto3.client('ce', region_name='us-east-1')

def get_bedrock_costs():
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'End': datetime.now().strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        Filter={
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': ['Amazon Bedrock']
            }
        }
    )
    
    return response['ResultsByTime']

# 查看成本
costs = get_bedrock_costs()
for day in costs:
    amount = day['Total']['UnblendedCost']['Amount']
    print(f"{day['TimePeriod']['Start']}: ${float(amount):.2f}")
```

#### 设置成本预算

```python
import boto3

budgets = boto3.client('budgets', region_name='us-east-1')

def create_bedrock_budget(account_id: str, budget_limit: float):
    response = budgets.create_budget(
        AccountId=account_id,
        Budget={
            'BudgetName': 'BedrockMonthlyBudget',
            'BudgetLimit': {
                'Amount': str(budget_limit),
                'Unit': 'USD'
            },
            'TimeUnit': 'MONTHLY',
            'BudgetType': 'COST',
            'CostFilters': {
                'Service': ['Amazon Bedrock']
            }
        },
        NotificationsWithSubscribers=[
            {
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 80.0,
                    'ThresholdType': 'PERCENTAGE'
                },
                'Subscribers': [
                    {
                        'SubscriptionType': 'EMAIL',
                        'Address': 'your-email@example.com'
                    }
                ]
            }
        ]
    )
    return response
```

## 最佳实践

### 1. 区域选择

```python
import boto3
from anthropic import AnthropicBedrock

def get_optimal_region():
    """选择延迟最低的区域"""
    regions = ['us-east-1', 'us-west-2', 'ap-southeast-1']
    
    # 测试每个区域的延迟
    best_region = None
    min_latency = float('inf')
    
    for region in regions:
        try:
            start = time.time()
            client = AnthropicBedrock(aws_region=region)
            # 发送测试请求
            client.messages.create(
                model="anthropic.claude-3-haiku-20240307-v1:0",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            latency = time.time() - start
            
            if latency < min_latency:
                min_latency = latency
                best_region = region
        except:
            continue
    
    return best_region

# 使用最优区域
optimal_region = get_optimal_region()
client = AnthropicBedrock(aws_region=optimal_region)
```

### 2. 错误处理和重试

```python
import time
from anthropic import AnthropicBedrock, APIError
from botocore.exceptions import ClientError

def robust_completion(prompt: str, max_retries: int = 3):
    client = AnthropicBedrock(aws_region="us-east-1")
    
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="anthropic.claude-3-haiku-20240307-v1:0",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'ThrottlingException':
                wait_time = 2 ** attempt
                print(f"速率限制，等待 {wait_time}s...")
                time.sleep(wait_time)
            
            elif error_code == 'ModelNotReadyException':
                print("模型未就绪，等待...")
                time.sleep(5)
            
            elif error_code == 'AccessDeniedException':
                print("权限不足，请检查 IAM 权限")
                raise
            
            else:
                print(f"AWS 错误: {error_code}")
                raise
        
        except APIError as e:
            print(f"Anthropic API 错误: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                raise
    
    raise Exception("达到最大重试次数")
```

### 3. 批量处理优化

```python
import asyncio
from anthropic import AsyncAnthropicBedrock

async def process_batch(prompts: list, region: str = "us-east-1"):
    client = AsyncAnthropicBedrock(aws_region=region)
    
    async def process_one(prompt: str):
        message = await client.messages.create(
            model="anthropic.claude-3-haiku-20240307-v1:0",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    # 并发处理，但限制并发数
    semaphore = asyncio.Semaphore(5)  # 最多 5 个并发请求
    
    async def process_with_limit(prompt):
        async with semaphore:
            return await process_one(prompt)
    
    tasks = [process_with_limit(p) for p in prompts]
    return await asyncio.gather(*tasks)

# 使用
prompts = ["提示1", "提示2", "提示3", "提示4", "提示5"]
results = asyncio.run(process_batch(prompts))
```

### 4. 安全最佳实践

```python
import boto3
from anthropic import AnthropicBedrock

# 使用 AWS Secrets Manager 存储敏感配置
def get_secret(secret_name: str, region: str = "us-east-1"):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )
    
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# 使用 KMS 加密数据
def encrypt_data(data: str, key_id: str, region: str = "us-east-1"):
    kms = boto3.client('kms', region_name=region)
    response = kms.encrypt(
        KeyId=key_id,
        Plaintext=data.encode('utf-8')
    )
    return response['CiphertextBlob']

def decrypt_data(ciphertext: bytes, region: str = "us-east-1"):
    kms = boto3.client('kms', region_name=region)
    response = kms.decrypt(CiphertextBlob=ciphertext)
    return response['Plaintext'].decode('utf-8')
```

## 故障排除

### 常见问题

#### 1. 凭证配置错误

**错误信息**：
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**解决方案**：
- 运行 `aws configure` 配置凭证
- 检查环境变量 `AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`
- 验证 IAM 角色配置（如在 EC2 上）
- 检查 `~/.aws/credentials` 文件

#### 2. 区域不支持

**错误信息**：
```
botocore.exceptions.ClientError: An error occurred (ValidationException) when calling the InvokeModel operation
```

**解决方案**：
- 确认所选区域支持 Bedrock
- 切换到支持的区域（如 `us-east-1`）
- 查看 [Bedrock 区域文档](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html#bedrock-regions)

#### 3. 模型访问被拒绝

**错误信息**：
```
botocore.exceptions.ClientError: An error occurred (AccessDeniedException)
```

**解决方案**：
- 在 Bedrock 控制台请求模型访问权限
- 等待访问请求批准（通常几分钟）
- 检查 IAM 权限是否包含 `bedrock:InvokeModel`
- 验证模型 ID 是否正确

#### 4. 权限不足

**错误信息**：
```
botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the InvokeModel operation: User is not authorized
```

**解决方案**：
- 添加必要的 IAM 权限
- 使用管理员账户测试
- 检查资源 ARN 是否正确
- 验证 IAM 策略语法

#### 5. 速率限制

**错误信息**：
```
botocore.exceptions.ClientError: An error occurred (ThrottlingException)
```

**解决方案**：
- 实现指数退避重试
- 减少并发请求数
- 请求提高配额限制
- 使用批量处理优化

### 调试技巧

#### 启用 Boto3 调试日志

```python
import boto3
import logging

# 启用 Boto3 调试
boto3.set_stream_logger('', logging.DEBUG)

# 或只启用特定级别
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('botocore')
logger.setLevel(logging.DEBUG)
```

#### 检查 AWS 配置

```python
import boto3

# 检查当前凭证
session = boto3.Session()
credentials = session.get_credentials()

print(f"Access Key: {credentials.access_key[:10]}...")
print(f"Region: {session.region_name}")

# 检查可用区域
ec2 = boto3.client('ec2')
regions = ec2.describe_regions()
print("可用区域:", [r['RegionName'] for r in regions['Regions']])
```

## 从 Anthropic 1P 迁移

### 迁移步骤

#### 1. 更新依赖

```bash
# 安装额外的 AWS 依赖
pip install boto3 botocore awscli
```

#### 2. 更新导入语句

```python
# 之前
import anthropic
client = anthropic.Anthropic(api_key=API_KEY)

# 之后
from anthropic import AnthropicBedrock
client = AnthropicBedrock(aws_region=AWS_REGION)
```

#### 3. 更新模型名称

```python
# 之前
model = "claude-3-haiku-20240307"

# 之后
model = "anthropic.claude-3-haiku-20240307-v1:0"
```

#### 4. 配置 AWS 凭证

```bash
aws configure
```

#### 5. 测试迁移

```python
# 创建迁移测试脚本
def test_migration():
    from anthropic import AnthropicBedrock
    
    client = AnthropicBedrock(aws_region="us-east-1")
    
    message = client.messages.create(
        model="anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    print("迁移成功！")
    print(message.content[0].text)

test_migration()
```

### 迁移检查清单

- [ ] 安装 AWS 依赖包
- [ ] 配置 AWS 凭证
- [ ] 更新导入语句
- [ ] 更新模型 ID
- [ ] 更新客户端初始化
- [ ] 测试基本功能
- [ ] 更新错误处理
- [ ] 配置 CloudWatch 监控
- [ ] 设置 IAM 权限
- [ ] 更新文档和注释

## 相关资源

### AWS 官方文档

- [Amazon Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
- [Bedrock API 参考](https://docs.aws.amazon.com/bedrock/latest/APIReference/)
- [Claude on Bedrock](https://docs.anthropic.com/claude/reference/claude-on-amazon-bedrock)
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### Anthropic 文档

- [Anthropic SDK 文档](https://github.com/anthropics/anthropic-sdk-python)
- [Bedrock 集成指南](https://docs.anthropic.com/claude/reference/claude-on-amazon-bedrock)

### 项目文档

- [版本对比](./comparison.md) - 了解不同版本的差异
- [Anthropic 1P 版本](./anthropic-1p.md) - 原生 API 版本
- [Bedrock Boto3 版本](./bedrock-boto3.md) - AWS 原生版本
- [安装指南](../getting-started/installation.md) - 详细安装说明

## 下一步

1. **开始学习**：打开 `00_Tutorial_How-To.ipynb` 开始教程
2. **配置监控**：设置 CloudWatch 日志和指标
3. **优化成本**：配置预算和成本告警
4. **增强安全**：配置 IAM 权限和 VPC 端点

如需了解其他版本，请参考：
- [Anthropic 1P 版本文档](./anthropic-1p.md)
- [Bedrock Boto3 版本文档](./bedrock-boto3.md)
