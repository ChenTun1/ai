import api from '@/lib/axios'
import type { Photo, GeneratePhotoRequest, GenerationTask } from '@/types'

export const photoService = {
  getAll: (params?: { pet_id?: number; location_id?: number }) =>
    api.get<Photo[]>('/photos', { params }),

  generate: (data: GeneratePhotoRequest) =>
    api.post<GenerationTask>('/photos/generate', data),

  getGenerationStatus: (taskId: string) =>
    api.get<GenerationTask>(`/photos/generate/${taskId}`),

  save: (data: { task_id: string; selected_url: string }) =>
    api.post<Photo>('/photos', data),

  delete: (id: number) =>
    api.delete(`/photos/${id}`),
}
