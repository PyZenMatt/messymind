# Istruzioni Testing Layout SEO Moderni

## 🎯 Obiettivo

Validare i layout `category-modern` e `subcluster-modern` rispetto ai KPI Core Web Vitals e SEO.

**Target:**
- SEO Score: ≥95
- Performance: ≥85
- Accessibility: ≥95
- CLS: ≤0.10
- LCP: ≤2.7s (mobile)
- TBT: ≤100ms

---

## 📋 Pre-requisiti

### 1. Build Locale

```bash
cd /home/teo/Project/messymind.it
bundle exec jekyll build
bundle exec jekyll serve
```

Verifica server attivo su `http://localhost:4000`

### 2. Pagine Test

- **Categoria:** `http://localhost:4000/test-category-mindfulness/`
- **Subcluster:** `http://localhost:4000/test-subcluster-mindfulness-lavoro/`

### 3. Tool Necessari

- **Lighthouse CLI:**
  ```bash
  npm install -g lighthouse
  ```

- **Chrome DevTools** (Performance, Coverage)

- **Rich Results Test:**  
  https://search.google.com/test/rich-results

---

## 🧪 Test Suite

### Test 1: Lighthouse Mobile (Categoria)

```bash
lighthouse http://localhost:4000/test-category-mindfulness/ \
  --only-categories=performance,seo,accessibility,best-practices \
  --form-factor=mobile \
  --throttling.cpuSlowdownMultiplier=4 \
  --output=html \
  --output-path=./reports/lighthouse-category-mobile.html
```

**Checklist:**
- [ ] SEO ≥95
- [ ] Performance ≥85
- [ ] Accessibility ≥95
- [ ] CLS ≤0.10
- [ ] LCP ≤2.7s
- [ ] TBT ≤100ms

### Test 2: Lighthouse Mobile (Subcluster)

```bash
lighthouse http://localhost:4000/test-subcluster-mindfulness-lavoro/ \
  --only-categories=performance,seo,accessibility,best-practices \
  --form-factor=mobile \
  --throttling.cpuSlowdownMultiplier=4 \
  --output=html \
  --output-path=./reports/lighthouse-subcluster-mobile.html
```

**Checklist:** (stessi target del Test 1)

### Test 3: Lighthouse Desktop (Baseline)

```bash
# Categoria Desktop
lighthouse http://localhost:4000/test-category-mindfulness/ \
  --only-categories=performance,seo \
  --form-factor=desktop \
  --output=html \
  --output-path=./reports/lighthouse-category-desktop.html

# Subcluster Desktop
lighthouse http://localhost:4000/test-subcluster-mindfulness-lavoro/ \
  --only-categories=performance,seo \
  --form-factor=desktop \
  --output=html \
  --output-path=./reports/lighthouse-subcluster-desktop.html
```

---

## 🔍 Test Manuali

### 1. HTML Semantico

**Categoria:**
```bash
curl -s http://localhost:4000/test-category-mindfulness/ | grep -c "<h1"
# Expected: 1
```

**Verifica:**
- [ ] Un solo `<h1>` per pagina
- [ ] Gerarchia heading: H1 > H2 > H3
- [ ] Breadcrumb visibile
- [ ] ARIA labels su `<nav>` e `<section>`

**Subcluster:**
```bash
curl -s http://localhost:4000/test-subcluster-mindfulness-lavoro/ | grep -c "<h1"
# Expected: 1
```

### 2. Schema.org Validation

**Estrai JSON-LD:**
```bash
# Categoria
curl -s http://localhost:4000/test-category-mindfulness/ \
  | grep -Pzo '(?s)<script type="application/ld\+json">.*?</script>' \
  > reports/schema-category.json

# Subcluster
curl -s http://localhost:4000/test-subcluster-mindfulness-lavoro/ \
  | grep -Pzo '(?s)<script type="application/ld\+json">.*?</script>' \
  > reports/schema-subcluster.json
```

**Valida su Rich Results Test:**

1. Apri https://search.google.com/test/rich-results
2. Incolla HTML o URL pubblico
3. Verifica:
   - [ ] BreadcrumbList valido
   - [ ] CollectionPage valido
   - [ ] ItemList valido
   - [ ] FAQPage valido (se presente)
   - [ ] Zero warning/errori

### 3. LCP Image Check

**DevTools > Performance:**

1. Apri pagina in Chrome
2. DevTools > Performance > Record (5s)
3. Stop > Cerca "LCP"
4. Verifica:
   - [ ] LCP element è hero image
   - [ ] Timing ≤2.7s (mobile throttling)
   - [ ] Preload presente in Network tab
   - [ ] fetchpriority="high" su `<img>`

