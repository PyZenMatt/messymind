# Lighthouse ×5 run su produzione via CI (fix Chromium snap)

## 🎯 Contesto

Chromium installato via **snap** su Ubuntu blocca Lighthouse locale a causa di limitazioni di sicurezza. Il browser headless non può essere lanciato da Lighthouse CLI/LHCI.

**Decisione**: Spostare tutti i run Lighthouse in **GitHub Actions** con Chrome dedicato installato via `browser-actions/setup-chrome@v1` (bypass snap).

**Obiettivo**: Eseguire **5 run mobile** per 3 URL di produzione, salvare report HTML+JSON come artifacts, applicare quality gates.

## 👤 Ruolo Agente

**QA Performance Runner**

- Esegue Lighthouse CI su produzione (messymind.it)
- Genera 15 report (5 run × 3 URL) con mediana automatica
- Salva artifacts per analisi manuale
- Applica soglie e blocca workflow se fail

## 📥 Input Richiesti

### Production Base URL

```text
https://messymind.it
```

### Lista URL Testati (Minimo 3)

1. **Home**: `/` — Landing principale, hero, cluster grid
2. **Category v2**: `/categorie/burnout-e-lavoro/` — Hero, topics, guide essenziali, subcluster
3. **Post**: `/2025/09/29/stress-correlato/` — Layout articolo, sidebar, related

**Facoltativo**: Aggiungi più URL (es. altre category, subclusters) modificando `lighthouserc.json`

## 🔧 Modifiche Implementate (A→E)

### A) Dipendenze Dev

✅ **Completato**

```json
// package.json
{
  "devDependencies": {
    "@lhci/cli": "^0.15.1"
  }
}
```

### B) Config LHCI (lighthouserc.json)

✅ **Completato**

```json
{
  "ci": {
    "collect": {
      "numberOfRuns": 5,
      "url": [
        "https://messymind.it/",
        "https://messymind.it/categorie/burnout-e-lavoro/",
        "https://messymind.it/2025/09/29/stress-correlato/"
      ],
      "settings": {
        "preset": "mobile",
        "chromeFlags": "--headless=new --no-sandbox",
        "maxWaitForFcp": 30000,
        "maxWaitForLoad": 60000
      }
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.80}],
        "categories:seo": ["error", {"minScore": 0.95}],
        "categories:accessibility": ["error", {"minScore": 0.90}],
        "categories:best-practices": ["error", {"minScore": 0.90}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}]
      }
    },
    "upload": {
      "target": "filesystem",
      "outputDir": ".lighthouseci"
    }
  }
}
```

### C) Workflow GitHub Actions (.github/workflows/lhci.yml)

✅ **Completato**

**Key Features**:

- `runs-on: ubuntu-latest`
- `setup-node@v4` (Node 20)
- `browser-actions/setup-chrome@v1` (Chrome stabile, **no snap**)
- `npm ci` → `lhci autorun`
- Assertions con soglie: Perf ≥80, SEO ≥95, A11y ≥90, BP ≥90, CLS ≤0.1
- Upload artifacts: `.lighthouseci/*.{html,json}` (retention 30 giorni)
- Summary automatico con Node/Chrome versions

**Triggers**:

- `workflow_dispatch` (manuale)
- `push` su branch `feat/layout-category-subcluster`
- `schedule: '0 2 * * 0'` (domenica 2 AM UTC)

### D) Output Repository

✅ **Completato**

**Artifacts GitHub Actions**:

```text
lighthouse-reports-<run_number>.zip
├── .lighthouseci/
    ├── lh_<hash_home>_1.html
    ├── lh_<hash_home>_1.json
    ... (5 run home)
    ├── lh_<hash_category>_1.html
    ... (5 run category)
    ├── lh_<hash_post>_1.html
    ... (5 run post)
```

**Totale**: 30 file (15 HTML + 15 JSON)

**Download**: Actions → Workflow run → Artifacts section

**Optional copy to repo**: Step "Copy reports with timestamp" salva anche in `docs/evidence/lighthouse/<YYYY-MM-DD>/` (non committato, solo per riferimento locale)

### E) Documentazione

✅ **Completato** — `docs/lighthouse-qa.md`

**Sezioni**:

- Comandi: `npx lhci autorun --config=lighthouserc.json`
- Soglie: Tabella quality gates mobile
- Posizione report: `.lighthouseci/` + GitHub Artifacts
- Come leggere i 5 run: Mediana automatica + lettura manuale HTML
- Nota: Run di laboratorio (GitHub Actions runner), non utenti reali
- **Nessun riferimento a PSI/API Google Cloud**

## ✅ Acceptance Criteria (DoD)

### 1. Job CI Verde

- [ ] Workflow "Lighthouse CI Production" eseguito con successo
- [ ] Tutte le assertions passate (nessun errore rosso)
- [ ] Step "Run Lighthouse CI" completato

### 2. Chrome Rilevato Senza Snap

- [ ] Log contiene `Chrome installed at: /opt/hostedtoolcache/chrome/...`
- [ ] **NON** contiene riferimenti a `/snap/chromium/...`
- [ ] Chrome version stampata correttamente (es. "Google Chrome 120.0.6099.109")

### 3. Per Ogni URL: 5 HTML + 5 JSON

- [ ] Artifacts contengono 30 file totali (15 HTML + 15 JSON)
- [ ] File nominati: `lh_<hash>_<run>.html` e `.json`
- [ ] Ogni URL ha esattamente 5 coppie HTML+JSON

