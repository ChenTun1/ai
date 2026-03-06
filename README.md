# 🐾 PetVoyageAI - AI宠物环游记

> 让你的宠物通过AI技术环游世界

## 项目简介

PetVoyageAI是一款创新的宠物旅游社交应用，通过AI图像生成技术，让宠物主人能够创建宠物在世界各地旅行的虚拟照片。结合地图解锁、成就系统等游戏化设计，为用户提供独特的"云养宠"+"云旅游"体验。

## 核心功能

- 🎨 **AI宠物虚拟化**: 上传宠物照片，AI自动生成多种风格的虚拟形象
- 🌍 **智能旅行照片生成**: 将宠物融入世界各地景点照片
- 🗺️ **地图解锁系统**: 收集地标建筑，点亮世界地图
- 🏆 **成就挑战系统**: 完成任务获取徽章和奖励
- 👥 **社交分享**: 应内朋友圈、旅行日记、排行榜
- 💎 **会员订阅**: Freemium模式，提供高级功能

## 技术栈

### 后端
- **语言**: Python 3.11+
- **框架**: FastAPI
- **数据库**: PostgreSQL + MongoDB
- **缓存**: Redis
- **存储**: 阿里云OSS / AWS S3
- **AI服务**: Replicate API / Stability AI

### 前端 (iOS)
- **语言**: Swift
- **UI框架**: SwiftUI
- **网络**: Alamofire
- **图片缓存**: Kingfisher

### DevOps
- **容器化**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **部署**: 阿里云ECS / AWS EC2
- **监控**: Prometheus + Grafana

## 项目结构

```
PetVoyageAI/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型
│   │   ├── services/    # 业务逻辑
│   │   └── utils/       # 工具函数
│   ├── tests/           # 测试
│   ├── requirements.txt
│   └── Dockerfile
├── mobile/              # iOS应用
│   ├── PetVoyageAI/
│   │   ├── Models/
│   │   ├── Views/
│   │   ├── ViewModels/
│   │   └── Services/
│   └── PetVoyageAI.xcodeproj
├── docs/                # 技术文档
│   ├── TECH_SPEC.md         # 技术规格
│   ├── API_DESIGN.md        # API设计
│   ├── DATABASE_SCHEMA.md   # 数据库设计
│   └── DEVELOPMENT_GUIDE.md # 开发指南
└── README.md
```

## 快速开始

### 后端开发环境搭建

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 运行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --reload
```

### iOS开发环境搭建

```bash
# 进入iOS项目目录
cd mobile/PetVoyageAI

# 安装CocoaPods依赖
pod install

# 使用Xcode打开项目
open PetVoyageAI.xcworkspace
```

## 开发规范

- 遵循 PEP 8 (Python) 和 Swift Style Guide
- 所有API必须编写单元测试
- 提交前运行 `pre-commit` 检查
- Commit Message 遵循 Conventional Commits

## 文档

详细技术文档请查看 `docs/` 目录：

- [技术规格文档](docs/TECH_SPEC.md)
- [API设计文档](docs/API_DESIGN.md)
- [数据库设计文档](docs/DATABASE_SCHEMA.md)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)

## 版本规划

### v1.0 MVP (8-10周)
- ✅ 用户注册登录
- ✅ 宠物虚拟化
- ✅ AI图片生成（2-3种风格）
- ✅ 地图解锁
- ✅ 基础成就系统
- ✅ 个人主页与照片发布

### v1.1 游戏化增强 (4-6周)
- ⏳ 每日任务系统
- ⏳ 排行榜
- ⏳ 完整成就体系
- ⏳ 虚拟货币

### v1.2 社交完善 (4-6周)
- ⏳ 应内朋友圈
- ⏳ 评论系统
- ⏳ 关注/粉丝
- ⏳ 旅行日记生成

### v2.0 商业化 (2-3周)
- ⏳ 订阅系统
- ⏳ 虚拟商城
- ⏳ 支付集成

## 团队

- 产品设计: TBD
- 后端开发: TBD
- iOS开发: TBD
- UI/UX设计: TBD

## 许可证

MIT License

## 联系方式

- 项目主页: https://github.com/yourname/PetVoyageAI
- 问题反馈: https://github.com/yourname/PetVoyageAI/issues
