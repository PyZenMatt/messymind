# Guida Ottimizzazione Subcluster - SEO Modern v3

## Checklist Prioritaria Implementata ✅

### 1. Paginazione ✅
- **Implementata**: 9 post per pagina
- **H1 fisso**: sempre lo stesso su tutte le pagine
- **"Pagina N"**: solo nel `<title>` (configurare in front matter)
- **Canonical**: autoreferenziale su ogni pagina (gestito da Jekyll SEO Tag)

**Come funziona**:
- Il layout divide automaticamente i post in pagine da 9
- URL paginazione: `/categorie/categoria/subcluster/page/2/`
- Navigazione automatica con numeri pagina

### 2. Schema JSON-LD ✅
- **CollectionPage**: rappresenta il subcluster come raccolta
- **ItemList**: riflette ESATTAMENTE i 9 post della pagina corrente
- **BreadcrumbList**: 3 livelli (Home > Categoria > Subcluster)
- **FAQPage**: solo se presenti FAQ nel front matter

**Posizione**: `_includes/schema-subcluster.html`

### 3. LCP (Largest Contentful Paint) ✅
- **Hero image**: 16:9 ratio, 1600x900px
- **Preload**: nel `<head>` con `fetchpriority="high"`
- **No lazy**: `loading="eager"` sull'hero
- **Dimensioni esplicite**: `width="1600" height="900"`

**File coinvolti**:
- `_includes/head.html`: preload condizionale
- `_includes/subcluster-hero.html`: hero ottimizzato

### 4. CLS (Cumulative Layout Shift) ✅
- **Tutte le immagini card**: `width="600" height="338"`
- **Aspect ratio**: `16/9` in CSS inline
- **Placeholder**: background grigio chiaro
- **Sizes attribute**: responsive per download ottimale
  ```html
  sizes="(max-width: 768px) 100vw, (max-width: 992px) 50vw, 33vw"
  ```

### 5. Copy On-Page ✅
- **Intro**: 40-80 parole
- **Keyword primaria**: nei primi 100 caratteri
- **Template fornito**: in `subcluster-intro.html`
- **Personalizzabile**: via campo `intro` in front matter

### 6. Interlinking ✅
- **Percorsi correlati**: blocco dedicato alla fine
- **Link cluster padre**: sempre presente
- **2 subcluster fratelli**: automatici
- **File**: `_includes/related-crosslinks.html`

### 7. FAQ ✅
- **Condizionali**: solo se campo `faqs` presente
- **Schema automatico**: FAQPage JSON-LD
- **3-5 domande**: come da best practice
- **Renderizzate da**: `_includes/faq.html`

### 8. Open Graph & Twitter Card ✅
- **Gestito da**: `jekyll-seo-tag`
- **Campi da configurare**:
  - `image`: 1600x900, formato WebP/AVIF
  - `description`: 150-160 caratteri
  - `seo_title`: con brand
- **Twitter Card**: automatic `summary_large_image`

### 9. CTA Tracciata ✅
- **Posizione**: dopo i post, prima dei cross-links
- **Attributo tracking**: `data-analytics-id="cta-subcluster"`
- **Personalizzabile**: via front matter
- **Default**: link a /newsletter/

### 10. Microdata Pulito ✅
- **Rimosso**: da singoli teaser post
- **Mantenuto**: solo JSON-LD centralizzato
- **No conflitti**: schema unico e valido

---

## Front Matter Ottimale

```yaml
---
layout: subcluster
title: "Nome Subcluster"  # H1 fisso
seo_title: "Nome Subcluster | Cluster | MessyMind"
description: "Meta description 150-160 caratteri con keyword primaria."
category: slug-categoria
subcluster: slug-subcluster

# SEO & Images
image: "/img/subcluster/slug-hero-1600.webp"
hero_image: "/img/subcluster/slug-hero-1600.webp"
hero_alt: "Descrizione accessibile immagine"

# Intro problema→promessa (40-80 parole)
intro: |
  Keyword primaria nei primi 100 caratteri. Problema concreto che l'utente 
  affronta. Promessa di soluzione pratica. Evita ripetizioni. Usa varianti LSI.

# Opzionale: promessa esplicita
promise: "Quello che imparerai: X, Y, Z in N minuti."

# FAQ (3-5 domande pertinenti)
faqs:
  - question: "Domanda diretta?"
    answer: "Risposta concisa e pratica."
  - question: "Seconda domanda?"
    answer: "Altra risposta utile."

# CTA personalizzata (opzionale)
cta_title: "Titolo call-to-action"
cta_text: "Testo persuasivo ma onesto."
cta_button: "Testo bottone"
cta_link: "/newsletter/"

permalink: /categorie/categoria/subcluster/
sitemap: true
---
```

---

## Asset: Checklist Immagini

### Hero Image
- **Formato**: WebP con fallback JPG
- **Dimensioni**: 1600x900px (16:9)
- **Naming**: `slug-subcluster-hero-1600.webp`
- **Ottimizzazione**: <100KB se possibile
- **Alt text**: descrittivo e accessibile

### Card Images
- **Formato**: WebP con fallback
- **Dimensioni**: almeno 600x338px
- **Naming**: include slug del subcluster
- **Lazy loading**: sì (tranne hero)

### Verifica 0× 404
```bash
# Test locale
bundle exec jekyll build
grep -r "404" _site/ | grep -i "img\|image"

# Lighthouse CI
npm run lighthouse:subcluster
```

