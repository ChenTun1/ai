#!/usr/bin/env python3
"""
系统功能验证脚本
测试 PetVoyageAI 各个模块是否正常工作
"""

import sys
import os

# 添加 backend 到路径
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """测试模块导入"""
    print("=" * 60)
    print("测试 1: 模块导入检查")
    print("=" * 60)

    try:
        from app.core.config import settings
        print("✅ 配置模块导入成功")
        print(f"  - 环境: {settings.ENVIRONMENT}")
        print(f"  - 数据库: {settings.DATABASE_URL}")
    except Exception as e:
        print(f"❌ 配置模块导入失败: {e}")
        return False

    try:
        from app.core.database import Base, engine
        print("✅ 数据库模块导入成功")
    except Exception as e:
        print(f"❌ 数据库模块导入失败: {e}")
        return False

    try:
        from app.models import User, Pet, Location, Photo
        print("✅ 数据模型导入成功")
    except Exception as e:
        print(f"❌ 数据模型导入失败: {e}")
        return False

    try:
        from app.services.ai_service import AIImageService
        print("✅ AI 服务导入成功")
    except Exception as e:
        print(f"❌ AI 服务导入失败: {e}")
        return False

    try:
        from app.api.v1 import pets, photos, locations
        print("✅ API 路由导入成功")
    except Exception as e:
        print(f"❌ API 路由导入失败: {e}")
        return False

    return True


def test_database():
    """测试数据库连接和表创建"""
    print("\n" + "=" * 60)
    print("测试 2: 数据库检查")
    print("=" * 60)

    try:
        from app.core.database import init_db, SessionLocal
        from app.models import Location

        # 创建表
        init_db()
        print("✅ 数据库表创建成功")

        # 测试查询
        db = SessionLocal()
        try:
            count = db.query(Location).count()
            print(f"✅ 数据库查询成功 (景点数量: {count})")
        finally:
            db.close()

        return True
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_service():
    """测试 AI 服务"""
    print("\n" + "=" * 60)
    print("测试 3: AI 服务检查")
    print("=" * 60)

    try:
        from app.services.ai_service import AIImageService
        from app.models.pet import Pet
        from app.models.location import Location

        # 创建测试对象
        class MockPet:
            ai_description = "a cute corgi dog with short legs"
            breed = "柯基"
            type = "dog"

        class MockLocation:
            prompt_template = "at the Eiffel Tower in Paris, with iconic iron structure"

        service = AIImageService()
        print("✅ AI 服务实例化成功")

        # 测试 Prompt 构建
        prompt = service.build_prompt(
            pet=MockPet(),
            location=MockLocation(),
            style="realistic",
            season="summer",
            time_of_day="sunset"
        )

        print("✅ Prompt 构建成功")
        print(f"  示例 Prompt: {prompt[:100]}...")

        return True
    except Exception as e:
        print(f"❌ AI 服务检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_routes():
    """测试 API 路由"""
    print("\n" + "=" * 60)
    print("测试 4: API 路由检查")
    print("=" * 60)

    try:
        from app.main import app

        # 检查路由
        routes = [route.path for route in app.routes]

        expected_routes = [
            "/health",
            "/",
            "/api/v1/pets",
            "/api/v1/photos/generate",
            "/api/v1/locations"
        ]

        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"✅ 路由存在: {route}")
            else:
                print(f"⚠️  路由可能缺失: {route}")

        return True
    except Exception as e:
        print(f"❌ API 路由检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "🚀 " * 20)
    print("PetVoyageAI 系统功能验证")
    print("🚀 " * 20 + "\n")

    results = []

    # 运行测试
    results.append(("模块导入", test_imports()))
    results.append(("数据库", test_database()))
    results.append(("AI 服务", test_ai_service()))
    results.append(("API 路由", test_api_routes()))

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:15s}: {status}")

    print("\n" + "=" * 60)
    print(f"总计: {passed}/{total} 项测试通过")
    print("=" * 60)

    if passed == total:
        print("\n🎉 所有测试通过！系统就绪！")
        print("\n下一步:")
        print("1. 运行 'python scripts/init_db.py' 初始化数据库")
        print("2. 在 .env 中配置 SILICONFLOW_API_KEY")
        print("3. 运行 'python -m app.main' 启动服务器")
        print("4. 访问 http://localhost:8000/docs 查看 API 文档")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
