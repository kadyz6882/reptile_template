#!/usr/bin/env python3
"""
自定义爬虫示例
演示如何创建自定义的爬虫来抓取特定网站
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import BaseScraper
from src.data import JSONStorage, DataValidator, DataEnricher
from src.loggers import get_logger
from src.utils import retry_on_failure


class NewsScraper(BaseScraper):
    """新闻网站爬虫示例"""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("news_scraper").get_logger()
        self.storage = JSONStorage("output")
        self.validator = DataValidator(required_fields=['title', 'url', 'content'])
        self.enricher = DataEnricher()
    
    @retry_on_failure(max_retries=3)
    def parse(self, response):
        """解析新闻页面"""
        self.logger.info(f"开始解析新闻页面: {response.url}")
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 提取新闻标题
        title = self._extract_title(soup)
        
        # 提取新闻内容
        content = self._extract_content(soup)
        
        # 提取发布时间
        publish_date = self._extract_publish_date(soup)
        
        # 提取作者信息
        author = self._extract_author(soup)
        
        # 提取图片
        images = self._extract_images(soup, response.url)
        
        # 构建数据结构
        news_data = {
            "url": response.url,
            "title": title,
            "content": content,
            "publish_date": publish_date,
            "author": author,
            "images": images,
            "status_code": response.status_code,
            "scraped_at": response.headers.get('date', '')
        }
        
        # 验证数据
        validated_data = self.validator.process(news_data)
        
        # 增强数据
        enriched_data = self.enricher.process(validated_data)
        
        self.logger.info(f"新闻解析完成: {title}")
        return enriched_data
    
    def _extract_title(self, soup):
        """提取标题"""
        # 尝试多种标题选择器
        selectors = [
            'h1',
            '.title',
            '.headline',
            '.article-title',
            '[data-testid="headline"]',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip()
                if title and len(title) > 5:  # 确保标题有意义
                    return title
        
        return ""
    
    def _extract_content(self, soup):
        """提取正文内容"""
        # 移除不需要的元素
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # 尝试多种内容选择器
        selectors = [
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            'article',
            '.main-content',
            '[data-testid="article-body"]'
        ]
        
        for selector in selectors:
            content_element = soup.select_one(selector)
            if content_element:
                content = content_element.get_text().strip()
                if len(content) > 100:  # 确保内容有意义
                    return content[:2000]  # 限制长度
        
        # 如果没有找到特定的内容区域，尝试获取body的文本
        body = soup.find('body')
        if body:
            return body.get_text().strip()[:2000]
        
        return ""
    
    def _extract_publish_date(self, soup):
        """提取发布时间"""
        # 尝试多种时间选择器
        selectors = [
            'time',
            '.date',
            '.publish-date',
            '.timestamp',
            '[datetime]',
            '.article-date'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # 尝试从datetime属性获取
                date_str = element.get('datetime') or element.get_text().strip()
                if date_str:
                    return date_str
        
        return ""
    
    def _extract_author(self, soup):
        """提取作者信息"""
        # 尝试多种作者选择器
        selectors = [
            '.author',
            '.byline',
            '.writer',
            '[data-testid="author"]',
            '.article-author'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                author = element.get_text().strip()
                if author and len(author) > 1:
                    return author
        
        return ""
    
    def _extract_images(self, soup, base_url):
        """提取图片信息"""
        images = []
        img_tags = soup.find_all('img', src=True)
        
        for img in img_tags:
            src = img['src']
            alt = img.get('alt', '')
            
            # 处理相对URL
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                from urllib.parse import urljoin
                src = urljoin(base_url, src)
            
            images.append({
                "src": src,
                "alt": alt
            })
        
        return images[:5]  # 限制图片数量


def main():
    """主函数"""
    scraper = NewsScraper()
    
    # 新闻网站URL示例（实际使用时请替换为真实的新闻网站）
    urls = [
        "https://httpbin.org/html",  # 示例URL
        # "https://news.example.com/article1",
        # "https://news.example.com/article2",
    ]
    
    try:
        scraper.logger.info(f"开始爬取 {len(urls)} 个新闻页面")
        
        results = scraper.scrape_multiple(urls)
        
        # 保存有效的新闻数据
        valid_news = []
        for result in results:
            if 'error' not in result and result.get('_is_valid', False):
                valid_news.append(result)
            else:
                scraper.logger.warning(f"无效数据: {result.get('url', 'Unknown')}")
        
        if valid_news:
            if scraper.storage.save(valid_news, "news_articles"):
                scraper.logger.info(f"成功保存 {len(valid_news)} 篇新闻")
            else:
                scraper.logger.error("保存新闻失败")
        else:
            scraper.logger.warning("没有有效的新闻数据")
        
        scraper.logger.info(f"新闻爬取完成，有效新闻: {len(valid_news)}/{len(urls)}")
        
    except KeyboardInterrupt:
        scraper.logger.info("用户中断爬取")
    except Exception as e:
        scraper.logger.error(f"爬取过程中发生错误: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
