# PetVoyageAI Web 前端完整重构设计文档

**设计日期**: 2026-03-07
**设计者**: Main Agent
**审批者**: 用户
**状态**: ✅ 已批准，执行中

---

## 1. 项目背景

### 1.1 现状问题
- ✅ 后端完整（19个API端点，完整的认证、AI生成、文件上传）
- ❌ 前端仅有框架（4个文件，只有一个简陋的首页）
- ❌ 无法让用户真正使用

### 1.2 设计目标
**开发一个真正可用、美观、功能完整的 Web 应用**

---

## 2. 技术栈

- React 18 + TypeScript
- Vite 5
- React Router 6
- Zustand (状态管理)
- Tailwind CSS + shadcn/ui
- TanStack Query
- Leaflet (地图)
- Framer Motion (动画)

---

## 3. 页面设计

### 7个核心页面
1. AuthPage - 登录/注册
2. DashboardPage - 首页仪表盘
3. PetsPage - 宠物管理
4. GeneratePage - AI照片生成
5. GalleryPage - 照片画廊
6. MapPage - 世界地图
7. ProfilePage - 个人中心

---

## 4. 开发计划

### Phase 1: 基础搭建（30分钟）
- 安装依赖
- 配置 TypeScript
- 设置 shadcn/ui
- 创建路由结构
- 封装 API 服务

### Phase 2: Agent Teams 并行开发（2小时）
- 7个Agent同时开发各自页面

### Phase 3: 集成测试（30分钟）
- 联调和测试

### Phase 4: 优化打磨（30分钟）
- 性能优化和适配

---

**总计：约3-4小时完成**
