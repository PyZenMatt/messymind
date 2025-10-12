#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════╗
# ║  Lighthouse Simple Runner - MINIMALISTA                       ║
# ║  Usa solo lighthouse CLI con Puppeteer bundled Chrome         ║
# ╚═══════════════════════════════════════════════════════════════╝

set -e

# Config
OUTPUT="./docs/evidence/lighthouse"
PORT=8080

echo "🚀 Starting Lighthouse tests..."
echo ""

# Build
echo "🔨 Building site..."
bundle exec jekyll build --config _config.yml,_config_dev.yml > /dev/null 2>&1
echo "✅ Built"

# Start server
echo "🌐 Starting server on port $PORT..."
npx http-server _site -p $PORT > /dev/null 2>&1 &
SERVER_PID=$!

# Trap cleanup
trap "echo ''; echo '🛑 Stopping server...'; kill $SERVER_PID 2>/dev/null || true; wait $SERVER_PID 2>/dev/null || true" EXIT

# Wait
echo "⏳ Waiting..."
sleep 5
echo "✅ Ready"
echo ""

# Create output dir
mkdir -p "$OUTPUT"

# Test URLs
declare -A URLS=(
    ["home"]="/"
    ["category"]="/categorie/burnout-e-lavoro/"
    ["post"]="/2025/09/29/stress-correlato/"
)

# Run tests
for name in "${!URLS[@]}"; do
    url="http://localhost:$PORT${URLS[$name]}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 $name: $url"
    
    # Desktop
    echo -n "  Desktop... "
    npx --yes lighthouse "$url" \
        --only-categories=performance,seo,accessibility,best-practices \
        --preset=desktop \
        --output=html --output=json \
        --output-path="$OUTPUT/lh-$name-desktop" \
        --quiet \
        --chrome-flags="--headless --disable-gpu --no-sandbox" \
        2>/dev/null || echo "FAILED"
    
    [ -f "$OUTPUT/lh-$name-desktop.json" ] && echo "✅" || echo "❌"
    
    # Mobile
    echo -n "  Mobile... "
    npx --yes lighthouse "$url" \
        --only-categories=performance,seo,accessibility,best-practices \
        --preset=mobile \
        --output=html --output=json \
        --output-path="$OUTPUT/lh-$name-mobile" \
        --quiet \
        --chrome-flags="--headless --disable-gpu --no-sandbox" \
        2>/dev/null || echo "FAILED"
    
    [ -f "$OUTPUT/lh-$name-mobile.json" ] && echo "✅" || echo "❌"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Done!"
echo ""
echo "📂 Reports: $OUTPUT/"
ls -lh "$OUTPUT/" 2>/dev/null || echo "No files generated"
