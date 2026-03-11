import os
import sys
from typing import Optional
from loguru import logger
from ..config import get_settings


class ScraperLogger:
    """爬虫日志管理器"""
    
    def __init__(self, name: str = "scraper"):
        self.settings = get_settings()
        self.name = name
        self._setup_logger()
    
    def _setup_logger(self):
        """设置日志配置"""
        # 移除默认处理器
        logger.remove()
        
        # 添加控制台输出
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>",
            level=self.settings.log_level,
            colorize=True
        )
        
        # 添加文件输出
        log_dir = os.path.dirname(self.settings.log_file)
        os.makedirs(log_dir, exist_ok=True)
        
        logger.add(
            self.settings.log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=self.settings.log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            encoding="utf-8"
        )
        
        # 添加错误日志文件
        error_log_file = self.settings.log_file.replace('.log', '_error.log')
        logger.add(
            error_log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            encoding="utf-8"
        )
    
    def get_logger(self):
        """获取logger实例"""
        return logger.bind(name=self.name)


# 全局logger实例
_loggers: dict = {}


def get_logger(name: str = "scraper") -> "ScraperLogger":
    """获取logger实例"""
    if name not in _loggers:
        _loggers[name] = ScraperLogger(name)
    return _loggers[name]
