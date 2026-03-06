# 🗺️ PetVoyageAI 产品路线图

## 分阶段实现方案

本文档提供**从0到1**的完整实现路径，每个阶段都有明确的功能、技术方案和验收标准。

---

## 📅 总览

| 阶段 | 周期 | 核心功能 | 交付物 |
|------|------|---------|--------|
| **Phase 0** | 1周 | API调研与Demo验证 | 可运行的图片生成脚本 |
| **Phase 1** | 2-3周 | 核心生成功能 | 宠物上传 + AI生成 + 保存 |
| **Phase 2** | 2-3周 | 地图解锁系统 | 虚拟地图 + 收集进度 |
| **Phase 3** | 2周 | 四季/地域主题 | 动态背景 + 主题切换 |
| **Phase 4** | 2周 | 社交分享 | 朋友圈 + 分享海报 |

---

## 🎯 Phase 0: API调研与验证（1周）

### 目标
确定最合适的AI图像生成API，并验证技术可行性。

### API对比方案

#### 方案A：硅基流动（SiliconFlow）⭐ 推荐

**优势**：
- ✅ 国内可访问，速度快
- ✅ 价格便宜（~¥0.01-0.05/张）
- ✅ 支持多种模型（Stable Diffusion、FLUX等）
- ✅ 有Image-to-Image能力

**API示例**：
```python
import requests

url = "https://api.siliconflow.cn/v1/image/generations"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "stabilityai/stable-diffusion-xl-base-1.0",
    "prompt": "a corgi dog at Eiffel Tower, realistic photography",
    "image_size": "1024x1024",
    "num_inference_steps": 20
}

response = requests.post(url, json=payload, headers=headers)
image_url = response.json()["images"][0]["url"]
```

**成本**：约¥0.02/张

---

#### 方案B：豆包（字节跳动）

**优势**：
- ✅ 大厂背书，稳定性好
- ✅ 国内服务器
- ✅ 可能有免费额度

**缺点**：
- ❓ API文档不如硅基流动完善
- ❓ 需要企业认证可能性

---

#### 方案C：文心一言（百度）

**优势**：
- ✅ 成熟稳定
- ✅ 有免费额度
- ✅ 文档完善

**缺点**：
- ❌ 图像生成质量一般
- ❌ 定制化能力弱

---

### 验证任务

创建一个独立的Python脚本，验证以下功能：

**1. 基础文生图**
```python
# test_text_to_image.py
# 功能：输入文字描述，生成宠物在景点的照片
# 验证：质量、速度、成本

prompt = "一只柯基狗在埃菲尔铁塔前，阳光明媚，专业摄影"
# 调用API生成图片
```

**2. Image-to-Image（如果API支持）**
```python
# test_image_to_image.py
# 功能：上传宠物照片作为参考，生成新场景
# 验证：是否能保持宠物特征

reference_image = "my_dog.jpg"
prompt = "这只狗在长城前，中国传统建筑背景"
# 调用API生成
```

**3. 批量测试**
- 测试不同景点：城市、自然景观、地标建筑
- 测试不同宠物：猫、狗、不同品种
- 测试不同风格：真实照片、动漫、像素风

**验收标准**：
- ✅ 能成功生成图片
- ✅ 质量可接受（80%以上满意）
- ✅ 速度可接受（< 30秒）
- ✅ 成本可接受（< ¥0.1/张）

---

## 🎨 Phase 1: 核心生成功能（2-3周）

### 产品功能

#### 1.1 宠物管理

**功能流程**：
```
打开App → 首次引导 → 添加宠物
    ↓
点击"添加我的宠物"
    ↓
拍照或从相册选择（1-3张照片）
    ↓
填写宠物信息（名字、种类、品种）
    ↓
保存 → 进入主页
```

**前端界面设计**：

**添加宠物页面**：
```
┌────────────────────────────┐
│  ← 添加我的宠物             │
├────────────────────────────┤
│                             │
│    ┌─────────────────┐     │
│    │                 │     │
│    │   📷  点击上传   │     │
│    │   宠物照片       │     │
│    │                 │     │
│    └─────────────────┘     │
│                             │
│  宠物名字                    │
│  ┌─────────────────────┐   │
│  │ 请输入名字...        │   │
│  └─────────────────────┘   │
│                             │
│  宠物类型                    │
│  ┌───┐ ┌───┐ ┌───┐         │
│  │🐕狗│ │🐈猫│ │🐰其他│      │
│  └───┘ └───┘ └───┘         │
│                             │
│  品种（可选）                │
│  ┌─────────────────────┐   │
│  │ 例如：柯基            │   │
│  └─────────────────────┘   │
│                             │
│  ┌─────────────────────┐   │
│  │   保存并开始旅行 🎉   │   │
│  └─────────────────────┘   │
└────────────────────────────┘
```

