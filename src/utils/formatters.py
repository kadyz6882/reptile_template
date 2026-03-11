import time
from datetime import datetime
from typing import Union


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def format_duration(seconds: Union[int, float]) -> str:
    """格式化时间长度"""
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}分钟"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f}小时"
    else:
        days = seconds / 86400
        return f"{days:.1f}天"


def format_timestamp(timestamp: Union[str, float, datetime], format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化时间戳"""
    if isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            return timestamp
    elif isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp)
    elif isinstance(timestamp, datetime):
        dt = timestamp
    else:
        return str(timestamp)
    
    return dt.strftime(format)


def format_number(number: Union[int, float], decimal_places: int = 2) -> str:
    """格式化数字"""
    if isinstance(number, int):
        return f"{number:,}"
    elif isinstance(number, float):
        return f"{number:,.{decimal_places}f}"
    else:
        return str(number)


def format_percentage(value: float, total: float, decimal_places: int = 1) -> str:
    """格式化百分比"""
    if total == 0:
        return "0%"
    
    percentage = (value / total) * 100
    return f"{percentage:.{decimal_places}f}%"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """截断文本"""
    if not isinstance(text, str):
        text = str(text)
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_url(url: str, max_length: int = 50) -> str:
    """格式化URL显示"""
    if not isinstance(url, str):
        return str(url)
    
    if len(url) <= max_length:
        return url
    
    # 尝试保留域名部分
    from urllib.parse import urlparse
    parsed = urlparse(url)
    
    if parsed.netloc:
        domain = parsed.netloc
        path = parsed.path
        
        if len(domain) + 3 <= max_length:
            remaining = max_length - len(domain) - 3
            if len(path) > remaining:
                path = path[:remaining] + "..."
            return f"{domain}{path}"
    
    return url[:max_length - 3] + "..."
