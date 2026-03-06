# PetVoyageAI Web 前端完整实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 开发一个真正可用、美观、功能完整的 Web 应用，让用户可以注册、管理宠物、生成AI照片、查看画廊和地图。

**Architecture:** 使用 React 18 + TypeScript + Vite 构建 SPA 应用。采用 shadcn/ui 组件库和 Tailwind CSS 实现现代化 UI。使用 Zustand 进行轻量级状态管理，TanStack Query 处理服务器状态。7个核心页面通过 React Router 连接，完整对接现有的 FastAPI 后端。

**Tech Stack:** React 18, TypeScript, Vite 5, React Router 6, Zustand, TanStack Query, shadcn/ui, Tailwind CSS, Leaflet.js, Framer Motion

---

## Phase 1: 基础搭建（Foundation Setup）

### Task 1.1: 安装依赖和配置 TypeScript

**Files:**
- Modify: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/tsconfig.node.json`

**Step 1: 安装核心依赖**

```bash
cd frontend
npm install --save \
  react-router-dom@6 \
  zustand@4 \
  @tanstack/react-query@5 \
  axios@1 \
  zod@3 \
  react-hook-form@7 \
  @hookform/resolvers@3 \
  clsx@2 \
  tailwind-merge@2
```

**Step 2: 安装 TypeScript 和开发依赖**

```bash
npm install --save-dev \
  typescript@5 \
  @types/react@18 \
  @types/react-dom@18 \
  @types/node@20
```

**Step 3: 创建 tsconfig.json**

创建文件 `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**Step 4: 创建 tsconfig.node.json**

创建文件 `frontend/tsconfig.node.json`:

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

**Step 5: 更新 vite.config 支持路径别名**

修改 `frontend/vite.config.js` 为 `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**Step 6: 提交**

```bash
git add package.json tsconfig.json tsconfig.node.json vite.config.ts
git commit -m "chore: setup TypeScript and core dependencies"
```

---

### Task 1.2: 配置 shadcn/ui

**Files:**
- Create: `frontend/components.json`
- Modify: `frontend/tailwind.config.js`
- Create: `frontend/src/lib/utils.ts`

**Step 1: 安装 shadcn/ui CLI**

```bash
npx shadcn-ui@latest init
```

选择以下选项:
- TypeScript: Yes
- Style: Default
- Base color: Slate
- CSS variables: Yes

**Step 2: 创建 utils.ts**

创建 `frontend/src/lib/utils.ts`:

```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Step 3: 安装基础 UI 组件**

```bash
npx shadcn-ui@latest add button card input label select dialog tabs toast form
```

**Step 4: 提交**

```bash
git add components.json tailwind.config.js src/lib src/components/ui
git commit -m "chore: setup shadcn/ui components"
```

---

### Task 1.3: 创建项目结构和类型定义

**Files:**
- Create: `frontend/src/types/auth.ts`
- Create: `frontend/src/types/pet.ts`
- Create: `frontend/src/types/photo.ts`
- Create: `frontend/src/types/location.ts`
- Create: `frontend/src/types/index.ts`

**Step 1: 创建认证类型**

创建 `frontend/src/types/auth.ts`:

```typescript
export interface User {
  id: number
  phone: string
  nickname: string
  subscription_type: 'free' | 'premium' | 'lifetime'
  daily_quota_total: number
  daily_quota_used: number
  created_at: string
}

export interface LoginRequest {
  phone: string
  password: string
}

export interface RegisterRequest {
  phone: string
  password: string
  nickname: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}
```

**Step 2: 创建宠物类型**

创建 `frontend/src/types/pet.ts`:

```typescript
export interface Pet {
  id: number
  user_id: number
  name: string
  type: 'dog' | 'cat' | 'other'
  description: string
  photo_url?: string
  ai_description?: string
  created_at: string
  updated_at: string
}

export interface PetCreateRequest {
  name: string
  type: 'dog' | 'cat' | 'other'
  description: string
  photo?: File
}
```

**Step 3: 创建照片类型**

创建 `frontend/src/types/photo.ts`:

```typescript
export interface Photo {
  id: number
  user_id: number
  pet_id: number
  location_id: number
  image_url: string
  prompt: string
  style: 'realistic' | 'pixel' | 'anime'
  season?: string
  time_of_day?: string
  created_at: string
}

export interface GeneratePhotoRequest {
  pet_id: number
  location_id: number
  style: 'realistic' | 'pixel' | 'anime'
  season?: string
  time_of_day?: string
}

export interface GenerationTask {
  task_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  result_urls?: string[]
  error?: string
}
```

**Step 4: 创建景点类型**

创建 `frontend/src/types/location.ts`:

