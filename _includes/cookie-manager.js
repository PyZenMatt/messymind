/*!
 * Cookie Manager - GDPR Compliant Cookie Management
 * Gestisce consenso e caricamento condizionale di Google Analytics
 */

const cookieManager = {
    // Configurazione
    config: {
        cookieName: 'cookie-consent',
        cookieExpiry: 365, // giorni
        analyticsId: '{{ site.google_analytics | default: "G-4ZS3K400HQ" }}',
        domain: window.location.hostname
    },

    // Inizializzazione
    init() {
        console.log('🍪 Cookie Manager initializing...');
        this.checkExistingConsent();
        this.bindEvents();
        this.showBannerIfNeeded();
        console.log('🍪 Cookie Manager initialized');
    },

    // Controlla se esiste già un consenso
    checkExistingConsent() {
        const consent = this.getCookie(this.config.cookieName);
        if (consent) {
            try {
                const consentData = JSON.parse(consent);
                this.applyConsent(consentData);
                this.hideBanner();
            } catch (e) {
                console.warn('Invalid cookie consent data, requesting new consent');
                this.deleteCookie(this.config.cookieName);
            }
        }
    },

    // Mostra il banner se necessario
    showBannerIfNeeded() {
        const consent = this.getCookie(this.config.cookieName);
        console.log('🍪 Cookie consent check:', consent);
        if (!consent) {
            console.log('🍪 No consent found, showing banner...');
            setTimeout(() => {
                const banner = document.getElementById('cookie-banner');
                console.log('🍪 Banner element:', banner);
                if (banner) {
                    banner.classList.add('show');
                    console.log('🍪 Banner shown successfully');
                } else {
                    console.error('🍪 Banner element not found!');
                }
            }, 1000); // Ritardo di 1 secondo per UX migliore
        } else {
            console.log('🍪 Consent already exists, banner not shown');
        }
    },

    // Accetta tutti i cookie
    acceptAll() {
        const consent = {
            essential: true,
            analytics: true,
            timestamp: Date.now(),
            version: '1.0'
        };
        
        this.saveConsent(consent);
        this.applyConsent(consent);
        this.hideBanner();
        this.hideSettings();
        
        // Feedback utente
        this.showNotification('Tutti i cookie sono stati accettati', 'success');
    },

    // Rifiuta cookie non essenziali
    rejectAll() {
        const consent = {
            essential: true,
            analytics: false,
            timestamp: Date.now(),
            version: '1.0'
        };
        
        this.saveConsent(consent);
        this.applyConsent(consent);
        this.hideBanner();
        this.hideSettings();
        
        // Feedback utente
        this.showNotification('Solo i cookie essenziali saranno utilizzati', 'info');
    },

    // Salva impostazioni personalizzate
    saveSettings() {
        const analyticsToggle = document.getElementById('analytics-cookies');
        
        const consent = {
            essential: true,
            analytics: analyticsToggle ? analyticsToggle.checked : false,
            timestamp: Date.now(),
            version: '1.0'
        };
        
        this.saveConsent(consent);
        this.applyConsent(consent);
        this.hideBanner();
        this.hideSettings();
        
        // Feedback utente
        this.showNotification('Le tue preferenze sono state salvate', 'success');
    },

    // Salva consenso nel cookie
    saveConsent(consent) {
        const consentString = JSON.stringify(consent);
        this.setCookie(this.config.cookieName, consentString, this.config.cookieExpiry);
    },

    // Applica il consenso caricando i servizi appropriati
    applyConsent(consent) {
        if (consent.analytics) {
            this.loadGoogleAnalytics();
        } else {
            this.removeGoogleAnalytics();
        }
    },

    // Carica Google Analytics
    loadGoogleAnalytics() {
        // Evita caricamenti multipli
        if (window.gtag || document.querySelector('[src*="googletagmanager"]')) {
            return;
        }

        // Carica gtag script
        const script = document.createElement('script');
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${this.config.analyticsId}`;
        document.head.appendChild(script);

        // Inizializza gtag
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        window.gtag = gtag;
        
        gtag('js', new Date());
        gtag('config', this.config.analyticsId, {
            'anonymize_ip': true,
            'cookie_flags': 'SameSite=None;Secure'
        });

        console.log('Google Analytics caricato con consenso');
    },

    // Rimuove Google Analytics (per conformità)
    removeGoogleAnalytics() {
        // Rimuove script Google Analytics
        const scripts = document.querySelectorAll('[src*="googletagmanager"], [src*="google-analytics"]');
        scripts.forEach(script => script.remove());

        // Pulisce dataLayer e gtag
        if (window.gtag) {
            window.gtag = undefined;
        }
        if (window.dataLayer) {
            window.dataLayer = [];
        }

        // Rimuove cookie Google Analytics esistenti
        this.deleteCookie('_ga');
        this.deleteCookie('_gid');
        this.deleteCookie('_gat');
        
        // Rimuove cookie GA con pattern _ga_*
        document.cookie.split(';').forEach(cookie => {
            const name = cookie.split('=')[0].trim();
            if (name.startsWith('_ga_')) {
                this.deleteCookie(name);
            }
        });
    },

    // Mostra modal impostazioni
    showSettings() {
        const modal = document.getElementById('cookie-settings-modal');
        const analyticsToggle = document.getElementById('analytics-cookies');
        
        // Imposta stato toggle basato su consenso corrente
        const consent = this.getCurrentConsent();
        if (analyticsToggle && consent) {
            analyticsToggle.checked = consent.analytics || false;
        }
        
        if (modal) {
            modal.classList.add('show');
            document.body.style.overflow = 'hidden'; // Previeni scroll
        }
    },

    // Nascondi modal impostazioni
    hideSettings() {
        const modal = document.getElementById('cookie-settings-modal');
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = ''; // Ripristina scroll
        }
    },

    // Nascondi banner
    hideBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.remove('show');
            banner.classList.add('hidden');
        }
    },

    // Ottieni consenso corrente
    getCurrentConsent() {
        const consent = this.getCookie(this.config.cookieName);
        if (consent) {
            try {
                return JSON.parse(consent);
            } catch (e) {
                return null;
            }
        }
        return null;
    },

    // Mostra notifica
    showNotification(message, type = 'info') {
        // Crea elemento notifica
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#27ae60' : '#3498db'};
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            z-index: 10002;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-width: 300px;
            word-wrap: break-word;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Rimuovi dopo 3 secondi
        setTimeout(() => {
            notification.remove();
        }, 3000);
    },

    // Event binding
    bindEvents() {
        // Chiudi modal cliccando fuori
        document.addEventListener('click', (e) => {
            const modal = document.getElementById('cookie-settings-modal');
            if (modal && e.target === modal) {
                this.hideSettings();
            }
        });

        // Chiudi modal con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideSettings();
            }
        });
    },

    // Utility: Set Cookie
    setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax`;
    },

    // Utility: Get Cookie
    getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    },

    // Utility: Delete Cookie
    deleteCookie(name) {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;domain=${this.config.domain};`;
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;domain=.${this.config.domain};`;
    },

    // Funzione pubblica per revocare consenso (per link privacy)
    revokeConsent() {
        this.deleteCookie(this.config.cookieName);
        this.removeGoogleAnalytics();
        this.showNotification('Consenso revocato. Ricarica la pagina per vedere il banner.', 'info');
        
        // Ricarica dopo 2 secondi
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    }
};

// Inizializza quando DOM è pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => cookieManager.init());
} else {
    cookieManager.init();
}

// Esponi funzioni globali per i link
window.cookieManager = cookieManager;
