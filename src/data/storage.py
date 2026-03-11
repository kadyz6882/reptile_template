import json
import csv
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from ..config import get_settings


class DataStorage(ABC):
    """数据存储基类"""
    
    @abstractmethod
    def save(self, data: Union[Dict, List[Dict]], filename: str) -> bool:
        """保存数据"""
        pass
    
    @abstractmethod
    def load(self, filename: str) -> Union[Dict, List[Dict]]:
        """加载数据"""
        pass
    
    @abstractmethod
    def exists(self, filename: str) -> bool:
        """检查文件是否存在"""
        pass


class JSONStorage(DataStorage):
    """JSON文件存储"""
    
    def __init__(self, output_dir: Optional[str] = None):
        self.settings = get_settings()
        self.output_dir = output_dir or self.settings.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save(self, data: Union[Dict, List[Dict]], filename: str) -> bool:
        """保存为JSON文件"""
        try:
            filepath = os.path.join(self.output_dir, f"{filename}.json")
            
            # 添加时间戳
            if isinstance(data, dict):
                data['saved_at'] = datetime.now().isoformat()
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        item['saved_at'] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存JSON文件失败: {e}")
            return False
    
    def load(self, filename: str) -> Union[Dict, List[Dict]]:
        """加载JSON文件"""
        try:
            filepath = os.path.join(self.output_dir, f"{filename}.json")
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载JSON文件失败: {e}")
            return {} if filename.endswith('.json') else []
    
    def exists(self, filename: str) -> bool:
        """检查文件是否存在"""
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        return os.path.exists(filepath)


class CSVStorage(DataStorage):
    """CSV文件存储"""
    
    def __init__(self, output_dir: Optional[str] = None):
        self.settings = get_settings()
        self.output_dir = output_dir or self.settings.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save(self, data: Union[Dict, List[Dict]], filename: str) -> bool:
        """保存为CSV文件"""
        try:
            filepath = os.path.join(self.output_dir, f"{filename}.csv")
            
            if isinstance(data, dict):
                data = [data]
            
            if not data:
                return False
            
            # 添加时间戳
            for item in data:
                item['saved_at'] = datetime.now().isoformat()
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            print(f"保存CSV文件失败: {e}")
            return False
    
    def load(self, filename: str) -> List[Dict]:
        """加载CSV文件"""
        try:
            filepath = os.path.join(self.output_dir, f"{filename}.csv")
            df = pd.read_csv(filepath, encoding='utf-8-sig')
            return df.to_dict('records')
        except Exception as e:
            print(f"加载CSV文件失败: {e}")
            return []
    
    def exists(self, filename: str) -> bool:
        """检查文件是否存在"""
        filepath = os.path.join(self.output_dir, f"{filename}.csv")
        return os.path.exists(filepath)


class DatabaseStorage(DataStorage):
    """数据库存储"""
    
    def __init__(self, table_name: str = "scraped_data"):
        self.settings = get_settings()
        self.table_name = table_name
        self.engine = create_engine(self.settings.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._create_table()
    
    def _create_table(self):
        """创建表"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data TEXT NOT NULL,
                        url TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
        except Exception as e:
            print(f"创建表失败: {e}")
    
    def save(self, data: Union[Dict, List[Dict]], filename: str = None) -> bool:
        """保存到数据库"""
        try:
            with self.SessionLocal() as session:
                if isinstance(data, dict):
                    data = [data]
                
                for item in data:
                    item_json = json.dumps(item, ensure_ascii=False)
                    url = item.get('url', '')
                    
                    session.execute(text(f"""
                        INSERT INTO {self.table_name} (data, url)
                        VALUES (:data, :url)
                    """), {"data": item_json, "url": url})
                
                session.commit()
            return True
        except Exception as e:
            print(f"保存到数据库失败: {e}")
            return False
    
    def load(self, filename: str = None, limit: int = 1000) -> List[Dict]:
        """从数据库加载数据"""
        try:
            with self.SessionLocal() as session:
                result = session.execute(text(f"""
                    SELECT data FROM {self.table_name}
                    ORDER BY created_at DESC
                    LIMIT :limit
                """), {"limit": limit})
                
                data = []
                for row in result:
                    data.append(json.loads(row[0]))
                return data
        except Exception as e:
            print(f"从数据库加载数据失败: {e}")
            return []
    
    def exists(self, filename: str = None) -> bool:
        """检查表是否存在"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='{self.table_name}'
                """))
                return result.fetchone() is not None
        except:
            return False


class MongoStorage(DataStorage):
    """MongoDB存储"""
    
    def __init__(self, collection_name: str = "scraped_data"):
        self.settings = get_settings()
        self.collection_name = collection_name
        self.client = MongoClient(self.settings.mongodb_url)
        self.db = self.client.get_default_db()
        self.collection = self.db[collection_name]
    
    def save(self, data: Union[Dict, List[Dict]], filename: str = None) -> bool:
        """保存到MongoDB"""
        try:
            if isinstance(data, dict):
                data = [data]
            
            # 添加时间戳
            for item in data:
                item['created_at'] = datetime.now()
            
            self.collection.insert_many(data)
            return True
        except Exception as e:
            print(f"保存到MongoDB失败: {e}")
            return False
    
    def load(self, filename: str = None, limit: int = 1000) -> List[Dict]:
        """从MongoDB加载数据"""
        try:
            cursor = self.collection.find().sort('created_at', -1).limit(limit)
            data = []
            for doc in cursor:
                doc.pop('_id', None)  # 移除MongoDB的_id字段
                data.append(doc)
            return data
        except Exception as e:
            print(f"从MongoDB加载数据失败: {e}")
            return []
    
    def exists(self, filename: str = None) -> bool:
        """检查集合是否存在"""
        try:
            return self.collection_name in self.db.list_collection_names()
        except:
            return False
    
    def close(self):
        """关闭连接"""
        self.client.close()


class StorageManager:
    """存储管理器"""
    
    def __init__(self):
        self.settings = get_settings()
        self.json_storage = JSONStorage()
        self.csv_storage = CSVStorage()
        self.db_storage = DatabaseStorage()
        self.mongo_storage = MongoStorage()
    
    def save(self, data: Union[Dict, List[Dict]], filename: str, format: str = None) -> bool:
        """根据格式保存数据"""
        format = format or self.settings.output_format
        
        if format.lower() == 'json':
            return self.json_storage.save(data, filename)
        elif format.lower() == 'csv':
            return self.csv_storage.save(data, filename)
        elif format.lower() == 'database':
            return self.db_storage.save(data, filename)
        elif format.lower() == 'mongodb':
            return self.mongo_storage.save(data, filename)
        else:
            print(f"不支持的格式: {format}")
            return False
    
    def load(self, filename: str, format: str = None, **kwargs) -> Union[Dict, List[Dict]]:
        """根据格式加载数据"""
        format = format or self.settings.output_format
        
        if format.lower() == 'json':
            return self.json_storage.load(filename)
        elif format.lower() == 'csv':
            return self.csv_storage.load(filename)
        elif format.lower() == 'database':
            return self.db_storage.load(filename, **kwargs)
        elif format.lower() == 'mongodb':
            return self.mongo_storage.load(filename, **kwargs)
        else:
            print(f"不支持的格式: {format}")
            return {}
