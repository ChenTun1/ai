#!/bin/bash
# PetVoyageAI 一键启动脚本

echo "=========================================="
echo "🚀 PetVoyageAI 启动中..."
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 检查是否在项目根目录
if [ ! -d "backend" ]; then
    echo -e "${RED}错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 步骤 1: 检查 Python 环境
echo -e "\n${BLUE}[1/5]${NC} 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${RED}✗ Python 3 未安装${NC}"
    exit 1
fi

# 步骤 2: 检查虚拟环境
echo -e "\n${BLUE}[2/5]${NC} 检查虚拟环境..."
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}虚拟环境不存在，正在创建...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    echo -e "${GREEN}✓ 虚拟环境创建完成${NC}"
else
    echo -e "${GREEN}✓ 虚拟环境已存在${NC}"
fi

# 步骤 3: 检查数据库
echo -e "\n${BLUE}[3/5]${NC} 检查数据库..."
if [ ! -f "backend/data/petvoyage.db" ]; then
    echo -e "${YELLOW}数据库不存在，正在初始化...${NC}"
    cd backend
    source venv/bin/activate
    python scripts/init_db.py
    cd ..
    echo -e "${GREEN}✓ 数据库初始化完成${NC}"
else
    echo -e "${GREEN}✓ 数据库已存在${NC}"
fi

# 步骤 4: 检查配置
echo -e "\n${BLUE}[4/5]${NC} 检查配置..."
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠ .env 文件不存在${NC}"
    echo -e "${YELLOW}提示: 请创建 backend/.env 并配置 SILICONFLOW_API_KEY${NC}"
fi

# 步骤 5: 启动服务
echo -e "\n${BLUE}[5/5]${NC} 启动后端服务..."
echo -e "${GREEN}✓ 准备就绪${NC}"
echo ""
echo "=========================================="
echo "📚 服务信息"
echo "=========================================="
echo -e "后端 API:  ${GREEN}http://localhost:8000${NC}"
echo -e "API 文档:  ${GREEN}http://localhost:8000/docs${NC}"
echo -e "健康检查:  ${GREEN}http://localhost:8000/health${NC}"
echo ""
echo "=========================================="
echo "🎯 下一步"
echo "=========================================="
echo "1. 配置 API Key: 编辑 backend/.env"
echo "2. 启动前端: cd frontend && npm install && npm run dev"
echo "3. Docker部署: docker-compose up -d"
echo ""
echo "正在启动后端服务..."
echo "按 Ctrl+C 停止服务"
echo "=========================================="
echo ""

cd backend
source venv/bin/activate
python -m app.main
