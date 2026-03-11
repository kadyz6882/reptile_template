#!/usr/bin/env python3
"""
基础爬虫示例
演示如何使用爬虫模板进行简单的网页抓取
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import SimpleScraper, BeautifulSoupParser
from src.data import StorageManager, DataCleaner
from src.loggers import get_logger


class BasicExampleScraper(SimpleScraper):
    """基础示例爬虫"""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("basic_scraper").get_logger()
        self.parser = BeautifulSoupParser()
        self.cleaner = DataCleaner()
        self.storage = StorageManager()
    
    def parse(self, response):
        """解析网页内容"""
        self.logger.info(f"开始解析页面: {response.url}")
        
        # 使用BeautifulSoup解析器
        parsed_data = self.parser.parse(response.text)
        
        # 添加额外的爬取信息
        data = {
            "url": response.url,
            "status_code": response.status_code,
            "content_length": len(response.content),
            "response_time": response.elapsed.total_seconds() if response.elapsed else 0,
            **parsed_data
        }
        
        # 清洗数据
        cleaned_data = self.cleaner.process(data)
        
        self.logger.info(f"解析完成，提取到 {len(cleaned_data)} 个字段")
        return cleaned_data


def main():
    """主函数"""
    scraper = BasicExampleScraper()
    
    # 要爬取的URL列表
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://example.com"
    ]
    
    try:
        # 爬取多个页面
        results = scraper.scrape_multiple(urls)
        
        # 保存结果
        success_count = 0
        for i, result in enumerate(results):
            if 'error' not in result:
                filename = f"basic_example_{i+1}"
                if scraper.storage.save(result, filename):
                    success_count += 1
                    scraper.logger.info(f"成功保存: {filename}")
                else:
                    scraper.logger.error(f"保存失败: {filename}")
            else:
                scraper.logger.error(f"爬取失败: {result.get('url', 'Unknown')} - {result.get('error')}")
        
        scraper.logger.info(f"爬取完成，成功: {success_count}/{len(urls)}")
        
    except KeyboardInterrupt:
        scraper.logger.info("用户中断爬取")
    except Exception as e:
        scraper.logger.error(f"爬取过程中发生错误: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
