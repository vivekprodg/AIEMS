/**
 * PWA Service Worker - AIEMS
 * 
 * Offline-first Service Worker featuring dynamic Network-First
 * caching strategies for CMS image assets, branded offline HTML page fallback,
 * and automatic development environment passthrough (localhost / 127.0.0.1).
 */

// ==============================================================================
// 1. CONFIGURATION & VERSIONING
// ==============================================================================
const VERSION = 'v1.0.9';
const CACHE_PREFIX = 'aiems';

const CACHE_NAMES = {
  SHELL: `${CACHE_PREFIX}-shell-${VERSION}`,
  STATIC: `${CACHE_PREFIX}-static-${VERSION}`,
  IMAGES: `${CACHE_PREFIX}-images-${VERSION}`,
  APIS: `${CACHE_PREFIX}-apis-${VERSION}`
};

// Core offline shell assets
const PRECACHE_ASSETS = [
  '/?utm_source=pwa',
  '/home?utm_source=pwa',
  '/manifest.json',
  '/logo.svg'
];

const MAX_CACHE_LIMITS = {
  IMAGES: 60,
  APIS: 40
};

// ==============================================================================
// 2. BRANDED OFFLINE FALLBACK PAGE
// ==============================================================================
const OFFLINE_HTML = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline | AIEMS</title>
    <style>
        :root {
            --color-primary: #009444;
            --color-secondary: #0e0e54;
            --color-background: #F8FAFC;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--color-background);
            color: #1e293b;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 500px;
            background: #ffffff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(14, 14, 84, 0.08);
            border-top: 6px solid var(--color-primary);
            text-align: center;
        }
        h1 { color: var(--color-secondary); font-size: 1.8rem; margin-bottom: 15px; font-weight: 700; }
        p { font-size: 1rem; line-height: 1.6; color: #475569; margin-bottom: 30px; }
        .btn-retry {
            background-color: var(--color-primary);
            color: #ffffff;
            border: none;
            padding: 12px 30px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Connectivity Issue</h1>
        <p>You are currently offline. Loaded academic profiles remain accessible, but live form submissions require an active network connection.</p>
        <button class="btn-retry" onclick="window.location.reload()">Retry Connection</button>
    </div>
</body>
</html>
`;

// ==============================================================================
// 3. UTILITY METHODS
// ==============================================================================
async function limitCacheSize(cacheName, maxItems) {
  try {
    const cache = await caches.open(cacheName);
    const keys = await cache.keys();
    if (keys.length > maxItems) {
      await cache.delete(keys[0]);
      await limitCacheSize(cacheName, maxItems);
    }
  } catch (error) {
    console.error(`[AIEMS PWA] Error limiting cache size for ${cacheName}:`, error);
  }
}

function isEligibleForCache(request) {
  if (request.method !== 'GET') return false;
  const url = new URL(request.url);

  // Passthrough protection: Never intercept local development server or Next.js HMR
  if (
    url.hostname === 'localhost' ||
    url.hostname === '127.0.0.1' ||
    url.port === '3000' ||
    url.pathname.includes('/_next/') ||
    url.pathname.includes('webpack-hmr') ||
    url.searchParams.has('bypass_cache') ||
    url.searchParams.get('bypass_cache') === 'true' ||
    url.pathname.includes('/aiems-control-admin-panel/') ||
    url.pathname.includes('/admin/') ||
    url.pathname.includes('/home-content') ||
    url.pathname.includes('/about-content') ||
    url.hostname.includes('tawk.to') ||
    url.hostname.includes('embed.tawk.to')
  ) {
    return false;
  }
  return true;
}

// ==============================================================================
// 4. LIFECYCLE MANAGEMENT EVENTS
// ==============================================================================
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAMES.SHELL).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  const activeCacheNames = Object.values(CACHE_NAMES);
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (!activeCacheNames.includes(key)) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// ==============================================================================
// 5. CACHING STRATEGIES
// ==============================================================================
self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (!isEligibleForCache(request)) return;

  const url = new URL(request.url);

  // Next.js static build files
  if (url.pathname.startsWith('/_next/static/') || url.pathname.includes('/fonts/')) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseCopy = networkResponse.clone();
            caches.open(CACHE_NAMES.STATIC).then((cache) => cache.put(request, responseCopy));
          }
          return networkResponse;
        });
      })
    );
    return;
  }

  // Dynamic Images & Uploads (Network-First)
  if (
    request.destination === 'image' ||
    url.pathname.includes('/img/') ||
    url.pathname.includes('/footer/') ||
    url.pathname.includes('/banners/') ||
    url.pathname.includes('/facilities/') ||
    url.pathname.includes('/programs/')
  ) {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseCopy = networkResponse.clone();
            caches.open(CACHE_NAMES.IMAGES).then((cache) => {
              cache.put(request, responseCopy);
              event.waitUntil(limitCacheSize(CACHE_NAMES.IMAGES, MAX_CACHE_LIMITS.IMAGES));
            });
          }
          return networkResponse;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // API Requests (Network-First)
  if (url.pathname.includes('/api/')) {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseCopy = networkResponse.clone();
            caches.open(CACHE_NAMES.APIS).then((cache) => {
              cache.put(request, responseCopy);
              event.waitUntil(limitCacheSize(CACHE_NAMES.APIS, MAX_CACHE_LIMITS.APIS));
            });
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(request).then((cached) => {
            if (cached) return cached;
            return new Response(
              JSON.stringify({ error: 'Offline mode active. Data unavailable.' }),
              { headers: { 'Content-Type': 'application/json' } }
            );
          });
        })
    );
    return;
  }

  // Navigation Requests (HTML Page Fallback)
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => {
        return caches.match(request).then((cached) => {
          if (cached) return cached;
          return new Response(OFFLINE_HTML, { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
        });
      })
    );
    return;
  }
});