**数据存储**：
```json
{
  "id": "pet-001",
  "user_id": "user-xxx",
  "name": "旺财",
  "type": "dog",
  "breed": "柯基",
  "photos": [
    "https://cdn.petvoyage.ai/pets/xxx-1.jpg"
  ],
  "ai_description": "一只短腿黄白色柯基犬，耳朵竖立，表情可爱",
  "created_at": "2024-03-06T10:00:00Z"
}
```

---

#### 1.2 景点选择与生成

**主页设计**：

```
┌────────────────────────────┐
│  🌍 旺财的环球之旅          │
├────────────────────────────┤
│                             │
│  我的宠物                    │
│  ┌────────────────────┐    │
│  │ 🐕 旺财              │    │
│  │ 已去过 12 个地方     │    │
│  └────────────────────┘    │
│                             │
│  选择目的地 🎯               │
│                             │
│  🔥 热门景点                 │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐      │
│  │埃│ │长│ │自│ │东│      │
│  │菲│ │城│ │由│ │京│      │
│  │尔│ │  │ │女│ │塔│      │
│  │铁│ │  │ │神│ │  │      │
│  │塔│ │  │ │像│ │  │      │
│  └──┘ └──┘ └──┘ └──┘      │
│                             │
│  🌏 按地区                   │
│  • 亚洲 (15个景点)           │
│  • 欧洲 (20个景点)           │
│  • 美洲 (12个景点)           │
│  • 其他 (8个景点)            │
│                             │
│  ┌─────────────────────┐   │
│  │  ✨ 生成我的照片      │   │
│  └─────────────────────┘   │
└────────────────────────────┘
```

**景点详情页**：

```
┌────────────────────────────┐
│  ← 埃菲尔铁塔 🗼             │
├────────────────────────────┤
│  ┌──────────────────────┐  │
│  │                      │  │
│  │  [景点预览图]         │  │
│  │                      │  │
│  └──────────────────────┘  │
│                             │
│  📍 法国 · 巴黎              │
│  ⭐ 已有 12,345 位旅行家打卡  │
│                             │
│  选择风格                    │
│  ┌───┐ ┌───┐ ┌───┐         │
│  │真实│ │像素│ │动漫│         │
│  │照片│ │风格│ │风格│         │
│  └─✓─┘ └───┘ └───┘         │
│                             │
│  选择季节                    │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐  │
│  │🌸春│ │☀️夏│ │🍁秋│ │❄️冬│  │
│  └───┘ └─✓─┘ └───┘ └───┘  │
│                             │
│  选择时间                    │
│  ┌───┐ ┌───┐ ┌───┐         │
│  │🌅日│ │🌇黄│ │🌃夜│         │
│  │出 │ │昏 │ │晚 │         │
│  └───┘ └─✓─┘ └───┘         │
│                             │
│  ┌─────────────────────┐   │
│  │  🎨 开始生成 (3张)    │   │
│  └─────────────────────┘   │
└────────────────────────────┘
```

**生成中状态**：

```
┌────────────────────────────┐
│                             │
│         ⏳                  │
│                             │
│    正在为旺财生成照片...     │
│                             │
│    [========>   ] 65%       │
│                             │
│    预计还需15秒              │
│                             │
└────────────────────────────┘
```

**生成结果页**：

```
┌────────────────────────────┐
│  ← 选择最喜欢的照片          │
├────────────────────────────┤
│  ┌──────────────────────┐  │
│  │                      │  │
│  │  [生成的照片 1]       │  │
│  │  旺财 @ 埃菲尔铁塔    │  │
│  │                      │  │
│  └──────────────────────┘  │
│             ❤️ 选择此照片    │
│                             │
│  ┌──────────────────────┐  │
│  │  [生成的照片 2]       │  │
│  └──────────────────────┘  │
│             🔁 选择此照片    │
│                             │
│  ┌──────────────────────┐  │
│  │  [生成的照片 3]       │  │
│  └──────────────────────┘  │
│             ✓ 选择此照片    │
│                             │
│  ┌─────────────────────┐   │
│  │  💾 保存到相册        │   │
│  └─────────────────────┘   │
└────────────────────────────┘
```

---

#### 1.3 相册功能

**我的相册页面**：

