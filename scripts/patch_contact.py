#!/usr/bin/env python3
"""Add primary and project contact email addresses to both portfolio languages.

The published static site is extracted from site.zip into _site.
This script changes only the contact pages inside the published artifact.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
addresses = (
    "info@bulentimat.ch",
    "info@gentianapp.com",
    "support@gentianapp.com",
    "info@isvicrerotam.com",
    "destek@isvicrerotam.com",
)
sections = {
    "contact/index.html": """
<div class="contact-email-section" aria-labelledby="email-contacts-en">
  <span class="section-kicker" style="display:block;margin-top:30px">EMAIL CONTACT</span>
  <h3 id="email-contacts-en" style="font-size:23px;margin:10px 0 12px">Contact by email</h3>
  <p style="font-size:14px;color:var(--muted);line-height:1.6;margin:0 0 17px">
    For portfolio enquiries and collaborations, use the main address below.
    For app support, use the project-specific addresses.
  </p>
  <a class="contact-link" style="background:rgba(70,120,96,.07);border:1px solid rgba(70,120,96,.28);border-radius:14px;padding:16px;margin:14px 0 18px" href="mailto:info@bulentimat.ch"><span>Bülent İmat · Main contact <small>info@bulentimat.ch</small></span><span aria-hidden="true">↗</span></a>
  <a class="contact-link" href="mailto:info@gentianapp.com"><span>Gentian · General enquiries <small>info@gentianapp.com</small></span><span aria-hidden="true">↗</span></a>
  <a class="contact-link" href="mailto:support@gentianapp.com"><span>Gentian · Support <small>support@gentianapp.com</small></span><span aria-hidden="true">↗</span></a>
  <a class="contact-link" href="mailto:info@isvicrerotam.com"><span>İsviçre Rotam · General enquiries <small>info@isvicrerotam.com</small></span><span aria-hidden="true">↗</span></a>
  <a class="contact-link" href="mailto:destek@isvicrerotam.com"><span>İsviçre Rotam · Support <small>destek@isvicrerotam.com</small></span><span aria-hidden="true">↗</span></a>
</div>
""",
    "tr/contact/index.html": """
<div class="contact-email-section" aria-labelledby="email-contacts-tr">
  <span class="section-kicker" style="display:block;margin-top:30px">E-POSTA İLETİŞİMİ</span>
  <h3 id="email-contacts-tr" style="font-size:23px;margin:10px 0 12px">E-posta adresleri</h3>
  <p style="font-size:14px;color:var(--muted);line-height:1.6;margin:0 0 17px">
    Portfolyo ve iş birliği talepleri için ana e-posta adresini kullanabilirsiniz.
    Uygulamalarla ilgili sorularınızı ise ilgili projenin adresine iletebilirsiniz.
  </p>
  <a class="contact-link" style="background:rgba(70,120,96,.07);border:1px solid rgba(70,120,96,.28);border-radius:14px;padding:16px;margin:14px 0 18px" href="mailto:info@bulentimat.ch"><span>Bülent İmat · Ana iletişim <small>info@bulentimat.ch</small></span><span aria-hidden="true">↗</span></a>
  <a class="contact-link" href="mailto:info@gentianapp.com"><span>Gentian · Genel iletişim <small>info@gentianapp.com</small></span><span aria-hidden="true">↗</span></a>
  <a class="contact-link" href="mailto:support@gentianapp.com"><span>Gentian · Destek <small>support@gentianapp.com</small></span><span aria-hidden="true">↗</span></a>
  <a class="contact-link" href="mailto:info@isvicrerotam.com"><span>İsviçre Rotam · Genel iletişim <small>info@isvicrerotam.com</small></span><span aria-hidden="true">↗</span></a>
  <a class="contact-link" href="mailto:destek@isvicrerotam.com"><span>İsviçre Rotam · Destek <small>destek@isvicrerotam.com</small></span><span aria-hidden="true">↗</span></a>
</div>
""",
}
needle = '<div class="contact-notice">'
for rel, section in sections.items():
    target = root / rel
    html = target.read_text(encoding="utf-8")
    if all(f'mailto:{addr}' in html for addr in addresses):
        print(f"Already contains all five addresses: {rel}")
        continue
    if html.count(needle) != 1:
        raise SystemExit(f"Expected exactly one contact notice in {rel}")
    html = html.replace(needle, section + needle, 1)
    if not all(html.count(f"mailto:{addr}") == 1 for addr in addresses):
        raise SystemExit(f"Email link validation failed: {rel}")
    target.write_text(html, encoding="utf-8")
    print(f"Updated bilingual contact page: {rel}")
