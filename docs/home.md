# Home Hub - Information Architecture

## Goal
Hub editoriale pulito con **1 solo hero**, navigazione cluster-centrica, zero duplicazioni above-the-fold.

## Flow Target
**Hero → Intro → Temi → Ultimi → Cornerstone → CTA**

## Sezioni

### 1. Hero (above-the-fold)
- **1 featured post** selezionato via governance
- H1 unico
- Intro breve (80-120 parole) con 2 link cluster
- LCP-optimized: 1600w WebP, preload allineato

### 2. Temi principali (cluster navigation)
- **H2**: "Temi principali" 
- 4 cluster con micro-descrizioni (20-30 parole)
- Link diretti a `/categorie/{cluster}/`
- Unico strato di navigazione topic-based

### 3. Ultimi articoli
- **H2**: "Ultimi Articoli"
- 6-8 post compatti **escludendo** il featured
- Schema.org `ItemList`
- Link a archivio completo

### 4. Cornerstone consigliati (below-the-fold)
- **H2**: "Cornerstone consigliati"  
- 3 card con post-pilastro
- Selezione editoriale manuale

### 5. CTA (optional)
- Newsletter signup o call-to-action principale

## Governance Featured

```yaml
# In front-matter:
featured_post: true
featured_rank: 1  # Optional: 1=highest priority
```

**Regole**:
1. Se >1 featured: prende `featured_rank` più basso, poi più recente
2. Se 0 featured: fallback al più recente del cluster principale
3. "Ultimi" **esclude** sempre il featured selezionato

## Schema.org Strategy

- **WebPage** unico per la home
- **ItemList** solo su sezione "Ultimi" 
- Nessun duplicato BreadcrumbList
- Rich Results validation: verde

## Performance Targets

- **LCP**: ≤ 2.5s (mobile lab)
- **CLS**: ≤ 0.02  
- **SEO**: ≥95 (Lighthouse mobile)
- **A11y**: ≥90
- **Best Practices**: ≥90

## Deduplication Rules

**REMOVE**:
- Blocco "Categorie" automatico duplicato
- Link ripetuti above-the-fold
- H2 duplicati per topic

**KEEP**:
- Solo "Temi principali" come cluster navigation
- Featured unico in hero
- "Ultimi" filtrati (senza featured)

## Viewport Constraints

- **320px**: Mobile portrait (testo contenuto)
- **768px**: Tablet breakpoint 
- **1440px**: Desktop max-width
- **Hero**: nessun overflow, wrapping garantito