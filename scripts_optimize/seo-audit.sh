#!/bin/bash

# Script per audit completo con Lighthouse e analisi LCP
echo "🔍 AUDIT PRESTAZIONI COMPLETO - messymind.it"
echo "================================================"

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SITE_URL="https://www.messymind.it"

echo -e "${BLUE}📊 1. LIGHTHOUSE AUDIT COMPLETO${NC}"
echo "-----------------------------------"

# Installa lighthouse se non presente
if [ ! -f "./node_modules/.bin/lighthouse" ]; then
    echo "Installando Lighthouse locale..."
    npm install lighthouse --save-dev
fi

# Test Lighthouse mobile
echo -e "${YELLOW}📱 Test Mobile:${NC}"
./node_modules/.bin/lighthouse $SITE_URL \
    --preset=perf \
    --chrome-flags="--headless --no-sandbox" \
    --output=json \
    --output-path=./lighthouse-mobile.json \
    --form-factor=mobile \
    --throttling-method=devtools

# Test Lighthouse desktop  
echo -e "${YELLOW}🖥️ Test Desktop:${NC}"
./node_modules/.bin/lighthouse $SITE_URL \
    --preset=perf \
    --chrome-flags="--headless --no-sandbox" \
    --output=json \
    --output-path=./lighthouse-desktop.json \
    --form-factor=desktop \
    --throttling-method=devtools

echo -e "${BLUE}📈 2. ANALISI RISULTATI LIGHTHOUSE${NC}"
echo "----------------------------------------"

# Estrai metriche principali
if [ -f "./lighthouse-mobile.json" ]; then
    echo -e "${GREEN}Mobile Performance:${NC}"
    cat lighthouse-mobile.json | jq -r '
        "Performance Score: " + (.lhr.categories.performance.score * 100 | tostring) + "/100",
        "FCP: " + (.lhr.audits."first-contentful-paint".displayValue // "N/A"),
        "LCP: " + (.lhr.audits."largest-contentful-paint".displayValue // "N/A"),
        "TBT: " + (.lhr.audits."total-blocking-time".displayValue // "N/A"),
        "CLS: " + (.lhr.audits."cumulative-layout-shift".displayValue // "N/A"),
        "Speed Index: " + (.lhr.audits."speed-index".displayValue // "N/A")
    '
    echo ""
fi

if [ -f "./lighthouse-desktop.json" ]; then
    echo -e "${GREEN}Desktop Performance:${NC}"
    cat lighthouse-desktop.json | jq -r '
        "Performance Score: " + (.lhr.categories.performance.score * 100 | tostring) + "/100",
        "FCP: " + (.lhr.audits."first-contentful-paint".displayValue // "N/A"),
        "LCP: " + (.lhr.audits."largest-contentful-paint".displayValue // "N/A"),
        "TBT: " + (.lhr.audits."total-blocking-time".displayValue // "N/A"),
        "CLS: " + (.lhr.audits."cumulative-layout-shift".displayValue // "N/A"),
        "Speed Index: " + (.lhr.audits."speed-index".displayValue // "N/A")
    '
    echo ""
fi

echo -e "${BLUE}🔍 3. ANALISI LCP ELEMENTO${NC}"
echo "-------------------------------"

# Identifica elemento LCP
if [ -f "./lighthouse-mobile.json" ]; then
    echo -e "${YELLOW}Elemento LCP identificato:${NC}"
    cat lighthouse-mobile.json | jq -r '.lhr.audits."largest-contentful-paint-element".details.items[0] | 
        "Element: " + (.node.snippet // "N/A"),
        "URL: " + (.url // "N/A")'
    echo ""
fi

echo -e "${BLUE}⚡ 4. OPPORTUNITÀ DI MIGLIORAMENTO${NC}"
echo "-----------------------------------"

if [ -f "./lighthouse-mobile.json" ]; then
    echo -e "${YELLOW}Top 5 opportunità (Mobile):${NC}"
    cat lighthouse-mobile.json | jq -r '.lhr.audits | to_entries | 
        map(select(.value.scoreDisplayMode == "numeric" and .value.score != null and .value.score < 0.9)) |
        sort_by(.value.score) | 
        limit(5; .[]) | 
        .key + ": " + (.value.displayValue // "N/A") + " (Score: " + (.value.score * 100 | tostring) + ")"'
    echo ""
fi

echo -e "${BLUE}🌐 5. ANALISI RETE E RISORSE${NC}"
echo "------------------------------"

# Test velocità risorse critiche
echo -e "${YELLOW}Test velocità risorse critiche:${NC}"

# CSS principale
CSS_TIME=$(curl -o /dev/null -s -w "%{time_total}" "$SITE_URL/assets/main.css")
echo "CSS principale: ${CSS_TIME}s"

# Immagine LCP
LCP_IMG_TIME=$(curl -o /dev/null -s -w "%{time_total}" "$SITE_URL/img/amore.webp")
echo "Immagine LCP (WebP): ${LCP_IMG_TIME}s"

# HTML documento
HTML_TIME=$(curl -o /dev/null -s -w "%{time_total}" "$SITE_URL/")
echo "HTML documento: ${HTML_TIME}s"

echo ""

echo -e "${BLUE}📋 6. ANALISI HEADERS HTTP${NC}"
echo "-----------------------------"

# Analizza headers critici
echo -e "${YELLOW}Headers cache e compressione:${NC}"
curl -s -I "$SITE_URL/" | grep -i -E "(cache-control|content-encoding|content-type)"
echo ""

echo -e "${BLUE}🎯 7. SUGGERIMENTI SPECIFICI${NC}"
echo "------------------------------"

# Controlla se ci sono problemi comuni
echo -e "${YELLOW}Controlli automatici:${NC}"

# Controlla presenza jQuery/Bootstrap
if curl -s "$SITE_URL/" | grep -q "jquery\|bootstrap.js"; then
    echo -e "${RED}❌ JavaScript pesante rilevato (jQuery/Bootstrap)${NC}"
else
    echo -e "${GREEN}✅ Nessun JavaScript pesante rilevato${NC}"
fi

# Controlla presenza di font esterni
if curl -s "$SITE_URL/" | grep -q "fonts.googleapis.com"; then
    echo -e "${RED}❌ Font esterni Google rilevati${NC}"
else
    echo -e "${GREEN}✅ Nessun font esterno rilevato${NC}"
fi

# Controlla compressione immagini
WEBP_SIZE=$(curl -s -I "$SITE_URL/img/amore.webp" | grep -i content-length | awk '{print $2}' | tr -d '\r')
if [ "$WEBP_SIZE" -gt 50000 ]; then
    echo -e "${RED}❌ Immagine LCP ancora troppo grande: ${WEBP_SIZE} bytes${NC}"
else
    echo -e "${GREEN}✅ Immagine LCP ottimizzata: ${WEBP_SIZE} bytes${NC}"
fi

echo ""
echo -e "${BLUE}📊 REPORT COMPLETO SALVATO${NC}"
echo "lighthouse-mobile.json, lighthouse-desktop.json"
echo ""
echo -e "${GREEN}🎯 PROSSIMI PASSI RACCOMANDATI:${NC}"
echo "1. Analizza elemento LCP specifico identificato"
echo "2. Verifica se il preload è effettivo" 
echo "3. Controlla se ci sono risorse che bloccano il rendering"
echo "4. Testa velocità server/CDN"
echo "================================================"
