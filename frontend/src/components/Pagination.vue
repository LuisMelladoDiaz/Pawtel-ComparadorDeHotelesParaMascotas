<template>
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
      <span v-for="page in totalPages" :key="page">
        <button @click="goToPage(page)" :class="{ active: page === currentPage }">{{ page }}</button>
      </span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
    </div>
  </template>

  <script>
  export default {
    props: {
      currentPage: Number,
      totalPages: Number,
    },
    methods: {
      prevPage() {
        if (this.currentPage > 1) {
          this.$emit("update:currentPage", this.currentPage - 1);
        }
      },
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.$emit("update:currentPage", this.currentPage + 1);
        }
      },
      goToPage(page) {
        this.$emit("update:currentPage", page);
      },
    },
  };
  </script>

  <style scoped>
  .pagination {
    display: flex;
    justify-content: center;
    margin: 20px 0;
  }
  button {
    margin: 0 5px;
    padding: 5px 10px;
  }
  .active {
    font-weight: bold;
    background-color: #4caf50;
    color: white;
  }
  </style>
