# Subcluster Layout - Allineamento con Category Style

## ✅ Completato: Subcluster ora identico a Category

Il layout **subcluster** è stato completamente allineato allo stile **category** per consistenza visiva e UX uniforme.

---

## 🎨 Componenti Allineati

### 1. Hero con CTA Button
**Prima**: Hero semplice con solo H1  
**Ora**: Hero stile category con:
- H1 title
- Tagline (da campo `intro`)
- **CTA button "Inizia da qui"** che scrolla a `#cornerstone-heading`
- Stesso overlay e stile visivo

**File**: `_includes/subcluster-hero.html`

```yaml
# Front matter
intro: |
  Testo breve (30 parole max) mostrato come tagline nell'hero
```

---

### 2. Sezione "Argomenti principali"
**Prima**: Intro testuale semplice  
**Ora**: Grid 1x2 con 2 card principali, stile "Temi Principali" della home

**File**: `_includes/subcluster-intro.html`

**Struttura**:
- Titolo: "Argomenti principali"
- Sottotitolo: campo `promise` (opzionale)
- 2 card con `title` + `description`
- Design responsive: 2 colonne desktop, stack mobile

**Front matter**:
```yaml
promise: "Breve promessa di valore (una frase)"
topics:
  - title: "Primo argomento"
    description: "Descrizione concisa (1-2 frasi)"
    url: ""  # Opzionale: link a post specifico
  - title: "Secondo argomento"
    description: "Altra descrizione pratica"
    url: ""
```

**Fallback**: Se `topics` non è definito ma c'è `promise`, mostra solo heading + promise centrati.

---

### 3. Sezione "Guide essenziali" (Cornerstone)
**Prima**: Card orizzontali custom  
**Ora**: Grid 3 card verticali, identico a category

**File**: `_includes/cornerstone-section.html` (componente condiviso)

**Features**:
- Thumbnail 16:9 ratio
- Max 3 post cornerstone
- Bottone "Leggi" in ogni card
- Layout responsive: 3 col desktop → stack mobile

**Logica cornerstone** (in ordine):
1. `page.cornerstone_ids` (array di slug)
2. Flag `is_cornerstone` o `cornerstone` nei post
3. Tag `cornerstone` nei post
4. Fallback ai 3 post più recenti (se `fallback_to_recent: true`)

---

### 4. Lista Post - Featured Cards
**Prima**: Grid semplice 3 colonne  
**Ora**: Featured card orizzontali, stile category

**Struttura**:
- Card orizzontale: immagine 50% | contenuto 50%
- Ratio 16:9 sull'immagine
- Titolo H3 + excerpt + data + badge categoria
- Una card per riga (full-width)
- Lazy loading su tutte le immagini (non LCP)
- `sizes="(max-width: 768px) 100vw, 50vw"`

**Paginazione**: 9 post per pagina (configurabile)

---

### 5. FAQ - Accordion Bootstrap
**Prima**: Include custom `faq.html`  
**Ora**: `category-faq.html` (condiviso)

**Features**:
- Accordion Bootstrap 5
- Schema FAQPage JSON-LD automatico
- Fallback JavaScript per browsers senza Bootstrap
- Max 5 domande visualizzate

**Fonti FAQ** (in ordine di priorità):
1. `_data/category_faqs.yml` → chiave `categoria:subcluster`
2. `page.faq` nel front matter della pagina

**Front matter esempio**:
```yaml
# Opzione 1: definire inline
faq:
  - question: "Domanda?"
    answer: "Risposta dettagliata."
  - question: "Altra domanda?"
    answer: "Altra risposta."
```

**Opzione 2**: Aggiungere in `_data/category_faqs.yml`:
```yaml
filosofia-pratica:decisioni-e-bias:
  - q: "Domanda?"
    a: "Risposta."
```

---

### 6. CTA Newsletter
**Prima**: Card blu con bottone bianco  
**Ora**: Card bianca con bordo, stile home/category

**Default**:
- Titolo: "Ricevi 1 pratica a settimana"
- Testo: "Zero spam. Una sola email con una micro‑tecnica testata sul campo."
- Bottone: "Iscriviti"
- Link: `/newsletter/`

**Personalizzabile**:
```yaml
cta_title: "Titolo custom"
cta_text: "Testo persuasivo personalizzato"
cta_button: "Testo bottone"
cta_link: "/altra-pagina/"
```

---

### 7. Schema JSON-LD
**Identico a category**:
- `CollectionPage` per il subcluster
- `ItemList` con SOLO i post della pagina corrente (paginati)
- `BreadcrumbList` a 3 livelli: Home → Categoria → Subcluster
- `FAQPage` condizionale (se FAQ presenti)

**File**: `_includes/schema-subcluster.html`

---

## 📋 Struttura Visiva Completa

