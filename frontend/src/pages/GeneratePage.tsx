import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { usePetStore } from '@/stores/petStore'
import { photoService } from '@/services/photoService'
import { locationService } from '@/services/locationService'
import { useAuthStore } from '@/stores/authStore'

export default function GeneratePage() {
  const navigate = useNavigate()
  const { pets, fetchPets } = usePetStore()
  const { logout } = useAuthStore()
  const [locations, setLocations] = useState<any[]>([])
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    pet_id: 0,
    location_id: 0,
    style: 'realistic' as 'realistic' | 'pixel' | 'anime',
    season: '',
    time_of_day: ''
  })
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetchPets()
    locationService.getAll().then(setLocations)
  }, [])

  const handleGenerate = async () => {
    if (!formData.pet_id || !formData.location_id) {
      alert('请选择宠物和景点')
      return
    }
    setGenerating(true)
    try {
      const task = await photoService.generate(formData)
      alert('生成成功！请前往画廊查看')
      navigate('/gallery')
    } catch (error) {
      alert('生成失败')
    }
    setGenerating(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center">
          <Link to="/dashboard" className="text-2xl font-bold text-primary">PetVoyage</Link>
          <nav className="flex items-center gap-6">
            <Link to="/dashboard" className="text-gray-600 hover:text-primary">首页</Link>
            <Link to="/pets" className="text-gray-600 hover:text-primary">宠物</Link>
            <Link to="/generate" className="text-primary font-medium">生成</Link>
            <Link to="/gallery" className="text-gray-600 hover:text-primary">画廊</Link>
            <Link to="/map" className="text-gray-600 hover:text-primary">地图</Link>
            <button onClick={logout} className="text-gray-600 hover:text-red-500">退出</button>
          </nav>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-8">AI 照片生成</h2>

        <div className="bg-white rounded-xl p-8 shadow-sm">
          <div className="mb-8">
            <div className="flex gap-4 mb-8">
              {[1,2,3].map(s => (
                <div key={s} className={`flex-1 text-center pb-2 border-b-2 ${step >= s ? 'border-primary text-primary font-medium' : 'border-gray-200 text-gray-400'}`}>
                  步骤 {s}
                </div>
              ))}
            </div>

            {step === 1 && (
              <div>
                <h3 className="text-xl font-bold mb-4">选择宠物</h3>
                <div className="grid md:grid-cols-4 gap-4">
                  {pets.map(pet => (
                    <div key={pet.id} onClick={() => {setFormData({...formData, pet_id: pet.id}); setStep(2)}} className={`p-4 border-2 rounded-lg cursor-pointer ${formData.pet_id === pet.id ? 'border-primary bg-primary/5' : 'border-gray-200 hover:border-primary/50'}`}>
                      <div className="text-4xl text-center mb-2">{pet.type === 'dog' ? '🐕' : '🐱'}</div>
                      <p className="text-center font-medium">{pet.name}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {step === 2 && (
              <div>
                <h3 className="text-xl font-bold mb-4">选择景点</h3>
                <div className="grid md:grid-cols-4 gap-4 max-h-96 overflow-y-auto">
                  {locations.map(loc => (
                    <div key={loc.id} onClick={() => {setFormData({...formData, location_id: loc.id}); setStep(3)}} className={`p-4 border-2 rounded-lg cursor-pointer ${formData.location_id === loc.id ? 'border-primary bg-primary/5' : 'border-gray-200 hover:border-primary/50'}`}>
                      <p className="font-medium">{loc.name}</p>
                      <p className="text-xs text-gray-500">{loc.country}</p>
                    </div>
                  ))}
                </div>
                <button onClick={() => setStep(1)} className="mt-4 px-4 py-2 border rounded-lg">上一步</button>
              </div>
            )}

            {step === 3 && (
              <div>
                <h3 className="text-xl font-bold mb-4">选择风格</h3>
                <div className="grid md:grid-cols-3 gap-4 mb-6">
                  {[{v:'realistic',n:'真实风格'},{v:'pixel',n:'像素风格'},{v:'anime',n:'动漫风格'}].map(s => (
                    <div key={s.v} onClick={() => setFormData({...formData, style: s.v as any})} className={`p-6 border-2 rounded-lg cursor-pointer ${formData.style === s.v ? 'border-primary bg-primary/5' : 'border-gray-200'}`}>
                      <p className="text-center font-medium">{s.n}</p>
                    </div>
                  ))}
                </div>
                <div className="flex gap-4">
                  <button onClick={() => setStep(2)} className="px-4 py-2 border rounded-lg">上一步</button>
                  <button onClick={handleGenerate} disabled={generating} className="flex-1 px-4 py-2 bg-primary text-white rounded-lg disabled:opacity-50">
                    {generating ? '生成中...' : '开始生成'}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
