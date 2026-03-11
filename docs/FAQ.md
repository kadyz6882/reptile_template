# ❓ 常见问题

## 🚨 导入错误

### Q: `ModuleNotFoundError: No module named 'src.data'`

**A**: 这是最常见的问题，解决方法：

```bash
# 方法1: 在项目根目录运行
cd /path/to/reptile_template
python your_script.py

# 方法2: 添加项目路径
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

# 方法3: 使用测试脚本
python run_tests.py
```

### Q: `ImportError: attempted relative import with no known parent package`

**A**: CLI工具运行问题，解决方法：

```bash
# 使用Python模块方式运行
python -m src.cli --help

# 或在项目根目录运行
python src/cli.py --help
```

## 🔧 配置问题

### Q: 如何配置代理？

**A**: 编辑 `.env` 文件：

```env
PROXY_ENABLED=true
PROXY_HOST=127.0.0.1
PROXY_PORT=8080
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
```

### Q: 如何调整爬取速度？

**A**: 修改 `.env` 文件：

```env
# 增加延迟（降低速度）
SCRAPER_DELAY=2.0

# 减少并发数（降低速度）
SCRAPER_CONCURRENT_REQUESTS=5

# 增加超时时间
SCRAPER_TIMEOUT=60
```

## 📊 存储问题

### Q: 数据保存在哪里？

**A**: 默认保存在以下目录：

- `output/` - JSON/CSV文件输出
- `logs/` - 日志文件
- `data/` - 数据库文件（如果使用）

### Q: 如何更改输出目录？

**A**: 在代码中指定：

```python
from src.data import JSONStorage

# 自定义输出目录
storage = JSONStorage("/path/to/your/output")
storage.save(data, "filename")
```

## 🚀 性能问题

### Q: 爬取速度太慢怎么办？

**A**: 优化建议：

1. **使用异步爬虫**：
```python
from src.core import AsyncScraper
# 异步爬虫比同步快5-10倍
```

2. **调整并发数**：
```env
SCRAPER_CONCURRENT_REQUESTS=20  # 适当增加
```

3. **减少延迟**：
```env
SCRAPER_DELAY=0.5  # 但不要太低
```

### Q: 内存占用过高？

**A**: 解决方案：

1. **分批处理**：
```python
# 分批爬取，不要一次性处理太多URL
for batch in chunk_list(urls, 100):
    results = scraper.scrape_multiple(batch)
    # 处理并清理
```

2. **及时清理**：
```python
# 处理完数据后及时清理
del results
import gc
gc.collect()
```

## 🌐 网络问题

### Q: 被网站封禁IP怎么办？

**A**: 防封策略：

1. **设置合理延迟**：
```env
SCRAPER_DELAY=2.0
```

2. **使用代理池**：
```env
PROXY_ENABLED=true
# 配置多个代理轮换
```

3. **随机User-Agent**：
```python
scraper = SimpleScraper()
scraper.session.random_user_agent = True
```

### Q: SSL证书错误？

**A**: 解决方案：

```python
from src.core import SimpleScraper

scraper = SimpleScraper()
scraper.session.verify_ssl = False  # 仅用于测试
```

## 🧪 测试问题

### Q: 测试失败怎么办？

**A**: 调试步骤：

1. **运行测试脚本**：
```bash
python run_tests.py
```

2. **查看详细错误**：
```bash
python tests/test_basic.py -v
```

3. **检查依赖**：
```bash
pip install -r requirements.txt
```

### Q: 某些测试跳过？

**A**: 可能原因：

- 缺少可选依赖（如数据库）
- 网络连接问题
- 权限不足

## 📦 依赖问题

### Q: Pydantic版本冲突？

**A**: v2.0.0已解决，确保安装：

```bash
pip install pydantic>=2.5.0
pip install pydantic-settings>=2.0.0
```

### Q: 某些依赖安装失败？

**A**: 替代方案：

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或分步安装
pip install requests beautifulsoup4 loguru
```

## 🔍 调试技巧

### Q: 如何启用调试模式？

**A**: 设置日志级别：

```env
LOG_LEVEL=DEBUG
```

或在代码中：

```python
from src.loggers import get_logger
logger = get_logger()
logger.setLevel("DEBUG")
```

### Q: 如何查看请求详情？

**A**: 启用详细日志：

```python
scraper = SimpleScraper()
scraper.session.debug = True
```

---

## 💡 更多帮助

如果以上解决方案都无法解决你的问题：

1. 查看 [示例代码](../examples/)
2. 阅读 [API文档](API_REFERENCE.md)
3. 提交 [GitHub Issue](https://github.com/kadyz6882/reptile-template/issues)
4. 加入讨论：[GitHub Discussions](https://github.com/kadyz6882/reptile-template/discussions)
