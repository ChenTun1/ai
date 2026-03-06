# PetVoyageAI 部署指南

## 1. 本地 Docker 部署

### 前置要求

- Docker >= 20.10
- Docker Compose >= 2.0

### 快速启动

```bash
# 克隆项目
git clone <repo-url>
cd PetVoyageAI

# 启动所有服务（包括数据库和 API）
docker compose up -d

# 查看服务状态
docker compose ps

# 查看 API 日志
docker compose logs -f api
```

### 仅启动基础设施（不含 API）

```bash
docker compose up -d postgres mongodb redis
```

### 单独构建 API 镜像

```bash
docker compose build api
```

### 停止并清理

```bash
# 停止所有服务
docker compose down

# 停止并删除数据卷
docker compose down -v
```

## 2. 生产环境部署建议

### 安全配置

- 修改所有默认密码（PostgreSQL、MongoDB、Redis）
- 设置强 `SECRET_KEY`，不要使用默认值
- 启用 HTTPS（使用 Nginx 反向代理 + Let's Encrypt）
- 限制数据库端口仅内网访问，不要暴露到公网

### 性能优化

- 根据服务器 CPU 核数调整 gunicorn workers 数量（推荐 `2 * CPU + 1`）
- 配置 Redis 持久化策略
- 为 PostgreSQL 配置合适的 `shared_buffers` 和 `work_mem`
- 启用 MongoDB 副本集以提高可用性

### 推荐架构

```
Nginx (反向代理 + SSL)
  -> API 服务 (gunicorn + uvicorn workers)
  -> PostgreSQL (主从复制)
  -> MongoDB (副本集)
  -> Redis (哨兵模式)
```

## 3. 环境变量配置

| 变量名 | 说明 | 默认值 | 是否必须 |
|--------|------|--------|----------|
| `DATABASE_URL` | PostgreSQL 连接字符串 | `postgresql://petvoyage:password@postgres:5432/petvoyage` | 是 |
| `MONGODB_URL` | MongoDB 连接字符串 | `mongodb://mongodb:27017/petvoyage` | 是 |
| `REDIS_URL` | Redis 连接字符串 | `redis://redis:6379/0` | 是 |
| `SECRET_KEY` | JWT 签名密钥 | `change-me-in-production` | 是 |
| `ENV` | 运行环境 | `production` | 否 |

### 使用 .env 文件

在项目根目录创建 `.env` 文件：

```env
DATABASE_URL=postgresql://petvoyage:your-strong-password@postgres:5432/petvoyage
MONGODB_URL=mongodb://mongodb:27017/petvoyage
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-very-long-random-secret-key
ENV=production
```

## 4. 常见问题

### Q: API 启动失败，提示数据库连接错误

确保数据库服务已就绪。docker-compose 已配置健康检查，API 会等待数据库就绪后再启动。如果仍然失败：

```bash
# 检查数据库状态
docker compose ps
docker compose logs postgres
```

### Q: 端口冲突

如果本地 5432/27017/6379/8000 端口被占用，修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "5433:5432"  # 将宿主机端口改为 5433
```

### Q: 如何查看 API 健康状态

```bash
curl http://localhost:8000/health
```

### Q: 如何进入容器调试

```bash
docker compose exec api bash
docker compose exec postgres psql -U petvoyage
```

### Q: 如何重建镜像

代码更新后需要重建：

```bash
docker compose build api
docker compose up -d api
```