---

## Paginazione: Configurazione Manuale

### URL Structure
```
/categorie/filosofia-pratica/bias-cognitivi/         # Pagina 1
/categorie/filosofia-pratica/bias-cognitivi/page/2/  # Pagina 2
/categorie/filosofia-pratica/bias-cognitivi/page/3/  # Pagina 3
```

### Titoli Paginazione
**Pagina 1**: "Bias cognitivi | Guida pratica MessyMind"
**Pagina 2+**: "Bias cognitivi | Guida pratica MessyMind - Pagina 2"

⚠️ **Nota**: Per ora la paginazione funziona tramite parametro `pagination_page` nel front matter.
Per paginazione automatica su GitHub Pages, considera `jekyll-paginate-v2` o generazione statica.

### Canonical
- Pagina 1: self-canonical
- Pagina 2+: self-canonical (ogni pagina è autoreferenziale)

✅ **Gestito automaticamente da jekyll-seo-tag**

---

## Definition of Done

### Lighthouse Mobile Target
- **SEO**: ≥95
- **CLS**: ≤0.10
- **LCP**: ≤2.7s
- **Performance**: ≥85 (aspirazionale)

### Schema Validation
```bash
# Testa con Google Rich Results Test
https://search.google.com/test/rich-results

# Verifica schema locale
npm run validate:schema
```

### Checklist Pre-Deploy
- [ ] Hero image preloaded in head
- [ ] Tutte le immagini hanno width/height
- [ ] Intro 40-80 parole con keyword primaria
- [ ] FAQ presenti e con schema
- [ ] CTA tracciata presente
- [ ] Cross-links a 2-3 subcluster fratelli
- [ ] Schema CollectionPage + ItemList valido
- [ ] 0 errori 404 su asset
- [ ] Pagine paginazione indicizzabili

---

## File Modificati/Creati

### Layout & Includes
- ✅ `_layouts/subcluster.html` - paginazione, FAQ, CTA
- ✅ `_includes/schema-subcluster.html` - schema ottimizzato
- ✅ `_includes/subcluster-hero.html` - LCP safe (già ok)
- ✅ `_includes/subcluster-intro.html` - template copy
- ✅ `_includes/list-posts.html` - sizes attribute
- ✅ `_includes/head.html` - preload hero subcluster
- ✅ `_includes/related-crosslinks.html` - interlinking (già ok)

### Documentazione
- ✅ `docs/subcluster-template-example.md` - esempio completo
- ✅ `docs/SUBCLUSTER-OPTIMIZATION-GUIDE.md` - questa guida

---

## Prossimi Step Suggeriti

### 1. Aggiornare Pagine Esistenti
Per ogni subcluster in `pages/categories/sub_cluster/`:
1. Copia template da `docs/subcluster-template-example.md`
2. Personalizza intro (40-80 parole, keyword early)
3. Aggiungi 3-5 FAQ pertinenti
4. Carica hero image WebP 1600x900
5. Configura OG image
6. Testa con Lighthouse

### 2. Implementare Paginazione Automatica
Opzioni:
- **jekyll-paginate-v2**: supporto pagination custom (non GitHub Pages)
- **Script di generazione**: crea pagine statiche `/page/N/index.md`
- **Client-side**: JavaScript per infinite scroll (sconsigliato per SEO)

### 3. Monitoraggio Performance
```bash
# Lighthouse CI su tutti i subcluster
npm run lighthouse:all-subclusters

# Core Web Vitals tracking
# Integra con Google Search Console
```

### 4. A/B Testing
- Testa varianti intro per CTR
- Verifica posizione CTA ottimale
- Monitora engagement FAQ

---

## FAQ Implementazione

### Q: Come aggiungo un nuovo subcluster?
1. Crea file in `pages/categories/sub_cluster/categoria/nome-subcluster.md`
2. Usa template da `docs/subcluster-template-example.md`
3. Aggiungi mapping in `_data/subcluster_slugs.yml` se necessario
4. Carica immagini in `/img/subcluster/`
5. Build e testa

### Q: La paginazione funziona su GitHub Pages?
Attualmente la paginazione è implementata tramite Liquid (manuale). Per paginazione automatica:
- **Locale/Netlify**: usa `jekyll-paginate-v2`
- **GitHub Pages**: genera pagine statiche con script

### Q: Come testo lo schema?
```bash
# 1. Build locale
bundle exec jekyll serve

# 2. Ispeziona source in browser
view-source:http://localhost:4000/categorie/categoria/subcluster/

# 3. Copia JSON-LD e testa su:
https://search.google.com/test/rich-results
https://validator.schema.org/
```

### Q: Posso rimuovere la CTA?
Sì, rimuovi o commenta la sezione nel front matter:
```yaml
# cta_title: ""  # Commenta per nascondere CTA
```

### Q: Come cambio il numero di post per pagina?
In `_layouts/subcluster.html`, modifica:
```liquid
{% assign posts_per_page = 9 %}  # Cambia a 12 o altro
```

---

## Supporto e Manutenzione

**Autore**: Ottimizzazione SEO Modern v3  
**Data**: 2025-10  
**Versione Layout**: subcluster v3  
**Compatibilità**: Jekyll 3.9+, GitHub Pages

Per domande o issue:
1. Controlla questa guida
2. Verifica template esempio
3. Testa in locale prima del deploy

---

**Buon lavoro! 🚀**
