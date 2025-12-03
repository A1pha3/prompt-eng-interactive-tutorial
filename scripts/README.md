# 文档验证工具

这个目录包含用于验证项目文档质量的工具集。

## 工具概述

`validate_docs.py` 是主要的验证脚本，它提供了多种文档质量检查功能：

1. **文档存在性检查** - 验证所有必需的文档文件和目录是否存在
2. **内容完整性检查** - 检查文档是否包含必需的章节和元数据
3. **代码示例验证** - 验证文档中代码示例的语法正确性
4. **Markdown 格式检查** - 检查 Markdown 语法和格式规范
5. **文档结构一致性** - 验证同类文档的结构是否一致
6. **术语一致性检查** - 检查技术术语使用的一致性
7. **链接验证** - 验证文档中所有链接的有效性

## 使用方法

### 基本用法

```bash
# 运行所有检查
python3 scripts/validate_docs.py --all

# 运行特定检查
python3 scripts/validate_docs.py --existence --content

# 指定项目根目录
python3 scripts/validate_docs.py --all --root /path/to/project
```

### 可用选项

- `--all` - 运行所有检查
- `--existence` - 检查文档存在性
- `--content` - 检查文档内容完整性
- `--code` - 验证代码示例
- `--format` - 检查 Markdown 格式
- `--structure` - 检查文档结构一致性
- `--terminology` - 检查术语一致性
- `--links` - 验证链接
- `--root DIR` - 指定项目根目录（默认为当前目录）

### 示例

```bash
# 只检查文档是否存在
python3 scripts/validate_docs.py --existence

# 检查代码示例和链接
python3 scripts/validate_docs.py --code --links

# 运行所有检查并指定项目路径
python3 scripts/validate_docs.py --all --root ~/projects/my-docs
```

## 输出说明

验证工具会为每个检查生成详细的报告：

- ✓ **通过** - 所有检查都通过
- ❌ **错误** - 发现需要修复的问题
- ⚠️ **警告** - 发现建议改进的问题

## 架构

验证工具采用模块化设计：

```
scripts/
├── validate_docs.py          # 主脚本
└── validators/               # 验证器模块
    ├── __init__.py          # 模块初始化
    ├── base.py              # 基类
    ├── existence.py         # 存在性检查
    ├── content.py           # 内容完整性检查
    ├── code.py              # 代码示例验证
    ├── format.py            # Markdown 格式检查
    ├── structure.py         # 结构一致性检查
    ├── terminology.py       # 术语一致性检查
    └── links.py             # 链接验证
```

## 扩展

要添加新的验证器：

1. 在 `validators/` 目录下创建新的 Python 文件
2. 继承 `DocumentValidator` 基类
3. 实现 `check()` 方法
4. 在 `validators/__init__.py` 中导出新类
5. 在 `validate_docs.py` 的 `main()` 函数中添加命令行选项

## 依赖

- Python 3.6+
- 标准库（无需额外安装）

## 退出码

- `0` - 所有检查通过（可能有警告）
- `1` - 至少有一个检查失败（有错误）