```
┌────────────────────────────┐
│  📸 旺财的旅行相册           │
├────────────────────────────┤
│                             │
│  全部 (12)  本月 (3)  收藏  │
│  ────                       │
│                             │
│  ┌───┐ ┌───┐ ┌───┐         │
│  │ 📷│ │ 📷│ │ 📷│         │
│  │   │ │   │ │   │         │
│  └───┘ └───┘ └───┘         │
│  埃菲   长城   自由          │
│  尔塔         女神           │
│  3/6   3/5    3/1           │
│                             │
│  ┌───┐ ┌───┐ ┌───┐         │
│  │ 📷│ │ 📷│ │ 📷│         │
│  └───┘ └───┘ └───┘         │
│                             │
└────────────────────────────┘
```

**照片详情页**：

```
┌────────────────────────────┐
│  ← 📷                       │
├────────────────────────────┤
│  ┌──────────────────────┐  │
│  │                      │  │
│  │                      │  │
│  │  [照片大图]           │  │
│  │                      │  │
│  │                      │  │
│  └──────────────────────┘  │
│                             │
│  🐕 旺财 @ 埃菲尔铁塔 🗼      │
│  📍 法国 · 巴黎              │
│  🕐 2024年3月6日 黄昏时分    │
│  🎨 真实照片风格              │
│                             │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐      │
│  │❤️│ │💬│ │📤│ │🗑️│      │
│  │收│ │评│ │分│ │删│      │
│  │藏│ │论│ │享│ │除│      │
│  └──┘ └──┘ └──┘ └──┘      │
└────────────────────────────┘
```

---

### 后端API设计

#### API 1: 创建宠物
```
POST /api/v1/pets
Content-Type: multipart/form-data

参数:
- name: 宠物名字
- type: 宠物类型 (dog/cat/other)
- breed: 品种（可选）
- photos: 照片文件（1-3张）

响应:
{
  "code": 0,
  "data": {
    "id": "pet-001",
    "name": "旺财",
    "type": "dog",
    "breed": "柯基",
    "photos": ["https://..."],
    "ai_description": "一只短腿黄白色柯基犬..."
  }
}
```

**后端处理流程**：
1. 接收照片上传
2. 上传到OSS
3. 调用AI API提取宠物特征描述（可选）
4. 保存到数据库

---

#### API 2: 获取景点列表
```
GET /api/v1/locations?region=asia&category=landmark

响应:
{
  "code": 0,
  "data": [
    {
      "id": "loc-eiffel",
      "name": "埃菲尔铁塔",
      "name_en": "Eiffel Tower",
      "country": "法国",
      "city": "巴黎",
      "icon": "🗼",
      "preview_image": "https://...",
      "unlock_count": 12345,
      "is_unlocked": false
    }
  ]
}
```

---

#### API 3: 生成照片
```
POST /api/v1/photos/generate

请求:
{
  "pet_id": "pet-001",
  "location_id": "loc-eiffel",
  "style": "realistic",  // realistic | pixel | anime
  "season": "summer",    // spring | summer | autumn | winter
  "time": "sunset",      // sunrise | noon | sunset | night
  "num_outputs": 3
}

响应:
{
  "code": 0,
  "data": {
    "task_id": "task-xxx",
    "status": "processing",
    "estimated_time": 20
  }
}
```

**后端处理**：
1. 构建AI Prompt
2. 调用硅基流动API
3. 异步生成（Celery任务）
4. 完成后推送通知

**Prompt构建逻辑**：
```python
def build_prompt(pet, location, style, season, time):
    # 基础描述
    pet_desc = pet.ai_description or f"a {pet.breed} {pet.type}"

    # 地点描述
    location_desc = location.prompt_template

    # 季节描述
    season_map = {
        "spring": "spring season, cherry blossoms, fresh green leaves",
        "summer": "summer, bright sunshine, clear blue sky",
        "autumn": "autumn, golden leaves, warm colors",
        "winter": "winter, snow, cold atmosphere"
    }

    # 时间描述
    time_map = {
        "sunrise": "sunrise, golden hour, soft morning light",
        "noon": "midday, bright sunlight",
        "sunset": "sunset, golden hour, warm evening light",
        "night": "night time, city lights, dark sky"
    }

    # 风格描述
    style_map = {
        "realistic": "professional photography, high quality, 8k, realistic",
        "pixel": "pixel art style, 8-bit retro game graphics",
        "anime": "anime style, Studio Ghibli, animated illustration"
    }

    prompt = f"{pet_desc} at {location_desc}, {season_map[season]}, {time_map[time]}, {style_map[style]}"

    return prompt

# 示例输出：
# "a corgi dog at Eiffel Tower in Paris, summer, bright sunshine, clear blue sky, sunset, golden hour, warm evening light, professional photography, high quality, 8k, realistic"
```

