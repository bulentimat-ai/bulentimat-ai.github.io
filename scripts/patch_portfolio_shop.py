#!/usr/bin/env python3
"""Apply approved Books + Apps storefront design to extracted bilingual site.

Only home-page feature panels, the requested Shop link, and two new Shop pages
are changed. Existing original product art, book previews and contact are kept.
"""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
styles = Path("assets/css/portfolio-v2.css").read_text(encoding="utf-8")
style_dest = root / "assets/css/portfolio-v2.css"
style_dest.parent.mkdir(parents=True, exist_ok=True)
style_dest.write_text(styles, encoding="utf-8")

app_store_svg = '''<svg viewBox="0 0 48 48" fill="none" aria-hidden="true" focusable="false"><path d="M18 9 33.7 37M30 9 14.3 37M10.5 29h27" stroke="white" stroke-width="5" stroke-linecap="round"/><path d="M21 9.5 16 18" stroke="white" stroke-width="4" stroke-linecap="round"/></svg>'''

def ribbon(kind, tr):
    if kind == "books":
        logo = '<span class="store-ribbon-logo amazon-wordmark" aria-hidden="true">amazon</span>'
        text = "Amazon Kindle"
        hint = "Amazon Kindle'da keşfet" if tr else "Available on"
        label = "Kitapları Amazon Kindle bölümünde görüntüle" if tr else "Explore the books on Amazon Kindle"
    else:
        logo = '<span class="store-ribbon-logo appstore-icon">' + app_store_svg + '</span>'
        text = "App Store"
        hint = "App Store'dan indir" if tr else "Download on the"
        label = "Uygulamaları App Store bölümünde görüntüle" if tr else "Browse the apps on the App Store"
    return f'''<a class="store-ribbon {kind}-ribbon" href="shop/#{kind}" aria-label="{label}">
       {logo}<span class="ribbon-divider" aria-hidden="true"></span>
       <span class="ribbon-copy"><small>{hint}</small><strong>{text}</strong></span>
       <span class="ribbon-arrow" aria-hidden="true">↗</span></a>'''

