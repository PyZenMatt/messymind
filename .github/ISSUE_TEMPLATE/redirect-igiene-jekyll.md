---
name: "Redirect e Igiene Struttura Progetto Jekyll"
about: "Issue template per gestire redirect e modifiche alla struttura categorie/subcluster"
title: "[OPS] Redirect e Igiene Struttura Progetto Jekyll"
labels: [ops, redirect, hygiene]
assignees: []
---

### Clausole operative obbligatorie (da rispettare SEMPRE)

1. **Rispettare la struttura del progetto**

   - Le categorie e i subcluster sono già definiti in `pages/categories/` e `pages/categories/sub_cluster/`.
   - Non creare nuove cartelle o duplicare file esistenti: aggiornare solo quelli previsti.

2. **Informarsi prima di agire**

   - Prima di proporre modifiche, eseguire:

     - ricerca globale nel repo (escludendo `_site`, `tmp`, `node_modules`) per trovare eventuali riferimenti residui,
     - individuare se esistono già i file corretti (es. `pages/categories/<slug>.md`).
   - Solo dopo questa verifica si procede con modifiche mirate.

3. **Nessuna invenzione**

   - Non inventare nuove categorie/subcluster: usare esclusivamente quelle già elencate in `_data/category_slugs.yml` e nei file `pages/categories/`.
   - I nomi e gli slug devono rimanere coerenti con la configurazione esistente (`_config.yml`, `_data/`, mapping slug).

4. **Build e verifica locale obbligatoria**

   - Dopo ogni modifica:

     ```sh
     bundle exec jekyll build
     ```

     - Verificare che non si generino 404.
     - Controllare `_site/` per confermare la presenza del redirect o della pagina aggiornata.

5. **Output richiesto dall’agente**

   - Elenco file modificati.
   - Differenza tra stato iniziale e finale (cosa è stato cambiato).
   - Conferma che i link funzionano nel build `_site/`.

---

### Task attuale (specifico)

Verificare e mantenere attivo il redirect `categorie/mindfulness → categorie/mindfulness-ironica/`.

Non toccare altre categorie o subcluster senza prima eseguire ricerca file e confermare la presenza di quelli già esistenti.