---

#### API 4: 查询生成状态
```
GET /api/v1/photos/generate/{task_id}

响应:
{
  "code": 0,
  "data": {
    "task_id": "task-xxx",
    "status": "completed",  // processing | completed | failed
    "photos": [
      {
        "url": "https://cdn.petvoyage.ai/photos/xxx-1.jpg",
        "thumbnail": "https://cdn.petvoyage.ai/photos/xxx-1-thumb.jpg"
      },
      // ...2张
    ]
  }
}
```

---

#### API 5: 保存照片
```
POST /api/v1/photos

请求:
{
  "task_id": "task-xxx",
  "selected_index": 0,  // 选择第几张
  "pet_id": "pet-001",
  "location_id": "loc-eiffel"
}

响应:
{
  "code": 0,
  "data": {
    "photo_id": "photo-xxx",
    "unlocked_location": {
      "id": "loc-eiffel",
      "name": "埃菲尔铁塔"
    },
    "new_achievements": [
      {
        "id": "ach-first-europe",
        "name": "初探欧洲"
      }
    ]
  }
}
```

---

### 技术实现要点

#### 前端（iOS）

**技术栈**：
- Swift + SwiftUI
- Kingfisher（图片缓存）
- Alamofire（网络请求）

**关键代码**：
```swift
// 生成照片ViewModel
class PhotoGenerateViewModel: ObservableObject {
    @Published var generatingStatus: GeneratingStatus = .idle
    @Published var generatedPhotos: [Photo] = []

    func generatePhoto(pet: Pet, location: Location, options: GenerateOptions) async {
        generatingStatus = .generating(progress: 0)

        // 1. 发起生成请求
        let task = try await APIService.generatePhoto(
            petId: pet.id,
            locationId: location.id,
            style: options.style,
            season: options.season,
            time: options.time
        )

        // 2. 轮询查询状态
        while true {
            try await Task.sleep(nanoseconds: 2_000_000_000)  // 2秒

            let result = try await APIService.checkGenerateStatus(taskId: task.taskId)

            if result.status == .completed {
                generatedPhotos = result.photos
                generatingStatus = .completed
                break
            } else if result.status == .failed {
                generatingStatus = .failed(error: result.errorMessage)
                break
            }

            // 更新进度
            generatingStatus = .generating(progress: estimateProgress())
        }
    }
}
```

---

#### 后端（Python + FastAPI）

**关键代码**：
```python
# app/services/ai_service.py

import httpx
from app.core.config import settings

class AIImageService:
    """AI图像生成服务"""

    def __init__(self):
        self.api_url = "https://api.siliconflow.cn/v1/image/generations"
        self.api_key = settings.SILICONFLOW_API_KEY

    async def generate_image(
        self,
        prompt: str,
        style: str = "realistic",
        num_outputs: int = 3
    ) -> list[str]:
        """
        生成图片

        Args:
            prompt: 提示词
            style: 风格
            num_outputs: 生成数量

        Returns:
            图片URL列表
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "stabilityai/stable-diffusion-xl-base-1.0",
                    "prompt": prompt,
                    "image_size": "1024x1024",
                    "num_inference_steps": 20,
                    "batch_size": num_outputs
                }
            )

            result = response.json()
            image_urls = [img["url"] for img in result["images"]]

            return image_urls
```

```python
# app/api/v1/photos.py

from fastapi import APIRouter, Depends, BackgroundTasks
from app.services.ai_service import AIImageService
from app.services.prompt_builder import PromptBuilder
from app.tasks import generate_photo_task

router = APIRouter()

@router.post("/generate")
async def generate_photo(
    request: GeneratePhotoRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """生成照片"""

    # 1. 检查用户配额
    if not await check_user_quota(current_user.id):
        raise HTTPException(400, "今日生成次数已用完")

    # 2. 获取宠物和地点信息
    pet = await get_pet(request.pet_id)
    location = await get_location(request.location_id)

    # 3. 构建Prompt
    prompt = PromptBuilder.build(
        pet=pet,
        location=location,
        style=request.style,
        season=request.season,
        time=request.time
    )

    # 4. 创建任务
    task_id = str(uuid.uuid4())

    # 5. 异步生成（后台任务）
    background_tasks.add_task(
        generate_photo_task,
        task_id=task_id,
        user_id=current_user.id,
        prompt=prompt,
        num_outputs=request.num_outputs
    )

    return {
        "code": 0,
        "data": {
            "task_id": task_id,
            "status": "processing",
            "estimated_time": 20
        }
    }
```

