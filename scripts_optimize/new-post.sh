#!/bin/bash

# Script per creare e ottimizzare nuovi articoli
echo "📝 CREAZIONE NUOVO ARTICOLO OTTIMIZZATO"
echo "======================================="

# Chiedi informazioni articolo
echo "📋 Inserisci le informazioni per il nuovo articolo:"
echo ""
read -p "🏷️  Titolo: " title
read -p "📄 Descrizione breve: " description
read -p "🏷️  Categoria (felicita/spiritualita/benessere/crescita-personale/auto-consapevolezza/scienza-e-spiritualita): " category
read -p "🖼️  Nome immagine principale (senza estensione, es: nuovo-articolo): " img_name

# Genera slug e data
slug=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' | tr ' ' '-' | sed 's/--*/-/g')
date=$(date +%Y-%m-%d)
filename="_posts/${date}-${slug}.md"

# Keywords basate sulla categoria
case $category in
    "felicita")
        keywords='["felicità", "benessere", "crescita personale", "psicologia positiva"]'
        ;;
    "spiritualita")
        keywords='["spiritualità", "meditazione", "consapevolezza", "crescita interiore"]'
        ;;
    "benessere")
        keywords='["benessere", "salute mentale", "equilibrio", "lifestyle"]'
        ;;
    "crescita-personale")
        keywords='["crescita personale", "sviluppo personale", "automiglioramento", "mindset"]'
        ;;
    "auto-consapevolezza")
        keywords='["autoconsapevolezza", "introspezione", "conoscenza di sé", "mindfulness"]'
        ;;
    "scienza-e-spiritualita")
        keywords='["scienza", "spiritualità", "neuroscienze", "fisica quantistica", "filosofia"]'
        ;;
    *)
        keywords='["crescita personale", "benessere", "consapevolezza"]'
        ;;
esac

# Crea template articolo ottimizzato
cat > "$filename" << EOF
---
title: "$title"
description: "$description"
slug: /${slug}/
date: $date
author: Teo, Il Filosofo Sgualcito
keywords: $keywords
og_image: /img/${img_name}.jpg
og_alt: "$title"
background: /img/${img_name}.jpg
categories:
  - $category
tags:
  - $(echo $category | tr '-' ' ')
featured_post: false
---

# $title

{% include optimized-image.html 
   src="/img/${img_name}.jpg" 
   alt="$title"
   class="img-fluid rounded mb-4" %}

## Introduzione

$description

<!-- Inserisci qui il contenuto del tuo articolo -->

## Conclusione

Ricorda: la vera saggezza non sta nel sapere tutte le risposte, ma nel fare le domande giuste. E a volte, la domanda giusta è: "Dove ho messo il telecomando?"

---

**💡 Cosa ne pensi?** Condividi nei commenti la tua esperienza o scrivimi a [info@matteoricci.net](mailto:info@messymind.it)
EOF

echo ""
echo "✅ Articolo creato: $filename"
echo ""
echo "📋 PROSSIMI PASSI:"
echo "=================="
echo "1. 🖼️  Aggiungi l'immagine: img/${img_name}.jpg"
echo "2. ✍️  Completa il contenuto in: $filename"
echo "3. 🖼️  Ottimizza immagine: ./scripts/optimize-single-image.sh img/${img_name}.jpg"
echo "4. ✅ Preview: bundle exec jekyll serve"
echo "5. 📤 Pubblica: git add . && git commit -m 'New post: $title' && git push"

# Crea script per ottimizzare singola immagine
cat > scripts/optimize-single-image.sh << 'SCRIPT_END'
#!/bin/bash

if [ -z "$1" ]; then
    echo "❌ Uso: $0 path/to/image.jpg"
    exit 1
fi

img_path="$1"

if [ ! -f "$img_path" ]; then
    echo "❌ File non trovato: $img_path"
    exit 1
fi

echo "🖼️  Ottimizzando: $img_path"

# Ottimizza e crea WebP
convert "$img_path" -resize "1200x800>" -quality 85 -strip -interlace Plane "$img_path"
cwebp -q 85 "$img_path" -o "${img_path%.*}.webp"

echo "✅ Ottimizzazione completata!"
echo "📊 Dimensioni:"
ls -lh "$img_path" "${img_path%.*}.webp"
SCRIPT_END

chmod +x scripts/optimize-single-image.sh

echo ""
echo "🎯 SCRIPT CREATI:"
echo "================="
echo "📝 Nuovo articolo: $filename"
echo "🖼️  Ottimizzazione singola: scripts/optimize-single-image.sh"
