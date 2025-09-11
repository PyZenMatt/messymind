Panoramica
- Tipo: sito Jekyll statico, organizzato per categorie e sotto-cluster (subcluster).
- Cartelle principali: contenuti in _posts + pagine hub in `pages/categories/` (le categorie e i subcluster sono gestiti dalle pagine in questa cartella).
- Layout e include centralizzati per SEO, schema.org, cookie e template di pagina.

Struttura chiave (file e cartelle)
- Pagine categoria / subcluster (hub)
  - crescita-personale-antiguru.md
  - filosofia-pratica.md
  - spiritualita-prudente.md
  - altri hub in pages/categories/
- Post (contenuti)
  - Esempi di post: [_posts/..._]
  - Esempio: 2025-09-02-costellazioni.md
- Layouts (render delle pagine)
  - [`_layouts/post.html`]( post.html )
  - [`_layouts/category.html`]( category.html )
  - [`_layouts/subcluster.html`]( subcluster.html )
  - [`_layouts/default.html`]( default.html )
- Includes (componenti riusabili)
  - Schema / JSON-LD: [`_includes/schema-markup.html`]( schema-markup.html ), [`_includes/schema-blogposting.html`]( schema-blogposting.html ), [`_includes/schema-faq.html`]( schema-faq.html ), [`_includes/schema-howto.html`]( schema-howto.html )
  - Head, script e cookie: [`_includes/head.html`]( head.html ), [`_includes/cookie-banner.html`]( cookie-banner.html ), cookie manager incluso via cookie-manager.js (incluso inline in default layout)
- Config/metadata
  - Mappatura slug/faq: [`_data/category_faqs.yml`]( category_faqs.yml ) e altri file in _data
- Script utili
  - Creazione post: new-post.sh
  - Build/test: build.sh
- Report / tmp
  - Migrazione schema: posts-needing-migration.md
  - Controlli sitemap/urls: urls-after.txt, sitemap-diff.txt
- Policy e pagine legali
  - cookie-policy.md, privacy-policy.md

Come sono gestite categorie e subcluster
- Le pagine hub in `pages/categories/` definiscono i metadati della categoria e dei subcluster (front matter con chiavi come `category`, `subcluster`, `faq`, `intro`, `promise`). Vedi esempio in filosofia-pratica.md e in pages/categories/sub_cluster/....
- Il layout di categoria [`_layouts/category.html`]( category.html ):
  - raccoglie i post con liquid: seleziona `site.posts` filtrando su `categories` (es. `where_exp: "p", "p.categories contains cat_slug"`),
  - compone liste di “guide essenziali” cercando flag come `is_cornerstone`, tag `cornerstone`, o la proprietà `featured_slugs`.
  - rende eventuali FAQ se la pagina hub ha `faq` in front matter o se `site.data.category_faqs` contiene elementi per quella chiave.
  - genera JSON-LD CollectionPage + ItemList (vedi sezione schema).

Come vengono creati i link (regole e mapping)
- Mapping da slug a URL “amichevole”: se esiste una voce in `_data/category_slugs` (usata in vari template), viene preferita; altrimenti viene costruita con `"/" + slugify(category) + "/"`.
  - Esempio di controllo e assegnazione in [`_includes/schema-markup.html`]( schema-markup.html ) (vedi: assign category_key → site.data.category_slugs[mapped] → absolute_url).
- Link ai hub:
  - Nei template si usa il mapping o la costruzione con slug: vedi `pages/categorie.html` e [`_layouts/post.html`]( post.html ) per i link “Vai all’hub”.
- Permalink dei post: si usano le proprietà front matter (`permalink`, `slug`, `redirect_from`) se presenti; altrimenti Jekyll genera URL da path/data. Controlla i post che impostano `permalink`/`redirect_from` per redirect compatibili.
- Breadcrumb / Schema: [`_includes/schema-markup.html`]( schema-markup.html ) costruisce canonical, breadcrumbList e (se presente) CollectionPage JSON-LD con `page.collection_posts`.

Structured data / FAQ / HowTo
- Inline JSON-LD rimosso da singoli post in favore di include centralizzati:
  - BlogPosting è reso tramite [`_includes/schema-blogposting.html`]( schema-blogposting.html ) (incluso in post.html).
  - Per rendere FAQ JSON-LD aggiungi un array `faqs` nel front matter del post/pagina; l’include [`_includes/schema-faq.html`]( schema-faq.html ) lo estrae e genera JSON-LD. Vedi avviso e suggerimenti nel report posts-needing-migration.md.
  - Per HowTo analogamente aggiungi `howto` in front matter (oggetto con `name`, `description`, `totalTime`, `step[]`) e schema-howto.html lo renderà.
