import os
from typing import Optional, List
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """爬虫配置类"""
    
    # 基础配置
    scraper_delay: float = Field(default=1.0, description="请求间隔时间(秒)")
    scraper_timeout: int = Field(default=30, description="请求超时时间(秒)")
    scraper_max_retries: int = Field(default=3, description="最大重试次数")
    scraper_concurrent_requests: int = Field(default=10, description="并发请求数")
    
    # 代理配置
    proxy_enabled: bool = Field(default=False, description="是否启用代理")
    proxy_host: Optional[str] = Field(default=None, description="代理主机")
    proxy_port: Optional[int] = Field(default=None, description="代理端口")
    proxy_username: Optional[str] = Field(default=None, description="代理用户名")
    proxy_password: Optional[str] = Field(default=None, description="代理密码")
    
    # 数据库配置
    database_url: str = Field(default="sqlite:///data/scraped_data.db", description="数据库URL")
    mongodb_url: str = Field(default="mongodb://localhost:27017/", description="MongoDB URL")
    redis_url: str = Field(default="redis://localhost:6379/", description="Redis URL")
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_file: str = Field(default="logs/scraping.log", description="日志文件路径")
    
    # 用户代理配置
    user_agent_rotation: bool = Field(default=True, description="是否轮换用户代理")
    custom_user_agent: Optional[str] = Field(default=None, description="自定义用户代理")
    
    # 输出配置
    output_format: str = Field(default="json", description="输出格式")
    output_dir: str = Field(default="output/", description="输出目录")
    
    # 请求头配置
    default_headers: dict = Field(
        default_factory=lambda: {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        },
        description="默认请求头"
    )
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }
    
    @property
    def proxy_url(self) -> Optional[str]:
        """获取代理URL"""
        if not self.proxy_enabled or not all([self.proxy_host, self.proxy_port]):
            return None
        
        if self.proxy_username and self.proxy_password:
            return f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}"
        return f"http://{self.proxy_host}:{self.proxy_port}"
    
    @property
    def user_agents(self) -> List[str]:
        """获取用户代理列表"""
        if self.custom_user_agent:
            return [self.custom_user_agent]
        
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
        ]


# 全局配置实例
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """获取全局配置实例"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """重新加载配置"""
    global _settings
    _settings = Settings()
    return _settings
