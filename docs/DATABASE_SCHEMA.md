# 数据库设计文档

## 数据库架构

本项目采用**多数据库架构**:
- **PostgreSQL**: 存储结构化数据（用户、订阅、交易、地点）
- **MongoDB**: 存储非结构化数据（照片、社交动态、评论）
- **Redis**: 缓存、会话、排行榜、限流

---

## PostgreSQL Schema

### 1. 用户表 (users)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) UNIQUE,
    phone_encrypted VARCHAR(255),  -- 加密存储
    email VARCHAR(255) UNIQUE,
    username VARCHAR(50) NOT NULL,
    avatar_url VARCHAR(500),
    bio TEXT,
    apple_user_id VARCHAR(255) UNIQUE,  -- Apple登录标识

    -- 订阅信息
    subscription_type VARCHAR(20) DEFAULT 'free',  -- free | premium | lifetime
    subscription_expire_at TIMESTAMP,
    subscription_platform VARCHAR(20),  -- apple_iap | alipay | wechat

    -- 统计信息
    pets_count INT DEFAULT 0,
    photos_count INT DEFAULT 0,
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    total_points INT DEFAULT 0,

    -- 每日额度
    daily_quota_total INT DEFAULT 3,  -- 免费用户3次/天
    daily_quota_used INT DEFAULT 0,
    daily_quota_reset_at TIMESTAMP DEFAULT CURRENT_DATE + INTERVAL '1 day',

    -- 状态
    status VARCHAR(20) DEFAULT 'active',  -- active | banned | deleted
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_apple_id ON users(apple_user_id);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
```

---

### 2. 宠物表 (pets)

```sql
CREATE TABLE pets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,  -- dog | cat | other
    breed VARCHAR(100),
    avatar_url VARCHAR(500),

    -- AI模型信息
    lora_model_id VARCHAR(255),  -- Replicate模型ID
    lora_model_status VARCHAR(20) DEFAULT 'pending',  -- pending | training | ready | failed
    training_started_at TIMESTAMP,
    training_completed_at TIMESTAMP,
    training_photos JSONB,  -- 训练用的照片URL数组

    -- 统计
    photos_count INT DEFAULT 0,
    locations_count INT DEFAULT 0,
    total_likes INT DEFAULT 0,

    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pets_user_id ON pets(user_id);
CREATE INDEX idx_pets_status ON pets(lora_model_status);
```

---

### 3. 地点表 (locations)

```sql
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,  -- 中文名
    name_en VARCHAR(255) NOT NULL,  -- 英文名
    description TEXT,

    -- 层级结构
    parent_id UUID REFERENCES locations(id),
    level INT NOT NULL,  -- 0:世界 1:大洲 2:国家 3:城市 4:景点
    path VARCHAR(500),  -- 路径，如: world/asia/china/beijing/forbidden-city

    -- 地理信息
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    country_code VARCHAR(2),  -- ISO国家代码

    -- 媒体资源
    icon_url VARCHAR(500),
    cover_image_url VARCHAR(500),

    -- 游戏化
    unlock_points INT DEFAULT 10,
    difficulty INT DEFAULT 1,  -- 1-5星难度

    -- 统计
    unlock_count INT DEFAULT 0,  -- 全站解锁人数
    photos_count INT DEFAULT 0,

    -- AI生成提示词
    prompt_template TEXT,  -- 预设的Prompt模板

    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_locations_parent_id ON locations(parent_id);
CREATE INDEX idx_locations_level ON locations(level);
CREATE INDEX idx_locations_path ON locations(path);
CREATE INDEX idx_locations_country ON locations(country_code);

-- 地理位置索引（需要PostGIS扩展）
CREATE EXTENSION IF NOT EXISTS postgis;
ALTER TABLE locations ADD COLUMN geom GEOMETRY(Point, 4326);
CREATE INDEX idx_locations_geom ON locations USING GIST(geom);
```

---

### 4. 地点解锁记录 (user_location_unlocks)

```sql
CREATE TABLE user_location_unlocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    photo_id UUID NOT NULL,  -- MongoDB中的照片ID
    points_earned INT DEFAULT 0,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, location_id)  -- 同一地点只能解锁一次
);

