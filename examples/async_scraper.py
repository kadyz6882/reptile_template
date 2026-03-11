#!/usr/bin/env python3
"""
异步爬虫示例
演示如何使用异步爬虫进行高效的并发抓取
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import AsyncScraper, ParselParser
from src.data import JSONStorage, DataCleaner
from src.loggers import get_logger


class AsyncExampleScraper(AsyncScraper):
    """异步示例爬虫"""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("async_scraper").get_logger()
        self.parser = ParselParser()
        self.cleaner = DataCleaner()
        self.storage = JSONStorage("output")
    
    async def parse(self, content):
        """解析网页内容"""
        self.logger.info("开始解析页面内容")
        
        # 使用Parsel解析器
        parsed_data = self.parser.parse(content)
        
        # 清洗数据
        cleaned_data = self.cleaner.process(parsed_data)
        
        self.logger.info(f"解析完成，提取到 {len(cleaned_data)} 个字段")
        return cleaned_data


async def main():
    """异步主函数"""
    scraper = AsyncExampleScraper()
    
    # 要爬取的URL列表
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://httpbin.org/robots.txt",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers",
        "https://example.com",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2"
    ]
    
    try:
        scraper.logger.info(f"开始异步爬取 {len(urls)} 个URL")
        
        # 异步爬取多个页面
        results = await scraper.scrape_multiple(urls, max_concurrent=4)
        
        # 保存结果
        success_count = 0
        for i, result in enumerate(results):
            if isinstance(result, dict) and 'error' not in result:
                filename = f"async_example_{i+1}"
                if scraper.storage.save(result, filename):
                    success_count += 1
                    scraper.logger.info(f"成功保存: {filename}")
                else:
                    scraper.logger.error(f"保存失败: {filename}")
            elif isinstance(result, Exception):
                scraper.logger.error(f"爬取异常: {result}")
            else:
                scraper.logger.error(f"爬取失败: {result}")
        
        scraper.logger.info(f"异步爬取完成，成功: {success_count}/{len(urls)}")
        
    except KeyboardInterrupt:
        scraper.logger.info("用户中断爬取")
    except Exception as e:
        scraper.logger.error(f"爬取过程中发生错误: {e}")
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
