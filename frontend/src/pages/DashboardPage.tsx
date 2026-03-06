import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { usePetStore } from '@/stores/petStore'
import { usePhotoStore } from '@/stores/photoStore'

export default function DashboardPage() {
  const { user, refreshUser, logout } = useAuthStore()
  const { pets, fetchPets } = usePetStore()
  const { photos, fetchPhotos } = usePhotoStore()
  const [stats, setStats] = useState({ pets: 0, photos: 0, locations: 0 })

  useEffect(() => {
    refreshUser()
    fetchPets()
    fetchPhotos()
  }, [])

  useEffect(() => {
    setStats({
      pets: pets.length,
      photos: photos.length,
      locations: new Set(photos.map(p => p.location_id)).size
    })
  }, [pets, photos])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-primary">PetVoyage</h1>
              <span className="text-sm text-gray-500">AI宠物旅行</span>
            </div>
            <nav className="flex items-center gap-6">
              <Link to="/dashboard" className="text-primary font-medium">首页</Link>
              <Link to="/pets" className="text-gray-600 hover:text-primary">宠物</Link>
              <Link to="/generate" className="text-gray-600 hover:text-primary">生成</Link>
              <Link to="/gallery" className="text-gray-600 hover:text-primary">画廊</Link>
              <Link to="/map" className="text-gray-600 hover:text-primary">地图</Link>
              <Link to="/profile" className="text-gray-600 hover:text-primary">我的</Link>
              <button
                onClick={logout}
                className="text-gray-600 hover:text-red-500 text-sm"
              >
                退出
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            欢迎回来, {user?.nickname || '用户'} 👋
          </h2>
          <p className="text-gray-600">
            您的订阅类型: <span className="font-medium text-primary">{user?.subscription_type || 'free'}</span>
            {' | '}今日配额: {user?.daily_quota_total - (user?.daily_quota_used || 0)}/{user?.daily_quota_total}
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">我的宠物</p>
                <p className="text-3xl font-bold text-gray-900">{stats.pets}</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">
                🐾
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">生成照片</p>
                <p className="text-3xl font-bold text-gray-900">{stats.photos}</p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center text-2xl">
                📸
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">解锁地点</p>
                <p className="text-3xl font-bold text-gray-900">{stats.locations}</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-2xl">
                🗺️
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 mb-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">快速操作</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Link
              to="/pets"
              className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary hover:bg-primary/5 transition text-center"
            >
              <div className="text-3xl mb-2">➕</div>
              <p className="font-medium text-gray-900">添加宠物</p>
            </Link>
            <Link
              to="/generate"
              className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary hover:bg-primary/5 transition text-center"
            >
              <div className="text-3xl mb-2">✨</div>
              <p className="font-medium text-gray-900">生成照片</p>
            </Link>
            <Link
              to="/gallery"
              className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary hover:bg-primary/5 transition text-center"
            >
              <div className="text-3xl mb-2">🖼️</div>
              <p className="font-medium text-gray-900">查看画廊</p>
            </Link>
            <Link
              to="/map"
              className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary hover:bg-primary/5 transition text-center"
            >
              <div className="text-3xl mb-2">🌍</div>
              <p className="font-medium text-gray-900">探索地图</p>
            </Link>
          </div>
        </div>

        {/* Recent Photos */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold text-gray-900">最近生成的照片</h3>
            <Link to="/gallery" className="text-primary hover:underline text-sm font-medium">
              查看全部 →
            </Link>
          </div>
          {photos.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {photos.slice(0, 8).map((photo) => (
                <div key={photo.id} className="aspect-square rounded-lg overflow-hidden bg-gray-100">
                  <img
                    src={photo.image_url}
                    alt="Generated photo"
                    className="w-full h-full object-cover hover:scale-105 transition"
                  />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <div className="text-6xl mb-4">📷</div>
              <p>还没有生成照片</p>
              <Link to="/generate" className="text-primary hover:underline mt-2 inline-block">
                立即生成 →
              </Link>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
