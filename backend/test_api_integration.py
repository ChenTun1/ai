#!/usr/bin/env python3
"""
PetVoyageAI API 端到端集成测试
模拟完整用户使用流程:
  1. 健康检查
  2. 创建宠物（上传照片）
  3. 查询宠物列表
  4. 查询景点列表
  5. 生成照片（选择宠物+景点）
  6. 查询生成状态
  7. 保存照片
  8. 查询照片列表

用法:
  python test_api_integration.py [--base-url http://localhost:8000]
"""

import sys
import time
import argparse
import io
from dataclasses import dataclass, field

try:
    import httpx
except ImportError:
    print("缺少依赖: httpx")
    print("请运行: pip install httpx")
    sys.exit(1)


BASE_URL = "http://localhost:8000"


@dataclass
class TestContext:
    """在测试步骤间传递数据"""
    pet_id: int | None = None
    location_id: int | None = None
    task_id: str | None = None
    photo_id: int | None = None
    results: list = field(default_factory=list)


def print_step(step_num: int, title: str):
    print(f"\n{'─' * 50}")
    print(f"  测试 {step_num}: {title}")
    print(f"{'─' * 50}")


def print_pass(msg: str):
    print(f"  [PASS] {msg}")


def print_fail(msg: str):
    print(f"  [FAIL] {msg}")


def print_info(msg: str):
    print(f"  [INFO] {msg}")


def check_response_structure(resp_json: dict) -> bool:
    """验证统一响应结构 {code, message, data}"""
    return (
        isinstance(resp_json, dict)
        and "code" in resp_json
        and "message" in resp_json
        and "data" in resp_json
    )


# ─── 测试步骤 ─────────────────────────────────────────────


def test_health_check(client: httpx.Client, ctx: TestContext) -> bool:
    """测试 1: 健康检查"""
    print_step(1, "健康检查")
    try:
        resp = client.get("/health")
        if resp.status_code != 200:
            print_fail(f"状态码 {resp.status_code}, 期望 200")
            return False

        data = resp.json()
        if data.get("status") != "healthy":
            print_fail(f"健康状态异常: {data}")
            return False

        print_pass(f"服务正常 - {data.get('service')} v{data.get('version')}")
        return True
    except httpx.ConnectError:
        print_fail(f"无法连接到 {BASE_URL}, 请确认服务已启动")
        return False
    except Exception as e:
        print_fail(f"异常: {e}")
        return False


def test_create_pet(client: httpx.Client, ctx: TestContext) -> bool:
    """测试 2: 创建宠物（带照片上传）"""
    print_step(2, "创建宠物（带照片上传）")
    try:
        # 创建一张简单的 1x1 PNG 图片作为测试文件
        png_header = (
            b'\x89PNG\r\n\x1a\n'  # PNG signature
            b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
            b'\x08\x02\x00\x00\x00\x90wS\xde'  # 1x1 RGB
            b'\x00\x00\x00\x0cIDATx'
            b'\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N'
            b'\x00\x00\x00\x00IEND\xaeB`\x82'
        )

        files = {"photo": ("test_pet.png", io.BytesIO(png_header), "image/png")}
        form_data = {
            "name": "integration_test_pet",
            "type": "dog",
            "breed": "柯基",
        }

        resp = client.post("/api/v1/pets", data=form_data, files=files)
        if resp.status_code != 200:
            print_fail(f"状态码 {resp.status_code}, 期望 200")
            print_info(f"响应: {resp.text[:300]}")
            return False

        body = resp.json()
        if not check_response_structure(body):
            print_fail(f"响应结构异常: {body}")
            return False

        if body["code"] != 0:
            print_fail(f"业务错误: code={body['code']}, message={body['message']}")
            return False

        pet_data = body["data"]
        ctx.pet_id = pet_data["id"]

        print_pass(f"宠物创建成功 - id={ctx.pet_id}, name={pet_data['name']}")
        print_info(f"类型: {pet_data['type']}, 品种: {pet_data.get('breed')}")
        print_info(f"头像: {pet_data.get('avatar_url', '无')}")
        return True
    except Exception as e:
        print_fail(f"异常: {e}")
        return False


