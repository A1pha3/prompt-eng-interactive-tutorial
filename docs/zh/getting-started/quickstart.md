# 快速开始

## 概述

本指南将帮助您在 5 分钟内快速上手 Anthropic Claude 提示工程交互式教程。我们将通过一个简单的示例，让您体验如何与 Claude 进行交互。

> **版本说明**：本快速开始指南以 🟦 Anthropic 1P 版本为例。如果您使用其他版本，请参考对应的版本文档：
> - [Bedrock Anthropic SDK 快速开始](../versions/bedrock-anthropic.md#安装指南)
> - [Bedrock Boto3 快速开始](../versions/bedrock-boto3.md#安装指南)
> - [版本对比](../versions/comparison.md)

## 目标读者

本指南适用于：
- 已完成安装的新用户
- 希望快速体验教程的学习者
- 想要验证环境配置是否正确的用户

## 前置条件

在开始之前，请确保您已完成以下步骤：

1. ✅ 安装了 Python 3.7 或更高版本
2. ✅ 安装了 Jupyter Notebook 或 JupyterLab
3. ✅ 安装了 Anthropic SDK（`pip install anthropic`）
4. ✅ 获取了 Anthropic API 密钥

如果尚未完成安装，请先阅读[安装指南](installation.md)。

## 5 分钟快速上手

### 步骤 1：启动 Jupyter Notebook（30 秒）

打开终端，导航到项目目录，启动 Jupyter：

```bash
# 进入项目目录
cd <repository-name>

# 激活虚拟环境（如果使用）
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 启动 Jupyter Notebook
jupyter notebook
```

浏览器将自动打开 Jupyter 界面。

### 步骤 2：打开教程入门文件（30 秒）

在 Jupyter 文件浏览器中：

1. 导航到 `Anthropic 1P` 目录
2. 点击打开 `00_Tutorial_How-To.ipynb`

### 步骤 3：配置 API 密钥（1 分钟）

找到包含以下代码的单元格，将 `"your_api_key_here"` 替换为您的实际 API 密钥：

```python
API_KEY = "your_api_key_here"  # 替换为您的 API 密钥
MODEL_NAME = "claude-3-haiku-20240307"

# 存储变量以便在其他 Notebook 中使用
%store API_KEY
%store MODEL_NAME
```

按 `Shift + Enter` 运行此单元格。

### 步骤 4：运行第一个示例（2 分钟）

继续运行下一个单元格，设置 API 客户端：

```python
import anthropic

client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt: str):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=[
          {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text
```

按 `Shift + Enter` 运行。

### 步骤 5：与 Claude 对话（1 分钟）

运行示例提示词单元格：

```python
# 提示词
prompt = "Hello, Claude!"

# 获取 Claude 的响应
print(get_completion(prompt))
```

按 `Shift + Enter` 运行。您应该会看到 Claude 的友好回复！

🎉 **恭喜！** 您已成功完成第一次与 Claude 的交互！

## 第一个完整示例

让我们尝试一个更有意义的示例，体验提示工程的基本概念。

### 示例：让 Claude 写一首诗

```python
# 简单的提示词
prompt = "请用中文写一首关于春天的五言绝句。"

print(get_completion(prompt))
```

**预期输出**（示例）：
```
春风拂柳绿，
细雨润花红。
燕子归来早，
人间四月中。
```

### 示例：使用角色提示

```python
# 使用角色提示的提示词
prompt = """你是一位经验丰富的 Python 程序员。
请解释什么是列表推导式，并给出一个简单的例子。"""

print(get_completion(prompt))
```

**预期输出**（示例）：
```
列表推导式（List Comprehension）是 Python 中一种简洁优雅的创建列表的方式。
它允许你在一行代码中完成循环和条件判断。

基本语法：
[表达式 for 元素 in 可迭代对象 if 条件]

简单例子：
# 创建一个包含 1-10 平方数的列表
squares = [x**2 for x in range(1, 11)]
# 结果：[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 筛选偶数
evens = [x for x in range(1, 11) if x % 2 == 0]
# 结果：[2, 4, 6, 8, 10]
```

### 示例：格式化输出

```python
# 要求特定格式输出的提示词
prompt = """请列出三种常见的排序算法，使用以下格式：

算法名称：[名称]
时间复杂度：[复杂度]
简要说明：[一句话说明]
"""

print(get_completion(prompt))
```

## 基本工作流程

完成快速开始后，建议按以下流程继续学习：

```
┌─────────────────────────────────────────────────────────────┐
│                      学习路径                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 基础篇（第 1-3 章）                                      │
│     ├── 基本提示词结构                                       │
│     ├── 清晰直接的表达                                       │
│     └── 角色分配                                            │
│                                                             │
│  2. 进阶篇（第 4-7 章）                                      │
│     ├── 分离数据与指令                                       │
│     ├── 格式化输出                                          │
│     ├── 逐步思考                                            │
│     └── 使用示例                                            │
│                                                             │
│  3. 高级篇（第 8-9 章）                                      │
│     ├── 避免幻觉                                            │
│     └── 构建复杂提示词                                       │
│                                                             │
│  4. 附录                                                    │
│     ├── 提示词链接                                          │
│     ├── 工具使用                                            │
│     └── 搜索与检索                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 常用快捷键

在 Jupyter Notebook 中，以下快捷键可以提高您的效率：

| 快捷键 | 功能 |
|--------|------|
| `Shift + Enter` | 运行当前单元格并移动到下一个 |
| `Ctrl + Enter` | 运行当前单元格但不移动 |
| `Esc` | 进入命令模式 |
| `Enter` | 进入编辑模式 |
| `A` | 在上方插入新单元格（命令模式） |
| `B` | 在下方插入新单元格（命令模式） |
| `DD` | 删除当前单元格（命令模式） |
| `M` | 将单元格转换为 Markdown（命令模式） |
| `Y` | 将单元格转换为代码（命令模式） |

## 常见问题

### 问题 1：API 密钥无效

**症状**：
```
anthropic.AuthenticationError: Invalid API Key
```

**解决方案**：
- 检查 API 密钥是否正确复制（无多余空格）
- 确认 API 密钥未过期
- 访问 [Anthropic Console](https://console.anthropic.com/) 验证密钥状态

### 问题 2：模块未找到

**症状**：
```
ModuleNotFoundError: No module named 'anthropic'
```

**解决方案**：
```bash
pip install anthropic
```

### 问题 3：响应超时

**症状**：
```
anthropic.APITimeoutError: Request timed out
```

**解决方案**：
- 检查网络连接
- 稍后重试
- 如果问题持续，可能是 API 服务暂时不可用

### 问题 4：配额超限

**症状**：
```
anthropic.RateLimitError: Rate limit exceeded
```

**解决方案**：
- 等待几分钟后重试
- 检查您的 API 使用配额
- 考虑升级您的 API 计划

## 实验练习场

现在您已经了解了基本操作，可以在下面的代码框中自由实验：

```python
# 在这里尝试您自己的提示词
my_prompt = """
[在这里输入您的提示词]
"""

print(get_completion(my_prompt))
```

### 练习建议

1. **尝试不同的问题类型**
   - 知识问答
   - 创意写作
   - 代码生成
   - 文本摘要

2. **实验提示词技巧**
   - 添加角色设定
   - 指定输出格式
   - 提供示例
   - 分步骤指导

3. **观察响应差异**
   - 比较简单提示词和详细提示词的效果
   - 注意 Claude 如何理解不同的指令

## 下一步

完成快速开始后，建议您：

1. **继续学习第一章**
   - 打开 `01_Basic_Prompt_Structure.ipynb`
   - 深入了解提示词的基本结构

2. **阅读完整使用手册**
   - 查看[使用手册](../user-guide/user-guide.md)获取详细说明

3. **探索示例集合**
   - 查看[示例集合](../user-guide/examples.md)获取更多实用示例

4. **了解不同版本**
   - 如果您使用 AWS，查看[版本对比](../versions/comparison.md)

## 另请参阅

**入门文档**：
- [安装指南](installation.md) - 如需重新配置环境
- [配置说明](../user-guide/configuration.md) - 高级配置选项

**学习资源**：
- [完整使用手册](../user-guide/user-guide.md) - 系统学习所有章节
- [示例集合](../user-guide/examples.md) - 实用示例和最佳实践
- [API 参考](../user-guide/api-reference.md) - API 详细文档

**版本相关**：
- [版本对比](../versions/comparison.md) - 选择适合的版本
- [Anthropic 1P 版本](../versions/anthropic-1p.md) - 本快速开始使用的版本

**问题解决**：
- [问题排查](../advanced/troubleshooting.md) - 解决常见问题
- [常见问题](../advanced/faq.md) - FAQ

## 获取帮助

如果遇到问题：
1. 查看[问题排查文档](../advanced/troubleshooting.md)
2. 查看[常见问题](../advanced/faq.md)
3. 在项目仓库提交 Issue

---

**文档导航**：
- **上一步**: [安装指南](installation.md)
- **下一步**: [完整使用手册](../user-guide/user-guide.md)
- **相关主题**: [示例集合](../user-guide/examples.md) | [API 参考](../user-guide/api-reference.md)
