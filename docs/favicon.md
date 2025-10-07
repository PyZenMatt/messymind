# Favicon light/dark per il tema

Questo documento spiega come funziona il sistema di favicon del tema e come sostituire le icone.

Posizione degli asset

- `assets/images/logo/fav_icon_light.svg` — favicon SVG per tema chiaro
- `assets/images/logo/fav_icon_dark.svg` — favicon SVG per tema scuro

Comportamento

Il layout include entrambi i file nel `<head>` con media query `prefers-color-scheme`. I browser moderni sceglieranno automaticamente la favicon corretta in base alla preferenza di sistema (light/dark).

Fallback

- Per user-agent legacy fornisco una piccola PNG inline come fallback (data URI) per evitare 404 su browser molto vecchi.
- `site.webmanifest` può essere aggiornato separatamente per PWA icons.

Recent change (cleanup)

The theme now exposes only three favicon entries in the `<head>` in this exact order:

1. `fav_icon_light.svg` with media `prefers-color-scheme: light`
2. `fav_icon_dark.svg` with media `prefers-color-scheme: dark`
3. fallback `favicon-32.png` (single legacy fallback, no media)

- Each href includes a version querystring `?v={{ site.github.build_revision | default: site.time | date: "%s" }}` to bust caches after deploy.

Important server requirement

- Ensure your server serves `.svg` files with `Content-Type: image/svg+xml`. On GitHub Pages this is handled automatically; on custom servers verify the MIME mapping.

How to test

- Build locally with `bundle exec jekyll build` and check generated pages under `_site` contain only the three favicon tags above.
- In DevTools > Network, reload the page and filter by `fav_icon` or `favicon-32.png` to see which asset the browser requests when emulating `prefers-color-scheme`.
- Test in Chrome/Firefox/Edge by switching the platform theme (or using DevTools rendering emulation) and force-reloading.

Notes

- Safari (standard tab) may not switch favicon reliably; this is a browser limitation. `mask-icon` is provided for pinned tabs.

Come sostituire le icone

1. Prepara due SVG quadrati con `viewBox="0 0 1024 1024"` (o equivalente) e mantieni il canvas quadrato.
2. Sovrascrivi `assets/images/logo/fav_icon_light.svg` e `fav_icon_dark.svg` con i nuovi file.
3. Se cambi i nomi, aggiorna `_includes/head.html` con i nuovi percorsi.
4. Se noti cache aggressive dopo il deploy, aggiungi querystring di versione, ad es. `?v=2` nel `href`.

Verifica

- Emula le preferenze colore in DevTools (Rendering > Emulate CSS media feature prefers-color-scheme).
- Controlla la presence del file in `_site` dopo `bundle exec jekyll build`.
- Verifica su Chrome, Firefox, Safari (macOS), e dispositivi mobili.

Note

- Lo switch avviene solo in base alle preferenze del browser/sistema; non c'è toggle UI nel tema.
