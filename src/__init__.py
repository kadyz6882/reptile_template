"""
Reptile Template - 通用爬虫模板
一个功能完整、易于使用的Python爬虫项目模板
"""

__version__ = "2.0.0"
__author__ = "kadyz6882"
__email__ = "kadhy2021120713@outlook.com"

# 延迟导入，避免循环依赖
def __getattr__(name):
    if name == "BaseScraper":
        from .core import BaseScraper
        return BaseScraper
    elif name == "AsyncScraper":
        from .core import AsyncScraper
        return AsyncScraper
    elif name == "SimpleScraper":
        from .core import SimpleScraper
        return SimpleScraper
    elif name == "Settings":
        from .config import Settings
        return Settings
    elif name == "get_settings":
        from .config import get_settings
        return get_settings
    elif name == "StorageManager":
        from .data import StorageManager
        return StorageManager
    elif name == "DataProcessor":
        from .data import DataProcessor
        return DataProcessor
    elif name == "DataCleaner":
        from .data import DataCleaner
        return DataCleaner
    elif name == "JSONStorage":
        from .data import JSONStorage
        return JSONStorage
    elif name == "CSVStorage":
        from .data import CSVStorage
        return CSVStorage
    elif name == "DatabaseStorage":
        from .data import DatabaseStorage
        return DatabaseStorage
    elif name == "get_logger":
        from .loggers import get_logger
        return get_logger
    elif name == "validate_url":
        from .utils import validate_url
        return validate_url
    elif name == "format_size":
        from .utils import format_size
        return format_size
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    "BaseScraper", "AsyncScraper", "SimpleScraper",
    "Settings", "get_settings",
    "StorageManager", "DataProcessor", "DataCleaner",
    "JSONStorage", "CSVStorage", "DatabaseStorage",
    "get_logger",
    "validate_url", "format_size"
]
