<template>
    <div class="flex items-center bg-terracota text-white p-2 px-4 rounded-lg shadow-sm">
      <span>{{ filterName }}</span>
      <button @click="removeFilter" class="ml-2 text-white hover:text-gray-200 cursor-pointer">
        <font-awesome-icon :icon="['fas', 'times']" />
      </button>
    </div>
  </template>

  <script setup>
    import { defineProps, defineEmits } from "vue";
    import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
    import { library } from "@fortawesome/fontawesome-svg-core";
    import { faTimes } from "@fortawesome/free-solid-svg-icons";

    library.add(faTimes);

    defineProps({
      filterName: { type: String, required: true },
    });

    const emit = defineEmits(["remove"]);
    const removeFilter = () => {
      emit("remove");
    };
    </script>

    <style scoped>
    button {
      transition: color 0.2s ease-in-out;
    }
  </style>
