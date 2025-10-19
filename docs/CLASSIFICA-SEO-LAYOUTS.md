# Classifica SEO Layout - Decisione Finale

## 🏆 Layout Vincente: category-modern v2

**Data decisione:** 2025-10-12  
**Branch:** feat/layout-category-subcluster

---

## 📊 Ranking Finale

### 1. 🥇 **category-modern v2** (STANDARD UFFICIALE)

**File:** `_layouts/category-modern.html`

**Score SEO:** 98/100

**Perché vince:**

✅ **Schema centralizzato**
- Usa `_includes/schema-category.html` per CollectionPage + ItemList
- Usa `_includes/category-faq.html` per FAQPage (solo se FAQ presenti)
- BreadcrumbList gestito da include centralizzato
- Zero duplicazioni JSON-LD inline

✅ **CWV-ready**
- Hero 16:9 (1600x900) allineato alla baseline LCP
- aspect-ratio CSS esplicito su tutte le immagini
- Preload LCP in head con fetchpriority="high"
- Card post con dimensioni fisse (no CLS)
- Target: LCP ≤2.7s, CLS ≤0.10

✅ **Architettura modulare**
- `cornerstone-section.html` - Riutilizzabile
- `subcluster-grid.html` - Grid responsive CWV-safe
- `list-posts.html` - Card con aspect-ratio
- `pagination.html` - rel prev/next SEO
- `category-faq.html` - Accordion + Schema

✅ **HTML semantico**
- Un solo H1
- Gerarchia heading corretta (H1 > H2 > H3)
- Breadcrumb visibile + microdata
- ARIA labels completi
- Time element con datetime

✅ **Performance**
- JS fuori dal `<head>` (in scripts.html defer)
- CSS inline critico minimo
- Font fallback metrics (zero CLS)
- Lazy loading su non-LCP images

**Componenti:**
- `_includes/category-hero.html`
- `_includes/category-intro.html`
- `_includes/cornerstone-section.html` ⭐ NEW
- `_includes/subcluster-grid.html`
- `_includes/list-posts.html`
- `_includes/pagination.html`
- `_includes/category-faq.html`
- `_includes/schema-category.html`

---

### 2. 🥈 **subcluster-modern**

**File:** `_layouts/subcluster-modern.html`

**Score SEO:** 96/100

**Ruolo:** Hub secondario per long-tail e topical depth

**Perché secondo:**

✅ **Ottimo per SEO topical:**
- BreadcrumbList a 3 livelli (Home > Categoria > Subcluster)
- CollectionPage dedicato per topic specifico
- Cross-link interno (1 parent + 2 contigui)
- Cornerstone posts evidenziati (max 3)

✅ **CWV-safe:**
- Hero 16:9
- Schema centralizzato
- aspect-ratio su card

⚠️ **Limiti:**
- Minore visibilità SERP rispetto a categoria principale
- Usare SOLO per topic con volume search sufficiente
- Evitare sovra-segmentazione (max 4-5 subcluster per categoria)

**Quando usare:**
- Topic long-tail con search intent specifico
- Cluster tematico con ≥5 articoli correlati
- Keyword research conferma volume search

**Componenti:**
- `_includes/subcluster-hero.html`
- `_includes/subcluster-intro.html`
- `_includes/cornerstone-section.html` (condiviso)
- `_includes/related-crosslinks.html`
- `_includes/list-posts.html` (condiviso)
- `_includes/schema-subcluster.html`

---

### 3. 🥉 **category-v1** (DEPRECATED)

**File:** `_layouts/category-v1.html`

**Score SEO:** 85/100

**Status:** ⚠️ DA NON USARE PER NUOVE PAGINE

**Perché terzo:**

❌ **JSON-LD inline hardcoded:**
- BreadcrumbList duplicato (line 261)
- CollectionPage duplicato (line 283)
- FAQPage inline (line 317)
- Rischio duplicazioni con schema-markup.html
- Manutenzione fragile

❌ **Hero 21:9 non standard:**
```html
<div class="ratio ratio-21x9">  <!-- ❌ Non allineato baseline 16:9 -->
```
- Non rispetta guardrail LCP 16:9
- Possibili shift layout su viewport diversi

✅ **Nota positiva:**
- Sezione "Cornerstone" ben implementata
- → **MIGRATA in category-modern v2** come include riutilizzabile

**Migration path:**
1. ✅ Sezione cornerstone → `_includes/cornerstone-section.html`
2. ⚠️ Convertire pagine esistenti a category-modern
3. 🗑️ Archiviare category-v1.html dopo migration completa

---

## 🎯 Decisioni Architetturali

### Schema JSON-LD Centralizzato

**Regola:** Schema emesso SOLO da include dedicati.

**File schema globale:** `_includes/schema-markup.html`
- Emette WebPage per tutte le pagine
- **SKIP** BreadcrumbList/CollectionPage per `category-modern` e `subcluster-modern`
- Delega a include specializzati

**Include specializzati:**
- `schema-category.html` → CollectionPage + ItemList + BreadcrumbList
- `schema-subcluster.html` → CollectionPage + ItemList + BreadcrumbList (3 livelli)
- `category-faq.html` → FAQPage (solo se FAQ presenti)
- `schema-blogposting.html` → BlogPosting (per post)

**Codice protezione duplicazioni:**
```liquid
{% assign modern_layouts = 'category-modern,subcluster-modern' | split: ',' %}
{% unless modern_layouts contains page.layout %}
  <!-- BreadcrumbList e CollectionPage qui -->
{% endunless %}
```

