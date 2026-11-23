#!/usr/bin/env python3
"""Keep both published AWOOO Kindle titles and Shop navigation in sync.

Executed after patch_kindle_links.py, which builds the bilingual Shop
and the original book's direct ASIN links. AWOOO CHRONICLES links use its
verified Amazon.com product ASIN B0HSP3CDBF, provided by the author.
"""
from pathlib import Path
import html
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
chronicles_asin = "B0HSP3CDBF"
stores = [
    ("🇺🇸", "United States", "Amerika Birleşik Devletleri", "amazon.com"),
    ("🇬🇧", "United Kingdom", "Birleşik Krallık", "amazon.co.uk"),
    ("🇩🇪", "Germany", "Almanya", "amazon.de"),
    ("🇫🇷", "France", "Fransa", "amazon.fr"),
    ("🇪🇸", "Spain", "İspanya", "amazon.es"),
    ("🇮🇹", "Italy", "İtalya", "amazon.it"),
    ("🇳🇱", "Netherlands", "Hollanda", "amazon.nl"),
    ("🇯🇵", "Japan", "Japonya", "amazon.co.jp"),
    ("🇧🇷", "Brazil", "Brezilya", "amazon.com.br"),
    ("🇨🇦", "Canada", "Kanada", "amazon.ca"),
    ("🇲🇽", "Mexico", "Meksika", "amazon.com.mx"),
    ("🇦🇺", "Australia", "Avustralya", "amazon.com.au"),
    ("🇮🇳", "India", "Hindistan", "amazon.in"),
]

def whole_div_end(doc, start):
    depth = 0
    for match in re.finditer(r"</?div\b[^>]*>", doc[start:], flags=re.I):
        if match.group().lower().startswith("</div"):
            depth -= 1
            if depth == 0:
                return start + match.end()
        else:
            depth += 1
    raise RuntimeError("Cannot find matching Kindle store-grid closing tag")

def chronicles_marketplaces(tr):
    cards = []
    for flag, en, tn, domain in stores:
        country = tn if tr else en
        url = "https://www." + domain + "/dp/" + chronicles_asin
        cards.append(
            '<a class="amazon-market-link" href="' + html.escape(url, quote=True) +
            '" target="_blank" rel="noopener noreferrer" aria-label="' +
            html.escape(country, quote=True) + ' Amazon Kindle">'
            '<span class="amazon-market-flag" aria-hidden="true">' + flag + '</span>'
            '<span class="amazon-market-copy"><strong>' + html.escape(country) +
            '</strong><small>Amazon ' + domain + '</small></span>'
            '<span class="amazon-market-arrow" aria-hidden="true">↗</span></a>'
        )
    intro = ("Kindle sürümünü görüntülemek veya satın almak için Amazon mağazanızı seçin." if tr else
             "Choose your Amazon marketplace to view or buy the Kindle edition.")
    note = ("Satın alma seçenekleri Amazon hesabınızın ülkesine ve mağazadaki satış durumuna göre değişebilir." if tr else
            "Purchase availability depends on your Amazon account country and each marketplace.")
    return (
        '<div class="store-grid kindle-only" id="amazon-stores">'
        '<div class="store-card kindle-card amazon-marketplaces">'
        '<h3>Amazon Kindle</h3><p class="market-intro">' + intro + '</p>'
        '<div class="amazon-market-grid">' + ''.join(cards) + '</div>'
        '<p class="amazon-market-note">' + note + '</p>'
        '</div></div>'
    )

for prefix, tr in (("", False), ("tr/", True)):
    path = root / (prefix + "books/awooo-chronicles/index.html")
    doc = path.read_text(encoding="utf-8")
    marker = '<div class="store-grid kindle-only">'
    if doc.count(marker) != 1:
        raise RuntimeError(f"Expected exactly one pending Chronicles store panel: {path}")
    start = doc.index(marker)
    end = whole_div_end(doc, start)
    doc = doc[:start] + chronicles_marketplaces(tr) + doc[end:]

    if tr:
        for old in ("Yayın sürecinde", "Yayımlanma sürecinde", "Yayınlanma sürecinde",
                    "Yayın aşamasında", "Yayımlanmayı bekliyor", "Yayına hazırlanıyor"):
            doc = doc.replace(old, "Amazon Kindle'da yayında")
    else:
        doc = doc.replace("Publication in progress", "Available on Amazon Kindle")
        doc = doc.replace("Awaiting publication", "Available on Amazon Kindle")

    css_href = ("../../../" if tr else "../../") + "assets/css/kindle-stores.css?v=20261123d"
    if "kindle-stores.css" not in doc:
        doc = doc.replace("</head>", '<link rel="stylesheet" href="' + css_href + '">\n</head>', 1)
    if doc.count('class="amazon-market-link"') != len(stores):
        raise RuntimeError(f"Chronicles marketplace link count incorrect: {path}")
    for _flag, _en, _tn, domain in stores:
        direct = "https://www." + domain + "/dp/" + chronicles_asin
        if doc.count('href="' + direct + '"') != 1:
            raise RuntimeError(f"Missing or duplicate direct Chronicles link {direct}: {path}")
    if '/s?k=' in doc or '/dp/B0HSMDXKWG' in doc:
        raise RuntimeError(f"Incorrect book or search URL on Chronicles page: {path}")
    if doc.count('id="amazon-stores"') != 1:
        raise RuntimeError(f"Missing unique Chronicles marketplace anchor: {path}")
    path.write_text(doc, encoding="utf-8")

