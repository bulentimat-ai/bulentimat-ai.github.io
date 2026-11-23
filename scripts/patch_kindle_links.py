#!/usr/bin/env python3
"""Add real Amazon Kindle marketplace links and revise Books Shop CTAs.

Patch only the published AWOOO: The Tale of a Husky page, and the Shop
books section, in both languages. Do not alter preview PDF files.
"""
from pathlib import Path
import html
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
asin = "B0HSMDXKWG"
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

css = """
/* Published AWOOO Kindle marketplaces; compatible with existing light/dark theme. */
.store-grid.kindle-only:has(.amazon-marketplaces){display:block;max-width:900px}
.amazon-marketplaces{max-width:900px;width:100%;box-sizing:border-box}
#amazon-stores{scroll-margin-top:110px}
.amazon-marketplaces h3{margin:0 0 10px;font-size:clamp(20px,2.3vw,27px)}
.amazon-marketplaces .market-intro{margin:0 0 22px;color:var(--muted);line-height:1.6}
.amazon-market-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:11px}
.amazon-market-link{display:flex;align-items:center;gap:10px;min-width:0;
 border:1px solid var(--line,#d5dbe0);border-radius:12px;padding:12px;
 text-decoration:none;color:var(--ink);background:var(--card,#fff);
 transition:border-color .18s,transform .18s,box-shadow .18s}
.amazon-market-link:hover,.amazon-market-link:focus-visible{border-color:#e99935;
 transform:translateY(-1px);box-shadow:0 4px 14px rgba(0,0,0,.09)}
.amazon-market-flag{font-size:22px;line-height:1;flex:none}
.amazon-market-copy{min-width:0;display:flex;flex-direction:column;gap:2px;flex:1}
.amazon-market-copy strong{font-size:14px;font-weight:700;line-height:1.25}
.amazon-market-copy small{font-size:12px;color:var(--muted)}
.amazon-market-arrow{font-size:15px;opacity:.7;flex:none}
.amazon-market-note{font-size:12px;color:var(--muted);margin:20px 0 0;line-height:1.5}
@media(max-width:750px){.amazon-market-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:440px){.amazon-market-grid{grid-template-columns:1fr}.amazon-market-link{padding:13px}}
"""
css_dest=root/"assets/css/kindle-stores.css"
css_dest.parent.mkdir(parents=True,exist_ok=True)
css_dest.write_text(css,encoding="utf-8")

def complete_div(text, begin):
    """Return the end offset of a balanced div (rather than a fragile .* regex)."""
    match = re.match(r'<div\b[^>]*>', text[begin:])
    if not match:
        raise RuntimeError("Expected div opening")
    level = 0
    for token in re.finditer(r'</?div\b[^>]*>', text[begin:], flags=re.I):
        if token.group().lower().startswith("</div"):
            level -= 1
            if level == 0:
                return begin + token.end()
        else:
            level += 1
    raise RuntimeError("Unbalanced book store-grid div")

def marketplace_widget(tr):
    cards=[]
    for flag,en,tn,domain in stores:
        country=tn if tr else en
        cards.append(
            '<a class="amazon-market-link" href="https://www.'+domain+'/dp/'+asin+
            '" target="_blank" rel="noopener noreferrer"'
            ' aria-label="'+html.escape(country)+' Amazon Kindle">'
            '<span class="amazon-market-flag" aria-hidden="true">'+flag+'</span>'
            '<span class="amazon-market-copy"><strong>'+html.escape(country)+
            '</strong><small>Amazon '+domain+'</small></span>'
            '<span class="amazon-market-arrow" aria-hidden="true">↗</span></a>'
        )
    intro=("Kitabı incelemek veya satın almak için Amazon mağazanızı seçin."
           if tr else "Choose your Amazon marketplace to view or buy the Kindle edition.")
    note=("Satın alma seçenekleri Amazon hesabınızın ülkesine ve mağazadaki satış durumuna göre değişebilir."
          if tr else "Purchase availability depends on your Amazon account country and each marketplace.")
    return (
        '<div class="store-grid kindle-only" id="amazon-stores">'
        '<div class="store-card kindle-card amazon-marketplaces">'
        '<h3>Amazon Kindle</h3><p class="market-intro">'+intro+'</p>'
        '<div class="amazon-market-grid">'+''.join(cards)+'</div>'
        '<p class="amazon-market-note">'+note+'</p>'
        '</div></div>'
    )

# Published title: swap the old coming-soon card for exact country-specific URLs.
for prefix,tr in (("",False),("tr/",True)):
    page=root/(prefix+"books/awooo-the-tale-of-a-husky/index.html")
    doc=page.read_text(encoding="utf-8")
    marker='<div class="store-grid kindle-only">'
    if doc.count(marker)!=1:
        raise RuntimeError(f"Expected one Kindle store block, got {doc.count(marker)}: {page}")
    begin=doc.index(marker)
    end=complete_div(doc,begin)
    doc=doc[:begin]+marketplace_widget(tr)+doc[end:]
    if not tr:
        doc=doc.replace("By Bülent İmat · Publication in progress",
                        "By Bülent İmat · Available on Amazon Kindle")
        doc=doc.replace("Store links will be activated when the book is available in the relevant store.",
                        "Choose an Amazon marketplace to view the Kindle edition.")
    relative="../../../" if tr else "../../"
    css_href=relative+"assets/css/kindle-stores.css?v=20261123"
    if "kindle-stores.css" not in doc:
        doc=doc.replace("</head>",'<link rel="stylesheet" href="'+css_href+'">\n</head>',1)
    if doc.count("/dp/"+asin)!=len(stores):
        raise RuntimeError(f"Wrong number of marketplace URLs: {page}")
    if "Store link coming soon" in doc:
        raise RuntimeError(f"Obsolete coming-soon text: {page}")
    page.write_text(doc,encoding="utf-8")