- Raccomandazione: usa i front matter `faqs` e `howto` (se presenti contenuti corrispondenti) per evitare JSON-LD inline e mantenere coerenza.

Onboarding tecnico rapido (passi)
1. Creare nuovo post
   - Eseguire: 
     ```sh
    ```sh
    new-post.sh
    ```
    ```
   - Lo script genera file in `_posts/...` e suggerisce immagine/ottimizzazione. Vedi [`scripts_optimize/new-post.sh`](scripts_optimize/new-post.sh).
2. Front matter minimo raccomandato (esempio)
    ```yaml
    ```yaml
    layout: post
    title: "Titolo articolo"
    date: 2025-09-XX
    categories:
      - filosofia-pratica
    subcluster: scienza-e-metodo
    tags:
      - tag1
      - tag2
    image: /img/nome-immagine.webp
    description: "Breve descrizione per SEO"
    faqs:
      - question: "Domanda?"
        answer: "Risposta."
    howto:
      name: "HowTo: 5 mosse"
      description: "Descrizione"
      totalTime: "PT10M"
      step:
        - name: "Passo 1"
          text: "Esegui X"
    ```
    ```
   - Nota: l’aggiunta di `faqs` abilita `_includes/schema-faq.html`; `howto` abilita `_includes/schema-howto.html`.
3. Immagini e ottimizzazione
   - Metti immagini in `img/` e segui le istruzioni dello script (`scripts_optimize/new-post.sh` suggerisce `img/${img_name}.jpg`). Usa conversione a webp/ottimizzazione: vedi eventuali script in `scripts/` (es. `scripts/optimize-single-image.sh` citato).
4. Build e test locale
   - Esegui:
     ```sh
    ```sh
    build.sh
    ```
    ```
   - Lo script supporta test locale (avvia simple server python se disponibile). Vedi [`scripts_optimize/build.sh`](scripts_optimize/build.sh).
5. Controlli SEO / Sitemap
   - I diff temporanei sono in `tmp/` (es. [`tmp/sitemap-diff.txt`](tmp/sitemap-diff.txt), [`tmp/urls-after.txt`](tmp/urls-after.txt)).
6. Cookie / Analytics
   - Banner cookie: [`_includes/cookie-banner.html`]( _includes/cookie-banner.html ) (collega le checkbox ai metodi `cookieManager.saveSettings()` e `cookieManager.acceptAll()`).
   - Policy: vedi [`cookie-policy.md`](cookie-policy.md) e [`privacy-policy.md`](privacy-policy.md).
   - Disattivazione GA: link in cookie-policy per opt-out; GA viene inserito tramite include in footer (`_includes/google-analytics.html` incluso da default layout).

Linee guida pratiche e checklist per pubblicazione
- Verifica front matter: title, date, categories (almeno 1), subcluster (se applicabile), description, image, seo_title/seo_description se necessario.
- Aggiungi `faqs` o `howto` in front matter se la pagina contiene Q/A o guida passo-passo (così gli include generano JSON-LD centralizzato).
- Evita JSON-LD inline nei post: usare gli include centralizzati.
- Controlla redirect in `redirect_from` se cambi URL.
- Ottimizza immagini e assegna `background` / `image` coerenti per LCP.
- Test locale: esegui `./scripts_optimize/build.sh` e controlla `/tmp` / report generati.

File utili da consultare (link rapido)
- Layouts: [`_layouts/post.html`]( _layouts/post.html ), [`_layouts/category.html`]( _layouts/category.html ), [`_layouts/subcluster.html`]( _layouts/subcluster.html ), [`_layouts/default.html`]( _layouts/default.html )
- Includes schema/SEO: [`_includes/schema-markup.html`]( _includes/schema-markup.html ), [`_includes/schema-blogposting.html`]( _includes/schema-blogposting.html ), [`_includes/schema-faq.html`]( _includes/schema-faq.html ), [`_includes/schema-howto.html`]( _includes/schema-howto.html ), [`_includes/head.html`]( _includes/head.html )
- Cookie / policy: [`_includes/cookie-banner.html`]( _includes/cookie-banner.html ), [`cookie-policy.md`](cookie-policy.md), [`privacy-policy.md`](privacy-policy.md)
- Scripts: [`scripts_optimize/new-post.sh`](scripts_optimize/new-post.sh), [`scripts_optimize/build.sh`](scripts_optimize/build.sh)
- Report migrazione schema: [`reports/posts-needing-migration.md`](reports/posts-needing-migration.md)
- Esempi hub & post: [pages/categories/filosofia-pratica.md](pages/categories/filosofia-pratica.md), [pages/categories/sub_cluster/mindfulness-ironica/spiritualita-prudente.md](pages/categories/sub_cluster/mindfulness-ironica/spiritualita-prudente.md), [_posts/filosofia_pratica/scienza-e-metodo/2025-09-02-costellazioni.md](_posts/filosofia_pratica/scienza-e-metodo/2025-09-02-costellazioni.md)

