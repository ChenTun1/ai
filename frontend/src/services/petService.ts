import api from '@/lib/axios'
import type { Pet } from '@/types'

export const petService = {
  getAll: () =>
    api.get<Pet[]>('/pets'),

  getById: (id: number) =>
    api.get<Pet>(`/pets/${id}`),

  create: (data: FormData) =>
    api.post<Pet>('/pets', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  update: (id: number, data: FormData) =>
    api.patch<Pet>(`/pets/${id}`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  delete: (id: number) =>
    api.delete(`/pets/${id}`),
}
