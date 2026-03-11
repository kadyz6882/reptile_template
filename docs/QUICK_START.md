# 🚀 快速开始指南

5分钟上手 Reptile Template！

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

### 3. 验证安装
```bash
python run_tests.py
```

看到 `🎉 所有测试通过！模板可以正常使用。` 就成功了！

### 4. 创建第一个爬虫

创建 `my_scraper.py`：

```python
#!/usr/bin/env python3
"""
我的第一个爬虫
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
    
    # 保存结果
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

## 🎯 下一步

- 查看 `examples/` 目录学习更多示例
- 阅读 [API文档](API_REFERENCE.md) 了解详细功能
- 查看 [配置指南](CONFIGURATION.md) 自定义配置

## ❓ 遇到问题？

1. **导入错误**：确保在项目根目录运行脚本
2. **依赖问题**：检查是否安装了所有依赖
3. **权限问题**：某些网站可能需要设置代理

更多帮助请查看 [常见问题](FAQ.md) 或提交 [Issue](https://github.com/kadyz6882/reptile-template/issues)。