---

### Phase 1 验收标准

- ✅ 用户可以添加宠物（上传照片、填写信息）
- ✅ 可以浏览景点列表
- ✅ 可以选择风格、季节、时间生成照片
- ✅ 生成3张照片供选择
- ✅ 保存照片到相册
- ✅ 查看已生成的照片
- ✅ 生成速度 < 30秒
- ✅ 生成成功率 > 90%

---

## 🗺️ Phase 2: 地图解锁系统（2-3周）

### 产品功能

#### 2.1 世界地图页面

**地图主页设计**：

```
┌────────────────────────────┐
│  🌍 世界地图                 │
├────────────────────────────┤
│                             │
│  我的进度                    │
│  ━━━━━━━━━━━━━━━━━━━━ 24%  │
│  12 / 50 个景点已解锁        │
│                             │
│  ┌──────────────────────┐  │
│  │                      │  │
│  │   [世界地图可视化]     │  │
│  │                      │  │
│  │   • 亚洲 ✓ 5/15       │  │
│  │   • 欧洲 ✓ 4/20       │  │
│  │   • 美洲   3/12       │  │
│  │   • 其他   0/3        │  │
│  │                      │  │
│  └──────────────────────┘  │
│                             │
│  按地区查看                  │
│  ┌────────┐ ┌────────┐    │
│  │ 🌏 亚洲 │ │ 🌍 欧洲 │    │
│  │  5/15  │ │  4/20  │    │
│  └────────┘ └────────┘    │
│  ┌────────┐ ┌────────┐    │
│  │ 🌎 美洲 │ │ 🌐 其他 │    │
│  │  3/12  │ │  0/3   │    │
│  └────────┘ └────────┘    │
└────────────────────────────┘
```

**大洲详情页（以亚洲为例）**：

```
┌────────────────────────────┐
│  ← 🌏 亚洲 (5/15)            │
├────────────────────────────┤
│                             │
│  中国 🇨🇳                    │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐      │
│  │✓ │ │✓ │ │  │ │  │      │
│  │长│ │故│ │兵│ │黄│      │
│  │城│ │宫│ │马│ │山│      │
│  └──┘ └──┘ │俑│ │  │      │
│            └──┘ └──┘      │
│                             │
│  日本 🇯🇵                    │
│  ┌──┐ ┌──┐ ┌──┐           │
│  │✓ │ │✓ │ │  │           │
│  │富│ │浅│ │清│           │
│  │士│ │草│ │水│           │
│  │山│ │寺│ │寺│           │
│  └──┘ └──┘ └──┘           │
│                             │
│  泰国 🇹🇭                    │
│  ┌──┐ ┌──┐               │
│  │✓ │ │  │               │
│  │大│ │玉│               │
│  │皇│ │佛│               │
│  │宫│ │寺│               │
│  └──┘ └──┘               │
└────────────────────────────┘
```

**地标解锁动画**：

生成并保存照片后触发：

```
┌────────────────────────────┐
│                             │
│         ✨ 恭喜！            │
│                             │
│    解锁新地标                │
│                             │
│      🗼                      │
│   埃菲尔铁塔                 │
│   法国 · 巴黎                │
│                             │
│  ┌─────────────────────┐   │
│  │  查看地图进度         │   │
│  └─────────────────────┘   │
│                             │
│  ┌─────────────────────┐   │
│  │  继续探索             │   │
│  └─────────────────────┘   │
└────────────────────────────┘
```

---

#### 2.2 收集进度

**个人统计页面**：

```
┌────────────────────────────┐
│  📊 我的旅行统计             │
├────────────────────────────┤
│                             │
│  🌍 已探索                   │
│  ┌───────────────────────┐ │
│  │ 12 个地标景点          │ │
│  │ 5 个国家               │ │
│  │ 3 个大洲               │ │
│  └───────────────────────┘ │
│                             │
│  🎨 照片统计                 │
│  ┌───────────────────────┐ │
│  │ 总照片数: 28 张        │ │
│  │ 真实风格: 15 张        │ │
│  │ 像素风格: 8 张         │ │
│  │ 动漫风格: 5 张         │ │
│  └───────────────────────┘ │
│                             │
│  🏆 成就徽章                 │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐    │
│  │🥇│ │🥈│ │🥉│ │  │    │
│  │初│ │亚│ │欧│ │环│    │
│  │探│ │洲│ │洲│ │球│    │
│  │险│ │通│ │通│ │旅│    │
│  └──┘ └──┘ └──┘ │行│    │
│                 │家│    │
│                 └──┘    │
│  已解锁 3/10              │
└────────────────────────────┘
```