def test_list_pets(client: httpx.Client, ctx: TestContext) -> bool:
    """测试 3: 查询宠物列表"""
    print_step(3, "查询宠物列表")
    try:
        resp = client.get("/api/v1/pets")
        if resp.status_code != 200:
            print_fail(f"状态码 {resp.status_code}, 期望 200")
            return False

        body = resp.json()
        if not check_response_structure(body) or body["code"] != 0:
            print_fail(f"响应异常: {body}")
            return False

        items = body["data"]["items"]
        total = body["data"]["total"]
        print_pass(f"查询成功 - 共 {total} 只宠物")

        # 确认之前创建的宠物在列表中
        found = any(p["id"] == ctx.pet_id for p in items)
        if found:
            print_pass(f"已验证新创建的宠物 (id={ctx.pet_id}) 在列表中")
        else:
            print_fail(f"未找到新创建的宠物 (id={ctx.pet_id})")
            return False

        return True
    except Exception as e:
        print_fail(f"异常: {e}")
        return False


def test_list_locations(client: httpx.Client, ctx: TestContext) -> bool:
    """测试 4: 查询景点列表"""
    print_step(4, "查询景点列表")
    try:
        resp = client.get("/api/v1/locations")
        if resp.status_code != 200:
            print_fail(f"状态码 {resp.status_code}, 期望 200")
            return False

        body = resp.json()
        if not check_response_structure(body) or body["code"] != 0:
            print_fail(f"响应异常: {body}")
            return False

        items = body["data"]["items"]
        total = body["data"]["total"]
        print_pass(f"查询成功 - 共 {total} 个景点")

        if total == 0:
            print_info("景点列表为空，请先运行 init_locations.py 初始化数据")
            print_info("跳过后续依赖景点的测试")
            return True

        # 取第一个景点用于后续生成测试
        first = items[0]
        ctx.location_id = first["id"]
        print_info(f"选取景点: {first['name']} ({first['name_en']}), id={ctx.location_id}")

        # 测试筛选功能
        resp2 = client.get("/api/v1/locations", params={"limit": 5})
        body2 = resp2.json()
        if resp2.status_code == 200 and body2["code"] == 0:
            print_pass(f"分页查询成功 - 返回 {len(body2['data']['items'])} 条")

        return True
    except Exception as e:
        print_fail(f"异常: {e}")
        return False


def test_generate_photo(client: httpx.Client, ctx: TestContext) -> bool:
    """测试 5: 发起照片生成"""
    print_step(5, "发起照片生成")

    if ctx.pet_id is None:
        print_fail("前置条件不满足: 缺少 pet_id")
        return False
    if ctx.location_id is None:
        print_fail("前置条件不满足: 缺少 location_id (景点列表可能为空)")
        return False

    try:
        payload = {
            "pet_id": ctx.pet_id,
            "location_id": ctx.location_id,
            "style": "realistic",
            "season": "summer",
            "time_of_day": "sunset",
        }

        resp = client.post("/api/v1/photos/generate", json=payload)
        if resp.status_code != 200:
            print_fail(f"状态码 {resp.status_code}, 期望 200")
            print_info(f"响应: {resp.text[:300]}")
            return False

        body = resp.json()
        if not check_response_structure(body) or body["code"] != 0:
            print_fail(f"响应异常: {body}")
            return False

        ctx.task_id = body["data"]["task_id"]
        status = body["data"]["status"]

        print_pass(f"照片生成已提交 - task_id={ctx.task_id}, status={status}")
        return True
    except Exception as e:
        print_fail(f"异常: {e}")
        return False


def test_check_generation_status(client: httpx.Client, ctx: TestContext) -> bool:
    """测试 6: 查询照片生成状态"""
    print_step(6, "查询照片生成状态")

    if ctx.task_id is None:
        print_fail("前置条件不满足: 缺少 task_id")
        return False

    try:
        max_attempts = 10
        for attempt in range(1, max_attempts + 1):
            resp = client.get(f"/api/v1/photos/generate/{ctx.task_id}")
            if resp.status_code != 200:
                print_fail(f"状态码 {resp.status_code}, 期望 200")
                return False

            body = resp.json()
            if not check_response_structure(body) or body["code"] != 0:
                print_fail(f"响应异常: {body}")
                return False

            task_data = body["data"]
            status = task_data["status"]
            progress = task_data["progress"]

            print_info(f"轮询 {attempt}/{max_attempts} - status={status}, progress={progress}%")

            if status == "completed":
                print_pass(f"照片生成完成 - image_url={task_data.get('image_url')}")
                return True
            elif status == "failed":
                print_fail(f"照片生成失败 - error={task_data.get('error')}")
                return False

            time.sleep(0.5)

        print_fail(f"超时: {max_attempts} 次轮询后仍未完成")
        return False
    except Exception as e:
        print_fail(f"异常: {e}")
        return False


