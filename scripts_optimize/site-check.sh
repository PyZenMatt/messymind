#!/bin/bash

# Script di verifica completo per messymind.it
echo "🔍 VERIFICA COMPLETA SITO"
echo "========================="

# Funzione per colorare output
green() { echo -e "\033[32m$1\033[0m"; }
red() { echo -e "\033[31m$1\033[0m"; }
yellow() { echo -e "\033[33m$1\033[0m"; }

echo ""
echo "📊 1. CONTROLLO PERFORMANCE"
echo "==========================="

# Build Jekyll pulito
echo "🔨 Build Jekyll..."
bundle exec jekyll build --quiet

if [ $? -eq 0 ]; then
    green "✅ Build Jekyll: OK"
else
    red "❌ Build Jekyll: ERRORE"
    exit 1
fi

# Verifica immagini WebP
webp_count=$(find img -name "*.webp" | wc -l)
jpg_count=$(find img -name "*.jpg" -o -name "*.jpeg" | wc -l)

echo "🖼️  Immagini WebP: $webp_count"
echo "🖼️  Immagini JPEG/JPG: $jpg_count"

if [ "$webp_count" -gt 0 ]; then
    green "✅ WebP: Ottimizzato"
else
    yellow "⚠️  WebP: Da ottimizzare"
fi

echo ""
echo "📝 2. CONTROLLO CONTENUTI"
echo "========================="

# Verifica link interni rotti
echo "🔗 Verificando link interni..."
broken_links=0

for post in _posts/*.md; do
    if [ -f "$post" ]; then
        # Estrai link immagini
        grep -o 'src="[^"]*"' "$post" | sed 's/src="\([^"]*\)"/\1/' | while read img_path; do
            # Rimuovi / iniziale se presente
            clean_path="${img_path#/}"
            if [ ! -f "$clean_path" ] && [ ! -f "img/${clean_path#img/}" ]; then
                echo "❌ Link rotto in $post: $img_path"
                ((broken_links++))
            fi
        done
    fi
done

if [ "$broken_links" -eq 0 ]; then
    green "✅ Link immagini: OK"
else
    red "❌ Link rotti trovati: $broken_links"
fi

echo ""
echo "🔧 3. CONTROLLO CONFIGURAZIONE"
echo "=============================="

# Verifica critical CSS
if [ -f "_includes/critical-css.html" ]; then
    green "✅ Critical CSS: Presente"
else
    red "❌ Critical CSS: Mancante"
fi

# Verifica compressione
if grep -q "compress_html" _config.yml; then
    green "✅ Compressione HTML: Attiva"
else
    yellow "⚠️  Compressione HTML: Non configurata"
fi

# Verifica ottimizzazioni head
if grep -q "optimized-image.html" _layouts/*.html; then
    green "✅ Template ottimizzati: OK"
else
    yellow "⚠️  Template: Da ottimizzare"
fi

echo ""
echo "📱 4. TEST LOCALE"
echo "================="

# Avvia server temporaneo per test
echo "🚀 Avviando server temporaneo..."
bundle exec jekyll serve --port 4001 --detach --quiet

sleep 3

# Test basic connectivity
if curl -s http://localhost:4001 > /dev/null; then
    green "✅ Server locale: Attivo"
    
    # Test velocità caricamento
    load_time=$(curl -o /dev/null -s -w '%{time_total}' http://localhost:4001)
    if (( $(echo "$load_time < 2.0" | bc -l) )); then
        green "✅ Velocità caricamento: ${load_time}s (OK)"
    else
        yellow "⚠️  Velocità caricamento: ${load_time}s (Lenta)"
    fi
else
    red "❌ Server locale: Non raggiungibile"
fi

# Ferma server
pkill -f "jekyll.*4001" 2>/dev/null

echo ""
echo "📊 5. RIEPILOGO"
echo "==============="

size_before="N/A"
size_after=$(du -sh img 2>/dev/null | cut -f1)

if [ -d "img_backup" ]; then
    size_before=$(du -sh img_backup 2>/dev/null | cut -f1)
    echo "📦 Dimensioni immagini: $size_before → $size_after"
else
    echo "📦 Dimensioni immagini attuali: $size_after"
fi

echo "🔄 Ultimo controllo: $(date)"

echo ""
echo "🎯 AZIONI SUGGERITE:"
echo "===================="
echo "✅ 1. Test online: https://pagespeed.web.dev/analysis?url=https://messymind.it"
echo "📊 2. Audit completo: ./scripts/performance-audit.sh"
echo "🧹 3. Pulizia immagini: ./scripts/cleanup-unused-images.sh"
echo "📝 4. Nuovo articolo: ./scripts/new-post.sh"
