import { create } from 'zustand'
import { authService } from '@/services/authService'
import type { User, LoginRequest, RegisterRequest } from '@/types'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  login: (data: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
  setUser: (user: User) => void
  clearError: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  isLoading: false,
  error: null,

  login: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.login(data)
      localStorage.setItem('token', response.access_token)
      set({
        user: response.user,
        token: response.access_token,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || '登录失败',
        isLoading: false,
      })
      throw error
    }
  },

  register: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const response = await authService.register(data)
      localStorage.setItem('token', response.access_token)
      set({
        user: response.user,
        token: response.access_token,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || '注册失败',
        isLoading: false,
      })
      throw error
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null,
    })
  },

  refreshUser: async () => {
    try {
      const user = await authService.getCurrentUser()
      set({ user })
    } catch (error) {
      console.error('Failed to refresh user:', error)
    }
  },

  setUser: (user) => set({ user }),
  clearError: () => set({ error: null }),
}))
