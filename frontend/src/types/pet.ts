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
