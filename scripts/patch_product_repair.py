#!/usr/bin/env python3
"""Repair local app covers and remove unsupported Apple Books channels."""
from pathlib import Path
import re
import shutil
import sys
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('_site')
assets = root / 'assets/images'
assets.mkdir(parents=True, exist_ok=True)
for name in ('swiss-alpine-cover.webp', 'gentian-cover.webp'):
    source = Path('assets/images') / name
    if not source.is_file() or source.stat().st_size < 10000:
        raise SystemExit(f'Missing app cover: {source}')
    shutil.copyfile(source, assets / name)
css = '''.app-list-card .app-list-poster{height:auto;aspect-ratio:2.27/1;background:#102c49}
.app-list-card .app-list-poster img{width:100%;height:100%;display:block;object-fit:contain;object-position:center}
#apps .shop-product .shop-app-cover-frame{width:100%;aspect-ratio:2.18/1;background:#10283e;border-radius:12px;overflow:hidden;display:flex;align-items:center;justify-content:center}
#apps .shop-product .shop-app-cover-frame img{display:block;width:100%;height:100%;max-width:100%;object-fit:contain;object-position:center;box-shadow:none;border-radius:0}
.store-grid.kindle-only{grid-template-columns:minmax(0,720px);max-width:720px}
.store-card.kindle-card{padding:clamp(24px,4vw,36px)}
.store-card .amazon-brand{display:block;width:min(220px,100%);height:76px;margin:0 0 10px}
.store-card .amazon-brand svg{width:100%;height:100%;display:block;overflow:visible}
.store-card .amazon-brand text{fill:var(--ink);font-family:Arial,Helvetica,sans-serif;font-size:61px;font-weight:800;letter-spacing:-3px}
@media(max-width:700px){.store-grid.kindle-only{grid-template-columns:minmax(0,1fr)}}'''
styles = root / 'assets/css/product-repair.css'
styles.parent.mkdir(parents=True, exist_ok=True)
styles.write_text(css, encoding='utf-8')
logo = '''<span class="store-mark amazon-brand" role="img" aria-label="Amazon logo"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 270 110" aria-hidden="true" focusable="false"><text x="6" y="67">amazon</text><path d="M49 79 C94 102 168 107 228 77" stroke="#ff9900" stroke-width="6.5" stroke-linecap="round" fill="none"/><path d="M207 75 L232 72 L226 94" stroke="#ff9900" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg></span>'''
old_swiss = 'https://d2ol7oe51mr4n9.cloudfront.net/user_3Lum1zJjO96eiqJljGZPc2qT8El/f0a4d040-c71c-4648-866d-baaabba8f240.jpg'
old_gentian = 'https://d2ol7oe51mr4n9.cloudfront.net/user_3Lum1zJjO96eiqJljGZPc2qT8El/603cd314-aba1-4b19-b789-1c0c3d9d2e0d.png'

def relpaths(page):
    base = '../' * (len(page.relative_to(root).parts) - 1) + 'assets/images/'
    return base+'swiss-alpine-cover.webp', base+'gentian-cover.webp'

def with_css(html,page):
    prefix = '../' * (len(page.relative_to(root).parts) - 1)
    if 'product-repair.css' not in html:
        html=html.replace('</head>',f'<link rel="stylesheet" href="{prefix}assets/css/product-repair.css?v=20261122e">\n</head>',1)
    return html

for path in ('apps/index.html','tr/apps/index.html'):
    page = root / path
    html = page.read_text(encoding='utf-8')
    swiss,gentian=relpaths(page)
    for slug,cover in [('swiss-alpine-routes',swiss),('gentian',gentian)]:
        pattern=r'(<a class="app-list-poster" href="'+re.escape(slug)+r'/">\s*<img\s+src=")[^"]+("[^>]*>)'
        html,n=re.subn(pattern,lambda m:m.group(1)+cover+m.group(2),html,count=1)
        if n!=1:raise RuntimeError(f'Cannot locate {slug} in {page}')
    if path.startswith('tr/'):
        html=html.replace('İsviçre’deki yürüyüş ve dağ bisikleti rotalarını haritalar, planlama araçları ve güvenlik bilgileriyle keşfetmek için Türkçe açık hava uygulaması.', 'İsviçre haritaları, yürüyüş, bisiklet ve MTB rotaları, çevrimdışı GPS ve dağ güvenliği sunan İngilizce ve Türkçe uygulama.')
    else:
        html=html.replace('A Turkish-language outdoor companion for exploring Swiss hiking and mountain-bike routes with maps, planning tools and safety information.', 'An English- and Turkish-language outdoor companion with Swiss maps, hiking, cycling and MTB routes, offline navigation and mountain safety.')
    html=with_css(html,page)
    assert swiss in html and gentian in html and 'rotam-banner.webp' not in html
    page.write_text(html,encoding='utf-8')

