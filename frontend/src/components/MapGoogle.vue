<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script>
  import GoogleMapsApiLoader from "google-maps-api-loader";
  export default {
    name: "GoogleMap",
      mounted() {
        this.loadMap();
    },
    methods: {
      async loadMap() {
        try {
          const google = await GoogleMapsApiLoader({
            apiKey: "AIzaSyCpK5brcYcvMEAAw0xx0ZQt8QRkroa4jI0", //Clave de API de Google Maps (solo para pruebas en modo desarrollo)
          });
          new google.maps.Map(this.$refs.mapContainer, {
            center: { lat: 37.3891, lng: -5.9845 }, //Coordenadas de Sevilla como ubicación de prueba
            zoom: 12,
          });
        } catch (error) {
          console.error("Error al cargar Google Maps:", error);
        }
      },
    },
  };
</script>

<style>
  .map-container {
    width: 100%;
    height: 400px;
  }
</style>
  