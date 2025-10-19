# ✅ LHCI su Produzione — Implementazione Completata

## 🎯 Obiettivo Raggiunto

Sistema automatizzato Lighthouse CI che esegue **5 run mobile** su **produzione** per 3 URL rappresentativi, bypassa limitazioni Chromium snap, applica quality gates, e salva 30 report (15 HTML + 15 JSON) come artifacts GitHub Actions.

## 📦 Deliverable

### File Creati/Modificati

1. **lighthouserc.json** (new)
   - 5 run mobile per URL
   - 3 URL produzione: home, category burnout, post stress
   - Quality gates: Perf ≥80, SEO ≥95, A11y ≥90, BP ≥90, CLS ≤0.1
   - Upload filesystem → `.lighthouseci/`

2. **.github/workflows/lhci.yml** (modified)
   - `browser-actions/setup-chrome@v1` (bypass snap)
   - Trigger: manual dispatch, push, schedule domenica 2 AM
   - Steps: setup-chrome → npm ci → lhci autorun → upload artifacts
   - Summary automatico con Node/Chrome versions

3. **docs/lighthouse-qa.md** (new)
   - Documentazione completa: comandi, soglie, lettura 5 run
   - Troubleshooting: Chrome not found, no sandbox, timeout
   - **Nessun riferimento PSI/API Google**

4. **package.json** + **package-lock.json** (updated)
   - `@lhci/cli: ^0.15.1` già presente

5. **docs/ISSUE-LIGHTHOUSE-CI-PRODUCTION.md** (new)
   - Issue completa con contesto, modifiche, DoD, troubleshooting, next steps

### Commit

```bash
03b0c5f — feat(qa): Lighthouse CI ×5 mobile runs su produzione
```

**Branch**: `feat/layout-category-subcluster`
**Status**: Pushed to remote ✅

## 🚀 Come Testare

### 1. Trigger Workflow Manualmente

```bash
# Da GitHub UI
Actions → "Lighthouse CI Production" → Run workflow
```

**Oppure** attendi il primo push (già fatto) → workflow si attiva automaticamente.

### 2. Monitorare Esecuzione

- Step "Setup Chrome" → Verifica path `/opt/hostedtoolcache/chrome/...`
- Step "Display Chrome version" → Conferma versione stabile
- Step "Run Lighthouse CI" → Leggi output 5 run × 3 URL
- Step "Upload artifacts" → 30 file caricati

### 3. Scaricare Report

- Scorri a "Artifacts" section
- Download `lighthouse-reports-<run_number>.zip`
- Estrai → 15 HTML (visuali) + 15 JSON (raw data)

### 4. Analizzare Punteggi

Apri HTML report per ogni URL:

- **Home**: 5 run → identifica mediana Performance
- **Category**: 5 run → verifica SEO ≥95
- **Post**: 5 run → controlla Accessibility ≥90

Se **tutte** le soglie OK → Job verde ✅
Se **una** soglia fail → Job rosso ❌ (expected, non bug)

## 📊 Metriche Attese

| Metrica | Soglia Mobile | Note |
|---------|---------------|------|
| Performance | ≥ 80 | Lab data, non utenti reali |
| SEO | ≥ 95 | Struttura semantic, meta, robots |
| Accessibility | ≥ 90 | ARIA, contrast, alt text |
| Best Practices | ≥ 90 | HTTPS, console errors, deprecations |
| CLS | ≤ 0.1 | Cumulative Layout Shift |

**Nota**: Se i punteggi reali sono stabilmente sotto le soglie (es. Perf 75-78), è OK abbassare le soglie in `lighthouserc.json` per riflettere la baseline reale. L'obiettivo è **tracking trends** nel tempo, non perfection score.

## 🐛 Troubleshooting Quick Reference

| Problema | Soluzione |
|----------|-----------|
| "Chrome not found" | Workflow usa `browser-actions/setup-chrome@v1` → verifica step log |
| "no usable sandbox" | Mantieni `--no-sandbox` in `chromeFlags` (safe in CI) |
| Timeout run | Aumenta `maxWaitForLoad` in `lighthouserc.json` |
| Assertions failed | Expected se punteggi sotto soglia → analizza report HTML |
| Artifacts vuoti | Verifica `.lighthouseci/` directory creata in step log |

## 📚 Documentazione

- **Setup**: `docs/lighthouse-qa.md`
- **Issue**: `docs/ISSUE-LIGHTHOUSE-CI-PRODUCTION.md`
- **Config**: `lighthouserc.json`
- **Workflow**: `.github/workflows/lhci.yml`

## 🎁 Bonus Features

### Schedule Settimanale

```yaml
schedule:
  - cron: '0 2 * * 0'  # Domenica 2 AM UTC
```

Report automatici ogni settimana per tracking long-term trends.

### Manual Dispatch

Trigger on-demand quando serve:

```bash
Actions → Lighthouse CI Production → Run workflow
```

Utile dopo deploy major o fix performance.

### Artifacts Retention

```yaml
retention-days: 30
```

30 giorni di report disponibili per analisi retrospettive.

## ✅ Definition of Done

- [x] **A)** Dipendenze dev: `@lhci/cli` presente
- [x] **B)** Config LHCI: 5 run mobile, URL produzione, filesystem upload
- [x] **C)** Workflow: setup-chrome, npm ci, lhci autorun, artifacts
- [x] **D)** Output: 30 file artifacts (15 HTML + 15 JSON)
- [x] **E)** Docs: `lighthouse-qa.md` completo, nessun PSI
- [x] **Commit**: Push su `feat/layout-category-subcluster`
- [ ] **Test**: Workflow eseguito con successo (prossimo step)

## 🚦 Next Action

**Monitora GitHub Actions tab** per vedere il primo run automatico triggerato dal push.

Expected timeline: ~3-5 minuti (15 run totali @ ~20s/run)

---

**Data**: 2025-10-12
**Commit**: `03b0c5f`
**Status**: ✅ Ready for testing