```typescript
export interface Location {
  id: number
  name: string
  name_en: string
  continent: string
  country: string
  city: string
  category: string
  icon: string
  description?: string
  unlock_count: number
}
```

**Step 5: 创建索引文件**

创建 `frontend/src/types/index.ts`:

```typescript
export * from './auth'
export * from './pet'
export * from './photo'
export * from './location'
```

**Step 6: 提交**

```bash
git add src/types
git commit -m "feat: add TypeScript type definitions"
```

---

### Task 1.4: 封装 API 服务层

**Files:**
- Create: `frontend/src/lib/axios.ts`
- Create: `frontend/src/services/authService.ts`
- Create: `frontend/src/services/petService.ts`
- Create: `frontend/src/services/photoService.ts`
- Create: `frontend/src/services/locationService.ts`

**Step 1: 配置 Axios 实例**

创建 `frontend/src/lib/axios.ts`:

```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
})

// 请求拦截器 - 添加 token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/auth'
    }
    return Promise.reject(error)
  }
)

export default api
```

**Step 2: 创建认证服务**

创建 `frontend/src/services/authService.ts`:

```typescript
import api from '@/lib/axios'
import type { LoginRequest, RegisterRequest, AuthResponse, User } from '@/types'

export const authService = {
  login: (data: LoginRequest) =>
    api.post<AuthResponse>('/auth/login', data),

  register: (data: RegisterRequest) =>
    api.post<AuthResponse>('/auth/register', data),

  getCurrentUser: () =>
    api.get<User>('/auth/me'),
}
```

**Step 3: 创建宠物服务**

创建 `frontend/src/services/petService.ts`:

```typescript
import api from '@/lib/axios'
import type { Pet } from '@/types'

export const petService = {
  getAll: () =>
    api.get<Pet[]>('/pets'),

  getById: (id: number) =>
    api.get<Pet>(`/pets/${id}`),

  create: (data: FormData) =>
    api.post<Pet>('/pets', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  update: (id: number, data: FormData) =>
    api.patch<Pet>(`/pets/${id}`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  delete: (id: number) =>
    api.delete(`/pets/${id}`),
}
```

**Step 4: 创建照片服务**

创建 `frontend/src/services/photoService.ts`:

```typescript
import api from '@/lib/axios'
import type { Photo, GeneratePhotoRequest, GenerationTask } from '@/types'

export const photoService = {
  getAll: (params?: { pet_id?: number; location_id?: number }) =>
    api.get<Photo[]>('/photos', { params }),

  generate: (data: GeneratePhotoRequest) =>
    api.post<GenerationTask>('/photos/generate', data),

  getGenerationStatus: (taskId: string) =>
    api.get<GenerationTask>(`/photos/generate/${taskId}`),

  save: (data: { task_id: string; selected_url: string }) =>
    api.post<Photo>('/photos', data),

  delete: (id: number) =>
    api.delete(`/photos/${id}`),
}
```

**Step 5: 创建景点服务**

创建 `frontend/src/services/locationService.ts`:

```typescript
import api from '@/lib/axios'
import type { Location } from '@/types'

export const locationService = {
  getAll: () =>
    api.get<Location[]>('/locations'),

  getById: (id: number) =>
    api.get<Location>(`/locations/${id}`),
}
```

**Step 6: 提交**

```bash
git add src/lib/axios.ts src/services
git commit -m "feat: add API service layer"
```

---

### Task 1.5: 设置状态管理（Zustand）

**Files:**
- Create: `frontend/src/stores/authStore.ts`
- Create: `frontend/src/stores/petStore.ts`
- Create: `frontend/src/stores/photoStore.ts`

**Step 1: 创建认证 Store**

创建 `frontend/src/stores/authStore.ts`:

```typescript
import { create } from 'zustand'
import { authService } from '@/services/authService'
import type { User, LoginRequest, RegisterRequest } from '@/types'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  login: (data: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
  setUser: (user: User) => void
  clearError: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  isLoading: false,
  error: null,

  login: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.login(data)
      localStorage.setItem('token', response.access_token)
      set({
        user: response.user,
        token: response.access_token,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || '登录失败',
        isLoading: false,
      })
      throw error
    }
  },

  register: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.register(data)
      localStorage.setItem('token', response.access_token)
      set({
        user: response.user,
        token: response.access_token,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || '注册失败',
        isLoading: false,
      })
      throw error
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null,
    })
  },

  refreshUser: async () => {
    try {
      const user = await authService.getCurrentUser()
      set({ user })
    } catch (error) {
      console.error('Failed to refresh user:', error)
    }
  },

  setUser: (user) => set({ user }),
  clearError: () => set({ error: null }),
}))
```

**Step 2: 创建宠物 Store**

创建 `frontend/src/stores/petStore.ts`:

