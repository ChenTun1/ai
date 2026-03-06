# 技术规格文档

## 1. 系统架构

### 1.1 整体架构

```
┌─────────────┐
│   iOS App   │
└──────┬──────┘
       │ HTTPS/REST
       │
┌──────▼──────────────────────────────────────┐
│          API Gateway (Nginx)                 │
└──────┬──────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────┐
│      Backend Service (FastAPI)               │
│  ┌────────────┬────────────┬──────────────┐ │
│  │   User     │    Pet     │   Social     │ │
│  │  Service   │  Service   │   Service    │ │
│  └────────────┴────────────┴──────────────┘ │
└──┬────────┬────────┬──────────┬─────────────┘
   │        │        │          │
   │        │        │          │
┌──▼──┐  ┌─▼──┐  ┌──▼───┐   ┌─▼──────────┐
│ PG  │  │Redis│ │MongoDB│   │ OSS/S3     │
└─────┘  └────┘  └──────┘   └─┬──────────┘
                                │
                          ┌─────▼─────────┐
                          │  AI Service   │
                          │ (Replicate)   │
                          └───────────────┘
```

### 1.2 技术选型理由

#### 后端: FastAPI
- **性能**: 异步支持，性能接近Node.js
- **开发效率**: 自动生成API文档（Swagger/OpenAPI）
- **类型安全**: Python type hints支持
- **AI集成**: Python生态对AI库支持最好

#### 数据库组合
- **PostgreSQL**:
  - 存储结构化数据（用户、订阅、交易）
  - ACID保证，适合金融交易
  - 支持地理位置查询（PostGIS扩展）

- **MongoDB**:
  - 存储非结构化数据（照片元数据、社交动态）
  - 灵活的Schema，便于快速迭代

- **Redis**:
  - 会话管理
  - API限流（令牌桶算法）
  - 排行榜（Sorted Set）
  - 缓存热点数据

#### iOS: Swift + SwiftUI
- **原生性能**: 最佳用户体验
- **SwiftUI**: 声明式UI，开发效率高
- **Combine**: 响应式编程，处理异步数据流

---

## 2. 核心模块设计

### 2.1 用户认证模块

#### 认证流程
```
1. 用户注册/登录
   ↓
2. 服务端验证 (手机号验证码 / Apple Sign In)
   ↓
3. 生成JWT Token (Access Token + Refresh Token)
   ↓
4. 客户端存储Token (Keychain)
   ↓
5. 后续请求携带Token
```

#### JWT结构
```json
{
  "user_id": "uuid",
  "username": "string",
  "subscription_type": "free|premium|lifetime",
  "exp": 1234567890,
  "iat": 1234567890
}
```

#### 安全措施
- Access Token有效期: 7天
- Refresh Token有效期: 30天
- 密码使用bcrypt加密 (cost=12)
- 敏感操作需要二次验证

---

### 2.2 宠物虚拟化模块

#### 技术方案: LoRA模型训练

**流程**:
```
用户上传3-5张宠物照片
    ↓
后端接收并上传至OSS
    ↓
调用Replicate API训练LoRA模型
    ↓
训练完成后保存model_id到数据库
    ↓
后续生成图片时使用该model_id
```

**API选择**: Replicate - `replicate/sdxl-lora-training`

**参数配置**:
```python
{
    "input_images": "zip file URL",
    "token_string": "sks",  # 触发词
    "num_train_steps": 1000,
    "learning_rate": 1e-4,
    "resolution": 1024
}
```

**成本估算**:
- 训练一次: $2-3
- 生成一张图: $0.02-0.04
- 优化方案: 批量生成降低成本

#### 风格模板

| 风格 | 模型 | 描述 |
|------|------|------|
| 真实摄影 | SDXL Base | 逼真的照片效果 |
| 像素风 | Pixel Art LoRA | 8-bit游戏风格 |
| 动漫风 | Anime Diffusion | 日式动漫风格 |

---

### 2.3 AI图片生成模块

#### 生成策略

**模式A: 景点融合**
```
输入: 用户上传的景点照片 + 宠物LoRA模型
Prompt: "sks dog standing in front of [detected landmark],
         professional photography, natural lighting"
```

**模式B: 文本生成**
```
输入: 用户文字描述
Prompt: "sks cat at Eiffel Tower in Paris,
         golden hour, professional photography, 4k"
```

**模式C: 模板库**
```
预设Prompt模板库（100+景点）
示例: "sks [pet] at Great Wall of China,
       sunny day, wide angle lens, cinematic"
```

#### Prompt工程最佳实践

```python
BASE_PROMPT = """
{pet_trigger} {pet_type} at {location},
{style_modifiers},
high quality, detailed, professional photography,
natural lighting, 8k resolution
"""

NEGATIVE_PROMPT = """
blurry, low quality, distorted,
cartoon (unless style=anime),
watermark, text, signature
"""
```

