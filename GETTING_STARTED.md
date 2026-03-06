# 🚀 快速开始

欢迎来到 **PetVoyageAI - AI宠物环游记** 项目！

本文档将帮助你快速搭建开发环境并开始开发。

---

## 📋 项目概览

PetVoyageAI 是一款创新的宠物旅游社交应用，主要功能包括:

- 🎨 **AI宠物虚拟化**: 上传宠物照片，生成多种风格的虚拟形象
- 🌍 **智能照片生成**: 将宠物融入世界各地景点
- 🗺️ **地图解锁**: 收集地标，点亮世界地图
- 🏆 **成就系统**: 完成任务获取奖励
- 👥 **社交分享**: 朋友圈、排行榜

---

## 🛠️ 技术栈

### 后端
- Python 3.11 + FastAPI
- PostgreSQL + MongoDB + Redis
- Replicate AI (图像生成)

### 前端
- iOS: Swift + SwiftUI
- (未来) Android: Kotlin

---

## ⚡ 5分钟启动后端

### 1. 克隆项目并进入目录

```bash
cd ~/PetVoyageAI
```

### 2. 启动数据库服务

```bash
# 启动PostgreSQL, MongoDB, Redis
docker-compose up -d

# 查看状态（确保都是healthy）
docker-compose ps
```

### 3. 配置后端环境

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
```

**重要**: 编辑 `.env` 文件，至少需要配置:
- `REPLICATE_API_TOKEN`: 从 https://replicate.com 获取
- 其他服务可以暂时使用默认配置

### 4. 初始化数据库

```bash
# 创建数据库
createdb petvoyage

# 运行迁移（首次需要先创建迁移文件）
# alembic upgrade head

# 或者直接使用SQL脚本初始化
# psql petvoyage < scripts/init_schema.sql
```

### 5. 启动API服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ 访问 http://localhost:8000/docs 查看API文档!

---

## 📱 启动iOS开发

### 1. 安装依赖

```bash
cd mobile/PetVoyageAI

# 安装CocoaPods依赖
pod install
```

### 2. 打开项目

```bash
open PetVoyageAI.xcworkspace
```

### 3. 配置环境

在 Xcode 中:
1. 选择开发团队 (Signing & Capabilities)
2. 修改 Bundle Identifier (如果需要)

### 4. 运行

选择模拟器或真机，点击 Run (⌘R)

---

## 📚 下一步

### 阅读文档

- [技术规格文档](docs/TECH_SPEC.md) - 了解系统架构
- [API设计文档](docs/API_DESIGN.md) - 查看所有API接口
- [数据库设计文档](docs/DATABASE_SCHEMA.md) - 了解数据结构
- [开发指南](docs/DEVELOPMENT_GUIDE.md) - 开发规范和最佳实践

### 开始开发

#### 后端第一个功能: 用户注册登录

1. 创建数据模型
```bash
cd backend
touch app/models/user.py
```

2. 创建API路由
```bash
touch app/api/v1/auth.py
```

3. 编写业务逻辑
```bash
touch app/services/auth_service.py
```

4. 编写测试
```bash
touch tests/test_auth.py
pytest tests/test_auth.py
```

#### iOS第一个功能: 登录界面

1. 创建登录视图
```swift
// Views/Auth/LoginView.swift
```

2. 创建ViewModel
```swift
// ViewModels/AuthViewModel.swift
```

3. 集成API服务
```swift
// Services/AuthService.swift
```

---

## 🔧 常用命令

### 后端

```bash
# 启动开发服务器
uvicorn app.main:app --reload

# 运行测试
pytest

# 代码格式化
black app/

# 数据库迁移
alembic upgrade head

# 进入Python Shell
python -c "from app.db.session import SessionLocal; db = SessionLocal()"
```

### Docker

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止所有服务
docker-compose down

# 重启某个服务
docker-compose restart postgres
```

### iOS

```bash
# 清理构建
rm -rf ~/Library/Developer/Xcode/DerivedData

# 重新安装Pod
pod deintegrate && pod install

# 运行测试
xcodebuild test -workspace PetVoyageAI.xcworkspace -scheme PetVoyageAI
```

---

## 🎯 开发路线图

### MVP v1.0 (8-10周)

**Week 1-2: 基础架构**
- [x] 项目初始化
- [ ] 数据库设计
- [ ] API框架搭建
- [ ] iOS项目搭建

**Week 3-4: 用户认证**
- [ ] 手机号登录
- [ ] Apple登录
- [ ] JWT认证
- [ ] iOS登录界面

**Week 5-6: 宠物管理**
- [ ] 创建宠物
- [ ] LoRA模型训练
- [ ] 宠物列表展示

**Week 7-8: AI生成**
- [ ] 接入Replicate API
- [ ] 图片生成队列
- [ ] 多种风格支持
- [ ] iOS生成界面

**Week 9-10: 地图与成就**
- [ ] 地图数据导入
- [ ] 解锁逻辑
- [ ] 成就系统
- [ ] 地图UI

---

## 🐛 遇到问题?

### 常见问题

**Q: Docker容器启动失败**
```bash
# 查看日志
docker-compose logs postgres

# 清理并重启
docker-compose down -v
docker-compose up -d
```

**Q: Python依赖安装失败**
```bash
# 升级pip
pip install --upgrade pip

# 清理缓存重试
pip cache purge
pip install -r requirements.txt
```

**Q: iOS编译错误**
```bash
# 清理DerivedData
rm -rf ~/Library/Developer/Xcode/DerivedData

# 重新安装Pod
pod deintegrate
pod install
```

### 获取帮助

- 查看 [开发指南](docs/DEVELOPMENT_GUIDE.md) 的"常见问题"章节
- 提交 GitHub Issue
- 加入开发者交流群

---

## 🎓 学习资源

### FastAPI入门
- [官方教程](https://fastapi.tiangolo.com/tutorial/)
- [Real Python - FastAPI](https://realpython.com/fastapi-python-web-apis/)

### SwiftUI入门
- [Apple官方教程](https://developer.apple.com/tutorials/swiftui)
- [Hacking with Swift](https://www.hackingwithswift.com/100/swiftui)

### AI图像生成
- [Replicate文档](https://replicate.com/docs)
- [Stable Diffusion指南](https://stable-diffusion-art.com/)

---

## 📝 贡献指南

### 提交代码

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交代码 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### Commit规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: 新功能
fix: Bug修复
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

---

## 📞 联系我们

- 项目主页: https://github.com/yourname/PetVoyageAI
- 问题反馈: https://github.com/yourname/PetVoyageAI/issues

---

**祝你开发愉快! 🎉**

如果觉得这个项目有帮助，请给我们一个 ⭐️ Star!
