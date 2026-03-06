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
