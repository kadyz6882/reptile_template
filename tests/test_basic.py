#!/usr/bin/env python3
"""
基础测试
测试爬虫模板的核心功能
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 确保能找到src模块
try:
    from src.config.settings import Settings, get_settings
    from src.core.scraper import SimpleScraper
    from src.core.parser import BeautifulSoupParser, ParselParser
    from src.data.storage import JSONStorage, CSVStorage
    from src.data.processors import DataCleaner, DataValidator
    from src.utils.validators import validate_url, validate_email
    from src.utils.formatters import format_size, format_duration
except ImportError as e:
    print(f"导入错误: {e}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path[:3]}")
    raise


class TestConfig(unittest.TestCase):
    """测试配置管理"""
    
    def test_settings_creation(self):
        """测试配置创建"""
        settings = Settings()
        self.assertIsInstance(settings.scraper_delay, float)
        self.assertIsInstance(settings.scraper_timeout, int)
        self.assertTrue(settings.scraper_max_retries >= 0)
    
    def test_get_settings(self):
        """测试全局配置获取"""
        settings = get_settings()
        self.assertIsInstance(settings, Settings)


class TestParsers(unittest.TestCase):
    """测试解析器"""
    
    def setUp(self):
        """设置测试数据"""
        self.html_content = """
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test description">
            </head>
            <body>
                <h1>Main Title</h1>
                <p>This is a test paragraph.</p>
                <a href="https://example.com">Test Link</a>
                <img src="test.jpg" alt="Test Image">
            </body>
        </html>
        """
    
    def test_beautifulsoup_parser(self):
        """测试BeautifulSoup解析器"""
        parser = BeautifulSoupParser()
        result = parser.parse(self.html_content)
        
        self.assertIn('title', result)
        self.assertIn('meta', result)
        self.assertIn('links', result)
        self.assertIn('images', result)
        self.assertEqual(result['title'], 'Test Page')
    
    def test_parsel_parser(self):
        """测试Parsel解析器"""
        parser = ParselParser()
        result = parser.parse(self.html_content)
        
        self.assertIn('title', result)
        self.assertIn('meta', result)
        self.assertIn('links', result)
        self.assertIn('images', result)
        self.assertEqual(result['title'], 'Test Page')


class TestDataProcessors(unittest.TestCase):
    """测试数据处理器"""
    
    def setUp(self):
        """设置测试数据"""
        self.test_data = {
            "title": "  Test Title  ",
            "content": "Test content with   extra   spaces",
            "url": "https://example.com",
            "email": "test@example.com"
        }
    
    def test_data_cleaner(self):
        """测试数据清洗"""
        cleaner = DataCleaner()
        result = cleaner.process(self.test_data)
        
        self.assertEqual(result['title'], "Test Title")
        self.assertEqual(result['content'], "Test content with extra spaces")
    
    def test_data_validator(self):
        """测试数据验证"""
        validator = DataValidator(required_fields=['title', 'url'])
        result = validator.process(self.test_data)
        
        self.assertTrue(result['_is_valid'])
        self.assertEqual(len(result['_validation_errors']), 0)
        
        # 测试无效数据
        invalid_data = {"title": "Test"}  # 缺少url字段
        result = validator.process(invalid_data)
        self.assertFalse(result['_is_valid'])
        self.assertGreater(len(result['_validation_errors']), 0)


class TestStorage(unittest.TestCase):
    """测试存储功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = "test_output"
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.test_data = [
            {"title": "Test 1", "url": "https://example1.com"},
            {"title": "Test 2", "url": "https://example2.com"}
        ]
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_json_storage(self):
        """测试JSON存储"""
        storage = JSONStorage(self.test_dir)
        
        # 测试保存
        success = storage.save(self.test_data, "test")
        self.assertTrue(success)
        self.assertTrue(storage.exists("test"))
        
        # 测试加载
        loaded_data = storage.load("test")
        self.assertEqual(len(loaded_data), 2)
        self.assertEqual(loaded_data[0]['title'], "Test 1")
    
    def test_csv_storage(self):
        """测试CSV存储"""
        storage = CSVStorage(self.test_dir)
        
        # 测试保存
        success = storage.save(self.test_data, "test")
        self.assertTrue(success)
        self.assertTrue(storage.exists("test"))
        
        # 测试加载
        loaded_data = storage.load("test")
        self.assertEqual(len(loaded_data), 2)
        self.assertEqual(loaded_data[0]['title'], "Test 1")


class TestUtils(unittest.TestCase):
    """测试工具函数"""
    
    def test_validators(self):
        """测试验证器"""
        # 测试URL验证
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("http://test.org"))
        self.assertFalse(validate_url("invalid-url"))
        self.assertFalse(validate_url(""))
        
        # 测试邮箱验证
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name@domain.co.uk"))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("@example.com"))
    
    def test_formatters(self):
        """测试格式化工具"""
        # 测试大小格式化
        self.assertEqual(format_size(1024), "1.0KB")
        self.assertEqual(format_size(1048576), "1.0MB")
        self.assertEqual(format_size(0), "0B")
        
        # 测试时间格式化
        self.assertEqual(format_duration(30), "30.0秒")
        self.assertEqual(format_duration(120), "2.0分钟")
        self.assertEqual(format_duration(7200), "2.0小时")


class TestScraper(unittest.TestCase):
    """测试爬虫功能"""
    
    def test_simple_scraper_creation(self):
        """测试简单爬虫创建"""
        scraper = SimpleScraper()
        self.assertIsNotNone(scraper.session_manager)
        self.assertIsNotNone(scraper.settings)
        scraper.close()


if __name__ == '__main__':
    unittest.main()
