# 🐾 PetVoyageAI Backend

个人开发者简化版 - 基于 SQLite + 硅基流动 AI

## 📦 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

编辑 `.env` 文件，配置你的硅基流动 API Key:

```bash
SILICONFLOW_API_KEY=你的API密钥
```

> 获取 API Key: 访问 https://siliconflow.cn 注册并获取

### 3. 系统检查

```bash
# 运行系统验证脚本
python test_system.py
```

如果所有测试通过，继续下一步。

### 4. 初始化数据库

```bash
# 创建数据库表并导入景点数据
python scripts/init_db.py
```

### 5. 启动服务器

```bash
# 方式 1: 使用 Python 直接运行
python -m app.main

# 方式 2: 使用 uvicorn（推荐）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 访问 API 文档

打开浏览器访问:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 📚 项目结构

```
backend/
├── app/
│   ├── api/v1/          # API 路由
│   │   ├── pets.py      # 宠物管理
│   │   ├── photos.py    # 照片生成
│   │   └── locations.py # 景点查询
│   ├── core/            # 核心模块
│   │   ├── config.py    # 配置管理
│   │   └── database.py  # 数据库连接
│   ├── models/          # 数据模型
│   ├── services/        # 业务服务
│   │   └── ai_service.py # AI 图像生成
│   ├── schemas/         # Pydantic Schema
│   └── main.py          # 应用入口
├── scripts/             # 工具脚本
│   ├── init_db.py       # 数据库初始化
│   └── init_locations.py # 景点数据
├── data/                # 数据目录（自动创建）
│   ├── petvoyage.db     # SQLite 数据库
│   ├── uploads/         # 上传的照片
│   └── generated/       # AI 生成的照片
├── .env                 # 环境配置
├── test_system.py       # 系统测试
└── requirements.txt     # 依赖列表
```

## 🧪 API 测试示例

### 获取景点列表

```bash
curl http://localhost:8000/api/v1/locations
```

### 创建宠物

```bash
curl -X POST http://localhost:8000/api/v1/pets \
  -F "name=旺财" \
  -F "type=dog" \
  -F "breed=柯基"
```

### 生成照片

```bash
curl -X POST http://localhost:8000/api/v1/photos/generate \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "location_id": 1,
    "style": "realistic",
    "season": "summer",
    "time_of_day": "sunset"
  }'
```

## 📊 数据库

### 查看数据库

```bash
# 使用 SQLite CLI
sqlite3 data/petvoyage.db

# 查看所有表
.tables

# 查看景点数据
SELECT * FROM locations LIMIT 5;

# 退出
.quit
```

### 重置数据库

```bash
# 删除数据库文件
rm -rf data/

# 重新初始化
python scripts/init_db.py
```

## 🐛 故障排除

### 导入错误

```bash
# 确保在 backend 目录下运行
cd backend

# 检查 Python 路径
python -c "import sys; print(sys.path)"
```

### 数据库错误

```bash
# 检查数据目录权限
ls -la data/

# 重新创建数据库
rm data/petvoyage.db
python scripts/init_db.py
```

### API Key 错误

检查 `.env` 文件中的 `SILICONFLOW_API_KEY` 是否正确配置。

## 📈 性能优化

### 生产环境建议

当用户数 > 1000 时：

1. **迁移到 PostgreSQL**
   - 修改 `DATABASE_URL` 配置
   - 使用 Alembic 迁移数据

2. **添加 Redis 缓存**
   - 缓存景点数据
   - 缓存用户信息

3. **使用对象存储**
   - 阿里云 OSS
   - 七牛云

4. **添加 Celery 队列**
   - 异步处理 AI 生成任务
   - 提高并发能力

## 📖 文档

- [技术规格](../docs/TECH_SPEC.md)
- [API 设计](../docs/API_DESIGN.md)
- [数据库设计](../docs/DATABASE_SCHEMA.md)
- [开发指南](../docs/DEVELOPMENT_GUIDE.md)
- [产品路线图](../docs/PRODUCT_ROADMAP.md)
- [个人开发者指南](../docs/SOLO_DEV_GUIDE.md)

## 🎯 下一步

- [ ] 实现用户认证（JWT）
- [ ] 接入真实的硅基流动 API
- [ ] 实现文件上传
- [ ] 添加地图解锁逻辑
- [ ] 创建 Web 前端
- [ ] 部署到服务器

## 💬 支持

遇到问题？查看 [项目状态](../STATUS.md) 或创建 Issue。
