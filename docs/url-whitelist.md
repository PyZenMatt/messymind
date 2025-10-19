# URL whitelist per slug/permalink

Questa whitelist documenta i file che mantengono `slug:` o `permalink:` hardcoded per motivi storici (link esterni, campagne, redirect legacy).

Formato: una riga per file con motivazione.

Esempio:
- `_posts/crescita_personale_antiguru/desiderio-e-rinuncia/2025-03-31-il-risveglio-interiore.md` — numerosi link esterni e citazioni; mantenere slug storico per 6 mesi dopo la pulizia.

Attenzione: la whitelist deve essere minima. Aggiungi qui i file da esentare prima della fase `--apply`.
