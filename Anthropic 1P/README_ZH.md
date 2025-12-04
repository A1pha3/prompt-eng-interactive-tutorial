# 欢迎使用 Anthropic 提示工程交互式教程 - Anthropic 1P 版本

🟦 **版本标识**：Anthropic 1P（第一方 API）

## 课程简介和目标

本课程旨在为您提供全面的分步指导，帮助您使用 Anthropic 官方 API 在 Claude 中进行最佳提示工程。

**完成本课程后，您将能够**：
- 掌握良好提示的基本结构
- 识别常见的失败模式并学习"二八法则"技术来解决它们
- 理解 Claude 的优势和局限性
- 从零开始为常见用例构建强大的提示

## 版本特点

### ✨ 核心优势

- **简单直接**：最少的配置步骤，快速上手
- **最新功能**：第一时间获得新模型和功能
- **独立部署**：不依赖云服务提供商
- **透明定价**：按 token 使用量计费，清晰的定价结构

### 🎯 适用场景

- 🎓 学习和教育：最适合学习提示工程的版本
- 🔬 研究和实验：快速测试新想法和方法
- 🚀 原型开发：快速构建概念验证
- 💻 个人项目：小规模应用和工具开发

## 快速开始

### 前置条件

1. **Anthropic API 密钥**
   - 访问 [Anthropic Console](https://console.anthropic.com/)
   - 注册或登录您的账户
   - 创建新的 API 密钥
   - 安全保存您的密钥

2. **Python 环境**
   - Python 3.7 或更高版本
   - Jupyter Notebook

### 5 分钟快速安装

#### 1. 克隆仓库
```bash
git clone https://github.com/anthropics/prompt-eng-interactive-tutorial.git
cd "prompt-eng-interactive-tutorial/Anthropic 1P"
```

#### 2. 安装依赖
```bash
pip install anthropic
```

#### 3. 启动 Jupyter Notebook
```bash
jupyter notebook
```

#### 4. 配置 API 密钥
打开 `00_Tutorial_How-To.ipynb`，在相应单元格中设置您的 API 密钥：

```python
API_KEY = "your_api_key_here"  # 替换为您的实际 API 密钥
MODEL_NAME = "claude-3-haiku-20240307"

# 存储变量供其他 notebook 使用
%store API_KEY
%store MODEL_NAME
```

⚠️ **安全提示**：不要将 API 密钥提交到版本控制系统或在公共场合分享。

#### 5. 验证安装
运行测试代码：

```python
import anthropic

client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt: str):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# 测试
print(get_completion("Hello, Claude!"))
```

如果看到 Claude 的回复，说明配置成功！🎉

## 课程结构和内容

本课程为您提供了许多练习编写和调试提示的机会。课程分为 **9 个章节及配套练习**，以及包含更多高级方法的附录。建议您**按章节顺序学习**。

**每节课底部都有"示例练习场"区域**，您可以自由实验课程中的示例，亲自观察更改提示如何改变 Claude 的响应。还有一个[答案键](https://docs.google.com/spreadsheets/d/1jIxjzUWG-6xBVIa2ay6yDpLyeuOh_hR_ZB75a47KX_E/edit?usp=sharing)可供参考。

注意：本教程使用我们最小、最快、最经济的模型 Claude 3 Haiku。Anthropic 还有[两个其他模型](https://docs.anthropic.com/claude/docs/models-overview)：Claude 3 Sonnet 和 Claude 3 Opus，它们比 Haiku 更智能，其中 Opus 是最智能的。

准备好后，请前往 `01_Basic_Prompt_Structure.ipynb` 开始学习。

## 目录

每章包含一节课和一组练习。

### 初级
- **第 1 章**：基本提示结构
  - 📓 `01_Basic_Prompt_Structure.ipynb`

- **第 2 章**：清晰直接的表达
  - 📓 `02_Being_Clear_and_Direct.ipynb`

- **第 3 章**：角色分配（角色提示）
  - 📓 `03_Assigning_Roles_Role_Prompting.ipynb`

### 中级
- **第 4 章**：分离数据和指令
  - 📓 `04_Separating_Data_and_Instructions.ipynb`

- **第 5 章**：格式化输出与为 Claude 代言
  - 📓 `05_Formatting_Output_and_Speaking_for_Claude.ipynb`

- **第 6 章**：预知（逐步思考）
  - 📓 `06_Precognition_Thinking_Step_by_Step.ipynb`

- **第 7 章**：使用示例（少样本提示）
  - 📓 `07_Using_Examples_Few-Shot_Prompting.ipynb`

### 高级
- **第 8 章**：避免幻觉
  - 📓 `08_Avoiding_Hallucinations.ipynb`

- **第 9 章**：从零开始构建复杂提示
  - 📓 `09_Complex_Prompts_from_Scratch.ipynb`

### 附录：超越标准提示
- **附录 10.1**：提示链接
  - 📓 `10.1_Appendix_Chaining Prompts.ipynb`

- **附录 10.2**：工具使用
  - 📓 `10.2_Appendix_Tool Use.ipynb`

- **附录 10.3**：搜索与检索
  - 📓 `10.3_Appendix_Search & Retrieval.ipynb`

## 使用技巧

### 推荐学习路径

1. **按顺序学习**：从第 1 章开始，逐章完成
2. **动手实践**：在示例练习场中尝试修改提示
3. **完成练习**：每章的练习帮助巩固知识
4. **参考答案**：遇到困难时查看答案键
5. **实验探索**：尝试将学到的技术应用到自己的用例

### 使用环境变量（推荐）

为了更安全地管理 API 密钥，推荐使用环境变量：

**Linux/macOS**：
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

**Windows (PowerShell)**：
```powershell
$env:ANTHROPIC_API_KEY="your_api_key_here"
```

然后在代码中：
```python
import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
```

### 模型选择

```python
# Claude 3 系列
MODEL_NAME = "claude-3-opus-20240229"    # 最强大
MODEL_NAME = "claude-3-sonnet-20240229"  # 平衡性能
MODEL_NAME = "claude-3-haiku-20240307"   # 最快速（教程默认）
```

**建议**：
- **学习教程**：使用 Haiku（快速且经济）
- **生产应用**：根据需求选择 Sonnet 或 Opus
- **成本优化**：Haiku < Sonnet < Opus

## 相关资源

### 官方文档
- [Anthropic API 文档](https://docs.anthropic.com/)
- [Python SDK 文档](https://github.com/anthropics/anthropic-sdk-python)
- [Claude 模型文档](https://docs.anthropic.com/claude/docs/models-overview)
- [定价信息](https://www.anthropic.com/pricing)

### 项目文档
- [中文主文档](../README.md)
- [Anthropic 1P 版本详细文档](../docs/zh/versions/anthropic-1p.md)
- [安装指南](../docs/zh/getting-started/installation.md)
- [快速开始](../docs/zh/getting-started/quickstart.md)
- [完整使用手册](../docs/zh/user-guide/user-guide.md)
- [API 参考](../docs/zh/user-guide/api-reference.md)
- [示例集合](../docs/zh/user-guide/examples.md)

### 版本对比
- [版本对比文档](../docs/zh/versions/comparison.md) - 了解不同版本的差异
- [Bedrock Anthropic SDK 版本](../docs/zh/versions/bedrock-anthropic.md)
- [Bedrock Boto3 版本](../docs/zh/versions/bedrock-boto3.md)

### 社区资源
- [Anthropic Discord](https://discord.gg/anthropic)
- [GitHub Issues](https://github.com/anthropics/anthropic-sdk-python/issues)
- [示例代码库](https://github.com/anthropics/anthropic-cookbook)

## 常见问题

### Q: 如何获取 API 密钥？

A: 访问 [Anthropic Console](https://console.anthropic.com/)，注册或登录账户，在 API Keys 页面创建新密钥。

### Q: API 如何计费？

A: 按输入和输出 token 分别计费。不同模型有不同的定价。查看最新定价：[Anthropic Pricing](https://www.anthropic.com/pricing)

### Q: 遇到 API 密钥无效错误怎么办？

A: 检查密钥是否正确复制，确认密钥未过期或被撤销，在 Anthropic Console 中验证密钥状态。

### Q: 如何控制成本？

A: 使用 Haiku 模型（最经济），限制 `max_tokens` 参数，实现缓存机制，监控 token 使用量。

### Q: 可以在生产环境使用吗？

A: 可以。Anthropic 1P API 适合生产环境。对于企业级需求，可以考虑 Bedrock 版本以获得 AWS 企业功能。

### Q: 如何迁移到 Bedrock？

A: 查看[版本对比文档](../docs/zh/versions/comparison.md)中的迁移指南，了解详细的迁移步骤和代码变更。

## 故障排除

### 常见错误

**1. 连接超时**
```python
# 增加超时时间
client = anthropic.Anthropic(
    api_key=API_KEY,
    timeout=60.0
)
```

**2. 速率限制**
```python
# 实现重试机制
import time
from anthropic import RateLimitError

try:
    response = get_completion(prompt)
except RateLimitError:
    time.sleep(2)
    response = get_completion(prompt)
```

**3. Token 限制超出**
```python
# 减少 max_tokens 或缩短输入
message = client.messages.create(
    model=MODEL_NAME,
    max_tokens=1000,  # 减少输出限制
    messages=[{"role": "user", "content": prompt}]
)
```

更多故障排除信息，请查看[故障排除指南](../docs/zh/advanced/troubleshooting.md)。

## 最佳实践

### 1. 安全管理 API 密钥
- ✅ 使用环境变量
- ✅ 使用配置文件（不提交到 Git）
- ❌ 不要硬编码在代码中
- ❌ 不要提交到版本控制

### 2. 错误处理
```python
from anthropic import APIError, APIConnectionError, RateLimitError

try:
    response = get_completion(prompt)
except RateLimitError:
    # 处理速率限制
    pass
except APIConnectionError:
    # 处理连接错误
    pass
except APIError as e:
    # 处理其他 API 错误
    print(f"API 错误: {e}")
```

### 3. 成本监控
```python
# 跟踪 token 使用
response = client.messages.create(...)
print(f"输入 tokens: {response.usage.input_tokens}")
print(f"输出 tokens: {response.usage.output_tokens}")
```

### 4. 性能优化
- 使用异步 API 进行批量处理
- 实现响应缓存
- 选择合适的模型（Haiku 最快）

详细最佳实践请查看[性能优化文档](../docs/zh/advanced/performance.md)。

## 获取帮助

如果您在使用过程中遇到问题：

1. **查看文档**：
   - [Anthropic 1P 版本详细文档](../docs/zh/versions/anthropic-1p.md)
   - [故障排除指南](../docs/zh/advanced/troubleshooting.md)
   - [常见问题](../docs/zh/advanced/faq.md)

2. **官方支持**：
   - [Anthropic 文档](https://docs.anthropic.com/)
   - [API 参考](https://docs.anthropic.com/claude/reference/)

3. **社区资源**：
   - [Anthropic Discord](https://discord.gg/anthropic)
   - [GitHub Issues](https://github.com/anthropics/anthropic-sdk-python/issues)

## 贡献

欢迎贡献！请查看我们的[贡献指南](../docs/zh/development/contributing.md)了解如何参与项目。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](../AmazonBedrock/LICENSE) 文件。

---

**准备好开始了吗？** 打开 `00_Tutorial_How-To.ipynb` 开始您的提示工程学习之旅！

如需更多信息，请访问[项目主页](../README.md)或查看[完整文档](../docs/zh/README.md)。

祝学习愉快！🚀
