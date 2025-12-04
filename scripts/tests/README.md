# 文档验证属性测试

本目录包含基于属性的测试（Property-Based Tests），用于验证文档系统的正确性属性。

## 测试框架

- **pytest**: 测试运行器
- **Hypothesis**: 属性测试库，用于生成测试数据和验证通用属性

## 安装依赖

```bash
pip install -r scripts/requirements-test.txt
```

## 运行测试

### 运行所有属性测试

```bash
python -m pytest scripts/test_validators.py -v
```

### 运行特定测试

```bash
# 运行文档存在性测试
python -m pytest scripts/test_validators.py::TestDocumentExistence -v

# 运行特定的属性测试
python -m pytest scripts/test_validators.py::TestDocumentExistence::test_required_documents_exist_for_all_categories -v
```

### 查看 Hypothesis 统计信息

```bash
python -m pytest scripts/test_validators.py -v --hypothesis-show-statistics
```

### 详细输出

```bash
python -m pytest scripts/test_validators.py -v --tb=long
```

## 测试说明

### 属性 1：必需文档存在性

**验证需求**: 1.2, 1.3, 2.1, 2.3, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4

**属性描述**: 对于任何文档类别（入门、使用、开发、进阶），该类别下的所有必需文档文件都应该存在于正确的目录路径中。

**测试内容**:
- `test_required_documents_exist_for_all_categories`: 验证所有类别的必需文档都存在
- `test_required_directories_exist`: 验证所有必需的目录结构都存在
- `test_all_categories_have_documents`: 验证文档类别定义的完整性
- `test_existence_checker_integration`: 集成测试，验证检查器的整体功能

## 测试配置

属性测试配置为运行多次迭代以确保覆盖所有可能的输入组合。由于我们使用 `sampled_from` 策略从有限集合中采样，Hypothesis 会智能地测试所有唯一值。

## 故障排查

如果测试失败，请检查：

1. **文档缺失**: 确保所有必需的文档文件都已创建
2. **目录结构**: 确保 `docs/zh/` 目录结构完整
3. **文件权限**: 确保文件可读
4. **空文件**: 确保文档文件不为空

## 添加新的属性测试

要添加新的属性测试：

1. 在 `test_validators.py` 中创建新的测试类或方法
2. 使用 `@given` 装饰器定义输入策略
3. 使用 `@settings(max_examples=100)` 配置测试迭代次数
4. 在文档字符串中标注验证的需求和属性
5. 使用格式: `**Feature: {feature_name}, Property {number}: {property_text}**`
6. 使用格式: `**Validates: Requirements X.Y, Z.W**`

## 参考资料

- [Hypothesis 文档](https://hypothesis.readthedocs.io/)
- [pytest 文档](https://docs.pytest.org/)
- [属性测试介绍](https://hypothesis.works/articles/what-is-property-based-testing/)
