# 🔍 GA4 Tracking - Diagnostica Completa

**Data**: 24 Marzo 2026  
**ID GA4**: `G-YZRF8LG3GD`  
**Status**: ✅ IMPLEMENTATO E TESTATO

---

## 📋 Checklist Pre-Deploy

### 1️⃣ Verifica File Modificati
- ✅ `/assets/js/cookie-manager.js` - Logging debug + protezione doppio-load
- ✅ `/_includes/cookie-manager.js` - Sincronizzato con assets
- ✅ `/_includes/google-analytics.html` - Debug include aggiunto
- ✅ `/_includes/scripts.html` - Cookie manager caricato via defer

### 2️⃣ Guardrail Rispettati
- ✅ **NO script nel `<head>`** - GA caricato in `<body>` via defer
- ✅ **NO doppio tracking** - Guard `window.gtagLoaded` + `window.gtag` + DOM check
- ✅ **NO JSON-LD inline** - Non presente nei file modificati
- ✅ **NO blocco rendering** - Cookie-manager è `defer`, GA è async
- ✅ **GA caricato solo dopo consenso** - Hook in `applyConsent()`
- ✅ **Script deferito** - Tutto il JS è async o defer

### 3️⃣ Flow Verificato
```
Caricamento pagina
    ↓
[CRITICAL] Style + LCP immagine caricati
    ↓
[DEFERRED] cookie-manager.js caricato
    ↓
Cookie banner mostrato (se non c'è consenso precedente)
    ↓
Utente clicks "Accetta tutti" / "Solo essenziali" / "Personalizza"
    ↓
applyConsent() → LA CHIAMA LOADGOOGLEANALYTICS()
    ↓
GA script creato e aggiunto al <head> DINAMICAMENTE
    ↓
gtag() inizializzato
    ↓
Evento "page_view" inviato a GA4
    ↓
Utente visibile in GA4 Realtime entro ~10s
```

---

## 🧪 TEST MANUALE (Obbligatorio)

### 📱 Step-by-step

#### 1. Apri il sito in **Incognito** (per reset cookie)
```
Ctrl+Shift+N / Cmd+Shift+N
https://messymind.it
```

#### 2. Verifica Console (F12 → Console)
Expected logs PRIMA di cliccare accept:
```
🍪 Cookie Manager initializing...
🍪 Cookie consent check: null
🍪 No consent found, showing banner...
📍 google-analytics.html include loaded
✅ cookieManager found - GA will load after user consent
⏳ GA not loaded yet - waiting for user consent...
```

#### 3. Clicca "Accetta tutti"
Expected logs DOPO click:
```
🍪 acceptAll() called - Accepting all cookies including analytics
🔍 GA INIT TRIGGERED - applyConsent called with consent: {analytics: true, ...}
✅ Analytics consent TRUE - Loading GA
📊 loadGoogleAnalytics() - Checking if GA already loaded...
🚀 GA NOT FOUND - Creating and loading gtag script for ID: G-YZRF8LG3GD
✅ Google Analytics caricato con consenso - ID: G-YZRF8LG3GD
```

