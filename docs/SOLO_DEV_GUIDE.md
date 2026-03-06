# 👤 个人开发者实战指南

> 为个人开发者量身定制的技术方案 - 简单、快速、低成本

---

## 🎯 核心原则

作为个人开发者，我们要遵循：
- ✅ **技术栈简单** - 一个人能搞定
- ✅ **快速上线** - MVP 2-3周
- ✅ **成本低廉** - 月成本 < ¥200
- ✅ **易于维护** - 不需要7x24运维

---

## 🛠️ 简化后的技术栈

### 后端

**方案A：纯Python全栈（推荐）**

```
FastAPI（Web框架）
    ↓
SQLite（数据库） - 开发环境
PostgreSQL（数据库） - 生产环境（可选）
    ↓
硅基流动 API（AI生成）
    ↓
本地文件存储 or 七牛云（图片）
```

**为什么这样选？**

1. **SQLite** vs PostgreSQL + MongoDB + Redis
   - ✅ 无需安装数据库服务器
   - ✅ 一个文件搞定
   - ✅ 适合早期MVP（< 1万用户）
   - ✅ 后期可无缝迁移到PostgreSQL

2. **本地文件存储** vs OSS
   - ✅ 开发阶段免费
   - ✅ 部署时再考虑七牛云（每月10GB免费）

3. **去掉Celery**
   - ✅ 用FastAPI的BackgroundTasks
   - ✅ 减少Redis依赖
   - ✅ 简化部署

---

### 前端

**方案B：Web优先 + PWA（推荐）**

```
React + Vite（Web应用）
    ↓
PWA（可安装到手机桌面）
    ↓
后期再考虑原生App
```

**为什么不直接做iOS？**

- ❌ iOS需要Mac + Xcode + $99/年开发者账号
- ❌ 审核周期长
- ❌ 迭代慢

- ✅ Web应用无需审核
- ✅ 跨平台（iOS/Android/PC都能用）
- ✅ 迭代快速
- ✅ PWA可以添加到手机桌面，体验接近App

---

## 📦 最简MVP架构

### 项目结构

```
PetVoyageAI/
├── backend/                  # 后端
│   ├── app/
│   │   ├── main.py          # FastAPI入口
│   │   ├── database.py      # SQLite数据库
│   │   ├── models.py        # 数据模型
│   │   ├── api.py           # API路由
│   │   └── ai_service.py    # AI调用服务
│   ├── data.db              # SQLite数据库文件
│   ├── uploads/             # 上传的照片
│   ├── generated/           # 生成的照片
│   └── requirements.txt
│
└── frontend/                 # 前端
    ├── public/
    ├── src/
    │   ├── pages/           # 页面
    │   ├── components/      # 组件
    │   └── api/             # API调用
    ├── package.json
    └── vite.config.js
```

---

## 🗄️ 数据库设计（SQLite版本）

### 为什么SQLite够用？

- ✅ 单用户每秒可以处理**1000次**读写
- ✅ 数据库文件 < 1GB时性能优秀
- ✅ 估算：1万用户 x 100张照片 = 100万条记录 ≈ 500MB

### 数据表设计

```sql
-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone VARCHAR(20) UNIQUE,
    username VARCHAR(50),
    avatar_url VARCHAR(500),
    subscription_type VARCHAR(20) DEFAULT 'free',
    daily_quota_used INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 宠物表
CREATE TABLE pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(50),
    type VARCHAR(20),  -- dog/cat/other
    breed VARCHAR(100),
    photo_url VARCHAR(500),  -- 只存一张代表照片
    ai_description TEXT,  -- AI提取的宠物特征描述
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 照片表
CREATE TABLE photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    pet_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    image_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    style VARCHAR(20),  -- realistic/pixel/anime
    season VARCHAR(20),  -- spring/summer/autumn/winter
    time_of_day VARCHAR(20),  -- sunrise/noon/sunset/night
    prompt TEXT,  -- 使用的提示词
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (pet_id) REFERENCES pets(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- 地点表（预置数据）
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    name_en VARCHAR(255),
    continent VARCHAR(50),  -- asia/europe/americas
    country VARCHAR(100),
    category VARCHAR(50),
    icon VARCHAR(10),
    prompt_template TEXT,  -- AI生成的提示词模板
    unlock_count INTEGER DEFAULT 0
);

-- 解锁记录
CREATE TABLE unlocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    photo_id INTEGER NOT NULL,
    unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, location_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- 成就表（预置数据）
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    description TEXT,
    icon VARCHAR(10),
    condition_type VARCHAR(50),
    condition_value INTEGER
);

-- 用户成就
CREATE TABLE user_achievements (
    user_id INTEGER,
    achievement_id INTEGER,
    unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, achievement_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(id)
);

-- 创建索引
CREATE INDEX idx_photos_user ON photos(user_id);
CREATE INDEX idx_photos_pet ON photos(pet_id);
CREATE INDEX idx_unlocks_user ON unlocks(user_id);
```

