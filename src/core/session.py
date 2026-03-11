import random
import time
from typing import Optional, Dict, Any
import requests
from fake_useragent import UserAgent
from ..config import get_settings


class SessionManager:
    """会话管理器，负责管理HTTP会话和请求配置"""
    
    def __init__(self):
        self.settings = get_settings()
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()
    
    def _setup_session(self):
        """设置会话配置"""
        # 设置代理
        if self.settings.proxy_enabled and self.settings.proxy_url:
            self.session.proxies = {
                'http': self.settings.proxy_url,
                'https': self.settings.proxy_url
            }
        
        # 设置默认请求头
        self.session.headers.update(self.settings.default_headers)
        
        # 设置超时
        self.session.timeout = self.settings.scraper_timeout
    
    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = self.settings.default_headers.copy()
        
        if self.settings.user_agent_rotation:
            try:
                headers['User-Agent'] = random.choice(self.settings.user_agents)
            except:
                headers['User-Agent'] = self.ua.random
        elif self.settings.custom_user_agent:
            headers['User-Agent'] = self.settings.custom_user_agent
        
        return headers
    
    def add_delay(self):
        """添加请求延迟"""
        if self.settings.scraper_delay > 0:
            time.sleep(self.settings.scraper_delay)
    
    def make_request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> requests.Response:
        """发起HTTP请求"""
        kwargs.setdefault('headers', self.get_headers())
        kwargs.setdefault('timeout', self.settings.scraper_timeout)
        
        max_retries = self.settings.scraper_max_retries
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                self.add_delay()
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                last_exception = e
                if attempt < max_retries:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                continue
        
        raise last_exception
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """GET请求"""
        return self.make_request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """POST请求"""
        return self.make_request('POST', url, **kwargs)
    
    def close(self):
        """关闭会话"""
        self.session.close()
