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
            
            # 演示自动创建目录功能
            print("\n🔧 演示自动目录创建功能...")
            
            try:
                from src.data import JSONStorage
                from src.loggers import get_logger
                
                # 演示数据存储和目录创建
                print("📁 创建示例数据文件...")
                storage = JSONStorage("output")
                sample_data = [
                    {
                        "title": "示例数据",
                        "url": "https://example.com",
                        "content": "这是Reptile Template v3.0.0创建的示例数据",
                        "created_at": "2024-03-12T00:00:00",
                        "version": "3.0.0"
                    }
                ]
                success = storage.save(sample_data, "demo_data")
                if success and os.path.exists("output/demo_data.json"):
                    print("✅ output目录已创建，示例数据已保存")
                else:
                    print("❌ 数据保存失败")
                
                # 演示日志系统
                print("📝 创建示例日志...")
                logger = get_logger("demo")
                logger_instance = logger.get_logger()  # 获取实际的logger实例
                logger_instance.info("Reptile Template v3.0.0 演示日志")
                logger_instance.success("自动目录创建功能正常")
                
                if os.path.exists("logs"):
                    print("✅ logs目录已创建，日志系统正常")
                else:
                    print("❌ 日志目录创建失败")
                    
                print("\n📊 生成的文件:")
                if os.path.exists("output"):
                    print("  📁 output/ - 数据输出目录")
                    if os.path.exists("output/demo_data.json"):
                        print("    📄 demo_data.json - 示例数据文件")
                
                if os.path.exists("logs"):
                    print("  📁 logs/ - 日志目录")
                    log_files = [f for f in os.listdir("logs") if f.endswith(".log")]
                    for log_file in log_files:
                        print(f"    📄 {log_file}")
                
                print("\n🎯 目录自动创建功能验证完成！")
                
            except Exception as e:
                print(f"❌ 演示功能失败: {e}")
            
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
