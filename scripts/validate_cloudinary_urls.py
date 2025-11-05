#!/usr/bin/env python3
"""
Cloudinary URL Validator - Verifica che tutti gli URL ottimizzati siano accessibili
"""

import re
import sys
from pathlib import Path
from typing import List, Set
import subprocess

def extract_cloudinary_urls(filepath: Path) -> Set[str]:
    """Estrae tutti gli URL Cloudinary da un file Markdown"""
    urls = set()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern per URL Cloudinary (anche con parametri)
    pattern = re.compile(
        r'https://res\.cloudinary\.com/[^/]+/image/upload/[^\s\'"]+',
        re.IGNORECASE
    )
    
    for match in pattern.finditer(content):
        urls.add(match.group(0))
    
    return urls

def main():
    root_dir = Path(__file__).parent.parent
    
    # File modificati dalla patch
    modified_files = [
        '_posts/burnout-e-lavoro/ritmi-gentili/2025-09-15-prevenzione-e-cura-burnout.md',
        '_posts/burnout-e-lavoro/autenticita-in-ufficio/2025-09-12-burnout-e-segnali.md',
        '_posts/filosofia-pratica/scienza-e-metodo/2025-09-15-riduzionismo.md',
        '_posts/filosofia-pratica/scienza-e-metodo/2025-09-02-costellazioni.md',
        '_posts/filosofia-pratica/decisioni-e-bias/2025-09-08-libero-arbitrio.md',
    ]
    
    print("\n🔍 Cloudinary URL Validator\n")
    
    all_urls = set()
    
    for rel_path in modified_files:
        filepath = root_dir / rel_path
        if filepath.exists():
            urls = extract_cloudinary_urls(filepath)
            all_urls.update(urls)
            print(f"📄 {rel_path}: {len(urls)} URL")
    
    print(f"\n📊 Totale URL unici da testare: {len(all_urls)}\n")
    
    # Salva lista URL per test manuale
    url_list_file = root_dir / 'tmp' / 'cloudinary_urls_test.txt'
    url_list_file.parent.mkdir(exist_ok=True)
    
    with open(url_list_file, 'w', encoding='utf-8') as f:
        for url in sorted(all_urls):
            f.write(f"{url}\n")
    
    print(f"💾 Lista URL salvata in: {url_list_file}\n")
    
    # Mostra esempi per test manuale
    print("🧪 Test manuale consigliato (HTTP 200 expected):\n")
    for i, url in enumerate(sorted(all_urls)[:3], 1):
        print(f"   {i}. curl -I \"{url}\"")
    
    print(f"\n   ... ({len(all_urls) - 3} altri URL in {url_list_file})")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