def feature_html(tr):
    img = "../assets/images/" if tr else "assets/images/"
    books = "Kitaplar" if tr else "Books"
    books_desc = ("Alplerden, dostluktan ve gerçek yolculuklardan ilham alan romanlar."
                  if tr else "Novels inspired by real journeys, friendship and the Alps.")
    apps = "Uygulamalar" if tr else "Apps"
    apps_desc = ("İsviçre'nin doğasını keşfetmek için outdoor uygulamaları."
                 if tr else "Outdoor apps for exploring Switzerland’s nature.")
    app_discover = "Uygulamayı incele ↗" if tr else "Discover the app ↗"
    gen_desc = "100 destinasyon · Arabasız gezi planlama" if tr else "Top 100 · Car-free trip planning"
    rot_desc = "Yürüyüş · MTB · Haritalar · SOS" if tr else "Hiking · MTB · Maps · SOS"
    return f'''<div class="feature-grid portfolio-shop-grid" aria-label="{'Öne çıkan çalışmalar' if tr else 'Featured books and apps'}">
  <section class="feature-panel books-feature" id="featured-books">
    <div class="panel-heading"><div>
      <h2><span class="heading-symbol" aria-hidden="true">▤</span> {books}</h2>
      <p class="panel-subtitle">{books_desc}</p>
    </div><a class="round-arrow" href="books/" aria-label="{'Tüm kitaplar' if tr else 'View all books'}">↗</a></div>
    <div class="home-books">
      <a class="home-book" href="books/awooo-chronicles/">
        <span class="book-cover-frame"><img src="{img}chronicles-front.webp" alt="AWOOO CHRONICLES — {'ön kapak' if tr else 'front cover'}" loading="lazy" width="380" height="608"></span>
        <strong>AWOOO CHRONICLES</strong><small>A NOVEL</small>
      </a>
      <a class="home-book" href="books/awooo-the-tale-of-a-husky/">
        <span class="book-cover-frame"><img src="{img}husky-front.webp" alt="AWOOO: The Tale of a Husky — {'ön kapak' if tr else 'front cover'}" loading="lazy" width="380" height="608"></span>
        <strong>AWOOO: The Tale of a Husky</strong><small>The Tale of a Husky</small>
      </a>
    </div>
    {ribbon("books", tr)}
  </section>
  <section class="feature-panel apps-feature" id="featured-apps">
    <div class="panel-heading"><div>
      <h2><span class="heading-symbol" aria-hidden="true">▯</span> {apps}</h2>
      <p class="panel-subtitle">{apps_desc}</p>
    </div><a class="round-arrow" href="apps/" aria-label="{'Tüm uygulamalar' if tr else 'View all apps'}">↗</a></div>
    <div class="home-apps">
      <a class="home-app" href="apps/gentian/">
        <div class="home-app-title"><span class="app-symbol gentian" role="img" aria-label="Gentian {'gerçek uygulama simgesi' if tr else 'original app icon'}"></span><div><strong>Gentian – Swiss Alps</strong><span>{gen_desc}</span></div></div>
        <div class="app-image-pair"><img src="{img}gentian-1.webp" alt="Gentian — {'keşif ekranı' if tr else 'Discover screen'}" loading="lazy"><img src="{img}gentian-2.webp" alt="Gentian — {'destinasyon ayrıntıları' if tr else 'destination details'}" loading="lazy"></div>
        <span class="card-text-link">{app_discover}</span>
      </a>
      <a class="home-app" href="apps/isvicre-rotam/">
        <div class="home-app-title"><span class="app-symbol rotam" role="img" aria-label="İsviçre Rotam {'gerçek uygulama simgesi' if tr else 'original app icon'}"></span><div><strong>İsviçre Rotam</strong><span>{rot_desc}</span></div></div>
        <div class="app-image-pair"><img src="{img}rotam-1.webp" alt="İsviçre Rotam — {'harita ekranı' if tr else 'map screen'}" loading="lazy"><img src="{img}rotam-2.webp" alt="İsviçre Rotam — {'rota listesi' if tr else 'route list'}" loading="lazy"></div>
        <span class="card-text-link">{app_discover}</span>
      </a>
    </div>
    {ribbon("apps", tr)}
  </section>
</div>'''

