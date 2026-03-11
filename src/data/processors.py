import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import pandas as pd
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


class DataProcessor:
    """数据处理器基类"""
    
    def process(self, data: Union[Dict, List[Dict]]) -> Union[Dict, List[Dict]]:
        """处理数据"""
        if isinstance(data, list):
            return [self._process_item(item) for item in data]
        return self._process_item(data)
    
    def _process_item(self, item: Dict) -> Dict:
        """处理单个数据项"""
        return item


class DataCleaner(DataProcessor):
    """数据清洗器"""
    
    def _process_item(self, item: Dict) -> Dict:
        """清洗单个数据项"""
        cleaned = {}
        
        for key, value in item.items():
            if value is None:
                cleaned[key] = ""
            elif isinstance(value, str):
                cleaned[key] = self._clean_text(value)
            else:
                cleaned[key] = value
        
        return cleaned
    
    def _clean_text(self, text: str) -> str:
        """清洗文本"""
        if not isinstance(text, str):
            return str(text) if text else ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除控制字符
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # 移除首尾空白
        text = text.strip()
        
        return text
    
    def remove_html_tags(self, text: str) -> str:
        """移除HTML标签"""
        if not isinstance(text, str):
            return str(text) if text else ""
        
        # 使用BeautifulSoup移除HTML标签
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()
    
    def extract_urls(self, text: str, base_url: str = "") -> List[str]:
        """提取并标准化URL"""
        if not isinstance(text, str):
            return []
        
        # 简单的URL正则表达式
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        # 标准化URL
        normalized_urls = []
        for url in urls:
            if base_url and not url.startswith(('http://', 'https://')):
                url = urljoin(base_url, url)
            normalized_urls.append(url)
        
        return normalized_urls
    
    def extract_emails(self, text: str) -> List[str]:
        """提取邮箱地址"""
        if not isinstance(text, str):
            return []
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    def extract_phone_numbers(self, text: str) -> List[str]:
        """提取电话号码"""
        if not isinstance(text, str):
            return []
        
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        return re.findall(phone_pattern, text)


class DataValidator(DataProcessor):
    """数据验证器"""
    
    def __init__(self, required_fields: Optional[List[str]] = None):
        self.required_fields = required_fields or []
    
    def _process_item(self, item: Dict) -> Dict:
        """验证单个数据项"""
        validated = item.copy()
        validated['_is_valid'] = self._is_valid(item)
        validated['_validation_errors'] = self._get_validation_errors(item)
        return validated
    
    def _is_valid(self, item: Dict) -> bool:
        """检查数据是否有效"""
        # 检查必需字段
        for field in self.required_fields:
            if field not in item or not item[field]:
                return False
        
        # 检查URL格式
        if 'url' in item and item['url']:
            if not self._is_valid_url(item['url']):
                return False
        
        # 检查邮箱格式
        if 'email' in item and item['email']:
            if not self._is_valid_email(item['email']):
                return False
        
        return True
    
    def _get_validation_errors(self, item: Dict) -> List[str]:
        """获取验证错误信息"""
        errors = []
        
        # 检查必需字段
        for field in self.required_fields:
            if field not in item:
                errors.append(f"缺少必需字段: {field}")
            elif not item[field]:
                errors.append(f"字段为空: {field}")
        
        # 检查URL格式
        if 'url' in item and item['url']:
            if not self._is_valid_url(item['url']):
                errors.append(f"无效的URL格式: {item['url']}")
        
        # 检查邮箱格式
        if 'email' in item and item['email']:
            if not self._is_valid_email(item['email']):
                errors.append(f"无效的邮箱格式: {item['email']}")
        
        return errors
    
    def _is_valid_url(self, url: str) -> bool:
        """验证URL格式"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _is_valid_email(self, email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class DataTransformer(DataProcessor):
    """数据转换器"""
    
    def __init__(self, transformations: Optional[Dict[str, callable]] = None):
        self.transformations = transformations or {}
    
    def _process_item(self, item: Dict) -> Dict:
        """转换单个数据项"""
        transformed = item.copy()
        
        for field, transform_func in self.transformations.items():
            if field in transformed:
                try:
                    transformed[field] = transform_func(transformed[field])
                except Exception as e:
                    print(f"转换字段 {field} 失败: {e}")
        
        return transformed
    
    def add_transformation(self, field: str, transform_func: callable):
        """添加字段转换规则"""
        self.transformations[field] = transform_func
    
    def remove_transformation(self, field: str):
        """移除字段转换规则"""
        if field in self.transformations:
            del self.transformations[field]


class DataDeduplicator(DataProcessor):
    """数据去重器"""
    
    def __init__(self, unique_fields: Optional[List[str]] = None):
        self.unique_fields = unique_fields or ['url']
        self.seen_values = set()
    
    def process(self, data: Union[Dict, List[Dict]]) -> List[Dict]:
        """去重处理"""
        if isinstance(data, dict):
            data = [data]
        
        unique_data = []
        for item in data:
            unique_key = self._get_unique_key(item)
            if unique_key not in self.seen_values:
                self.seen_values.add(unique_key)
                unique_data.append(item)
        
        return unique_data
    
    def _get_unique_key(self, item: Dict) -> str:
        """获取唯一标识"""
        key_parts = []
        for field in self.unique_fields:
            value = item.get(field, '')
            key_parts.append(str(value))
        return '|'.join(key_parts)
    
    def reset(self):
        """重置去重状态"""
        self.seen_values.clear()


class DataEnricher(DataProcessor):
    """数据增强器"""
    
    def _process_item(self, item: Dict) -> Dict:
        """增强单个数据项"""
        enriched = item.copy()
        
        # 添加处理时间戳
        enriched['processed_at'] = datetime.now().isoformat()
        
        # 添加域名信息
        if 'url' in enriched and enriched['url']:
            enriched['domain'] = self._extract_domain(enriched['url'])
        
        # 添加文本统计信息
        if 'content' in enriched and enriched['content']:
            content_stats = self._get_content_stats(enriched['content'])
            enriched.update({f'content_{k}': v for k, v in content_stats.items()})
        
        return enriched
    
    def _extract_domain(self, url: str) -> str:
        """提取域名"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return ""
    
    def _get_content_stats(self, content: str) -> Dict[str, int]:
        """获取内容统计信息"""
        if not isinstance(content, str):
            content = str(content) if content else ""
        
        return {
            'length': len(content),
            'word_count': len(content.split()),
            'sentence_count': len(re.split(r'[.!?]+', content)),
            'paragraph_count': len([p for p in content.split('\n') if p.strip()])
        }
