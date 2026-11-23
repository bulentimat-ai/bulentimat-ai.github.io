#!/usr/bin/env python3
"""Refresh personal, creator and Husky Instagram profiles on EN/TR portfolio pages."""
from pathlib import Path
import base64
import hashlib
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
photos = {
    "personal": "ab4faf00890060b31b73a97d8802d5bf3ec87e42caa7d0f51030e286e515338b",
    "creator": "fd721a9a6961947ecda34b8d4e8f78679a1c09692554eaff1cba6a5a0cdab067",
}
for kind, expected_sha in photos.items():
    source = Path(f"assets/images/avatar-{kind}-2026.webp.b64")
    image = base64.b64decode(source.read_text(encoding="ascii").strip(), validate=True)
    if hashlib.sha256(image).hexdigest() != expected_sha:
        raise RuntimeError(f"Unexpected image checksum: {source}")
    target = root / f"assets/images/avatar-{kind}-2026.webp"
    target.write_bytes(image)
    print(f"Installed {target}: {len(image)} bytes")

css = """
<style id="instagram-2026-layout">
.story-social .story-profiles {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:clamp(6px,1.5vw,18px);
    align-items:start;
    justify-items:center;
    width:100%;
    max-width:550px;
    margin-inline:auto;
}
.story-social .story-profiles > a {
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:flex-start;
    min-width:0;
    width:100%;
    max-width:165px;
    padding-inline:2px;
    text-align:center;
    text-decoration:none;
}
.story-social .story-profiles > a img {
    display:block;
    width:clamp(54px,8vw,94px);
    height:clamp(54px,8vw,94px);
    max-width:100%;
    aspect-ratio:1;
    object-fit:cover;
    border-radius:50%;
}
.story-social .story-profiles > a span {
    display:block;
    max-width:100%;
    font-size:clamp(10px,2.65vw,14px);
    line-height:1.3;
    overflow-wrap:anywhere;
}
.story-social .story-profiles > a small {
    display:block;
    margin-top:5px;
    font-size:clamp(9px,2.25vw,11px);
    font-weight:600;
    letter-spacing:.02em;
    color:#b9c9cb;
    line-height:1.2;
}
@media(max-width:420px){
    .story-social .story-profiles {gap:4px}
    .story-social .story-profiles > a {padding-inline:0}
    .story-social .story-profiles > a img {width:clamp(50px,15vw,72px);height:clamp(50px,15vw,72px)}
    .story-social .story-profiles > a span {font-size:clamp(10px,2.7vw,12px);letter-spacing:-.01em}
}
</style>
"""

