#!/usr/bin/env python3
"""Align Shop and Apps listing cards with the approved homepage Apps design.

Source artwork is never regenerated, edited, or replaced. Marketing phrases
'Offline' / 'Çevrimdışı' are omitted only from the requested short summaries.
"""
from pathlib import Path
import re
import sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
images=root/"assets/images"
for required in ("gentian-cover.webp","swiss-alpine-cover.webp","swiss-alpine-icon.png","gentian-banner.webp"):
    if not (images/required).is_file():
        raise RuntimeError(f"Required authentic image missing: {required}")

style=r"""
/* Consistent premium product-card hierarchy: icon + title + strapline, cover, CTA. */
.shop-product.showcase-product{display:flex;flex-direction:column;gap:0;min-width:0}
.showcase-heading{display:flex;align-items:center;gap:13px;min-width:0}
.shop-product.showcase-product>.showcase-heading{min-height:82px;margin:0 0 17px}
.showcase-logo{display:block;flex:0 0 54px;width:54px;height:54px;border-radius:14px;object-fit:cover;box-shadow:0 5px 14px rgba(10,33,48,.16);background-color:#123047}
/* The generic .shop-product img width:100% rule must never stretch the header app icon. */
.shop-product.showcase-product .showcase-heading img.showcase-logo{
 width:54px;height:54px;min-width:54px;max-width:54px;flex:0 0 54px;object-fit:cover
}
.shop-product.showcase-product .showcase-heading .showcase-title{
 flex:1 1 auto;min-width:0
}
.shop-product.showcase-product .showcase-heading .showcase-title h3{
 overflow-wrap:normal;word-break:normal;hyphens:none
}
.showcase-logo-gentian{background-image:url('../images/gentian-banner.webp');background-repeat:no-repeat;background-size:1275% auto;background-position:36.9% 35.3%}
.showcase-title{min-width:0}
.shop-product.showcase-product .showcase-title h3,
.app-list-card.showcase-app-list-card .showcase-title h2{font-size:clamp(16px,1.75vw,21px);font-weight:760;line-height:1.22;letter-spacing:-.025em;margin:0 0 5px;overflow-wrap:break-word}
.shop-product.showcase-product .showcase-title p,
.app-list-card.showcase-app-list-card .showcase-title p{font-size:clamp(12px,1.25vw,14px);line-height:1.4;color:var(--muted);margin:0;min-height:0}
.shop-product.showcase-product .showcase-cover{display:block;aspect-ratio:2.18/1;width:100%;margin:0 0 18px;border-radius:13px;background:#10283e;overflow:hidden}
.shop-product.showcase-product .showcase-cover img{display:block;width:100%;height:100%;object-fit:contain;object-position:center;border-radius:0;box-shadow:none}
.shop-product.showcase-product .showcase-actions{margin-top:auto;display:flex;flex-direction:column;align-items:flex-start;gap:12px}
.shop-product.showcase-product .showcase-actions .button{max-width:100%;margin:0;white-space:normal;text-align:center}
.shop-product.showcase-product .showcase-actions .shop-platform-link{margin:0}
.app-list-card.showcase-app-list-card .showcase-heading{min-height:94px;padding:21px 24px 17px}
.app-list-card.showcase-app-list-card .showcase-cover{display:block;margin:0 24px;width:calc(100% - 48px);height:auto;aspect-ratio:2.18/1;border-radius:14px;overflow:hidden;background:#10283e}
.app-list-card.showcase-app-list-card .showcase-cover img{display:block;width:100%;height:100%;object-fit:contain;object-position:center}
.app-list-card.showcase-app-list-card .app-list-body{padding-top:20px}
@media(max-width:760px){
 .shop-product.showcase-product{padding:13px 11px 17px;border-radius:16px}
 .shop-product.showcase-product>.showcase-heading{gap:8px;min-height:69px;margin-bottom:11px;align-items:center}
 .showcase-logo{width:39px;height:39px;flex-basis:39px;border-radius:11px}
 .shop-product.showcase-product .showcase-heading img.showcase-logo{
  width:39px;height:39px;min-width:39px;max-width:39px;flex-basis:39px
 }
 .shop-product.showcase-product .showcase-title h3,
 .app-list-card.showcase-app-list-card .showcase-title h2{font-size:clamp(12px,3.5vw,18px);line-height:1.2;letter-spacing:-.015em}
 .shop-product.showcase-product .showcase-title p,
 .app-list-card.showcase-app-list-card .showcase-title p{font-size:clamp(10px,2.6vw,12px);line-height:1.35}
 .shop-product.showcase-product .showcase-cover{margin-bottom:15px;border-radius:10px}
 .shop-product.showcase-product .showcase-actions{gap:10px}
 .shop-product.showcase-product .showcase-actions .button{font-size:clamp(11px,2.7vw,14px);padding:11px 10px}
 .shop-product.showcase-product .showcase-actions .shop-platform-link{font-size:clamp(11px,2.7vw,14px);overflow-wrap:anywhere}
 .app-list-card.showcase-app-list-card .showcase-heading{padding:16px 15px 12px;gap:9px;min-height:76px}
 .app-list-card.showcase-app-list-card .showcase-cover{width:calc(100% - 30px);margin:0 15px;border-radius:10px}
 .app-list-card.showcase-app-list-card .app-list-body{padding-top:16px}
}
/* On narrow phones, app listings need full-width cards for readable titles
   and product imagery. The two-column Books cards stay unchanged. */
@media(max-width:650px){
 .shop-section#apps .shop-product-grid{grid-template-columns:minmax(0,1fr)}
 .shop-section#apps .shop-product.showcase-product{min-width:0;max-width:100%}
 .shop-section#apps .shop-product.showcase-product>.showcase-heading{width:100%;min-width:0}
 .shop-section#apps .shop-product.showcase-product .showcase-title h3{font-size:18px}
 .shop-section#apps .shop-product.showcase-product .showcase-title p{font-size:12px}
 .shop-section#apps .shop-product.showcase-product .showcase-cover{width:100%;max-width:100%}
}
"""
css=root/"assets/css/showcase-cards.css"
css.write_text(style,encoding="utf-8")

