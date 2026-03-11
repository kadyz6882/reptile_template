"""
Reptile Template - 通用爬虫模板
一个功能完整、易于使用的Python爬虫项目模板
"""

__version__ = "2.0.0"
__author__ = "kadyz6882"
__email__ = "kadhy2021120713@outlook.com"

from .core import BaseScraper, AsyncScraper, SimpleScraper
from .config import Settings, get_settings
from .data import StorageManager, DataProcessor, DataCleaner
from .loggers import get_logger
from .utils import validate_url, format_size

__all__ = [
    "BaseScraper", "AsyncScraper", "SimpleScraper",
    "Settings", "get_settings",
    "StorageManager", "DataProcessor", "DataCleaner",
    "get_logger",
    "validate_url", "format_size"
]