CREATE INDEX idx_unlocks_user_id ON user_location_unlocks(user_id);
CREATE INDEX idx_unlocks_location_id ON user_location_unlocks(location_id);
CREATE INDEX idx_unlocks_unlocked_at ON user_location_unlocks(unlocked_at DESC);
```

---

### 5. 成就表 (achievements)

```sql
CREATE TABLE achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon_url VARCHAR(500),

    category VARCHAR(20) NOT NULL,  -- explore | active | collect

    -- 解锁条件
    condition_type VARCHAR(50) NOT NULL,  -- unlock_count | photo_count | like_count | specific_locations
    condition_value INT,
    condition_data JSONB,  -- 额外条件数据，如特定地点ID列表

    -- 奖励
    reward_points INT DEFAULT 0,

    -- 显示设置
    is_hidden BOOLEAN DEFAULT FALSE,  -- 隐藏成就
    display_order INT DEFAULT 0,

    -- 统计
    unlock_count INT DEFAULT 0,

    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_achievements_category ON achievements(category);
```

---

### 6. 用户成就解锁记录 (user_achievements)

```sql
CREATE TABLE user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_id UUID NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, achievement_id)
);

CREATE INDEX idx_user_ach_user_id ON user_achievements(user_id);
CREATE INDEX idx_user_ach_unlocked_at ON user_achievements(unlocked_at DESC);
```

---

### 7. 任务表 (tasks)

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(20) NOT NULL,  -- daily | weekly | challenge
    title VARCHAR(100) NOT NULL,
    description TEXT,

    -- 任务条件
    condition_type VARCHAR(50) NOT NULL,  -- generate_photo | unlock_location | share_photo
    condition_value INT DEFAULT 1,

    -- 奖励
    reward_points INT DEFAULT 0,
    reward_quota INT DEFAULT 0,  -- 额外生成次数

    -- 时间设置
    start_date DATE,
    end_date DATE,
    duration_days INT,  -- 任务周期（天）

    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_type ON tasks(type);
CREATE INDEX idx_tasks_dates ON tasks(start_date, end_date);
```

---

### 8. 用户任务进度 (user_tasks)

```sql
CREATE TABLE user_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,

    -- 进度
    progress_current INT DEFAULT 0,
    progress_target INT NOT NULL,

    -- 状态
    status VARCHAR(20) DEFAULT 'active',  -- active | completed | expired | claimed
    completed_at TIMESTAMP,
    claimed_at TIMESTAMP,
    expire_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, task_id, expire_at)
);

CREATE INDEX idx_user_tasks_user_id ON user_tasks(user_id);
CREATE INDEX idx_user_tasks_status ON user_tasks(status);
CREATE INDEX idx_user_tasks_expire_at ON user_tasks(expire_at);
```

---

### 9. 关注关系表 (follows)

```sql
CREATE TABLE follows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    follower_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,  -- 关注者
    followee_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,  -- 被关注者
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(follower_id, followee_id),
    CHECK (follower_id != followee_id)  -- 不能关注自己
);

CREATE INDEX idx_follows_follower ON follows(follower_id);
CREATE INDEX idx_follows_followee ON follows(followee_id);
CREATE INDEX idx_follows_created_at ON follows(created_at DESC);
```

---

### 10. 订单表 (orders)

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_no VARCHAR(32) UNIQUE NOT NULL,  -- 订单号
    user_id UUID NOT NULL REFERENCES users(id),

    -- 商品信息
    product_type VARCHAR(20) NOT NULL,  -- subscription | virtual_item
    product_id VARCHAR(100),  -- 套餐ID或商品ID
    product_name VARCHAR(255),

    -- 金额
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'CNY',

    -- 支付信息
    payment_method VARCHAR(20),  -- apple_iap | alipay | wechat
    payment_platform_order_id VARCHAR(255),  -- 第三方订单ID
    receipt_data TEXT,  -- Apple IAP收据

    -- 状态
    status VARCHAR(20) DEFAULT 'pending',  -- pending | paid | failed | refunded
    paid_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
