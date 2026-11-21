#!/usr/bin/env python3
"""Rebuild bilingual portfolio Contact pages in user-approved priority order.

Runs at deployment time on the *extracted* site.zip. Keeps the original
release archive and other site pages untouched.
"""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
base_style = """
<style id="contact-2026-order">
  .contact-grid.contact-priority {
    grid-template-columns: minmax(0,1fr);
    max-width: 960px;
    margin-inline: auto;
    gap: 18px;
  }
  .contact-priority .contact-panel { padding: clamp(24px, 4vw, 37px); }
  .contact-priority .contact-panel > p { min-height: 0; margin-bottom: 17px; }
  .contact-priority .contact-panel h2 { margin-top: 10px; }
  .contact-main-link {
    background: var(--panel-soft);
    border: 1px solid var(--line);
    padding: 21px 23px;
    border-radius: 16px;
    text-decoration: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    font-weight: 800;
    color: var(--text);
  }
  .contact-main-link:hover { border-color: var(--green); }
  .contact-main-link small {
    display: block;
    color: var(--muted);
    font-size: 13px;
    font-weight: 520;
    margin-top: 5px;
    overflow-wrap: anywhere;
  }
  .contact-main-link .contact-main-arrow { font-size: 23px; }
  .contact-project { padding: 7px 0 20px; }
  .contact-project + .contact-project { border-top: 1px solid var(--line); padding-top: 18px; }
  .contact-project .contact-link { border-top: 0; padding: 9px 3px 13px; }
  .contact-project .contact-link small { margin-top: 3px; }
  .contact-support-links {
    display: flex;
    flex-wrap: wrap;
    gap: 9px 22px;
    padding: 0 3px;
  }
  .contact-support-links a {
    font-size: 13px;
    font-weight: 600;
    color: var(--green);
    overflow-wrap: anywhere;
    text-decoration: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 4px;
  }
  .contact-support-links a:hover { text-decoration-thickness: 2px; }
  @media (max-width: 540px) {
    .contact-support-links { flex-direction: column; gap: 11px; }
    .contact-main-link { padding: 18px; }
  }
</style>
"""
def common_project_links(tr):
    gen = "Genel iletişim" if tr else "General enquiries"
    sup = "Destek" if tr else "Support"
    website = "Resmî web sitesi" if tr else "Official website"
    return f"""
<div class="contact-project">
  <a href="https://gentianapp.com/" target="_blank" rel="noopener noreferrer" class="contact-link"><span>Gentian <small>{website} · gentianapp.com</small></span><span aria-hidden="true">↗</span></a>
  <div class="contact-support-links">
    <a href="mailto:info@gentianapp.com">{gen}: info@gentianapp.com</a>
    <a href="mailto:support@gentianapp.com">{sup}: support@gentianapp.com</a>
  </div>
</div>
<div class="contact-project">
  <a href="https://isvicrerotam.com/" target="_blank" rel="noopener noreferrer" class="contact-link"><span>İsviçre Rotam <small>{website} · isvicrerotam.com</small></span><span aria-hidden="true">↗</span></a>
  <div class="contact-support-links">
    <a href="mailto:info@isvicrerotam.com">{gen}: info@isvicrerotam.com</a>
    <a href="mailto:destek@isvicrerotam.com">{sup}: destek@isvicrerotam.com</a>
  </div>
</div>
"""
def make_contact(tr):
    main_kicker = "ANA İLETİŞİM" if tr else "PRIMARY CONTACT"
    main_title = "Doğrudan iletişim" if tr else "Get in touch directly"
    main_desc = ("İş birlikleri, kitaplar ve genel sorular için benimle doğrudan iletişime geçebilirsiniz."
                 if tr else "For collaborations, books and general enquiries, contact me directly.")
    main_label = "Bülent İmat · Ana iletişim" if tr else "Bülent İmat · Main contact"
    project_kicker = "RESMÎ PROJELER" if tr else "OFFICIAL PROJECTS"
    project_title = "Uygulamalar ve destek" if tr else "Apps & support"
    project_desc = ("Uygulamaların resmî siteleri ile genel iletişim ve destek e-posta adresleri."
                    if tr else "Official product websites with their dedicated contact and support emails.")
    social_kicker = "SOSYAL MEDYA" if tr else "SOCIAL MEDIA"
    social_title = "Yolculuğumu takip et" if tr else "Follow my journey"
    social_desc = ("Benim ve Güney’in maceralarımızı Instagram’da takip edebilir, GitHub’daki çalışmalarımı inceleyebilirsiniz."
                   if tr else "Follow my adventures with Güney on Instagram, or explore my projects on GitHub.")
    notice = ("Bu portfolyoda hesap açmak veya form doldurmak gerekmiyor. Bağlantılar yalnızca siz seçtiğinizde açılır."
              if tr else "No registration or contact form is required. Links open only when you choose them.")
    return f"""<div class="contact-grid contact-priority">
<section class="contact-panel" id="primary-contact">
  <span class="section-kicker">{main_kicker}</span>
  <h2>{main_title}</h2>
  <p>{main_desc}</p>
  <a href="mailto:info@bulentimat.ch" class="contact-main-link"><span>{main_label}<small>info@bulentimat.ch</small></span><span class="contact-main-arrow" aria-hidden="true">↗</span></a>
</section>
<section class="contact-panel" id="official-projects">
  <span class="section-kicker">{project_kicker}</span>
  <h2>{project_title}</h2>
  <p>{project_desc}</p>
  {common_project_links(tr)}
</section>
<section class="contact-panel" id="social-media">
  <span class="section-kicker">{social_kicker}</span>
  <h2>{social_title}</h2>
  <p>{social_desc}</p>
  <a href="https://www.instagram.com/bulentimat/" target="_blank" rel="noopener noreferrer" class="contact-link"><span>Instagram <small>@bulentimat</small></span><span aria-hidden="true">↗</span></a>
  <a href="https://www.instagram.com/guneythehusky/" target="_blank" rel="noopener noreferrer" class="contact-link"><span>Instagram <small>@guneythehusky</small></span><span aria-hidden="true">↗</span></a>
  <a href="https://github.com/bulentimat-ai" target="_blank" rel="noopener noreferrer" class="contact-link"><span>GitHub <small>bulentimat-ai</small></span><span aria-hidden="true">↗</span></a>
  <div class="contact-notice">{notice}</div>
</section>
</div>"""

