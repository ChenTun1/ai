# 🚀 快速启动指南

## 环境要求

- Python 3.11+
- pip

## 步骤1: 安装依赖

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 步骤2: 配置环境变量

编辑 `.env` 文件，填入你的硅基流动 API Key:

```bash
SILICONFLOW_API_KEY=你的API密钥
```

获取方式：访问 https://siliconflow.cn 注册并获取 API Key

## 步骤3: 初始化数据库

```bash
python scripts/init_db.py
```

这将：
- 创建 SQLite 数据库文件
- 创建所有数据表
- 导入景点初始数据

## 步骤4: 启动服务器

```bash
python -m app.main
```

或使用 uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 步骤5: 访问 API 文档

打开浏览器访问:

- Swagger 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 📝 API 测试示例

### 1. 获取景点列表

```bash
curl http://localhost:8000/api/v1/locations
```

### 2. 创建宠物

```bash
curl -X POST http://localhost:8000/api/v1/pets \
  -F "name=旺财" \
  -F "type=dog" \
  -F "breed=柯基" \
  -F "photo=@/path/to/dog.jpg"
```

### 3. 生成照片

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

## 🐛 常见问题

### 数据库文件在哪？

`data/petvoyage.db`

### 上传的图片在哪？

`data/uploads/`

### 生成的图片在哪？

`data/generated/`

### 如何查看日志？

日志默认输出到控制台，级别为 INFO

### 如何重置数据库？

```bash
rm -rf data/
python scripts/init_db.py
```

## 📚 下一步

- 查看 [API设计文档](../docs/API_DESIGN.md)
- 查看 [开发指南](../docs/DEVELOPMENT_GUIDE.md)
- 查看 [产品路线图](../docs/PRODUCT_ROADMAP.md)