#### 图片质量控制

- **分辨率**:
  - 免费用户: 1024x1024
  - 付费用户: 2048x2048

- **生成数量**: 一次生成4张供用户选择

- **内容审核**: 集成百度云内容审核API
  - 涉黄、涉政、暴力内容拦截
  - 审核不通过不扣除用户次数

---

### 2.4 地图解锁系统

#### 地理数据结构

**地点分类**:
```
世界 (World)
├── 亚洲 (Asia)
│   ├── 中国 (China)
│   │   ├── 北京 (Beijing)
│   │   │   ├── 故宫 (Forbidden City)
│   │   │   └── 长城 (Great Wall)
│   │   └── 上海 (Shanghai)
│   └── 日本 (Japan)
├── 欧洲 (Europe)
└── 美洲 (Americas)
```

**数据库设计**:
```sql
CREATE TABLE locations (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    name_en VARCHAR(255),
    parent_id UUID REFERENCES locations(id),
    level INT,  -- 0:世界, 1:大洲, 2:国家, 3:城市, 4:景点
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    icon_url VARCHAR(500),
    unlock_points INT DEFAULT 10
);
```

#### 解锁逻辑

```python
def unlock_location(user_id: str, location_id: str, photo_id: str):
    """
    解锁地点并递归解锁父级区域
    """
    # 1. 记录解锁
    await create_unlock_record(user_id, location_id, photo_id)

    # 2. 增加用户积分
    await add_user_points(user_id, location.unlock_points)

    # 3. 检查是否解锁成就
    await check_achievement_unlock(user_id)

    # 4. 递归解锁父级（如果首次）
    if location.parent_id and not is_unlocked(user_id, location.parent_id):
        await unlock_location(user_id, location.parent_id, photo_id)
```

---

### 2.5 成就系统

#### 成就类型

**探索类**:
- 环球旅行家: 解锁5个大洲
- 中国通: 解锁全部34个省级行政区
- 世界奇迹: 收集世界七大奇迹

**活跃类**:
- 每日打卡: 连续7天生成照片
- 摄影师: 累计生成100张照片
- 社交达人: 获得1000个点赞

**收藏类**:
- 名山大川: 收集中国五岳
- 城堡猎人: 收集20座欧洲古堡
- 现代奇观: 收集全球摩天大楼

#### 数据结构

```python
class Achievement(BaseModel):
    id: str
    name: str
    description: str
    icon_url: str
    category: AchievementCategory  # EXPLORE, ACTIVE, COLLECT
    condition_type: str  # unlock_count, photo_count, like_count
    condition_value: int
    reward_points: int
    is_hidden: bool  # 隐藏成就，达成后才显示
```

---

### 2.6 社交系统

#### 朋友圈设计

**Feed流算法** (MVP版本: 时间倒序):
```python
async def get_user_feed(user_id: str, page: int, size: int):
    """
    获取用户Feed流
    """
    # 1. 获取关注列表
    following_ids = await get_following_list(user_id)

    # 2. 查询动态（自己 + 关注的人）
    posts = await Post.find({
        "user_id": {"$in": [user_id] + following_ids},
        "status": "published"
    }).sort("created_at", -1).skip(page * size).limit(size)

    return posts
```

**未来优化** (算法推荐):
- 基于用户兴趣标签
- 热度衰减算法
- 去重与多样性

#### 点赞与评论

```python
# 点赞（幂等性设计）
await redis.sadd(f"post:{post_id}:likes", user_id)
like_count = await redis.scard(f"post:{post_id}:likes")

# 评论（存MongoDB）
comment = {
    "post_id": post_id,
    "user_id": user_id,
    "content": content,
    "created_at": datetime.utcnow()
}
await db.comments.insert_one(comment)
```

---

## 3. 性能优化

### 3.1 图片处理优化

#### CDN加速
```
用户上传 → OSS Origin → CDN边缘节点 → 用户访问
```

#### 图片格式优化
- 原图: PNG (无损)
- 缩略图: WebP (iOS 14+支持)
- 尺寸:
  - 缩略图: 300x300
  - 预览图: 1024x1024
  - 原图: 2048x2048

#### 懒加载策略
```swift
// iOS端使用Kingfisher
imageView.kf.setImage(
    with: url,
    placeholder: UIImage(named: "placeholder"),
    options: [
        .transition(.fade(0.2)),
        .cacheOriginalImage,
        .scaleFactor(UIScreen.main.scale)
    ]
)
```

### 3.2 API性能优化

#### 数据库索引
```sql
-- 用户查询
CREATE INDEX idx_users_phone ON users(phone_number);

-- 照片查询
CREATE INDEX idx_photos_user_created ON photos(user_id, created_at DESC);

-- 地点解锁
CREATE INDEX idx_unlocks_user_location ON user_unlocks(user_id, location_id);
```

