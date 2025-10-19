#!/bin/bash

# Performance Audit Script per messymind.it
echo "🚀 Performance Audit - messymind.it"
echo "======================================"

# Controlla se Lighthouse è installato localmente
if [ -f "node_modules/.bin/lighthouse" ]; then
    LIGHTHOUSE_CMD="./node_modules/.bin/lighthouse"
    echo "✅ Usando Lighthouse locale"
elif command -v lighthouse >/dev/null 2>&1; then
    LIGHTHOUSE_CMD="lighthouse"
    echo "✅ Usando Lighthouse globale"
else
    echo "❌ Lighthouse non trovato. Installa con: npm install lighthouse --save-dev"
    exit 1
fi

SITE_URL="https://messymind.it"
REPORT_DIR="performance-reports/$(date +%Y%m%d-%H%M%S)"

mkdir -p "$REPORT_DIR"

echo "📊 Eseguendo audit Lighthouse..."

# Desktop audit
$LIGHTHOUSE_CMD "$SITE_URL" \
  --preset=desktop \
  --output=html \
  --output-path="$REPORT_DIR/desktop-report.html" \
  --chrome-flags="--headless --no-sandbox"

# Mobile audit  
$LIGHTHOUSE_CMD "$SITE_URL" \
  --preset=mobile \
  --output=html \
  --output-path="$REPORT_DIR/mobile-report.html" \
  --chrome-flags="--headless --no-sandbox"

# Performance only audit con JSON
$LIGHTHOUSE_CMD "$SITE_URL" \
  --only-categories=performance \
  --output=json \
  --output-path="$REPORT_DIR/performance.json" \
  --chrome-flags="--headless --no-sandbox"

echo "✅ Report generati in: $REPORT_DIR"

# Estrai metriche chiave
if [ -f "$REPORT_DIR/performance.json" ]; then
    echo ""
    echo "📈 METRICHE CHIAVE:"
    echo "=================="
    
    # Estrai score performance
    PERF_SCORE=$(cat "$REPORT_DIR/performance.json" | grep -o '"performance":[^}]*"score":[^,]*' | grep -o '[0-9.]*$')
    echo "Performance Score: $(echo "$PERF_SCORE * 100" | bc)%"
    
    # Trova metriche Core Web Vitals se presenti
    echo "Dettagli completi nei report HTML generati."
fi

echo ""
echo "🎯 AZIONI IMMEDIATE:"
echo "==================="
echo "1. Ottimizza le immagini con lo script optimize-images.sh"
echo "2. Controlla i report generati per metriche dettagliate"
echo "3. Implementa le correzioni suggerite nel report"
echo "4. Rilanicia questo script per monitorare i miglioramenti"

# Apri report se su desktop
if [[ "$OSTYPE" == "linux-gnu"* ]] && command -v xdg-open >/dev/null 2>&1; then
    echo ""
    echo "🌐 Aprendo report desktop..."
    xdg-open "$REPORT_DIR/desktop-report.html"
fi
