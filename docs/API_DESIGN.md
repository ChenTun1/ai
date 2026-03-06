# API设计文档

## 基础信息

- **Base URL**: `https://api.petvoyage.ai/v1`
- **协议**: HTTPS
- **数据格式**: JSON
- **认证方式**: JWT Bearer Token
- **字符编码**: UTF-8

---

## 通用规范

### 请求头

```http
Authorization: Bearer {access_token}
Content-Type: application/json
X-Device-ID: {unique_device_id}
X-App-Version: 1.0.0
X-Platform: iOS
```

### 响应格式

#### 成功响应
```json
{
  "code": 0,
  "message": "success",
  "data": {
    // 业务数据
  },
  "timestamp": 1234567890
}
```

#### 错误响应
```json
{
  "code": 40001,
  "message": "Invalid token",
  "data": null,
  "timestamp": 1234567890
}
```

### 错误码

| Code | 说明 |
|------|------|
| 0 | 成功 |
| 40001 | Token无效 |
| 40002 | Token过期 |
| 40003 | 权限不足 |
| 40004 | 参数错误 |
| 40005 | 资源不存在 |
| 40006 | 操作过于频繁 |
| 40007 | 余额不足（生成次数用完） |
| 50001 | 服务器内部错误 |
| 50002 | AI服务异常 |
| 50003 | 第三方服务异常 |

### 分页参数

```json
{
  "page": 1,
  "page_size": 20,
  "total": 100,
  "items": []
}
```

---

## 1. 用户认证模块

### 1.1 发送验证码

**POST** `/auth/send-code`

**请求参数**:
```json
{
  "phone": "+8613800138000",
  "scene": "login"  // login | register
}
```

**响应**:
```json
{
  "code": 0,
  "message": "验证码已发送",
  "data": {
    "expire_in": 300  // 5分钟有效期
  }
}
```

---

### 1.2 手机号登录/注册

**POST** `/auth/login`

**请求参数**:
```json
{
  "phone": "+8613800138000",
  "code": "123456"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 604800,  // 7天
    "user": {
      "id": "uuid-xxx",
      "phone": "+8613800138000",
      "username": "用户_1234",
      "avatar": "https://cdn.petvoyage.ai/avatars/default.png",
      "subscription_type": "free",  // free | premium | lifetime
      "created_at": "2024-03-06T10:00:00Z"
    }
  }
}
```

---

### 1.3 Apple登录

**POST** `/auth/apple`

**请求参数**:
```json
{
  "identity_token": "apple_identity_token",
  "user_identifier": "apple_user_id",
  "email": "user@privaterelay.appleid.com",
  "full_name": "张三"  // 可选，仅首次授权时提供
}
```

**响应**: 同手机号登录

---

### 1.4 刷新Token

**POST** `/auth/refresh`

