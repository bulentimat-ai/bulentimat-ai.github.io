#!/usr/bin/env python3
"""Swiss Alpine Routes branding update for extracted bilingual portfolio site."""
from pathlib import Path
import re, sys, shutil
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('_site')
hero='https://d2ol7oe51mr4n9.cloudfront.net/user_3Lum1zJjO96eiqJljGZPc2qT8El/f0a4d040-c71c-4648-866d-baaabba8f240.jpg'
gentian_hero='https://d2ol7oe51mr4n9.cloudfront.net/user_3Lum1zJjO96eiqJljGZPc2qT8El/603cd314-aba1-4b19-b789-1c0c3d9d2e0d.png'
screens={
'map':'https://d2ol7oe51mr4n9.cloudfront.net/user_3Lum1zJjO96eiqJljGZPc2qT8El/e9d41b95-78ce-4635-8315-92839146fac9.jpg',
'planning':'https://d2ol7oe51mr4n9.cloudfront.net/user_3Lum1zJjO96eiqJljGZPc2qT8El/da4cd8bd-4ee1-46f8-b30b-9b2b14bc7c4e.jpg',
'safety':'https://d2ol7oe51mr4n9.cloudfront.net/user_3Lum1zJjO96eiqJljGZPc2qT8El/2d5ec587-ade2-4d7b-ac67-d6da77e94d4b.jpg'}
css='''.sar-home-card .sar-cover{width:100%;aspect-ratio:2.4/1;object-fit:cover;border-radius:13px;margin:12px 0}.sar-home-card .sar-note{font-size:12px;color:#297768}.sar-icon{display:grid;place-items:center;width:52px;height:52px;border-radius:14px;background:#dc291e;color:white;font-size:26px}.sar-shop img{width:100%;aspect-ratio:2.4/1;object-fit:cover}.sar-product{padding-bottom:70px}.sar-product>section{margin-top:35px}.sar-product .sar-hero{width:100%;border-radius:22px;display:block}.sar-product .sar-shots{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.sar-shots img{width:100%;border-radius:14px}.sar-product h1{font-size:clamp(36px,5vw,66px)}@media(max-width:650px){.sar-product .sar-shots{grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}}'''
css+='''.portfolio-shop-grid .home-app.sar-promo-card{display:flex;flex-direction:column;min-width:0;gap:0}
.portfolio-shop-grid .sar-promo-card .home-app-title{width:100%;min-height:64px;margin-bottom:14px}
.portfolio-shop-grid .sar-promo-card .sar-promo-image{display:block;width:100%;height:auto;aspect-ratio:2.27/1;object-fit:cover;object-position:center;border-radius:13px;border:1px solid rgba(17,43,61,.11);margin:0}
.portfolio-shop-grid .sar-promo-card .sar-app-icon{display:block;width:56px;height:56px;object-fit:cover;border-radius:15px;flex:none;box-shadow:0 5px 15px rgba(15,36,52,.16)}
.portfolio-shop-grid .sar-promo-card .card-text-link{margin-top:auto;display:block;padding-top:16px;text-align:center}
.portfolio-shop-grid .sar-promo-card .sar-premium-caption{font-size:11px;color:#628273;font-weight:700;margin:9px 0 0;line-height:1.2}
@media(max-width:650px){.portfolio-shop-grid .sar-promo-card .sar-promo-image{aspect-ratio:2.18/1}.portfolio-shop-grid .sar-promo-card .sar-app-icon{width:44px;height:44px;border-radius:12px}.portfolio-shop-grid .sar-promo-card .home-app-title{min-height:56px}}
'''
icon_source=Path('assets/images/swiss-alpine-icon.png')
if not icon_source.is_file(): raise RuntimeError('Authentic Swiss Alpine Routes icon missing from repository')
shutil.copyfile(icon_source,root/'assets/images/swiss-alpine-icon.png')
(root/'assets/css/swiss-alpine-portfolio.css').write_text(css,encoding='utf-8')
for tr in (False,True):
    prefix='tr/' if tr else ''
    home=root/(prefix+'index.html')
    html=home.read_text(encoding='utf-8')
    description='İsviçre haritaları · Yürüyüş · MTB · Çevrimdışı' if tr else 'Swiss maps · Hiking · Cycling · MTB · Offline'
    gen_desc='Top 100 · Arabasız gezi planlama' if tr else 'Top 100 · Car-free trip planning'
    button='Uygulamayı keşfet ↗' if tr else 'Discover the app ↗'
    logo_path='../assets/images/swiss-alpine-icon.png' if tr else 'assets/images/swiss-alpine-icon.png'
    gentian_card=f'''<a class="home-app sar-promo-card" href="apps/gentian/">
      <div class="home-app-title"><span class="app-symbol gentian" role="img" aria-label="Gentian app icon"></span><div><strong>Gentian – Swiss Alps</strong><span>{gen_desc}</span></div></div>
      <img class="sar-promo-image" src="{gentian_hero}" alt="Gentian promotional cover with two iPhones showing Discover and Oeschinensee" loading="lazy" decoding="async">
      <span class="card-text-link">{button}</span></a>'''
    swiss_card=f'''<a class="home-app sar-promo-card" href="apps/swiss-alpine-routes/">
      <div class="home-app-title"><img class="sar-app-icon" src="{logo_path}" alt="Swiss Alpine Routes original app icon with white mountain on red background"><div><strong>Swiss Alpine Routes</strong><span>{description}</span></div></div>
      <img class="sar-promo-image" src="{hero}" alt="Swiss Alpine Routes promotional cover with two iPhones showing map and cycling route" loading="lazy" decoding="async">
      <span class="card-text-link">{button}</span></a>'''
    html,n=re.subn(r'<a class="home-app" href="apps/gentian/">.*?</a>',lambda _:gentian_card,html,count=1,flags=re.S)
    if n!=1:raise RuntimeError('Could not find Gentian card: '+str(home))
    html,n=re.subn(r'<a class="home-app" href="apps/isvicre-rotam/">.*?</a>',lambda _:swiss_card,html,count=1,flags=re.S)
    if n!=1:raise RuntimeError('Could not find Swiss Alpine Routes card: '+str(home))
    html=html.replace('</head>',f'<link rel="stylesheet" href="{"../" if tr else ""}assets/css/swiss-alpine-portfolio.css?v=20261122c"></head>',1)
    if html.count('class="home-app sar-promo-card"')!=2:raise RuntimeError('Two balanced app cards required')
    home.write_text(html,encoding='utf-8')

    shop=root/(prefix+'shop/index.html')
    html=shop.read_text(encoding='utf-8')
    desc='İsviçre Rotam, bu uygulamanın Türkçe dil seçeneğidir.' if tr else 'English by default, with a built-in Turkish interface.'
    article=f'''<article class="shop-product sar-shop"><img src="{hero}" alt="Swiss Alpine Routes latest promotional cover" loading="lazy"><h3>Swiss Alpine Routes</h3><p>Hiking · Cycling · MTB · Swiss Top 100 · Offline</p><p>{desc}</p><a class="button button-outline" href="../apps/swiss-alpine-routes/">{button}</a><a class="shop-platform-link" href="https://isvicrerotam.com/">Official website ↗</a></article>'''
    html,n=re.subn(r'<article class="shop-product"><img[^>]*rotam-banner\.webp[^>]*>.*?</article>',lambda _:article,html,count=1,flags=re.S)
    if n!=1:raise RuntimeError('Cannot find old shop card: '+str(shop))
    shop.write_text(html,encoding='utf-8')

    directory=root/(prefix+'apps/index.html')
    html=directory.read_text(encoding='utf-8').replace('İsviçre Rotam','Swiss Alpine Routes').replace('isvicre-rotam/','swiss-alpine-routes/')
    html=re.sub(r'(?:(?:\.\./)+|assets/)images/rotam-banner\.webp',hero,html)
    html=re.sub(r'(?:(?:\.\./)+|assets/)images/rotam-1\.webp',screens['map'],html)
    html=re.sub(r'(?:(?:\.\./)+|assets/)images/rotam-2\.webp',screens['planning'],html)
    directory.write_text(html,encoding='utf-8')

    old=root/(prefix+'apps/isvicre-rotam/index.html')
    page=old.read_text(encoding='utf-8')
    intro='İsviçre Rotam, Swiss Alpine Routes uygulamasının Türkçe dil seçeneğidir.' if tr else 'One app for Switzerland. İsviçre Rotam is the Turkish localization, not a separate product.'
    heading='İsviçre Alpleri, tek uygulamada.' if tr else 'The Swiss Alps, beautifully mapped.'
    summary='Harita, rota planlama, çevrimdışı navigasyon, Swiss Top 100 ve dağ güvenliği.' if tr else 'Swiss mapping, route planning, offline navigation, Swiss Top 100 and mountain safety.'
    body=f'''<main id="main" class="container-wide sar-product"><section><span class="section-kicker">SWISS ALPINE ROUTES · IOS</span><h1>{heading}</h1><p>{intro}</p><img class="sar-hero" src="{hero}" alt="Swiss Alpine Routes real app screens"><p>{summary}</p><p><a class="button button-primary" href="https://isvicrerotam.com/">Official app website ↗</a></p></section><section><h2>Swiss maps · Hiking · Cycling · MTB</h2><p>swisstopo · SchweizMobil · swissALTI3D · GPX · GPS · Offline · Mountain weather · SLF · SOS · Swiss public transport</p><div class="sar-shots"><img src="{screens['map']}" alt="Map screen"><img src="{screens['planning']}" alt="Route planner"><img src="{screens['safety']}" alt="Safety screen"></div></section></main>'''
    page,n=re.subn(r'<main id="main"[^>]*>.*?</main>',lambda _:body,page,count=1,flags=re.S)
    if n!=1:raise RuntimeError('Cannot find product main: '+str(old))
    page=page.replace('İsviçre Rotam','Swiss Alpine Routes').replace('<title>','<title>Swiss Alpine Routes · ',1)
    page=page.replace('</head>','<link rel="stylesheet" href="../../../assets/css/swiss-alpine-portfolio.css?v=20261122b"></head>',1)
    new=root/(prefix+'apps/swiss-alpine-routes/index.html')
    new.parent.mkdir(parents=True,exist_ok=True)
    new.write_text(page,encoding='utf-8')
    old.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../swiss-alpine-routes/"><title>Swiss Alpine Routes</title></head><body><a href="../swiss-alpine-routes/">Swiss Alpine Routes</a></body></html>',encoding='utf-8')
for p in ['index.html','tr/index.html','shop/index.html','tr/shop/index.html','apps/swiss-alpine-routes/index.html','tr/apps/swiss-alpine-routes/index.html']:
    if 'Swiss Alpine Routes' not in (root/p).read_text(encoding='utf-8'):raise RuntimeError('Missing branding '+p)
print('Swiss Alpine Routes portfolio update complete')