```typescript
import { create } from 'zustand'
import { petService } from '@/services/petService'
import type { Pet } from '@/types'

interface PetState {
  pets: Pet[]
  selectedPet: Pet | null
  isLoading: boolean

  fetchPets: () => Promise<void>
  selectPet: (pet: Pet | null) => void
  createPet: (data: FormData) => Promise<Pet>
  updatePet: (id: number, data: FormData) => Promise<void>
  deletePet: (id: number) => Promise<void>
}

export const usePetStore = create<PetState>((set, get) => ({
  pets: [],
  selectedPet: null,
  isLoading: false,

  fetchPets: async () => {
    set({ isLoading: true })
    try {
      const pets = await petService.getAll()
      set({ pets, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  selectPet: (pet) => set({ selectedPet: pet }),

  createPet: async (data) => {
    const newPet = await petService.create(data)
    set({ pets: [...get().pets, newPet] })
    return newPet
  },

  updatePet: async (id, data) => {
    await petService.update(id, data)
    await get().fetchPets()
  },

  deletePet: async (id) => {
    await petService.delete(id)
    set({ pets: get().pets.filter((p) => p.id !== id) })
  },
}))
```

**Step 3: 创建照片 Store**

创建 `frontend/src/stores/photoStore.ts`:

```typescript
import { create } from 'zustand'
import { photoService } from '@/services/photoService'
import type { Photo } from '@/types'

interface PhotoState {
  photos: Photo[]
  isLoading: boolean

  fetchPhotos: (params?: { pet_id?: number; location_id?: number }) => Promise<void>
  deletePhoto: (id: number) => Promise<void>
}

export const usePhotoStore = create<PhotoState>((set, get) => ({
  photos: [],
  isLoading: false,

  fetchPhotos: async (params) => {
    set({ isLoading: true })
    try {
      const photos = await photoService.getAll(params)
      set({ photos, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  deletePhoto: async (id) => {
    await photoService.delete(id)
    set({ photos: get().photos.filter((p) => p.id !== id) })
  },
}))
```

**Step 4: 提交**

```bash
git add src/stores
git commit -m "feat: add Zustand stores for state management"
```

---