for tr in (False, True):
    prefix = "tr/" if tr else ""
    img_prefix = "../" if tr else ""
    filename = root / (prefix + "index.html")
    html = filename.read_text(encoding="utf-8")
    personal_label = "Kişisel" if tr else "Personal"
    creator_label = "Profesyonel" if tr else "Creator"
    base = '<div class="story-profiles"><a href="https://www.instagram.com/bulentimat/" target="_blank" rel="noopener noreferrer"><img src="' + img_prefix + 'assets/images/avatar-bulent.webp" alt="Bülent İmat"><span>@bulentimat</span></a>'
    new = ('<div class="story-profiles">'
           '<a href="https://www.instagram.com/bulentimat/" target="_blank" rel="noopener noreferrer" aria-label="Instagram · @bulentimat · ' + personal_label + '">'
           '<img src="' + img_prefix + 'assets/images/avatar-personal-2026.webp?v=20261123" alt="Bülent İmat ve Güney · kişisel portre">'
           '<span>@bulentimat</span><small>' + personal_label + '</small></a>'
           '<a href="https://www.instagram.com/bulentcreates/" target="_blank" rel="noopener noreferrer" aria-label="Instagram · @bulentcreates · ' + creator_label + '">'
           '<img src="' + img_prefix + 'assets/images/avatar-creator-2026.webp?v=20261123" alt="Bülent İmat ve Güney · yazar ve uygulama geliştiricisi portresi">'
           '<span>@bulentcreates</span><small>' + creator_label + '</small></a>')
    if html.count(base) != 1:
        raise RuntimeError(f"Expected one original personal profile in {filename}, got {html.count(base)}")
    html = html.replace(base, new, 1)
    dog_old = '<span>@guneythehusky</span></a></div></div>'
    dog_new = '<span>@guneythehusky</span><small>Güney</small></a></div></div>'
    if html.count(dog_old) != 1:
        raise RuntimeError(f"Expected one Husky profile in {filename}")
    html = html.replace(dog_old, dog_new, 1)
    html = html.replace("</head>", css + "\n</head>", 1)
    profile_markup = html.split('<div class="story-profiles">', 1)[1].split('</div></div>', 1)[0]
    for handle in ("bulentimat", "bulentcreates", "guneythehusky"):
        if profile_markup.count('href="https://www.instagram.com/' + handle + '/"') != 1:
            raise RuntimeError(f"Wrong profile-card handle count: {handle} in {filename}")
    filename.write_text(html, encoding="utf-8")
    print(f"Validated EN/TR homepage Instagram trio: {filename}")

    contact = root / (prefix + "contact/index.html")
    html = contact.read_text(encoding="utf-8")
    original = '<a href="https://www.instagram.com/bulentimat/" target="_blank" rel="noopener noreferrer" class="contact-link"><span>Instagram <small>@bulentimat</small></span><span aria-hidden="true">↗</span></a>'
    person = "Instagram · Kişisel" if tr else "Instagram · Personal"
    professional = "Instagram · Profesyonel" if tr else "Instagram · Creator"
    dog = "Instagram · Güney"
    replacement = (
       '<a href="https://www.instagram.com/bulentimat/" target="_blank" rel="noopener noreferrer" class="contact-link"><span>' + person + ' <small>@bulentimat</small></span><span aria-hidden="true">↗</span></a>\n'
       '<a href="https://www.instagram.com/bulentcreates/" target="_blank" rel="noopener noreferrer" class="contact-link"><span>' + professional + ' <small>@bulentcreates</small></span><span aria-hidden="true">↗</span></a>\n'
    )
    if html.count(original) != 1:
        raise RuntimeError(f"Expected one personal contact link in {contact}")
    html = html.replace(original, replacement.rstrip(), 1)
    original_dog = '<a href="https://www.instagram.com/guneythehusky/" target="_blank" rel="noopener noreferrer" class="contact-link"><span>Instagram <small>@guneythehusky</small></span><span aria-hidden="true">↗</span></a>'
    new_dog = original_dog.replace('Instagram <small>', dog + ' <small>')
    if html.count(original_dog) != 1:
        raise RuntimeError(f"Expected one Husky contact link in {contact}")
    html = html.replace(original_dog, new_dog, 1)
    old_desc = ("Benim ve Güney’in maceralarımızı Instagram’da takip edebilir, GitHub’daki çalışmalarımı inceleyebilirsiniz." if tr else "Follow my adventures with Güney on Instagram, or explore my projects on GitHub.")
    new_desc = ("Kişisel paylaşımlarımı @bulentimat, kitap ve uygulama çalışmalarımı @bulentcreates, Güney’in maceralarını @guneythehusky hesabında takip edebilirsiniz. Kod projelerim GitHub’da." if tr else "Follow my personal journey at @bulentimat, books and apps at @bulentcreates, and Güney’s adventures at @guneythehusky. Explore my projects on GitHub.")
    if html.count(old_desc) != 1:
        raise RuntimeError(f"Contact description changed unexpectedly in {contact}")
    html = html.replace(old_desc, new_desc, 1)
    section = html.split('id="social-media"', 1)[1].split("</section>", 1)[0]
    for handle in ("bulentimat", "bulentcreates", "guneythehusky"):
        if section.count(f'https://www.instagram.com/{handle}/') != 1:
            raise RuntimeError(f"Wrong contact handle count for {handle} in {contact}")
    if 'https://github.com/bulentimat-ai' not in section:
        raise RuntimeError(f"Lost GitHub link in {contact}")
    contact.write_text(html, encoding="utf-8")
    print(f"Validated EN/TR Contact social links: {contact}")

print("PASS: three distinct Instagram accounts and two new portrait assets; EN/TR and mobile layout.")