pattern = re.compile(r'<div class="contact-grid(?: contact-priority)?">.*?</div>\s*</main>', re.S)
expected = (
    "mailto:info@bulentimat.ch",
    "https://gentianapp.com/",
    "mailto:info@gentianapp.com",
    "mailto:support@gentianapp.com",
    "https://isvicrerotam.com/",
    "mailto:info@isvicrerotam.com",
    "mailto:destek@isvicrerotam.com",
    "https://www.instagram.com/bulentimat/",
    "https://www.instagram.com/guneythehusky/",
    "https://github.com/bulentimat-ai",
)

for rel, tr in (("contact/index.html", False), ("tr/contact/index.html", True)):
    target = root / rel
    html = target.read_text(encoding="utf-8")
    replacement = make_contact(tr)
    html, n = pattern.subn(lambda m: replacement + "\n</main>", html, count=1)
    if n != 1:
        raise SystemExit(f"Missing single contact container in {rel}")
    if "id=\"contact-2026-order\"" not in html:
        if "</head>" not in html:
            raise SystemExit(f"Missing </head> in {rel}")
        html = html.replace("</head>", base_style + "\n</head>", 1)
    content = html.split('<div class="contact-grid contact-priority">', 1)[-1].split("</main>", 1)[0]
    for link in expected:
        if content.count(f'href="{link}"') != 1:
            raise SystemExit(f"Unexpected number of {link} in {rel}")
    for term in ("id=\"primary-contact\"", "id=\"official-projects\"", "id=\"social-media\""):
        if content.count(term) != 1:
            raise SystemExit(f"Unexpected section count: {term} in {rel}")
    if not(content.index('id="primary-contact"') < content.index('id="official-projects"') < content.index('id="social-media"')):
        raise SystemExit(f"Incorrect contact order in {rel}")
    target.write_text(html, encoding="utf-8")
    print(f"Validated contact priority and 10 links: {rel}")
