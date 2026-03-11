# 🚀 快速开始指南 - v3.0.0

5分钟上手 Reptile Template v3.0.0！

## 📋 前置要求

- Python 3.8+
- pip 包管理器

## ⚡ 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/kadyz6882/reptile_template.git
cd reptile_template
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**重要**: v3.0.0版本需要以下关键依赖：
- `pydantic>=2.5.0` 和 `pydantic-settings>=2.0.0` - 配置管理
- `requests>=2.31.0` - HTTP请求库
- `aiohttp>=3.9.0` - 异步HTTP支持
- `beautifulsoup4>=4.12.0` - HTML解析
- `loguru>=0.7.0` - 日志系统

### 3. 验证安装

运行测试确保一切正常：

```bash
# 方法1: 使用测试脚本（推荐）
python run_tests.py

# 方法2: 直接运行测试
python tests/test_basic.py

# 方法3: 使用unittest模块
python -m unittest tests.test_basic -v
```

如果看到 `🎉 所有测试通过！模板可以正常使用。` 说明安装成功！

### 4. 创建第一个爬虫

创建 `my_scraper.py`：

```python
#!/usr/bin/env python3
"""
我的第一个爬虫 - Reptile Template v3.0.0
"""

import sys
import os
sys.path.insert(0, '.')

from src.core import SimpleScraper
from src.data import JSONStorage

def main():
    # 创建爬虫实例
    scraper = SimpleScraper()
    
    # 爬取网页
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json"
    ]
    
    print("开始爬取...")
    results = scraper.scrape_multiple(urls)
    
    # 保存结果（自动创建output/目录）
    storage = JSONStorage("output")
    success = storage.save(results, "my_first_scrape")
    
    if success:
        print(f"✅ 成功爬取 {len(results)} 个页面")
        print(f"📁 结果保存在: output/my_first_scrape.json")
    else:
        print("❌ 保存失败")
    
    # 关闭爬虫
    scraper.close()

if __name__ == "__main__":
    main()
```

### 5. 运行爬虫

```bash
python my_scraper.py
```

### 6. 了解数据存储

Reptile Template v3.0.0 提供多种数据存储方式：

```python
from src.data import JSONStorage, DatabaseStorage

# 文件存储（自动创建 output/ 目录）
json_storage = JSONStorage("output")
json_storage.save(results, "my_scrape")

# 数据库存储（自动创建 data/runtime/ 目录）
db_storage = DatabaseStorage("scraped_data")
db_storage.save(results)

# 使用示例数据进行测试
example_storage = JSONStorage("data/examples")
sample_data = example_storage.load("sample_data")
print(f"示例数据: {len(sample_data)} 条")
```

## 🎯 下一步

- 查看 `examples/` 目录学习更多示例
- 阅读 [配置指南](CONFIGURATION.md) 了解详细配置
- 查看 [数据存储指南](DATA_STORAGE.md) 了解数据管理
- 阅读 [常见问题](FAQ.md) 解决常见问题

## 🆕 v3.0.0 新特性

- ✅ **完整文档体系** - 包含快速开始、配置指南、FAQ等
- ✅ **自动目录创建** - 无需手动创建output、logs、data目录
- ✅ **示例数据** - 提供JSON和CSV格式的示例数据
- ✅ **数据库架构** - 提供SQLite和MySQL的完整架构
- ✅ **用户友好测试** - run_tests.py脚本，快速验证安装

## ❓ 遇到问题？

1. **导入错误**：确保在项目根目录运行脚本
2. **依赖问题**：检查是否安装了所有依赖
3. **权限问题**：某些网站可能需要设置代理

更多帮助请查看 [常见问题](FAQ.md) 或提交 [Issue](https://github.com/kadyz6882/reptile-template/issues)。
