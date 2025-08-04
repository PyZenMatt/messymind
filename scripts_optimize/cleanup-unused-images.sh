#!/bin/bash

# Script per identificare e rimuovere immagini non utilizzate
echo "🧹 PULIZIA IMMAGINI NON UTILIZZATE"
echo "=================================="

# Directory delle immagini
IMG_DIR="img"
UNUSED_FILE="unused_images.txt"
USED_FILE="used_images.txt"

# Trova tutte le immagini
echo "📊 Analizzando utilizzo immagini..."
find "$IMG_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.webp" \) > all_images.txt

# Inizializza file risultati
> "$USED_FILE"
> "$UNUSED_FILE"

# Controlla ogni immagine
while IFS= read -r img_path; do
    # Estrai nome file senza path
    img_name=$(basename "$img_path")
    img_name_no_ext="${img_name%.*}"
    
    # Cerca in tutti i file markdown, html e configurazione
    if grep -r -q --include="*.md" --include="*.html" --include="*.yml" --include="*.scss" \
        -e "$img_name" -e "$img_name_no_ext" -e "${img_path#img/}" . 2>/dev/null; then
        echo "$img_path" >> "$USED_FILE"
        echo "✅ USATA: $img_path"
    else
        echo "$img_path" >> "$UNUSED_FILE"
        echo "❌ NON USATA: $img_path"
    fi
done < all_images.txt

# Rimuovi file ottimizzati duplicati (mantenendo gli originali)
echo ""
echo "🔄 Rimuovendo duplicati '_optimized'..."
find "$IMG_DIR" -name "*_optimized_optimized.*" -delete
find "$IMG_DIR" -name "*_optimized.*" -type f | while read optimized_file; do
    original_file=$(echo "$optimized_file" | sed 's/_optimized//')
    if [ -f "$original_file" ]; then
        echo "🗑️  Rimuovo duplicato: $optimized_file"
        rm "$optimized_file"
    fi
done

echo ""
echo "📊 RISULTATI:"
echo "============="
echo "🖼️  Immagini totali: $(wc -l < all_images.txt)"
echo "✅ Immagini utilizzate: $(wc -l < "$USED_FILE")"
echo "❌ Immagini non utilizzate: $(wc -l < "$UNUSED_FILE")"

if [ -s "$UNUSED_FILE" ]; then
    echo ""
    echo "🗑️  IMMAGINI DA RIMUOVERE:"
    echo "========================="
    cat "$UNUSED_FILE"
    echo ""
    echo "❓ Vuoi rimuovere le immagini non utilizzate? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        while IFS= read -r unused_img; do
            rm "$unused_img"
            echo "🗑️  Rimossa: $unused_img"
        done < "$UNUSED_FILE"
        echo "✅ Pulizia completata!"
    else
        echo "ℹ️  Pulizia annullata. File salvati in: $UNUSED_FILE"
    fi
fi

# Cleanup
rm -f all_images.txt "$USED_FILE" "$UNUSED_FILE" 2>/dev/null

echo ""
echo "📈 Spazio recuperato:"
du -sh "$IMG_DIR"