**Network Tab:**
```
Filter: "hero" OR "lcp"
```
- [ ] Immagine hero richiesta con priorità "Highest"
- [ ] No lazy loading su LCP
- [ ] Preload presente in `<head>`

### 4. CLS Prevention

**DevTools > Performance Insights:**

1. Record 5s con scroll
2. Cerca "Layout Shift"
3. Verifica:
   - [ ] CLS totale ≤0.10
   - [ ] Zero shift da hero image
   - [ ] Zero shift da font swap (fallback metrics)
   - [ ] Zero shift da card images (aspect-ratio)

**Checklist visivo:**
- [ ] Hero image con width/height espliciti
- [ ] aspect-ratio CSS su card images
- [ ] Background color su img wrapper (no flash bianco)

---

## 📊 Metriche Attese

### Categoria (Mindfulness Ironica)

| Metrica | Mobile | Desktop |
|---------|--------|---------|
| SEO | ≥95 | ≥98 |
| Performance | ≥85 | ≥95 |
| Accessibility | ≥95 | ≥95 |
| CLS | ≤0.10 | ≤0.05 |
| LCP | ≤2.7s | ≤1.8s |
| TBT | ≤100ms | ≤50ms |

### Subcluster (Mindfulness al Lavoro)

| Metrica | Mobile | Desktop |
|---------|--------|---------|
| SEO | ≥95 | ≥98 |
| Performance | ≥85 | ≥95 |
| Accessibility | ≥95 | ≥95 |
| CLS | ≤0.10 | ≤0.05 |
| LCP | ≤2.7s | ≤1.8s |
| TBT | ≤100ms | ≤50ms |

---

## 🐛 Troubleshooting

### Issue: LCP > 2.7s

**Possibili cause:**
- Preload mancante/errato in `<head>`
- Lazy loading su hero image
- fetchpriority non "high"
- Immagine troppo pesante (>300KB)

**Fix:**
```liquid
<!-- In head.html -->
<link rel="preload" as="image" 
      href="{{ page.hero_image | absolute_url }}" 
      fetchpriority="high">

<!-- In hero include -->
<img loading="eager" fetchpriority="high">
```

### Issue: CLS > 0.10

**Possibili cause:**
- width/height mancanti su `<img>`
- aspect-ratio CSS assente
- Font swap senza fallback metrics
- Card images senza dimensioni fisse

**Fix:**
```html
<img width="1600" height="900" 
     style="aspect-ratio: 16/9; object-fit: cover;">
```

### Issue: SEO < 95

**Checklist:**
- [ ] Canonical URL presente
- [ ] Meta description (max 160 char)
- [ ] H1 unico e descrittivo
- [ ] Breadcrumb visibile + JSON-LD
- [ ] rel="prev/next" su pagination
- [ ] Immagini con alt (se non decorative)

---

## 📝 Report Template

```markdown
# Test Report: Layout SEO Moderni

**Data:** 2025-10-10
**Tester:** [Nome]

## Categoria Test

**URL:** http://localhost:4000/test-category-mindfulness/

### Lighthouse Mobile
- SEO: __/100
- Performance: __/100
- Accessibility: __/100
- CLS: __
- LCP: __s
- TBT: __ms

### HTML Semantico
- H1 count: __
- Breadcrumb: ✅ / ❌
- ARIA labels: ✅ / ❌

### Schema.org
- BreadcrumbList: ✅ / ❌
- CollectionPage: ✅ / ❌
- ItemList: ✅ / ❌

### Note:
[Eventuali problemi o osservazioni]

---

## Subcluster Test

**URL:** http://localhost:4000/test-subcluster-mindfulness-lavoro/

[Ripeti struttura categoria]

---

## Conclusioni

✅ **Pass** / ❌ **Fail**

**Azioni richieste:**
1. [Se fail, elencare fix necessari]
```

---

## 🚀 Deploy Checklist

Prima di mergiare il branch:

- [ ] Tutti i test Lighthouse pass (≥target)
- [ ] Rich Results validation ok
- [ ] Zero errori HTML (W3C validator)
- [ ] CLS ≤0.10 su tutte le pagine
- [ ] LCP ≤2.7s mobile
- [ ] Breadcrumb visibile e funzionante
- [ ] Schema JSON-LD valido
- [ ] Canonical URL corretto
- [ ] rel="prev/next" se pagination
- [ ] Documentazione aggiornata

---

**Autore:** SEO Layout Engineer  
**Versione:** 1.0  
**Branch:** feat/layout-category-subcluster
