import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { nextTick } from 'vue'

export const useFiltersStore = defineStore('filters', () => {
  const selectedCity = ref(null)
  const startDate = ref(null)
  const endDate = ref(null)
  const selectedPetType = ref(null)

  const router = useRouter()

  watch(
    () => router.currentRoute.value.query,
    (query) => {
      selectedCity.value = query.filterCity as string || null
      selectedPetType.value = query.filterType as string || null
      startDate.value = query.filterStartDate || null
      endDate.value = query.filterEndDate || null
    },
    { immediate: true }
  )

  watch(
    () => ({
      city: selectedCity.value || "",
      type: selectedPetType.value || null,
      startDate: startDate.value || null,
      endDate: endDate.value || null,
    }),
    (newQuery) => {
      const currentQuery = router.currentRoute.value.query
      const updatedQuery = {
        ...currentQuery,
        filterCity: newQuery.city,
        filterType: newQuery.type,
        filterStartDate: newQuery.startDate,
        filterEndDate: newQuery.endDate,
      }
      router.push({ query: updatedQuery, path: '/hotels' })
    },
    { deep: true }
  )




  function updateAndSearch({ selectedCity: _selectedCity, startDate: _startDate, endDate: _endDate, selectedPetType: _selectedPetType }) {
    selectedCity.value = _selectedCity
    startDate.value = _startDate
    endDate.value = _endDate
    selectedPetType.value = _selectedPetType
  }

  return {
    selectedCity,
    startDate,
    endDate,
    selectedPetType,
    updateAndSearch,
  }
})