**请求参数**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "access_token": "new_access_token",
    "expires_in": 604800
  }
}
```

---

### 1.5 登出

**POST** `/auth/logout`

**请求头**: 需要Authorization

**响应**:
```json
{
  "code": 0,
  "message": "已登出"
}
```

---

## 2. 用户模块

### 2.1 获取个人信息

**GET** `/users/me`

**响应**:
```json
{
  "code": 0,
  "data": {
    "id": "uuid-xxx",
    "username": "宠物旅行家",
    "avatar": "https://cdn.petvoyage.ai/avatars/xxx.jpg",
    "bio": "带着我的柯基环游世界",
    "subscription": {
      "type": "premium",
      "expire_at": "2025-03-06T10:00:00Z"
    },
    "stats": {
      "pets_count": 2,
      "photos_count": 156,
      "unlocked_locations": 48,
      "achievements_count": 12,
      "followers_count": 234,
      "following_count": 189
    },
    "daily_quota": {
      "total": 100,  // 付费用户每日100次
      "used": 15,
      "reset_at": "2024-03-07T00:00:00Z"
    }
  }
}
```

---

### 2.2 更新个人信息

**PATCH** `/users/me`

**请求参数**:
```json
{
  "username": "新昵称",
  "bio": "个人简介",
  "avatar": "https://cdn.petvoyage.ai/avatars/new.jpg"  // 需先上传图片
}
```

---

### 2.3 获取用户主页

**GET** `/users/{user_id}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "id": "uuid-xxx",
    "username": "宠物旅行家",
    "avatar": "https://...",
    "bio": "...",
    "stats": { /* 同上 */ },
    "is_following": false,  // 当前用户是否关注该用户
    "recent_photos": [
      {
        "id": "photo-xxx",
        "image_url": "https://...",
        "thumbnail_url": "https://...",
        "location": {
          "id": "loc-xxx",
          "name": "埃菲尔铁塔"
        },
        "likes_count": 128,
        "created_at": "2024-03-05T10:00:00Z"
      }
    ]
  }
}
```

---

## 3. 宠物模块

### 3.1 创建宠物

**POST** `/pets`

**请求参数** (multipart/form-data):
```
pet_name: "旺财"
pet_type: "dog"  // dog | cat | other
breed: "柯基"
photos: [File, File, File]  // 3-5张照片
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "id": "pet-xxx",
    "name": "旺财",
    "type": "dog",
    "breed": "柯基",
    "photos": [
      "https://cdn.petvoyage.ai/pets/xxx-1.jpg",
      "https://cdn.petvoyage.ai/pets/xxx-2.jpg"
    ],
    "lora_model_status": "training",  // training | ready | failed
    "lora_model_id": null,
    "training_started_at": "2024-03-06T10:00:00Z",
    "created_at": "2024-03-06T10:00:00Z"
  }
}
```

**训练时长**: 约5-10分钟，完成后通过Push通知用户

---

### 3.2 获取宠物列表

**GET** `/pets`

**响应**:
```json
{
  "code": 0,
  "data": [
    {
      "id": "pet-xxx",
      "name": "旺财",
      "type": "dog",
      "avatar": "https://cdn.petvoyage.ai/pets/xxx-avatar.jpg",
      "lora_model_status": "ready",
      "photos_count": 89,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

### 3.3 获取宠物详情

**GET** `/pets/{pet_id}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "id": "pet-xxx",
    "name": "旺财",
    "type": "dog",
    "breed": "柯基",
    "photos": [ /* 训练用的原始照片 */ ],
    "lora_model_status": "ready",
    "lora_model_id": "replicate-model-xxx",
    "stats": {
      "photos_count": 89,
      "locations_count": 23,
      "total_likes": 1234
    },
    "recent_photos": [ /* 最近生成的照片 */ ]
  }
}
```

---

### 3.4 更新宠物信息

**PATCH** `/pets/{pet_id}`

**请求参数**:
```json
{
  "name": "新名字",
  "breed": "新品种"
}
```

---

### 3.5 删除宠物

**DELETE** `/pets/{pet_id}`

⚠️ 注意: 会同时删除该宠物的所有照片

---

## 4. 照片生成模块

### 4.1 生成照片

**POST** `/photos/generate`

**请求参数**:
```json
{
  "pet_id": "pet-xxx",
  "mode": "template",  // template | upload | text
  "location_id": "loc-xxx",  // mode=template时必填
  "style": "realistic",  // realistic | pixel | anime
  "custom_prompt": "在埃菲尔铁塔前，黄昏时分",  // mode=text时必填
  "image_url": "https://...",  // mode=upload时必填，用户上传的景点照
  "num_outputs": 4  // 生成数量，免费用户最多4张
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "task_id": "task-xxx",
    "status": "queued",  // queued | processing | completed | failed
    "estimated_time": 30  // 预估完成时间（秒）
  }
}
```

**异步任务**: 客户端需要轮询或使用WebSocket获取结果

---

### 4.2 查询生成任务状态

**GET** `/photos/generate/{task_id}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "task_id": "task-xxx",
    "status": "completed",
    "photos": [
      {
        "image_url": "https://cdn.petvoyage.ai/photos/xxx-1.jpg",
        "thumbnail_url": "https://cdn.petvoyage.ai/photos/xxx-1-thumb.jpg",
        "width": 2048,
        "height": 2048
      },
      // ...其他3张
    ],
    "created_at": "2024-03-06T10:00:30Z"
  }
}
```

---

### 4.3 保存照片

**POST** `/photos`

用户从生成的4张中选择满意的保存

**请求参数**:
```json
{
  "task_id": "task-xxx",
  "selected_index": 0,  // 选择第几张（0-3）
  "pet_id": "pet-xxx",
  "location_id": "loc-xxx",
  "caption": "我的旺财在巴黎！"  // 可选
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "id": "photo-xxx",
    "image_url": "https://...",
    "thumbnail_url": "https://...",
    "pet": { /* 宠物信息 */ },
    "location": { /* 地点信息 */ },
    "caption": "我的旺财在巴黎！",
    "style": "realistic",
    "created_at": "2024-03-06T10:01:00Z",
    "unlocked_locations": [
      {
        "id": "loc-paris",
        "name": "巴黎",
        "level": 3
      },
      {
        "id": "loc-france",
        "name": "法国",
        "level": 2
      }
    ],
    "earned_achievements": [
      {
        "id": "ach-first-europe",
        "name": "初探欧洲",
        "icon": "https://..."
      }
    ]
  }
}
```

---

### 4.4 获取照片列表

**GET** `/photos`

**查询参数**:
```
?user_id=xxx        # 可选，默认当前用户
&pet_id=xxx         # 可选，筛选特定宠物
&location_id=xxx    # 可选，筛选特定地点
&style=realistic    # 可选，筛选风格
&page=1
&page_size=20
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "page": 1,
    "page_size": 20,
    "total": 156,
    "items": [
      {
        "id": "photo-xxx",
        "image_url": "https://...",
        "thumbnail_url": "https://...",
        "pet": {
          "id": "pet-xxx",
          "name": "旺财",
          "avatar": "https://..."
        },
        "location": {
          "id": "loc-xxx",
          "name": "埃菲尔铁塔",
          "country": "法国"
        },
        "caption": "黄昏下的巴黎",
        "likes_count": 128,
        "comments_count": 15,
        "is_liked": false,
        "created_at": "2024-03-05T10:00:00Z"
      }
    ]
  }
}
```

---

### 4.5 删除照片

**DELETE** `/photos/{photo_id}`

---

## 5. 地图解锁模块

### 5.1 获取地图数据

**GET** `/locations`

**查询参数**:
```
?level=1            # 地点层级 (0=世界, 1=大洲, 2=国家, 3=城市, 4=景点)
&parent_id=xxx      # 父级ID，获取子地点
```

**响应**:
```json
{
  "code": 0,
  "data": [
    {
      "id": "loc-asia",
      "name": "亚洲",
      "name_en": "Asia",
      "level": 1,
      "parent_id": "loc-world",
      "icon": "https://cdn.petvoyage.ai/icons/asia.png",
      "children_count": 48,
      "is_unlocked": true,
      "unlock_progress": 0.35  // 子地点解锁进度
    }
  ]
}
```

---

### 5.2 获取用户解锁记录

**GET** `/users/me/unlocks`

**响应**:
```json
{
  "code": 0,
  "data": {
    "total_unlocked": 48,
    "by_level": {
      "continents": 5,
      "countries": 18,
      "cities": 25,
      "landmarks": 48
    },
    "recent_unlocks": [
      {
        "location": {
          "id": "loc-xxx",
          "name": "埃菲尔铁塔",
          "level": 4
        },
        "photo": {
          "id": "photo-xxx",
          "thumbnail_url": "https://..."
        },
        "unlocked_at": "2024-03-05T10:00:00Z"
      }
    ]
  }
}
```

---

### 5.3 获取地点详情

**GET** `/locations/{location_id}`

**响应**:
```json
{
  "code": 0,
  "data": {
    "id": "loc-eiffel",
    "name": "埃菲尔铁塔",
    "name_en": "Eiffel Tower",
    "description": "法国巴黎的标志性建筑...",
    "level": 4,
    "latitude": 48.8584,
    "longitude": 2.2945,
    "icon": "https://...",
    "cover_image": "https://...",
    "is_unlocked": true,
    "unlocked_at": "2024-03-05T10:00:00Z",
    "unlock_count": 12456,  // 全站解锁人数
    "related_photos": [
      /* 该地点的热门照片 */
    ]
  }
}
```

---

## 6. 成就系统模块

### 6.1 获取成就列表

**GET** `/achievements`

**查询参数**:
```
?category=explore   # explore | active | collect
&status=unlocked    # all | unlocked | locked
```

**响应**:
```json
{
  "code": 0,
  "data": [
    {
      "id": "ach-world-traveler",
      "name": "环球旅行家",
      "description": "解锁全部5个大洲",
      "category": "explore",
      "icon": "https://cdn.petvoyage.ai/achievements/world-traveler.png",
      "is_unlocked": false,
      "is_hidden": false,
      "progress": {
        "current": 3,
        "target": 5,
        "percentage": 0.6
      },
      "reward_points": 500,
      "unlock_count": 12345  // 全站解锁人数
    }
  ]
}
```

---

### 6.2 获取用户成就

**GET** `/users/me/achievements`

**响应**:
```json
{
  "code": 0,
  "data": {
    "total_unlocked": 12,
    "total_points": 2400,
    "recent_unlocks": [
      {
        "achievement": { /* 成就信息 */ },
        "unlocked_at": "2024-03-05T10:00:00Z"
      }
    ]
  }
}
```

---

## 7. 任务系统模块

### 7.1 获取任务列表

**GET** `/tasks`

**查询参数**:
```
?type=daily         # daily | weekly | challenge
&status=active      # active | completed | expired
```

**响应**:
```json
{
  "code": 0,
  "data": [
    {
      "id": "task-daily-photo",
      "type": "daily",
      "title": "每日一拍",
      "description": "生成1张新照片",
      "progress": {
        "current": 0,
        "target": 1
      },
      "rewards": {
        "points": 10,
        "quota": 1  // 额外生成次数
      },
      "status": "active",
      "expire_at": "2024-03-07T00:00:00Z"
    }
  ]
}
```

---

### 7.2 领取任务奖励

**POST** `/tasks/{task_id}/claim`

**响应**:
```json
{
  "code": 0,
  "data": {
    "task": { /* 任务信息 */ },
    "rewards": {
      "points": 10,
      "quota": 1
    }
  }
}
```

---

## 8. 社交模块

### 8.1 获取Feed流

**GET** `/feed`

**查询参数**:
```
?type=following     # following | discover | hot
&cursor=xxx         # 游标分页
&limit=20
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "cursor": "next-cursor-xxx",
    "has_more": true,
    "items": [
      {
        "id": "post-xxx",
        "user": {
          "id": "user-xxx",
          "username": "旅行家",
          "avatar": "https://..."
        },
        "photo": {
          "id": "photo-xxx",
          "image_url": "https://...",
          "thumbnail_url": "https://..."
        },
        "caption": "旺财的巴黎之旅！",
        "location": {
          "id": "loc-xxx",
          "name": "埃菲尔铁塔"
        },
        "likes_count": 128,
        "comments_count": 15,
        "is_liked": false,
        "is_bookmarked": false,
        "created_at": "2024-03-05T10:00:00Z"
      }
    ]
  }
}
```

---

### 8.2 点赞/取消点赞

**POST** `/photos/{photo_id}/like`

**响应**:
```json
{
  "code": 0,
  "data": {
    "is_liked": true,
    "likes_count": 129
  }
}
```

**DELETE** `/photos/{photo_id}/like` - 取消点赞

---

### 8.3 评论

**POST** `/photos/{photo_id}/comments`

**请求参数**:
```json
{
  "content": "太可爱了！",
  "reply_to": "comment-xxx"  // 可选，回复某条评论
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "id": "comment-xxx",
    "user": {
      "id": "user-xxx",
      "username": "评论者",
      "avatar": "https://..."
    },
    "content": "太可爱了！",
    "reply_to": null,
    "likes_count": 0,
    "created_at": "2024-03-06T10:00:00Z"
  }
}
```

---

### 8.4 获取评论列表

**GET** `/photos/{photo_id}/comments`

**查询参数**: `?page=1&page_size=20`

---

### 8.5 关注用户

**POST** `/users/{user_id}/follow`

**响应**:
```json
{
  "code": 0,
  "data": {
    "is_following": true,
    "followers_count": 235
  }
}
```

**DELETE** `/users/{user_id}/follow` - 取消关注

---

### 8.6 获取关注列表

**GET** `/users/{user_id}/following`

**GET** `/users/{user_id}/followers`

---

### 8.7 排行榜

**GET** `/leaderboard`

**查询参数**:
```
?type=weekly        # daily | weekly | monthly | all_time
&metric=unlocks     # unlocks | photos | likes
&limit=100
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "my_rank": 42,
    "my_score": 156,
    "list": [
      {
        "rank": 1,
        "user": {
          "id": "user-xxx",
          "username": "旅行大师",
          "avatar": "https://..."
        },
        "score": 523,
        "pet": {
          "id": "pet-xxx",
          "name": "旺财",
          "avatar": "https://..."
        }
      }
    ]
  }
}
```

---

## 9. 订阅与支付模块

### 9.1 获取订阅套餐

**GET** `/subscriptions/plans`

**响应**:
```json
{
  "code": 0,
  "data": [
    {
      "id": "plan-monthly",
      "name": "高级会员（月付）",
      "type": "premium",
      "duration": "monthly",
      "price": 19.8,
      "currency": "CNY",
      "features": [
        "无限AI生图",
        "全部风格解锁",
        "高清无水印",
        "优先生成队列"
      ],
      "apple_product_id": "com.petvoyage.premium.monthly"
    },
    {
      "id": "plan-yearly",
      "name": "高级会员（年付）",
      "type": "premium",
      "duration": "yearly",
      "price": 128,
      "currency": "CNY",
      "discount": "省109元",
      "apple_product_id": "com.petvoyage.premium.yearly"
    },
    {
      "id": "plan-lifetime",
      "name": "终身会员",
      "type": "lifetime",
      "duration": "lifetime",
      "price": 298,
      "currency": "CNY",
      "apple_product_id": "com.petvoyage.lifetime"
    }
  ]
}
```

---

### 9.2 创建订阅订单

**POST** `/subscriptions/orders`

**请求参数**:
```json
{
  "plan_id": "plan-monthly",
  "payment_method": "apple_iap"  // apple_iap | alipay | wechat
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "order_id": "order-xxx",
    "plan": { /* 套餐信息 */ },
    "amount": 19.8,
    "currency": "CNY",
    "status": "pending",
    "payment_info": {
      // iOS: 无需额外信息，走IAP
      // 其他: 返回支付参数
    },
    "created_at": "2024-03-06T10:00:00Z"
  }
}
```

---

### 9.3 验证Apple IAP收据

**POST** `/subscriptions/verify-receipt`

**请求参数**:
```json
{
  "order_id": "order-xxx",
  "receipt_data": "base64_encoded_receipt"
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "order_id": "order-xxx",
    "status": "paid",
    "subscription": {
      "type": "premium",
      "expire_at": "2025-03-06T10:00:00Z"
    }
  }
}
```

---

### 9.4 获取订阅状态

**GET** `/subscriptions/status`

**响应**:
```json
{
  "code": 0,
  "data": {
    "type": "premium",
    "expire_at": "2025-03-06T10:00:00Z",
    "is_active": true,
    "auto_renew": true,
    "platform": "apple_iap"
  }
}
```

---

## 10. 文件上传模块

### 10.1 获取上传凭证

**POST** `/upload/token`

**请求参数**:
```json
{
  "file_type": "image/jpeg",
  "file_size": 2048576,
  "purpose": "pet_photo"  // pet_photo | avatar | scene_photo
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "upload_url": "https://oss.aliyuncs.com/...",
    "upload_token": "xxx",
    "file_key": "pets/xxx.jpg",
    "expire_at": "2024-03-06T11:00:00Z"
  }
}
```

**说明**: 客户端直传OSS，减轻服务器压力

---

### 10.2 确认上传完成

**POST** `/upload/confirm`

**请求参数**:
```json
{
  "file_key": "pets/xxx.jpg"
}
```

**响应**:
```json
{
  "code": 0,
  "data": {
    "file_url": "https://cdn.petvoyage.ai/pets/xxx.jpg",
    "thumbnail_url": "https://cdn.petvoyage.ai/pets/xxx-thumb.jpg"
  }
}
```

---

## 11. 通知模块

### 11.1 获取通知列表

**GET** `/notifications`

**查询参数**: `?page=1&page_size=20&status=unread`

**响应**:
```json
{
  "code": 0,
  "data": {
    "unread_count": 5,
    "items": [
      {
        "id": "notif-xxx",
        "type": "like",  // like | comment | follow | achievement | system
        "title": "有人点赞了你的照片",
        "content": "用户"旅行家"点赞了你的照片",
        "data": {
          "photo_id": "photo-xxx",
          "user_id": "user-xxx"
        },
        "is_read": false,
        "created_at": "2024-03-06T09:30:00Z"
      }
    ]
  }
}
```

---

### 11.2 标记已读

**POST** `/notifications/{notif_id}/read`

**POST** `/notifications/read-all` - 全部标记已读

---

## 12. WebSocket实时通信

### 连接

**URL**: `wss://api.petvoyage.ai/ws?token={access_token}`

### 消息格式

#### 客户端 → 服务端
```json
{
  "type": "subscribe",
  "channel": "user:{user_id}"
}
```

#### 服务端 → 客户端

**照片生成完成**:
```json
{
  "type": "photo_generated",
  "data": {
    "task_id": "task-xxx",
    "photos": [ /* 照片列表 */ ]
  }
}
```

**新通知**:
```json
{
  "type": "notification",
  "data": {
    "id": "notif-xxx",
    "type": "like",
    "title": "...",
    "content": "..."
  }
}
```

---

## 附录

### A. 限流规则

| 接口 | 免费用户 | 付费用户 |
|------|----------|----------|
| 登录 | 10次/小时 | 20次/小时 |
| 生成照片 | 3次/天 | 100次/天 |
| 上传图片 | 10次/小时 | 无限制 |
| 点赞评论 | 100次/小时 | 200次/小时 |

### B. 图片规格

| 用途 | 尺寸 | 格式 | 大小限制 |
|------|------|------|----------|
| 宠物训练照 | 任意 | JPG/PNG | 5MB |
| 头像 | 512x512 | JPG/PNG | 2MB |
| 生成照片(免费) | 1024x1024 | JPG | - |
| 生成照片(付费) | 2048x2048 | PNG | - |

### C. 环境

- **开发环境**: `https://api-dev.petvoyage.ai/v1`
- **测试环境**: `https://api-test.petvoyage.ai/v1`
- **生产环境**: `https://api.petvoyage.ai/v1`
