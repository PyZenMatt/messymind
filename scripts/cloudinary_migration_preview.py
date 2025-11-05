#!/usr/bin/env python3
"""
Cloudinary Migration Script - Preview Mode
Migra immagini locali → Cloudinary con front matter standardizzato
"""

import re
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime

# Mapping file → URL Cloudinary base
MIGRATION_MAP = {
    '2025-02-25-come-ho-smesso-di-inseguire-il-tempo.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1756042377/accettazione_gmjnsx.png',
    '2024-10-21-le-fondamenta-della-felicita.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1762330002/sandwich_hlgntm.webp',
    '2024-10-22-autoconsapevolezza-e-felicita.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1756042405/velo_vbcr50.webp',
    '2025-02-11-cuore-e-mente-in-armonia.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1756042383/cuore_srndvo.jpg',
    '2025-02-18-e-mc2-spiritualita-verita-scomoda.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1756042397/relativita_pnbubc.webp',
    '2024-12-10-la-legge-del-ritmo.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1756042399/ritmo_pfwx3o.jpg',
    '2025-02-12-osservatore-e-osservato.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1756042395/osservatore_qtteo7.webp',
    '2025-02-15-arte-del-silenzio.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1756042401/silenzio_sjrsqk.webp',
    '2025-02-22-come-ritrovare-contatto-materia-oggetti-quotidiani.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1756042393/materialismo_qy6qqd.webp',
    '2025-05-11-kundalini.md': 'https://res.cloudinary.com/dkoc4knvv/image/upload/v1762329736/kundalini_1920_h2ueif.webp',
}

# Parametri Cloudinary per tipologia
def get_cloudinary_url(base_url: str, field_type: str) -> str:
    """Genera URL Cloudinary ottimizzato per tipologia campo"""
    # Estrai base_url senza parametri esistenti
    pattern = r'(https://res\.cloudinary\.com/[^/]+/image/upload/)(.+)'
    match = re.match(pattern, base_url)
    
    if not match:
        return base_url
    
    base = match.group(1)
    filename = match.group(2)
    
    # Parametri per tipologia
    params = {
        'image': 'f_auto,q_auto,dpr_auto,c_fill,ar_16:9,w_1600',
        'lcp_image': 'f_auto,q_auto,dpr_auto,c_fill,ar_16:9,w_1600',
        'background': 'f_auto,q_auto,dpr_auto,c_fill,ar_3:2,w_600',
        'og_image': 'f_jpg,q_auto,c_fill,ar_1.91:1,w_1200',
    }
    
    param = params.get(field_type, params['image'])
    return f"{base}{param}/{filename}"


def analyze_file(filepath: Path, base_url: str) -> Dict:
    """Analizza file e genera preview modifiche"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    changes = []
    
    # Analizza front matter
    in_fm = False
    fm_end_line = 0
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_fm:
                in_fm = True
            else:
                fm_end_line = i
                break
    
    # Trova campi immagine esistenti
    existing_fields = {}
    for i in range(fm_end_line):
        line = lines[i]
        for field in ['image', 'lcp_image', 'background', 'og_image']:
            if line.strip().startswith(f'{field}:'):
                existing_fields[field] = (i, line)
    
    # Genera nuovi valori
    new_fields = {
        'image': get_cloudinary_url(base_url, 'image'),
        'lcp_image': get_cloudinary_url(base_url, 'lcp_image'),
        'background': get_cloudinary_url(base_url, 'background'),
        'og_image': get_cloudinary_url(base_url, 'og_image'),
    }
    
    return {
        'filepath': filepath,
        'existing_fields': existing_fields,
        'new_fields': new_fields,
        'changes_needed': True
    }


def main():
    root = Path('/home/teo/Project/messymind.it')
    
    print("\n" + "="*80)
    print("🔍 CLOUDINARY MIGRATION - PREVIEW MODE")
    print("="*80 + "\n")
    
    files_found = []
    
    # Trova tutti i file
    for filename, base_url in MIGRATION_MAP.items():
        matches = list(root.glob(f'**/{filename}'))
        if matches:
            files_found.append((matches[0], base_url))
        else:
            print(f"⚠️  File non trovato: {filename}")
    
    print(f"📄 File trovati: {len(files_found)}/10\n")
    
    # Analizza e mostra preview
    for i, (filepath, base_url) in enumerate(files_found, 1):
        print(f"\n{'─'*80}")
        print(f"📝 {i}. {filepath.name}")
        print(f"   Path: {filepath.relative_to(root)}")
        print(f"{'─'*80}\n")
        
        analysis = analyze_file(filepath, base_url)
        
        # Mostra diff per ciascun campo
        for field, new_url in analysis['new_fields'].items():
            if field in analysis['existing_fields']:
                old_line_num, old_line = analysis['existing_fields'][field]
                print(f"   Campo: {field} (linea {old_line_num + 1})")
                print(f"   \033[91m- {old_line.strip()}\033[0m")
                print(f"   \033[92m+ {field}: {new_url}\033[0m")
            else:
                print(f"   Campo: {field} (NEW)")
                print(f"   \033[92m+ {field}: {new_url}\033[0m")
            print()
    
    print("\n" + "="*80)
    print("📊 RIEPILOGO")
    print("="*80)
    print(f"   • File da migrare: {len(files_found)}")
    print(f"   • Campi per file: 4 (image, lcp_image, background, og_image)")
    print(f"   • Totale URL da ottimizzare: {len(files_found) * 4}")
    print("="*80 + "\n")
    
    print("⚠️  QUESTO È UN DRY-RUN - Nessun file modificato")
    print("   Per applicare le modifiche, confermare con l'utente.\n")
    
    return 0


if __name__ == '__main__':
    main()