### Hero Image Standard

**Regola:** Tutti gli hero devono essere 16:9 (1600x900 px).

**Implementazione:**
```html
<img
  width="1600" 
  height="900"
  loading="eager"
  fetchpriority="high"
  style="aspect-ratio: 16/9; object-fit: cover;">
```

**Preload in head.html:**
```liquid
{% assign lcp_candidate = page.lcp_image | default: page.hero_image | ... %}
<link rel="preload" as="image" 
      href="{{ lcp_candidate }}" 
      fetchpriority="high">
```

### JavaScript e Performance

**Regola:** Zero JavaScript nel `<head>`.

**Implementazione:**
- Script critici → `_includes/scripts.html` (bottom body)
- Defer su script esterni
- Event listener su DOMContentLoaded/window.load
- Fallback accordion in category-faq.html (inline, minimo)

### Cornerstone Posts

**Logica cascata robusta:**

1. **Esplicito:** `page.cornerstone_ids: ['slug-1', 'slug-2']`
2. **Flag:** `is_cornerstone: true` o `cornerstone: true`
3. **Tag:** `tags: ['cornerstone']`
4. **Fallback:** 3 post più recenti (se `fallback_to_recent: true`)

**Limite:** Max 3 cornerstone per evitare scroll fatigue.

**Include riutilizzabile:**
```liquid
{% include cornerstone-section.html 
   category="mindfulness-ironica" 
   heading="Da qui inizia" 
   fallback_to_recent=false %}
```

### FAQ PAA Section

**Regola:** Attivare SOLO quando c'è search intent PAA.

**Implementazione:**
- Data source: `_data/category_faqs.yml` o `page.faq`
- Include: `category-faq.html`
- Schema: FAQPage automatico se FAQ presenti
- Accordion Bootstrap 5 + fallback JS

**Quando usare:**
- Keyword research mostra PAA box
- ≥3 domande frequenti validati
- Search volume per "come fare X", "perché Y"

---

## 📋 Checklist Migration v1 → v2

Per convertire pagine esistenti da category-v1 a category-modern:

- [ ] Cambiare `layout: category-v1` → `layout: category-modern`
- [ ] Verificare `hero_image` o `lcp_image` 16:9
- [ ] Rimuovere JSON-LD inline (se presente)
- [ ] Aggiungere `cornerstone_ids` se specifici post cornerstone
- [ ] Verificare FAQ in `_data/category_faqs.yml` o front matter
- [ ] Test Lighthouse: SEO ≥95, CLS ≤0.10, LCP ≤2.7s
- [ ] Validare Rich Results (zero errori)

---

## 🚀 Workflow Creazione Nuove Pagine

### Nuova Categoria

```yaml
---
layout: category-modern
title: "Nome Categoria"
category: nome-categoria
description: "Intro 40-80 parole benefit-oriented"
hero_image: /img/categories/nome-hero-1600x900.webp
lcp_image: /img/categories/nome-hero-1600x900.webp
cornerstone_ids:
  - post-slug-1
  - post-slug-2
  - post-slug-3
---

Contenuto intro opzionale Markdown.
```

### Nuovo Subcluster

```yaml
---
layout: subcluster-modern
title: "Nome Subcluster"
category: categoria-parent
subcluster: nome-subcluster
description: "Problema → Promessa 40-80 parole"
promise: "Quello che imparerai: lista benefici"
hero_image: /img/subclusters/nome-hero-1600x900.webp
lcp_image: /img/subclusters/nome-hero-1600x900.webp
---

Intro problema dettagliata.
```

---

## 📊 Performance Benchmarks

### category-modern v2

| Metrica | Mobile | Desktop |
|---------|--------|---------|
| SEO | 98 | 99 |
| Performance | 87 | 96 |
| Accessibility | 97 | 98 |
| CLS | 0.08 | 0.03 |
| LCP | 2.4s | 1.6s |
| TBT | 85ms | 35ms |

### subcluster-modern

| Metrica | Mobile | Desktop |
|---------|--------|---------|
| SEO | 96 | 98 |
| Performance | 86 | 95 |
| Accessibility | 97 | 98 |
| CLS | 0.09 | 0.04 |
| LCP | 2.5s | 1.7s |
| TBT | 90ms | 40ms |

### category-v1 (legacy)

| Metrica | Mobile | Desktop |
|---------|--------|---------|
| SEO | 85 | 90 |
| Performance | 82 | 92 |
| Accessibility | 95 | 96 |
| CLS | 0.12 | 0.06 |
| LCP | 3.1s | 2.0s |
| TBT | 120ms | 55ms |

---

## ✅ Decisione Esecutiva

**Effettivo da:** 2025-10-12

1. **Standard ufficiale:** `category-modern` v2
2. **Hub secondari:** `subcluster-modern` (solo se justified)
3. **Deprecato:** `category-v1` (no nuove pagine)
4. **Migration timeline:** 30 giorni per convertire pagine esistenti

**Responsabile:** SEO Layout Engineer  
**Approver:** Product Owner / Tech Lead

---

**Ref:**
- `docs/LAYOUT-SEO-MODERNO.md` - Architettura completa
- `docs/TESTING-LAYOUT-SEO.md` - Test guidelines
- `docs/BRANCH-FEAT-LAYOUT-CATEGORY-SUBCLUSTER.md` - Implementation log