---

### 后端实现

#### 数据库设计

**地点表（locations）**：
```sql
CREATE TABLE locations (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    continent VARCHAR(50),  -- asia, europe, americas, other
    country VARCHAR(100),
    city VARCHAR(100),
    category VARCHAR(50),  -- landmark, nature, city, culture
    icon VARCHAR(10),
    preview_image VARCHAR(500),
    description TEXT,
    unlock_points INT DEFAULT 10,
    unlock_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**解锁记录（user_unlocks）**：
```sql
CREATE TABLE user_unlocks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50) NOT NULL,
    location_id VARCHAR(50) NOT NULL,
    photo_id VARCHAR(50) NOT NULL,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_location (user_id, location_id)
);
```

**成就表（achievements）**：
```sql
CREATE TABLE achievements (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    icon VARCHAR(10),
    condition_type VARCHAR(50),  -- unlock_count, country_count, etc.
    condition_value INT,
    reward_points INT DEFAULT 0
);

-- 示例数据
INSERT INTO achievements VALUES
('ach-first', '初探险家', '解锁第一个景点', '🥇', 'unlock_count', 1, 10),
('ach-asia', '亚洲通', '解锁5个亚洲景点', '🌏', 'continent_unlock', 5, 50),
('ach-world', '环球旅行家', '解锁5个大洲', '🌍', 'continent_count', 5, 500);
```

**用户成就（user_achievements）**：
```sql
CREATE TABLE user_achievements (
    user_id VARCHAR(50),
    achievement_id VARCHAR(50),
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, achievement_id)
);
```

---

#### API实现

**API: 保存照片并解锁**
```python
@router.post("/photos")
async def save_photo(
    request: SavePhotoRequest,
    current_user: User = Depends(get_current_user)
):
    """保存照片并解锁地点"""

    # 1. 保存照片记录
    photo = await create_photo_record(
        user_id=current_user.id,
        pet_id=request.pet_id,
        location_id=request.location_id,
        image_url=request.image_url,
        style=request.style,
        season=request.season,
        time=request.time
    )

    # 2. 解锁地点
    is_first_unlock = await unlock_location(
        user_id=current_user.id,
        location_id=request.location_id,
        photo_id=photo.id
    )

    # 3. 检查成就
    new_achievements = []
    if is_first_unlock:
        new_achievements = await check_and_unlock_achievements(
            user_id=current_user.id
        )

    return {
        "code": 0,
        "data": {
            "photo": photo,
            "unlocked_location": await get_location(request.location_id),
            "new_achievements": new_achievements
        }
    }
```

**成就检查逻辑**：
```python
async def check_and_unlock_achievements(user_id: str) -> list[Achievement]:
    """检查并解锁成就"""
    new_achievements = []

    # 获取用户解锁统计
    stats = await get_user_unlock_stats(user_id)

    # 检查所有成就
    all_achievements = await get_all_achievements()

    for ach in all_achievements:
        # 已解锁则跳过
        if await is_achievement_unlocked(user_id, ach.id):
            continue

        # 检查条件
        if ach.condition_type == "unlock_count":
            if stats.total_unlocks >= ach.condition_value:
                await unlock_achievement(user_id, ach.id)
                new_achievements.append(ach)

        elif ach.condition_type == "continent_unlock":
            # 检查某个大洲的解锁数
            continent_unlocks = stats.by_continent.get(ach.continent, 0)
            if continent_unlocks >= ach.condition_value:
                await unlock_achievement(user_id, ach.id)
                new_achievements.append(ach)

        elif ach.condition_type == "continent_count":
            # 检查解锁的大洲数量
            if len(stats.by_continent) >= ach.condition_value:
                await unlock_achievement(user_id, ach.id)
                new_achievements.append(ach)

    return new_achievements
```

---

### Phase 2 验收标准

- ✅ 可以查看世界地图
- ✅ 生成照片后自动解锁对应地点
- ✅ 地图上显示已解锁/未解锁状态
- ✅ 显示解锁进度统计
- ✅ 达成条件时自动解锁成就
- ✅ 查看已获得的成就列表

---

## 🎨 Phase 3: 四季/地域主题（2周）

### 产品设计

#### 3.1 动态背景系统

**功能描述**：
- 根据选择的季节和时间，App背景/主题色动态变化
- 地图界面根据地域显示不同的视觉风格

**春季主题**：
```
颜色方案：
- 主色: 粉色 #FFB6C1
- 辅色: 嫩绿 #90EE90
- 背景: 浅粉 #FFF0F5

