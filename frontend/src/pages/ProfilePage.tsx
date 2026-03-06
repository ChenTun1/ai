import { useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'

export default function ProfilePage() {
  const { user, refreshUser, logout } = useAuthStore()
  const navigate = useNavigate()

  useEffect(() => {
    refreshUser()
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/auth')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center">
          <Link to="/dashboard" className="text-2xl font-bold text-primary">PetVoyage</Link>
          <nav className="flex items-center gap-6">
            <Link to="/dashboard" className="text-gray-600 hover:text-primary">首页</Link>
            <Link to="/pets" className="text-gray-600 hover:text-primary">宠物</Link>
            <Link to="/generate" className="text-gray-600 hover:text-primary">生成</Link>
            <Link to="/gallery" className="text-gray-600 hover:text-primary">画廊</Link>
            <Link to="/map" className="text-gray-600 hover:text-primary">地图</Link>
            <Link to="/profile" className="text-primary font-medium">我的</Link>
          </nav>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-8">个人中心</h2>

        <div className="bg-white rounded-xl p-8 shadow-sm mb-6">
          <h3 className="text-xl font-bold mb-6">基本信息</h3>
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center text-3xl">
                👤
              </div>
              <div>
                <p className="text-lg font-bold">{user?.nickname || '用户'}</p>
                <p className="text-sm text-gray-600">{user?.phone}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-8 shadow-sm mb-6">
          <h3 className="text-xl font-bold mb-6">订阅信息</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">订阅类型</p>
              <p className="text-lg font-bold">{user?.subscription_type === 'free' ? '免费版' : user?.subscription_type === 'premium' ? '高级版' : '终身版'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">每日配额</p>
              <p className="text-lg font-bold">{user?.daily_quota_total - (user?.daily_quota_used || 0)} / {user?.daily_quota_total}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-8 shadow-sm">
          <h3 className="text-xl font-bold mb-6">账户操作</h3>
          <button onClick={handleLogout} className="w-full px-4 py-3 border-2 border-red-300 text-red-600 rounded-lg hover:bg-red-50 font-medium">
            退出登录
          </button>
        </div>
      </main>
    </div>
  )
}
