import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { CollectionFilter } from '@/shared/interfaces/http/CollectionSearchRequest'

export const useCatalogStore = defineStore('catalog', () => {
  // State

  const catalogViewOptions = ['all', 'my']

  const catalogView = ref<string>('all')

  const is_file_empty = ref<boolean>(false)

  const is_filter_visible = ref<boolean>(true)

  const collectionFilters = ref<CollectionFilter[]>([])

  // Getters
  const getCatalogView = computed<string>(() => catalogView.value)
  const getIsFileEmpty = computed<boolean>(() => is_file_empty.value)

  // Setters
  function setCatalogView(value: string): void {
    if (!catalogViewOptions.includes(value)) {
      throw new Error(`Invalid catalog view option: ${value}`)
    }
    catalogView.value = value
  }

  function setIsFileEmpty(value: boolean): void {
    is_file_empty.value = value
  }

  function setCollectionFilters(filters: CollectionFilter[]): void {
    collectionFilters.value = filters
  }

  function setIsFilterVisible(value: boolean): void {
    is_filter_visible.value = value
  }

  function clearCollectionFilters(): void {
    collectionFilters.value = []
    is_filter_visible.value = true
  }

  return {
    catalogView,
    collectionFilters,
    getCatalogView,
    setCatalogView,
    setIsFilterVisible,
    setCollectionFilters,
    clearCollectionFilters,
    is_filter_visible,
    is_file_empty,
    getIsFileEmpty,
    setIsFileEmpty,
  }
})

export interface CatalogStore {
  catalogView: string
  getCatalogView: string
  setCatalogView: (value: string) => void
  is_file_empty: boolean
  getIsFileEmpty: boolean
  setIsFileEmpty: (value: boolean) => void
}
