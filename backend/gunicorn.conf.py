"""Gunicorn 生产环境配置"""

# 绑定地址
bind = "0.0.0.0:8000"

# Worker 配置
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000

# 超时配置
timeout = 60
keepalive = 5
graceful_timeout = 30

# 日志配置
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 进程命名
proc_name = "petvoyage-api"

# 预加载应用（减少内存占用）
preload_app = True

# 最大请求数（防止内存泄漏）
max_requests = 1000
max_requests_jitter = 50
