# Analisi Struttura Stili MessyMind.it

## 📊 Organizzazione Attuali

### File Entry Point
- **`/assets/main.scss`** - File principale che importa tutto (FONDAMENTALE)

### Struttura Gerarchica Import
```
assets/main.scss
├── styles (bootstrap-purged bootstrap base)
├── custom-purged
├── messymind-variables (VARIABILI COLORI E FONT)
├── messymind-base
├── messymind-utilities
├── messymind-components (componenti reutilizzabili)
├── [NEW] components/newsletter-form (form newsletter)
├── messymind-overrides (override specificity)
├── mobile-fixes
└── pages/
    ├── [NEW] pages/home (home page specific)
    └── pages/category (category page specific)
```

## 🏗️ Livelli di Cascata CSS

1. **Bootstrap Purged** - Base framework
2. **MessyMind Variables** - Design tokens (colori, spacing, font)
3. **MessyMind Base** - Reset e base styles
4. **MessyMind Components** - Componenti globali reutilizzabili
5. **Component-Specific** - newsletter-form.scss (specifico al component)
6. **MessyMind Overrides** - Override a specificità alta
7. **Mobile Fixes** - Override mobile-first
8. **Page-Specific** - Stili per pagine specifiche (home, category)

## 📁 Dove Aggiungere Stili Nuovi

| Tipo di Stile | File | Uso |
|---|---|---|
| Variabili design globali | `_sass/_messymind-variables.scss` | Colori, font, spacing ricorrenti |
| Componenti reutilizzabili (button, card, etc) | `_sass/_messymind-components.scss` | Componenti usati in + pagine |
| Specifico per pagina home | `_sass/pages/_home.scss` | Stili solo della home |
| Specifico per pagina category | `_sass/pages/_category.scss` | Stili solo category |
| Nuovo component specifico | `_sass/components/_[name].scss` | Componenti con stili propri |

## 🎨 Newsletter - Caso di Studio

### PRIMA (❌ Sbagliato)
- CSS inline in `_layouts/home.html` (section newsletter)
- CSS inline in `_includes/newsletter-form.html` (form)
- Difficile da mantenere, duplicato, tema non coerente

### DOPO (✅ Corretto)
- **Stili section:** `_sass/pages/_home.scss`
- **Stili form:** `_sass/components/_newsletter-form.scss`
- **Import in:** `assets/main.scss`
- HTML pulito, CSS centralizzato, tema coerente

## 🎯 Regole di Buona Pratica

✅ **DO:**
- CSS va nei file SCSS, mai inline negli HTML
- Usare variabili per colori ricorrenti
- Componenti reutilizzabili in `_messymind-components.scss`
- Stili pagina-specifici in `pages/`
- Tema light/dark gestito con `@media (prefers-color-scheme)` + `html[data-theme]`

❌ **DON'T:**
- CSS inline negli HTML
- Colori hardcoded (usare variabili)
- Stili specifici pagina in _components.scss
- Dimenticare di aggiungere import in `assets/main.scss`

## 🌓 Tema Light/Dark - Ordine di Precedenza

```scss
// 1. Default (tema chiaro fallback)
.elemento { color: #000; }

// 2. Sistema (se utente a sistema preferisce dark)
@media (prefers-color-scheme: dark) {
  .elemento { color: #fff; }
}

// 3. Toggle manuale (override sistema)
html[data-theme='light'] {
  .elemento { color: #000; } // Force light
}

html[data-theme='dark'] {
  .elemento { color: #fff; } // Force dark
}
```

**Importante:** `html[data-theme]` ha priorità su `@media (prefers-color-scheme)` perché ne è più specifico.
