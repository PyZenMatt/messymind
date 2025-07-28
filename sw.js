const CACHE_NAME = 'matteoricci-v2.0-optimized';
const STATIC_CACHE = 'static-v2.0';
const RUNTIME_CACHE = 'runtime-v2.0';

// Risorse da cachare immediatamente - OTTIMIZZATE
const PRECACHE_URLS = [
  '/',
  '/offline.html',
  '/assets/main.css',
  '/img/amore.webp',
  '/assets/vendor/bootstrap/js/bootstrap.bundle.min.js',
  '/assets/vendor/startbootstrap-clean-blog/js/scripts.js'
];

// Strategie di cache per diversi tipi di risorsa
const CACHE_STRATEGIES = {
  // Cache First: per risorse statiche
  static: [
    /\.(?:js|css|woff2?|ttf|eot)$/,
    /\/assets\//,
    /\/img\//
  ],
  
  // Network First: per contenuti dinamici
  networkFirst: [
    /\/api\//,
    /\/admin\//
  ],
  
  // Stale While Revalidate: per pagine
  staleWhileRevalidate: [
    /\.(?:html)$/,
    /\/$/,
    /\/[^.]*$/
  ]
};

// Installazione del Service Worker
self.addEventListener('install', event => {
  console.log('SW: Install event');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('SW: Precaching static assets');
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => {
        console.log('SW: Skip waiting');
        return self.skipWaiting();
      })
  );
});

// Attivazione del Service Worker
self.addEventListener('activate', event => {
  console.log('SW: Activate event');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(cacheName => {
              return cacheName !== STATIC_CACHE && 
                     cacheName !== RUNTIME_CACHE;
            })
            .map(cacheName => {
              console.log('SW: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log('SW: Claiming clients');
        return self.clients.claim();
      })
  );
});

// Intercettazione delle richieste
self.addEventListener('fetch', event => {
  // Salta richieste non HTTP
  if (!event.request.url.startsWith('http')) {
    return;
  }
  
  // Salta richieste POST/PUT/DELETE
  if (event.request.method !== 'GET') {
    return;
  }
  
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  
  // Strategia per risorse statiche
  if (isStaticAsset(request)) {
    return cacheFirst(request);
  }
  
  // Strategia per pagine HTML
  if (isHTMLPage(request)) {
    return staleWhileRevalidate(request);
  }
  
  // Strategia per immagini
  if (isImage(request)) {
    return cacheFirst(request, {
      cacheName: 'images-v1',
      maxEntries: 100,
      maxAgeSeconds: 7 * 24 * 60 * 60 // 7 giorni
    });
  }
  
  // Default: network only
  return fetch(request);
}

// Cache First Strategy
async function cacheFirst(request, options = {}) {
  const cacheName = options.cacheName || STATIC_CACHE;
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  
  if (cached) {
    console.log('SW: Cache hit for', request.url);
    return cached;
  }
  
  try {
    const response = await fetch(request);
    
    if (response.status === 200) {
      cache.put(request, response.clone());
      
      // Gestione maxEntries se specificato
      if (options.maxEntries) {
        await trimCache(cacheName, options.maxEntries);
      }
    }
    
    return response;
  } catch (error) {
    console.log('SW: Network failed for', request.url);
    
    // Fallback per pagine offline
    if (isHTMLPage(request)) {
      return caches.match('/offline.html');
    }
    
    throw error;
  }
}

// Network First Strategy
async function networkFirst(request) {
  const cache = await caches.open(RUNTIME_CACHE);
  
  try {
    const response = await fetch(request);
    
    if (response.status === 200) {
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.log('SW: Network failed, trying cache for', request.url);
    const cached = await cache.match(request);
    
    if (cached) {
      return cached;
    }
    
    throw error;
  }
}

// Stale While Revalidate Strategy
async function staleWhileRevalidate(request) {
  const cache = await caches.open(RUNTIME_CACHE);
  const cached = await cache.match(request);
  
  // Fetch in background
  const fetchPromise = fetch(request).then(response => {
    if (response.status === 200) {
      cache.put(request, response.clone());
    }
    return response;
  });
  
  // Ritorna cache se disponibile, altrimenti aspetta il network
  return cached || fetchPromise;
}

// Utility functions
function isStaticAsset(request) {
  return CACHE_STRATEGIES.static.some(regex => regex.test(request.url));
}

function isHTMLPage(request) {
  return request.headers.get('accept').includes('text/html');
}

function isImage(request) {
  return request.headers.get('accept').includes('image/');
}

async function trimCache(cacheName, maxEntries) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  
  if (keys.length > maxEntries) {
    const keysToDelete = keys.slice(0, keys.length - maxEntries);
    await Promise.all(keysToDelete.map(key => cache.delete(key)));
  }
}

// Background Sync per analytics offline
self.addEventListener('sync', event => {
  if (event.tag === 'analytics-sync') {
    event.waitUntil(syncAnalytics());
  }
});

async function syncAnalytics() {
  // Implementa sincronizzazione analytics quando torna online
  console.log('SW: Syncing analytics data');
}

// Push notifications (per future funzionalità)
self.addEventListener('push', event => {
  if (event.data) {
    const options = {
      body: event.data.text(),
      icon: '/img/icon-192.png',
      badge: '/img/badge-72.png',
      vibrate: [100, 50, 100],
      data: {
        dateOfArrival: Date.now(),
        primaryKey: 1
      }
    };
    
    event.waitUntil(
      self.registration.showNotification('Nuovo articolo su matteoricci.net', options)
    );
  }
});

// Cleanup automatico cache vecchie
setInterval(() => {
  caches.keys().then(cacheNames => {
    cacheNames.forEach(cacheName => {
      if (cacheName.includes('v1.1') || cacheName.includes('v1.0')) {
        caches.delete(cacheName);
      }
    });
  });
}, 24 * 60 * 60 * 1000); // Ogni 24 ore