视觉元素：
- 樱花飘落动画
- 嫩芽图标
- 清新配色
```

**夏季主题**：
```
颜色方案：
- 主色: 天蓝 #87CEEB
- 辅色: 亮黄 #FFD700
- 背景: 浅蓝 #F0F8FF

视觉元素：
- 阳光光晕
- 海浪动画
- 明亮配色
```

**秋季主题**：
```
颜色方案：
- 主色: 橙色 #FF8C00
- 辅色: 棕色 #A0522D
- 背景: 米黄 #FFF8DC

视觉元素：
- 落叶动画
- 枫叶图标
- 温暖配色
```

**冬季主题**：
```
颜色方案：
- 主色: 冰蓝 #B0E0E6
- 辅色: 银白 #F5F5F5
- 背景: 雪白 #FFFAFA

视觉元素：
- 雪花飘落
- 冰晶图标
- 冷色调
```

---

#### 3.2 地域特色

**亚洲风格**：
- 配色：红色、金色（中国风）
- 字体：使用毛笔字效果
- 背景：水墨画风格

**欧洲风格**：
- 配色：蓝色、白色（地中海）
- 字体：优雅衬线字体
- 背景：古典建筑

**美洲风格**：
- 配色：绿色、棕色（自然）
- 字体：现代无衬线
- 背景：自由女神、大峡谷

---

### 技术实现

#### iOS实现

**主题管理器**：
```swift
// ThemeManager.swift

class ThemeManager: ObservableObject {
    @Published var currentTheme: AppTheme = .spring

    // 根据季节切换主题
    func switchTheme(for season: Season) {
        switch season {
        case .spring:
            currentTheme = .spring
        case .summer:
            currentTheme = .summer
        case .autumn:
            currentTheme = .autumn
        case .winter:
            currentTheme = .winter
        }
    }
}

struct AppTheme {
    let primaryColor: Color
    let secondaryColor: Color
    let backgroundColor: Color
    let backgroundAnimation: AnimationType

    static let spring = AppTheme(
        primaryColor: Color(hex: "#FFB6C1"),
        secondaryColor: Color(hex: "#90EE90"),
        backgroundColor: Color(hex: "#FFF0F5"),
        backgroundAnimation: .cherryBlossom
    )

    // ...其他季节
}
```

**背景动画**：
```swift
// BackgroundAnimationView.swift

struct CherryBlossomView: View {
    @State private var petals: [Petal] = []

    var body: some View {
        ZStack {
            ForEach(petals) { petal in
                Image("cherry_blossom")
                    .resizable()
                    .frame(width: 30, height: 30)
                    .position(petal.position)
                    .opacity(petal.opacity)
                    .rotationEffect(.degrees(petal.rotation))
            }
        }
        .onAppear {
            startAnimation()
        }
    }

    func startAnimation() {
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
            let newPetal = Petal(
                position: CGPoint(x: CGFloat.random(in: 0...UIScreen.main.bounds.width), y: -50),
                opacity: Double.random(in: 0.3...0.8),
                rotation: Double.random(in: 0...360)
            )
            petals.append(newPetal)

            // 移动花瓣
            withAnimation(.linear(duration: 10)) {
                if let index = petals.firstIndex(where: { $0.id == newPetal.id }) {
                    petals[index].position.y = UIScreen.main.bounds.height + 50
                }
            }
        }
    }
}
```

---

### Phase 3 验收标准

- ✅ 选择不同季节时，App主题自动切换
- ✅ 背景有对应季节的动画效果
- ✅ 不同地区的地图页有特色视觉
- ✅ 主题切换流畅自然
- ✅ 不影响性能

---

## 👥 Phase 4: 社交分享（2周）

### 产品功能

#### 4.1 分享海报生成

**功能流程**：
```
查看照片详情 → 点击"分享"
    ↓
自动生成精美海报
    ↓
选择分享渠道（微信/朋友圈/保存）
```

**海报设计**：

```
┌──────────────────────────────┐
│                               │
│   [顶部装饰 - 季节元素]         │
│                               │
│     ┌─────────────────┐      │
│     │                 │      │
│     │                 │      │
│     │  [照片]          │      │
│     │                 │      │
│     │                 │      │
│     └─────────────────┘      │
│                               │
│       🐕 旺财的巴黎之旅        │
│                               │
│       📍 埃菲尔铁塔            │
│       🕐 2024年3月6日 黄昏     │
│                               │
│   ┌───────────────────────┐  │
│   │ 扫码下载PetVoyageAI   │  │
│   │ 带你的宠物环游世界     │  │
│   │      [二维码]         │  │
│   └───────────────────────┘  │
│                               │
│   [底部装饰 - 品牌Logo]        │
│                               │
└──────────────────────────────┘
```

---

#### 4.2 应内朋友圈（二期扩展）

**动态发布**：
```
发布照片 → 添加文字
    ↓