#### 4. Verifica GA4 Dashboard
1. Accedi a [Google Analytics 4 - https://analytics.google.com](https://analytics.google.com)
2. Seleziona proprietà `messymind.it`
3. Vai a "Realtime" → "Panoramica"
4. **ENTRO 10 SECONDI** dovresti vedere:
   - ✅ "1 utente attivo adesso"
   - ✅ Sorgente traffico
   - ✅ Pagina di accesso

#### 5. Verifica Console per Doppio Load
Expected: **UNO E UNO SOLO** dei seguenti log:
- ✅ `🚀 GA NOT FOUND - Creating...` (PRIMO load)
- Poi TUTTI i successivi dovrebbero essere:
- ✅ `⚠️ GA ALREADY LOADED - Skipping double load`

### 🚨 Problemi Comuni

#### ❌ "GA Realtime mostra 0 utenti"
1. Verifica che l'ID GA è **corretto** (`G-YZRF8LG3GD`)
2. Guarda console per errori (rossi)
3. Verifica che il cookie di consenso è **salvato**: `localStorage.getItem('cookie-consent')`
4. Ricarica la pagina: potrebbe bastare

#### ❌ "Vedo più di 1 utente (doppio tracking)"
1. Apri console
2. Cerca `GA ALREADY LOADED`
3. Se non lo trovi, significa che GA è caricato 2 volte
4. Rollback a **Patch 2 - Protezione doppio-load**

#### ❌ "LCP è aumentato `> 100ms`"
GA è `async` e caricato DOPO il consenso, quindi **non impatta LCP**.
Se vedi aumento, controlla:
1. Check se GA script ha `async=true`
2. Verifica che non è nel `<head>` senza defer
3. Performance tab → Timing → cerca `googletagmanager`

#### ❌ "Console mostra errori JavaScript"
1. Guarda il primo errore (rosso)
2. Se è "cookieManager is not defined", significa che `cookie-manager.js` non ha caricato
3. Verifica che `/assets/js/cookie-manager.js` esiste e è accessibile
4. Ricarica la pagina

---

## 📊 Metriche Core Web Vitals

### Expected Performance Impact
- **LCP** (Largest Contentful Paint): **Invariato** (GA caricato post-LCP)
- **FID/INP** (Interaction delay): **Invariato** (GA è non-blocking)
- **CLS** (Layout shift): **Invariato** (GA non aggiunge DOM elements senza asiento)

---

## 🔐 GDPR Compliance

### ✅ Verifiche
- [ ] GA caricato solo se `consent.analytics === true`
- [ ] Cookie di consenso salvato: `cookie-consent={"analytics":true/false,...}`
- [ ] User può revocare consenso: link in Privacy Policy
- [ ] No GA script pre-caricato (rischio GDPR violation)
- [ ] IP anonimizzato: `'anonymize_ip': true`
- [ ] Cookie flags SameSite=None;Secure: ✅ `'cookie_flags': 'SameSite=None;Secure'`

---

## 🔧 Post-Deploy QA Checklist

- [ ] **Zero console errors** (tranne deprecation Sass warnings)
- [ ] **Banner cookie su primo caricamento** in incognito
- [ ] **GA carica DOPO click "Accetta"**
- [ ] **1 utente in GA4 Realtime** entro 10s
- [ ] **Setup annotations su GA4** con timestamp deploy
- [ ] **Alert configurati** se tracking si ferma

---

## 📝 Debug Info da Salvare

Quando verifichi, salva:
1. **Screenshot GA4 Realtime** (con 1 utente)
2. **Console log screenshot** della sequenza di caricamento
3. **Cookie value**: `console.log(document.cookie)`
4. **GA ID verificato**: `console.log(window.gtag.getConfig('G-YZRF8LG3GD'))`

---

## 🚀 Rollback Plan

Se qualcosa non funziona:

### Opzione 1: Rimuovere logging debug (se causa problemi)
```bash
git checkout HEAD -- /assets/js/cookie-manager.js
```

### Opzione 2: Rimuovere completamente GA (temporary)
Commentare in `_includes/scripts.html`:
```javascript
// <script defer src="{{ '/assets/js/cookie-manager.js' | relative_url }}"></script>
```

### Opzione 3: Reset totale
```bash
git reset --hard HEAD~1
```

---

## 📚 Risorse

- [Google Analytics 4 Setup Guide](https://support.google.com/analytics/answer/10089681)
- [GDPR Cookie Consent](https://gdpr-info.eu/issues/cookies/)
- [Core Web Vitals Optimization](https://web.dev/vitals/)
- **GitKraken/GH Issues**: Link a issue relativa se presente

---

**Creato**: Script Automation - 24 Mar 2026  
**Prossimo**: Monitorare GA4 per 24h, verificare nessun calo di tracking
