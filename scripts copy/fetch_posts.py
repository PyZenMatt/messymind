import os
import requests
import yaml
from datetime import datetime

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000/api/blog/posts/")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "_posts")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN")  # es: https://messymind.it

os.makedirs(OUTPUT_DIR, exist_ok=True)

params = {}
if SITE_DOMAIN:
    params['site'] = SITE_DOMAIN

print(f"Fetching posts from {API_URL} for site: {SITE_DOMAIN or 'ALL'}")
resp = requests.get(API_URL, params=params)
resp.raise_for_status()
data = resp.json()

for post in data.get('results', []):
    # Frontmatter YAML
    frontmatter = {
        'title': post['title'],
        'date': post['published_at'],
        'author': post['author']['name'] if post['author'] else None,
        'categories': [cat['slug'] for cat in post['categories']],
        'site': post['site']['domain'],
        'slug': post['slug'],
        'published': post['is_published'],
        'updated_at': post['updated_at'],
    }
    # Commenti come lista YAML
    comments = post.get('comments', [])
    if comments:
        frontmatter['comments'] = [
            {
                'author': c['author_name'],
                'email': c['author_email'],
                'text': c['text'],
                'created_at': c['created_at'],
            } for c in comments
        ]
    # File name Jekyll: YYYY-MM-DD-slug.md
    pub_date = datetime.fromisoformat(post['published_at'].replace('Z', '+00:00'))
    filename = f"{pub_date.strftime('%Y-%m-%d')}-{post['slug']}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    # Scrivi file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(frontmatter, f, allow_unicode=True, sort_keys=False)
        f.write('---\n\n')
        f.write(post['content'])
    print(f"Wrote {filepath}")
