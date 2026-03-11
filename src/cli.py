#!/usr/bin/env python3
"""
命令行接口
提供简单的CLI工具来运行爬虫
"""

import click
import asyncio
import sys
import os
from typing import List

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core import SimpleScraper, AsyncScraper
from src.data import StorageManager
from src.config import get_settings
from src.loggers import get_logger


@click.group()
@click.version_option(version="3.0.0")
def cli():
    """Reptile Template - 通用爬虫模板"""
    pass


@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--output', '-o', default='scraped_data', help='输出文件名')
@click.option('--format', '-f', default='json', type=click.Choice(['json', 'csv', 'database']), help='输出格式')
@click.option('--async', 'use_async', is_flag=True, help='使用异步爬虫')
@click.option('--concurrent', '-c', default=5, help='并发请求数（仅异步模式）')
def scrape(urls: List[str], output: str, format: str, use_async: bool, concurrent: int):
    """爬取指定的URL列表"""
    
    if not urls:
        click.echo("错误: 请提供至少一个URL")
        return
    
    click.echo(f"开始爬取 {len(urls)} 个URL...")
    click.echo(f"输出格式: {format}")
    click.echo(f"输出文件: {output}")
    
    if use_async:
        click.echo(f"使用异步模式，并发数: {concurrent}")
        asyncio.run(_async_scrape(urls, output, format, concurrent))
    else:
        click.echo("使用同步模式")
        _sync_scrape(urls, output, format)


def _sync_scrape(urls: List[str], output: str, format: str):
    """同步爬取"""
    scraper = SimpleScraper()
    storage = StorageManager()
    logger = get_logger("cli").get_logger()
    
    try:
        results = scraper.scrape_multiple(urls)
        
        # 过滤有效结果
        valid_results = [r for r in results if 'error' not in r]
        
        if storage.save(valid_results, output, format):
            click.echo(f"成功保存 {len(valid_results)} 条记录")
        else:
            click.echo("保存失败")
    
    except Exception as e:
        click.echo(f"爬取过程中发生错误: {e}")
        logger.error(f"爬取错误: {e}")
    finally:
        scraper.close()


async def _async_scrape(urls: List[str], output: str, format: str, concurrent: int):
    """异步爬取"""
    scraper = AsyncScraper()
    storage = StorageManager()
    logger = get_logger("cli").get_logger()
    
    try:
        results = await scraper.scrape_multiple(urls, max_concurrent=concurrent)
        
        # 过滤有效结果
        valid_results = []
        for result in results:
            if isinstance(result, dict) and 'error' not in result:
                valid_results.append(result)
            else:
                logger.error(f"爬取失败: {result}")
        
        if storage.save(valid_results, output, format):
            click.echo(f"成功保存 {len(valid_results)} 条记录")
        else:
            click.echo("保存失败")
    
    except Exception as e:
        click.echo(f"爬取过程中发生错误: {e}")
        logger.error(f"爬取错误: {e}")
    finally:
        await scraper.close()


@cli.command()
def config():
    """显示当前配置"""
    settings = get_settings()
    
    click.echo("当前配置:")
    click.echo(f"  请求延迟: {settings.scraper_delay}秒")
    click.echo(f"  请求超时: {settings.scraper_timeout}秒")
    click.echo(f"  最大重试: {settings.scraper_max_retries}次")
    click.echo(f"  并发请求: {settings.scraper_concurrent_requests}")
    click.echo(f"  代理启用: {settings.proxy_enabled}")
    click.echo(f"  输出格式: {settings.output_format}")
    click.echo(f"  输出目录: {settings.output_dir}")
    click.echo(f"  日志级别: {settings.log_level}")
    click.echo(f"  日志文件: {settings.log_file}")


@cli.command()
@click.argument('filename')
@click.option('--format', '-f', default='json', type=click.Choice(['json', 'csv']), help='文件格式')
def convert(filename: str, format: str):
    """转换数据文件格式"""
    storage = StorageManager()
    
    try:
        if format == 'json':
            data = storage.json_storage.load(filename)
            # 保存为CSV
            storage.csv_storage.save(data, filename)
            click.echo(f"已将 {filename}.json 转换为 {filename}.csv")
        
        elif format == 'csv':
            data = storage.csv_storage.load(filename)
            # 保存为JSON
            storage.json_storage.save(data, filename)
            click.echo(f"已将 {filename}.csv 转换为 {filename}.json")
    
    except Exception as e:
        click.echo(f"转换失败: {e}")


if __name__ == '__main__':
    cli()


def main():
    """CLI主入口点，供pyproject.toml使用"""
    cli()
