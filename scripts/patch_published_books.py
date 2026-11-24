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


# AWOOO: The Tale of a Husky — Kindle + paperback (author-supplied US ASIN).
# Keep existing Kindle marketplace links: print availability varies by country.
paperback_url = "https://www.amazon.com/dp/B0HSSS6M5P"
kindle_url = "https://www.amazon.com/dp/B0HSMDXKWG"

for prefix, tr in (("", False), ("tr/", True)):
    format_label = "Kindle e-kitap · Basılı kitap (Paperback)" if tr else "Kindle eBook · Paperback"
    page = root / (prefix + "books/awooo-the-tale-of-a-husky/index.html")
    doc = page.read_text(encoding="utf-8")
    start = doc.index('<div class="store-grid kindle-only" id="amazon-stores">')
    end = whole_div_end(doc, start)
    panel = doc[start:end]
    assert panel.count('class="amazon-market-link"') == len(stores)
    intro = ("Amazon.com üzerinden Kindle e-kitap veya basılı kitap (paperback) seçeneğini görüntüleyin."
             if tr else "View the Kindle eBook and paperback editions on Amazon.com.")
    availability = ("Basılı kitabın stok ve teslimat durumu ülkeye ve teslimat adresine göre değişebilir."
                    if tr else "Paperback availability and delivery may vary by country and shipping address.")
    local = "Ülkenize göre Kindle mağazaları" if tr else "Kindle marketplaces by country"
    print_label = "Paperback · Basılı kitap" if tr else "Paperback · Print edition"
    choose_label = "Amazon'da görüntüle ↗" if tr else "View on Amazon ↗"
    kindle_label = "Kindle · E-kitap" if tr else "Kindle · eBook"
    formats = (
        '<h3>' + ("Amazon kitap sürümleri" if tr else "Amazon book editions") + '</h3>'
        '<p class="market-intro">' + intro + '</p>'
        '<div class="book-edition-grid">'
        '<a class="button button-primary" href="' + paperback_url + '" target="_blank" rel="noopener noreferrer">'
        '<strong>' + print_label + '</strong><small>' + choose_label + '</small></a>'
        '<a class="button button-outline" href="' + kindle_url + '" target="_blank" rel="noopener noreferrer">'
        '<strong>' + kindle_label + '</strong><small>' + choose_label + '</small></a>'
        '</div><p class="amazon-market-note edition-note">' + availability + '</p>'
        '<h4 class="edition-market-heading">' + local + '</h4>'
    )
    panel, n = re.subn(r'<h3>Amazon Kindle</h3><p class="market-intro">.*?</p>',
                       lambda _: formats, panel, count=1, flags=re.S)
    assert n == 1, page
    doc = doc[:start] + panel + doc[end:]
    # Change the existing publication status and other title-specific Kindle-only text.
    if tr:
        doc = doc.replace("Amazon Kindle’da yayında", "Kindle e-kitap ve paperback")
        doc = doc.replace("Amazon Kindle'da yayında", "Kindle e-kitap ve paperback")
    else:
        doc = doc.replace("Available on Amazon Kindle", "Kindle eBook &amp; Paperback")
        doc = doc.replace("Choose an Amazon marketplace to view the Kindle edition.",
                          "Choose Kindle eBook or paperback on Amazon.")
    doc = doc.replace("kindle-stores.css?v=20261123", "kindle-stores.css?v=20261124-print")
    assert doc.count('href="' + paperback_url + '"') == 1, page
    assert doc.count('class="amazon-market-link"') == len(stores), page
    page.write_text(doc, encoding="utf-8")

    page = root / (prefix + "shop/index.html")
    doc = page.read_text(encoding="utf-8")
    old = "<h3>AWOOO: The Tale of a Husky</h3><p>The Tale of a Husky</p>"
    # Allow intervening whitespace from the earlier layout patch.
    doc, n = re.subn(r'<h3>AWOOO: The Tale of a Husky</h3>\s*<p>The Tale of a Husky</p>',
                     lambda _: '<h3>AWOOO: The Tale of a Husky</h3><p>' + format_label + '</p>',
                     doc, count=1)
    assert n == 1, page
    old_note = ("Her iki AWOOO kitabı da Amazon Kindle'da yayımlandı." if tr
                else "Both AWOOO books are published on Amazon Kindle.")
    new_note = ("AWOOO: The Tale of a Husky — Kindle e-kitap ve paperback. AWOOO CHRONICLES — Kindle e-kitap."
                if tr else "AWOOO: The Tale of a Husky — Kindle eBook and paperback. AWOOO CHRONICLES — Kindle eBook.")
    assert old_note in doc, page
    doc = doc.replace(old_note, new_note, 1).replace(
        '<span class="section-kicker">AMAZON KINDLE</span>',
        '<span class="section-kicker">AMAZON</span>', 1)
    page.write_text(doc, encoding="utf-8")

    page = root / (prefix + "index.html")
    doc = page.read_text(encoding="utf-8")
    old = '<strong>AWOOO: The Tale of a Husky</strong><small>The Tale of a Husky</small>'
    assert old in doc, page
    doc = doc.replace(old, '<strong>AWOOO: The Tale of a Husky</strong><small>' + format_label + '</small>', 1)
    page.write_text(doc, encoding="utf-8")

    page = root / (prefix + "books/index.html")
    doc = page.read_text(encoding="utf-8")
    # The book listing is inherited from site.zip. Add a title-specific
    # format annotation after its title, or near its store panel if needed.
    pattern = r'(<(?:h[1-6]|strong)\b[^>]*>\s*(?:AWOOO:\s*)?The Tale of a Husky\s*</(?:h[1-6]|strong)>)'
    doc, n = re.subn(pattern, lambda m: m.group(1) + '<p class="book-format-label">' + format_label + '</p>',
                     doc, count=1, flags=re.I)
    if not n:
        marker = '<div class="store-grid kindle-only">'
        assert marker in doc, page
        doc = doc.replace(marker, '<p class="book-format-label">AWOOO: The Tale of a Husky — ' + format_label + '</p>' + marker, 1)
    page.write_text(doc, encoding="utf-8")

css_path = root / "assets/css/kindle-stores.css"
css = css_path.read_text(encoding="utf-8")
css += """
/* Two direct edition links; independent of the country-specific Kindle grid. */
.book-edition-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.book-edition-grid .button{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:5px;min-height:70px;box-sizing:border-box;white-space:normal;text-align:left;padding:14px}
.book-edition-grid .button strong{font-size:15px;line-height:1.3}
.book-edition-grid .button small{font-size:12px;line-height:1.4}
.edition-note{margin:12px 0 24px}
.edition-market-heading{font-size:16px;margin:0 0 12px}
@media(max-width:520px){.book-edition-grid{grid-template-columns:1fr}}
"""
css_path.write_text(css, encoding="utf-8")
print("PASS: bilingual AWOOO Husky Kindle + paperback links, home, Books and Shop labels; Chronicles links unchanged.")
