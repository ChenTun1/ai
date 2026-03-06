import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    phone: '',
    password: '',
    nickname: '',
  })
  const navigate = useNavigate()
  const { login, register, isLoading, error, clearError } = useAuthStore()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    clearError()

    try {
      if (isLogin) {
        await login({ phone: formData.phone, password: formData.password })
      } else {
        await register({
          phone: formData.phone,
          password: formData.password,
          nickname: formData.nickname,
        })
      }
      navigate('/dashboard')
    } catch (err) {
      // Error is handled by store
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* 左侧 - 品牌展示 */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary to-secondary p-12 text-white flex-col justify-center">
        <div className="max-w-md">
          <h1 className="text-5xl font-bold mb-6">PetVoyage AI</h1>
          <p className="text-xl mb-8 opacity-90">
            让您的宠物与世界名胜同框，AI 生成专属旅行照片
          </p>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center">
                ✨
              </div>
              <div>
                <h3 className="font-semibold">AI 智能生成</h3>
                <p className="text-sm opacity-75">专业级照片质量</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center">
                🗺️
              </div>
              <div>
                <h3 className="font-semibold">18+ 世界景点</h3>
                <p className="text-sm opacity-75">解锁全球地标</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center">
                🎨
              </div>
              <div>
                <h3 className="font-semibold">多种风格</h3>
                <p className="text-sm opacity-75">真实/像素/动漫</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 右侧 - 登录表单 */}
      <div className="flex-1 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                {isLogin ? '欢迎回来' : '创建账号'}
              </h2>
              <p className="text-gray-600">
                {isLogin ? '登录继续您的旅程' : '开始您的 AI 宠物旅行'}
              </p>
            </div>

            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  手机号
                </label>
                <input
                  type="tel"
                  required
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition"
                  placeholder="请输入手机号"
                />
              </div>

              {!isLogin && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    昵称
                  </label>
                  <input
                    type="text"
                    required={!isLogin}
                    value={formData.nickname}
                    onChange={(e) => setFormData({ ...formData, nickname: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition"
                    placeholder="请输入昵称"
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  密码
                </label>
                <input
                  type="password"
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition"
                  placeholder="请输入密码"
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? '处理中...' : isLogin ? '登录' : '注册'}
              </button>
            </form>

            <div className="mt-6 text-center">
              <button
                onClick={() => {
                  setIsLogin(!isLogin)
                  clearError()
                }}
                className="text-primary hover:underline text-sm font-medium"
              >
                {isLogin ? '还没有账号？立即注册' : '已有账号？立即登录'}
              </button>
            </div>
          </div>

          <p className="text-center text-sm text-gray-500 mt-6">
            登录即表示您同意我们的服务条款和隐私政策
          </p>
        </div>
      </div>
    </div>
  )
}