Se vuoi, posso:
- Generare un template front matter standardizzato da aggiungere nello script `new-post.sh`.
- Applicare (proposta) un controllo CI che verifica la presenza di `faqs`/`howto` quando il contenuto contiene sezioni FAQ/HowTo (analisi automatica).

GitHub Copilot   - Lo script supporta test locale (avvia simple server python se disponibile). Vedi [`scripts_optimize/build.sh`](scripts_optimize/build.sh).
5. Controlli SEO / Sitemap
   - I diff temporanei sono in `tmp/` (es. [`tmp/sitemap-diff.txt`](tmp/sitemap-diff.txt), [`tmp/urls-after.txt`](tmp/urls-after.txt)).
6. Cookie / Analytics
   - Banner cookie: [`_includes/cookie-banner.html`]( _includes/cookie-banner.html ) (collega le checkbox ai metodi `cookieManager.saveSettings()` e `cookieManager.acceptAll()`).
   - Policy: vedi [`cookie-policy.md`](cookie-policy.md) e [`privacy-policy.md`](privacy-policy.md).
   - Disattivazione GA: link in cookie-policy per opt-out; GA viene inserito tramite include in footer (`_includes/google-analytics.html` incluso da default layout).

Linee guida pratiche e checklist per pubblicazione
- Verifica front matter: title, date, categories (almeno 1), subcluster (se applicabile), description, image, seo_title/seo_description se necessario.
- Aggiungi `faqs` o `howto` in front matter se la pagina contiene Q/A o guida passo-passo (così gli include generano JSON-LD centralizzato).
- Evita JSON-LD inline nei post: usare gli include centralizzati.
- Controlla redirect in `redirect_from` se cambi URL.
- Ottimizza immagini e assegna `background` / `image` coerenti per LCP.
- Test locale: esegui `./scripts_optimize/build.sh` e controlla `/tmp` / report generati.

File utili da consultare (link rapido)
- Layouts: [`_layouts/post.html`]( _layouts/post.html ), [`_layouts/category.html`]( _layouts/category.html ), [`_layouts/subcluster.html`]( _layouts/subcluster.html ), [`_layouts/default.html`]( _layouts/default.html )
- Includes schema/SEO: [`_includes/schema-markup.html`]( _includes/schema-markup.html ), [`_includes/schema-blogposting.html`]( _includes/schema-blogposting.html ), [`_includes/schema-faq.html`]( _includes/schema-faq.html ), [`_includes/schema-howto.html`]( _includes/schema-howto.html ), [`_includes/head.html`]( _includes/head.html )
- Cookie / policy: [`_includes/cookie-banner.html`]( _includes/cookie-banner.html ), [`cookie-policy.md`](cookie-policy.md), [`privacy-policy.md`](privacy-policy.md)
- Scripts: [`scripts_optimize/new-post.sh`](scripts_optimize/new-post.sh), [`scripts_optimize/build.sh`](scripts_optimize/build.sh)
- Report migrazione schema: [`reports/posts-needing-migration.md`](reports/posts-needing-migration.md)
- Esempi hub & post: [pages/categories/filosofia-pratica.md](pages/categories/filosofia-pratica.md), [pages/categories/sub_cluster/mindfulness-ironica/spiritualita-prudente.md](pages/categories/sub_cluster/mindfulness-ironica/spiritualita-prudente.md), [_posts/filosofia_pratica/scienza-e-metodo/2025-09-02-costellazioni.md](_posts/filosofia_pratica/scienza-e-metodo/2025-09-02-costellazioni.md)

Se vuoi, posso:
- Generare un template front matter standardizzato da aggiungere nello script `new-post.sh`.
- Applicare (proposta) un controllo CI che verifica la presenza di `faqs`/`howto` quando il contenuto contiene sezioni FAQ/HowTo (analisi automatica).