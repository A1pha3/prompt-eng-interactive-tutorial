# 示例集合

## 目录

- [概述](#概述)
- [基础示例](#基础示例)
- [文本处理](#文本处理)
- [数据分析](#数据分析)
- [代码相关](#代码相关)
- [创意写作](#创意写作)
- [对话系统](#对话系统)
- [实用工具](#实用工具)

---

## 概述

本文档收集了从教程 Notebook 中提取的实用示例，按使用场景分类组织。每个示例都包含完整的代码、说明和预期输出。

### 使用说明

1. 确保已正确配置 API 密钥
2. 复制示例代码到您的环境
3. 根据需要修改参数
4. 运行并观察输出

### 前置准备

```python
import anthropic
import os

# 初始化客户端
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# 辅助函数
def get_completion(prompt: str, system_prompt: str = "") -> str:
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.0,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

---

## 基础示例

### 示例 1：简单问答

**场景**：基本的问答交互

**代码**：
```python
prompt = "什么是机器学习？"
response = get_completion(prompt)
print(response)
```

**预期输出**：
```
机器学习是人工智能的一个分支，它使计算机系统能够从数据中学习和改进，
而无需明确编程。机器学习算法通过分析大量数据来识别模式，并使用这些
模式来做出预测或决策...
```

### 示例 2：使用系统提示

**场景**：通过系统提示设定角色

**代码**：
```python
system_prompt = "你是一位幽默风趣的老师，善于用简单有趣的方式解释复杂概念。"
prompt = "什么是量子纠缠？"

response = get_completion(prompt, system_prompt)
print(response)
```

**预期输出**：
```
想象一下，你和你的好朋友有一对神奇的骰子。不管你们相隔多远，
当你掷出6点时，你朋友的骰子也会神奇地显示6点！这就像量子纠缠——
两个粒子之间有一种神秘的联系，改变其中一个，另一个会立即"知道"...
```

### 示例 3：多轮对话

**场景**：维护对话上下文

**代码**：
```python
messages = [
    {"role": "user", "content": "我想学习 Python"},
    {"role": "assistant", "content": "太好了！Python 是一门很适合初学者的语言。你想从哪里开始？"},
    {"role": "user", "content": "从基础语法开始"}
]

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=messages
)

print(message.content[0].text)
```

**预期输出**：
```
好的！让我们从 Python 的基础语法开始：

1. 变量和数据类型
   - 数字：整数和浮点数
   - 字符串：文本数据
   - 布尔值：True 和 False

2. 基本操作
   - 算术运算：+, -, *, /
   - 比较运算：==, !=, <, >
...
```

---

## 文本处理

### 示例 4：文本总结

**场景**：总结长文本

**代码**：
```python
text = """
人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。
这包括学习、推理、问题解决、感知和语言理解。AI 技术已经在许多领域得到应用，
包括医疗诊断、自动驾驶汽车、语音识别和推荐系统。机器学习是 AI 的一个子集，
它使系统能够从数据中学习而无需明确编程。深度学习则是机器学习的一个分支，
使用神经网络来处理复杂的模式识别任务。
"""

prompt = f"""请总结以下文本，用3-4句话概括主要内容：

<text>
{text}
</text>"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
人工智能是计算机科学的一个分支，旨在创建能执行类人智能任务的系统。
AI 已广泛应用于医疗、自动驾驶、语音识别等领域。机器学习是 AI 的子集，
使系统能从数据中学习，而深度学习则使用神经网络处理复杂的模式识别。
```

### 示例 5：情感分析

**场景**：分析文本情感

**代码**：
```python
reviews = [
    "这个产品太棒了！质量很好，物超所值。",
    "还可以，有优点也有缺点。",
    "非常失望，质量很差，不推荐购买。"
]

for review in reviews:
    prompt = f"""分析以下评论的情感（正面/负面/中性）：

评论："{review}"

输出格式：
情感：[正面/负面/中性]
置信度：[高/中/低]
理由：[简短说明]"""

    response = get_completion(prompt)
    print(f"评论：{review}")
    print(response)
    print("-" * 50)
```

**预期输出**：
```
评论：这个产品太棒了！质量很好，物超所值。
情感：正面
置信度：高
理由：使用了"太棒了"、"很好"、"物超所值"等明显的正面词汇
--------------------------------------------------
评论：还可以，有优点也有缺点。
情感：中性
置信度：高
理由：明确表示"有优点也有缺点"，态度中立
--------------------------------------------------
评论：非常失望，质量很差，不推荐购买。
情感：负面
置信度：高
理由：包含"失望"、"很差"、"不推荐"等明显的负面表达
--------------------------------------------------
```

### 示例 6：文本分类

**场景**：将文本分类到预定义类别

**代码**：
```python
prompt = """将以下客户反馈分类到相应类别：

类别：产品质量、配送服务、客户服务、价格、其他

反馈："快递小哥态度很好，送货很及时。"

输出格式：
类别：[类别名称]
关键词：[识别出的关键词]"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
类别：配送服务
关键词：快递、送货、及时
```

---

## 数据分析

### 示例 7：数据提取

**场景**：从非结构化文本中提取结构化信息

**代码**：
```python
text = "张三是一名软件工程师，在北京工作，年龄28岁，擅长Python和JavaScript。"

prompt = f"""从以下文本中提取信息，以JSON格式输出：

<text>
{text}
</text>

输出格式：
{{
  "姓名": "...",
  "职业": "...",
  "地点": "...",
  "年龄": ...,
  "技能": [...]
}}"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```json
{
  "姓名": "张三",
  "职业": "软件工程师",
  "地点": "北京",
  "年龄": 28,
  "技能": ["Python", "JavaScript"]
}
```

### 示例 8：数据转换

**场景**：将数据从一种格式转换为另一种格式

**代码**：
```python
csv_data = """姓名,年龄,城市
张三,25,北京
李四,30,上海
王五,28,深圳"""

prompt = f"""将以下CSV数据转换为JSON数组：

<csv>
{csv_data}
</csv>

输出格式：
[
  {{"name": "...", "age": ..., "city": "..."}},
  ...
]"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```json
[
  {"name": "张三", "age": 25, "city": "北京"},
  {"name": "李四", "age": 30, "city": "上海"},
  {"name": "王五", "age": 28, "city": "深圳"}
]
```

### 示例 9：数据验证

**场景**：验证数据的正确性

**代码**：
```python
data = {
    "email": "user@example.com",
    "phone": "13800138000",
    "age": 25,
    "website": "https://example.com"
}

prompt = f"""验证以下数据的有效性：

<data>
{data}
</data>

检查项：
1. email 格式是否正确
2. phone 是否为有效的中国手机号
3. age 是否在合理范围（0-150）
4. website 是否为有效URL

输出格式：
字段：[字段名]
有效性：[有效/无效]
说明：[如果无效，说明原因]"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
email：有效
说明：格式正确，包含@和域名

phone：有效
说明：符合中国手机号格式（13开头，11位数字）

age：有效
说明：在合理范围内（0-150）

website：有效
说明：格式正确，使用https协议
```

---

## 代码相关

### 示例 10：代码生成

**场景**：根据需求生成代码

**代码**：
```python
prompt = """编写一个 Python 函数，实现以下功能：
- 函数名：calculate_average
- 参数：一个数字列表
- 返回：列表的平均值
- 处理空列表的情况

请包含文档字符串和示例用法。"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```python
def calculate_average(numbers):
    """
    计算数字列表的平均值
    
    参数:
        numbers (list): 数字列表
    
    返回:
        float: 平均值，如果列表为空则返回 0
    
    示例:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
        >>> calculate_average([])
        0
    """
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

# 使用示例
print(calculate_average([1, 2, 3, 4, 5]))  # 输出: 3.0
print(calculate_average([]))  # 输出: 0
```

### 示例 11：代码解释

**场景**：解释代码的功能

**代码**：
```python
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

prompt = f"""解释以下代码的功能：

<code>
{code}
</code>

请说明：
1. 函数的作用
2. 算法原理
3. 时间复杂度
4. 潜在问题"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
1. 函数的作用：
   计算斐波那契数列的第 n 项

2. 算法原理：
   使用递归方法，每次调用计算前两项的和
   基础情况：n <= 1 时直接返回 n

3. 时间复杂度：
   O(2^n) - 指数级复杂度，效率很低

4. 潜在问题：
   - 大量重复计算，效率低下
   - 可能导致栈溢出
   - 建议使用动态规划或迭代方法优化
```

### 示例 12：代码审查

**场景**：审查代码并提供改进建议

**代码**：
```python
code_to_review = """
def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            result.append(data[i] * 2)
    return result
"""

prompt = f"""审查以下代码并提供改进建议：

<code>
{code_to_review}
</code>

请从以下角度评估：
1. 代码风格
2. 性能
3. 可读性
4. 最佳实践"""

response = get_completion(prompt)
print(response)
```

---

## 创意写作

### 示例 13：故事创作

**场景**：创作短篇故事

**代码**：
```python
prompt = """写一个关于时间旅行的短篇科幻故事，要求：
- 长度：300字左右
- 包含一个意外的转折
- 结局引人深思"""

response = get_completion(prompt)
print(response)
```

### 示例 14：诗歌创作

**场景**：创作诗歌

**代码**：
```python
system_prompt = "你是一位现代诗人，擅长创作富有意境的诗歌。"
prompt = "以'城市的夜晚'为主题，创作一首现代诗。"

response = get_completion(prompt, system_prompt)
print(response)
```

### 示例 15：文案撰写

**场景**：撰写营销文案

**代码**：
```python
product_info = {
    "名称": "智能手表",
    "特点": ["健康监测", "长续航", "防水"],
    "目标用户": "运动爱好者"
}

prompt = f"""为以下产品撰写营销文案：

产品信息：
{product_info}

要求：
- 标题吸引人
- 突出产品优势
- 包含行动号召
- 长度：100字左右"""

response = get_completion(prompt)
print(response)
```

---

## 对话系统

### 示例 16：客服机器人

**场景**：构建客服对话系统

**代码**：
```python
system_prompt = """你是一位友好专业的客服代表。
在回答时：
- 保持礼貌和耐心
- 提供清晰的解决方案
- 如果无法解决，引导至人工客服"""

conversation = [
    {"role": "user", "content": "我的订单还没收到"}
]

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    system=system_prompt,
    messages=conversation
)

print(message.content[0].text)
```

### 示例 17：教学助手

**场景**：构建教学对话系统

**代码**：
```python
system_prompt = """你是一位耐心的编程导师。
教学风格：
- 循序渐进
- 使用简单例子
- 鼓励学生思考
- 及时给予反馈"""

prompt = "我不理解什么是变量，能解释一下吗？"

response = get_completion(prompt, system_prompt)
print(response)
```

---

## 实用工具

### 示例 18：翻译

**场景**：多语言翻译

**代码**：
```python
text = "Hello, how are you today?"

prompt = f"""将以下文本翻译成中文：

<text>
{text}
</text>

要求：
- 自然流畅
- 符合中文表达习惯"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
你好，你今天怎么样？
```

### 示例 19：邮件撰写

**场景**：自动生成邮件

**代码**：
```python
context = {
    "收件人": "张经理",
    "目的": "请假",
    "日期": "2024年1月15日至17日",
    "原因": "家庭事务"
}

prompt = f"""撰写一封正式的请假邮件：

上下文：
{context}

要求：
- 语气正式礼貌
- 结构清晰
- 包含必要信息"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
尊敬的张经理：

您好！

我因家庭事务需要处理，特此申请于2024年1月15日至17日请假三天。
在此期间，我已安排好工作交接，确保不影响团队进度。

恳请批准，谢谢！

此致
敬礼

[您的姓名]
[日期]
```

### 示例 20：会议纪要生成

**场景**：从会议记录生成纪要

**代码**：
```python
meeting_notes = """
参会人员：张三、李四、王五
时间：2024-01-10 14:00
讨论内容：
- 张三：项目进度正常，预计下周完成开发
- 李四：测试环境已搭建完成
- 王五：需要增加两名开发人员
决定：批准增加人员，预算由财务部审核
"""

prompt = f"""根据以下会议记录生成正式的会议纪要：

<notes>
{meeting_notes}
</notes>

格式要求：
1. 会议基本信息
2. 讨论要点
3. 决议事项
4. 后续行动"""

response = get_completion(prompt)
print(response)
```

### 示例 21：简历优化

**场景**：优化简历内容

**代码**：
```python
original = "负责开发和维护公司网站"

prompt = f"""优化以下简历描述，使其更专业和具体：

原文：{original}

要求：
- 使用动作动词
- 量化成果
- 突出技能
- 简洁有力"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
主导公司官网的全栈开发与运维，使用 React 和 Node.js 技术栈，
成功提升网站性能 40%，日均访问量增长至 10 万+，
并实现 99.9% 的系统可用性
```

### 示例 22：SQL 查询生成

**场景**：将自然语言转换为 SQL

**代码**：
```python
prompt = """将以下需求转换为 SQL 查询：

需求：查找所有在北京工作、年龄在 25-35 岁之间、
职位为软件工程师的员工，按工资降序排列，显示前 10 名

表结构：
employees (id, name, age, city, position, salary)

只输出 SQL 语句。"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```sql
SELECT *
FROM employees
WHERE city = '北京'
  AND age BETWEEN 25 AND 35
  AND position = '软件工程师'
ORDER BY salary DESC
LIMIT 10;
```

### 示例 23：正则表达式生成

**场景**：生成正则表达式

**代码**：
```python
prompt = """生成一个正则表达式，用于验证中国手机号：

要求：
- 11位数字
- 以1开头
- 第二位是3-9

请提供：
1. 正则表达式
2. Python 使用示例
3. 测试用例"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```python
# 正则表达式
pattern = r'^1[3-9]\d{9}$'

# Python 使用示例
import re

def validate_phone(phone):
    return bool(re.match(pattern, phone))

# 测试用例
print(validate_phone('13800138000'))  # True
print(validate_phone('12345678901'))  # False
print(validate_phone('1380013800'))   # False
```

### 示例 24：错误消息改进

**场景**：将技术错误转换为用户友好的消息

**代码**：
```python
error = "NullPointerException at line 42 in UserService.java"

prompt = f"""将以下技术错误转换为用户友好的错误消息：

技术错误：{error}

要求：
- 用户能理解
- 提供解决建议
- 保持简洁"""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
抱歉，系统遇到了一个问题。请稍后重试，
如果问题持续存在，请联系客服支持。
```

---

## 高级示例

### 示例 25：思维链推理

**场景**：复杂问题的逐步推理

**代码**：
```python
prompt = """解决以下问题，请展示完整的推理过程：

问题：一个水池有两个进水管和一个出水管。
进水管A每小时注水10升，进水管B每小时注水15升，
出水管每小时排水8升。
如果同时打开三个管道，多久能注满100升的水池？

请逐步计算。"""

response = get_completion(prompt)
print(response)
```

### 示例 26：少样本学习

**场景**：通过示例学习任务

**代码**：
```python
prompt = """将产品评论分类为：功能、价格、质量、服务

示例1：
评论："这个功能很实用，解决了我的问题。"
分类：功能

示例2：
评论："价格有点贵，但质量不错。"
分类：价格, 质量

现在分类：
评论："客服态度很好，问题解决得很快。"
分类："""

response = get_completion(prompt)
print(response)
```

**预期输出**：
```
服务
```

### 示例 27：结构化输出

**场景**：生成复杂的结构化数据

**代码**：
```python
prompt = """分析以下产品评论，输出结构化的JSON：

评论："这款手机拍照效果很棒，但是电池续航一般。
价格有点贵，不过整体还是值得购买的。"

输出格式：
{
  "overall_sentiment": "正面/负面/中性",
  "aspects": [
    {
      "aspect": "方面名称",
      "sentiment": "正面/负面/中性",
      "keywords": ["关键词"]
    }
  ],
  "recommendation": "推荐/不推荐/中立"
}"""

response = get_completion(prompt)
print(response)
```

---

## 使用技巧

### 技巧 1：组合多个示例

将多个技术组合使用以获得更好的结果：

```python
system_prompt = "你是一位数据分析专家。"  # 角色提示

prompt = """<data>
销售数据...
</data>

参考示例：
[示例...]

请逐步分析：
1. 识别趋势
2. 发现异常
3. 提供建议"""  # XML标签 + 少样本 + 思维链

response = get_completion(prompt, system_prompt)
```

### 技巧 2：迭代优化

从简单开始，逐步优化：

```python
# 版本1：基础
prompt_v1 = "总结这篇文章"

# 版本2：添加要求
prompt_v2 = "用3句话总结这篇文章的主要内容"

# 版本3：添加格式
prompt_v3 = """总结这篇文章：
1. 主题（1句话）
2. 关键点（2-3点）
3. 结论（1句话）"""
```

### 技巧 3：错误处理

在生产环境中添加错误处理：

```python
def safe_completion(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return get_completion(prompt)
        except Exception as e:
            if attempt == max_retries - 1:
                return f"错误：{str(e)}"
            time.sleep(2 ** attempt)
```

---

## 相关资源

- [完整使用手册](user-guide.md)
- [API 参考](api-reference.md)
- [配置说明](configuration.md)
- [最佳实践](../advanced/performance.md)

---

**文档版本**：1.0  
**最后更新**：2024-01  
**示例总数**：27 个

