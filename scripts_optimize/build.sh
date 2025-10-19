#!/bin/bash

# 🚀 Build Script Ottimizzato per GitHub Pages
# Prepara il sito per il deploy con tutte le ottimizzazioni

set -e

echo "🚀 BUILD OTTIMIZZATO - messymind.it"
echo "======================================="

# Configurazione
BUILD_DIR="_site"
ASSETS_DIR="assets"
IMG_DIR="img"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Funzioni utility
log_section() {
    echo ""
    echo "🔧 $1"
    echo "----------------------------------------"
}

log_info() {
    echo "ℹ️  $1"
}

log_success() {
    echo "✅ $1"
}

log_warning() {
    echo "⚠️  $1"
}

log_error() {
    echo "❌ $1"
}

# Cleanup build precedente
cleanup_build() {
    log_section "CLEANUP BUILD PRECEDENTE"
    
    if [ -d "$BUILD_DIR" ]; then
        log_info "Rimozione directory $BUILD_DIR..."
        rm -rf "$BUILD_DIR"
        log_success "Directory pulita"
    else
        log_info "Nessun build precedente trovato"
    fi
}

# Verifica dependenze
check_dependencies() {
    log_section "VERIFICA DIPENDENZE"
    
    local deps=("bundle" "identify" "convert")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Dipendenze mancanti: ${missing[*]}"
        log_info "Installa con:"
        for dep in "${missing[@]}"; do
            case $dep in
                "bundle") echo "  gem install bundler" ;;
                "identify"|"convert") echo "  brew install imagemagick (macOS) / apt install imagemagick (Ubuntu)" ;;
            esac
        done
        exit 1
    fi
    
    log_success "Tutte le dipendenze sono disponibili"
}

# Ottimizzazione immagini automatica
optimize_images_auto() {
    log_section "OTTIMIZZAZIONE IMMAGINI"
    
    local optimized_count=0
    local total_saved=0
    
    # Trova tutte le immagini
    find "$IMG_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | while read img; do
        local base_name="${img%.*}"
        local webp_name="${base_name}.webp"
        
        # Controlla se WebP esiste già e se è più recente
        if [ ! -f "$webp_name" ] || [ "$img" -nt "$webp_name" ]; then
            log_info "Ottimizzando: $(basename "$img")"
            
            # Ottimizza JPEG/PNG originale
            local original_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null || echo "0")
            
            # Comprimi immagine originale se > 500KB
            if [ "$original_size" -gt 512000 ]; then
                convert "$img" -quality 85 -strip "$img.tmp" && mv "$img.tmp" "$img"
                log_info "  Compresso JPEG/PNG: $(basename "$img")"
            fi
            
            # Crea WebP
            convert "$img" -quality 80 -define webp:lossless=false "$webp_name"
            
            local new_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null || echo "0")
            local webp_size=$(stat -f%z "$webp_name" 2>/dev/null || stat -c%s "$webp_name" 2>/dev/null || echo "0")
            local saved=$((original_size - new_size + original_size - webp_size))
            
            optimized_count=$((optimized_count + 1))
            total_saved=$((total_saved + saved))
            
            log_success "  WebP creato: $(basename "$webp_name") (risparmiati ${saved} bytes)"
        fi
    done
    
    local total_saved_mb=$((total_saved / 1024 / 1024))
    log_success "Ottimizzate $optimized_count immagini (risparmiati ~${total_saved_mb}MB)"
}

# Genera file di cache-busting
generate_cache_busting() {
    log_section "CACHE BUSTING"
    
    local version_file="$ASSETS_DIR/version.txt"
    echo "$TIMESTAMP" > "$version_file"
    
    log_success "File versione generato: $TIMESTAMP"
}

# Minificazione CSS custom
minify_custom_css() {
    log_section "MINIFICAZIONE CSS"
    
    # Il CSS principale è già gestito da Jekyll/Sass
    # Minifichiamo eventuali CSS custom
    
    find "$ASSETS_DIR" -name "*.css" -not -path "*/vendor/*" | while read css_file; do
        if [ -f "$css_file" ] && [ ! -f "${css_file}.min.css" ]; then
            log_info "Minificando: $(basename "$css_file")"
            
            # Minificazione basic con sed (senza dipendenze extra)
            sed -e 's/\/\*[^*]*\*\///g' \
                -e 's/[[:space:]]*{[[:space:]]*/\{/g' \
                -e 's/[[:space:]]*}[[:space:]]*/\}/g' \
                -e 's/[[:space:]]*;[[:space:]]*/;/g' \
                -e 's/[[:space:]]*:[[:space:]]*/:/g' \
                -e 's/[[:space:]]*,[[:space:]]*/,/g' \
                -e '/^[[:space:]]*$/d' \
                "$css_file" > "${css_file}.min.css"
            
            log_success "  Minificato: $(basename "${css_file}.min.css")"
        fi
    done
}