```

---

### 11. 通知表 (notifications)

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    type VARCHAR(20) NOT NULL,  -- like | comment | follow | achievement | system
    title VARCHAR(255) NOT NULL,
    content TEXT,

    -- 关联数据
    data JSONB,  -- 存储photo_id, user_id等

    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(user_id, is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);
```

---

## MongoDB Schema

### 1. 照片集合 (photos)

```javascript
{
  _id: ObjectId,
  id: "uuid-xxx",  // 与PostgreSQL保持一致的UUID
  user_id: "uuid-xxx",
  pet_id: "uuid-xxx",
  location_id: "uuid-xxx",

  // 图片信息
  image_url: "https://cdn.petvoyage.ai/photos/xxx.jpg",
  thumbnail_url: "https://cdn.petvoyage.ai/photos/xxx-thumb.jpg",
  width: 2048,
  height: 2048,
  file_size: 1048576,

  // 生成信息
  style: "realistic",  // realistic | pixel | anime
  generation_task_id: "task-xxx",
  generation_time_ms: 15000,
  ai_model: "replicate/sdxl",
  prompt: "sks dog at Eiffel Tower...",

  // 内容
  caption: "我的旺财在巴黎！",
  tags: ["旅游", "宠物", "巴黎"],

  // 统计
  likes_count: 128,
  comments_count: 15,
  views_count: 1523,
  shares_count: 8,

  // 状态
  status: "published",  // draft | published | deleted
  is_public: true,

  // 内容审核
  moderation_status: "approved",  // pending | approved | rejected
  moderation_result: {},

  created_at: ISODate("2024-03-06T10:00:00Z"),
  updated_at: ISODate("2024-03-06T10:00:00Z")
}

// 索引
db.photos.createIndex({ user_id: 1, created_at: -1 })
db.photos.createIndex({ pet_id: 1, created_at: -1 })
db.photos.createIndex({ location_id: 1, created_at: -1 })
db.photos.createIndex({ status: 1, created_at: -1 })
db.photos.createIndex({ likes_count: -1 })  // 热门排序
```

---

### 2. 动态集合 (posts)

```javascript
{
  _id: ObjectId,
  id: "uuid-xxx",
  user_id: "uuid-xxx",
  photo_id: "uuid-xxx",  // 关联的照片

  content: "今天带旺财去了巴黎！",

  // 统计
  likes_count: 128,
  comments_count: 15,
  shares_count: 8,

  // 可见性
  visibility: "public",  // public | followers | private

  status: "published",
  created_at: ISODate("2024-03-06T10:00:00Z"),
  updated_at: ISODate("2024-03-06T10:00:00Z")
}

db.posts.createIndex({ user_id: 1, created_at: -1 })
db.posts.createIndex({ created_at: -1 })
db.posts.createIndex({ likes_count: -1 })
```

---

### 3. 点赞集合 (likes)

```javascript
{
  _id: ObjectId,
  user_id: "uuid-xxx",
  target_type: "photo",  // photo | post | comment
  target_id: "uuid-xxx",
  created_at: ISODate("2024-03-06T10:00:00Z")
}

// 复合唯一索引，防止重复点赞
db.likes.createIndex({ user_id: 1, target_type: 1, target_id: 1 }, { unique: true })
db.likes.createIndex({ target_type: 1, target_id: 1, created_at: -1 })
```

---

### 4. 评论集合 (comments)

```javascript
{
  _id: ObjectId,
  id: "uuid-xxx",
  user_id: "uuid-xxx",
  photo_id: "uuid-xxx",

  content: "太可爱了！",

  // 回复
  reply_to_comment_id: "uuid-xxx",  // null表示一级评论
  reply_to_user_id: "uuid-xxx",

  // 统计
  likes_count: 5,
  replies_count: 2,

  status: "published",  // published | deleted
  created_at: ISODate("2024-03-06T10:00:00Z"),
  updated_at: ISODate("2024-03-06T10:00:00Z")
}

db.comments.createIndex({ photo_id: 1, created_at: -1 })
db.comments.createIndex({ user_id: 1, created_at: -1 })
db.comments.createIndex({ reply_to_comment_id: 1 })
```

---

### 5. AI生成任务集合 (generation_tasks)

