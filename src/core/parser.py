from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from bs4 import BeautifulSoup, Tag
from parsel import Selector
import re


class BaseParser(ABC):
    """基础解析器类"""
    
    @abstractmethod
    def parse(self, content: Union[str, BeautifulSoup, Selector]) -> Dict[str, Any]:
        """解析内容的抽象方法"""
        pass


class BeautifulSoupParser(BaseParser):
    """BeautifulSoup解析器"""
    
    def __init__(self, parser: str = 'html.parser'):
        self.parser = parser
    
    def parse(self, content: Union[str, BeautifulSoup, Selector]) -> Dict[str, Any]:
        """使用BeautifulSoup解析内容"""
        if isinstance(content, str):
            soup = BeautifulSoup(content, self.parser)
        elif isinstance(content, BeautifulSoup):
            soup = content
        else:  # Selector
            soup = BeautifulSoup(content.get(), self.parser)
        
        return {
            "title": self._get_title(soup),
            "meta": self._get_meta_info(soup),
            "links": self._get_links(soup),
            "images": self._get_images(soup),
            "text": self._get_clean_text(soup),
            "headings": self._get_headings(soup)
        }
    
    def _get_title(self, soup: BeautifulSoup) -> str:
        """获取页面标题"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ""
    
    def _get_meta_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """获取meta信息"""
        meta_info = {}
        meta_tags = soup.find_all('meta')
        
        for tag in meta_tags:
            name = tag.get('name') or tag.get('property')
            content = tag.get('content')
            if name and content:
                meta_info[name] = content
        
        return meta_info
    
    def _get_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """获取所有链接"""
        links = []
        for link in soup.find_all('a', href=True):
            links.append({
                "text": link.get_text().strip(),
                "href": link['href'],
                "title": link.get('title', '')
            })
        return links
    
    def _get_images(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """获取所有图片"""
        images = []
        for img in soup.find_all('img', src=True):
            images.append({
                "src": img['src'],
                "alt": img.get('alt', ''),
                "title": img.get('title', '')
            })
        return images
    
    def _get_clean_text(self, soup: BeautifulSoup) -> str:
        """获取清理后的文本"""
        # 移除script和style标签
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        # 清理多余的空白字符
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:2000]  # 限制文本长度
    
    def _get_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """获取标题层级"""
        headings = {}
        for level in range(1, 7):
            tags = soup.find_all(f'h{level}')
            headings[f'h{level}'] = [tag.get_text().strip() for tag in tags]
        return headings


class ParselParser(BaseParser):
    """Parsel解析器（支持CSS选择器和XPath）"""
    
    def parse(self, content: Union[str, BeautifulSoup, Selector]) -> Dict[str, Any]:
        """使用Parsel解析内容"""
        if isinstance(content, str):
            selector = Selector(text=content)
        elif isinstance(content, Selector):
            selector = content
        else:  # BeautifulSoup
            selector = Selector(text=str(content))
        
        return {
            "title": self._extract_title(selector),
            "meta": self._extract_meta(selector),
            "links": self._extract_links(selector),
            "images": self._extract_images(selector),
            "text": self._extract_text(selector),
            "headings": self._extract_headings(selector)
        }
    
    def _extract_title(self, selector: Selector) -> str:
        """提取标题"""
        return selector.css("title::text").get("").strip()
    
    def _extract_meta(self, selector: Selector) -> Dict[str, str]:
        """提取meta信息"""
        meta_info = {}
        
        # 提取name meta标签
        name_metas = selector.css("meta[name]")
        for meta in name_metas:
            name = meta.css("::attr(name)").get()
            content = meta.css("::attr(content)").get()
            if name and content:
                meta_info[name] = content
        
        # 提取property meta标签
        property_metas = selector.css("meta[property]")
        for meta in property_metas:
            property_name = meta.css("::attr(property)").get()
            content = meta.css("::attr(content)").get()
            if property_name and content:
                meta_info[property_name] = content
        
        return meta_info
    
    def _extract_links(self, selector: Selector) -> List[Dict[str, str]]:
        """提取链接"""
        links = []
        for link in selector.css("a[href]"):
            links.append({
                "text": link.css("::text").get("").strip(),
                "href": link.css("::attr(href)").get(),
                "title": link.css("::attr(title)").get("")
            })
        return links
    
    def _extract_images(self, selector: Selector) -> List[Dict[str, str]]:
        """提取图片"""
        images = []
        for img in selector.css("img[src]"):
            images.append({
                "src": img.css("::attr(src)").get(),
                "alt": img.css("::attr(alt)").get(""),
                "title": img.css("::attr(title)").get("")
            })
        return images
    
    def _extract_text(self, selector: Selector) -> str:
        """提取文本"""
        # 移除script和style
        text = selector.css("body ::text").getall()
        # 清理和合并文本
        clean_text = " ".join([t.strip() for t in text if t.strip()])
        return clean_text[:2000]
    
    def _extract_headings(self, selector: Selector) -> Dict[str, List[str]]:
        """提取标题"""
        headings = {}
        for level in range(1, 7):
            heading_texts = selector.css(f"h{level}::text").getall()
            headings[f"h{level}"] = [t.strip() for t in heading_texts if t.strip()]
        return headings


class RegexParser:
    """正则表达式解析器"""
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """提取邮箱地址"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """提取电话号码"""
        pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """提取URL"""
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_prices(text: str) -> List[str]:
        """提取价格信息"""
        pattern = r'[$¥£€]\s?\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s?[$¥£€]'
        return re.findall(pattern, text)
