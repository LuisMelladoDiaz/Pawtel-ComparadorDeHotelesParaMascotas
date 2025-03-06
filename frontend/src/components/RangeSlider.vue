<template>
  <div>
    <h4 class="text-lg font-semibold mb-2">Precio</h4>
    <input type="range" v-model="price" min="0" max="500" step="10" class="w-full" @input="emitChange" />
    <div class="text-base text-gray-600">{{ price }} €</div>
  </div>
</template>
  
<script>
  export default {
    props: {
      modelValue: Number
    },
    data() {
      return {
        price: this.modelValue || 100
      };
    },
    methods: {
      emitChange() {
        this.$emit("update:modelValue", this.price);
      }
    }
  };
  </script>