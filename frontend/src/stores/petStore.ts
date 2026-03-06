import { create } from 'zustand'
import { petService } from '@/services/petService'
import type { Pet } from '@/types'

interface PetState {
  pets: Pet[]
  selectedPet: Pet | null
  isLoading: boolean

  fetchPets: () => Promise<void>
  selectPet: (pet: Pet | null) => void
  createPet: (data: FormData) => Promise<Pet>
  updatePet: (id: number, data: FormData) => Promise<void>
  deletePet: (id: number) => Promise<void>
}

export const usePetStore = create<PetState>((set, get) => ({
  pets: [],
  selectedPet: null,
  isLoading: false,

  fetchPets: async () => {
    set({ isLoading: true })
    try {
      const pets = await petService.getAll()
      set({ pets, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  selectPet: (pet) => set({ selectedPet: pet }),

  createPet: async (data) => {
    const newPet = await petService.create(data)
    set({ pets: [...get().pets, newPet] })
    return newPet
  },

  updatePet: async (id, data) => {
    await petService.update(id, data)
    await get().fetchPets()
  },

  deletePet: async (id) => {
    await petService.delete(id)
    set({ pets: get().pets.filter((p) => p.id !== id) })
  },
}))
