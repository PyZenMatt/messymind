
// NOTE: This file is a copy of `_includes/cookie-manager.js` to enable loading via <script src="/assets/js/cookie-manager.js" defer>

const cookieManager = {
    config: {
        cookieName: 'cookie-consent',
        cookieExpiry: 365,
        analyticsId: (function(){ try { return (typeof SITE_GOOGLE_ANALYTICS !== 'undefined') ? SITE_GOOGLE_ANALYTICS : 'G-3X8F40ST1M'; } catch(e){ return 'G-YZRF8LG3GD'; } })(),
        domain: window.location.hostname
    },
    init() {
        console.log('🍪 Cookie Manager initializing...');
        console.log('⏱️  INIT → checking existing consent flow');
        this.checkExistingConsent();
        this.bindEvents();
        this.showBannerIfNeeded();
        console.log('🍪 Cookie Manager initialized');
    },
    checkExistingConsent() {
        console.log('🔎 checkExistingConsent() called');
        const consent = this.getCookie(this.config.cookieName);
        console.log('📌 Raw cookie value:', consent);
        if (consent) {
            try {
                const consentData = JSON.parse(consent);
                console.log('✅ Parsed consent data:', consentData);
                console.log('📌 consent.analytics:', consentData.analytics);
                this.applyConsent(consentData);
                this.hideBanner();
            } catch (e) {
                console.warn('❌ Invalid cookie consent data:', e.message);
                this.deleteCookie(this.config.cookieName);
            }
        } else {
            console.log('⚠️  No existing consent found - banner will show');
        }
    },
    showBannerIfNeeded() {
        const consent = this.getCookie(this.config.cookieName);
        if (!consent) {
            // Show banner without forcing layout calculations. Use rAF to batch style changes.
            const banner = document.getElementById('cookie-banner');
            if (!banner) return;
            // ensure initial state (hidden via transform) is present
            banner.classList.remove('hidden');
            // Use a tiny timeout to allow the browser to paint the initial state, then use rAF to add the class.
            requestAnimationFrame(() => requestAnimationFrame(() => banner.classList.add('show')));
        } else {
            // Consent already exists — nothing to do.
        }
    },
    acceptAll() {
        console.log('🍪 acceptAll() called - Accepting all cookies including analytics');
        const consent = { essential: true, analytics: true, timestamp: Date.now(), version: '1.0' };
        this.saveConsent(consent);
        this.applyConsent(consent);
        this.hideBanner();
        this.hideSettings();
        this.showNotification('Tutti i cookie sono stati accettati', 'success');
    },
    rejectAll() {
        console.log('🍪 rejectAll() called - Rejecting analytics cookies');
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
    applyConsent(consent) { 
        console.log('═══ APPLY CONSENT CALLED ═══');
        console.log('Received consent object:', JSON.stringify(consent));
        console.log('consent.analytics value:', consent.analytics);
        console.log('typeof consent.analytics:', typeof consent.analytics);
        
        if (consent.analytics === true) { 
            console.log('→ DECISION: Should LOAD GA');
            this.loadGoogleAnalytics(); 
        } else { 
            console.log('→ DECISION: Should NOT load GA (analytics is', consent.analytics, ')');
            this.removeGoogleAnalytics(); 
        }
        console.log('═══════════════════════════');
    },
    loadGoogleAnalytics() {
        // Blocca GA in ambiente locale (localhost / 127.0.0.1)
        if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
            console.log('🚫 GA disabilitato in ambiente locale');
            return;
        }
        
        console.log('🔥 LOAD GA CALLED');
        console.log('📊 loadGoogleAnalytics() - Checking protection flags...');
        console.log('  window.gtagLoaded:', window.gtagLoaded);
        console.log('  window.gtag:', typeof window.gtag !== 'undefined' ? 'defined' : 'undefined');
        const gaScript = document.querySelector('[src*="googletagmanager"]');
        console.log('  GA script in DOM:', !!gaScript);
        
        // Protezione multipla contro doppi load
        if (window.gtagLoaded || window.gtag || gaScript) { 
            console.log('⚠️  GA ALREADY LOADED - Skipping double load');
            return; 
        }
        
        console.log('🚀 GA NOT FOUND - Creating and loading gtag script for ID:', this.config.analyticsId);
        window.gtagLoaded = true; // Flag per evitare carichi doppi
        console.log('✏️  Set window.gtagLoaded = true');
        const script = document.createElement('script');
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${this.config.analyticsId}`;
        console.log('📝 Script src:', script.src);
        document.head.appendChild(script);
        console.log('✅ Script appended to head');
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);} window.gtag = gtag;
        gtag('js', new Date());
        gtag('config', this.config.analyticsId, { 'anonymize_ip': true, 'cookie_flags': 'SameSite=None;Secure' });
        console.log('✅ gtag() initialized and configured with ID:', this.config.analyticsId);
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

// DEBUG FUNCTION: Globale per diagnostica manuale
window.debugCookieManager = function() {
    console.log('\n====== COOKIE MANAGER DEBUG ======\n');
    
    // 1. Raw cookie value
    const rawCookie = cookieManager.getCookie('cookie-consent');
    console.log('1️⃣  Raw cookie value:', rawCookie);
    
    // 2. Parsed consent
    let parsed = null;
    if (rawCookie) {
        try {
            parsed = JSON.parse(rawCookie);
            console.log('2️⃣  Parsed consent:', parsed);
            console.log('    consent.analytics:', parsed.analytics);
        } catch (e) {
            console.error('2️⃣  Parse error:', e.message);
        }
    } else {
        console.log('2️⃣  No cookie saved');
    }
    
    // 3. GA stato
    console.log('\n3️⃣  GA Status:');
    console.log('    window.gtagLoaded:', window.gtagLoaded);
    console.log('    window.gtag exists:', typeof window.gtag !== 'undefined');
    const gaScript = document.querySelector('script[src*="googletagmanager.com/gtag"]');
    console.log('    GA script in DOM:', !!gaScript, gaScript ? '(src: ' + gaScript.src + ')' : '');
    
    // 4. Decision logic
    console.log('\n4️⃣  Decision Logic:');
    if (!parsed) {
        console.log('    ❌ Consenso NON salvato → GA non dovrebbe caricare');
    } else if (parsed.analytics === true) {
        console.log('    ✅ Analytics ACCEPTED → GA dovrebbe essere attivo');
        if (typeof window.gtag !== 'undefined' && gaScript) {
            console.log('    ✅✅ BUONO: GA è effettivamente caricato');
        } else {
            console.log('    ❌ PROBLEMA: Analytics accettato ma GA NON caricato!');
        }
    } else if (parsed.analytics === false) {
        console.log('    ⛔ Analytics REJECTED → GA non dovrebbe caricare');
        if (typeof window.gtag === 'undefined' && !gaScript) {
            console.log('    ✅ BUONO: GA corettamente non caricato');
        } else {
            console.log('    ❌ PROBLEMA: Analytics rifiutato ma GA è caricato!');
        }
    }
    
    // 5. Google Analytics ID
    console.log('\n5️⃣  GA Configuration:');
    console.log('    Configured ID: ' + cookieManager.config.analyticsId);
    
    console.log('\n====== END DEBUG ======\n');
};

if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', () => cookieManager.init()); } else { cookieManager.init(); }
window.cookieManager = cookieManager;
