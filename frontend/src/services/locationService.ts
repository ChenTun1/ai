import api from '@/lib/axios'
import type { Location } from '@/types'

export const locationService = {
  getAll: () =>
    api.get<Location[]>('/locations'),

  getById: (id: number) =>
    api.get<Location>(`/locations/${id}`),
}
