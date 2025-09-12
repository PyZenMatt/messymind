/*! Cookie Manager - extracted for deferred loading */

// NOTE: This file is a copy of `_includes/cookie-manager.js` to enable loading via <script src="/assets/js/cookie-manager.js" defer>

const cookieManager = {
    config: {
        cookieName: 'cookie-consent',
        cookieExpiry: 365,
        analyticsId: (function(){ try { return (typeof SITE_GOOGLE_ANALYTICS !== 'undefined') ? SITE_GOOGLE_ANALYTICS : 'G-MLB32YW721'; } catch(e){ return 'G-MLB32YW721'; } })(),
        domain: window.location.hostname
    },
    init() {
        console.log('🍪 Cookie Manager initializing...');
        this.checkExistingConsent();
        this.bindEvents();
        this.showBannerIfNeeded();
        console.log('🍪 Cookie Manager initialized');
    },
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
            }, 1000);
        } else {
            console.log('🍪 Consent already exists, banner not shown');
        }
    },
    acceptAll() {
        const consent = { essential: true, analytics: true, timestamp: Date.now(), version: '1.0' };
        this.saveConsent(consent);
        this.applyConsent(consent);
        this.hideBanner();
        this.hideSettings();
        this.showNotification('Tutti i cookie sono stati accettati', 'success');
    },
    rejectAll() {
        const consent = { essential: true, analytics: false, timestamp: Date.now(), version: '1.0' };
        this.saveConsent(consent);
        this.applyConsent(consent);
        this.hideBanner();
        this.hideSettings();
        this.showNotification('Solo i cookie essenziali saranno utilizzati', 'info');
    },
    saveSettings() {
        const analyticsToggle = document.getElementById('analytics-cookies');
        const consent = { essential: true, analytics: analyticsToggle ? analyticsToggle.checked : false, timestamp: Date.now(), version: '1.0' };
        this.saveConsent(consent);
        this.applyConsent(consent);
        this.hideBanner();
        this.hideSettings();
        this.showNotification('Le tue preferenze sono state salvate', 'success');
    },
    saveConsent(consent) { const consentString = JSON.stringify(consent); this.setCookie(this.config.cookieName, consentString, this.config.cookieExpiry); },
    applyConsent(consent) { if (consent.analytics) { this.loadGoogleAnalytics(); } else { this.removeGoogleAnalytics(); } },
    loadGoogleAnalytics() {
        if (window.gtag || document.querySelector('[src*="googletagmanager"]')) { return; }
        const script = document.createElement('script');
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${this.config.analyticsId}`;
        document.head.appendChild(script);
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);} window.gtag = gtag;
        gtag('js', new Date());
        gtag('config', this.config.analyticsId, { 'anonymize_ip': true, 'cookie_flags': 'SameSite=None;Secure' });
        console.log('Google Analytics caricato con consenso');
    },
    removeGoogleAnalytics() {
        const scripts = document.querySelectorAll('[src*="googletagmanager"], [src*="google-analytics"]'); scripts.forEach(script => script.remove());
        if (window.gtag) { window.gtag = undefined; }
        if (window.dataLayer) { window.dataLayer = []; }
        this.deleteCookie('_ga'); this.deleteCookie('_gid'); this.deleteCookie('_gat');
        document.cookie.split(';').forEach(cookie => { const name = cookie.split('=')[0].trim(); if (name.startsWith('_ga_')) { this.deleteCookie(name); } });
    },
    showSettings() { const modal = document.getElementById('cookie-settings-modal'); const analyticsToggle = document.getElementById('analytics-cookies'); const consent = this.getCurrentConsent(); if (analyticsToggle && consent) { analyticsToggle.checked = consent.analytics || false; } if (modal) { modal.classList.add('show'); document.body.style.overflow = 'hidden'; } },
    hideSettings() { const modal = document.getElementById('cookie-settings-modal'); if (modal) { modal.classList.remove('show'); document.body.style.overflow = ''; } },
    hideBanner() { const banner = document.getElementById('cookie-banner'); if (banner) { banner.classList.remove('show'); banner.classList.add('hidden'); } },
    getCurrentConsent() { const consent = this.getCookie(this.config.cookieName); if (consent) { try { return JSON.parse(consent); } catch (e) { return null; } } return null; },
    showNotification(message, type = 'info') { const notification = document.createElement('div'); notification.style.cssText = `position: fixed; top: 20px; right: 20px; background: ${type === 'success' ? '#27ae60' : '#3498db'}; color: white; padding: 15px 20px; border-radius: 5px; z-index: 10002; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); max-width: 300px; word-wrap: break-word;`; notification.textContent = message; document.body.appendChild(notification); setTimeout(() => { notification.remove(); }, 3000); },
    bindEvents() { document.addEventListener('click', (e) => { const modal = document.getElementById('cookie-settings-modal'); if (modal && e.target === modal) { this.hideSettings(); } }); document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { this.hideSettings(); } }); },
    setCookie(name, value, days) { const expires = new Date(); expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000)); document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax`; },
    getCookie(name) { const nameEQ = name + "="; const ca = document.cookie.split(';'); for (let i = 0; i < ca.length; i++) { let c = ca[i]; while (c.charAt(0) === ' ') c = c.substring(1, c.length); if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length); } return null; },
    deleteCookie(name) { document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`; document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;domain=${this.config.domain};`; document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;domain=.${this.config.domain};`; },
    revokeConsent() { this.deleteCookie(this.config.cookieName); this.removeGoogleAnalytics(); this.showNotification('Consenso revocato. Ricarica la pagina per vedere il banner.', 'info'); setTimeout(() => { window.location.reload(); }, 2000); }
};

if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', () => cookieManager.init()); } else { cookieManager.init(); }
window.cookieManager = cookieManager;