for prefix, tr in (("", False), ("tr/", True)):
    page = root / (prefix + "shop/index.html")
    doc = page.read_text(encoding="utf-8")
    first, opening, after = doc.partition('<section class="shop-section" id="books">')
    if not opening:
        raise RuntimeError(f"Missing Shop Books section: {page}")
    books, closing, rest = after.partition("</section>")
    if not closing:
        raise RuntimeError(f"Unterminated Shop Books section: {page}")

    buy = "Satın Al ↗" if tr else "Buy ↗"
    preview = "Ön İzleme ↗" if tr else "Preview ↗"
    chronicles_buy = (
        '<div class="shop-book-actions">'
        '<a class="button button-primary" href="../books/awooo-chronicles/#amazon-stores">' +
        buy + '</a>'
        '<a class="button button-outline" href="../books/awooo-chronicles/" aria-label="' +
        ("Kitap bilgilerini ve örnek okuma seçeneğini görüntüle" if tr else
         "View book information and sample reading option") + '">' +
        preview + '</a></div>'
    )
    books, changed = re.subn(
        r'<a class="button button-primary" href="../books/awooo-chronicles/">[^<]*</a>',
        lambda _: chronicles_buy, books, count=1,
    )
    if changed != 1:
        raise RuntimeError(f"Chronicles Details button not found: {page}")

    husky_preview = (
        '<a class="button button-outline" href="../books/awooo-the-tale-of-a-husky/" '
        'aria-label="' + ("Kitap bilgilerini ve örnek okuma seçeneğini görüntüle" if tr
                          else "View book information and sample reading option") + '">' +
        preview + '</a>'
    )
    books, changed = re.subn(
        r'<a class="button button-outline" href="[^"]*awooo-the-tale-of-a-husky-preview\.pdf"[^>]*>[^<]*</a>',
        lambda _: husky_preview, books, count=1,
    )
    if changed != 1:
        raise RuntimeError(f"Husky direct PDF Preview button not found: {page}")

    published_note = (
        "Her iki AWOOO kitabı da Amazon Kindle'da yayımlandı." if tr
        else "Both AWOOO books are published on Amazon Kindle."
    )
    books, changed = re.subn(
        r'<div class="shop-platform-note">.*?</div>',
        lambda _: '<div class="shop-platform-note">' + published_note + '</div>',
        books, count=1, flags=re.S,
    )
    if changed != 1:
        raise RuntimeError(f"Shop publication note missing: {page}")

    if (books.count('class="shop-book-actions"') != 2 or
            books.count('href="../books/awooo-chronicles/#amazon-stores"') != 1 or
            books.count('href="../books/awooo-the-tale-of-a-husky/#amazon-stores"') != 1 or
            books.count('href="../books/awooo-chronicles/"') != 1 or
            books.count('href="../books/awooo-the-tale-of-a-husky/"') != 1 or
            "preview.pdf" in books):
        raise RuntimeError(f"Book navigation validation failed: {page}")

    page.write_text(first + opening + books + closing + rest, encoding="utf-8")

# The previous marketplace stylesheet mixed a white surface with light text
# under the dark theme, making country names illegible on mobile Safari.
css_path = root / "assets/css/kindle-stores.css"
css = css_path.read_text(encoding="utf-8")
css += """
/* Stable foreground contrast for both light and dark theme Amazon rows. */
.amazon-market-link{background:#f8fafb!important;color:#172c3b!important}
.amazon-market-link .amazon-market-copy strong{color:#172c3b!important}
.amazon-market-link .amazon-market-copy small{color:#526879!important}
.amazon-market-link .amazon-market-arrow{color:#172c3b!important;opacity:1}
.amazon-market-link:focus-visible{outline:3px solid #1c8869;outline-offset:2px}
"""
css_path.write_text(css, encoding="utf-8")
print("PASS: both Kindle books published, 13 Chronicles direct ASIN links, Shop Buy and landing-page Preview in EN/TR.")
