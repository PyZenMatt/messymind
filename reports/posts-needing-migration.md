# Report: Post needing manual migration of structured data

Generated: 2025-09-10

This report lists posts where inline JSON-LD was removed and a manual front-matter migration is recommended.

For each entry:
- path
- title (from front matter when present)
- front matter excerpt
- comment/snippet left by automated cleanup
- recommendation (faqs/howto front matter shape)

---
 
## 1) /_posts/filosofia_pratica/decisioni-e-bias/libero-arbitrio.md

Title: Libero arbitrio e determinismo: guida semplice (compatibilismo, Libet, Schurger)

Front matter excerpt:

```yaml
categories:
- filosofia-pratica
title: 'Libero arbitrio e determinismo: guida semplice (compatibilismo, Libet, Schurger)'
og_image: /assets/libero-arbitrio-cover.webp
updated: '2025-09-08'
---
```

Cleanup note (context):

```liquid
{%- comment -%} Inline BlogPosting/FAQ JSON-LD removed. Use `_includes/schema-blogposting.html` for BlogPosting and add `faqs` in front matter to render FAQ JSON-LD via `_includes/schema-faq.html`.
{%- endcomment -%}
```

Recommendation: If this post contains a FAQ section, add to front matter:

```yaml
faqs:
- question: "Prima domanda FAQ..."
	answer: "Risposta..."
# ...
```

---

## 2) /_posts/filosofia_pratica/decisioni-e-bias/bias-cognitivi.md

Title: (from front matter: none explicit 'title' key — use filename)

Front matter excerpt:

```yaml
author: Redazione MessyMind
categories:
- filosofia-pratica
date: '2025-09-09'
description: Definizione chiara, 10 esempi reali e 3 tecniche di debiasing pratiche
image: /images/bias-cognitivi-2025-og.jpg
```

Cleanup note (context):

```liquid
{%- comment -%} Inline BlogPosting/FAQ JSON-LD removed. BlogPosting will be rendered by `_includes/schema-blogposting.html`. To render FAQs, add `faqs` array in front matter and `_includes/schema-faq.html` will output JSON-LD.
{%- endcomment -%}
```

Recommendation: Add `faqs` front matter if the post includes an FAQ block; otherwise no immediate action required.

---

## 3) /_posts/filosofia_pratica/coscienza-e-ai/2025-09-10-faggin-ia-non-cosciente.md

Title: IA cosciente? Per Faggin è un’illusione (2025)

Front matter excerpt: (top keys)

```yaml
layout: post
lang: it-IT
title: IA cosciente? Per Faggin è un’illusione (2025)
description: 'Perché secondo Federico Faggin l''IA non capirà mai davvero...'
image: https://res.cloudinary.com/...
author: MessyMind
featured_post: true
```

Cleanup note (context):

```liquid
<!-- Schema.org: BlogPosting -->
{%- comment -%} Inline BlogPosting and FAQ JSON-LD removed from this post. BlogPosting will be rendered via `_includes/schema-blogposting.html` (included in the post layout). If you want FAQ structured data, add a `faqs` array in the post front matter and it will be rendered via `_includes/schema-faq.html`.
{%- endcomment -%}
```

Recommendation: If the article contains Q/A or reader questions, add `faqs` to front matter; otherwise ok.

---

## 4) /_posts/filosofia_pratica/coscienza-e-ai/2025-09-12-federico-faggin-qip-seita.md

Title: (from front matter if present)

Cleanup note (context):

```
<!-- Inline BlogPosting/FAQ JSON-LD removed from this post. BlogPosting is provided by `_includes/schema-blogposting.html` in the post layout. Add `faqs` front matter to render FAQ JSON-LD via `_includes/schema-faq.html`. -->
```

Recommendation: Add `faqs` front matter for FAQ blocks.

---

## 5) /_posts/filosofia_pratica/scienza-e-metodo/riduzionismo.md

Cleanup note (context):

```liquid
{%- comment -%} Inline BlogPosting/FAQ JSON-LD removed; use `_includes/schema-blogposting.html` for post schema and `_includes/schema-faq.html` when `faqs` exist in front matter.
{%- endcomment -%}
```

Recommendation: Add `faqs` front matter if FAQ content is present.

---

## 6) /_posts/mindfulness_ironica/spiritualita-prudente/2025-05-11-kundalini.md

Cleanup note (context):

```liquid
{%- comment -%} Inline BlogPosting/FAQ JSON-LD removed. BlogPosting will be rendered by `_includes/schema-blogposting.html`. If this post has FAQs, add them to front matter as `faqs` to render via `_includes/schema-faq.html`.
{%- endcomment -%}
```

Recommendation: Add `faqs` front matter if applicable.

---

## 7) /_posts/filosofia_pratica/scienza-e-metodo/2025-02-18-e-mc2-spiritualita-verita-scomoda.md

Cleanup note (context):

```html
<!-- Inline BlogPosting/FAQ JSON-LD removed. BlogPosting included via `_includes/schema-blogposting.html`; add `faqs` in front matter to render FAQ JSON-LD via `_includes/schema-faq.html`. -->
```

Recommendation: Manual check; update front matter `faqs` if needed.

---

## 8) /_posts/mindfulness_ironica/equilibrio-per-persone-normali/2024-10-13-la-felicita-non-è-un-linkedin-post.md

Cleanup note (context):

```liquid
{%- comment -%} Inline BlogPosting/FAQ JSON-LD removed. Use `_includes/schema-blogposting.html` for the post and `_includes/schema-faq.html` when adding `faqs` to front matter.
{%- endcomment -%}
```

Additionally this post originally included a HowTo JSON-LD; recommendation: move HowTo into front matter:

```yaml
# howto:
#   name: "Equilibrio interiore in 10 minuti: 5 mosse anti-guru"
#   description: "Cinque esercizi brevi..."
#   totalTime: "PT10M"
#   step:
#     - name: "Camminata consapevole"
#       text: "Per 5 minuti..."
# ...
```

---

### Notes

This report intentionally leaves the content of each post untouched. The comments inserted are guidance for manual migration.

Next step (optional): I can either attempt an automated migration to create `faqs` / `howto` front matter, or leave this as a manual checklist. Automated migration risks imperfect parsing; manual is safer.


---


