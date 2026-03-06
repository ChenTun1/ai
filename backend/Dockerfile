# ============================================
# 阶段1: 构建阶段 - 安装依赖
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /build

# 安装编译所需的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖到用户目录
RUN pip install --no-cache-dir --user -r requirements.txt \
    && pip install --no-cache-dir --user gunicorn

# ============================================
# 阶段2: 运行阶段 - 最小化镜像
# ============================================
FROM python:3.11-slim

WORKDIR /app

# 安装运行时系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制 Python 包
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 -m appuser

# 复制应用代码
COPY . .

# 复制 gunicorn 配置
COPY gunicorn.conf.py .

# 设置文件所有权
RUN chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 使用 gunicorn 启动（4个 worker）
CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
