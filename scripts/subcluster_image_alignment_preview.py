#!/usr/bin/env python3
"""
Preview allineamento immagini subcluster → articolo cornerstone
Dry-run obbligatorio prima di applicare modifiche.
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

WORKSPACE = Path("/home/teo/Project/messymind.it")
SUBCLUSTER_DIR = WORKSPACE / "pages/categories/sub_cluster"
POSTS_DIR = WORKSPACE / "_posts"

# Cloudinary optimization template
CLOUDINARY_PARAMS = "f_auto,q_auto,dpr_auto,c_fill,ar_16:9,w_1600"

def extract_front_matter(file_path):
    """Estrae front matter YAML da file Markdown"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None, content
    
    try:
        front_matter = yaml.safe_load(match.group(1))
        return front_matter, content
    except yaml.YAMLError as e:
        print(f"{RED}✗ Errore YAML in {file_path}: {e}{RESET}")
        return None, content

def find_cornerstone_posts():
    """Trova tutti gli articoli cornerstone con metadati"""
    cornerstones = {}
    
    for post_file in POSTS_DIR.rglob("*.md"):
        front_matter, _ = extract_front_matter(post_file)
        if not front_matter:
            continue
        
        tags = front_matter.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        if 'cornerstone' not in tags:
            continue
        
        # Ricava subcluster dal path
        # Pattern: _posts/category/subcluster/file.md
        parts = post_file.relative_to(POSTS_DIR).parts
        if len(parts) >= 3:
            category = parts[0]
            subcluster = parts[1]
        elif len(parts) == 2:
            # Caso _posts/category/file.md
            category = parts[0]
            subcluster = None
        else:
            continue
        
        # Estrai immagine (priorità: image > lcp_image)
        image = front_matter.get('image') or front_matter.get('lcp_image')
        
        if not image:
            continue
        
        key = f"{category}:{subcluster}" if subcluster else category
        
        cornerstones[key] = {
            'file': str(post_file.relative_to(WORKSPACE)),
            'image': image,
            'title': front_matter.get('title', 'N/A'),
            'category': category,
            'subcluster': subcluster
        }
    
    return cornerstones

def optimize_cloudinary_url(url):
    """Aggiunge parametri Cloudinary se non presenti"""
    if 'cloudinary.com' not in url:
        return url
    
    # Se già ottimizzato, restituisce invariato
    if 'f_auto' in url:
        return url
    
    # Inserisce parametri dopo /upload/
    pattern = r'(cloudinary\.com/[^/]+/image/upload/)(.+)'
    match = re.search(pattern, url)
    if match:
        return f"{match.group(1)}{CLOUDINARY_PARAMS}/{match.group(2)}"
    
    return url

def analyze_subclusters(cornerstones):
    """Analizza subcluster e genera preview diff"""
    changes = []
    
    for subcluster_file in SUBCLUSTER_DIR.rglob("*.md"):
        front_matter, full_content = extract_front_matter(subcluster_file)
        if not front_matter:
            continue
        
        category = front_matter.get('category') or front_matter.get('cluster')
        subcluster = front_matter.get('subcluster')
        
        if not category or not subcluster:
            continue
        
        # Verifica se usa ancora og-default
        current_image = front_matter.get('image', '')
        current_hero = front_matter.get('hero_image', '')
        
        if 'og-default.jpg' not in current_image and 'og-default.jpg' not in current_hero:
            continue
        
        # Cerca cornerstone corrispondente
        key = f"{category}:{subcluster}"
        cornerstone = cornerstones.get(key)
        
        if not cornerstone:
            print(f"{YELLOW}⚠ Nessun cornerstone trovato per {key}{RESET}")
            continue
        
        new_image = optimize_cloudinary_url(cornerstone['image'])
        
        changes.append({
            'subcluster_file': str(subcluster_file.relative_to(WORKSPACE)),
            'subcluster_title': front_matter.get('title', 'N/A'),
            'category': category,
            'subcluster': subcluster,
            'current_image': current_image,
            'current_hero': current_hero,
            'new_image': new_image,
            'cornerstone_file': cornerstone['file'],
            'cornerstone_title': cornerstone['title'],
            'full_content': full_content,
            'absolute_path': str(subcluster_file)
        })
    
    return changes