---

## 🚀 快速启动（30分钟搭建环境）

### 步骤1：安装依赖

```bash
# 进入项目目录
cd ~/PetVoyageAI

# 后端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pillow httpx python-multipart

# 前端（可选，先做后端）
# cd ../frontend
# npm install
```

### 步骤2：创建数据库

```python
# backend/create_db.py

from sqlalchemy import create_engine, text

# 创建SQLite数据库
engine = create_engine('sqlite:///data.db')

# 执行上面的CREATE TABLE语句
with open('schema.sql', 'r') as f:
    schema = f.read()

with engine.connect() as conn:
    for statement in schema.split(';'):
        if statement.strip():
            conn.execute(text(statement))
    conn.commit()

print("✅ 数据库创建成功！")
```

```bash
python create_db.py
```

### 步骤3：启动后端

```python
# backend/app/main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import httpx

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库
engine = create_engine('sqlite:///data.db')

# 静态文件（存储上传的照片）
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

# ==================== API ====================

@app.get("/")
def root():
    return {"message": "PetVoyageAI API"}

# 创建宠物
@app.post("/api/pets")
async def create_pet(
    name: str,
    type: str,
    breed: str = None,
    photo: UploadFile = File(...)
):
    # 1. 保存照片
    photo_path = f"uploads/pets/{photo.filename}"
    with open(photo_path, "wb") as f:
        f.write(await photo.read())

    # 2. 调用AI提取宠物特征（可选）
    ai_description = await extract_pet_features(photo_path)

    # 3. 保存到数据库
    with Session(engine) as session:
        # 插入数据库的代码...
        pass

    return {"id": 1, "name": name, "photo_url": f"/{photo_path}"}


# 生成照片
@app.post("/api/photos/generate")
async def generate_photo(
    pet_id: int,
    location_id: int,
    style: str = "realistic",
    season: str = "summer",
    time_of_day: str = "sunset"
):
    # 1. 获取宠物和地点信息
    with Session(engine) as session:
        # 查询数据库...
        pet_desc = "a corgi dog"
        location_prompt = "at Eiffel Tower in Paris"

    # 2. 构建Prompt
    prompt = build_prompt(pet_desc, location_prompt, style, season, time_of_day)

    # 3. 调用硅基流动API
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.siliconflow.cn/v1/image/generations",
            headers={
                "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "stabilityai/stable-diffusion-xl-base-1.0",
                "prompt": prompt,
                "image_size": "1024x1024",
                "num_inference_steps": 20,
                "batch_size": 3
            }
        )

    result = response.json()
    image_urls = [img["url"] for img in result["images"]]

    # 4. 下载并保存图片
    saved_urls = []
    for i, url in enumerate(image_urls):
        # 下载图片并保存到本地
        saved_url = await download_and_save(url, f"generated/photo_{i}.jpg")
        saved_urls.append(saved_url)

    return {
        "task_id": "xxx",
        "status": "completed",
        "photos": [{"url": url} for url in saved_urls]
    }


def build_prompt(pet_desc, location, style, season, time_of_day):
    """构建AI提示词"""

    season_desc = {
        "spring": "spring season, cherry blossoms, fresh green",
        "summer": "summer, bright sunshine, blue sky",
        "autumn": "autumn, golden leaves, warm colors",
        "winter": "winter, snow, cold atmosphere"
    }

    time_desc = {
        "sunrise": "sunrise, golden hour, soft morning light",
        "noon": "midday, bright sunlight",
        "sunset": "sunset, golden hour, warm evening light",
        "night": "night time, city lights"
    }

    style_desc = {
        "realistic": "professional photography, 8k, realistic",
        "pixel": "pixel art style, 8-bit retro game",
        "anime": "anime style, Studio Ghibli illustration"
    }

    prompt = f"{pet_desc} {location}, {season_desc[season]}, {time_desc[time_of_day]}, {style_desc[style]}"

    return prompt


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# 启动
python -m app.main
```