```javascript
{
  _id: ObjectId,
  task_id: "task-xxx",
  user_id: "uuid-xxx",
  pet_id: "uuid-xxx",

  // 生成参数
  mode: "template",  // template | upload | text
  location_id: "uuid-xxx",
  style: "realistic",
  custom_prompt: "",
  scene_image_url: "",
  num_outputs: 4,

  // AI参数
  model: "replicate/sdxl",
  lora_model_id: "xxx",
  final_prompt: "sks dog at Eiffel Tower...",
  negative_prompt: "blurry, low quality...",

  // 结果
  status: "completed",  // queued | processing | completed | failed
  output_images: [
    {
      url: "https://...",
      width: 2048,
      height: 2048
    }
  ],
  error_message: "",

  // 成本与性能
  cost_usd: 0.03,
  generation_time_ms: 15000,

  created_at: ISODate("2024-03-06T10:00:00Z"),
  completed_at: ISODate("2024-03-06T10:00:15Z")
}

db.generation_tasks.createIndex({ task_id: 1 }, { unique: true })
db.generation_tasks.createIndex({ user_id: 1, created_at: -1 })
db.generation_tasks.createIndex({ status: 1, created_at: -1 })
```

---

### 6. 旅行日记集合 (travel_journals)

```javascript
{
  _id: ObjectId,
  id: "uuid-xxx",
  user_id: "uuid-xxx",
  pet_id: "uuid-xxx",

  title: "旺财的2024欧洲之旅",
  description: "为期一个月的欧洲旅行...",

  // 封面
  cover_photo_id: "uuid-xxx",

  // 照片列表（按时间排序）
  photos: [
    {
      photo_id: "uuid-xxx",
      location_id: "uuid-xxx",
      caption: "...",
      order: 1
    }
  ],

  // 统计
  photos_count: 25,
  locations_count: 8,
  views_count: 523,
  likes_count: 89,

  status: "published",  // draft | published
  created_at: ISODate("2024-03-06T10:00:00Z"),
  updated_at: ISODate("2024-03-06T10:00:00Z")
}

db.travel_journals.createIndex({ user_id: 1, created_at: -1 })
db.travel_journals.createIndex({ status: 1, created_at: -1 })
```

---

## Redis数据结构

### 1. 会话管理

```
# JWT Token黑名单（登出时加入）
key: blacklist:token:{token_hash}
type: String
value: "1"
ttl: token剩余有效期

# 用户会话信息
key: session:user:{user_id}
type: Hash
fields: {
  device_id: "xxx",
  platform: "iOS",
  last_active: timestamp
}
ttl: 7天
```

---

### 2. 限流

```
# API限流（令牌桶算法）
key: ratelimit:api:{user_id}:{endpoint}
type: String
value: "remaining_count"
ttl: 1小时

# 生成限流
key: ratelimit:generate:{user_id}:{date}
type: String
value: "3"  # 已使用次数
ttl: 到当天结束
```

---

### 3. 缓存

```
# 用户信息缓存
key: cache:user:{user_id}
type: String (JSON)
value: {user对象}
ttl: 1小时

# 热门照片缓存
key: cache:hot_photos:{date}
type: List
value: [photo_id1, photo_id2, ...]
ttl: 10分钟

# 地点信息缓存
key: cache:location:{location_id}
type: String (JSON)
value: {location对象}
ttl: 24小时
```

---

### 4. 排行榜

```
# 周排行榜（解锁数）
key: leaderboard:weekly:unlocks:{week}
type: Sorted Set
score: unlock_count
member: user_id

# 月排行榜（照片数）
key: leaderboard:monthly:photos:{month}
type: Sorted Set
score: photo_count
member: user_id

# 总排行榜（点赞数）
key: leaderboard:all_time:likes
type: Sorted Set
score: total_likes
member: user_id
```

---

### 5. 点赞计数

```
# 照片点赞集合
key: photo:{photo_id}:likes
type: Set
members: [user_id1, user_id2, ...]

# 照片点赞数（缓存）
key: photo:{photo_id}:likes_count
type: String
value: "128"
ttl: 10分钟
```

---

### 6. Feed流缓存

```
# 用户Feed流（关注的人的动态）
key: feed:user:{user_id}
type: List
value: [post_id1, post_id2, ...]  # 最新1000条
```

