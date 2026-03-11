import re
from typing import Optional
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """验证URL格式"""
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """验证电话号码格式"""
    if not phone or not isinstance(phone, str):
        return False
    
    # 简单的电话号码验证
    pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    return bool(re.match(pattern, phone))


def validate_ip_address(ip: str) -> bool:
    """验证IP地址格式"""
    if not ip or not isinstance(ip, str):
        return False
    
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    # 检查每个数字是否在0-255范围内
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)


def validate_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
    """验证日期格式"""
    if not date_str or not isinstance(date_str, str):
        return False
    
    try:
        from datetime import datetime
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def is_empty(value: Any) -> bool:
    """检查值是否为空"""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) == 0
    return False


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    if not isinstance(filename, str):
        filename = str(filename)
    
    # 移除或替换非法字符
    illegal_chars = r'[<>:"/\\|?*]'
    filename = re.sub(illegal_chars, '_', filename)
    
    # 移除多余的空格和点
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'\.+', '.', filename)
    
    # 限制长度
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + '.' + ext if ext else name[:255]
    
    return filename.strip(' .')