访问 http://localhost:8000 测试！

---

## 💰 成本估算（个人开发者版）

### 开发阶段（免费）

- ✅ **服务器**: 本地开发，¥0
- ✅ **数据库**: SQLite，¥0
- ✅ **图片存储**: 本地文件，¥0
- ✅ **AI生成**: 硅基流动（前期测试可能有免费额度）

**总成本: ¥0**

---

### 上线后（100个用户）

假设每用户每月生成10张照片：

| 项目 | 方案 | 成本 |
|------|------|------|
| 服务器 | 阿里云/腾讯云学生机<br>1核2G | **¥10/月** |
| 图片存储 | 七牛云对象存储<br>10GB免费 | **¥0** |
| 流量 | 10GB/月 | **¥0** |
| AI生成 | 硅基流动<br>1000张 x ¥0.02 | **¥20** |
| 域名 | .com域名 | **¥5/月** |
| **总计** | | **¥35/月** |

---

### 扩展后（1000个用户）

| 项目 | 方案 | 成本 |
|------|------|------|
| 服务器 | 阿里云2核4G | **¥50/月** |
| 图片存储 | 七牛云50GB | **¥5/月** |
| 流量 | 50GB/月 | **¥10/月** |
| AI生成 | 10000张 x ¥0.02 | **¥200** |
| 数据库 | 迁移到PostgreSQL（可选） | **¥0-30/月** |
| **总计** | | **¥265-295/月** |

**均摊**：¥0.27/用户/月

---

## 🎨 Web前端（React + Vite）

### 为什么选Web？

**对比表**：

| 方案 | 优点 | 缺点 | 适合场景 |
|------|------|------|----------|
| **iOS原生** | 性能好，体验佳 | 需要Mac、审核慢、迭代慢 | 有资金、有团队 |
| **React Native** | 跨平台 | 学习成本高、打包复杂 | 有React经验 |
| **Web + PWA** | 快速开发、跨平台、无需审核 | 性能略差 | **个人开发者** ⭐ |

### 技术栈

```
React 18（UI框架）
  ↓
Vite（构建工具，比Webpack快10倍）
  ↓
Tailwind CSS（样式，快速美化）
  ↓
React Query（API请求管理）
  ↓
Zustand（状态管理，比Redux简单）
```

### 快速启动

```bash
# 创建项目
npm create vite@latest frontend -- --template react
cd frontend
npm install

# 安装依赖
npm install tailwindcss axios @tanstack/react-query zustand

# 启动
npm run dev
```

访问 http://localhost:5173

### 示例代码

```jsx
// src/pages/Home.jsx

import { useState } from 'react'
import axios from 'axios'

function HomePage() {
  const [pet, setPet] = useState(null)
  const [location, setLocation] = useState(null)
  const [generating, setGenerating] = useState(false)
  const [photos, setPhotos] = useState([])

  const handleGenerate = async () => {
    setGenerating(true)

    try {
      const response = await axios.post('http://localhost:8000/api/photos/generate', {
        pet_id: pet.id,
        location_id: location.id,
        style: 'realistic',
        season: 'summer',
        time_of_day: 'sunset'
      })

      setPhotos(response.data.photos)
    } catch (error) {
      console.error(error)
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">🌍 旺财的环球之旅</h1>

      {/* 选择宠物 */}
      <div className="mb-4">
        <h2 className="text-xl mb-2">选择宠物</h2>
        {/* 宠物列表 */}
      </div>

      {/* 选择景点 */}
      <div className="mb-4">
        <h2 className="text-xl mb-2">选择目的地</h2>
        {/* 景点列表 */}
      </div>

      {/* 生成按钮 */}
      <button
        onClick={handleGenerate}
        disabled={!pet || !location || generating}
        className="bg-blue-500 text-white px-6 py-3 rounded-lg"
      >
        {generating ? '生成中...' : '✨ 生成照片'}
      </button>

      {/* 生成的照片 */}
      {photos.length > 0 && (
        <div className="mt-8 grid grid-cols-3 gap-4">
          {photos.map((photo, i) => (
            <img key={i} src={photo.url} alt="" className="rounded-lg" />
          ))}
        </div>
      )}
    </div>
  )
}

export default HomePage
```

