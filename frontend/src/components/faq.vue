<template>
    <div class="faq-container">
      <h2 class="title">Preguntas Frecuentes</h2>
      <div class="faq-item" v-for="(faq, index) in faqs" :key="index">
        <div class="faq-question" @click="toggleFAQ(index)">
          {{ faq.question }}
          <span class="icon">{{ faq.open ? "−" : "+" }}</span>
        </div>
        <div class="faq-answer" v-if="faq.open">
          {{ faq.answer }}
        </div>
      </div>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        faqs: [
          { question: "¿Cuáles son los requisitos para hospedar a mi mascota?", answer: "Cada hotel tiene sus propios requisitos...", open: false },
          { question: "¿Los hoteles incluyen servicio de alimentación?", answer: "Depende del hotel, algunos incluyen comida...", open: false },
          { question: "¿Puedo visitar el hotel antes de reservar?", answer: "Sí, la mayoría de los hoteles permiten visitas previas...", open: false },
        ],
      };
    },
    methods: {
      toggleFAQ(index) {
        this.faqs[index].open = !this.faqs[index].open;
      },
    },
  };
  </script>

  <style scoped>
  .faq-container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
  }

  .title {
    font-size: 24px;
    text-align: center;
    margin-bottom: 20px;
  }

  .faq-item {
    border-bottom: 1px solid #ccc;
    padding: 10px;
    cursor: pointer;
  }

  .faq-question {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
  }

  .faq-answer {
    margin-top: 5px;
    padding-left: 10px;
    color: #555;
  }

  .icon {
    font-size: 20px;
  }
  </style>
