import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { usePetStore } from '@/stores/petStore'
import { useAuthStore } from '@/stores/authStore'

export default function PetsPage() {
  const { pets, fetchPets, createPet, deletePet, isLoading } = usePetStore()
  const { logout } = useAuthStore()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    type: 'dog' as 'dog' | 'cat' | 'other',
    description: '',
    photo: null as File | null,
  })

  useEffect(() => {
    fetchPets()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const data = new FormData()
    data.append('name', formData.name)
    data.append('type', formData.type)
    data.append('description', formData.description)
    if (formData.photo) {
      data.append('photo', formData.photo)
    }

    try {
      await createPet(data)
      setShowForm(false)
      setFormData({ name: '', type: 'dog', description: '', photo: null })
    } catch (error) {
      alert('创建失败')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center">
          <Link to="/dashboard" className="text-2xl font-bold text-primary">PetVoyage</Link>
          <nav className="flex items-center gap-6">
            <Link to="/dashboard" className="text-gray-600 hover:text-primary">首页</Link>
            <Link to="/pets" className="text-primary font-medium">宠物</Link>
            <Link to="/generate" className="text-gray-600 hover:text-primary">生成</Link>
            <Link to="/gallery" className="text-gray-600 hover:text-primary">画廊</Link>
            <Link to="/map" className="text-gray-600 hover:text-primary">地图</Link>
            <button onClick={logout} className="text-gray-600 hover:text-red-500">退出</button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">我的宠物</h2>
          <button onClick={() => setShowForm(true)} className="bg-primary text-white px-6 py-2 rounded-lg">+ 添加宠物</button>
        </div>

        {showForm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl p-8 max-w-md w-full">
              <h3 className="text-2xl font-bold mb-6">添加新宠物</h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">名字</label>
                  <input type="text" required value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} className="w-full px-4 py-2 border rounded-lg" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">类型</label>
                  <select value={formData.type} onChange={(e) => setFormData({ ...formData, type: e.target.value as any })} className="w-full px-4 py-2 border rounded-lg">
                    <option value="dog">狗狗</option>
                    <option value="cat">猫咪</option>
                    <option value="other">其他</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">描述</label>
                  <textarea required value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} className="w-full px-4 py-2 border rounded-lg" rows={3} />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">照片（可选）</label>
                  <input type="file" accept="image/*" onChange={(e) => setFormData({ ...formData, photo: e.target.files?.[0] || null })} className="w-full px-4 py-2 border rounded-lg" />
                </div>
                <div className="flex gap-3">
                  <button type="button" onClick={() => setShowForm(false)} className="flex-1 px-4 py-2 border rounded-lg">取消</button>
                  <button type="submit" disabled={isLoading} className="flex-1 px-4 py-2 bg-primary text-white rounded-lg">{isLoading ? '创建中...' : '创建'}</button>
                </div>
              </form>
            </div>
          </div>
        )}

        {pets.length > 0 ? (
          <div className="grid md:grid-cols-3 gap-6">
            {pets.map((pet) => (
              <div key={pet.id} className="bg-white rounded-xl shadow-sm border">
                <div className="aspect-square bg-gray-100">
                  {pet.photo_url ? <img src={pet.photo_url} alt={pet.name} className="w-full h-full object-cover" /> : <div className="w-full h-full flex items-center justify-center text-6xl">{pet.type === 'dog' ? '🐕' : '🐱'}</div>}
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-bold mb-2">{pet.name}</h3>
                  <p className="text-sm text-gray-600 mb-4">{pet.description}</p>
                  <Link to="/generate" className="block text-center px-4 py-2 bg-primary text-white rounded-lg">生成照片</Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-8xl mb-4">🐾</div>
            <h3 className="text-2xl font-bold mb-2">还没有宠物</h3>
            <button onClick={() => setShowForm(true)} className="bg-primary text-white px-8 py-3 rounded-lg">+ 添加宠物</button>
          </div>
        )}
      </main>
    </div>
  )
}