def head(page,tr,kind):
    relative="../"*(len(page.relative_to(root).parts)-1)
    if kind=="gentian":
        icon='<span class="showcase-logo showcase-logo-gentian" role="img" aria-label="Gentian app icon"></span>'
        title="Gentian – Swiss Alps"
        sub="Top 100 · Arabasız gezi planlama" if tr else "Top 100 · Car-free trip planning"
    else:
        icon=f'<img class="showcase-logo" src="{relative}assets/images/swiss-alpine-icon.png" alt="Swiss Alpine Routes original red app icon">'
        title="Swiss Alpine Routes"
        sub="İsviçre haritaları · Yürüyüş · Bisiklet · MTB" if tr else "Swiss maps · Hiking · Cycling · MTB"
    heading="h2" if "/apps/" in "/"+page.relative_to(root).as_posix() else "h3"
    return f'<div class="showcase-heading">{icon}<div class="showcase-title"><{heading}>{title}</{heading}><p>{sub}</p></div></div>'

def css_link(html,page):
    relative="../"*(len(page.relative_to(root).parts)-1)
    href=f'{relative}assets/css/showcase-cards.css?v=20261123b'
    return html.replace('</head>',f'<link rel="stylesheet" href="{href}">\n</head>',1)

for lang in ("en","tr"):
    tr=lang=="tr"
    prefix="tr/" if tr else ""
    page=root/(prefix+"shop/index.html")
    doc=page.read_text(encoding="utf-8")
    before,sep,after=doc.partition('<section class="shop-section" id="apps">')
    if not sep: raise RuntimeError(f"No Shop Apps section found: {page}")
    content,close,post=after.partition("</section>")
    if not close:raise RuntimeError("Missing closing Shop section")
    cards=re.findall(r'<article class="shop-product(?: sar-shop)?">.*?</article>',content,flags=re.S)
    if len(cards)!=2:raise RuntimeError(f"Shop expected 2 cards, got {len(cards)}: {page}")
    updated=[]
    for card,kind in zip(cards,("gentian","swiss")):
        expected=f'{kind}-cover.webp' if kind=="gentian" else 'swiss-alpine-cover.webp'
        img=re.search(r'<div class="shop-app-cover-frame"><img[^>]*></div>',card)
        if not img or expected not in img.group():raise RuntimeError(f"Missing original {kind} artwork: {page}")
        links=re.findall(r'<a class="(?:button [^"]+|shop-platform-link)"[^>]*>.*?</a>',card,flags=re.S)
        if len(links)!=2:raise RuntimeError(f"Expected 2 original links for {kind}, found {len(links)}")
        # No duplicate app names below the artwork; preserve the existing actions.
        art=img.group().replace('class="shop-app-cover-frame"','class="shop-app-cover-frame showcase-cover"')
        cardnew='<article class="shop-product showcase-product">'+head(page,tr,kind)+art+'<div class="showcase-actions">'+''.join(links)+'</div></article>'
        updated.append(cardnew)
    for old,new in zip(cards,updated):
        content=content.replace(old,new,1)
    doc=css_link(before+sep+content+close+post,page)
    sec=doc.split(sep,1)[1].split("</section>",1)[0]
    if sec.count('class="showcase-heading"')!=2 or "· Offline" in sec or "· Çevrimdışı" in sec:
        raise RuntimeError(f"Shop validation failed: {page}")
    page.write_text(doc,encoding="utf-8")

    page=root/(prefix+"apps/index.html")
    doc=page.read_text(encoding="utf-8")
    start=doc.index('<section class="app-list-grid">')
    before=doc[:start]
    inside,cut,rest=doc[start:].partition('</section>')
    if not cut:raise RuntimeError(f"No apps-list section end: {page}")
    cards=re.findall(r'<article class="app-list-card">.*?</article>',inside,flags=re.S)
    if len(cards)!=2:raise RuntimeError(f"Apps listing expected 2 cards, got {len(cards)}")
    updated=[]
    for card,kind in zip(cards,("gentian","swiss")):
        key="gentian-cover.webp" if kind=="gentian" else "swiss-alpine-cover.webp"
        anchor=re.search(r'<a class="app-list-poster"[^>]*>.*?</a>',card,flags=re.S)
        details=re.search(r'<div class="app-list-body">.*</div>(?=</article>$)',card,flags=re.S)
        if not anchor or key not in anchor.group() or not details:
            raise RuntimeError(f"Cannot parse original {kind} listing: {page}")
        preserved=details.group()
        # Title has moved to the branded header; only one app name remains visible.
        preserved,n=re.subn(r'<h2>.*?</h2>','',preserved,count=1)
        if n!=1:raise RuntimeError(f"Missing prior card heading: {page}")
        if 'class="button button-primary"' not in preserved:
            raise RuntimeError(f"App detail navigation button lost: {page}")
        preserved=preserved.replace(
          'offline navigation and mountain safety','mountain safety').replace(
          'çevrimdışı GPS ve dağ güvenliği','dağ güvenliği')
        art=anchor.group().replace('class="app-list-poster"','class="app-list-poster showcase-cover"')
        updated.append('<article class="app-list-card showcase-app-list-card">'+head(page,tr,kind)+art+preserved+'</article>')
    for old,new in zip(cards,updated):
        inside=inside.replace(old,new,1)
    doc=css_link(before+inside+cut+rest,page)
    sec=doc.split('<section class="app-list-grid">',1)[1].split('</section>',1)[0]
    if sec.count('class="showcase-heading"')!=2 or "çevrimdışı" in sec.lower() or "offline" in sec.lower():
        raise RuntimeError(f"Apps listing validation failed: {page}")
    page.write_text(doc,encoding="utf-8")

# The approved homepage layout is already correct; change only the short labels.
for path in ("index.html","tr/index.html"):
    page=root/path
    html=page.read_text(encoding="utf-8")
    html=html.replace("Swiss maps · Hiking · Cycling · MTB · Offline","Swiss maps · Hiking · Cycling · MTB")
    html=html.replace("İsviçre haritaları · Yürüyüş · MTB · Çevrimdışı","İsviçre haritaları · Yürüyüş · MTB")
    for s in ("· Offline","· Çevrimdışı"):
        if s in html.split('id="featured-apps"',1)[-1].split('</section>',1)[0]:
            raise RuntimeError(f"Homepage card still contains {s}")
    page.write_text(html,encoding="utf-8")

for p in ("shop/index.html","tr/shop/index.html","apps/index.html","tr/apps/index.html"):
    s=(root/p).read_text(encoding="utf-8")
    if s.count('class="showcase-heading"')!=2:
        raise RuntimeError(f"Missing branded headers in {p}")
print("PASS: EN/TR Shop and Apps cards use icons/title/subtitle above original artwork; no Offline/Çevrimdışı card labels.")