def test_save_photo(client: httpx.Client, ctx: TestContext) -> bool:
    """测试 7: 保存生成的照片"""
    print_step(7, "保存生成的照片")

    if ctx.task_id is None:
        print_fail("前置条件不满足: 缺少 task_id")
        return False

    try:
        payload = {
            "task_id": ctx.task_id,
            "caption": "集成测试自动生成的照片",
        }

        resp = client.post("/api/v1/photos", json=payload)
        if resp.status_code != 200:
            print_fail(f"状态码 {resp.status_code}, 期望 200")
            print_info(f"响应: {resp.text[:300]}")
            return False

        body = resp.json()
        if not check_response_structure(body) or body["code"] != 0:
            print_fail(f"响应异常: {body}")
            return False

        photo_data = body["data"]
        ctx.photo_id = photo_data["id"]

        print_pass(f"照片保存成功 - id={ctx.photo_id}")
        print_info(f"风格: {photo_data['style']}, 季节: {photo_data['season']}, 时段: {photo_data['time_of_day']}")
        print_info(f"说明: {photo_data.get('caption')}")
        print_info(f"Prompt: {(photo_data.get('prompt') or '')[:80]}...")
        return True
    except Exception as e:
        print_fail(f"异常: {e}")
        return False


def test_list_photos(client: httpx.Client, ctx: TestContext) -> bool:
    """测试 8: 查询照片列表"""
    print_step(8, "查询照片列表")
    try:
        resp = client.get("/api/v1/photos")
        if resp.status_code != 200:
            print_fail(f"状态码 {resp.status_code}, 期望 200")
            return False

        body = resp.json()
        if not check_response_structure(body) or body["code"] != 0:
            print_fail(f"响应异常: {body}")
            return False

        items = body["data"]["items"]
        total = body["data"]["total"]
        print_pass(f"查询成功 - 共 {total} 张照片")

        # 验证刚保存的照片在列表中
        if ctx.photo_id is not None:
            found = any(p["id"] == ctx.photo_id for p in items)
            if found:
                print_pass(f"已验证新保存的照片 (id={ctx.photo_id}) 在列表中")
            else:
                print_fail(f"未找到新保存的照片 (id={ctx.photo_id})")
                return False

        # 测试按宠物筛选
        if ctx.pet_id is not None:
            resp2 = client.get("/api/v1/photos", params={"pet_id": ctx.pet_id})
            if resp2.status_code == 200:
                body2 = resp2.json()
                print_pass(f"按宠物筛选成功 - pet_id={ctx.pet_id}, 共 {body2['data']['total']} 张")

        return True
    except Exception as e:
        print_fail(f"异常: {e}")
        return False


# ─── 主流程 ──────────────────────────────────────────────


def main():
    global BASE_URL

    parser = argparse.ArgumentParser(description="PetVoyageAI API 集成测试")
    parser.add_argument("--base-url", default=BASE_URL, help=f"API 基地址 (默认: {BASE_URL})")
    args = parser.parse_args()
    BASE_URL = args.base_url

    print("=" * 60)
    print("  PetVoyageAI API 集成测试")
    print(f"  目标: {BASE_URL}")
    print("=" * 60)

    ctx = TestContext()

    tests = [
        ("健康检查", test_health_check),
        ("创建宠物", test_create_pet),
        ("查询宠物列表", test_list_pets),
        ("查询景点列表", test_list_locations),
        ("发起照片生成", test_generate_photo),
        ("查询生成状态", test_check_generation_status),
        ("保存照片", test_save_photo),
        ("查询照片列表", test_list_photos),
    ]

    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        for name, test_func in tests:
            try:
                passed = test_func(client, ctx)
            except Exception as e:
                print_fail(f"未捕获异常: {e}")
                passed = False
            ctx.results.append((name, passed))

    # 汇总结果
    print("\n" + "=" * 60)
    print("  测试结果汇总")
    print("=" * 60)

    passed_count = 0
    for name, passed in ctx.results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")
        if passed:
            passed_count += 1

    total = len(ctx.results)
    print(f"\n  通过: {passed_count}/{total}")
    print("=" * 60)

    if passed_count == total:
        print("\n  所有测试通过!")
    else:
        print(f"\n  {total - passed_count} 个测试失败，请检查日志。")

    return 0 if passed_count == total else 1


if __name__ == "__main__":
    sys.exit(main())