for path in ('index.html','tr/index.html','shop/index.html','tr/shop/index.html','apps/swiss-alpine-routes/index.html','tr/apps/swiss-alpine-routes/index.html'):
    page=root/path
    html=page.read_text(encoding='utf-8')
    swiss,gentian=relpaths(page)
    html=html.replace(old_swiss,swiss).replace(old_gentian,gentian)
    if 'swiss-alpine-routes/index.html' in path:html=with_css(html,page)
    page.write_text(html,encoding='utf-8')

# The Apps page already uses the owner's original cover artwork. Apply those
# exact same local image files to both Shop cards without re-rendering or cropping.
for path in ('shop/index.html', 'tr/shop/index.html'):
    page=root/path
    html=page.read_text(encoding='utf-8')
    swiss,gentian=relpaths(page)
    before,tag,rest=html.partition('<section class="shop-section" id="apps">')
    if not tag:raise RuntimeError(f'Missing Shop Apps section: {page}')
    apps,close,after=rest.partition('</section>')
    if not close:raise RuntimeError(f'Malformed Shop Apps section: {page}')
    image_files=[(gentian,'Gentian original promotional cover with two iPhone screenshots'),
                 (swiss,'Swiss Alpine Routes original promotional cover with two iPhone screenshots')]
    it=iter(image_files)
    def use_original(m):
        src,alt=next(it)
        return m.group(1)+f'<div class="shop-app-cover-frame"><img src="{src}" alt="{alt}" loading="lazy" decoding="async"></div>'
    apps,n=re.subn(r'(<article class="shop-product(?: sar-shop)?">)\s*<img\b[^>]*>',use_original,apps)
    if n!=2:raise RuntimeError(f'Expected both app cards; found {n}: {page}')
    html=before+tag+apps+close+after
    html=with_css(html,page)
    if 'gentian-banner.webp' in apps:raise RuntimeError('Outdated Gentian banner remained')
    for src in (swiss,gentian):
        if apps.count(src)!=1 or not (page.parent/src).is_file():
            raise RuntimeError(f'Shop artwork not found or repeated: {src}')
    page.write_text(html,encoding='utf-8')

for path in ('books/index.html','books/awooo-chronicles/index.html','books/awooo-the-tale-of-a-husky/index.html','tr/books/index.html','tr/books/awooo-chronicles/index.html','tr/books/awooo-the-tale-of-a-husky/index.html'):
    page=root/path
    html=page.read_text(encoding='utf-8')
    html,removed=re.subn(r'<div class="store-card">\s*<span class="store-mark apple-book">.*?</div>','',html,flags=re.S)
    if removed!=1:raise RuntimeError(f'Apple Books card count {removed}: {page}')
    html,renamed=re.subn(r'<span class="store-mark">kindle</span>',lambda _:logo,html,count=1)
    if renamed!=1:raise RuntimeError(f'Amazon placeholder count {renamed}: {page}')
    html,count=re.subn(r'<div class="store-grid">','<div class="store-grid kindle-only">',html,count=1)
    if count!=1:raise RuntimeError(f'Bookstore grid count {count}: {page}')
    html=html.replace('<div class="store-card">'+logo,'<div class="store-card kindle-card">'+logo,1)
    html=with_css(html,page)
    assert 'Apple Books' not in html and 'apple-book' not in html and 'amazon-brand' in html
    page.write_text(html,encoding='utf-8')

for path in ('apps/index.html','tr/apps/index.html'):
    html=(root/path).read_text(encoding='utf-8')
    assert 'swiss-alpine-cover.webp' in html and 'gentian-cover.webp' in html
for path in ('books/awooo-chronicles/index.html','books/awooo-the-tale-of-a-husky/index.html','tr/books/awooo-chronicles/index.html','tr/books/awooo-the-tale-of-a-husky/index.html'):
    html=(root/path).read_text(encoding='utf-8')
    assert html.count('class="store-card')==1
    assert 'Amazon Kindle' in html and 'Apple Books' not in html
print('Validated: both app covers and six Kindle-only book pages (EN/TR)')