#### 查询优化
```python
# 分页查询优化（游标分页）
async def get_photos_cursor(cursor: str = None, limit: int = 20):
    query = {"status": "published"}
    if cursor:
        query["_id"] = {"$lt": ObjectId(cursor)}

    photos = await db.photos.find(query).sort("_id", -1).limit(limit)
    return photos
```

#### 缓存策略
```python
# 热点数据缓存
@cache(key="user:{user_id}:profile", ttl=3600)
async def get_user_profile(user_id: str):
    return await db.users.find_one({"id": user_id})

# 排行榜缓存（Redis Sorted Set）
await redis.zadd("leaderboard:weekly", {user_id: score})
top_users = await redis.zrevrange("leaderboard:weekly", 0, 99, withscores=True)
```

### 3.3 并发控制

#### API限流
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/generate-photo")
@limiter.limit("10/minute")  # 免费用户每分钟10次
async def generate_photo(request: Request):
    pass
```

#### AI生成队列
```python
# 使用Celery处理异步任务
@celery.task
def generate_image_task(user_id: str, pet_id: str, location_id: str):
    # 1. 调用Replicate API
    result = replicate.run(model_id, input={...})

    # 2. 下载图片到OSS
    image_url = upload_to_oss(result.output[0])

    # 3. 保存到数据库
    create_photo_record(user_id, image_url, ...)

    # 4. 推送通知给用户
    send_push_notification(user_id, "您的照片已生成！")
```

---

## 4. 安全设计

### 4.1 数据安全

#### 敏感信息加密
```python
from cryptography.fernet import Fernet

# 手机号加密存储
def encrypt_phone(phone: str) -> str:
    cipher = Fernet(settings.ENCRYPTION_KEY)
    return cipher.encrypt(phone.encode()).decode()
```

#### SQL注入防护
```python
# 使用SQLAlchemy ORM（参数化查询）
result = await session.execute(
    select(User).where(User.phone == phone)
)
```

### 4.2 业务安全

#### 防刷策略
```python
# 设备指纹 + IP限流
device_key = f"device:{device_id}:generate"
if await redis.get(device_key):
    raise TooManyRequestsError()

await redis.setex(device_key, 60, "1")  # 1分钟冷却
```

#### 内容审核
```python
async def moderate_image(image_url: str) -> bool:
    """
    调用百度云内容审核API
    """
    result = await baidu_api.image_censor(image_url)

    if result.conclusion == "不合规":
        return False
    return True
```

---

## 5. 监控与运维

### 5.1 日志系统

```python
import structlog

logger = structlog.get_logger()

# 结构化日志
logger.info(
    "photo_generated",
    user_id=user_id,
    pet_id=pet_id,
    location_id=location_id,
    generation_time_ms=elapsed_time,
    cost_usd=cost
)
```

### 5.2 性能监控

#### 关键指标
- API响应时间 (P50, P95, P99)
- AI生成成功率
- 用户留存率 (次日、7日、30日)
- 付费转化率

#### APM工具
- Sentry: 错误追踪
- Prometheus + Grafana: 性能监控
- ELK Stack: 日志分析

---

## 6. 部署方案

### 6.1 Docker化

**Dockerfile (Backend)**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/petvoyage
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf

volumes:
  postgres_data:
```

### 6.2 CI/CD流程

**GitHub Actions**:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          ssh user@server "cd /app && docker-compose pull && docker-compose up -d"
```

---

## 7. 成本估算

### 7.1 服务器成本 (月)

| 资源 | 配置 | 成本 |
|------|------|------|
| ECS (API服务) | 4核8G | ¥300 |
| RDS PostgreSQL | 2核4G | ¥200 |
| Redis | 2G内存 | ¥100 |
| OSS存储 | 100GB | ¥10 |
| CDN流量 | 500GB | ¥50 |
| **合计** | | **¥660/月** |

### 7.2 AI成本估算

假设每月1000活跃用户：
- 每人训练1次LoRA: $2 × 1000 = $2000
- 每人生成20张图: $0.03 × 20 × 1000 = $600
- **月AI成本**: ~$2600 (¥18,000)

**优化方案**:
- 限制免费用户生成次数
- 付费用户分摊成本
- 用户达5万后自建GPU服务器

---

## 8. 技术债务与未来优化

### 短期优化 (3个月内)
- [ ] 实现图片生成队列优先级
- [ ] 优化数据库查询性能
- [ ] 添加API文档自动生成

### 中期优化 (6个月内)
- [ ] 迁移到Kubernetes集群
- [ ] 实现多区域部署
- [ ] 自建GPU服务器降低AI成本

### 长期规划 (1年内)
- [ ] 微服务架构拆分
- [ ] 实时推荐算法
- [ ] 多语言国际化
