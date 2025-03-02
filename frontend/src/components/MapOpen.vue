<template>
  <div ref="mapContainer" class="map-container"></div>
</template>
  
<script>
  import { onMounted, ref } from "vue";
  import "ol/ol.css"; // Estilos de OpenLayers
  import { Map, View } from "ol";
  import TileLayer from "ol/layer/Tile";
  import OSM from "ol/source/OSM";
  import { fromLonLat } from "ol/proj";
  
  export default {
    setup() {
      const mapContainer = ref(null);
  
      onMounted(() => {
        new Map({
          target: mapContainer.value, // Renderiza el mapa en este div
          layers: [
            new TileLayer({
              source: new OSM(), //Capa de OpenStreetMap
            }),
          ],
          view: new View({
            center: fromLonLat([-5.9845, 37.3891]), //Coordenadas de Sevilla como ubicación de prueba
            zoom: 12,
          }),
        });
      });
      return { mapContainer };
    },
  };
</script>
  
<style>
  .map-container {
    width: 100%;
    height: 400px;
  }
</style>
  