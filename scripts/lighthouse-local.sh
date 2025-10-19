#!/bin/bash
set -e

#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════╗
# ║  Lighthouse Local Test Runner - SIMPLIFIED VERSION            ║
# ║  Uses puppeteer bundled Chrome (no snap issues)               ║
# ╚═══════════════════════════════════════════════════════════════╝

set -e

# Configurazione
OUTPUT_DIR="./docs/evidence/lighthouse"
PORT=8080

# URL da testare (relativi al server locale)
URLS=(
    "home|/"
    "category-burnout|/categorie/burnout-e-lavoro/"
    "post-stress|/2025/09/29/stress-correlato/"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 LIGHTHOUSE LOCAL TEST RUNNER (SIMPLE)              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENVIRONMENT CHECK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "📋 Environment Check:"
echo "   Node: $(node -v)"
echo "   NPM: $(npm -v)"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BUILD JEKYLL SITE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "🔨 Building Jekyll site..."
bundle exec jekyll build --config _config.yml,_config_dev.yml > /dev/null 2>&1
echo "✅ Build complete"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# START HTTP SERVER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "🌐 Starting HTTP server..."
npx http-server _site -p ${PORT} > /dev/null 2>&1 &
SERVER_PID=$!
echo "   Server PID: ${SERVER_PID}"

# Cleanup trap
trap "echo '🛑 Stopping server (PID: ${SERVER_PID})...'; kill ${SERVER_PID} 2>/dev/null || true; wait ${SERVER_PID} 2>/dev/null || true" EXIT

# Wait for server
echo "⏳ Waiting for server to be ready..."
npx wait-on http://localhost:${PORT} -t 30000
echo "✅ Server ready"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CREATE OUTPUT DIRECTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
mkdir -p "${OUTPUT_DIR}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RUN LIGHTHOUSE TESTS (uses LHCI for reliability)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for url_pair in "${URLS[@]}"; do
    IFS="|" read -r name path <<< "$url_pair"
    full_url="http://localhost:${PORT}${path}"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 Testing: ${name}"
    echo "   URL: ${full_url}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Desktop - run 1 time for speed
    echo "🖥️  Desktop preset..."
    npx @lhci/cli collect \
        --url="${full_url}" \
        --settings.preset=desktop \
        --numberOfRuns=1 \
        --settings.chromeFlags="--headless=new --no-sandbox --disable-dev-shm-usage" 2>&1 | grep -v "ChromeLauncher" || true
    
    # Move reports
    if [ -d ".lighthouseci" ]; then
        mv .lighthouseci/*.html "${OUTPUT_DIR}/lh-${name}-desktop.html" 2>/dev/null || true
        mv .lighthouseci/*.json "${OUTPUT_DIR}/lh-${name}-desktop.json" 2>/dev/null || true
        rm -rf .lighthouseci
    fi
    
    # Mobile - run 1 time for speed  
    echo "📱 Mobile preset..."
    npx @lhci/cli collect \
        --url="${full_url}" \
        --settings.preset=mobile \
        --numberOfRuns=1 \
        --settings.chromeFlags="--headless=new --no-sandbox --disable-dev-shm-usage" 2>&1 | grep -v "ChromeLauncher" || true
    
    # Move reports
    if [ -d ".lighthouseci" ]; then
        mv .lighthouseci/*.html "${OUTPUT_DIR}/lh-${name}-mobile.html" 2>/dev/null || true
        mv .lighthouseci/*.json "${OUTPUT_DIR}/lh-${name}-mobile.json" 2>/dev/null || true
        rm -rf .lighthouseci
    fi
    
    echo "✅ Reports saved for ${name}"
    echo ""
done

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUMMARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║ ✅ ALL REPORTS GENERATED                                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📂 Reports location: ${OUTPUT_DIR}"
echo "🌐 Open reports with: firefox ${OUTPUT_DIR}/*.html"
echo ""
echo "📋 Generated files:"
ls -lh "${OUTPUT_DIR}" 2>/dev/null || echo "No reports found - check for errors above"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 LIGHTHOUSE LOCAL TEST RUNNER                       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Variables
BASE_URL="http://localhost:8080"
OUTPUT_DIR="./docs/evidence/lighthouse"
SERVER_PID=""

# Cleanup function
cleanup() {
  if [ ! -z "$SERVER_PID" ]; then
    echo "🛑 Stopping server (PID: $SERVER_PID)..."
    kill $SERVER_PID 2>/dev/null || true
  fi
}

trap cleanup EXIT

# Check environment
echo "📋 Environment Check:"
echo "   Node: $(node -v)"
echo "   NPM: $(npm -v)"
echo "   Chrome: $(chromium --version 2>/dev/null || google-chrome --version 2>/dev/null || echo 'Not found')"
echo ""

# Build Jekyll
echo "🔨 Building Jekyll site..."
bundle exec jekyll build --quiet
if [ ! -d "_site" ]; then
  echo "❌ Error: _site directory not found"
  exit 1
fi
echo "✅ Build complete"
echo ""

# Start server
echo "🌐 Starting HTTP server..."
npx http-server _site -p 8080 --silent &
SERVER_PID=$!
echo "   Server PID: $SERVER_PID"

# Wait for server
echo "⏳ Waiting for server to be ready..."
npx wait-on http://localhost:8080 --timeout 10000
echo "✅ Server ready"
echo ""

# Test URLs
declare -a URLS=(
  "http://localhost:8080/|home"
  "http://localhost:8080/categorie/burnout-e-lavoro/|category-burnout"
  "http://localhost:8080/2025/09/29/stress-correlato/|post-stress"
)

# Run Lighthouse for each URL (Desktop + Mobile)
for url_pair in "${URLS[@]}"; do
  IFS='|' read -r url name <<< "$url_pair"
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📊 Testing: $name"
  echo "   URL: $url"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  # Desktop
  echo "🖥️  Desktop preset..."
  npx lighthouse "$url" \
    --preset=desktop \
    --output=html \
    --output=json \
    --output-path="$OUTPUT_DIR/lh-${name}-desktop" \
    --chrome-flags="--headless=new --no-sandbox" \
    --quiet 2>&1 | grep -E "Performance|Accessibility|Best Practices|SEO|scores" || true
  
  # Mobile
  echo "📱 Mobile preset..."
  npx lighthouse "$url" \
    --preset=mobile \
    --output=html \
    --output=json \
    --output-path="$OUTPUT_DIR/lh-${name}-mobile" \
    --chrome-flags="--headless=new --no-sandbox" \
    --quiet 2>&1 | grep -E "Performance|Accessibility|Best Practices|SEO|scores" || true
  
  echo "✅ Reports saved:"
  echo "   - $OUTPUT_DIR/lh-${name}-desktop.html"
  echo "   - $OUTPUT_DIR/lh-${name}-desktop.json"
  echo "   - $OUTPUT_DIR/lh-${name}-mobile.html"
  echo "   - $OUTPUT_DIR/lh-${name}-mobile.json"
  echo ""
done

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║ ✅ ALL REPORTS GENERATED                                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📂 Reports location: $OUTPUT_DIR"
echo "🌐 Open reports with: firefox $OUTPUT_DIR/*.html"
echo ""

# List all generated files
echo "📋 Generated files:"
ls -lh "$OUTPUT_DIR" | grep "lh-"

cleanup
