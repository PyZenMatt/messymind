# 📊 Lighthouse QA Performance Runner

Sistema automatizzato di test delle performance con Lighthouse su **sito di produzione**.

## 🎯 Obiettivi

- **Generare 5 run Lighthouse mobile** per 3 URL rappresentativi (home, category, post)
- **Test automatici in produzione** ogni settimana (domenica 2 AM UTC)
- **Quality gates** che bloccano il workflow se le metriche scendono sotto soglia
- **Report salvati** come GitHub Actions artifacts (retention 30 giorni)
- **Nessuna dipendenza da API Google** (PSI non utilizzato)

## 📋 Quality Gates (Soglie Minime)

| Metrica | Mobile |
|---------|--------|
| **Performance** | ≥ 80 |
| **SEO** | ≥ 95 |
| **Accessibility** | ≥ 90 |
| **Best Practices** | ≥ 90 |

**Core Web Vitals**:

- **CLS** (Cumulative Layout Shift): ≤ 0.1

## 🛠️ Setup

### Prerequisiti Installati

```bash
npm install --save-dev @lhci/cli
```

### File di Configurazione

- **`lighthouserc.json`**: Configurazione LHCI con URL produzione, 5 run, mobile preset
- **`.github/workflows/lhci.yml`**: GitHub Actions workflow con Chrome dedicato
- **`docs/evidence/lighthouse/<YYYY-MM-DD>/`**: Directory report per data

## 🚀 Utilizzo

### Test Automatici in CI/CD (Produzione)

I test Lighthouse vengono eseguiti automaticamente su **https://messymind.it**:

1. **Ogni domenica alle 2 AM UTC** (cron schedule)
2. **Push** su branch `feat/layout-category-subcluster`
3. **Manualmente** tramite GitHub Actions → "Lighthouse CI Production" → "Run workflow"

Il workflow:

1. ✅ Installa Chrome dedicato (bypass snap issues)
2. ✅ Esegue Lighthouse **5 volte per URL** su mobile preset
3. ✅ Calcola **mediana automatica** dei punteggi
4. ✅ Valuta le soglie
5. ❌ **FAIL** se una soglia non è raggiunta
6. ✅ Carica report HTML/JSON come artifacts (30 giorni)
7. � Genera summary con Node/Chrome versions

### Come Leggere i 5 Run

LHCI genera **15 report totali** (5 run × 3 URL):

- Report nominati: `lh_<url_hash>_<run_number>.html/json`
- **Mediana usata per assertions**: LHCI calcola automaticamente
- **Lettura manuale**: Scarica artifacts → apri 5 HTML per URL → confronta punteggi

Esempio per home (5 run):

```text
Run 1: Performance 87, SEO 98, A11y 92
Run 2: Performance 85, SEO 98, A11y 91  ← Mediana (usata)
Run 3: Performance 89, SEO 97, A11y 93
Run 4: Performance 82, SEO 98, A11y 90
Run 5: Performance 88, SEO 98, A11y 92
```

**Nota**: I run sono di **laboratorio** (GitHub Actions runner). Non rappresentano utenti reali ma sono **consistenti** per tracking trends.

### Nessun PSI/API Google

Questo setup **NON usa**:

- ❌ PageSpeed Insights API
- ❌ Google Cloud credentials
- ❌ Rate limits esterni

Usa solo:

- ✅ Lighthouse CLI bundled con @lhci/cli
- ✅ Chromium controllato da Puppeteer
- ✅ Test diretti HTTP su produzione

### URL Testati

I test vengono eseguiti su produzione:

1. **Home**: `/`
   - Rappresenta la landing page principale
   - Testa hero image, grid cluster, performance generale

2. **Category Burnout**: `/categorie/burnout-e-lavoro/`
   - Rappresenta tutte le pagine category
   - Testa hero category, topics grid, guide essenziali, subcluster grid

