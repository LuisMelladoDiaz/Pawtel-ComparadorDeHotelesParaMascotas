<script setup>
import AppliedFilter from '../AppliedFilter.vue';

defineProps({
  filters: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['remove-filter']);
</script>

<template>
  <AppliedFilter 
    v-for="(filter, index) in filters" 
    :key="index" 
    :filterName="filter" 
    @remove="$emit('remove-filter', filter)" 
  />
</template>