```
┌─────────────────────────────────────┐
│ HERO (1600x900, 16:9)              │
│ - H1 Title                         │
│ - Tagline (intro)                  │
│ - CTA "Inizia da qui"              │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ BREADCRUMB                         │
│ Home > Categoria > Subcluster      │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ ARGOMENTI PRINCIPALI (Grid 1x2)   │
│ ┌────────────┐  ┌────────────┐    │
│ │ Topic 1    │  │ Topic 2    │    │
│ │ Descrizione│  │ Descrizione│    │
│ └────────────┘  └────────────┘    │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ GUIDE ESSENZIALI (Grid 1x3)       │
│ ┌───┐ ┌───┐ ┌───┐               │
│ │ 1 │ │ 2 │ │ 3 │               │
│ └───┘ └───┘ └───┘               │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ ULTIMI ARTICOLI                    │
│ ┌─────────────────────────────┐   │
│ │ Featured Card 1             │   │
│ └─────────────────────────────┘   │
│ ┌─────────────────────────────┐   │
│ │ Featured Card 2             │   │
│ └─────────────────────────────┘   │
│        [...]                       │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ PAGINAZIONE (se > 9 post)          │
│ ‹ 1 2 3 ›                         │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ FAQ (Accordion)                    │
│ ▼ Domanda 1                       │
│ ▼ Domanda 2                       │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ CTA NEWSLETTER                     │
│ "Ricevi 1 pratica a settimana"    │
│        [Iscriviti]                 │
└─────────────────────────────────────┘
```

---

## 🔧 File Modificati

### Layout
- ✅ `_layouts/subcluster.html` - Completamente riallineato a category

### Includes
- ✅ `_includes/subcluster-hero.html` - Aggiunto CTA button "Inizia da qui"
- ✅ `_includes/subcluster-intro.html` - Grid 1x2 "Argomenti principali"
- ✅ `_includes/head.html` - Preload hero per layout subcluster
- ✅ `_includes/schema-subcluster.html` - Paginazione + FAQPage
- ✅ `_includes/list-posts.html` - Sizes attribute ottimizzato
- ℹ️ `_includes/cornerstone-section.html` - Già condiviso, nessuna modifica
- ℹ️ `_includes/category-faq.html` - Già condiviso, nessuna modifica

### Documentazione
- ✅ `docs/subcluster-template-example.md` - Template aggiornato
- ✅ `docs/SUBCLUSTER-OPTIMIZATION-GUIDE.md` - Guida SEO completa
- ✅ `docs/SUBCLUSTER-CATEGORY-ALIGNMENT.md` - Questo file

### Esempi Pagine
- ✅ `pages/.../decisioni-e-bias.md` - Aggiornato con topics
- ✅ `pages/.../pratiche-quotidiane-urbane.md` - Aggiornato completo

---

## 📝 Front Matter Completo

### Template Minimo
```yaml
---
layout: subcluster
title: "Nome Subcluster"
seo_title: "Nome Subcluster | Categoria | MessyMind"
description: "Meta description 150-160 caratteri"
category: slug-categoria
subcluster: slug-subcluster

image: "/img/subcluster/hero.webp"
hero_image: "/img/subcluster/hero.webp"
hero_alt: "Descrizione accessibile"

intro: |
  Tagline breve (max 30 parole) mostrata nell'hero sotto il titolo.

permalink: /categorie/categoria/subcluster/
sitemap: true
---
```

### Template Completo (Raccomandato)
```yaml
---
layout: subcluster
title: "Nome Subcluster"
seo_title: "Nome Subcluster | Categoria | MessyMind"
description: "Meta description SEO-friendly 150-160 caratteri"
category: slug-categoria
subcluster: slug-subcluster

# SEO & Images
image: "/img/subcluster/hero-1600.webp"
hero_image: "/img/subcluster/hero-1600.webp"
hero_alt: "Descrizione accessibile immagine"

# Hero
intro: |
  Tagline accattivante (max 30 parole) che appare nell'hero.
  Problema → Promessa in una frase.

# Argomenti principali (Grid 1x2)
promise: "Promessa di valore in una frase"
topics:
  - title: "Primo argomento chiave"
    description: "Cosa imparerai o troverai. 1-2 frasi max."
    url: ""  # Opzionale
  - title: "Secondo argomento chiave"
    description: "Altra area tematica coperta. Pratico e concreto."
    url: ""

# FAQ (3-5 domande pertinenti)
faq:
  - question: "Domanda frequente 1?"
    answer: "Risposta concisa e utile."
  - question: "Domanda frequente 2?"
    answer: "Altra risposta pratica."
  - question: "Domanda frequente 3?"
    answer: "Terza risposta."

# CTA Newsletter (opzionale, default fornito)
cta_title: "Vuoi approfondire [tema]?"
cta_text: "Ogni settimana condivido tecniche pratiche. Zero spam."
cta_button: "Iscriviti gratis"
cta_link: "/newsletter/"

# Cornerstone (opzionale, usa slug dei post)
cornerstone_ids:
  - "slug-post-essenziale-1"
  - "slug-post-essenziale-2"
  - "slug-post-essenziale-3"

permalink: /categorie/categoria/subcluster/
sitemap: true
noindex: false
---
```