选择可见范围（公开/好友）
    ↓
发布成功
```

**动态流**：
```
┌────────────────────────────┐
│  🏠 广场                     │
├────────────────────────────┤
│                             │
│  张三的旺财                  │
│  刚刚 · 公开                │
│  ┌──────────────────────┐  │
│  │ [照片]                │  │
│  └──────────────────────┘  │
│  旺财第一次来巴黎！好开心～   │
│  📍 埃菲尔铁塔               │
│                             │
│  ❤️ 128  💬 15  📤 8        │
│  ─────────────────────────  │
│                             │
│  李四的喵喵                  │
│  1小时前 · 仅好友            │
│  ┌──────────────────────┐  │
│  │ [照片]                │  │
│  └──────────────────────┘  │
│  带喵喵去看富士山啦🗻         │
│                             │
│  ❤️ 89  💬 7  📤 3          │
└────────────────────────────┘
```

---

### 后端实现

#### API设计

**生成分享海报**：
```
POST /api/v1/photos/{photo_id}/share

请求:
{
  "template": "default",  // 海报模板
  "include_qrcode": true
}

响应:
{
  "code": 0,
  "data": {
    "poster_url": "https://cdn.petvoyage.ai/posters/xxx.jpg"
  }
}
```

**实现逻辑**：
```python
from PIL import Image, ImageDraw, ImageFont
import qrcode

async def generate_share_poster(photo: Photo) -> str:
    """生成分享海报"""

    # 1. 创建画布
    canvas = Image.new('RGB', (1080, 1920), color='white')
    draw = ImageDraw.Draw(canvas)

    # 2. 添加照片
    photo_img = Image.open(download_image(photo.image_url))
    photo_img = photo_img.resize((900, 900))
    canvas.paste(photo_img, (90, 200))

    # 3. 添加文字
    font_title = ImageFont.truetype("fonts/PingFang-Bold.ttf", 60)
    font_info = ImageFont.truetype("fonts/PingFang-Regular.ttf", 40)

    title = f"🐕 {photo.pet.name}的{photo.location.city}之旅"
    draw.text((540, 1200), title, font=font_title, fill='#333', anchor='mm')

    info = f"📍 {photo.location.name}\n🕐 {photo.created_at.strftime('%Y年%m月%d日')}"
    draw.text((540, 1350), info, font=font_info, fill='#666', anchor='mm')

    # 4. 添加二维码
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data("https://petvoyage.ai/download")
    qr.make()
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((200, 200))
    canvas.paste(qr_img, (440, 1550))

    # 5. 保存并上传
    poster_path = f"/tmp/poster_{photo.id}.jpg"
    canvas.save(poster_path, quality=95)

    poster_url = await upload_to_oss(poster_path)

    return poster_url
```

---

### Phase 4 验收标准

- ✅ 可以生成精美分享海报
- ✅ 海报包含照片、文字、二维码
- ✅ 可以保存到相册
- ✅ 可以分享到微信/朋友圈
- ✅ 海报生成速度 < 3秒

---

## 📋 总结

### 最小MVP功能清单

**Phase 0-1（必须）**：
- ✅ 用户注册登录
- ✅ 添加宠物
- ✅ 选择景点
- ✅ AI生成照片（3张可选）
- ✅ 保存到相册

**Phase 2（重要）**：
- ✅ 世界地图
- ✅ 解锁地点
- ✅ 统计进度
- ✅ 成就系统

**Phase 3（提升体验）**：
- ✅ 四季主题
- ✅ 地域特色

**Phase 4（增长引擎）**：
- ✅ 分享海报

---

### 技术栈最终确认

**后端**：
- Python 3.11 + FastAPI
- PostgreSQL（用户、宠物、地点）
- MongoDB（照片、动态）
- Redis（缓存、队列）
- 硅基流动 API（AI图像生成）

**前端（iOS）**：
- Swift + SwiftUI
- Kingfisher（图片）
- Alamofire（网络）

**部署**：
- Docker + Docker Compose
- 阿里云ECS
- 阿里云OSS（图片存储）

---

### 下一步行动

你现在可以：

1. **确认方案**是否符合你的预期
2. **调整细节**（如果有不满意的地方）
3. **开始开发**（我可以帮你写具体代码）
4. **先做Demo**（Phase 0，验证API）

你希望我接下来做什么？
