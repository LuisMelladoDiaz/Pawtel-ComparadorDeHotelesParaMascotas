self.addEventListener('install', (event) => {
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(cacheNames.map((cache) => caches.delete(cache)))
    }).then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request))
})