---

## 🎯 SEO & Performance

### Core Web Vitals Target
- **LCP**: ≤ 2.7s (hero preloaded, fetchpriority="high")
- **CLS**: ≤ 0.10 (dimensioni esplicite su tutte le immagini)
- **SEO Score**: ≥ 95 (schema completo, semantic HTML)

### Image Optimization
- **Hero**: 1600x900px, WebP/AVIF, preload in `<head>`
- **Cornerstone thumbnails**: 600x338px, lazy loading
- **Featured cards**: ratio 16:9, sizes attribute, lazy loading
- **Sizes**: `(max-width: 768px) 100vw, 50vw` per immagini card

### Schema Markup
- ✅ CollectionPage
- ✅ ItemList (solo post pagina corrente)
- ✅ BreadcrumbList (3 livelli)
- ✅ FAQPage (condizionale)

---

## 🚀 Come Usare

### 1. Creare Nuovo Subcluster
```bash
# Copia template
cp docs/subcluster-template-example.md pages/categories/sub_cluster/categoria/nuovo-subcluster.md

# Personalizza front matter
vim pages/categories/sub_cluster/categoria/nuovo-subcluster.md

# Build e testa
bundle exec jekyll serve
```

### 2. Aggiornare Subcluster Esistente
- Apri il file `.md` in `pages/categories/sub_cluster/`
- Aggiungi/modifica campi:
  - `intro`: tagline hero (max 30 parole)
  - `promise` + `topics`: grid argomenti principali
  - `faq`: 3-5 domande pertinenti
  - `cta_*`: personalizza CTA newsletter
- Salva e rebuilda

### 3. Testare Localmente
```bash
bundle exec jekyll serve
# Vai a http://localhost:4000/categorie/categoria/subcluster/
```

### 4. Validare Schema
```bash
# Build
bundle exec jekyll build

# Copia JSON-LD da _site/categorie/.../index.html
# Testa su: https://validator.schema.org/
```

---

## ❓ FAQ Implementazione

### Q: Devo sempre definire `topics`?
**A**: No, è opzionale. Se ometti `topics`, la sezione "Argomenti principali" non appare. Utile se preferisci contenuto markdown custom.

### Q: Posso avere più di 2 topics?
**A**: Il layout mostra solo i primi 2 (limit:2). Per categorie (non subcluster) puoi usare 4 topics.

### Q: Le FAQ devono essere nel front matter?
**A**: No. Puoi anche definirle in `_data/category_faqs.yml` con chiave `categoria:subcluster`. Il layout cerca prima lì, poi nel front matter.

### Q: Come funziona la paginazione?
**A**: Automatica a 9 post per pagina. Per ora manuale (devi creare `/page/2/index.md` con `pagination_page: 2`). Paginazione automatica richiede plugin non-GitHub-Pages.

### Q: Posso nascondere la CTA?
**A**: Sì, non definire `cta_title` o commenta la sezione CTA nel front matter. Il default appare sempre.

### Q: Cornerstone non appare?
**A**: Verifica:
1. Post hanno `is_cornerstone: true` o tag `cornerstone`
2. Post appartengono alla categoria+subcluster corretti
3. Oppure definisci `cornerstone_ids` esplicitamente

---

## 📊 Confronto Prima/Dopo

| Elemento | Prima (v2) | Ora (v3 aligned) |
|----------|-----------|------------------|
| Hero | Solo H1 | H1 + tagline + CTA button |
| Intro | Testo semplice | Grid 1x2 "Argomenti principali" |
| Cornerstone | Card orizzontali custom | Grid 3 card verticali (condiviso) |
| Lista post | Grid 3 col | Featured cards orizzontali |
| FAQ | Include custom | Accordion Bootstrap (condiviso) |
| CTA | Card blu custom | Card bianca stile home (condiviso) |
| Paginazione | Assente | 9 post/pagina |
| Schema | Basic | Completo + FAQPage |

---

## ✨ Vantaggi Allineamento

1. **UX Consistente**: Navigazione uniforme tra category e subcluster
2. **Manutenzione**: Componenti condivisi (`cornerstone-section`, `category-faq`)
3. **Performance**: Stesso livello di ottimizzazione LCP/CLS
4. **SEO**: Schema markup identico e completo
5. **Design**: Visual identity coerente in tutto il sito

---

**Data**: 2025-10-12  
**Versione**: Subcluster v3 (aligned with Category v2)  
**Status**: ✅ Production Ready
