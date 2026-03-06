#!/bin/bash
# PetVoyageAI 项目进度检查脚本

echo "=========================================="
echo "🚀 PetVoyageAI 项目进度检查"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查文件是否存在
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $2"
        return 0
    else
        echo -e "${RED}❌${NC} $2"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅${NC} $2"
        return 0
    else
        echo -e "${RED}❌${NC} $2"
        return 1
    fi
}

echo "【第一阶段：核心后端】"
check_file "backend/app/core/config.py" "配置管理系统"
check_file "backend/app/core/database.py" "数据库连接"
check_file "backend/app/models/user.py" "用户模型"
check_file "backend/app/models/pet.py" "宠物模型"
check_file "backend/app/models/location.py" "景点模型"
check_file "backend/app/models/photo.py" "照片模型"
check_file "backend/app/services/ai_service.py" "AI 图像生成服务"
check_file "backend/app/api/v1/pets.py" "宠物 API"
check_file "backend/app/api/v1/photos.py" "照片 API"
check_file "backend/app/api/v1/locations.py" "景点 API"
check_file "backend/scripts/init_db.py" "数据库初始化脚本"
check_file "backend/scripts/init_locations.py" "景点数据"
echo ""

echo "【第二阶段：扩展功能】"
check_file "backend/app/utils/file_handler.py" "文件上传工具"
check_file "backend/app/core/security.py" "安全和 JWT"
check_file "backend/app/core/deps.py" "依赖注入"
check_file "backend/app/api/v1/auth.py" "认证 API"
check_file "backend/test_api_integration.py" "集成测试"
echo ""

echo "【第三阶段：前端开发】"
check_dir "frontend" "前端目录"
check_file "frontend/package.json" "前端依赖配置"
check_file "frontend/vite.config.js" "Vite 配置"
check_file "frontend/src/main.jsx" "React 入口"
check_file "frontend/src/App.jsx" "主应用组件"
echo ""

echo "【第四阶段：部署配置】"
check_file "backend/Dockerfile" "后端 Docker 配置"
check_file "docker-compose.yml" "Docker Compose 配置"
check_file "backend/gunicorn.conf.py" "Gunicorn 配置"
check_file "DEPLOYMENT.md" "部署文档"
echo ""

echo "=========================================="
echo "📊 统计信息"
echo "=========================================="

# 统计代码行数
if command -v cloc &> /dev/null; then
    echo ""
    echo "代码统计："
    cloc backend/app --quiet
else
    echo "Python 文件数量："
    find backend/app -name "*.py" | wc -l
fi

echo ""
echo "✅ 检查完成！"
echo ""
echo "下一步："
echo "1. 运行 'python backend/test_system.py' 测试系统"
echo "2. 运行 'python backend/scripts/init_db.py' 初始化数据库"
echo "3. 运行 'python -m backend.app.main' 启动后端"
echo "4. 访问 http://localhost:8000/docs 查看 API"
