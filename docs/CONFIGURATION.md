# ⚙️ 配置指南

详细说明 Reptile Template 的所有配置选项。

## 📄 配置文件

### 环境变量配置 (.env)

复制示例配置文件：
```bash
cp .env.example .env
```

## 🔧 配置选项详解

### 🕷️ 爬虫配置

#### `SCRAPER_DELAY`
- **类型**: `float`
- **默认值**: `1.0`
- **说明**: 请求间隔时间（秒）
- **建议**: 
  - 开发环境: `1.0-2.0`
  - 生产环境: `0.5-1.5`
  - 激进爬取: `0.1-0.5`（谨慎使用）

```env
SCRAPER_DELAY=1.5
```

#### `SCRAPER_TIMEOUT`
- **类型**: `int`
- **默认值**: `30`
- **说明**: 单个请求超时时间（秒）
- **建议**: 
  - 快速网站: `10-20`
  - 一般网站: `30-60`
  - 慢速网站: `60-120`

```env
SCRAPER_TIMEOUT=45
```

#### `SCRAPER_MAX_RETRIES`
- **类型**: `int`
- **默认值**: `3`
- **说明**: 最大重试次数
- **建议**: 
  - 稳定网络: `2-3`
  - 不稳定网络: `5-10`
  - 重要任务: `10+`

```env
SCRAPER_MAX_RETRIES=5
```

#### `SCRAPER_CONCURRENT_REQUESTS`
- **类型**: `int`
- **默认值**: `10`
- **说明**: 并发请求数（仅异步爬虫）
- **建议**: 
  - 小型网站: `5-10`
  - 中型网站: `10-20`
  - 大型网站: `20-50`

```env
SCRAPER_CONCURRENT_REQUESTS=15
```

### 🌐 代理配置

#### `PROXY_ENABLED`
- **类型**: `bool`
- **默认值**: `false`
- **说明**: 是否启用代理

```env
PROXY_ENABLED=true
```

#### `PROXY_HOST`
- **类型**: `str`
- **默认值**: `""`
- **说明**: 代理服务器地址

```env
PROXY_HOST=127.0.0.1
```

#### `PROXY_PORT`
- **类型**: `int`
- **默认值**: `8080`
- **说明**: 代理服务器端口

```env
PROXY_PORT=8080
```

#### `PROXY_USERNAME`
- **类型**: `str`
- **默认值**: `""`
- **说明**: 代理认证用户名

```env
PROXY_USERNAME=myuser
```

#### `PROXY_PASSWORD`
- **类型**: `str`
- **默认值**: `""`
- **说明**: 代理认证密码

```env
PROXY_PASSWORD=mypass
```

### 🗄️ 数据库配置

#### `DATABASE_URL`
- **类型**: `str`
- **默认值**: `sqlite:///data/scraped_data.db`
- **说明**: 数据库连接URL

```env
# SQLite
DATABASE_URL=sqlite:///data/scraped_data.db

# MySQL
DATABASE_URL=mysql+pymysql://user:pass@localhost/dbname

# PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

#### `MONGODB_URL`
- **类型**: `str`
- **默认值**: `mongodb://localhost:27017/`
- **说明**: MongoDB连接URL

```env
MONGODB_URL=mongodb://user:pass@localhost:27017/dbname
```

### 📝 日志配置

#### `LOG_LEVEL`
- **类型**: `str`
- **默认值**: `INFO`
- **可选值**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **说明**: 日志级别

```env
LOG_LEVEL=DEBUG
```

#### `LOG_FILE`
- **类型**: `str`
- **默认值**: `logs/scraping.log`
- **说明**: 日志文件路径

```env
LOG_FILE=logs/my_project.log
```

### 🌍 用户代理配置

#### `USER_AGENT_ENABLED`
- **类型**: `bool`
- **默认值**: `true`
- **说明**: 是否启用随机User-Agent

```env
USER_AGENT_ENABLED=true
```

## 🎯 配置最佳实践

### 1. 开发环境配置
```env
# 开发环境 .env
SCRAPER_DELAY=2.0
SCRAPER_TIMEOUT=30
SCRAPER_MAX_RETRIES=3
SCRAPER_CONCURRENT_REQUESTS=5
LOG_LEVEL=DEBUG
PROXY_ENABLED=false
```

### 2. 生产环境配置
```env
# 生产环境 .env
SCRAPER_DELAY=1.0
SCRAPER_TIMEOUT=60
SCRAPER_MAX_RETRIES=5
SCRAPER_CONCURRENT_REQUESTS=20
LOG_LEVEL=INFO
PROXY_ENABLED=true
PROXY_HOST=proxy.example.com
PROXY_PORT=8080
```

### 3. 激进爬取配置
```env
# 激进爬取 .env（谨慎使用）
SCRAPER_DELAY=0.3
SCRAPER_TIMEOUT=30
SCRAPER_MAX_RETRIES=2
SCRAPER_CONCURRENT_REQUESTS=50
LOG_LEVEL=WARNING
```

## 🔍 动态配置

### 代码中修改配置

```python
from src.config import get_settings

# 获取配置
settings = get_settings()

# 动态修改
settings.scraper_delay = 2.0
settings.proxy_enabled = True
settings.log_level = "DEBUG"
```

### 配置验证

```python
from src.config import Settings

# 创建自定义配置
custom_settings = Settings(
    scraper_delay=0.5,
    scraper_timeout=120,
    proxy_enabled=True
)

# 验证配置
print(f"延迟: {custom_settings.scraper_delay}")
print(f"代理URL: {custom_settings.proxy_url}")
```

## 📊 性能调优

### 1. 内存优化
```env
# 减少内存占用
SCRAPER_CONCURRENT_REQUESTS=5
SCRAPER_DELAY=1.0
```

### 2. 速度优化
```env
# 提高爬取速度
SCRAPER_DELAY=0.5
SCRAPER_CONCURRENT_REQUESTS=30
SCRAPER_TIMEOUT=30
```

### 3. 稳定性优化
```env
# 提高稳定性
SCRAPER_DELAY=2.0
SCRAPER_MAX_RETRIES=10
SCRAPER_TIMEOUT=120
```

## 🔧 高级配置

### 自定义配置类

```python
from src.config.settings import Settings
from pydantic import Field

class MyCustomSettings(Settings):
    custom_field: str = Field(default="default_value", description="自定义字段")
    
    @property
    def custom_property(self) -> str:
        return f"custom_{self.custom_field}"

# 使用自定义配置
settings = MyCustomSettings()
```

### 环境特定配置

```python
import os
from src.config import get_settings

settings = get_settings()

# 根据环境调整配置
if os.getenv("ENVIRONMENT") == "production":
    settings.scraper_delay = 2.0
    settings.log_level = "INFO"
else:
    settings.scraper_delay = 0.5
    settings.log_level = "DEBUG"
```

## ❓ 常见问题

### Q: 配置不生效？

**A**: 检查：
1. `.env` 文件是否在项目根目录
2. 环境变量名称是否正确
3. 是否重新加载了配置

### Q: 如何重置配置？

**A**: 删除 `.env` 文件，重新复制：
```bash
rm .env
cp .env.example .env
```

### Q: 配置优先级？

**A**: 优先级从高到低：
1. 代码中直接设置
2. 环境变量
3. `.env` 文件
4. 默认值

---

更多配置问题请查看 [FAQ](FAQ.md) 或提交 [Issue](https://github.com/kadyz6882/reptile-template/issues)。
