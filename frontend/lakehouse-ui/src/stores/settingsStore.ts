import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', () => {
  // State
  const updateListTrigger = ref<boolean>(false)

  // Getters
  const getTriggerValue = computed<boolean>(() => updateListTrigger.value)

  // Actions
  function setUpdateTrigger(value: boolean): void {
    updateListTrigger.value = value
  }

  return { updateListTrigger, getTriggerValue, setUpdateTrigger }
})

export interface SettingsStore {
  updateListTrigger: boolean
  getTriggerValue: boolean
  setUpdateTrigger: (value: boolean) => void
}
