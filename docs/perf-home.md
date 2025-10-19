# Performance Optimization Report: Home Page CWV Stabilization

**Branch:** `fix/home-cwv-stabilization`  
**Merged to:** `main` (deployed)  
**Date:** 2025-10-10

---

## Obiettivo

Stabilizzare i Core Web Vitals della homepage per soddisfare i criteri:
- **CLS ≤ 0.10** (layout shift cumulativo)
- **LCP ≤ 2.5 s** (largest contentful paint)
- **FCP ≤ 2.2 s** (first contentful paint)
- **TBT ≤ 100 ms** (total blocking time)

---

## Metriche Baseline (Prima)

**Fonte:** PageSpeed Insights mobile (emulated Slow 4G, 4× CPU throttle)

| Metrica | Valore | Note |
|---------|--------|------|
| **FCP** | ~3.5 s | Hero non ottimizzato, font blocking |
| **LCP** | ~3.5 s | Hero background CSS, no preload match |
| **CLS** | **0.349** | Cookie banner 0.32, content-box shift 0.014, font swap |
| **TBT** | 0 ms | ✓ OK |
| **Performance** | 67/100 | Penalizzato da LCP e CLS |

### CLS Breakdown (da PSI report)
- `.content-box`: **0.320** (maggior colpevole) → immagini card senza dimensions, font swap
- Cookie banner: **0.013** (minore) → già fixed, solo animazione transform residua
- Font swap: **0.014** → web fonts senza fallback metric
- **Totale:** 0.349 (target: ≤0.10)

---

## Task Implementati (A → E)

### Task A: Hero come vero LCP ✅

**Problema:** Hero era background CSS (`background-image: url(...)`), non rilevabile come LCP. Browser non poteva prioritizzarlo e nessun preload efficace.

**Soluzione:**
1. Convertito hero in `<picture><img>` visibile sopra-the-fold.
2. Aggiunto `width="1600" height="900"` per intrinsic size e aspect-ratio 16:9 riservato in CSS.
3. Rimosso `loading="lazy"` e aggiunto `fetchpriority="high"`.
4. Generati 3 variant srcset: `bg-home-1600.webp` (1600w), `bg-home-800.webp` (800w), `bg-home-400.webp` (400w).
5. Sincronizzato preload in `_includes/head.html` con `imagesrcset` identico all'hero `<img>`.

**File modificati:**
- `_includes/home-hero.html`: hero img con srcset completo.
- `_includes/head.html`: preload con imagesrcset matching.
- `index.md`: front matter `lcp_image: '/img/home/bg-home-1600.webp'`.
- Generati: `img/home/bg-home-800.webp` (15 KiB), `img/home/bg-home-400.webp` (5.8 KiB).

**Impatto atteso:** LCP ridotto ~1–1.5 s (da 3.5 s → 2.0–2.5 s).

---

### Task B: Cookie banner senza shift ✅

**Problema:** Banner mostra shift di 0.013 CLS (minore ma contribuisce al totale).

**Stato attuale:** Banner già usa `position: fixed` e `transform: translateY(100%)` per show/hide (no height animation). Script JS (`cookie-manager.js`) caricato con `defer` e usa `requestAnimationFrame` per batching.

**Azioni:** Nessun cambiamento necessario. Banner già ottimizzato.

**File verificati:**
- `_sass/cookie-banner.scss`: position fixed, transform only.
- `assets/js/cookie-manager.js`: rAF per show, no forced reflow.

**Impatto atteso:** CLS cookie banner rimane ~0.01 (trascurabile).

---

### Task C: Immagini liste e card stabili ✅

**Problema:** `.content-box` mostra CLS 0.32 a causa di immagini card senza width/height e font swap.

**Soluzione:**
1. `_includes/optimized-image.html` aggiornato:
   - Se `include.width` e `include.height` forniti, emette attributi e aspect-ratio CSS.
   - Se `is_lcp`, forza width/height intrinsic (1600×900).
   - **Fallback:** tutte le altre immagini ricevono `style="aspect-ratio: 16/9"` per riservare spazio.
