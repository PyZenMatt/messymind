# 🔍 Cookie Manager & GA4 - Debug Guide

**Ultimo update**: 24 Mar 2026  
**Status**: ✅ Diagnostica Completa Implementata

---

## 🎯 Quick Test - 3 Minuti

### Step 1: Apri Incognito + Console
```
Ctrl+Shift+N/N (new incognito window)
Vai a: https://messymind.it
Premi: F12 (apri Developer Console)
```

### Step 2: Guarda Console BEFORE Click

Dovresti vedere questa sequenza:
```
⏱️  INIT → checking existing consent flow
🍪 Cookie Manager initializing...
🔎 checkExistingConsent() called
📋 Raw cookie value: null
⚠️  No existing consent found - banner will show
🍪 Cookie Manager initialized
```

**Ce devrebbe essere**: NESSUN GA caricato prima del click

---

### Step 3: Clicca "Accetta tutti"

Dovresti vedere:

#### 3a. Console sequence (in ordine):
```
════════ APPLY CONSENT CALLED ════════
Received consent object: {"essential":true,"analytics":true,"timestamp":...}
consent.analytics value: true
typeof consent.analytics: boolean
→ DECISION: Should LOAD GA
════════════════════════════════════════════════════════════ (divider line)

🚀 LOAD GA CALLED
📋 loadGoogleAnalytics() - Checking protection flags...
  window.gtagLoaded: false
  window.gtag: undefined
  GA script in DOM: false

🚀 GA NOT FOUND - Creating and loading gtag script for ID: G-YZRF8LG3GD
✏️  Set window.gtagLoaded = true
📝 Script src: https://www.googletagmanager.com/gtag/js?id=G-YZRF8LG3GD
✅ Script appended to head
✅ gtag() initialized and configured with ID: G-YZRF8LG3GD
```

**Critical checks**:
- ✅ `consent.analytics value: true`
- ✅ `GA NOT FOUND` (non `GA ALREADY LOADED`)
- ✅ gtag script ID corretto: `G-YZRF8LG3GD`
- ✅ Two lines: setup AND configuration

---

### Step 4: Debug Manuale (Se Problema)

In console, digita:
```javascript
debugCookieManager()
```

Vedi output come questo:
```
====== COOKIE MANAGER DEBUG ======

1️⃣  Raw cookie value: {"essential":true,"analytics":true,"timestamp":1711270801234,"version":"1.0"}

2️⃣  Parsed consent: {essential: true, analytics: true, timestamp: 1711270801234, version: '1.0'}
    consent.analytics: true

3️⃣  GA Status:
    window.gtagLoaded: true
    window.gtag exists: true
    GA script in DOM: true (src: https://www.googletagmanager.com/gtag/js?id=G-YZRF8LG3GD)

4️⃣  Decision Logic:
    ✅ Analytics ACCEPTED → GA dovrebbe essere attivo
    ✅✅ BUONO: GA è effettivamente caricato

5️⃣  GA Configuration:
    Configured ID: G-YZRF8LG3GD

====== END DEBUG ======
```

---

## 🚨 Problema? Leggi Qui

### ❌ "Dopo click, vedo `GA NOT FOUND`... ma poi niente"

**Cattura console COMPLETA** (tutti i log dopo `GA NOT FOUND`)

Possibili rotture:
1. Script non appended a `<head>` → controlla `document.head` nel debugger
2. gtag() fallisce → controlla errore rosso in console
3. ID GA errato → controlla output `debugCookieManager()` → punto 5️⃣

---

### ❌ "Vedo 2+ volte `GA NOT FOUND`"

Doppio load! Cerca `debugCookieManager()`:
- Se `window.gtagLoaded: true` ma vedi 2x `GA NOT FOUND`, significa il flag non viene rispettato
- Potrebbe essere una race condition

---

### ❌ "Consent salvato ma `GA ALREADY LOADED` subito"

Ricarica pagina → se `debugCookieManager()` mostra `GA script in DOM: true` PRIMA di click:
- ❌ GA è stato pre-caricato (ERRORE GDPR)
- Controlla che `google-analytics.html` NON ha `<script>` senza `defer`

---

### ❌ "GA caricato ma GA4 Realtime = 0 utenti"

1. ID corretto? → `debugCookieManager()` → punto 5️⃣
2. Network OK? → F12 → Network tab → filtra `gtag.js` → vedi 200 OK?
3. Wait 10s → GA Realtime ha lag
4. Incognito? → no cache di GA

---

## 📊 Output Atteso per Ogni Scenario

### Scenario 1: Nuovo utente, nessun consenso, niente click
```
✅ Aspettazioni:
- Init logs OK
- Raw cookie: null
- No GA in DOM
- Banner visible

❌ Problemi se:
- Vedi GA script nel DOM
- window.gtag è definito
```

### Scenario 2: Utente ACCETTA
```
✅ Aspettazioni:
- APPLY CONSENT CALLED
- consent.analytics: true
- LOAD GA CALLED (SOLO UNA VOLTA)
- GA script in DOM dopo
- window.gtagLoaded: true

❌ Problemi se:
- LOAD GA CALLED 2+ volte
- console error rosso
- gtag() undefined dopo init
```

### Scenario 3: Utente RIFIUTA
```
✅ Aspettazioni:
- APPLY CONSENT CALLED
- consent.analytics: false
- DECISION: Should NOT load GA
- GA script NON nel DOM
- window.gtag: undefined

❌ Problemi se:
- GA script nel DOM still
- window.gtag definito
```

---

## 🔧 Come Comunicare il Problema

Se GA non funziona, inviami:

1. **Output completo console** (da quando apri la pagina a dopo click)
2. **Risultato di**:
   ```javascript
   debugCookieManager()
   ```
3. **Screenshot GA4 Realtime** (Utenti: 0 o 1?)
4. **Risposta a**: Il problema è in quale sezione?
   ```
   A) [ ] INIT (nessun consenso)
   B) [ ] CLICK (dopo click, niente accade)
   C) [ ] GA REALTIME (caricato ma GA4 = 0)
   D) [ ] Doppio tracking
   ```

---

## 📝 Checklist Prima di Deploy

- [ ] `INIT → checking existing consent flow` présent? (sì = OK)
- [ ] Clicca accept → Vedi `APPLY CONSENT CALLED`? (sì = OK)
- [ ] Clicca accept → Vedi `LOAD GA CALLED` ESATTAMENTE 1 VOLTA? (sì = OK)
- [ ] Con `debugCookieManager()` vedi `✅✅ BUONO: GA è effettivamente caricato`? (sì = OK)
- [ ] Apri GA4 Realtime → 1 utente entro 10s? (sì = OK)

---

## 🚀 Rimozione Debug (Quando Funziona)

Quando tutto ok, rimuovere debug per production:

```bash
# Remove all console.log lines
git checkout HEAD -- _includes/cookie-manager.js assets/js/cookie-manager.js

# Verifica che debugCookieManager è rimosso
grep -n "debugCookieManager" _includes/cookie-manager.js
```

Ma per ora **TIENI IL DEBUG ATTIVO** finché non vedi:
✅ GA4 Realtime = 1 utente

---

**Nota**: `window.debugCookieManager()` rimane globale anche dopo deploy (removibile quando pronto)

