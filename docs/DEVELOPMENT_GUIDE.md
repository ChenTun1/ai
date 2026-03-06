# 开发指南

本文档提供PetVoyageAI项目的开发环境搭建、开发规范、测试指南等内容。

---

## 1. 开发环境搭建

### 1.1 前置要求

#### 后端开发
- Python 3.11+
- PostgreSQL 15+
- MongoDB 6.0+
- Redis 7.0+
- Docker & Docker Compose

#### iOS开发
- macOS 13.0+
- Xcode 15.0+
- CocoaPods 1.12+
- iOS 16.0+ (部署目标)

---

### 1.2 后端环境搭建

#### 克隆项目
```bash
git clone https://github.com/yourname/PetVoyageAI.git
cd PetVoyageAI/backend
```

#### 使用Docker Compose启动依赖服务
```bash
# 启动PostgreSQL, MongoDB, Redis
docker-compose up -d

# 查看服务状态
docker-compose ps
```

#### 创建Python虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows
```

#### 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

#### 配置环境变量
```bash
cp .env.example .env
```

编辑 `.env` 文件:
```bash
# 数据库配置
DATABASE_URL=postgresql://petvoyage:password@localhost:5432/petvoyage
MONGODB_URL=mongodb://localhost:27017/petvoyage
REDIS_URL=redis://localhost:6379

# JWT密钥
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7天

# AI服务配置
REPLICATE_API_TOKEN=r8_xxx  # 从replicate.com获取
AI_MODEL=stability-ai/sdxl

# 对象存储
OSS_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
OSS_ACCESS_KEY_ID=your-access-key
OSS_ACCESS_KEY_SECRET=your-secret-key
OSS_BUCKET=petvoyage-prod

# 第三方服务
ALIYUN_SMS_ACCESS_KEY=xxx
ALIYUN_SMS_SECRET=xxx
BAIDU_API_KEY=xxx  # 内容审核
APPLE_TEAM_ID=xxx
```

#### 初始化数据库
```bash
# 创建数据库
createdb petvoyage

# 运行迁移
alembic upgrade head

# 加载初始数据
python scripts/init_data.py
```

#### 启动开发服务器
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看API文档

---

### 1.3 iOS环境搭建

#### 打开项目
```bash
cd mobile/PetVoyageAI
pod install
open PetVoyageAI.xcworkspace
```

#### 配置环境
创建 `Config.xcconfig`:
```
API_BASE_URL = https://api-dev.petvoyage.ai/v1
REPLICATE_API_TOKEN = r8_xxx
```

#### 运行项目
1. 选择模拟器或真机
2. 点击 Run (⌘R)

---

## 2. 项目结构

### 2.1 后端结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   │
│   ├── api/                 # API路由
│   │   ├── v1/
│   │   │   ├── auth.py      # 认证相关
│   │   │   ├── users.py     # 用户相关
│   │   │   ├── pets.py      # 宠物相关
│   │   │   ├── photos.py    # 照片生成
│   │   │   ├── locations.py # 地图相关
│   │   │   ├── social.py    # 社交相关
│   │   │   └── ...
│   │
│   ├── core/                # 核心模块
│   │   ├── auth.py          # JWT认证
│   │   ├── security.py      # 安全工具
│   │   └── deps.py          # 依赖注入
│   │
│   ├── models/              # 数据模型
│   │   ├── user.py
│   │   ├── pet.py
│   │   └── ...
│   │
│   ├── schemas/             # Pydantic Schema
│   │   ├── user.py
│   │   ├── pet.py
│   │   └── ...
│   │
│   ├── services/            # 业务逻辑
│   │   ├── ai_service.py    # AI图像生成
│   │   ├── oss_service.py   # 对象存储
│   │   ├── sms_service.py   # 短信服务
│   │   └── ...
│   │
│   ├── db/                  # 数据库
│   │   ├── postgresql.py    # PG连接
│   │   ├── mongodb.py       # Mongo连接
│   │   └── redis.py         # Redis连接
│   │
│   └── utils/               # 工具函数
│       ├── image.py         # 图片处理
│       ├── validation.py    # 数据验证
│       └── ...
│
├── alembic/                 # 数据库迁移
│   └── versions/
│
├── tests/                   # 测试
│   ├── test_auth.py
│   ├── test_pets.py
│   └── ...
│
├── scripts/                 # 脚本
│   ├── init_data.py         # 初始化数据
│   └── migrate_mongo.py     # MongoDB迁移
│
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── docker-compose.yml
└── Dockerfile
```

