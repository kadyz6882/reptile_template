import time
import random
import asyncio
from functools import wraps
from typing import Any, Callable
import logging


def get_random_delay(min_delay: float = 0.5, max_delay: float = 2.0) -> float:
    """获取随机延迟时间"""
    return random.uniform(min_delay, max_delay)


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        sleep_time = delay * (2 ** attempt) + random.uniform(0, 1)
                        time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator


def rate_limiter(calls_per_second: float = 1.0):
    """速率限制器"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


async def async_rate_limiter(calls_per_second: float = 1.0):
    """异步速率限制器"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    async def limit():
        elapsed = time.time() - last_called[0]
        if elapsed < min_interval:
            await asyncio.sleep(min_interval - elapsed)
        last_called[0] = time.time()
    
    return limit


def setup_logging(level: str = "INFO"):
    """设置日志"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def chunk_list(lst: list, chunk_size: int) -> list:
    """将列表分块"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    """扁平化字典"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