### Task 1.6: 配置路由结构

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/main.tsx`
- Create: `frontend/src/components/layout/ProtectedRoute.tsx`

**Step 1: 重命名文件为 TypeScript**

```bash
mv src/App.jsx src/App.tsx
mv src/main.jsx src/main.tsx
mv src/pages/Home.jsx src/pages/HomePage.tsx
```

**Step 2: 创建受保护路由组件**

创建 `frontend/src/components/layout/ProtectedRoute.tsx`:

```typescript
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />
  }

  return <>{children}</>
}
```

**Step 3: 创建页面占位符**

```bash
mkdir -p src/pages
touch src/pages/AuthPage.tsx
touch src/pages/DashboardPage.tsx
touch src/pages/PetsPage.tsx
touch src/pages/GeneratePage.tsx
touch src/pages/GalleryPage.tsx
touch src/pages/MapPage.tsx
touch src/pages/ProfilePage.tsx
```

**Step 4: 更新 App.tsx 配置路由**

修改 `frontend/src/App.tsx`:

```typescript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ProtectedRoute } from '@/components/layout/ProtectedRoute'
import AuthPage from '@/pages/AuthPage'
import DashboardPage from '@/pages/DashboardPage'
import PetsPage from '@/pages/PetsPage'
import GeneratePage from '@/pages/GeneratePage'
import GalleryPage from '@/pages/GalleryPage'
import MapPage from '@/pages/MapPage'
import ProfilePage from '@/pages/ProfilePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/auth" element={<AuthPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/pets"
          element={
            <ProtectedRoute>
              <PetsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/generate"
          element={
            <ProtectedRoute>
              <GeneratePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/gallery"
          element={
            <ProtectedRoute>
              <GalleryPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/map"
          element={
            <ProtectedRoute>
              <MapPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

**Step 5: 更新 main.tsx**

修改 `frontend/src/main.tsx`:

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**Step 6: 提交**

```bash
git add src/App.tsx src/main.tsx src/components/layout src/pages
git commit -m "feat: setup React Router with protected routes"
```

---

## Phase 2: Agent Teams 并行开发

### Task 2.1: 创建 Agent Team - auth-frontend

**目标**: 开发登录注册页面

**交付物**:
- AuthPage.tsx（完整的登录/注册页面）
- 表单验证
- 错误提示
- 与 authStore 集成

**Agent 任务文档**: 见 `docs/agents/auth-frontend-task.md`

---

### Task 2.2: 创建 Agent Team - pets-frontend

**目标**: 开发宠物管理页面

**交付物**:
- PetsPage.tsx
- PetCard 组件
- PetForm 组件（创建/编辑）
- 文件上传组件

**Agent 任务文档**: 见 `docs/agents/pets-frontend-task.md`

---

### Task 2.3: 创建 Agent Team - generate-frontend

**目标**: 开发 AI 照片生成页面

**交付物**:
- GeneratePage.tsx
- 三步向导组件
- 生成进度组件
- 结果展示组件

**Agent 任务文档**: 见 `docs/agents/generate-frontend-task.md`

---

### Task 2.4: 创建 Agent Team - gallery-frontend

**目标**: 开发照片画廊页面

**交付物**:
- GalleryPage.tsx
- 瀑布流布局
- 照片灯箱组件
- 筛选工具栏

**Agent 任务文档**: 见 `docs/agents/gallery-frontend-task.md`

---

### Task 2.5: 创建 Agent Team - map-frontend

**目标**: 开发世界地图页面

**交付物**:
- MapPage.tsx
- Leaflet 地图集成
- 景点标记组件
- 侧边栏抽屉

**Agent 任务文档**: 见 `docs/agents/map-frontend-task.md`

---

### Task 2.6: 创建 Agent Team - dashboard-profile

**目标**: 开发 Dashboard 和个人中心页面

**交付物**:
- DashboardPage.tsx
- ProfilePage.tsx
- 统计卡片组件
- Header/Sidebar 布局

**Agent 任务文档**: 见 `docs/agents/dashboard-profile-task.md`

---

## Phase 3: 集成测试

### Task 3.1: 页面联调和路由测试

**Step 1: 测试所有路由跳转**

- 登录后跳转到 dashboard
- 点击导航切换页面
- 未登录访问受保护页面重定向到登录

**Step 2: 测试 API 对接**

- 注册新用户
- 登录
- 创建宠物
- 生成照片
- 查看画廊和地图

**Step 3: 修复发现的 Bug**

**Step 4: 提交**

```bash
git add .
git commit -m "fix: integration bugs and route navigation"
```

---

### Task 3.2: 样式统一和响应式适配

**Step 1: 检查各页面样式一致性**

- 颜色、字体、间距统一
- 组件风格统一

**Step 2: 测试响应式布局**

- 手机端（375px, 414px）
- 平板端（768px）
- 桌面端（1024px, 1440px）

**Step 3: 调整样式**

**Step 4: 提交**

```bash
git add .
git commit -m "style: unify styles and responsive design"
```

---

## Phase 4: 优化打磨

### Task 4.1: 性能优化

**Step 1: 代码分割（Lazy Loading）**

修改 `src/App.tsx` 使用懒加载:

```typescript
import { lazy, Suspense } from 'react'

const AuthPage = lazy(() => import('@/pages/AuthPage'))
const DashboardPage = lazy(() => import('@/pages/DashboardPage'))
// ... 其他页面

// 在 Routes 中包裹 Suspense
<Suspense fallback={<div>Loading...</div>}>
  <Routes>
    // ... routes
  </Routes>
</Suspense>
```

**Step 2: 图片懒加载**

安装并配置 react-lazy-load-image-component

**Step 3: 提交**

```bash
git add .
git commit -m "perf: add code splitting and lazy loading"
```

---

### Task 4.2: 添加动画效果

**Step 1: 安装 Framer Motion**

```bash
npm install framer-motion
```

**Step 2: 添加页面切换动画**

**Step 3: 添加卡片悬浮动画**

**Step 4: 提交**

```bash
git add .
git commit -m "feat: add smooth animations with Framer Motion"
```

---

### Task 4.3: 最终验收和文档

**Step 1: 完整功能测试**

- [ ] 用户注册
- [ ] 用户登录
- [ ] 创建宠物
- [ ] 生成照片
- [ ] 查看画廊
- [ ] 查看地图
- [ ] 修改个人信息
- [ ] 退出登录

**Step 2: 浏览器兼容性测试**

- Chrome
- Firefox
- Safari
- Edge

**Step 3: 创建前端使用文档**

创建 `frontend/USER_GUIDE.md`

**Step 4: 最终提交**

```bash
git add .
git commit -m "docs: add user guide and final polish"
```

---

## 验收标准

### 功能完整性
- ✅ 7 个页面全部实现
- ✅ 所有 API 对接正确
- ✅ 用户流程完整

### 代码质量
- ✅ TypeScript 类型覆盖 100%
- ✅ 无 ESLint 错误
- ✅ 组件可复用

### 用户体验
- ✅ 响应式设计（手机/平板/桌面）
- ✅ 加载速度快
- ✅ 动画流畅
- ✅ 错误提示友好

---

## 下一步

Phase 1 (基础搭建) 已完成后，将启动 Agent Teams 并行开发 Phase 2。

每个 Agent 的详细任务将在 `docs/agents/` 目录中创建。