---

### 2.2 iOS结构

```
PetVoyageAI/
├── App/
│   ├── PetVoyageAIApp.swift    # 应用入口
│   └── AppDelegate.swift
│
├── Models/                     # 数据模型
│   ├── User.swift
│   ├── Pet.swift
│   ├── Photo.swift
│   └── ...
│
├── Views/                      # 视图
│   ├── Auth/
│   │   ├── LoginView.swift
│   │   └── RegisterView.swift
│   ├── Home/
│   │   └── HomeView.swift
│   ├── Pets/
│   │   ├── PetListView.swift
│   │   ├── PetDetailView.swift
│   │   └── CreatePetView.swift
│   ├── Generate/
│   │   ├── GenerateView.swift
│   │   └── StyleSelectorView.swift
│   ├── Map/
│   │   └── MapView.swift
│   ├── Social/
│   │   ├── FeedView.swift
│   │   └── ProfileView.swift
│   └── Components/            # 可复用组件
│       ├── PhotoCard.swift
│       ├── PetAvatar.swift
│       └── ...
│
├── ViewModels/                # 视图模型
│   ├── AuthViewModel.swift
│   ├── PetViewModel.swift
│   └── ...
│
├── Services/                  # 服务层
│   ├── APIService.swift       # API请求
│   ├── AuthService.swift      # 认证服务
│   ├── ImageService.swift     # 图片处理
│   └── StorageService.swift   # 本地存储
│
├── Utils/                     # 工具
│   ├── Extensions/
│   ├── Constants.swift
│   └── ImagePicker.swift
│
├── Resources/                 # 资源
│   ├── Assets.xcassets
│   ├── Localizable.strings
│   └── Info.plist
│
└── PetVoyageAITests/
    └── ...
```

---

## 3. 开发规范

### 3.1 代码风格

#### Python (遵循PEP 8)
```python
# 使用black格式化
black app/

# 使用flake8检查
flake8 app/

# 使用mypy类型检查
mypy app/
```

#### Swift (遵循Swift Style Guide)
```swift
// 使用SwiftLint检查
swiftlint
```

---

### 3.2 Git工作流

#### 分支命名
```
main              # 生产分支
develop           # 开发分支
feature/xxx       # 功能分支
bugfix/xxx        # bug修复
hotfix/xxx        # 紧急修复
release/v1.0.0    # 发布分支
```

#### Commit Message规范 (Conventional Commits)

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**:
```
feat(auth): 添加Apple登录支持

- 集成Sign in with Apple
- 添加Apple用户标识绑定逻辑
- 更新登录流程

Closes #123
```

---

### 3.3 代码审查清单

#### 通用
- [ ] 代码符合风格规范
- [ ] 无明显性能问题
- [ ] 无安全漏洞（SQL注入、XSS等）
- [ ] 错误处理完善
- [ ] 日志记录合理

#### 后端
- [ ] API遵循RESTful设计
- [ ] 数据验证完整（Pydantic Schema）
- [ ] 数据库查询已优化（索引、N+1问题）
- [ ] 单元测试覆盖率 > 80%

#### 前端
- [ ] UI符合设计稿
- [ ] 网络请求有加载状态
- [ ] 错误提示友好
- [ ] 图片使用缓存

---

## 4. 测试

### 4.1 后端测试

#### 单元测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_auth.py