def shop_main(tr):
    imagebase = "../../assets/images/" if tr else "../assets/images/"
    shop_k = "KİTAPLAR VE UYGULAMALAR" if tr else "BOOKS & APPS"
    shop_title = "Alışveriş" if tr else "Shop"
    shop_sub = ("Kitapları ve uygulamaları keşfedin. Yayımlanmış ürünlerin mağaza bağlantıları ve ürün sayfaları burada."
                if tr else "Discover the books and apps, with official store links and product pages when available.")
    books_intro = ("Kitap kapaklarına tıklayarak açıklamaları ve ücretsiz örnek sayfaları inceleyebilirsiniz."
                   if tr else "Open each book to read details and its permitted sample preview.")
    apps_intro = ("Uygulamaların resmî sayfalarını ve doğrulanmış indirme bağlantılarını görüntüleyin."
                  if tr else "Official product pages and verified download links for the apps.")
    details = "Kitabı incele ↗" if tr else "View book & preview ↗"
    app_details = "Uygulamayı incele ↗" if tr else "Explore the app ↗"
    gen_button = "App Store'da görüntüle ↗" if tr else "View on App Store ↗"
    note = ("Amazon Kindle satın alma bağlantıları doğrulanana kadar ilgili kitapların örnek sayfalarına yönlendiriyoruz; doğrudan satın alma bağlantısı uydurmuyoruz."
            if tr else "Until the individual Kindle purchase URLs are verified, we link to the books' preview pages rather than invent a purchase link.")
    rot_note = ("İsviçre Rotam için doğrulanmış App Store bağlantısı henüz eklenmedi."
                if tr else "A verified App Store listing URL for İsviçre Rotam has not yet been provided.")
    return f'''<section class="subhero"><span class="section-kicker">{shop_k}</span><h1>{shop_title}</h1><p class="shop-hero-sub">{shop_sub}</p></section>
<div class="shop-content">
  <section class="shop-section" id="books">
    <span class="section-kicker">AMAZON KINDLE</span><h2>{'Kitaplar' if tr else 'Books'}</h2><p>{books_intro}</p>
    <div class="shop-product-grid">
      <article class="shop-product"><img src="{imagebase}chronicles-front.webp" alt="AWOOO CHRONICLES — cover" loading="lazy"><h3>AWOOO CHRONICLES</h3><p>A NOVEL</p><a class="button button-primary" href="../books/awooo-chronicles/">{details}</a></article>
      <article class="shop-product"><img src="{imagebase}husky-front.webp" alt="AWOOO: The Tale of a Husky — cover" loading="lazy"><h3>AWOOO: The Tale of a Husky</h3><p>The Tale of a Husky</p><a class="button button-primary" href="../books/awooo-the-tale-of-a-husky/">{details}</a></article>
    </div>
    <div class="shop-platform-note">{note}</div>
  </section>
  <section class="shop-section" id="apps">
    <span class="section-kicker">APPLE APP STORE</span><h2>{'Uygulamalar' if tr else 'Apps'}</h2><p>{apps_intro}</p>
    <div class="shop-product-grid">
      <article class="shop-product"><img src="{imagebase}gentian-banner.webp" alt="Official Gentian promotional artwork" loading="lazy"><h3>Gentian – Swiss Alps</h3><p>Top 100 · Car-free trip planning</p><a class="button button-primary" href="https://apps.apple.com/app/id6836983660" target="_blank" rel="noopener noreferrer">{gen_button}</a><a class="shop-platform-link" href="../apps/gentian/">{app_details}</a></article>
      <article class="shop-product"><img src="{imagebase}rotam-banner.webp" alt="Official İsviçre Rotam promotional artwork" loading="lazy"><h3>İsviçre Rotam</h3><p>Hiking · MTB · Maps · SOS</p><a class="button button-outline" href="../apps/isvicre-rotam/">{app_details}</a><span class="shop-platform-note">{rot_note}</span></article>
    </div>
  </section>
</div>'''

def inject_nav(doc, tr, rel):
    label = "Kitaplar" if tr else "Books"
    shop_label = "Alışveriş" if tr else "Shop"
    root_prefix = "../" * (len(rel.parts) - 1)
    shop_href = root_prefix + ("tr/shop/" if tr else "shop/")
    def update(nav):
        section = nav.group(0)
        if re.search(r'>' + shop_label + r'</a>', section):
            return section
        m = re.search(r'<a href="[^"]+"[^>]*>' + re.escape(label) + r'</a>', section)
        if not m:
            raise SystemExit(f"Cannot find Book link in navigation: {rel}")
        shop = f'<a href="{shop_href}">{shop_label}</a>'
        return section[:m.end()] + shop + section[m.end():]
    doc, a = re.subn(r'<nav class="main-nav"[^>]*>.*?</nav>', update, doc, count=1, flags=re.S)
    doc, b = re.subn(r'<nav aria-label="(?:Footer navigation|Alt menü)">.*?</nav>', update, doc, count=1, flags=re.S)
    if a != 1 or b != 1:
        raise SystemExit(f"Navigation injection mismatch: {rel}")
    if rel in (Path("shop/index.html"), Path("tr/shop/index.html")):
        doc = doc.replace(f'<a href="{shop_href}">{shop_label}</a>',
                          f'<a href="{shop_href}" aria-current="page">{shop_label}</a>', 1)
    return doc

