import { create } from 'zustand'
import { photoService } from '@/services/photoService'
import type { Photo } from '@/types'

interface PhotoState {
  photos: Photo[]
  isLoading: boolean

  fetchPhotos: (params?: { pet_id?: number; location_id?: number }) => Promise<void>
  deletePhoto: (id: number) => Promise<void>
}

export const usePhotoStore = create<PhotoState>((set, get) => ({
  photos: [],
  isLoading: false,

  fetchPhotos: async (params) => {
    set({ isLoading: true })
    try {
      const photos = await photoService.getAll(params)
      set({ photos, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  deletePhoto: async (id) => {
    await photoService.delete(id)
    set({ photos: get().photos.filter((p) => p.id !== id) })
  },
}))
