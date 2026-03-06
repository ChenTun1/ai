import api from '@/lib/axios'
import type { LoginRequest, RegisterRequest, AuthResponse, User } from '@/types'

export const authService = {
  login: (data: LoginRequest) =>
    api.post<AuthResponse>('/auth/login', data),

  register: (data: RegisterRequest) =>
    api.post<AuthResponse>('/auth/register', data),

  getCurrentUser: () =>
    api.get<User>('/auth/me'),
}
