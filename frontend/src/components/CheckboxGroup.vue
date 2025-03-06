<template>
  <div>
    <h4 class="text-lg font-semibold mb-2">Servicios</h4>
    <div class="flex flex-col gap-2">
      <label v-for="service in servicesList" :key="service" class="flex items-center gap-2">
        <input type="checkbox" :value="service" v-model="selectedServices" class="w-4 h-4" @change="emitChange" />
        <span>{{ service }}</span>
      </label>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      modelValue: Array,
      servicesList: Array
    },
    data() {
      return {
        selectedServices: this.modelValue || []
      };
    },
    methods: {
      emitChange() {
        this.$emit("update:modelValue", this.selectedServices);
      }
    }
  };
</script>
  