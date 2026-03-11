# Reptile Template - 通用爬虫模板 v3.0.0

一个功能完整、易于使用的Python爬虫项目模板，支持同步和异步爬取，具备完整的数据处理、存储和日志功能。

## 🆕 v3.0.0 新特性

- ✅ **完整文档体系** - 包含快速开始、配置指南、FAQ等完整文档
- ✅ **数据目录结构** - 完善的示例数据、数据库架构和使用指南
- ✅ **自动目录创建** - 无需手动创建output、logs、data目录
- ✅ **修复所有导入问题** - 解决模块导入和循环依赖问题
- ✅ **增强示例代码** - 所有示例代码可正常运行，包含最佳实践
- ✅ **完善测试覆盖** - 11个单元测试，覆盖所有核心功能
- ✅ **用户友好体验** - run_tests.py脚本，新用户快速验证安装

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
├── data/                  # 📊 数据目录
│   ├── .gitkeep           # 保持目录在版本控制中
│   ├── README.md          # 数据目录说明
│   ├── examples/          # 示例数据文件
│   │   ├── sample_data.json
│   │   └── test_data.csv
│   ├── schema/            # 数据库架构
│   │   ├── sqlite_schema.sql
│   │   └── mysql_schema.sql
│   └── runtime/           # 运行时数据（gitignored）
├── examples/              # 示例代码
│   ├── basic_scraper.py   # 基础爬虫示例
│   ├── async_scraper.py   # 异步爬虫示例
│   └── custom_scraper.py   # 自定义爬虫示例
├── tests/                 # 测试代码
├── docs/                  # 文档
├── run_tests.py           # 测试运行脚本
├── output/                # 输出目录（自动创建）
├── logs/                  # 日志目录（自动创建）
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

如果看到 `🎉 所有测试通过！模板可以正常使用。` 说明安装成功。

### 4. 配置环境变量

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

### 数据存储

```python
from src.data import JSONStorage, CSVStorage, DatabaseStorage

# 文件存储（自动创建 output/ 目录）
json_storage = JSONStorage("output")
csv_storage = CSVStorage("output")

# 数据库存储（自动创建 data/runtime/ 目录）
db_storage = DatabaseStorage("scraped_data")

# 使用示例数据
from src.data import JSONStorage
example_storage = JSONStorage("data/examples")
sample_data = example_storage.load("sample_data")
print(f"加载了 {len(sample_data)} 条示例数据")
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

### v3.0.0 (2024-03-12)
**重大更新 - 完整文档和用户体验版本**

#### 🐛 修复的问题
- **导入问题**: 修复BeautifulSoupParser和DataEnricher导入错误
- **示例代码**: 修复所有示例文件的导入和存储类使用
- **循环依赖**: 完全解决模块间的循环依赖问题
- **文件结构**: 确保文档说明与实际文件结构完全一致

#### ✨ 新增功能
- **完整文档体系**: 添加6个详细文档（快速开始、配置指南、FAQ、数据存储等）
- **数据目录结构**: 添加示例数据、数据库架构、使用指南
- **测试脚本**: 添加run_tests.py用户友好测试脚本
- **自动目录创建**: 无需手动创建任何目录，自动创建output、logs、data
- **示例数据**: 提供JSON和CSV格式的示例数据文件
- **数据库架构**: 提供SQLite和MySQL的完整数据库架构

#### 🔧 改进
- **文档完整性**: 所有功能都有详细文档说明
- **用户体验**: 新用户5分钟内可完成安装和验证
- **代码质量**: 所有示例代码经过测试，可直接使用
- **错误处理**: 改进错误信息和调试体验
- **结构一致性**: 文档与实际代码结构100%匹配

#### 📚 文档更新
- **快速开始指南**: 5分钟上手教程
- **配置指南**: 详细的配置选项说明
- **FAQ文档**: 常见问题和解决方案
- **数据存储指南**: 完整的数据存储使用说明
- **项目文档**: 完整的文档索引和规划

#### ⚠️ 破坏性变更
- **导入路径**: 某些导入路径已优化（向后兼容）
- **示例更新**: 示例代码使用新的最佳实践

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
