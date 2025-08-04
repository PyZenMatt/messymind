#!/bin/bash

# Script per ottimizzazione automatica immagini
# Converte PNG/JPG pesanti in WebP ottimizzate

echo "🖼️  Iniziando ottimizzazione immagini..."

# Controlla se cwebp è installato
if ! command -v cwebp &> /dev/null; then
    echo "❌ cwebp non trovato. Installare con:"
    echo "sudo apt install webp"
    exit 1
fi

# Directory delle immagini
IMG_DIR="./img"
BACKUP_DIR="./img_backup"

# Crea backup se non esiste
if [ ! -d "$BACKUP_DIR" ]; then
    echo "📁 Creando backup immagini originali..."
    cp -r "$IMG_DIR" "$BACKUP_DIR"
fi

# Converti immagini in WebP (solo se WebP non esiste già)
echo "🔄 Convertendo immagini in WebP..."

find "$IMG_DIR" -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" | while read img; do
    # Nome file senza estensione
    basename=$(basename "$img" | sed 's/\.[^.]*$//')
    dirname=$(dirname "$img")
    webp_file="$dirname/$basename.webp"
    
    # Controlla se WebP esiste già
    if [ ! -f "$webp_file" ]; then
        echo "  📸 Convertendo: $img"
        
        # Ottimizzazione aggressiva per file > 100KB
        size=$(stat -c%s "$img")
        if [ $size -gt 102400 ]; then
            cwebp -q 80 -m 6 "$img" -o "$webp_file"
        else
            cwebp -q 85 -m 4 "$img" -o "$webp_file"
        fi
        
        echo "    ✅ Creato: $webp_file"
        
        # Mostra risparmio spazio
        new_size=$(stat -c%s "$webp_file" 2>/dev/null || echo "0")
        if [ $new_size -gt 0 ]; then
            savings=$((100 - (new_size * 100 / size)))
            echo "    💾 Risparmio: ${savings}%"
        fi
    else
        echo "  ⏭️  WebP esiste già: $webp_file"
    fi
done

# Statistiche finali
echo ""
echo "📊 Statistiche ottimizzazione:"
echo "   📁 Immagini PNG/JPG: $(find "$IMG_DIR" -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | wc -l)"
echo "   🖼️  Immagini WebP: $(find "$IMG_DIR" -name "*.webp" | wc -l)"

# Calcola spazio totale
original_size=$(find "$IMG_DIR" \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) -exec stat -c%s {} + | awk '{s+=$1} END {print s}')
webp_size=$(find "$IMG_DIR" -name "*.webp" -exec stat -c%s {} + | awk '{s+=$1} END {print s}')

if [ ! -z "$original_size" ] && [ ! -z "$webp_size" ] && [ $original_size -gt 0 ]; then
    total_savings=$((100 - (webp_size * 100 / original_size)))
    echo "   💰 Risparmio totale: ${total_savings}%"
fi

echo ""
echo "✅ Ottimizzazione completata!"
echo "💡 Ricorda di aggiornare i riferimenti alle immagini per usare i file .webp"
