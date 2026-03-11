#!/usr/bin/env python3
"""
测试运行脚本
确保新用户克隆项目后能正常运行测试
"""

import sys
import os

def main():
    """主函数"""
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = script_dir
    
    # 添加项目根目录到Python路径
    sys.path.insert(0, project_root)
    
    print(f"项目根目录: {project_root}")
    print(f"Python路径: {sys.path[0]}")
    
    try:
        # 测试基本导入
        print("测试基本导入...")
        from src.config.settings import Settings, get_settings
        from src.core.scraper import SimpleScraper
        from src.data.storage import JSONStorage
        from src.data.processors import DataCleaner
        print("✅ 基本导入成功")
        
        # 运行单元测试
        print("运行单元测试...")
        import unittest
        
        # 发现并运行测试
        loader = unittest.TestLoader()
        start_dir = os.path.join(project_root, 'tests')
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("\n🎉 所有测试通过！模板可以正常使用。")
            return 0
        else:
            print(f"\n❌ 测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
            return 1
            
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保:")
        print("1. 在项目根目录运行此脚本")
        print("2. 已安装所有依赖: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