### 4. Soglie Rispettate o Job Fallisce

Se **tutte** le soglie rispettate:

- [ ] Job status: ✅ Green
- [ ] Log: "All assertions passed"

Se **una** soglia non rispettata:

- [ ] Job status: ❌ Red
- [ ] Log: "Assertion failed: categories:performance..."
- [ ] Expected behavior (non è un bug)

### 5. Log Contiene Versioni Node e Chrome

- [ ] Step "Display Node version": `v20.x.x`
- [ ] Step "Display Chrome version": `Google Chrome 1xx.x.xxxx.xx`
- [ ] Summary section mostra entrambe le versioni

### 6. Nessun Riferimento a PSI/API Google Cloud

- [ ] Nessun step che chiama `https://www.googleapis.com/pagespeedonline/...`
- [ ] Nessuna variabile `GOOGLE_CLOUD_API_KEY`
- [ ] Documentazione non menziona PageSpeed Insights API
- [ ] Config usa solo `lhci autorun` (Lighthouse bundled)

## 🐛 Troubleshooting Noto

### "Chrome not found"

**Soluzione**: Workflow usa `browser-actions/setup-chrome@v1` che fornisce `CHROME_PATH`.

Verifica step "Setup Chrome":

```bash
Chrome installed at: /opt/hostedtoolcache/chrome/...
```

Se missing, aggiungi env var esplicitamente:

```yaml
env:
  CHROME_PATH: ${{ steps.setup-chrome.outputs.chrome-path }}
```

### "no usable sandbox"

**Soluzione**: Mantieni `--no-sandbox` in `chromeFlags`. È **safe** in ambiente CI containerizzato.

**NON rimuovere** `--no-sandbox` o il job fallirà con errore sandbox.

### Timeout su Run

Se Lighthouse timeout su siti lenti (>60s load):

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

Aumenta progressivamente fino a completamento.

## 🚀 Prossimi Step

### 1. Verifica Workflow

- [ ] Vai su **GitHub Actions** → "Lighthouse CI Production"
- [ ] Clicca "Run workflow" → "Run workflow" (manuale trigger)
- [ ] Attendi ~3-5 minuti (5 run × 3 URL = ~15 run totali)

### 2. Controlla Log

- [ ] Espandi step "Setup Chrome" → Verifica path `/opt/hostedtoolcache/...`
- [ ] Espandi step "Display Chrome version" → Conferma versione
- [ ] Espandi step "Run Lighthouse CI" → Leggi output LHCI

### 3. Scarica Artifacts

- [ ] Scorri in basso a "Artifacts" section
- [ ] Download `lighthouse-reports-<run_number>.zip`
- [ ] Estrai ZIP → Verifica 30 file presenti

### 4. Analizza Report

- [ ] Apri 5 HTML per home → Confronta punteggi Performance
- [ ] Identifica **mediana** (es. Run 3 se ordinato)
- [ ] Controlla "Opportunities" per fix eventuali

### 5. Aggiorna Soglie (se necessario)

Se i punteggi sono **stabilmente sotto** le soglie attuali (es. Performance sempre 75-78):

- [ ] Edita `lighthouserc.json` → `minScore: 0.75`
- [ ] Commit + push
- [ ] Rirun workflow

**Nota**: Abbassare le soglie è OK se riflette la realtà del sito. L'obiettivo è **tracking trends**, non score perfetto.

## 📊 Metriche di Successo

- ✅ **15 report HTML** generati (visuali, human-readable)
- ✅ **15 report JSON** generati (parsabili, automation-ready)
- ✅ **Mediana calcolata** automaticamente da LHCI
- ✅ **Workflow verde** se soglie OK (o rosso se fail → expected)
- ✅ **Chrome .deb** installato (no snap issues)
- ✅ **Schedule attivo** (run settimanale domenica 2 AM)

## 🎁 Bonus (Opzionale)

### Aggiungere Altri URL

Edita `lighthouserc.json`:

```json
{
  "collect": {
    "url": [
      "https://messymind.it/",
      "https://messymind.it/categorie/burnout-e-lavoro/",
      "https://messymind.it/2025/09/29/stress-correlato/",
      "https://messymind.it/categorie/mindfulness-ironica/",
      "https://messymind.it/subclusters/burnout-e-lavoro/ritmi-gentili/"
    ]
  }
}
```

**Costo tempo**: +2-3 min per ogni 5 run aggiuntivi

### Confrontare Desktop vs Mobile

Crea secondo workflow `lhci-desktop.yml` con:

```json
{
  "settings": {
    "preset": "desktop"
  }
}
```

Rename artifacts: `lighthouse-reports-desktop-<run_number>`

### Tracking Trends

Salva i JSON in repo:

```bash
# In workflow dopo lhci
git config user.name "GitHub Actions"
git add docs/evidence/lighthouse/$(date +%Y-%m-%d)/*.json
git commit -m "chore: Lighthouse reports $(date +%Y-%m-%d)"
git push
```

Poi usa tool tipo `lighthouse-ci-diff` per comparare settimane.

---

## 📌 Status Implementazione

**Branch**: `feat/layout-category-subcluster`
**Commit**: `03b0c5f` — "feat(qa): Lighthouse CI ×5 mobile runs su produzione"
**Files Changed**:

- `lighthouserc.json` (new)
- `.github/workflows/lhci.yml` (modified)
- `docs/lighthouse-qa.md` (new)
- `package.json` + `package-lock.json` (updated)

**Next**: Push triggerò automaticamente il primo run. Monitorare Actions tab.