2. Tutte le card home usano `{% include optimized-image.html %}`, quindi beneficiano automaticamente.
3. Aggiunto `loading="lazy"` e `decoding="async"` per tutte le non-LCP.

**File modificati:**
- `_includes/optimized-image.html`: srcset generation, aspect-ratio fallback.

**Impatto atteso:** CLS `.content-box` ridotto da 0.32 → ~0.05.

---

### Task D: Font stabili con fallback metric ✅

**Problema:** Font swap causava micro-shift (CLS ~0.014).

**Soluzione:**
1. Aggiunta `@font-face` fallback locale in `_includes/head.html`:
   - `Merriweather Fallback` → local('Georgia') con size-adjust 96%, ascent/descent override.
   - `Poppins Fallback` → local('Arial') con size-adjust 107%.
2. CSS critico hero usa `font-family: Poppins, 'Poppins Fallback', sans-serif`.
3. Font preload woff2 con `crossorigin="anonymous"` e `as="font"`.
4. Google Fonts chiamata usa `display=swap` (già presente).

**File modificati:**
- `_includes/head.html`: critical CSS con fallback @font-face.
- `_includes/messymind-fonts.html`: crossorigin su preload.

**Impatto atteso:** CLS font swap ridotto da 0.014 → ~0.002.

---

### Task E: JS e Analytics gating ✅

**Problema:** JS non-critico o Analytics potrebbero ritardare FCP/LCP.

**Stato attuale:**
1. Google Analytics caricato solo con consenso cookie (`cookie-manager.js` lo gestisce).
2. Tutti gli script usano `defer` (cookie-manager, theme-toggle).
3. Script inline minimali e DOMContentLoaded-based, no blocking.

**Azioni:** Nessun cambiamento necessario.

**File verificati:**
- `_includes/google-analytics.html`: caricamento condizionato.
- `_includes/scripts.html`: defer su tutti gli external script.

**Impatto atteso:** FCP/TBT già ottimali (TBT 0 ms).

---

## Modifiche Tecniche (Summary)

| File | Cambiamento |
|------|------------|
| `_includes/home-hero.html` | srcset hero 1600/800/400w, fetchpriority=high |
| `_includes/head.html` | Preload imagesrcset matching, fallback font metric |
| `_includes/optimized-image.html` | Aspect-ratio fallback per tutte le immagini |
| `_includes/messymind-fonts.html` | crossorigin su preload font |
| `img/home/bg-home-800.webp` | Generato (15 KiB) |
| `img/home/bg-home-400.webp` | Generato (5.8 KiB) |

---

## Metriche Attese (Dopo) — target

| Metrica | Target | Confidence |
|---------|--------|------------|
| **FCP** | ≤ 2.2 s | Alta (preload hero, defer scripts) |
| **LCP** | ≤ 2.5 s | Alta (hero <img> + preload + fetchpriority) |
| **CLS** | ≤ 0.10 | Media-alta (aspect-ratio, font fallback; dipende da timing) |
| **TBT** | ≤ 100 ms | Alta (già 0 ms) |
| **Performance** | ≥ 85/100 | Alta |

---

## Metriche Reali (Dopo) — da misurare

**TODO:** Eseguire 3 run Lighthouse mobile su https://messymind.it/ dopo deploy.

### Run 1 (mobile, Slow 4G, 4× CPU)
- FCP: __ s
- LCP: __ s
- CLS: __
- TBT: __ ms
- Performance: __

### Run 2
- FCP: __ s
- LCP: __ s
- CLS: __
- TBT: __ ms
- Performance: __

### Run 3
- FCP: __ s
- LCP: __ s
- CLS: __
- TBT: __ ms
- Performance: __

### Mediana (Finale)
- **FCP:** __ s
- **LCP:** __ s
- **CLS:** __
- **TBT:** __ ms
- **Performance:** __

---

## Comandi per Testing