def add_css_link(doc, href):
    if "portfolio-v2.css" not in doc:
        doc = doc.replace("</head>", f'<link rel="stylesheet" href="{href}">\n</head>', 1)
    return doc

# Generate new Shop pages from the existing app-index template (same directory depth).
for tr in (False, True):
    source = root / ("tr/apps/index.html" if tr else "apps/index.html")
    target = root / ("tr/shop/index.html" if tr else "shop/index.html")
    page = source.read_text(encoding="utf-8")
    page, n = re.subn(r'<main id="main" class="container-wide">.*?</main>',
                       lambda _: '<main id="main" class="container-wide">' + shop_main(tr) + '</main>',
                       page, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"Cannot build Shop page: {source}")
    if tr:
        page = page.replace('Uygulamalar, Kitaplar ve Görsel Hikâyeler', 'Alışveriş · Kitaplar ve Uygulamalar')
        page = page.replace('<title>Uygulamalar ', '<title>Alışveriş ')
        page = page.replace('<a href="./" aria-current="page">Uygulamalar</a>', '<a href="../apps/">Uygulamalar</a>')
        page = page.replace('<a href="./">Uygulamalar</a>', '<a href="../apps/">Uygulamalar</a>')
        page = page.replace('href="../../apps/" lang="en"', 'href="../../shop/" lang="en"')
        page = page.replace('hreflang="en" href="../../apps/"', 'hreflang="en" href="../../shop/"')
        page = page.replace('href="../tr/apps/"', 'href="../tr/shop/"')
        page = page.replace('hreflang="tr" href="./"', 'hreflang="tr" href="./"')
        page = page.replace('content="Keşif, yolculuk planlama ve açık hava deneyimleri için bağımsız geliştirilen mobil uygulamalar."', 'content="Bülent İmat kitapları, Amazon Kindle ve App Store uygulamaları."')
        css_href = "../../assets/css/portfolio-v2.css"
    else:
        page = page.replace('<title>Apps ', '<title>Shop ')
        page = page.replace('<a href="./" aria-current="page">Apps</a>', '<a href="../apps/">Apps</a>')
        page = page.replace('<a href="./">Apps</a>', '<a href="../apps/">Apps</a>')
        page = page.replace('href="../tr/apps/"', 'href="../tr/shop/"')
        page = page.replace('content="Independent mobile experiences made for discovery, smarter travel and the outdoors."', 'content="Bülent İmat books, Amazon Kindle and App Store apps."')
        css_href = "../assets/css/portfolio-v2.css"
    page = add_css_link(page, css_href)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")

for file in sorted(root.rglob("index.html")):
    rel = file.relative_to(root)
    tr = str(rel).startswith("tr/")
    page = file.read_text(encoding="utf-8")
    if str(rel) in ("index.html", "tr/index.html"):
        path = "../assets/css/portfolio-v2.css" if tr else "assets/css/portfolio-v2.css"
        page = add_css_link(page, path)
        page, n = re.subn(r'<div class="feature-grid"[^>]*>.*?(?=\s*<section class="story-feature">)',
                          lambda _: feature_html(tr) + "\n  ",
                          page, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"Could not find old feature grid in {rel}")
        if tr:
            page = page.replace('href="about/">Hakkımda <span aria-hidden="true">→</span>',
                                'href="shop/">Alışveriş <span aria-hidden="true">↗</span>')
        else:
            page = page.replace('href="about/">About me <span aria-hidden="true">→</span>',
                                'href="shop/">Shop <span aria-hidden="true">↗</span>')
        for must in ('chronicles-front.webp','husky-front.webp','gentian-1.webp',
                     'gentian-2.webp','rotam-1.webp','rotam-2.webp',
                     'store-ribbon books-ribbon','store-ribbon apps-ribbon',
                     'app-symbol gentian','app-symbol rotam','href="shop/"'):
            if must not in page:
                raise SystemExit(f"Missing homepage element {must}: {rel}")
    page = inject_nav(page, tr, rel)
    file.write_text(page, encoding="utf-8")

