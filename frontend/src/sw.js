
import { cleanupOutdatedCaches } from 'workbox-precaching'
import { clientsClaim } from 'workbox-core'

// Claim clients immediately
self.skipWaiting()
clientsClaim()

// Clean precache leftovers
cleanupOutdatedCaches()

// Delete all runtime caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const cacheNames = await caches.keys()
      await Promise.all(cacheNames.map((cache) => caches.delete(cache)))
    })()
  )
})

// Always bypass cache, fetch everything fresh
self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request))
})
