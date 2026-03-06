"""
数据库初始化脚本
- 创建所有表
- 导入景点初始数据
- 创建测试用户（可选）
"""

import sys
import os

# 将 backend 目录加入 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import init_db, SessionLocal
from app.models.location import Location
from app.models.user import User
from scripts.init_locations import get_locations


def seed_locations(db):
    """导入景点数据"""
    existing_count = db.query(Location).count()
    if existing_count > 0:
        print(f"  景点表已有 {existing_count} 条数据，跳过导入")
        return

    locations = get_locations()
    for loc_data in locations:
        location = Location(**loc_data)
        db.add(location)

    db.commit()
    print(f"  成功导入 {len(locations)} 个景点")


def seed_test_user(db):
    """创建测试用户"""
    existing = db.query(User).filter(User.phone == "13800000000").first()
    if existing:
        print("  测试用户已存在，跳过创建")
        return

    test_user = User(
        phone="13800000000",
        username="测试用户",
        bio="这是一个测试账号",
        subscription_type="free",
        daily_quota_total=3,
    )
    db.add(test_user)
    db.commit()
    print("  成功创建测试用户 (手机: 13800000000)")


def main():
    print("=" * 50)
    print("PetVoyageAI 数据库初始化")
    print("=" * 50)

    # 1. 创建所有表
    print("\n[1/3] 创建数据库表...")
    init_db()

    # 2. 导入景点数据
    print("\n[2/3] 导入景点数据...")
    db = SessionLocal()
    try:
        seed_locations(db)

        # 3. 创建测试用户
        print("\n[3/3] 创建测试用户...")
        seed_test_user(db)
    finally:
        db.close()

    print("\n" + "=" * 50)
    print("数据库初始化完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
