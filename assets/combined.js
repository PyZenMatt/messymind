/* Combined JS - Generated Mon Jul 28 11:52:54 CEST 2025 */
/* From: performance.js */
/* Async CSS Loading Utilities */

(function() {
  'use strict';
  
  // Preload CSS con callback di caricamento
  function loadCSS(href, onload) {
    var link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'style';
    link.href = href;
    
    link.onload = function() {
      this.rel = 'stylesheet';
      if (onload) onload();
    };
    
    // Fallback per browser che non supportano preload
    link.onerror = function() {
      var fallback = document.createElement('link');
      fallback.rel = 'stylesheet';
      fallback.href = href;
      document.head.appendChild(fallback);
      if (onload) onload();
    };
    
    document.head.appendChild(link);
    return link;
  }
  
  // Caricamento Font Awesome con priorità bassa
  function loadFontAwesome() {
    if (!document.querySelector('link[href*="font-awesome"]')) {
      loadCSS('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css', function() {
        console.log('Font Awesome caricato');
      });
    }
  }
  
  // Caricamento Google Fonts con font-display: swap
  function loadGoogleFonts() {
    if (!document.querySelector('link[href*="fonts.googleapis.com"]')) {
      loadCSS('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;700&family=Lora:wght@400;700&display=swap', function() {
        console.log('Google Fonts caricato');
        document.body.classList.add('fonts-loaded');
      });
    }
  }
  
  // Caricamento progressivo delle risorse
  function initProgressiveLoading() {
    // Priorità 1: CSS principale (già caricato via preload)
    // Priorità 2: Google Fonts
    setTimeout(loadGoogleFonts, 100);
    
    // Priorità 3: Font Awesome (non critico)
    setTimeout(loadFontAwesome, 500);
    
    // Priorità 4: Analytics e script non critici
    setTimeout(function() {
      if (window.loadDeferredScripts) {
        window.loadDeferredScripts();
      }
    }, 1000);
  }
  
  // Web Fonts loading con fallback
  function optimizeFontLoading() {
    if ('fonts' in document) {
      var fontTimeouts = [];
      
      // Timeout per fallback fonts
      fontTimeouts.push(setTimeout(function() {
        document.body.classList.add('fonts-timeout');
      }, 3000));
      
      // Carica font specifici se disponibili
      Promise.all([
        document.fonts.load('400 16px "Open Sans"'),
        document.fonts.load('700 16px "Open Sans"'),
        document.fonts.load('400 16px "Lora"'),
        document.fonts.load('700 16px "Lora"')
      ]).then(function() {
        document.body.classList.add('fonts-loaded');
        fontTimeouts.forEach(clearTimeout);
      }).catch(function() {
        console.log('Alcuni font non sono stati caricati');
        document.body.classList.add('fonts-timeout');
      });
    }
  }
  
  // Intersection Observer per lazy loading avanzato
  function setupAdvancedLazyLoading() {
    if ('IntersectionObserver' in window) {
      var lazyImageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            var img = entry.target;
            
            // Pre-carica l'immagine
            var tempImg = new Image();
            tempImg.onload = function() {
              img.src = img.dataset.src;
              img.classList.remove('lazy');
              img.classList.add('loaded');
            };
            tempImg.src = img.dataset.src;
            
            lazyImageObserver.unobserve(img);
          }
        });
      }, {
        rootMargin: '50px 0px',
        threshold: 0.1
      });
      
      document.querySelectorAll('img[data-src]').forEach(function(img) {
        lazyImageObserver.observe(img);
      });
    }
  }
  
  // Preconnect alle risorse esterne
  function setupPreconnections() {
    var connections = [
      'https://fonts.googleapis.com',
      'https://fonts.gstatic.com',
      'https://cdnjs.cloudflare.com'
    ];
    
    connections.forEach(function(url) {
      var link = document.createElement('link');
      link.rel = 'preconnect';
      link.href = url;
      link.crossOrigin = 'anonymous';
      document.head.appendChild(link);
    });
  }
  
  // Service Worker per caching
  function registerServiceWorker() {
    if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
      navigator.serviceWorker.register('/sw.js').then(function(registration) {
        console.log('SW registrato:', registration.scope);
      }).catch(function(error) {
        console.log('SW fallito:', error);
      });
    }
  }
  
  // Performance monitoring
  function trackPerformance() {
    if ('performance' in window) {
      window.addEventListener('load', function() {
        setTimeout(function() {
          var perfData = performance.timing;
          var loadTime = perfData.loadEventEnd - perfData.navigationStart;
          var domReady = perfData.domContentLoadedEventEnd - perfData.navigationStart;
          
          console.log('Load Time:', loadTime + 'ms');
          console.log('DOM Ready:', domReady + 'ms');
          
          // Invia metriche (se hai analytics)
          if (window.gtag) {
            gtag('event', 'timing_complete', {
              'name': 'load',
              'value': loadTime
            });
          }
        }, 0);
      });
    }
  }
  
  // Inizializzazione al DOM ready
  function init() {
    setupPreconnections();
    initProgressiveLoading();
    optimizeFontLoading();
    setupAdvancedLazyLoading();
    trackPerformance();
    
    // Service worker solo in produzione
    if (window.location.hostname !== 'localhost') {
      registerServiceWorker();
    }
  }
  
  // Avvia quando il DOM è pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  // Esporta funzioni globalmente se necessario
  window.performanceUtils = {
    loadCSS: loadCSS,
    loadGoogleFonts: loadGoogleFonts,
    loadFontAwesome: loadFontAwesome
  };
  
})();

/* From: scripts.js */
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


