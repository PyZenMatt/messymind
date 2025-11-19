# Google Analytics 4 - Architettura MessyMind

## 📊 Overview

MessyMind utilizza Google Analytics 4 (GA4) con un'implementazione **GDPR-compliant** che carica il tracking solo dopo il consenso esplicito dell'utente.

**Measurement ID**: `G-MLB32YW721`  
**Property ID**: 498950157 (da verificare in Google Analytics)

---

## 🏗️ Architettura

### Flusso di Caricamento

```
Utente visita il sito
         ↓
Banner cookie appare (se non già accettato)
         ↓
Utente accetta cookie analytics
         ↓
cookie-manager.js carica dinamicamente gtag.js
         ↓
GA4 inizializzato con G-MLB32YW721
         ↓
Eventi tracking iniziano
```

### Componenti Principali

#### 1. Configurazione (_config.yml)
```yaml
google_analytics: "G-MLB32YW721"
```

Jekyll usa questa variabile per iniettare l'ID nel template Liquid.

#### 2. Cookie Manager (_includes/cookie-manager.js)
Template Liquid che viene processato da Jekyll:
- Legge `{{ site.google_analytics }}`
- Gestisce consenso cookie
- Carica GA4 dinamicamente solo dopo consenso
- Include protezioni anti-duplicazione

#### 3. Cookie Manager Static (assets/js/cookie-manager.js)
Versione statica con fallback hardcoded:
- Usata come backup
- ⚠️ **Deve essere mantenuta sincronizzata** con _includes/cookie-manager.js

#### 4. Cookie Banner (_includes/cookie-banner.html)
- UI per richiedere consenso
- Tre opzioni: Accetta tutto, Rifiuta, Personalizza
- Persistenza consenso: 365 giorni

#### 5. Layout Integration
- `_layouts/default.html` include `google-analytics.html`
- `google-analytics.html` è solo un commento/placeholder
- Script effettivo caricato da `_includes/scripts.html` via `cookie-manager.js`

---

## 🔒 Conformità GDPR

### Caratteristiche
✅ **Consenso esplicito**: Richiesto prima del caricamento  
✅ **Anonimizzazione IP**: `anonymize_ip: true`  
✅ **Cookie sicuri**: `SameSite=None;Secure`  
✅ **Revoca consenso**: Disponibile via link "Gestisci preferenze cookie"  
✅ **Pulizia dati**: Rimuove cookie GA4 alla revoca  

### Cookie Utilizzati
- `cookie-consent`: Memorizza preferenze utente (365 giorni)
- `_ga`: Google Analytics (dopo consenso)
- `_gid`: Google Analytics (dopo consenso)
- `_ga_*`: Google Analytics stream-specific (dopo consenso)

---

## 🛠️ Come Modificare il Measurement ID

### 1. Aggiornare la Configurazione
Modifica `_config.yml`:
```yaml
google_analytics: "G-NUOVOID123"
```

### 2. Aggiornare il Fallback Statico
Modifica `assets/js/cookie-manager.js`:
```javascript
analyticsId: (function(){ 
    try { 
        return (typeof SITE_GOOGLE_ANALYTICS !== 'undefined') 
            ? SITE_GOOGLE_ANALYTICS 
            : 'G-NUOVOID123';  // ← Cambia qui
    } catch(e){ 
        return 'G-NUOVOID123';  // ← E qui
    } 
})()
```

### 3. Rebuild del Sito
```bash
bundle exec jekyll build
```

### 4. Test
Vedi sezione "Testing" più sotto.

---

## 🧪 Testing

### Test Locale
1. **Build del sito**:
   ```bash
   bundle exec jekyll serve
   ```

2. **Verifica nel browser**:
   - Apri http://localhost:4000
   - Apri DevTools (F12)
   - Verifica comparsa banner cookie
   - Accetta cookie analytics

3. **Verifica caricamento GA4**:
   - DevTools → Network
   - Filtra: `googletagmanager.com`
   - Verifica chiamata a `gtag/js?id=G-MLB32YW721`

4. **Verifica inizializzazione**:
   - DevTools → Console
   - Digita: `window.gtag`
   - Dovrebbe essere una funzione (non undefined)

5. **Verifica cookie**:
   - DevTools → Application → Cookies
   - Verifica presenza: `_ga`, `_gid`, `_ga_*`

### Test Produzione
1. **Visita il sito live**: https://messymind.it
2. **Ripeti i test sopra**
3. **Verifica Real-Time in GA4**:
   - Apri Google Analytics
   - Vai su Reports → Real-time
   - Verifica che la tua visita appaia

---

## 🐛 Troubleshooting

### GA4 non si carica
**Sintomo**: Nessuna chiamata a googletagmanager.com nel Network tab

**Possibili cause**:
1. ❌ Cookie non accettati
   - Soluzione: Accetta i cookie analytics dal banner
2. ❌ AdBlocker attivo
   - Soluzione: Disabilita l'adblocker per il test
3. ❌ Script bloccato da Content Security Policy
   - Soluzione: Verifica CSP headers
4. ❌ JavaScript disabilitato
   - Soluzione: Abilita JavaScript nel browser

### Duplicazione Eventi
**Sintomo**: Eventi tracciati due volte in GA4

**Possibili cause**:
1. ❌ GA4 caricato due volte
   - Soluzione: Verifica con `grep -r "G-MLB32YW721" _site/`
2. ❌ Altra implementazione GA4 presente
   - Soluzione: Cerca altri tag analytics nel codice

### Measurement ID Errato
**Sintomo**: Eventi non appaiono nella property corretta

**Verifica**:
```bash
# Cerca tutti i Measurement ID nel progetto
grep -r "G-[A-Z0-9]\{10\}" . --exclude-dir=node_modules --exclude-dir=.git
```

---

## 📚 Riferimenti

### File Chiave
- `_config.yml`: Configurazione Measurement ID
- `_includes/cookie-manager.js`: Logica principale (template Liquid)
- `assets/js/cookie-manager.js`: Versione statica (fallback)
- `_includes/cookie-banner.html`: UI banner consenso
- `_includes/google-analytics.html`: Placeholder (solo commento)
- `_layouts/default.html`: Include google-analytics.html

### Documentazione Esterna
- [Google Analytics 4 - Guida Ufficiale](https://support.google.com/analytics/answer/10089681)
- [GA4 Measurement ID](https://support.google.com/analytics/answer/12270356)
- [GDPR e Google Analytics](https://support.google.com/analytics/answer/9019185)

### Documentazione Interna
- `docs/GA4_AUDIT_REPORT_2025-11-19.md`: Audit completo

---

## ✅ Checklist Manutenzione

### Mensile
- [ ] Verifica funzionamento GA4 su produzione
- [ ] Controlla report Real-Time in Google Analytics
- [ ] Verifica che banner cookie appaia per nuovi utenti

### Annuale
- [ ] Verifica scadenza cookie consent (365 giorni)
- [ ] Review conformità GDPR/normative privacy
- [ ] Audit duplicati GA4 (come questo)

### Ad Ogni Modifica
- [ ] Sincronizza `_includes/cookie-manager.js` e `assets/js/cookie-manager.js`
- [ ] Test su locale prima del deploy
- [ ] Verifica build Jekyll senza errori
- [ ] Test su produzione dopo deploy

---

**Ultimo Aggiornamento**: 2025-11-19  
**Versione**: 1.0