### 1. Lighthouse CLI (3 run production)
```bash
mkdir -p ./reports/after
for i in {1..3}; do
  npx -y lighthouse https://messymind.it/ \
    --throttling-method=simulate \
    --preset=perf \
    --emulated-form-factor=mobile \
    --output=json \
    --output-path=./reports/after/lh-prod-$i.json \
    --quiet
done
```

### 2. Estrarre mediane (Python)
```python
import json, statistics

files = ['./reports/after/lh-prod-1.json', './reports/after/lh-prod-2.json', './reports/after/lh-prod-3.json']
fcps, lcps, clss, tbts, perfs = [], [], [], [], []

for f in files:
    with open(f) as fp:
        d = json.load(fp)
        fcps.append(d['audits']['first-contentful-paint']['numericValue'])
        lcps.append(d['audits']['largest-contentful-paint']['numericValue'])
        clss.append(d['audits']['cumulative-layout-shift']['numericValue'])
        tbts.append(d['audits']['total-blocking-time']['numericValue'])
        perfs.append(d['categories']['performance']['score'])

print(f"Mediana FCP: {statistics.median(fcps)/1000:.2f} s")
print(f"Mediana LCP: {statistics.median(lcps)/1000:.2f} s")
print(f"Mediana CLS: {statistics.median(clss):.3f}")
print(f"Mediana TBT: {statistics.median(tbts):.0f} ms")
print(f"Mediana Performance: {statistics.median(perfs)*100:.0f}")
```

---

## Note e Prossimi Passi

### Se CLS non scende sotto 0.10:
1. Verificare timing caricamento font (web font observer?).
2. Aggiungere `min-height` esplicita a `.content-box` per riservare viewport.
3. Ridurre ulteriormente font swap delay (font-display: optional?).
4. Analizzare filmstrip Lighthouse per identificare shift frames esatti.

### Se LCP non scende sotto 2.5 s:
1. Verificare mismatch preload/srcset (browser inspector Network tab).
2. Verificare cache server (TTL hero image, CDN).
3. Considerare AVIF in aggiunta a WebP (supporto browser).
4. Ridurre dimensioni file hero (compression, blur placeholder).

### Infra/Hosting Opportunities (da applicare):
1. **Cache TTL:** estendere max-age per `/img/home/*` da 10 min a 1 anno (immutable).
2. **Compression:** abilitare Brotli per text/html, application/json.
3. **HTTP/2+:** verificare che il server usi HTTP/2 o HTTP/3 (Netlify: ✓ built-in).
4. **CDN:** assicurarsi che immagini siano servite da edge locations (Netlify CDN: ✓).

### Accessibility/Best Practices/SEO:
- Nessun cambio atteso in questi score (già buoni).
- Verificare post-deploy che non ci siano regressioni.

---

## Screenshots

**TODO:** Allegare screenshot Lighthouse/PSI prima e dopo.

- `docs/screenshots/perf-home-before.png`
- `docs/screenshots/perf-home-after.png`

---

## Rollback Plan

Se CLS/LCP peggiorano:
1. Revert merge commit su main:
   ```bash
   git revert -m 1 HEAD
   git push origin main
   ```
2. Analizzare cause tramite Lighthouse JSON diffs.
3. Applicare fix atomici via micro-PR.

---

## Conclusioni Preliminari

Task A–E implementati con successo. Hero LCP ora è un `<img>` preloaded con srcset matching e fetchpriority high. Immagini card hanno aspect-ratio fallback. Font usano fallback metric per ridurre swap CLS. Cookie banner e JS già ottimizzati.

**Prossima azione:** Eseguire 3× Lighthouse mobile su produzione e aggiornare questo doc con mediane finali.

**Rischio residuo:** CLS potrebbe rimanere sopra 0.10 se il timing font-swap o il banner producono shift inaspettati. Monitorare con Lighthouse filmstrip e iterare se necessario.

---

**Autore:** GitHub Copilot + teo  
**Data aggiornamento:** 2025-10-10
