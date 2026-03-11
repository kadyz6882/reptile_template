# Reptile Template - 通用爬虫模板 v2.0.0

一个功能完整、易于使用的Python爬虫项目模板，支持同步和异步爬取，具备完整的数据处理、存储和日志功能。

## 🆕 v2.0.0 新特性

- ✅ **修复Pydantic兼容性** - 支持Pydantic v1和v2版本
- ✅ **完善CLI工具** - 修复入口点，支持命令行操作
- ✅ **优化依赖管理** - 移除无效依赖，添加必要组件
- ✅ **增强稳定性** - 修复所有已知问题，通过完整测试
- ✅ **改进导入系统** - 修复模块导入路径问题

## 🚀 核心特性

- **模块化设计**: 核心功能模块化，易于扩展和维护
- **同步/异步支持**: 同时支持同步和异步爬虫，满足不同场景需求
- **多种解析器**: 支持BeautifulSoup、Parsel等多种解析方式
- **灵活的存储**: 支持JSON、CSV、数据库、MongoDB等多种存储方式
- **数据处理**: 内置数据清洗、验证、去重、增强等功能
- **完善的日志**: 基于loguru的多级日志系统
- **配置管理**: 基于Pydantic的配置管理，支持环境变量
- **代理支持**: 内置代理配置和管理
- **速率控制**: 内置请求延迟和速率限制
- **错误重试**: 自动重试机制，提高爬取稳定性

## 📁 项目结构

```
reptile_template/
├── src/                    # 源代码目录
│   ├── core/              # 核心爬虫模块
│   │   ├── __init__.py
│   │   ├── scraper.py     # 爬虫基类
│   │   ├── parser.py      # 解析器
│   │   └── session.py     # 会话管理
│   ├── config/            # 配置管理
│   │   ├── __init__.py
│   │   └── settings.py    # 配置类
│   ├── data/              # 数据处理
│   │   ├── __init__.py
│   │   ├── storage.py     # 存储管理
│   │   └── processors.py  # 数据处理器
│   ├── utils/             # 工具类
│   │   ├── __init__.py
│   │   ├── helpers.py     # 辅助函数
│   │   ├── validators.py  # 验证器
│   │   └── formatters.py  # 格式化工具
│   └── loggers/           # 日志系统
│       ├── __init__.py
│       └── scraper_logger.py
├── examples/              # 示例代码
│   ├── basic_scraper.py   # 基础爬虫示例
│   ├── async_scraper.py   # 异步爬虫示例
│   └── custom_scraper.py   # 自定义爬虫示例
├── tests/                 # 测试代码
├── docs/                  # 文档
├── output/                # 输出目录
├── logs/                  # 日志目录
├── requirements.txt       # 依赖列表
├── pyproject.toml        # 项目配置
├── .env.example          # 环境变量示例
└── README.md             # 项目说明
```

## 🛠️ 安装和配置

### 1. 克隆项目

```bash
git clone <repository-url>
cd reptile_template
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**重要**: v2.0.0版本需要以下关键依赖：
- `pydantic>=2.5.0` 和 `pydantic-settings>=2.0.0` - 配置管理
- `requests>=2.31.0` - HTTP请求库
- `aiohttp>=3.9.0` - 异步HTTP支持
- `beautifulsoup4>=4.12.0` - HTML解析
- `loguru>=0.7.0` - 日志系统

或使用pip安装（开发模式）：

```bash
pip install -e .
```

### 3. 配置环境变量

复制环境变量示例文件并根据需要修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置你的爬虫参数：

```env
# 爬虫配置
SCRAPER_DELAY=1
SCRAPER_TIMEOUT=30
SCRAPER_MAX_RETRIES=3
SCRAPER_CONCURRENT_REQUESTS=10

# 代理配置
PROXY_ENABLED=false
PROXY_HOST=
PROXY_PORT=

# 数据库配置
DATABASE_URL=sqlite:///data/scraped_data.db
MONGODB_URL=mongodb://localhost:27017/

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/scraping.log
```

## 📖 使用指南

### 基础爬虫

```python
from src.core import SimpleScraper
from src.data import StorageManager

# 创建爬虫实例
scraper = SimpleScraper()

# 爬取单个页面
result = scraper.scrape("https://example.com")
print(result)

# 爬取多个页面
urls = ["https://example1.com", "https://example2.com"]
results = scraper.scrape_multiple(urls)

# 保存结果
storage = StorageManager()
storage.save(results, "scraped_data")

# 关闭爬虫
scraper.close()
```

### 异步爬虫

```python
import asyncio
from src.core import AsyncScraper
from src.data import StorageManager

async def main():
    # 创建异步爬虫
    scraper = AsyncScraper()
    
    # 异步爬取多个页面
    urls = ["https://example1.com", "https://example2.com"]
    results = await scraper.scrape_multiple(urls, max_concurrent=5)
    
    # 保存结果
    storage = StorageManager()
    storage.save(results, "async_scraped_data")
    
    # 关闭爬虫
    await scraper.close()

