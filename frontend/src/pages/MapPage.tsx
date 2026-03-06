import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { locationService } from '@/services/locationService'
import { usePhotoStore } from '@/stores/photoStore'
import { useAuthStore } from '@/stores/authStore'

export default function MapPage() {
  const [locations, setLocations] = useState<any[]>([])
  const { photos, fetchPhotos } = usePhotoStore()
  const { logout } = useAuthStore()
  const [unlockedIds, setUnlockedIds] = useState<Set<number>>(new Set())

  useEffect(() => {
    locationService.getAll().then(setLocations)
    fetchPhotos()
  }, [])

  useEffect(() => {
    setUnlockedIds(new Set(photos.map(p => p.location_id)))
  }, [photos])

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
            <Link to="/map" className="text-primary font-medium">地图</Link>
            <button onClick={logout} className="text-gray-600 hover:text-red-500">退出</button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">世界地图</h2>
          <p className="text-gray-600">解锁进度: {unlockedIds.size}/{locations.length} 个景点</p>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm">
          {['Asia', 'Europe', 'Americas', 'Other'].map(continent => {
            const locs = locations.filter(l => l.continent === continent || (continent === 'Other' && !['Asia','Europe','Americas'].includes(l.continent)))
            if (locs.length === 0) return null
            return (
              <div key={continent} className="mb-8">
                <h3 className="text-xl font-bold mb-4">{continent === 'Asia' ? '亚洲' : continent === 'Europe' ? '欧洲' : continent === 'Americas' ? '美洲' : '其他'}</h3>
                <div className="grid md:grid-cols-4 gap-4">
                  {locs.map(loc => (
                    <div key={loc.id} className={`p-4 border-2 rounded-lg ${unlockedIds.has(loc.id) ? 'border-green-500 bg-green-50' : 'border-gray-200 bg-gray-50'}`}>
                      <p className="font-medium">{loc.name}</p>
                      <p className="text-sm text-gray-600">{loc.country}</p>
                      {unlockedIds.has(loc.id) ? (
                        <p className="text-xs text-green-600 mt-2">✓ 已解锁</p>
                      ) : (
                        <p className="text-xs text-gray-400 mt-2">未解锁</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      </main>
    </div>
  )
}