3. **Post Stress**: `/2025/09/29/stress-correlato/`
   - Rappresenta tutti i post del blog
   - Testa layout post, sidebar, related posts

**URL Base**: `https://messymind.it`

## 📊 Report

### Artifacts GitHub Actions

Dopo ogni run del workflow:

1. Vai su **Actions** → "Lighthouse CI Production" → Seleziona run
2. Scorri in basso a **Artifacts**
3. Scarica `lighthouse-reports-<run_number>` (ZIP con 15 file: 5 HTML + 5 JSON per 3 URL)

### Struttura Report

```text
.lighthouseci/
├── lh_<hash_home>_1.html           # Home run 1
├── lh_<hash_home>_1.json
├── lh_<hash_home>_2.html           # Home run 2
... (5 run home)
├── lh_<hash_category>_1.html       # Category run 1
... (5 run category)
├── lh_<hash_post>_1.html           # Post run 1
... (5 run post)
```

**Totale**: 30 file (15 HTML + 15 JSON)

## 🔧 Configurazione Avanzata

### Modificare le Soglie

Edita `lighthouserc.json` sezione `assert.assertions`:

```json
{
  "assert": {
    "assertions": {
      "categories:performance": ["error", {"minScore": 0.8}],
      "categories:seo": ["error", {"minScore": 0.95}]
    }
  }
}
```

### Aggiungere URL

Edita `lighthouserc.json` sezione `collect.url`:

```json
{
  "collect": {
    "url": [
      "https://messymind.it/",
      "https://messymind.it/nuovo-url-da-testare/"
    ]
  }
}
```

### Cambiare Numero di Run

Edita `lighthouserc.json` sezione `collect.numberOfRuns`:

```json
{
  "collect": {
    "numberOfRuns": 3
  }
}
```

**Nota**: Più run = più tempo (~30s/run). 5 run = ~2.5min/URL.

### Cambiare Preset (Mobile/Desktop)

Edita `lighthouserc.json` sezione `collect.settings.preset`:

```json
{
  "collect": {
    "settings": {
      "preset": "desktop"
    }
  }
}
```

## 🐛 Troubleshooting

### "Chrome not found" (CI)

Il workflow usa `browser-actions/setup-chrome@v1` che installa Chrome **fuori da snap**.

Verifica step "Setup Chrome" nel log:

```text
Chrome installed at: /opt/hostedtoolcache/chrome/...
```

### "no usable sandbox"

Mantieni `--no-sandbox` in `chromeFlags`. È safe in ambiente CI containerizzato.

### Timeout sui run

Se Lighthouse timeout su siti lenti, aumenta in `lighthouserc.json`:

```json
{
  "collect": {
    "settings": {
      "maxWaitForFcp": 45000,
      "maxWaitForLoad": 90000
    }
  }
}
```

### Assertions fallite (expected behavior)

Se il workflow fallisce con "Assertion failed", i punteggi sono **sotto soglia**.

1. Scarica artifacts
2. Apri HTML reports
3. Controlla "Opportunities" e "Diagnostics" per fix

## 📚 Documentazione Lighthouse CI

- [Lighthouse CI Docs](https://github.com/GoogleChrome/lighthouse-ci)
- [Configuration Reference](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md)
- [Assertions Guide](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/assertions.md)

## ✅ Checklist Pre-Deploy

Prima di deployare modifiche SEO/Performance, verifica:

- [ ] Workflow "Lighthouse CI Production" eseguito manualmente
- [ ] Tutti i 3 URL testati (15 report totali)
- [ ] Metriche Performance ≥80, SEO ≥95, A11y ≥90, BP ≥90
- [ ] CLS ≤ 0.1 su tutti i 5 run
- [ ] Nessun errore critico nei report Lighthouse
- [ ] Mediana dei punteggi stabile o migliorata vs. run precedente

---

**Ultimo aggiornamento**: 2025-10-12
**Maintainer**: <teo@messymind.it>
