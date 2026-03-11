import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Union
import requests
from bs4 import BeautifulSoup
from parsel import Selector
from .session import SessionManager
from ..config import get_settings


class BaseScraper(ABC):
    """基础爬虫类"""
    
    def __init__(self):
        self.settings = get_settings()
        self.session_manager = SessionManager()
    
    @abstractmethod
    def parse(self, response: requests.Response) -> Dict[str, Any]:
        """解析响应数据的抽象方法"""
        pass
    
    def scrape(self, url: str, **kwargs) -> Dict[str, Any]:
        """爬取单个URL"""
        try:
            response = self.session_manager.get(url, **kwargs)
            return self.parse(response)
        except Exception as e:
            return {"error": str(e), "url": url}
    
    def scrape_multiple(self, urls: List[str], **kwargs) -> List[Dict[str, Any]]:
        """爬取多个URL"""
        results = []
        for url in urls:
            result = self.scrape(url, **kwargs)
            results.append(result)
        return results
    
    def close(self):
        """关闭爬虫"""
        self.session_manager.close()


class AsyncScraper(ABC):
    """异步爬虫类"""
    
    def __init__(self):
        self.settings = get_settings()
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建异步会话"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.settings.scraper_timeout)
            
            connector_kwargs = {}
            if self.settings.proxy_enabled and self.settings.proxy_url:
                connector_kwargs['proxy'] = self.settings.proxy_url
            
            connector = aiohttp.TCPConnector(**connector_kwargs)
            
            headers = self.settings.default_headers.copy()
            if self.settings.user_agent_rotation:
                import random
                headers['User-Agent'] = random.choice(self.settings.user_agents)
            
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers=headers
            )
        
        return self._session
    
    async def _add_delay(self):
        """添加请求延迟"""
        if self.settings.scraper_delay > 0:
            await asyncio.sleep(self.settings.scraper_delay)
    
    @abstractmethod
    async def parse(self, response: Union[str, aiohttp.ClientResponse]) -> Dict[str, Any]:
        """解析响应数据的抽象方法"""
        pass
    
    async def scrape(self, url: str, **kwargs) -> Dict[str, Any]:
        """异步爬取单个URL"""
        session = await self._get_session()
        max_retries = self.settings.scraper_max_retries
        
        for attempt in range(max_retries + 1):
            try:
                await self._add_delay()
                async with session.get(url, **kwargs) as response:
                    response.raise_for_status()
                    content = await response.text()
                    return await self.parse(content)
            except Exception as e:
                if attempt == max_retries:
                    return {"error": str(e), "url": url}
                await asyncio.sleep((2 ** attempt) + 0.5)
    
    async def scrape_multiple(
        self, 
        urls: List[str], 
        max_concurrent: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """异步爬取多个URL"""
        if max_concurrent is None:
            max_concurrent = self.settings.scraper_concurrent_requests
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_with_semaphore(url: str):
            async with semaphore:
                return await self.scrape(url)
        
        tasks = [scrape_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def close(self):
        """关闭异步爬虫"""
        if self._session and not self._session.closed:
            await self._session.close()


class SimpleScraper(BaseScraper):
    """简单爬虫实现示例"""
    
    def parse(self, response: requests.Response) -> Dict[str, Any]:
        """简单的解析实现"""
        soup = BeautifulSoup(response.content, 'html.parser')
        selector = Selector(text=response.text)
        
        return {
            "url": response.url,
            "status_code": response.status_code,
            "title": soup.title.string if soup.title else "",
            "content": soup.get_text()[:1000],  # 限制内容长度
            "headers": dict(response.headers),
            "selector_example": selector.css("title::text").get()
        }