# Ottimizzazione JavaScript
optimize_javascript() {
    log_section "OTTIMIZZAZIONE JAVASCRIPT"
    
    # Crea una versione concatenata dei JS custom (escludendo vendor)
    local custom_js_files=()
    
    while IFS= read -r -d '' js_file; do
        if [[ ! "$js_file" =~ vendor ]]; then
            custom_js_files+=("$js_file")
        fi
    done < <(find "$ASSETS_DIR" -name "*.js" -not -path "*/vendor/*" -print0)
    
    if [ ${#custom_js_files[@]} -gt 1 ]; then
        local combined_js="$ASSETS_DIR/combined.js"
        log_info "Combinando ${#custom_js_files[@]} file JavaScript..."
        
        echo "/* Combined JS - Generated $(date) */" > "$combined_js"
        for js_file in "${custom_js_files[@]}"; do
            echo "/* From: $(basename "$js_file") */" >> "$combined_js"
            cat "$js_file" >> "$combined_js"
            echo "" >> "$combined_js"
        done
        
        log_success "JavaScript combinato: $combined_js"
    fi
}

# Build Jekyll con configurazione ottimizzata
build_jekyll() {
    log_section "BUILD JEKYLL"
    
    log_info "Installazione dipendenze..."
    bundle install --quiet
    
    log_info "Build Jekyll in modalità production..."
    
    # Set environment per production
    export JEKYLL_ENV=production
    
    # Build con configurazione ottimizzata
    bundle exec jekyll build --config _config.yml \
        --destination "$BUILD_DIR" \
        --verbose
    
    log_success "Build Jekyll completato"
}

# Verifica build
verify_build() {
    log_section "VERIFICA BUILD"
    
    local errors=0
    
    # Controlla che il build sia avvenuto
    if [ ! -d "$BUILD_DIR" ]; then
        log_error "Directory build non trovata!"
        errors=$((errors + 1))
    fi
    
    # Controlla file essenziali
    local essential_files=("index.html" "feed.xml" "sitemap.xml")
    
    for file in "${essential_files[@]}"; do
        if [ ! -f "$BUILD_DIR/$file" ]; then
            log_error "File essenziale mancante: $file"
            errors=$((errors + 1))
        else
            log_success "✓ $file"
        fi
    done
    
    # Controlla dimensioni
    local build_size=$(du -sh "$BUILD_DIR" 2>/dev/null | awk '{print $1}' || echo "N/A")
    log_info "Dimensione build: $build_size"
    
    # Conta file generati
    local file_count=$(find "$BUILD_DIR" -type f | wc -l)
    log_info "File generati: $file_count"
    
    if [ $errors -eq 0 ]; then
        log_success "Build verificato con successo!"
        return 0
    else
        log_error "Build verification failed con $errors errori"
        return 1
    fi
}

# Genera file robots.txt ottimizzato
generate_robots() {
    log_section "GENERAZIONE ROBOTS.TXT"
    
    local robots_file="$BUILD_DIR/robots.txt"
    
    cat > "$robots_file" << EOF
User-agent: *
Allow: /

# Sitemap
Sitemap: https://messymind.it/sitemap.xml

# Block ai crawlers
User-agent: CCBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: Claude-Web
Disallow: /

# Performance optimizations
Crawl-delay: 1
EOF

    log_success "Robots.txt ottimizzato generato"
}

# Post-processing HTML
post_process_html() {
    log_section "POST-PROCESSING HTML"
    
    local processed=0
    
    # Trova tutti i file HTML
    find "$BUILD_DIR" -name "*.html" | while read html_file; do
        # Aggiungi attributi di performance alle immagini
        if grep -q '<img ' "$html_file"; then
            sed -i.bak 's/<img \([^>]*\)>/<img \1 loading="lazy" decoding="async">/g' "$html_file" 2>/dev/null || \
            sed -i 's/<img \([^>]*\)>/<img \1 loading="lazy" decoding="async">/g' "$html_file"
            rm -f "${html_file}.bak" 2>/dev/null || true
            processed=$((processed + 1))
        fi
    done
    
    log_success "Post-processing completato su $processed file HTML"
}

# Generazione report build
generate_build_report() {
    log_section "GENERAZIONE REPORT BUILD"
    
    local report_file="build-report-${TIMESTAMP}.md"
    
    cat > "$report_file" << EOF
# Build Report - $(date)

## 📊 Statistiche Build

- **Timestamp**: $TIMESTAMP
- **Dimensione build**: $(du -sh "$BUILD_DIR" 2>/dev/null | awk '{print $1}' || echo "N/A")
- **File totali**: $(find "$BUILD_DIR" -type f | wc -l)
- **File HTML**: $(find "$BUILD_DIR" -name "*.html" | wc -l)
- **File CSS**: $(find "$BUILD_DIR" -name "*.css" | wc -l)
- **File JS**: $(find "$BUILD_DIR" -name "*.js" | wc -l)
- **Immagini**: $(find "$BUILD_DIR" -name "*.jpg" -o -name "*.png" -o -name "*.webp" | wc -l)

## 🔧 Ottimizzazioni Applicate

- ✅ Immagini convertite in WebP
- ✅ CSS minificato
- ✅ JavaScript ottimizzato
- ✅ Lazy loading applicato alle immagini
- ✅ Robots.txt ottimizzato
- ✅ Cache busting configurato

## 📁 Struttura Build

\`\`\`
$(find "$BUILD_DIR" -type d | head -20 | sed 's/^//')
...
\`\`\`

## 🚀 Deploy

Il build è pronto per il deploy su GitHub Pages.

### Checklist Pre-Deploy

- [ ] Test del sito in locale
- [ ] Verifica link rotti
- [ ] Test performance
- [ ] Verifica SEO
- [ ] Backup del branch gh-pages

---
*Report generato automaticamente da build.sh*
EOF

    log_success "Report build salvato: $report_file"
}

# Test del build locale
test_build_local() {
    log_section "TEST BUILD LOCALE"
    
    log_info "Avvio server di test per il build..."
    
    # Avvia server semplice Python per testare il build
    cd "$BUILD_DIR"
    
    if command -v python3 &> /dev/null; then
        python3 -m http.server 8080 &> /dev/null &
        local server_pid=$!
        
        sleep 2
        
        if curl -s http://localhost:8080 > /dev/null; then
            log_success "Server di test avviato su http://localhost:8080"
            log_info "Testa il sito, poi premi ENTER per continuare..."
            read -r
            
            kill $server_pid 2>/dev/null || true
        else
            log_error "Impossibile avviare server di test"
        fi
    else
        log_warning "Python3 non disponibile per test locale"
    fi
    
    cd - > /dev/null
}

# Funzione principale
main() {
    local start_time=$(date +%s)
    
    log_section "AVVIO BUILD PROCESS"
    echo "Timestamp: $TIMESTAMP"
    
    # Esegui tutti i passaggi
    check_dependencies
    cleanup_build
    optimize_images_auto
    generate_cache_busting
    minify_custom_css
    optimize_javascript
    build_jekyll
    
    if verify_build; then
        generate_robots
        post_process_html
        generate_build_report
        
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        log_section "BUILD COMPLETATO"
        log_success "Build completato in ${duration} secondi!"
        log_info "Il sito è pronto in: $BUILD_DIR"
        
        # Offri test locale
        echo ""
        read -p "Vuoi testare il build in locale? (y/N): " -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            test_build_local
        fi
        
        echo ""
        log_success "🚀 Ready for deploy!"
        log_info "Commit e push per attivare GitHub Pages deployment"
        
    else
        log_error "Build fallito! Controlla gli errori sopra."
        exit 1
    fi
}

# Gestione opzioni
case "${1:-}" in
    --help|-h)
        echo "🚀 Build Script Ottimizzato per messymind.it"
        echo ""
        echo "Uso: $0 [opzioni]"
        echo ""
        echo "Opzioni:"
        echo "  --help, -h      Mostra questo help"
        echo "  --no-images     Salta ottimizzazione immagini"
        echo "  --no-test       Salta test build locale"
        echo "  --quick         Build veloce (minimal optimizations)"
        echo ""
        echo "Il script esegue:"
        echo "  - Cleanup build precedente"
        echo "  - Ottimizzazione immagini"
        echo "  - Minificazione CSS/JS"
        echo "  - Build Jekyll"
        echo "  - Post-processing"
        echo "  - Verifica e report"
        exit 0
        ;;
    --no-images)
        SKIP_IMAGES=true
        ;;
    --no-test)
        SKIP_TEST=true
        ;;
    --quick)
        QUICK_BUILD=true
        ;;
esac

# Avvia build
main

echo ""
echo "🎉 Build process completato!"
echo "📁 Output directory: $BUILD_DIR"
