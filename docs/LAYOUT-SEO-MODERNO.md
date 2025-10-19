# Layout SEO Moderni - Categoria e Subcluster

## Overview

Implementazione di layout SEO-ottimizzati per pagine Categoria e Subcluster, progettati per Core Web Vitals e accessibilità.

**KPI Target:**
- SEO Score: ≥95 (Lighthouse mobile)
- CLS: ≤0.10
- LCP: ≤2.7s
- TBT: ≤100ms
- Zero errori Rich Results

---

## 📁 Struttura File

### Layout Principali

- **`_layouts/category-modern.html`** - Layout categoria hub
- **`_layouts/subcluster-modern.html`** - Layout subcluster tematico

### Include Categoria

- **`_includes/category-hero.html`** - Hero LCP-safe 16:9
- **`_includes/category-intro.html`** - Intro 40-80 parole
- **`_includes/subcluster-grid.html`** - Grid subclusters responsive
- **`_includes/category-faq.html`** - FAQ accordion + Schema
- **`_includes/schema-category.html`** - CollectionPage + ItemList

### Include Subcluster

- **`_includes/subcluster-hero.html`** - Hero ottimizzato
- **`_includes/subcluster-intro.html`** - Intro problema→promessa
- **`_includes/related-crosslinks.html`** - Internal linking
- **`_includes/schema-subcluster.html`** - Schema 3 livelli

### Include Condivisi

- **`_includes/list-posts.html`** - Card post CWV-safe
- **`_includes/pagination.html`** - Pagination SEO (rel prev/next)
- **`_includes/breadcrumb.html`** - Breadcrumb visibile + JSON-LD

---

## 🎯 Caratteristiche SEO

### Hero LCP-Safe
```html
<img
  src="image-1600.webp"
  width="1600" height="900"
  loading="eager"
  fetchpriority="high"
  style="aspect-ratio: 16/9; object-fit: cover;">
```

**Prevenzione CLS:**
- Dimensioni esplicite width/height
- aspect-ratio CSS inline
- No lazy loading su LCP
- fetchpriority="high"

### Schema.org Markup

**Categoria:**
- CollectionPage
- ItemList (max 20 post)
- BreadcrumbList (2 livelli)
- FAQPage (opzionale)

**Subcluster:**
- CollectionPage
- ItemList (max 20 post)
- BreadcrumbList (3 livelli: Home > Categoria > Subcluster)

### HTML Semantico

✅ **Un solo H1 per pagina**
✅ **Gerarchia heading corretta** (H1 > H2 > H3)
✅ **ARIA labels** su navigazione e sezioni
✅ **Breadcrumb visibile** + microdata
✅ **Time element** con datetime

---

## 🚀 Utilizzo

### Creare Pagina Categoria

```yaml
---
layout: category-modern
title: "Mindfulness ironica"
category: mindfulness-ironica
description: "Mindfulness pratica senza incenso né fuffa. Guide per ridurre stress e aumentare presenza nella vita quotidiana."
hero_image: /img/categories/mindfulness-hero.webp
image: /img/categories/mindfulness-og.jpg
---

Intro opzionale in Markdown (40-80 parole).
```

### Creare Pagina Subcluster

```yaml
---
layout: subcluster-modern
title: "Mindfulness al lavoro"
category: mindfulness-ironica
subcluster: mindfulness-al-lavoro
description: "Tecniche pratiche per gestire stress lavorativo senza meditare 2 ore al giorno."
promise: "Imparerai a creare micro-pause efficaci, gestire riunioni stressanti e proteggere il tuo tempo mentale."
hero_image: /img/subclusters/mindfulness-lavoro-hero.webp
image: /img/subclusters/mindfulness-lavoro-og.jpg
---

Intro Markdown opzionale.
```

---

## 🎨 Componenti

### Subcluster Grid

Automaticamente genera card per tutti i subclusters della categoria:

- **Layout:** Grid responsive 3 colonne (1 su mobile)
- **Immagine:** Aspect-ratio 16:9, lazy loading
- **Descrizione:** Troncata a 2 righe (-webkit-line-clamp)
- **Counter:** "N articoli"

### Post Cards

**Caratteristiche CWV:**
```css
.card-img-wrapper {
  aspect-ratio: 16/9;
  overflow: hidden;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}
```

- Dimensioni fisse → no CLS
- Background placeholder → no flash bianco
- Lazy loading + decoding=async
- Hover effect smooth

### Pagination

**SEO-friendly:**
```html
<link rel="prev" href="/page/2/">
<link rel="next" href="/page/4/">
```

- rel="prev/next" in `<head>`
- Canonical autocoerente
- ARIA labels accessibili
- Responsive (nascondi numeri su mobile)

