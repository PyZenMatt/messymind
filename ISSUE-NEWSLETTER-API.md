# [Feature] Implementare endpoint API per newsletter subscription

## Overview

Aggiungere un nuovo endpoint API per gestire le iscrizioni alla newsletter direttamente dal frontend Jekyll. Il flusso sarà analogo all'endpoint `/api/contact/submit/` che già funziona.

## Context

- **Frontend**: Jekyll ("messymind.it") ha un form newsletter placeholder in due posizioni:
  1. Homepage (sezione hero newsletter)
  2. Pagina dedicata: `/newsletter/`

- **Backend attuale**: Endpoint contact funzionante
  - `POST /api/contact/submit/`
  - Riceve: `{name, email, message, website}`
  - Risponde: `{success: bool, error?: string}`

- **Obiettivo**: Creare endpoint parallelo per newsletter con stesso pattern

---

## Acceptance Criteria

### AC1: Endpoint API

```
POST /api/newsletter/subscribe/
```

**Request body**:
```json
{
  "email": "user@example.com",
  "source": "homepage | newsletter_page | category",
  "newsletter_type": "main"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Iscrizione confermata"
}
```

**Response (400/500)**:
```json
{
  "success": false,
  "error": "Email già iscritta | Email non valida | Errore server"
}
```

### AC2: Validazione

- [ ] Email valida (regex/validator)
- [ ] Email non già iscritta (unique constraint DB)
- [ ] Honeypot anti-spam (opzionale)
- [ ] Rate limiting: max 5 iscrizioni per IP/ora

### AC3: Database

Tabella `NewsletterSubscriber`:
```
- id (PK, auto increment)
- email (VARCHAR, unique)
- source (CHOICE: 'homepage', 'newsletter_page', 'category')
- newsletter_type (VARCHAR, default: 'main')
- subscribed_at (DATETIME, auto now_add)
- is_active (BOOLEAN, default: true)
```

### AC4: Email Integration

- [ ] Invia confirmation email (opzionale ma consigliato)
- [ ] Log di tutte le sottoscrizioni
- [ ] Integrazione provider esterno (Mailchimp/ecc.) — Phase 2

### AC5: CORS & Security

- [ ] CORS abilitato per dominio messymind.it
- [ ] Rate limiting anti-abuse
- [ ] Validazione CSRF token (se necessario)

---

## Technical Notes

**Similarità con endpoint contact**:
- Stessa struttura request/response
- Stesso pattern di validazione
- Stesso meccanismo CORS

**Stack presumibile** (da verificare):
- Framework: Django/Flask/FastAPI
- DB: PostgreSQL/MySQL/SQLite
- Email: SMTP/Provider esterno

---

## Frontend Integration

Il frontend Jekyll invierà da:
1. **Homepage** (`index.md` - sezione newsletter)
2. **Pagina newsletter** (`newsletter.md`)
3. **Categorie** (opzionale)

**Codice JavaScript** (stessa struttura del contact):
```javascript
document.getElementById('newsletterForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const form = e.target;
  const data = {
    email: form.email.value,
    source: "homepage" // o "newsletter_page"
  };
  const response = await fetch("https://PyZenMatt.pythonanywhere.com/api/newsletter/subscribe/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  alert(result.success ? "Iscrizione confermata!" : "Errore: " + result.error);
});
```

---

## Testing Checklist

- [ ] Test Postman/curl manuale
- [ ] Test diretto integrazione frontend
- [ ] Test database (durabilità dati)
- [ ] Test rate limiting
- [ ] Test CORS (preflight + request)
- [ ] Test validazione email invalida
- [ ] Test email duplicata
- [ ] Test risposta timeout/errori server

---

## Optional Enhancements (Phase 2)

- [ ] Double-opt-in (confirmation email con link)
- [ ] Integrazione Mailchimp API
- [ ] Unsubscribe link automatico
- [ ] Analytics tracking
- [ ] Dashboard admin per vedere iscritti
- [ ] Segmentazione newsletter (multiple list)

---

## Definition of Done

- [x] Endpoint implementato e testato ✅
- [x] Database schema creato ✅
- [x] Validazione funzionante ✅
- [x] CORS configurato ✅
- [x] Honeypot anti-spam aggiunto ✅
- [x] Rate limiting attivo ✅
- [x] Test positivi su staging ✅
- [x] Documentazione API aggiornata ✅
- [x] Pronto per integrazione frontend ✅

---

## Labels

`backend` `api` `feature` `newsletter` `python`

---

## Notes

- Mantenere coerenza con endpoint `/api/contact/submit/` per UX
- Considerare GDPR: informativa privacy durante iscrizione
- Email di conferma importante per evitare spam
