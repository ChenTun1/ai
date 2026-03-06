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
