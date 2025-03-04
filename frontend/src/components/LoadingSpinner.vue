<template>
    <div class="spinner-container">
      <div class="spinner"></div>
    </div>
  </template>

  <style scoped>

  .spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
  }

  .spinner {
    border: 8px solid #f3f3f3;
    border-top: 8px solid #C36C6C;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
  }

  /* Animación de giro */
  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  </style>