def print_preview(changes):
    """Stampa preview colorato delle modifiche"""
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}DRY-RUN PREVIEW — Allineamento Immagini Subcluster → Cornerstone{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
    
    if not changes:
        print(f"{YELLOW}✓ Nessuna modifica necessaria: tutti i subcluster già allineati.{RESET}\n")
        return
    
    print(f"{BOLD}File da modificare: {len(changes)}{RESET}\n")
    
    for i, change in enumerate(changes, 1):
        print(f"{BOLD}{BLUE}[{i}/{len(changes)}] {change['subcluster_title']}{RESET}")
        print(f"  {CYAN}File:{RESET} {change['subcluster_file']}")
        print(f"  {CYAN}Categoria:{RESET} {change['category']} → {change['subcluster']}")
        print(f"  {CYAN}Cornerstone:{RESET} {change['cornerstone_title']}")
        print(f"  {CYAN}Fonte:{RESET} {change['cornerstone_file']}\n")
        
        print(f"  {RED}− image: {change['current_image']}{RESET}")
        print(f"  {GREEN}+ image: {change['new_image']}{RESET}\n")
        
        print(f"  {RED}− hero_image: {change['current_hero']}{RESET}")
        print(f"  {GREEN}+ hero_image: {change['new_image']}{RESET}\n")
        
        print(f"  {'-'*78}\n")
    
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}Riepilogo modifiche:{RESET}")
    print(f"  • File subcluster da aggiornare: {GREEN}{len(changes)}{RESET}")
    print(f"  • Campi per file: {GREEN}2{RESET} (image, hero_image)")
    print(f"  • Totale sostituzioni: {GREEN}{len(changes) * 2}{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
    
    print(f"{YELLOW}⚠ GUARDRAIL:{RESET}")
    print(f"  • Nessun permalink/slug modificato")
    print(f"  • Nessun schema JSON-LD toccato")
    print(f"  • Solo image + hero_image aggiornati")
    print(f"  • Backup automatico in .backup_subcluster_*/\n")
    
    # Tabella mapping
    print(f"{BOLD}{CYAN}Tabella Mapping Subcluster → Cornerstone:{RESET}\n")
    print(f"{'SUBCLUSTER':<40} {'CORNERSTONE':<50}")
    print(f"{'-'*90}")
    for change in changes:
        subcluster_name = f"{change['category']}/{change['subcluster']}"
        cornerstone_short = Path(change['cornerstone_file']).name
        print(f"{subcluster_name:<40} {cornerstone_short:<50}")
    print()

def generate_apply_script(changes):
    """Genera script Python per applicare modifiche"""
    if not changes:
        return
    
    script_path = WORKSPACE / "scripts/apply_subcluster_alignment.py"
    
    script_content = f'''#!/usr/bin/env python3
"""
Script di applicazione allineamento immagini subcluster.
Generato automaticamente il {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

UTILIZZO:
    python3 scripts/apply_subcluster_alignment.py
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

CHANGES = {changes!r}

def apply_changes():
    """Applica modifiche ai file subcluster"""
    
    # Crea backup
    backup_dir = Path("/home/teo/Project/messymind.it") / f".backup_subcluster_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}"
    backup_dir.mkdir(exist_ok=True)
    print(f"✓ Backup creato: {{backup_dir}}")
    
    for i, change in enumerate(CHANGES, 1):
        file_path = Path(change['absolute_path'])
        
        # Backup file originale
        backup_file = backup_dir / file_path.name
        shutil.copy2(file_path, backup_file)
        
        # Leggi contenuto
        content = change['full_content']
        
        # Sostituisci image
        old_image_line = f'image: "{{change["current_image"]}}"'
        new_image_line = f'image: "{{change["new_image"]}}"'
        content = content.replace(old_image_line, new_image_line)
        
        # Gestisci anche senza virgolette
        old_image_line_noq = f'image: {{change["current_image"]}}'
        new_image_line_noq = f'image: {{change["new_image"]}}'
        content = content.replace(old_image_line_noq, new_image_line_noq)
        
        # Sostituisci hero_image
        old_hero_line = f'hero_image: "{{change["current_hero"]}}"'
        new_hero_line = f'hero_image: "{{change["new_image"]}}"'
        content = content.replace(old_hero_line, new_hero_line)
        
        # Gestisci anche senza virgolette
        old_hero_line_noq = f'hero_image: {{change["current_hero"]}}'
        new_hero_line_noq = f'hero_image: {{change["new_image"]}}'
        content = content.replace(old_hero_line_noq, new_hero_line_noq)
        
        # Scrivi file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[{{i}}/{{len(CHANGES)}}] ✓ {{change['subcluster_title']}}")
    
    print(f"\\n✓ {{len(CHANGES)}} file aggiornati con successo!")
    print(f"✓ Backup salvato in: {{backup_dir}}")
    print(f"\\nEsegui build Jekyll: bundle exec jekyll build --config _config.dev.yml")

if __name__ == '__main__':
    print("\\n⚠ ATTENZIONE: Stai per modificare {{len(CHANGES)}} file subcluster.")
    confirm = input("Confermi applicazione modifiche? [s/N]: ")
    if confirm.lower() == 's':
        apply_changes()
    else:
        print("✗ Operazione annullata.")
'''
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    print(f"{GREEN}✓ Script di applicazione generato: {script_path}{RESET}")
    print(f"{CYAN}  Esegui con: python3 {script_path}{RESET}\n")

def main():
    print(f"{BOLD}{CYAN}Analisi in corso...{RESET}\n")
    
    # Step 1: Trova articoli cornerstone
    cornerstones = find_cornerstone_posts()
    print(f"✓ Trovati {len(cornerstones)} articoli cornerstone\n")
    
    # Step 2: Analizza subcluster
    changes = analyze_subclusters(cornerstones)
    
    # Step 3: Stampa preview
    print_preview(changes)
    
    # Step 4: Genera script di applicazione
    if changes:
        generate_apply_script(changes)
        
        print(f"{YELLOW}NEXT STEP:{RESET}")
        print(f"  1. Rivedi la preview sopra")
        print(f"  2. Se OK, esegui: {CYAN}python3 scripts/apply_subcluster_alignment.py{RESET}")
        print(f"  3. Verifica build: {CYAN}bundle exec jekyll build --config _config.dev.yml{RESET}\n")
    else:
        print(f"{GREEN}✓ Nessuna azione necessaria.{RESET}\n")

if __name__ == '__main__':
    main()
