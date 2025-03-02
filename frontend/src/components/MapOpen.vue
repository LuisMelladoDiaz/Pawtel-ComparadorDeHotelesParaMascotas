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
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import Feature from "ol/Feature";
import Point from "ol/geom/Point";
import Style from "ol/style/Style";
import Icon from "ol/style/Icon";

export default {
  setup() {
    const mapContainer = ref(null);
    let map;

    onMounted(() => {
      map = new Map({
        target: mapContainer.value,
        layers: [
          new TileLayer({
            source: new OSM(), // Capa base de OpenStreetMap
          }),
        ],
        view: new View({
          center: fromLonLat([-5.9845, 37.3891]), // Coordenadas de Sevilla como ubicación de prueba
          zoom: 12,
        }),
      });

      // Lista de coordenadas para los marcadores (tendria que ser dinamico)
      const locations = [
        { name: "Plaza de España", coords: [-5.9869, 37.3772] },
        { name: "Catedral de Sevilla", coords: [-5.9928, 37.3860] },
        { name: "Metropol Parasol", coords: [-5.9931, 37.3936] },
      ];

      const vectorSource = new VectorSource();
      
      // Agregar marcadores al mapa
      locations.forEach((location) => {
        const marker = new Feature({
          geometry: new Point(fromLonLat(location.coords)),
        });

        // Estilo del marcador
        marker.setStyle(
          new Style({
            image: new Icon({
              anchor: [0.5, 1],
              //src: "/images/pawprint.png",
              src: "/images/pawpaw.png",
              scale: 0.07,
            }),
          })
        );
        vectorSource.addFeature(marker);
      });

      // Agregar la capa de los marcadores al mapa
      const markerLayer = new VectorLayer({
        source: vectorSource,
      });

      map.addLayer(markerLayer);
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
