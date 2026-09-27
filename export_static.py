#!/usr/bin/env python3
"""
Static site exporter for GitHub Pages deployment.
Renders all Django templates, collects static assets, rewrites URLs for GitHub Pages repository subpath,
and outputs everything into dist/ folder ready to be published to gh-pages branch.
"""
import os
import shutil
import re
from pathlib import Path
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_config.settings')
django.setup()

from django.test import Client
from portfolio.models import Project

BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / 'dist'
REPO_PREFIX = '/portfolio/'

def clean_dist():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Cleaned {DIST_DIR}")

def rewrite_urls(html_content, prefix=REPO_PREFIX):
    """
    Rewrite root-relative URLs so they resolve correctly under GitHub Pages subpath (e.g. /portfolio/)
    """
    # Replace static assets
    html_content = re.sub(r'href=["\']/static/', f'href="{prefix}static/', html_content)
    html_content = re.sub(r'src=["\']/static/', f'src="{prefix}static/', html_content)
    
    # Replace media assets
    html_content = re.sub(r'href=["\']/media/', f'href="{prefix}media/', html_content)
    html_content = re.sub(r'src=["\']/media/', f'src="{prefix}media/', html_content)
    
    # Replace page links
    html_content = re.sub(r'href=["\']/resume/', f'href="{prefix}resume/', html_content)
    html_content = re.sub(r'href=["\']/project/', f'href="{prefix}project/', html_content)
    
    # Replace anchor hash links
    html_content = re.sub(r'href=["\']/#', f'href="{prefix}#', html_content)
    
    # Replace root home links
    html_content = re.sub(r'href=["\']/(["\'])', f'href="{prefix}\\1', html_content)
    
    # Replace favicon
    html_content = re.sub(r'href=["\']/favicon\.ico["\']', f'href="{prefix}favicon.ico"', html_content)
    
    # Form action to local anchor
    html_content = re.sub(r'action=["\']/[^"\']*#contact["\']', 'action="#contact"', html_content)

    return html_content

def export_site():
    clean_dist()
    client = Client()

    # 1. Render Home Page
    print("Rendering Home Page (/) ...")
    resp = client.get('/')
    assert resp.status_code == 200, f"Home page failed with {resp.status_code}"
    home_html = rewrite_urls(resp.content.decode('utf-8'))
    with open(DIST_DIR / 'index.html', 'w', encoding='utf-8') as f:
        f.write(home_html)
    print(f" -> Wrote {DIST_DIR / 'index.html'} ({len(home_html)} chars)")

    # 2. Render Resume Page (/resume/)
    print("Rendering Resume Page (/resume/) ...")
    resp = client.get('/resume/')
    assert resp.status_code == 200, f"Resume page failed with {resp.status_code}"
    resume_html = rewrite_urls(resp.content.decode('utf-8'))
    resume_dir = DIST_DIR / 'resume'
    resume_dir.mkdir(parents=True, exist_ok=True)
    with open(resume_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(resume_html)
    print(f" -> Wrote {resume_dir / 'index.html'} ({len(resume_html)} chars)")

    # 3. Render Project Detail Pages
    projects = Project.objects.all()
    print(f"Rendering {projects.count()} Project Detail Pages ...")
    for p in projects:
        resp = client.get(f'/project/{p.slug}/')
        assert resp.status_code == 200, f"Project {p.slug} failed with {resp.status_code}"
        proj_html = rewrite_urls(resp.content.decode('utf-8'))
        proj_dir = DIST_DIR / 'project' / p.slug
        proj_dir.mkdir(parents=True, exist_ok=True)
        with open(proj_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(proj_html)
        print(f" -> Wrote {proj_dir / 'index.html'} for {p.slug}")

    # 4. Copy Static Assets
    print("Copying static assets ...")
    static_src = BASE_DIR / 'portfolio' / 'static'
    static_dst = DIST_DIR / 'static'
    if static_src.exists():
        shutil.copytree(static_src, static_dst)
        print(f" -> Copied static assets from {static_src} to {static_dst}")

    # Copy Media Assets if present
    media_src = BASE_DIR / 'media'
    if media_src.exists():
        media_dst = DIST_DIR / 'media'
        shutil.copytree(media_src, media_dst)
        print(f" -> Copied media assets to {media_dst}")

    # 5. Create Favicon if needed
    fav_src = static_src / 'portfolio' / 'images' / 'isrel_profile.jpg'
    fav_dst = DIST_DIR / 'favicon.ico'
    if fav_src.exists() and not fav_dst.exists():
        shutil.copy2(fav_src, fav_dst)

    # 6. Create .nojekyll for GitHub Pages
    (DIST_DIR / '.nojekyll').touch()
    print(" -> Created .nojekyll")

    # 7. Create 404.html (fallback to index.html with redirect or message)
    with open(DIST_DIR / '404.html', 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="3; url=/portfolio/">
    <title>Page Not Found - ISREL Portfolio</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-6 text-center font-sans">
    <div class="max-w-md p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl">
        <h1 class="text-5xl font-extrabold text-cyan-400 mb-4">404</h1>
        <h2 class="text-xl font-bold text-white mb-2">Page Not Found</h2>
        <p class="text-sm text-slate-400 mb-6">The page you were looking for doesn't exist. Redirecting you back to the portfolio homepage...</p>
        <a href="/portfolio/" class="inline-block px-6 py-3 rounded-xl font-bold bg-cyan-500 text-slate-950 hover:bg-cyan-400 transition">Return to Home</a>
    </div>
</body>
</html>""")
    print(" -> Created 404.html")
    print("\n[SUCCESS] Static portfolio export completed successfully in dist/ directory.")

if __name__ == '__main__':
    export_site()