---

## 📊 Dati e Mapping

### `_data/category_slugs.yml`

Mappa chiavi categoria → URL canonico:

```yaml
mindfulness-ironica: /categorie/mindfulness-ironica/
filosofia-pratica: /categorie/filosofia-pratica/
burnout-lavoro: /categorie/burnout-lavoro/
```

### `_data/subcluster_slugs.yml`

Mappa "categoria:subcluster" → URL:

```yaml
mindfulness-ironica:mindfulness-al-lavoro: /categorie/mindfulness-ironica/mindfulness-al-lavoro/
filosofia-pratica:scienza-e-spiritualita: /categorie/filosofia-pratica/scienza-e-spiritualita/
```

### `_data/category_faqs.yml`

FAQ per categoria:

```yaml
mindfulness-ironica:
  - question: "Devo meditare 2 ore al giorno?"
    answer: "No. Bastano 5-10 minuti per iniziare."
  - question: "Funziona davvero?"
    answer: "Sì, se praticata con costanza."
```

---

## 🧪 Testing

### Lighthouse Mobile

```bash
# Categoria
lighthouse https://messymind.it/categorie/mindfulness-ironica/ \
  --only-categories=performance,seo,accessibility \
  --form-factor=mobile \
  --throttling.cpuSlowdownMultiplier=4

# Subcluster
lighthouse https://messymind.it/categorie/mindfulness-ironica/mindfulness-al-lavoro/ \
  --only-categories=performance,seo,accessibility \
  --form-factor=mobile
```

**Target mediana (3 run):**
- Performance: ≥85
- SEO: ≥95
- Accessibility: ≥95
- CLS: ≤0.10
- LCP: ≤2.7s

### Rich Results

Testa schema su:
https://search.google.com/test/rich-results

**Validazioni:**
- ✅ BreadcrumbList
- ✅ CollectionPage
- ✅ ItemList
- ✅ FAQPage (se presente)

---

## 🔧 Ottimizzazioni CWV

### Preload LCP in `head.html`

```liquid
{% assign lcp_candidate = page.lcp_image | default: page.image %}
<link rel="preload" as="image" 
      href="{{ lcp_candidate | absolute_url }}"
      fetchpriority="high">
```

### CSS Inline Critico

Ogni hero include ha CSS inline per:
- Dimensioni min-height
- Overlay gradient
- Text shadow
- Responsive breakpoint

### Font Display Swap

```css
@font-face {
  font-family: 'Poppins';
  font-display: swap;
  /* ... */
}
```

---

## 🛡️ Guardrail

### ❌ Non Fare

- ❌ Inline CSS pesante (>5KB)
- ❌ Lazy loading su hero LCP
- ❌ Più di un H1
- ❌ Contenuto testuale nuovo senza approvazione
- ❌ Cambi URL/slug senza redirect
- ❌ Immagini senza width/height

### ✅ Fare

- ✅ Preload immagine LCP
- ✅ width/height espliciti su img
- ✅ aspect-ratio CSS per stabilità
- ✅ fetchpriority="high" su LCP
- ✅ Banner cookie fuori dal flow (position: fixed)
- ✅ Breadcrumb visibile
- ✅ Schema JSON-LD valido

---

## 📝 Checklist Pre-Deploy

- [ ] H1 unico e descrittivo
- [ ] Hero con width/height espliciti
- [ ] LCP preload in head
- [ ] Breadcrumb visibile e con JSON-LD
- [ ] Schema CollectionPage + ItemList
- [ ] rel="prev/next" su pagination
- [ ] Canonical self su ogni pagina
- [ ] ARIA labels su nav e sezioni
- [ ] Lighthouse SEO ≥95
- [ ] CLS ≤0.10
- [ ] Zero errori Rich Results

---

## 🚢 Rollout Plan

### Fase 1: Test Branch
- Branch: `feat/layout-category-subcluster`
- Test su 1 categoria + 1 subcluster
- Misura KPI baseline vs new

### Fase 2: Staged Rollout
- Deploy categoria principale (50% traffico)
- Monitor CWV per 7 giorni
- Se ok → 100%

### Fase 3: Full Migration
- Migra tutte le categorie
- Aggiorna subclusters
- Archive vecchi layout

---

## 📚 Riferimenti

- [Web Vitals](https://web.dev/vitals/)
- [Schema.org CollectionPage](https://schema.org/CollectionPage)
- [Google Search Central - Breadcrumbs](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb)
- [Lighthouse Scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/)

---

**Autore:** SEO Layout Engineer  
**Data:** 2025-10-10  
**Versione:** 2.0
