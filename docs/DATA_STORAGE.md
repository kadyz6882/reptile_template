# 📊 数据存储指南

详细说明 Reptile Template 的数据存储系统。

## 📁 目录结构

```
data/
├── .gitkeep              # 保持目录在版本控制中
├── README.md             # 数据目录说明
├── examples/              # 示例数据文件
│   ├── sample_data.json   # JSON格式示例数据
│   └── test_data.csv      # CSV格式示例数据
├── schema/                # 数据库架构
│   ├── sqlite_schema.sql  # SQLite数据库结构
│   └── mysql_schema.sql   # MySQL数据库结构
└── runtime/               # 运行时数据（gitignored）
    ├── scraped_data.db    # SQLite数据库（自动创建）
    └── cache.db           # 缓存数据库（自动创建）
```

## 🎯 存储类型

### 1. 文件存储

#### JSON存储
```python
from src.data import JSONStorage

# 创建存储器（自动创建目录）
storage = JSONStorage("output")

# 保存数据
data = [{"title": "Example", "url": "https://example.com"}]
success = storage.save(data, "my_scrape")
# → output/my_scrape.json

# 加载数据
loaded_data = storage.load("my_scrape")
```

#### CSV存储
```python
from src.data import CSVStorage

storage = CSVStorage("output")
success = storage.save(data, "my_scrape")
# → output/my_scrape.csv
```

### 2. 数据库存储

#### SQLite存储
```python
from src.data import DatabaseStorage

# 自动创建 data/runtime/ 目录和数据库文件
db_storage = DatabaseStorage("scraped_data")
success = db_storage.save(data)
# → data/runtime/scraped_data.db
```

#### 自定义数据库
```python
# MySQL
db_storage = DatabaseStorage(
    "my_table", 
    connection_string="mysql+pymysql://user:pass@localhost/db"
)

# PostgreSQL
db_storage = DatabaseStorage(
    "my_table",
    connection_string="postgresql://user:pass@localhost/db"
)
```

## 📖 示例数据

### 使用示例数据
```python
from src.data import JSONStorage

# 加载示例数据
example_storage = JSONStorage("data/examples")
sample_data = example_storage.load("sample_data")

print(f"示例数据条数: {len(sample_data)}")
print(f"第一条数据: {sample_data[0]}")
```

### 示例数据结构
```json
[
  {
    "url": "https://example.com/page1",
    "title": "Example Page 1",
    "content": "This is sample content",
    "scraped_at": "2024-03-12T00:00:00",
    "status": "success",
    "response_time": 1.23,
    "size": 1024
  }
]
```

## 🗄️ 数据库架构

### SQLite架构
```bash
# 使用预定义架构
sqlite3 data/runtime/scraped_data.db < data/schema/sqlite_schema.sql
```

### MySQL架构
```bash
# 使用预定义架构
mysql -u username -p database_name < data/schema/mysql_schema.sql
```

## 🚀 实际使用示例

### 完整爬虫示例
```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from src.core import SimpleScraper
from src.data import JSONStorage, DatabaseStorage

def main():
    # 创建爬虫
    scraper = SimpleScraper()
    
    # 爬取数据
    urls = ["https://example.com"]
    raw_data = scraper.scrape_multiple(urls)
    
    # 保存到JSON文件
    file_storage = JSONStorage("output")
    file_storage.save(raw_data, "scraped_data")
    print("✅ 数据保存到: output/scraped_data.json")
    
    # 保存到数据库
    db_storage = DatabaseStorage("scraped_data")
    db_storage.save(raw_data)
    print("✅ 数据保存到: data/runtime/scraped_data.db")
    
    # 使用示例数据进行测试
    example_storage = JSONStorage("data/examples")
    sample_data = example_storage.load("sample_data")
    print(f"✅ 加载示例数据: {len(sample_data)} 条")

if __name__ == "__main__":
    main()
```

## 📊 数据处理流程

### 1. 数据采集
```python
# 爬虫采集原始数据
scraper = SimpleScraper()
raw_data = scraper.scrape_multiple(urls)
```

### 2. 数据清洗
```python
from src.data import DataCleaner

cleaner = DataCleaner()
cleaned_data = cleaner.process(raw_data)
```

### 3. 数据验证
```python
from src.data import DataValidator

validator = DataValidator(required_fields=['title', 'url'])
validated_data = validator.process(cleaned_data)
```

### 4. 数据存储
```python
# 多格式存储
JSONStorage("output").save(validated_data, "final_data")
CSVStorage("output").save(validated_data, "final_data")
DatabaseStorage("scraped_data").save(validated_data)
```

## 🔧 配置选项

### 环境变量配置
```env
# 数据库配置
DATABASE_URL=sqlite:///data/runtime/scraped_data.db
MONGODB_URL=mongodb://localhost:27017/

# 输出配置
OUTPUT_DIR=output/
OUTPUT_FORMAT=json
```

### 代码配置
```python
from src.config import get_settings

settings = get_settings()
print(f"输出目录: {settings.output_dir}")
print(f"数据库URL: {settings.database_url}")
```

## 📈 性能优化

### 1. 批量处理
```python
# 分批保存大量数据
for batch in chunk_list(large_data, 1000):
    storage.save(batch, f"batch_{batch_id}")
```

### 2. 异步存储
```python
# 异步保存（如果支持）
await async_storage.save(data, "async_data")
```

### 3. 压缩存储
```python
# 压缩JSON文件
import gzip
import json

with gzip.open("output/compressed_data.json.gz", "wt") as f:
    json.dump(data, f)
```

## 🛡️ 数据安全

### 1. 敏感数据处理
```python
# 移除敏感信息
def sanitize_data(data):
    for item in data:
        item.pop('password', None)
        item.pop('token', None)
    return data
```

### 2. 数据加密
```python
# 加密存储（示例）
from cryptography.fernet import Fernet

def encrypt_data(data):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(json.dumps(data).encode())
    return encrypted_data
```

## 📝 最佳实践

1. **目录管理**
   - 使用 `output/` 存储最终结果
   - 使用 `data/runtime/` 存储数据库
   - 使用 `data/examples/` 存储示例数据

2. **命名规范**
   - 使用描述性文件名
   - 包含时间戳信息
   - 使用一致的格式

3. **数据备份**
   ```python
   # 定期备份重要数据
   import shutil
   import datetime
   
   backup_name = f"backup_{datetime.now().strftime('%Y%m%d')}"
   shutil.make_archive(backup_name, 'zip', 'output')
   ```

4. **清理策略**
   ```python
   # 清理过期数据
   import os
   import time
   
   def clean_old_files(directory, days=7):
       cutoff = time.time() - (days * 86400)
       for filename in os.listdir(directory):
           filepath = os.path.join(directory, filename)
           if os.path.getmtime(filepath) < cutoff:
               os.remove(filepath)
   ```

## ❓ 常见问题

### Q: 如何处理大量数据？
A: 使用数据库存储，分批处理，考虑压缩。

### Q: 如何迁移数据？
A: 使用标准的数据库迁移工具或导出/导入功能。

### Q: 如何备份重要数据？
A: 定期复制 `output/` 和 `data/runtime/` 目录。

---

更多数据存储问题请查看 [FAQ](FAQ.md) 或提交 [Issue](https://github.com/kadyz6882/reptile-template/issues)。