# 生成覆盖率报告
pytest --cov=app --cov-report=html
```

#### 测试示例
```python
# tests/test_pets.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_pet(auth_headers):
    """测试创建宠物"""
    response = client.post(
        "/api/v1/pets",
        json={
            "name": "旺财",
            "type": "dog",
            "breed": "柯基"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "旺财"
```

#### 集成测试
```python
@pytest.mark.integration
def test_photo_generation_flow():
    """测试完整的照片生成流程"""
    # 1. 创建宠物
    pet = create_test_pet()

    # 2. 触发生成
    task = generate_photo(pet.id, location_id="loc-xxx")

    # 3. 等待完成
    result = wait_for_task(task.task_id)

    # 4. 保存照片
    photo = save_photo(result.photos[0])

    assert photo.status == "published"
```

---

### 4.2 iOS测试

#### 单元测试
```swift
// PetVoyageAITests/ViewModelTests.swift
import XCTest
@testable import PetVoyageAI

class PetViewModelTests: XCTestCase {
    var viewModel: PetViewModel!

    override func setUp() {
        super.setUp()
        viewModel = PetViewModel()
    }

    func testCreatePet() async throws {
        let pet = try await viewModel.createPet(
            name: "旺财",
            type: .dog,
            breed: "柯基",
            photos: []
        )

        XCTAssertEqual(pet.name, "旺财")
        XCTAssertEqual(pet.type, .dog)
    }
}
```

#### UI测试
```swift
// PetVoyageAIUITests/LoginUITests.swift
class LoginUITests: XCTestCase {
    func testLoginFlow() {
        let app = XCUIApplication()
        app.launch()

        // 输入手机号
        app.textFields["phone"].tap()
        app.textFields["phone"].typeText("13800138000")

        // 发送验证码
        app.buttons["send_code"].tap()

        // 输入验证码
        app.textFields["code"].tap()
        app.textFields["code"].typeText("123456")

        // 登录
        app.buttons["login"].tap()

        // 验证跳转到主页
        XCTAssertTrue(app.tabBars["main_tab"].exists)
    }
}
```

---

## 5. 调试技巧

### 5.1 后端调试

#### 使用pdb调试
```python
import pdb

def generate_photo(pet_id: str):
    # 设置断点
    pdb.set_trace()

    result = ai_service.generate(...)
    return result
```

#### 查看SQL日志
```python
# config.py
SQLALCHEMY_ECHO = True  # 打印所有SQL
```

#### 使用日志
```python
import logging

logger = logging.getLogger(__name__)

logger.debug("调试信息")
logger.info("常规信息")
logger.warning("警告")
logger.error("错误", exc_info=True)  # 包含堆栈
```

---

### 5.2 iOS调试

#### 使用断点
```swift
func generatePhoto() {
    let prompt = buildPrompt()  // 设置断点
    apiService.generate(prompt)
}
```

#### 打印调试
```swift
// 使用dump打印完整结构
dump(user)

// 条件断点
print("User ID: \(user.id)")
```

#### 网络请求调试
```swift
// 使用Charles或Proxyman抓包
// 配置：设置 → Wi-Fi → HTTP代理
```

---

## 6. 部署

### 6.1 后端部署

#### Docker部署
```bash
# 构建镜像
docker build -t petvoyage-api:v1.0.0 .

# 推送到镜像仓库
docker tag petvoyage-api:v1.0.0 registry.cn-hangzhou.aliyuncs.com/petvoyage/api:v1.0.0
docker push registry.cn-hangzhou.aliyuncs.com/petvoyage/api:v1.0.0

# 在服务器上运行
docker run -d \
  --name petvoyage-api \
  -p 8000:8000 \
  --env-file .env.prod \
  petvoyage-api:v1.0.0
```

#### Nginx配置
```nginx
server {
    listen 80;
    server_name api.petvoyage.ai;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

### 6.2 iOS部署

#### TestFlight内测
```bash
# 1. Archive构建
Xcode → Product → Archive

# 2. 上传到App Store Connect
Organizer → Distribute App → App Store Connect

# 3. 在App Store Connect添加测试用户
```

#### App Store发布
```bash
# 1. 准备材料
- 应用截图 (6.5" & 5.5")
- 应用描述
- 关键词
- 隐私政策URL

# 2. 提交审核
App Store Connect → 我的App → 准备提交

# 3. 等待审核（通常1-3天）
```

---

## 7. 常见问题

### Q1: 本地运行时数据库连接失败
**A**: 检查Docker容器是否正常运行:
```bash
docker-compose ps
docker-compose logs postgres
```

### Q2: AI生成图片失败
**A**:
1. 检查Replicate API Token是否正确
2. 查看API配额是否用完
3. 检查网络连接

### Q3: iOS编译失败
**A**:
```bash
# 清理构建缓存
rm -rf ~/Library/Developer/Xcode/DerivedData

# 重新安装Pod
pod deintegrate
pod install
```

### Q4: 照片上传OSS失败
**A**:
1. 检查OSS配置是否正确
2. 验证Bucket权限
3. 查看OSS控制台日志

---

## 8. 性能优化建议

### 8.1 后端性能

#### 数据库查询优化
```python
# Bad: N+1查询
for photo in photos:
    user = db.query(User).filter(User.id == photo.user_id).first()

# Good: 预加载
photos = db.query(Photo).options(
    joinedload(Photo.user),
    joinedload(Photo.pet)
).all()
```

#### 使用缓存
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_location_by_id(location_id: str):
    return db.query(Location).filter(Location.id == location_id).first()
```

#### 异步处理
```python
# 耗时任务使用Celery异步处理
@celery.task
def generate_image_async(pet_id: str, location_id: str):
    # AI生成逻辑
    pass
```

---

### 8.2 iOS性能

#### 图片加载优化
```swift
// 使用缩略图
imageView.kf.setImage(
    with: photo.thumbnailURL,
    placeholder: UIImage(named: "placeholder")
)

// 懒加载
LazyVGrid {
    ForEach(photos) { photo in
        PhotoCard(photo: photo)
            .task { await loadPhotoIfNeeded(photo) }
    }
}
```

#### 减少重绘
```swift
// 使用equatable避免不必要的重绘
struct PhotoCard: View, Equatable {
    let photo: Photo

    static func == (lhs: PhotoCard, rhs: PhotoCard) -> Bool {
        lhs.photo.id == rhs.photo.id
    }
}
```

---

## 9. 开发工具推荐

### 后端
- **IDE**: PyCharm / VS Code
- **API测试**: Postman / Insomnia
- **数据库**: DBeaver / TablePlus
- **日志查看**: Kibana / Grafana
- **性能分析**: py-spy / cProfile

### iOS
- **IDE**: Xcode
- **网络抓包**: Charles / Proxyman
- **设计工具**: Figma
- **崩溃分析**: Firebase Crashlytics
- **性能分析**: Instruments

### 通用
- **版本控制**: Git + GitHub
- **项目管理**: Linear / Jira
- **文档**: Notion / Confluence
- **沟通**: Slack / Discord

---

## 10. 学习资源

### FastAPI
- 官方文档: https://fastapi.tiangolo.com/
- 教程: Real Python FastAPI Guide

### SwiftUI
- 官方文档: https://developer.apple.com/documentation/swiftui
- 教程: Hacking with Swift - 100 Days of SwiftUI

### AI图像生成
- Replicate文档: https://replicate.com/docs
- Stable Diffusion: https://stability.ai/

### PostgreSQL
- 官方文档: https://www.postgresql.org/docs/
- 性能优化: Use The Index, Luke

---

## 附录

### A. 开发环境变量完整示例

```bash
# .env.development
DEBUG=true
ENVIRONMENT=development

# 数据库
DATABASE_URL=postgresql://petvoyage:dev123@localhost:5432/petvoyage_dev
MONGODB_URL=mongodb://localhost:27017/petvoyage_dev
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=dev-secret-key-not-for-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI服务
REPLICATE_API_TOKEN=r8_xxx
AI_DEFAULT_MODEL=stability-ai/sdxl

# 对象存储（开发环境用测试bucket）
OSS_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
OSS_ACCESS_KEY_ID=xxx
OSS_ACCESS_KEY_SECRET=xxx
OSS_BUCKET=petvoyage-dev

# 短信服务（开发环境不发送真实短信）
SMS_ENABLED=false
ALIYUN_SMS_ACCESS_KEY=xxx
ALIYUN_SMS_SECRET=xxx

# 日志
LOG_LEVEL=DEBUG
```

### B. 有用的命令

```bash
# 后端
make run          # 启动开发服务器
make test         # 运行测试
make lint         # 代码检查
make format       # 格式化代码
make migrate      # 运行数据库迁移
make shell        # 进入Python Shell

# Docker
docker-compose up -d          # 启动所有服务
docker-compose logs -f api    # 查看API日志
docker-compose exec db psql   # 进入PostgreSQL
docker-compose down           # 停止所有服务

# iOS
xcodebuild clean              # 清理
xcodebuild test               # 运行测试
swiftlint autocorrect         # 自动修复lint问题
```
