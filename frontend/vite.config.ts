import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'
import path from "path";


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    VitePWA({

      strategies: "injectManifest",
      filename: "sw.js",
      srcDir: "src",
      workbox: {
        disableDevLogs: true,
      },
      // Controls whether the browser should update the pwa automatically, or prompt the user
      registerType: "autoUpdate",
      devOptions: {
        enabled: true,
        type: "module",
      },
      injectManifest: {
        rollupFormat: "iife",
        injectionPoint: undefined,
      },
      manifest:{
        display: 'standalone',
        display_override: ['window-controls-overlay'],
        theme_color: '#FFFFFF',
        background_color: '#FFFFFF',
        lang: 'es-ES',
        name: 'Pawtel',
        short_name: 'Pawtel',
        description: 'Bienvenido a Pawtel, una plataforma innovadora para la busqueda y reserva de hoteles para mascotas. Nuestra misión es ofrecer una experiencia fácil e intuitva que permita encontrar el hospedaje perfecto para su mejor amigo.',
        icons: [
          {
            src: '/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: '/pwa-maskable-192x192.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'maskable'
          },
          {
            src: '/pwa-maskable-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ],
      },}),
  ],
  resolve: {
    alias: {
        "@": path.resolve(__dirname, "src"),
    },
  },
})