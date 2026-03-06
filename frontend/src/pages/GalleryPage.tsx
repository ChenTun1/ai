import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { usePhotoStore } from '@/stores/photoStore'
import { useAuthStore } from '@/stores/authStore'

export default function GalleryPage() {
  const { photos, fetchPhotos, deletePhoto } = usePhotoStore()
  const { logout } = useAuthStore()

  useEffect(() => {
    fetchPhotos()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center">
          <Link to="/dashboard" className="text-2xl font-bold text-primary">PetVoyage</Link>
          <nav className="flex items-center gap-6">
            <Link to="/dashboard" className="text-gray-600 hover:text-primary">首页</Link>
            <Link to="/pets" className="text-gray-600 hover:text-primary">宠物</Link>
            <Link to="/generate" className="text-gray-600 hover:text-primary">生成</Link>
            <Link to="/gallery" className="text-primary font-medium">画廊</Link>
            <Link to="/map" className="text-gray-600 hover:text-primary">地图</Link>
            <button onClick={logout} className="text-gray-600 hover:text-red-500">退出</button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-8">照片画廊</h2>

        {photos.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {photos.map((photo) => (
              <div key={photo.id} className="group relative aspect-square rounded-lg overflow-hidden bg-gray-100">
                <img src={photo.image_url} alt="Generated" className="w-full h-full object-cover" />
                <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-2">
                  <button onClick={() => window.open(photo.image_url)} className="px-3 py-1 bg-white rounded text-sm">查看</button>
                  <button onClick={() => deletePhoto(photo.id)} className="px-3 py-1 bg-red-500 text-white rounded text-sm">删除</button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-8xl mb-4">📷</div>
            <h3 className="text-2xl font-bold mb-2">还没有照片</h3>
            <Link to="/generate" className="inline-block bg-primary text-white px-8 py-3 rounded-lg">立即生成</Link>
          </div>
        )}
      </main>
    </div>
  )
}