# Semantic, link and archive-safety checks.
for rel in ('index.html', 'tr/index.html'):
    html = (root / rel).read_text(encoding="utf-8")
    if html.index('books-feature') >= html.index('apps-feature') or html.index('apps-feature') >= html.index('story-feature'):
        raise SystemExit(f"Wrong feature order: {rel}")
    if (html.count('class="store-ribbon books-ribbon"') != 1 or
        html.count('class="store-ribbon apps-ribbon"') != 1 or
        html.count('class="app-symbol') != 2):
        raise SystemExit(f"Store ribbons or brand icon count failed: {rel}")
for rel in ("shop/index.html", "tr/shop/index.html"):
    text = (root / rel).read_text(encoding="utf-8")
    for item in ("AWOOO CHRONICLES", "AWOOO: The Tale of a Husky", "Gentian – Swiss Alps", "İsviçre Rotam"):
        if item not in text:
            raise SystemExit(f"Shop product missing in {rel}: {item}")
print("Validated bilingual homepage, Shop pages, store destinations and authentic brand artwork.")


# Homepage hero: four distinct routes, with the projects CTA leading to the
# existing combined showcase instead of duplicating the Apps destination.
for tr in (False, True):
    rel = "tr/index.html" if tr else "index.html"
    page = root / rel
    doc = page.read_text(encoding="utf-8")
    items = (
        ("#featured-projects", "Projeleri keşfet" if tr else "Explore projects", "button-primary", "↓"),
        ("apps/", "Uygulamaları keşfet" if tr else "Explore apps", "button-ghost", "↗"),
        ("books/", "Kitapları keşfet" if tr else "Explore books", "button-ghost", "↗"),
        ("shop/", "Satın al" if tr else "Buy", "button-primary", "↗"),
    )
    actions = '<div class="hero-cta home-hero-navigation">' + ''.join(
        f'<a class="button {style}" href="{href}">{label} <span aria-hidden="true">{arrow}</span></a>'
        for href, label, style, arrow in items
    ) + '</div>'
    doc, n = re.subn(r'<div class="hero-cta">.*?</div>', lambda _: actions, doc, count=1, flags=re.S)
    assert n == 1, rel
    marker = '<div class="feature-grid portfolio-shop-grid"'
    assert doc.count(marker) == 1, rel
    doc = doc.replace(marker, marker + ' id="featured-projects"', 1)
    doc, n = re.subn(r'(assets/css/portfolio-v2\.css)(?:\?[^"]*)?"', r'\1?v=20261126-home-nav"', doc, count=1)
    assert n == 1, rel
    assert actions.count('<a ') == 4 and doc.count('id="featured-projects"') == 1, rel
    for href, label, _, _ in items:
        assert f'href="{href}">{label} ' in actions, (rel, href)
        if not href.startswith("#"):
            assert (page.parent / href / "index.html").is_file(), (rel, href)
    page.write_text(doc, encoding="utf-8")

home_css = root / "assets/css/portfolio-v2.css"
home_css.write_text(home_css.read_text(encoding="utf-8") + """
/* Four homepage-only hero destinations, maintaining the existing theme. */
#featured-projects{scroll-margin-top:100px}
.home-hero .home-hero-navigation{display:flex;flex-wrap:wrap;gap:10px;align-items:stretch}
.home-hero .home-hero-navigation .button{white-space:normal;min-height:44px;box-sizing:border-box}
@media(max-width:760px){
  .home-hero .home-hero-navigation{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;width:100%;max-width:470px}
  .home-hero .home-hero-navigation .button{justify-content:center;text-align:center;font-size:12px;padding:10px 8px;gap:5px;line-height:1.25}
}
@media(max-width:340px){
  .home-hero .home-hero-navigation .button{font-size:11px;padding:9px 6px}
}
""", encoding="utf-8")
print("PASS: bilingual homepage hero has four distinct validated destinations.")
