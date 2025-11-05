#!/usr/bin/env python3
"""
Cloudinary URL Optimizer - Preview & Patch Mode
Reinserisce i parametri di ottimizzazione Cloudinary nei front matter Markdown
"""

import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import shutil
from datetime import datetime

# Parametri Cloudinary per tipologia
CLOUDINARY_PARAMS = {
    'image': 'f_auto,q_auto,dpr_auto,c_fill,ar_16:9,w_1600',
    'lcp_image': 'f_auto,q_auto,dpr_auto,c_fill,ar_16:9,w_1600',
    'background': 'f_auto,q_auto,dpr_auto,c_fill,ar_3:2,w_600',
    'og_image': 'f_jpg,q_auto,c_fill,ar_1.91:1,w_1200',
}

# Pattern per identificare URL Cloudinary senza ottimizzazione
CLOUDINARY_PATTERN = re.compile(
    r'(https://res\.cloudinary\.com/)([^/]+)(/image/upload/)(?!f_auto|f_jpg)([vV]\d+/)?([^\s\'"]+)',
    re.IGNORECASE
)

class CloudinaryOptimizer:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.changes: Dict[str, List[Tuple[str, str]]] = {}
        self.stats = {
            'files_scanned': 0,
            'files_with_changes': 0,
            'total_urls_fixed': 0
        }
        
    def find_markdown_files(self) -> List[Path]:
        """Trova tutti i file .md in _posts/, pages/ e root"""
        patterns = [
            '_posts/**/*.md',
            'pages/**/*.md',
            '*.md'
        ]
        
        files = []
        for pattern in patterns:
            files.extend(self.root_dir.glob(pattern))
        
        return sorted(set(files))
    
    def detect_field_type(self, line: str) -> str:
        """Rileva il tipo di campo YAML (image, background, lcp_image, og_image)"""
        line_lower = line.lower().strip()
        
        if line_lower.startswith('lcp_image:'):
            return 'lcp_image'
        elif line_lower.startswith('og_image:'):
            return 'og_image'
        elif line_lower.startswith('background:'):
            return 'background'
        elif line_lower.startswith('image:'):
            return 'image'
        
        return None
    
    def optimize_url(self, url: str, field_type: str) -> str:
        """Ottimizza un singolo URL Cloudinary"""
        match = CLOUDINARY_PATTERN.search(url)
        
        if not match:
            return url
        
        base_url = match.group(1)
        cloud_name = match.group(2)
        upload_path = match.group(3)
        version = match.group(4) or ''
        filename = match.group(5)
        
        # Seleziona parametri in base al tipo di campo
        params = CLOUDINARY_PARAMS.get(field_type, CLOUDINARY_PARAMS['image'])
        
        # Ricostruisci URL ottimizzato
        optimized = f"{base_url}{cloud_name}{upload_path}{params}/{version}{filename}"
        
        return optimized
    
    def process_file(self, filepath: Path) -> bool:
        """Processa un singolo file e raccoglie i cambiamenti"""
        self.stats['files_scanned'] += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Errore lettura {filepath}: {e}")
            return False
        
        lines = content.split('\n')
        changes = []
        in_frontmatter = False
        frontmatter_count = 0
        
        for i, line in enumerate(lines):
            # Traccia i delimitatori del front matter
            if line.strip() == '---':
                frontmatter_count += 1
                if frontmatter_count == 1:
                    in_frontmatter = True
                elif frontmatter_count == 2:
                    in_frontmatter = False
                continue
            
            # Processa solo righe dentro il front matter
            if not in_frontmatter or frontmatter_count != 1:
                continue
            
            # Rileva tipo di campo
            field_type = self.detect_field_type(line)
            
            if not field_type:
                continue
            
            # Cerca URL Cloudinary non ottimizzati
            match = CLOUDINARY_PATTERN.search(line)
            
            if match:
                old_url = match.group(0)
                new_url = self.optimize_url(old_url, field_type)
                
                if old_url != new_url:
                    old_line = line
                    new_line = line.replace(old_url, new_url)
                    changes.append((old_line, new_line, i + 1, field_type))
        
        if changes:
            self.changes[str(filepath)] = changes
            self.stats['files_with_changes'] += 1
            self.stats['total_urls_fixed'] += len(changes)
            return True
        
        return False
    
    def preview_changes(self):
        """Mostra preview di tutti i cambiamenti"""
        if not self.changes:
            print("✅ Nessun URL da ottimizzare trovato!")
            return
        
        print(f"\n{'='*80}")
        print(f"📋 PREVIEW CAMBIAMENTI - {self.stats['files_with_changes']} file(s) da modificare")
        print(f"{'='*80}\n")
        
        for filepath, changes in self.changes.items():
            rel_path = Path(filepath).relative_to(self.root_dir)
            print(f"\n📄 {rel_path}")
            print(f"   {len(changes)} URL da ottimizzare:\n")
            
            for old_line, new_line, line_num, field_type in changes:
                print(f"   Linea {line_num} ({field_type}):")
                print(f"   \033[91m- {old_line.strip()}\033[0m")
                print(f"   \033[92m+ {new_line.strip()}\033[0m")
                print()
        
        print(f"\n{'='*80}")
        print(f"📊 RIEPILOGO:")
        print(f"   • File analizzati: {self.stats['files_scanned']}")
        print(f"   • File da modificare: {self.stats['files_with_changes']}")
        print(f"   • URL da ottimizzare: {self.stats['total_urls_fixed']}")
        print(f"{'='*80}\n")
    
    def apply_changes(self, create_backup: bool = True):
        """Applica i cambiamenti ai file"""
        if not self.changes:
            return
        
        backup_dir = self.root_dir / f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if create_backup:
            backup_dir.mkdir(exist_ok=True)
            print(f"💾 Backup creato in: {backup_dir}\n")
        
        for filepath, changes in self.changes.items():
            filepath = Path(filepath)
            
            # Backup
            if create_backup:
                rel_path = filepath.relative_to(self.root_dir)
                backup_file = backup_dir / rel_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(filepath, backup_file)
            
            # Leggi contenuto
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Applica modifiche
            for old_line, new_line, _, _ in changes:
                content = content.replace(old_line, new_line)
            
            # Scrivi file modificato
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filepath.relative_to(self.root_dir)} - {len(changes)} URL ottimizzati")
        
        print(f"\n🎉 Completato! {self.stats['total_urls_fixed']} URL ottimizzati in {self.stats['files_with_changes']} file.")

def main():
    root_dir = Path(__file__).parent.parent
    
    print("\n🔍 Cloudinary URL Optimizer\n")
    print(f"📂 Directory: {root_dir}\n")
    
    optimizer = CloudinaryOptimizer(root_dir)
    
    # Trova file
    print("🔎 Ricerca file Markdown...")
    files = optimizer.find_markdown_files()
    print(f"   Trovati {len(files)} file .md\n")
    
    # Processa file
    print("⚙️  Analisi URL Cloudinary...")
    for filepath in files:
        optimizer.process_file(filepath)
    
    # Mostra preview
    optimizer.preview_changes()
    
    # Richiedi conferma
    if not optimizer.changes:
        return 0
    
    print("⚠️  ATTENZIONE: Stai per modificare i file sopra elencati.")
    response = input("   Vuoi procedere? [s/N]: ").strip().lower()
    
    if response in ['s', 'y', 'si', 'yes']:
        print("\n🚀 Applicazione modifiche...\n")
        optimizer.apply_changes(create_backup=True)
        return 0
    else:
        print("\n❌ Operazione annullata.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
