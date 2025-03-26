<template>
  <div class="filter-section flex flex-col w-full">
    <h4 class="text-lg font-semibold mb-2">Número de Habitaciones</h4>
    <div class="flex items-center w-full gap-2">
      <button @click="decreaseRooms" class="text-xl font-semibold bg-gray-200 px-3 py-2 rounded flex-1">−</button>
      <input type="number" v-model="rooms" min="0" class="text-base text-gray-600 text-center border border-gray-300 rounded flex-1 appearance-none" @input="emitChange"/>
      <button @click="increaseRooms" class="text-xl font-semibold bg-gray-200 px-3 py-2 rounded flex-1">+</button>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      modelValue: Number
    },
    data() {
      return {
        rooms: this.modelValue || 0
      };
    },
    methods: {
      increaseRooms() {
        this.rooms++;
        this.emitChange();
      },
      decreaseRooms() {
        if (this.rooms > 0) this.rooms--;
        this.emitChange();
      },
      emitChange() {
        this.$emit("update:modelValue", this.rooms);
      }
    }
  };
  </script>
