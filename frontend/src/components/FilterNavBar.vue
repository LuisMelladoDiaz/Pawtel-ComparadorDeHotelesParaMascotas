<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useFiltersStore } from '@/filters'

import DatePicker from '../components/DatePicker.vue'
import DatePickerMobile from './DatePickerMobile.vue'
import Button from '../components/Button.vue'

const router = useRouter()
const filters = useFiltersStore()

const cities = ref(["Sevilla","Málaga","Cádiz","Córdoba","Jaén","Almería","Granada","Huelva"
].sort())

const petTypes = ["DOG", "CAT", "BIRD", "MIXED"].sort()

const petTypeMapping = {
  DOG: 'Perro',
  CAT: 'Gato',
  BIRD: 'Pájaro',
  MIXED: 'Mixto'
}

const petTypesInSpanish = petTypes.map((petType) => petTypeMapping[petType])

// Temporary local state
const selectedCity = ref(filters.selectedCity || "")
const selectedPetType = ref(filters.selectedPetType || "")
const startDate = ref(filters.startDate || null)
const endDate = ref(filters.endDate || null)

const onSearch = () => {
  filters.updateAndSearch({
    selectedCity: selectedCity.value,
    selectedPetType: selectedPetType.value,
    startDate: startDate.value,
    endDate: endDate.value
  })
}
</script>

<template>
  <div class="filter-navbar bg-terracota h-[100px]">
    <div class="filter-content max-w-7xl mx-auto px-5 h-full flex items-center justify-between">

      <!-- City Dropdown -->
      <div class="relative inline-block text-pawtel-black">
        <i class="fas fa-map-marker-alt absolute left-2 bottom-1 transform -translate-y-1/2 text-[18px]"></i>
        <select
          :value="selectedCity"
          @change="selectedCity = $event.target.value"
          class="bg-white min-h-[42px] pl-8 text-[18px] shadow-sm font-complementario rounded-lg min-w-[300px] cursor-pointer"
        >
          <option disabled value="">Selecciona una ciudad</option>
          <option value="">Todas</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>

      <!-- DatePicker (Desktop) -->
      <DatePicker
        class="bg-white hidden md:flex"
        :startDate="startDate"
        :endDate="endDate"
        @update:startDate="startDate = $event"
        @update:endDate="endDate = $event"
      />

      <!-- DatePicker (Mobile) -->
      <DatePicker
        class="bg-white md:hidden"
        :startDate="startDate"
        :endDate="endDate"
        @update:startDate="startDate = $event"
        @update:endDate="endDate = $event"
      />

      <!-- Pet Type Dropdown -->
      <div class="relative inline-block">
        <i class="fa-solid fa-paw absolute left-2 bottom-1 transform -translate-y-1/2 text-pawtel-black text-[18px]"></i>
        <select
          :value="selectedPetType"
          @change="selectedPetType = $event.target.value"
          class="bg-white min-h-[42px] pl-8 text-[18px] text-pawtel-black shadow-sm font-complementario rounded-lg p-2 min-w-[300px] cursor-pointer"
        >
          <option disabled value="">Elige un tipo de mascota</option>
          <option v-for="(pet, index) in petTypesInSpanish" :key="index" :value="petTypes[index]">
            {{ pet }}
          </option>
        </select>
      </div>

      <!-- Search Button -->
      <Button
        @click="onSearch"
        class="bg-white m-0! rounded-lg cursor-pointer h-[42px]! max-w-[150px]! w-full! shadow-sm flex items-center justify-between text-xl gap-1 font-bold text-pawtel-black"
      >
        <p class="grow text-center">Buscar</p>
      </Button>
    </div>
  </div>
</template>

<style scoped>
.no-interaction {
  pointer-events: none;
  opacity: 0.6;
}

@media (max-width: 1100px) {
  .filter-navbar {
    height: 260px;
    width: 100%;
  }

  .filter-content {
    flex-direction: column;
    padding: 20px;
  }

  .text {
    max-width: 300px;
  }
}
</style>
