<template>
    <div class="filters flex flex-col gap-4">
      <RangeSlider v-model="priceRange" />
      <NumericStepper v-model="numRooms" />
      <DropdownPicker v-model="selectedType" label="Tipo de alojamiento" :options="[
          { label: 'Seleccionar', value: '' },
          { label: 'Hotel', value: 'hotel' },
          { label: 'Casa', value: 'casa' },
          { label: 'Apartamento', value: 'apartamento' }
        ]"
      />
      <CheckboxGroup v-model="selectedServices" :servicesList="services" />
      <Button type="accept" @click="applyFilters">Aceptar</Button>
    </div>
  </template>

  <script setup>
  import RangeSlider from "./RangeSlider.vue";
  import NumericStepper from "./NumericStepper.vue";
  import DropdownPicker from '../components/DropdownPicker.vue';
  import CheckboxGroup from "./CheckboxGroup.vue";
  import Button from "../components/Button.vue";
  </script>

  <script>
  export default {
    data() {
      return {
        priceRange: 100,
        numRooms: 0,
        selectedType: "",
        services: ["Cámaras de vigilancia", "WiFi", "Jardín", "Otros parámetros"],
        selectedServices: []
      };
    },
    methods: {
      applyFilters() {
        this.$emit("filter-changed", {
          price: this.priceRange,
          rooms: this.numRooms,
          type: this.selectedType,
          services: this.selectedServices
        });
      }
    }
  };
  </script>
