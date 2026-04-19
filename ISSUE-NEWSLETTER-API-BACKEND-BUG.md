# [Bug] API Newsletter Subscriber — HTTP 500 Internal Server Error

## Overview

L'endpoint `POST /api/contact/newsletter/subscribe/` restituisce un **HTTP 500 Internal Server Error** senza dettagli utili. L'endpoint è stato implementato ma non funziona in produzione.

## Context

- **Frontend**: ✅ Integrato e testato (Jekyll messymind.it)
- **Backend**: ❌ Endpoint restituisce 500
- **Status**: Bloccante per il deployment del form

## Reproduction Steps

```bash
curl -X POST https://pyzenmatt.pythonanywhere.com/api/contact/newsletter/subscribe/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "source": "homepage",
    "newsletter_type": "main"
  }'
```

**Response:**
```
HTTP/1.1 500 Internal Server Error
Content-Type: text/html; charset=utf-8

<!doctype html>
<html lang="en">
<head>
  <title>Server Error (500)</title>
</head>
<body>
  <h1>Server Error (500)</h1><p></p>
</body>
</html>
```

## Expected Behavior

**Success (200 OK)**:
```json
{
  "success": true,
  "message": "Iscrizione confermata",
  "id": 123
}
```

**Error (400/409)**:
```json
{
  "success": false,
  "error": "Email já iscritta | Email non valida | Errore server"
}
```

## Actual Behavior

Generic 500 error con nessun messaggio di diagnostica:
```
HTTP/1.1 500 Internal Server Error
<h1>Server Error (500)</h1><p></p>
```

## Technical Information

### What We Know ✅
- Richiesta arriva al server correttamente
- CORS preflight funziona
- Rete e SSL OK (4504ms per processare la richiesta)
- Frontend manda i dati corretti

### What We Don't Know ❌
- Quale exception esattamente sta sollevando
- Se è un problema di modello, database, validazione o import
- Se il codice è stato deployato correttamente

## Possible Causes

1. **Exception nel modello NewsletterSubscriber**
   - Errore di save() nel database
   - Constraint violato
   - Campo mancante

2. **Database issue**
   - Tabella non migrate
   - Constraint non creato
   - Connection error

3. **Import/Configuration**
   - Modello non importato nel view
   - Serializer non configurato
   - URL pattern mancante

4. **Email sending** (se implementato)
   - Provider email non configurato
   - Credential mancanti
   - SMTP timeout

5. **Rate limiting**
   - Libreria rate limiting non importata
   - Decorator non applicato

## Debugging Checklist

- [ ] Controllare error log su PythonAnywhere
- [ ] Aggiungere try/except con logging
- [ ] Abilitare DEBUG=True temporaneamente (solo dev)
- [ ] Verificare che la tabella NewsletterSubscriber esista
- [ ] Verificare le migrations sono applicate
- [ ] Test diretto con `python manage.py shell`
- [ ] Verificare CORS headers in risposta
- [ ] Check if email backend is configured
- [ ] Verify rate_limiting decorator syntax

## Proposed Solution

### Step 1: Enable Logging
```python
# In view or settings
import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@csrf_exempt
def newsletter_subscribe(request):
    try:
        # ... codice ...
    except Exception as e:
        logger.exception("Newsletter subscribe error")  # Cattura stack trace completo
        return Response({
            'success': False, 
            'error': 'Errore server'
        }, status=500)
```

### Step 2: Check Logs
- PythonAnywhere Web app → Logs → Error log
- Django logs in file system
- Stderr output

### Step 3: Verify Database
```bash
python manage.py dbshell
SELECT * FROM contact_newslettersubscriber LIMIT 1;
```

### Step 4: Test in Shell
```bash
python manage.py shell
>>> from contact.models import NewsletterSubscriber
>>> obj = NewsletterSubscriber.objects.create(
    email='test@example.com',
    source='homepage'
)
>>> print(obj.id)
```

## Links

- **API Docs**: [docs/API_NEWSLETTER.md](https://github.com/PyZenMatt/blogmanager/blob/main/docs/API_NEWSLETTER.md)
- **Backend Repo**: https://github.com/PyZenMatt/blogmanager
- **Frontend Form**: [messymind.it/_includes/newsletter-form.html](https://github.com/PyZenMatt/messymind.it/blob/main/_includes/newsletter-form.html)
- **Endpoint**: POST `/api/contact/newsletter/subscribe/`

## Timeline

- 🔴 **Priority**: CRITICAL (blocca deployment)
- 📅 **Estimated**: 1-2 ore per debug
- ⏰ **Urgency**: Fix immediately

## Definition of Done

- [x] Exception loggata e traceback disponibile
- [x] Root cause identificato
- [x] Fix implementato e testato
- [x] Endpoint restituisce 200/400 appropriatamente
- [x] Email di iscrizione ricevuta (se implementato)
- [x] Deployment su produzione
- [x] Test con curl verificato
- [x] Frontend form funziona end-to-end

## Labels

`backend` `api` `bug` `newsletter` `critical` `python` `django`

## Notes

- **Non modificare il frontend** — è già pronto, il problema è 100% backend
- **Temporaneo**: Disabilitare email confirmation se causano l'errore (Phase 2)
- **Veloce**: Se è un problema di migrations, basta `python manage.py migrate`
- **Check**: Assicurarsi che il modello `NewsletterSubscriber` sia stato committato

---

**Next Steps:**
1. Accedi a PythonAnywhere error log
2. Condividi il traceback completo
3. Verifica che la migration sia stata applicata
4. Test con Python shell