# Shop's already-generated two cards: provide Buy + Preview for the live book.
# AWOOO CHRONICLES remains under review, so do not claim it is on sale.
for prefix,tr in (("",False),("tr/",True)):
    page=root/(prefix+"shop/index.html")
    doc=page.read_text(encoding="utf-8")
    first,sep,after=doc.partition('<section class="shop-section" id="books">')
    if not sep:
        raise RuntimeError(f"Missing Books section: {page}")
    books,close,rest=after.partition("</section>")
    if not close:
        raise RuntimeError(f"Unterminated Books section: {page}")
    def relabel(slug, label, buy=False):
        global books
        pattern=(r'<a class="button button-primary" href="../books/'+
                 re.escape(slug)+r'/">.*?</a>')
        url="../books/"+slug+"/"+("#amazon-stores" if buy else "")
        replacement='<a class="button button-primary" href="'+url+'">'+label+'</a>'
        books,n=re.subn(pattern,lambda _:replacement,books,count=1,flags=re.S)
        if n!=1:
            raise RuntimeError(f"Book CTA not found for {slug}: {page}")
    # A pending title must not present a functioning Buy option.
    relabel("awooo-chronicles", "Kitap Ayrıntıları ↗" if tr else "Details ↗")
    # Main green button jumps directly to all 13 Amazon links.
    relabel("awooo-the-tale-of-a-husky", "Satın Al ↗" if tr else "Buy ↗", buy=True)

    # Keep the Buy CTA, and place a separate sample PDF Preview beside it.
    # The exact publicly released, limited preview already exists in site.zip.
    buy_label = "Satın Al ↗" if tr else "Buy ↗"
    preview_label = "Ön İzleme ↗" if tr else "Preview ↗"
    pdf_href = "../assets/previews/awooo-the-tale-of-a-husky-preview.pdf"
    buy_anchor = (
        '<a class="button button-primary" '
        'href="../books/awooo-the-tale-of-a-husky/#amazon-stores">'
        + buy_label + '</a>'
    )
    preview_anchor = (
        '<a class="button button-outline" href="' + pdf_href +
        '" target="_blank" rel="noopener noreferrer"'
        ' aria-label="' + ("Kitabın ücretsiz örneğini aç" if tr else "Open free book sample") + '">'
        + preview_label + '</a>'
    )
    if books.count(buy_anchor) != 1:
        raise RuntimeError(f"Missing expected Buy action: {page}")
    books = books.replace(
        buy_anchor,
        '<div class="shop-book-actions">' + buy_anchor + preview_anchor + '</div>',
        1
    )
    books=books.replace(
        "Open each book to read details and its permitted sample preview.",
        "Explore the books and choose an Amazon marketplace for published titles."
    ).replace(
        "Kitap kapaklarına tıklayarak açıklamaları ve ücretsiz örnek sayfaları inceleyebilirsiniz.",
        "Kitapları keşfedin ve yayımlanan kitaplar için Amazon mağazanızı seçin."
    )
    books,n=re.subn(
        r'<div class="shop-platform-note">.*?</div>',
        ('<div class="shop-platform-note">AWOOO: The Tale of a Husky is available on Amazon Kindle. '
         'AWOOO CHRONICLES is awaiting publication.</div>' if not tr else
         '<div class="shop-platform-note">AWOOO: The Tale of a Husky Amazon Kindle’da yayında. '
         'AWOOO CHRONICLES henüz inceleme aşamasında.</div>'),
        books,count=1,flags=re.S
    )
    if n!=1: raise RuntimeError(f"Old Books note not found: {page}")
    doc=first+sep+books+close+rest
    if ("#amazon-stores" not in books or
        books.count('class="shop-book-actions"') != 1 or
        books.count('awooo-the-tale-of-a-husky-preview.pdf') != 1 or
        "coming soon" in books.lower()):
        raise RuntimeError(f"Shop Buy/Preview controls missing: {page}")
    # Use a small separately versioned stylesheet to avoid stale iOS caching.
    css_href = ("../../" if tr else "../") + "assets/css/book-actions.css?v=20261123c"
    doc=doc.replace("</head>", '<link rel="stylesheet" href="' + css_href + '">\n</head>', 1)
    page.write_text(doc,encoding="utf-8")

book_actions_css = """
/* Shop: the published Kindle book has adjacent Buy and Preview buttons. */
#books .shop-book-actions{
    display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:auto;
    max-width:100%;
}
#books .shop-book-actions .button{
    margin:0;align-self:auto;display:inline-flex;align-items:center;
    justify-content:center;box-sizing:border-box;min-height:44px;
    font-size:clamp(11px,2.8vw,14px);line-height:1.2;
    padding:10px 12px;white-space:nowrap;text-align:center;
}
#books .shop-book-actions .button-outline{
    border:1px solid var(--line,#62717b);background:transparent;color:var(--ink);
}
#books .shop-book-actions .button-outline:hover,
#books .shop-book-actions .button-outline:focus-visible{
    border-color:var(--green);color:var(--green);
}
@media(max-width:760px){
    #books .shop-book-actions{gap:6px}
    #books .shop-book-actions .button{padding:10px 9px}
}
@media(max-width:410px) and (min-width:381px){
    #books .shop-book-actions .button{padding:10px 7px;font-size:11px}
}
"""
css_path = root / "assets/css/book-actions.css"
css_path.write_text(book_actions_css, encoding="utf-8")

print("PASS: 13 Kindle destinations and bilingual Shop Buy + adjacent Preview PDF; pending title retains Details.")