---

## 📲 PWA配置（让Web变成App）

### 添加manifest.json

```json
{
  "name": "PetVoyageAI",
  "short_name": "宠物环游记",
  "description": "带你的宠物环游世界",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4F46E5",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 用户使用体验

iOS Safari:
1. 打开网站
2. 点击"分享"
3. 选择"添加到主屏幕"
4. 🎉 像App一样使用

Android Chrome:
1. 打开网站
2. 弹出提示"添加到主屏幕"
3. 🎉 安装完成

---

## 🚀 部署方案

### 方案1：Vercel（最简单）⭐

**前端部署**：
```bash
# 安装Vercel CLI
npm install -g vercel

# 部署
cd frontend
vercel
```

3分钟搞定！自动HTTPS、自动CDN。

**成本**：免费（hobby plan）

---

### 方案2：服务器（完整控制）

**1. 购买服务器**
- 阿里云学生机：¥10/月（1核2G）
- 腾讯云轻量应用服务器：¥50/月（2核4G）

**2. 部署**

```bash
# SSH登录服务器
ssh root@your-server-ip

# 安装Python
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 克隆代码
git clone https://github.com/yourname/PetVoyageAI.git
cd PetVoyageAI/backend

# 安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 运行（使用gunicorn）
pip install gunicorn
gunicorn app.main:app --bind 0.0.0.0:8000 --workers 2 --daemon

# 配置Nginx反向代理
sudo apt install nginx
sudo nano /etc/nginx/sites-available/petvoyage

# 写入配置
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    location /uploads {
        alias /path/to/uploads;
    }
}

# 启用配置
sudo ln -s /etc/nginx/sites-available/petvoyage /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## ⚡ 性能优化建议

### 1. 图片优化

```python
from PIL import Image

def optimize_image(input_path, output_path, quality=85):
    """压缩图片"""
    img = Image.open(input_path)

    # 缩放
    if img.width > 1024:
        ratio = 1024 / img.width
        new_size = (1024, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    # 保存（优化质量）
    img.save(output_path, quality=quality, optimize=True)
```

### 2. 添加缓存

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_location(location_id: int):
    """缓存地点信息"""
    # 查询数据库...
    return location
```

### 3. CDN加速（七牛云）

免费10GB存储 + 10GB流量/月

---

## 📝 总结

### 个人开发者优化后的方案

| 之前方案 | 现在方案 | 理由 |
|---------|---------|------|
| PostgreSQL + MongoDB + Redis | **SQLite** | 简单，够用 |
| Docker部署 | **直接运行** | 减少复杂度 |
| Celery异步 | **BackgroundTasks** | 无需Redis |
| OSS | **本地文件 + 七牛云** | 免费 |
| iOS原生 | **Web + PWA** | 快速迭代 |

### 开发时间线

**Week 1**:
- ✅ 搭建后端（FastAPI + SQLite）
- ✅ 实现宠物管理API
- ✅ 接入硅基流动API

**Week 2**:
- ✅ 实现照片生成API
- ✅ 地点数据导入
- ✅ 解锁逻辑

**Week 3**:
- ✅ 搭建前端（React）
- ✅ 主要页面开发
- ✅ 前后端联调

**Week 4**:
- ✅ 四季主题
- ✅ 分享功能
- ✅ 部署上线

**总计：4周MVP上线**

---

## 🆘 我能帮你什么？

现在我可以：

1. **立即开始写代码**
   - 从后端开始，完整的FastAPI代码
   - 可运行的Demo

2. **先做一个最小Demo**
   - 一个Python脚本调用硅基流动API
   - 验证AI生成效果

3. **详细讲解某个部分**
   - 如何构建好的Prompt
   - SQLite如何设计
   - React前端如何写

你希望我从哪里开始？