---

### 7. 实时统计

```
# 在线用户数
key: stats:online_users
type: HyperLogLog
members: [user_id1, user_id2, ...]

# 今日新增用户
key: stats:new_users:{date}
type: Set
members: [user_id1, user_id2, ...]
```

---

## 数据迁移与版本管理

### Alembic配置 (PostgreSQL)

```python
# alembic/versions/001_initial.py
def upgrade():
    op.create_table('users', ...)
    op.create_table('pets', ...)
    # ...

def downgrade():
    op.drop_table('pets')
    op.drop_table('users')
```

### MongoDB迁移

使用 `pymongo-migrate` 或自定义脚本:

```python
# migrations/001_create_indexes.py
def upgrade(db):
    db.photos.create_index([("user_id", 1), ("created_at", -1)])
    db.photos.create_index([("location_id", 1)])

def downgrade(db):
    db.photos.drop_index("user_id_1_created_at_-1")
```

---

## 备份策略

### PostgreSQL
- **全量备份**: 每天凌晨2点
- **增量备份**: 每小时一次WAL归档
- **保留策略**: 30天

### MongoDB
- **全量备份**: 每天凌晨3点 (mongodump)
- **Oplog备份**: 持续同步
- **保留策略**: 30天

### Redis
- **RDB快照**: 每小时一次
- **AOF日志**: 每秒fsync
- **保留策略**: 7天

---

## 性能优化建议

### 1. 分库分表
当单表数据超过1000万时考虑:
- 用户表按user_id哈希分片
- 照片表按created_at时间分片

### 2. 读写分离
- 主库: 写操作
- 从库: 读操作（可配置多个从库）

### 3. 缓存策略
- 热点数据（用户信息、热门照片）: Redis缓存
- 冷数据（历史记录）: 直接查数据库

### 4. 索引优化
- 定期分析慢查询日志
- 根据实际查询模式调整索引

---

## 数据安全

### 1. 敏感信息加密
- 手机号: AES-256加密
- 密码: bcrypt哈希 (cost=12)
- 支付信息: 不存储完整信息

### 2. 访问控制
- 数据库账号最小权限原则
- 应用层row-level security

### 3. 审计日志
记录所有关键操作:
- 用户登录
- 订阅购买
- 敏感信息修改

---

## 附录: 初始化数据

### 地点数据初始化

```sql
-- 世界
INSERT INTO locations (id, name, name_en, level, path)
VALUES ('loc-world', '世界', 'World', 0, 'world');

-- 亚洲
INSERT INTO locations (id, name, name_en, parent_id, level, path)
VALUES ('loc-asia', '亚洲', 'Asia', 'loc-world', 1, 'world/asia');

-- 中国
INSERT INTO locations (id, name, name_en, parent_id, level, path, country_code)
VALUES ('loc-china', '中国', 'China', 'loc-asia', 2, 'world/asia/china', 'CN');

-- 北京
INSERT INTO locations (id, name, name_en, parent_id, level, path, latitude, longitude)
VALUES ('loc-beijing', '北京', 'Beijing', 'loc-china', 3, 'world/asia/china/beijing', 39.9042, 116.4074);

-- 故宫
INSERT INTO locations (id, name, name_en, parent_id, level, path, latitude, longitude, prompt_template)
VALUES (
  'loc-forbidden-city',
  '故宫',
  'Forbidden City',
  'loc-beijing',
  4,
  'world/asia/china/beijing/forbidden-city',
  39.9163,
  116.3972,
  'sks {pet_type} at the Forbidden City in Beijing, traditional Chinese architecture, red walls and golden roofs, sunny day, professional photography'
);
```

### 成就数据初始化

```sql
INSERT INTO achievements (id, name, description, category, condition_type, condition_value, reward_points) VALUES
('ach-first-photo', '首次尝试', '生成第一张照片', 'active', 'photo_count', 1, 10),
('ach-explorer', '探索者', '解锁10个地点', 'explore', 'unlock_count', 10, 50),
('ach-world-traveler', '环球旅行家', '解锁5个大洲', 'explore', 'unlock_count', 5, 500);
```
