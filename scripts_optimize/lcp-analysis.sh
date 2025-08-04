#!/bin/bash

# Script specifico per analisi LCP dettagliata
echo "🎯 ANALISI LCP SPECIFICA - messymind.it"
echo "=========================================="

SITE_URL="https://www.messymind.it"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}1. LIGHTHOUSE LCP-FOCUSED AUDIT${NC}"
echo "-----------------------------------"

# Test Lighthouse con focus su LCP e metriche di caricamento
./node_modules/.bin/lighthouse $SITE_URL \
    --only-categories=performance \
    --chrome-flags="--headless --no-sandbox --disable-dev-shm-usage" \
    --output=json \
    --output-path=./lcp-analysis.json \
    --form-factor=mobile \
    --throttling-method=devtools \
    --preset=perf

echo -e "${BLUE}2. ANALISI ELEMENTO LCP${NC}"
echo "----------------------------"

if [ -f "./lcp-analysis.json" ]; then
    echo -e "${YELLOW}Elemento LCP identificato:${NC}"
    cat lcp-analysis.json | jq -r '
        .lhr.audits."largest-contentful-paint-element".details.items[0] | 
        "Elemento: " + (.node.snippet // "N/A") + "\n" +
        "URL: " + (.url // "N/A") + "\n" +
        "Dimensione: " + (.size // "N/A" | tostring) + " bytes"
    '
    
    echo -e "${YELLOW}Timing LCP dettagliato:${NC}"
    cat lcp-analysis.json | jq -r '
        .lhr.audits."largest-contentful-paint" | 
        "LCP Time: " + (.displayValue // "N/A") + "\n" +
        "Score: " + ((.score * 100) // "N/A" | tostring) + "/100"
    '
    
    echo -e "${YELLOW}Breakdown LCP (se disponibile):${NC}"
    cat lcp-analysis.json | jq -r '
        .lhr.audits."lcp-lazy-loaded" // empty |
        "Lazy Loading Issues: " + (.displayValue // "N/A")
    '
    
    echo ""
fi

echo -e "${BLUE}3. ANALISI RISORSE CRITICHE${NC}"
echo "--------------------------------"

if [ -f "./lcp-analysis.json" ]; then
    echo -e "${YELLOW}Opportunità di miglioramento LCP:${NC}"
    
    # Largest Contentful Paint element
    cat lcp-analysis.json | jq -r '
        .lhr.audits."largest-contentful-paint-element" |
        if .score < 0.9 then
            "❌ LCP Element: " + (.displayValue // "Needs optimization")
        else
            "✅ LCP Element: Optimized"
        end
    '
    
    # Preload LCP image
    cat lcp-analysis.json | jq -r '
        .lhr.audits."preload-lcp-image" |
        if .score < 0.9 then
            "❌ Preload LCP Image: " + (.displayValue // "Missing preload")
        else
            "✅ Preload LCP Image: Present"
        end
    '
    
    # Reduce initial server response time
    cat lcp-analysis.json | jq -r '
        .lhr.audits."server-response-time" |
        if .score < 0.9 then
            "❌ Server Response: " + (.displayValue // "Too slow")
        else
            "✅ Server Response: Fast"
        end
    '
    
    # Remove resource load impact
    cat lcp-analysis.json | jq -r '
        .lhr.audits."render-blocking-resources" |
        if .score < 0.9 then
            "❌ Render Blocking: " + (.displayValue // "Resources blocking")
        else
            "✅ Render Blocking: None"
        end
    '
    
    echo ""
fi

echo -e "${BLUE}4. WATERFALL ANALYSIS${NC}"
echo "------------------------"

if [ -f "./lcp-analysis.json" ]; then
    echo -e "${YELLOW}Critical Resource Timing:${NC}"
    
    # Estrai i tempi delle risorse critiche
    cat lcp-analysis.json | jq -r '
        .lhr.audits."network-requests".details.items[] |
        select(.url | contains("amore.webp") or contains("main.css") or test("/$")) |
        .url + ": " + (.startTime | tostring) + "ms start, " + (.endTime | tostring) + "ms end"
    ' | head -10
    
    echo ""
fi

echo -e "${BLUE}5. TEST MANUALE VELOCITÀ${NC}"
echo "----------------------------"

echo -e "${YELLOW}Velocità caricamento risorse:${NC}"

# Test specifico immagine LCP
echo -n "Immagine LCP (amore.webp): "
LCP_TIME=$(curl -o /dev/null -s -w "%{time_total},%{size_download}" "$SITE_URL/img/amore.webp")
echo "${LCP_TIME} (tempo,bytes)"

# Test CSS
echo -n "CSS principale: "
CSS_TIME=$(curl -o /dev/null -s -w "%{time_total},%{size_download}" "$SITE_URL/assets/main.css")
echo "${CSS_TIME} (tempo,bytes)"

# Test HTML + headers
echo -n "HTML documento: "
HTML_TIME=$(curl -o /dev/null -s -w "%{time_total},%{size_download}" "$SITE_URL/")
echo "${HTML_TIME} (tempo,bytes)"

echo ""

echo -e "${BLUE}6. VERIFICA PRELOAD${NC}"
echo "--------------------"

echo -e "${YELLOW}Controllo preload nell'HTML:${NC}"
curl -s "$SITE_URL/" | grep -E "(preload|prefetch)" || echo "Nessun preload trovato"

echo ""

echo -e "${BLUE}7. RACCOMANDAZIONI SPECIFICHE${NC}"
echo "--------------------------------"

echo -e "${YELLOW}Analisi automatica problemi:${NC}"

# Controlla se l'immagine LCP è troppo grande
WEBP_SIZE=$(curl -s -I "$SITE_URL/img/amore.webp" | grep -i content-length | awk '{print $2}' | tr -d '\r')
if [ "$WEBP_SIZE" -gt 30000 ]; then
    echo -e "${RED}❌ Immagine LCP ancora troppo grande: ${WEBP_SIZE} bytes (target: <30KB)${NC}"
else
    echo -e "${GREEN}✅ Immagine LCP ottimizzata: ${WEBP_SIZE} bytes${NC}"
fi

# Controlla TTFB
TTFB=$(curl -o /dev/null -s -w "%{time_starttransfer}" "$SITE_URL/")
if (( $(echo "$TTFB > 0.6" | bc -l) )); then
    echo -e "${RED}❌ TTFB troppo lento: ${TTFB}s (target: <0.6s)${NC}"
else
    echo -e "${GREEN}✅ TTFB accettabile: ${TTFB}s${NC}"
fi

# Controlla se ci sono ancora script bloccanti
if curl -s "$SITE_URL/" | grep -E "<script.*src.*>" | grep -v "defer\|async"; then
    echo -e "${RED}❌ Script bloccanti rilevati${NC}"
else
    echo -e "${GREEN}✅ Nessun script bloccante${NC}"
fi

echo ""
echo -e "${GREEN}🎯 PROSSIMI PASSI PER LCP < 2.5s:${NC}"
echo "1. Riduci ulteriormente immagine LCP se >30KB"
echo "2. Migliora TTFB se >600ms" 
echo "3. Assicurati che preload LCP sia presente"
echo "4. Rimuovi qualsiasi risorsa render-blocking"
echo "5. Considera di inlineare CSS critico"
echo ""
