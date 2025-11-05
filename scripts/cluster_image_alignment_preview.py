#!/usr/bin/env python3
"""
Preview allineamento immagini cluster → articolo cornerstone principale
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
CLUSTER_DIR = WORKSPACE / "pages/categories"
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

def optimize_cloudinary_url(url):
    """Aggiunge parametri Cloudinary se non presenti"""
    if not url or 'cloudinary.com' not in url:
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

def find_cluster_cornerstone(category_slug):
    """
    Trova il cornerstone principale di un cluster.
    Logica: primo post con tag 'cornerstone' nella categoria,
    oppure il cornerstone con più tags se ce ne sono multipli.
    """
    cornerstones = []
    
    for post_file in POSTS_DIR.rglob("*.md"):
        front_matter, _ = extract_front_matter(post_file)
        if not front_matter:
            continue
        
        # Verifica categoria
        categories = front_matter.get('categories', [])
        if isinstance(categories, str):
            categories = [categories]
        
        if category_slug not in categories:
            continue
        
        # Verifica tag cornerstone
        tags = front_matter.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        if 'cornerstone' not in tags:
            continue
        
        # Estrai immagine
        image = front_matter.get('image') or front_matter.get('lcp_image')
        if not image:
            continue
        
        cornerstones.append({
            'file': str(post_file.relative_to(WORKSPACE)),
            'image': image,
            'title': front_matter.get('title', 'N/A'),
            'tags_count': len(tags),
            'featured': front_matter.get('featured', False)
        })
    
    if not cornerstones:
        return None
    
    # Priorità: featured > più tags > primo trovato
    cornerstones.sort(key=lambda x: (
        -1 if x['featured'] else 0,
        -x['tags_count']
    ))
    
    return cornerstones[0]

def analyze_clusters():
    """Analizza cluster e genera preview diff"""
    changes = []
    
    for cluster_file in CLUSTER_DIR.glob("*.md"):
        front_matter, full_content = extract_front_matter(cluster_file)
        if not front_matter:
            continue
        
        category = front_matter.get('category')
        if not category:
            continue
        
        # Verifica se usa immagine custom o default
        current_image = front_matter.get('image', '')
        current_hero = front_matter.get('hero_image', '')
        current_lcp = front_matter.get('lcp_image', '')
        
        # Skip se già ha immagini custom (non og-default)
        if current_image and 'og-default' not in current_image:
            continue
        
        # Cerca cornerstone principale
        cornerstone = find_cluster_cornerstone(category)
        
        if not cornerstone:
            print(f"{YELLOW}⚠ Nessun cornerstone trovato per cluster: {category}{RESET}")
            continue
        
        new_image = optimize_cloudinary_url(cornerstone['image'])
        
        changes.append({
            'cluster_file': str(cluster_file.relative_to(WORKSPACE)),
            'cluster_title': front_matter.get('title', 'N/A'),
            'category': category,
            'current_image': current_image or '(vuoto)',
            'current_hero': current_hero or '(vuoto)',
            'current_lcp': current_lcp or '(vuoto)',
            'new_image': new_image,
            'cornerstone_file': cornerstone['file'],
            'cornerstone_title': cornerstone['title'],
            'full_content': full_content,
            'absolute_path': str(cluster_file)
        })
    
    return changes

def print_preview(changes):
    """Stampa preview colorato delle modifiche"""
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}DRY-RUN PREVIEW — Allineamento Immagini Cluster → Cornerstone{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
    
    if not changes:
        print(f"{YELLOW}✓ Nessuna modifica necessaria: tutti i cluster già allineati.{RESET}\n")
        return
    
    print(f"{BOLD}File da modificare: {len(changes)}{RESET}\n")
    
    for i, change in enumerate(changes, 1):
        print(f"{BOLD}{BLUE}[{i}/{len(changes)}] {change['cluster_title']}{RESET}")
        print(f"  {CYAN}File:{RESET} {change['cluster_file']}")
        print(f"  {CYAN}Categoria:{RESET} {change['category']}")
        print(f"  {CYAN}Cornerstone:{RESET} {change['cornerstone_title']}")
        print(f"  {CYAN}Fonte:{RESET} {change['cornerstone_file']}\n")
        
        # Mostra solo i campi che verranno modificati
        if change['current_image'] and change['current_image'] != '(vuoto)':
            print(f"  {RED}− image: {change['current_image']}{RESET}")
            print(f"  {GREEN}+ image: {change['new_image']}{RESET}\n")
        
        if change['current_hero'] and change['current_hero'] != '(vuoto)':
            print(f"  {RED}− hero_image: {change['current_hero']}{RESET}")
            print(f"  {GREEN}+ hero_image: {change['new_image']}{RESET}\n")
        
        if change['current_lcp'] and change['current_lcp'] != '(vuoto)':
            print(f"  {RED}− lcp_image: {change['current_lcp']}{RESET}")
            print(f"  {GREEN}+ lcp_image: {change['new_image']}{RESET}\n")
        
        print(f"  {'-'*78}\n")
    
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}Riepilogo modifiche:{RESET}")
    print(f"  • File cluster da aggiornare: {GREEN}{len(changes)}{RESET}")
    print(f"  • Campi per file: {GREEN}image, hero_image, lcp_image{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
    
    print(f"{YELLOW}⚠ GUARDRAIL:{RESET}")
    print(f"  • Nessun permalink/slug modificato")
    print(f"  • Nessun schema JSON-LD toccato")
    print(f"  • Solo image + hero_image + lcp_image aggiornati")
    print(f"  • Backup automatico in .backup_cluster_*/\n")
    
    # Tabella mapping
    print(f"{BOLD}{CYAN}Tabella Mapping Cluster → Cornerstone:{RESET}\n")
    print(f"{'CLUSTER':<40} {'CORNERSTONE':<50}")
    print(f"{'-'*90}")
    for change in changes:
        cluster_name = change['category']
        cornerstone_short = Path(change['cornerstone_file']).name
        print(f"{cluster_name:<40} {cornerstone_short:<50}")
    print()

def generate_apply_script(changes):
    """Genera script Python per applicare modifiche"""
    if not changes:
        return
    
    script_path = WORKSPACE / "scripts/apply_cluster_alignment.py"
    
    script_content = f'''#!/usr/bin/env python3
"""
Script di applicazione allineamento immagini cluster.
Generato automaticamente il {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

UTILIZZO:
    python3 scripts/apply_cluster_alignment.py
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

CHANGES = {changes!r}

def apply_changes():
    """Applica modifiche ai file cluster"""
    
    # Crea backup
    backup_dir = Path("/home/teo/Project/messymind.it") / f".backup_cluster_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}"
    backup_dir.mkdir(exist_ok=True)
    print(f"✓ Backup creato: {{backup_dir}}")
    
    for i, change in enumerate(CHANGES, 1):
        file_path = Path(change['absolute_path'])
        
        # Backup file originale
        backup_file = backup_dir / file_path.name
        shutil.copy2(file_path, backup_file)
        
        # Leggi contenuto
        content = change['full_content']
        
        # Sostituisci image (se presente)
        if change['current_image'] != '(vuoto)':
            old_pattern = re.escape(f'image: {{change["current_image"]}}')
            new_line = f'image: {{change["new_image"]}}'
            content = re.sub(old_pattern, new_line, content)
        
        # Sostituisci hero_image (se presente)
        if change['current_hero'] != '(vuoto)':
            old_pattern = re.escape(f'hero_image: {{change["current_hero"]}}')
            new_line = f'hero_image: {{change["new_image"]}}'
            content = re.sub(old_pattern, new_line, content)
        
        # Sostituisci lcp_image (se presente)
        if change['current_lcp'] != '(vuoto)':
            old_pattern = re.escape(f'lcp_image: {{change["current_lcp"]}}')
            new_line = f'lcp_image: {{change["new_image"]}}'
            content = re.sub(old_pattern, new_line, content)
        
        # Scrivi file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[{{i}}/{{len(CHANGES)}}] ✓ {{change['cluster_title']}}")
    
    print(f"\\n✓ {{len(CHANGES)}} file aggiornati con successo!")
    print(f"✓ Backup salvato in: {{backup_dir}}")
    print(f"\\nEsegui build Jekyll: bundle exec jekyll build --config _config.dev.yml")

if __name__ == '__main__':
    print("\\n⚠ ATTENZIONE: Stai per modificare {{len(CHANGES)}} file cluster.")
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
    print(f"{BOLD}{CYAN}Analisi cluster in corso...{RESET}\n")
    
    # Analizza cluster
    changes = analyze_clusters()
    
    # Stampa preview
    print_preview(changes)
    
    # Genera script di applicazione
    if changes:
        generate_apply_script(changes)
        
        print(f"{YELLOW}NEXT STEP:{RESET}")
        print(f"  1. Rivedi la preview sopra")
        print(f"  2. Se OK, esegui: {CYAN}python3 scripts/apply_cluster_alignment.py{RESET}")
        print(f"  3. Verifica build: {CYAN}bundle exec jekyll build --config _config.dev.yml{RESET}\n")
    else:
        print(f"{GREEN}✓ Nessuna azione necessaria.{RESET}\n")

if __name__ == '__main__':
    main()