# 运行异步爬虫
asyncio.run(main())
```

### 自定义爬虫

```python
from src.core import BaseScraper
from bs4 import BeautifulSoup

class MyCustomScraper(BaseScraper):
    def parse(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            "url": response.url,
            "title": soup.title.string if soup.title else "",
            "content": soup.get_text()[:1000]
        }

# 使用自定义爬虫
scraper = MyCustomScraper()
result = scraper.scrape("https://example.com")
scraper.close()
```

### 数据处理

```python
from src.data import DataCleaner, DataValidator, DataEnricher

# 数据清洗
cleaner = DataCleaner()
cleaned_data = cleaner.process(raw_data)

# 数据验证
validator = DataValidator(required_fields=['title', 'url'])
validated_data = validator.process(data)

# 数据增强
enricher = DataEnricher()
enriched_data = enricher.process(data)
```

### 配置管理

```python
from src.config import get_settings

# 获取配置
settings = get_settings()

# 使用配置
print(f"请求延迟: {settings.scraper_delay}")
print(f"并发数: {settings.scraper_concurrent_requests}")
print(f"代理URL: {settings.proxy_url}")
```

## 🔧 高级功能

### 代理配置

```python
from src.config import get_settings

settings = get_settings()

# 启用代理
settings.proxy_enabled = True
settings.proxy_host = "127.0.0.1"
settings.proxy_port = 8080
settings.proxy_username = "user"
settings.proxy_password = "pass"
```

### 自定义解析器

```python
from src.core.parser import BaseParser

class MyParser(BaseParser):
    def parse(self, content):
        # 自定义解析逻辑
        return {"custom_field": "custom_value"}

# 在爬虫中使用自定义解析器
scraper = MyCustomScraper()
scraper.parser = MyParser()
```

### 数据存储

```python
from src.data import JSONStorage, CSVStorage, DatabaseStorage

# JSON存储
json_storage = JSONStorage()
json_storage.save(data, "my_data")

# CSV存储
csv_storage = CSVStorage()
csv_storage.save(data, "my_data")

# 数据库存储
db_storage = DatabaseStorage("my_table")
db_storage.save(data)
```

## 📝 示例项目

查看 `examples/` 目录中的示例代码：

- `basic_scraper.py` - 基础爬虫示例
- `async_scraper.py` - 异步爬虫示例  
- `custom_scraper.py` - 自定义爬虫示例

运行示例：

```bash
python examples/basic_scraper.py
python examples/async_scraper.py
python examples/custom_scraper.py
```

## 🧪 测试

运行测试：

```bash
pytest tests/
```

## 📊 性能优化

1. **使用异步爬虫**: 对于大量URL，异步爬虫性能更好
2. **调整并发数**: 根据目标网站调整 `SCRAPER_CONCURRENT_REQUESTS`
3. **合理设置延迟**: 避免过于频繁的请求
4. **使用代理**: 避免IP被封禁
5. **数据去重**: 避免重复处理相同数据

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 📄 许可证

MIT License

### 升级指南
从v1.0.0升级到v2.0.0：
1. 备份现有项目
2. 更新依赖：`pip install -r requirements.txt`
3. 检查配置文件兼容性
4. 运行测试验证功能正常

### 🆘 支持

如果你在使用过程中遇到问题，可以：

1. 查看 `docs/` 目录中的详细文档
2. 查看示例代码了解具体用法
3. 提交Issue寻求帮助：[GitHub Issues](https://github.com/kadyz6882/reptile-template/issues)

## 🔄 更新日志

### v2.0.0 (2024-03-11)
**重大更新 - 完全重构版本**

#### 🐛 修复的问题
- **Pydantic兼容性**: 修复BaseSettings导入问题，支持v1和v2版本
- **CLI入口点**: 修复main()函数缺失问题，完善命令行工具
- **依赖管理**: 移除asyncio无效依赖，添加pydantic-settings
- **模块导入**: 修复所有模块导入路径和循环依赖问题
- **配置系统**: 修复Config和model_config冲突问题

#### ✨ 新增功能
- **兼容性检查**: 自动检测并适配不同版本的依赖库
- **增强测试**: 添加完整的单元测试覆盖
- **错误处理**: 改进异常处理和错误信息

#### 🔧 改进
- **代码质量**: 重构核心代码，提高可维护性
- **文档完善**: 更新所有文档和使用示例
- **性能优化**: 优化导入和初始化性能

#### ⚠️ 破坏性变更
- **Python版本**: 最低支持Python 3.8+
- **依赖更新**: 部分依赖版本要求提升

### v1.0.0 (2024-03-11)
- 初始版本发布
- 支持同步和异步爬虫
- 完整的数据处理和存储功能
- 模块化的项目结构
