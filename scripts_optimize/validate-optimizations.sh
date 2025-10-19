#!/bin/bash

# Validazione finale ottimizzazioni messymind.it
echo "✅ VALIDAZIONE OTTIMIZZAZIONI"
echo "============================="

echo "📊 CONTROLLO IMMAGINI:"
echo "======================"

# Conta immagini WebP generate
webp_count=$(find img -name "*.webp" | wc -l)
echo "🆕 File WebP creati: $webp_count"

# Dimensioni prima/dopo
if [ -d "img_backup" ]; then
    before_size=$(du -sh img_backup | cut -f1)
    after_size=$(du -sh img | cut -f1)
    echo "📉 Riduzione dimensioni: $before_size → $after_size"
fi

echo ""
echo "📝 CONTROLLO TEMPLATE:"
echo "====================="

# Verifica uso componente ottimizzato
if grep -q "optimized-image.html" _layouts/home.html; then
    echo "✅ Template home.html ottimizzato"
else
    echo "❌ Template home.html NON ottimizzato"
fi

# Verifica critical CSS
if [ -f "_includes/critical-css.html" ]; then
    echo "✅ Critical CSS implementato"
else
    echo "❌ Critical CSS mancante"
fi

echo ""
echo "🔧 CONTROLLO CONFIGURAZIONE:"
echo "============================"

# Verifica config Jekyll
if grep -q "compress_html" _config.yml; then
    echo "✅ Compressione HTML abilitata"
else
    echo "❌ Compressione HTML non configurata"
fi

# Verifica rimozione duplicati
if ! grep -q "font-awesome.*font-awesome" _sass/styles.scss && ! grep -q "startbootstrap.*startbootstrap" _sass/styles.scss; then
    echo "✅ Duplicazioni CSS rimosse"
else
    echo "❌ Ancora presenti duplicazioni CSS"
fi

echo ""
echo "🚀 PROSSIMI PASSI:"
echo "=================="
echo "1. 📊 Esegui: ./scripts/performance-audit.sh"
echo "2. 🧪 Testa: bundle exec jekyll serve"
echo "3. 📤 Deploy: git add . && git commit -m 'Performance optimizations' && git push"
echo "4. 🔍 Verifica: https://pagespeed.web.dev/analysis/matteoricci-net"

echo ""
echo "🎯 RISULTATI ATTESI:"
echo "==================="
echo "• ⚡ Velocità caricamento: +40-60%"
echo "• 📱 Performance mobile: 80-90+"
echo "• 🖥️  Performance desktop: 90-95+"
echo "• 📦 Riduzione peso pagina: -30-50%"
echo "• 🌐 Core Web Vitals: PASS"
