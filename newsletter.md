---
layout: page
title: Newsletter
description: Iscriviti alla newsletter di Messy Mind per ricevere contenuti esclusivi, articoli in anteprima e riflessioni senza fuffa direttamente nella tua inbox.
permalink: /newsletter/
image: /img/og-default.jpg
noindex: false
sitemap: true
---

# Newsletter Messy Mind

Ricevi i migliori contenuti direttamente nella tua inbox. Niente spam, solo valore.

## Cosa riceverai

- **Articoli in anteprima** prima della pubblicazione sul sito
- **Contenuti esclusivi** disponibili solo per gli iscritti
- **Riflessioni settimanali** su mindfulness, crescita personale e filosofia pratica
- **Strumenti pratici** per navigare il caos quotidiano

## Frequenza

Una email a settimana, ogni domenica mattina. Puoi annullare l'iscrizione in qualsiasi momento.

---

<div class="newsletter-form bg-light p-4 rounded">
  <h3 class="h4 mb-4">Iscriviti ora</h3>
  
  <!-- TODO: Integrare form newsletter (Mailchimp, ConvertKit, Buttondown, ecc.) -->
  <p class="text-muted mb-3">
    <strong>Form in configurazione.</strong> Nel frattempo puoi contattarci via email a 
    <a href="mailto:{{ site.email }}">{{ site.email }}</a> per iscriverti manualmente.
  </p>
  
  <form action="#" method="post" class="newsletter-signup">
    <div class="mb-3">
      <label for="email" class="form-label">Email</label>
      <input 
        type="email" 
        class="form-control" 
        id="email" 
        name="email" 
        placeholder="tua@email.it" 
        required
        aria-describedby="emailHelp">
      <div id="emailHelp" class="form-text">Non condivideremo mai la tua email con terzi.</div>
    </div>
    
    <div class="mb-3 form-check">
      <input 
        type="checkbox" 
        class="form-check-input" 
        id="privacy" 
        name="privacy" 
        required>
      <label class="form-check-label" for="privacy">
        Accetto la <a href="{{ '/privacy-policy' | relative_url }}" target="_blank">Privacy Policy</a>
      </label>
    </div>
    
    <button 
      type="submit" 
      class="btn btn-primary btn-lg w-100"
      data-analytics-id="newsletter-form-submit">
      Iscriviti gratuitamente
    </button>
  </form>
</div>

---

## Privacy e sicurezza

I tuoi dati sono al sicuro. Usiamo provider certificati GDPR e non condividiamo mai le tue informazioni con terze parti. Puoi consultare la nostra [Privacy Policy]({{ '/privacy-policy' | relative_url }}) per maggiori dettagli.
