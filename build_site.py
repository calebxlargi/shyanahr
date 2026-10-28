"""Build the complete local-only ShyanaHR site from retained source material."""
from pathlib import Path
import re,json,html,shutil,runpy,os
from urllib.parse import quote

ROOT=Path(__file__).resolve().parent
D=ROOT/'dist';R=ROOT.parent/'rebuild-resources'
ORIGIN=os.environ.get('SITE_URL','https://shyanahr.com.my').rstrip('/')
runpy.run_path(str(ROOT/'build_page.py'))
base=(D/'index.html').read_text()
e=html.escape
clean=lambda text:' '.join(html.unescape(re.sub(r'<[^>]+>',' ',text)).split())
manifest=json.loads((R/'resource-manifest.json').read_text()) if (R/'resource-manifest.json').is_file() else []
lookup={x['url']:x for x in manifest}

def source(route):
    retained=R/'mirror/shyanahr.com.my'/route/'index.html'
    return (retained if retained.is_file() else ROOT/'content/source-pages'/route/'index.html').read_text()
def copy_url(url,name):
    target=D/'assets'/name;target.parent.mkdir(parents=True,exist_ok=True)
    if url not in lookup and target.is_file():return '/assets/'+name
    shutil.copy2(R/lookup[url]['file'],target)
    return '/assets/'+name
def copy_relative(route,path,name):
    src=(R/'mirror/shyanahr.com.my'/route/path).resolve()
    target=D/'assets'/name;target.parent.mkdir(parents=True,exist_ok=True)
    if not src.is_file() and target.is_file():return '/assets/'+name
    shutil.copy2(src,target)
    return '/assets/'+name

def localize(page):
    page=re.sub(r'(<a\b[^>]*\bhref=")https://shyanahr\.com\.my/([a-z0-9/-]+)(")',lambda m:m[1]+'/'+m[2].rstrip('/')+'/'+m[3],page)
    page=page.replace('href="./"','href="/"')
    page=re.sub(r'((?:href|src|data-image)=")assets/',r'\1/assets/',page)
    page=page.replace('href="styles.css"','href="/styles.css"').replace('src="app.js"','src="/app.js"')
    page=page.replace('https://shyanahr-homepage-2026.sillycamel128.chatgpt.site/assets/shyana-logo.webp','/assets/shyana-logo.webp')
    return page

base=localize(base)
base=re.sub(r'<meta property="og:image"[^>]*>',f'<meta property="og:image" content="{ORIGIN}/assets/shyana-logo.webp">',base)
header=re.search(r'<header class="site-header">.*?</header>',base,re.S)[0]
footer=re.search(r'<footer class="site-footer.*?</footer>',base,re.S)[0]
footer=footer.replace('href="#services"','href="/#services"')
clientstrip=re.search(r'<section class="clients wrap".*?</section>',base,re.S)[0]
head=re.search(r'<!doctype html>.*?</head>',base,re.S)[0]
head=head.replace('</head>','<link rel="stylesheet" href="/pages.css"><script src="/pages.js" defer></script></head>')
arrow='<svg class="arrow" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 15 15 5M5 5h10v10"/></svg>'
records=[]

def service_contact():
    return '<section class="wrap section service-contact"><div><p class="eyebrow muted">ShyanaHR</p><h2>Wish to know <span class="serif">more?</span></h2><a class="text-link" href="/contact/">Contact Us Now! '+arrow+'</a></div><div><h3>Contact Us / Address</h3><p>L-07-01, Level 7, Block L<br>Solaris Mont Kiara No 2 Jalan Solaris<br>Mont Kiara 50480 Kuala Lumpur Malaysia</p></div><div><h3>Hotline</h3><a href="tel:+60362000670">03-6200 0670</a><a href="tel:+60362000699">03-6200-0699 (Fax)</a><a href="mailto:support@shyanahr.com.my">support@shyanahr.com.my</a><h3 class="social-heading">Social Links</h3><p><a href="https://www.facebook.com/shyanahrmy">Facebook</a> · <a href="https://wa.me/60193351697">Whatsapp</a> · <a href="https://instagram.com/shyana.hr/">Instagram</a> · <a href="https://www.tiktok.com/@shyanahr7">TikTok</a></p></div></section>'

def intro(label,title,emphasis='',description=''):
    heading=e(title)+(f'<span class="serif">{e(emphasis)}</span>' if emphasis else '')
    return f'<section class="page-intro wrap"><div class="page-topline"><a href="/">Home</a><span>/</span><span>{e(label)}</span><span class="page-location">Kuala Lumpur · Malaysia</span></div><div class="page-intro-grid"><div><p class="eyebrow muted">{e(label)}</p><h1>{heading}</h1></div><div class="intro-note">{description}</div></div></section>'

def write(route,title,body,description,group):
    pagehead=re.sub(r'<title>.*?</title>',f'<title>{e(title)} | ShyanaHR</title>',head)
    pagehead=re.sub(r'<meta name="description"[^>]*>',f'<meta name="description" content="{e(description)}">',pagehead)
    pagehead=re.sub(r'<meta property="og:title"[^>]*>',f'<meta property="og:title" content="{e(title)} | ShyanaHR">',pagehead)
    pagehead=re.sub(r'<meta property="og:description"[^>]*>',f'<meta property="og:description" content="{e(description)}">',pagehead)
    pagehead=pagehead.replace('</head>',f'<link rel="canonical" href="{ORIGIN}/{route}/"><meta property="og:url" content="{ORIGIN}/{route}/"></head>')
    pageheader=header.replace('class="nav-link active"','class="nav-link"').replace(' aria-current="page"','')
    if route=='about':pageheader=pageheader.replace('class="nav-link" href="/about/"','class="nav-link active" href="/about/" aria-current="page"')
    if route=='contact':pageheader=pageheader.replace('class="nav-contact"','class="nav-contact active" aria-current="page"')
    for i,name in enumerate(['Services','Awards','Gallery']):
        if group==name:pageheader=pageheader.replace(f'aria-controls="nav-group-{i}"',f'aria-controls="nav-group-{i}" class="current-group"')
    dialog='''<dialog class="media-dialog" aria-label="Image viewer"><div class="dialog-toolbar"><span id="lightbox-caption"></span><button class="dialog-close" aria-label="Close image viewer">Close ×</button></div><div class="dialog-image-wrap"><button class="dialog-prev" aria-label="Previous image">←</button><img id="lightbox-image" alt=""><button class="dialog-next" aria-label="Next image">→</button></div><p class="dialog-counter" aria-live="polite"></p></dialog>'''
    page=pagehead+'<body id="top"><a href="#main" class="skip-link">Skip to content</a>'+pageheader+'<main id="main">'+body+clientstrip+'</main>'+footer+dialog+'</body></html>'
    directory=D/route;directory.mkdir(parents=True,exist_ok=True);(directory/'index.html').write_text(localize(page))
    records.append({'route':'/'+route+'/','title':title})

# About: retain every paragraph and the four original values illustrations.
about_copy=[
"Shyana HR Consulting & Training (SCT) is registered with HRDF and have been providing these services for various GLCs, MNCs and SMEs. SCT is a team of passionate and forward-thinking individuals who would want to make a difference in people's lives and organization.",
"Our diverse training & consultancy services cater to all employees across the organization. It is our duty to bring about improvements to their performance and make them realize their most important goals.",
'We enthusiastically believe that learning & development is pivotal in ensuring employees\' skills and competence are relevant to face "The New Normal" and future challenges.',
"Apart from providing high impact quality programs, SCT recognizes the importance of total customer experience. With our strong core values of ATTITUDE, BELIEVE, COMMITMENT & DISCIPLINE, we make it our business and take pride in ensuring that we walk the talk and strive to continuously improve our offerings to all our clients.",
"Our team comprises talented and dedicated HRM experts and consultants who will engage and interact with the decision makers in your organization.",
"Our partnership is based around the objective of HRM & Training Solutions. In order to help the individual, team and the organization to reach their fullest potential, it is paramount that we recognize, value, endorse and see through the solutions."]
body=intro('About Us','About','ShyanaHR.',f'<p>{e(about_copy[0])}</p><a class="text-link" href="/company-profile/">Explore our company profile {arrow}</a>')
photo=copy_url('https://shyanahr.com.my/assets/img/slides/slide1.jpg','about-team.webp')
body+=f'<div class="wrap page-wide-photo"><img src="{photo}" alt="People learning and collaborating in a training session" width="1600" height="650"></div><section class="section wrap about-principles"><article><p class="eyebrow muted">01 / Our purpose</p><h2>Unique Solution</h2><p>{e(about_copy[1])}</p></article><article><p class="eyebrow muted">02 / Our mindset</p><h2>Keep improving</h2><p>{e(about_copy[2])}</p></article></section>'
body+='<section id="values" class="section wrap core-values"><div class="section-head"><div><p class="eyebrow muted">What guides us</p><h2>Our Core <span class="serif">Values.</span></h2></div><p>ATTITUDE · BELIEVE · COMMITMENT · DISCIPLINE</p></div><p class="core-description">'+e(about_copy[3])+'</p><div class="values-grid">'
for i,(value,letter) in enumerate(zip(['Attitude','Believe','Commitment','Discipline'],'abcd'),1):
    src=copy_url('https://shyanahr.com.my/assets/img/about/'+letter+'.jpg','value-'+letter+'.webp')
    body+=f'<article class="value-item"><img src="{src}" alt="{value} — ShyanaHR core value" loading="lazy"><div><span class="eyebrow muted">0{i}</span><h3>{value}</h3></div></article>'
body+='</div></section><section class="section wrap about-team-copy"><p class="eyebrow muted">Our people / Our partnership</p><h2>People with passion.<br><span class="serif">Solutions with purpose.</span></h2><div>'+''.join('<p>'+e(x)+'</p>' for x in about_copy[4:])+'</div></section>'
body+='<section class="section wrap about-contact"><div><p class="eyebrow muted">Together we inspire</p><h2>Get in touch <span class="serif">with us.</span></h2></div><div><p>Unique training solutions from experienced consultants specializing in a variety of HR areas.</p><a class="text-link" href="/contact/">Contact Us '+arrow+'</a></div></section>'
write('about','About Us',body,'Learn about Shyana HR Consulting & Training, our people, our approach and our core values.','About')

# HR Management & Consulting: source order, six full service lists.
s=source('hr-management-consulting')
description=clean(re.search(r'<div class="title-section">.*?<p>(.*?)</p>',s,re.S)[1])
body=intro('Our services','HR Management','& Consulting.',f'<p>{e(description)}</p>')
body+='<section class="section wrap consulting-grid" aria-label="HR consulting services">'
for i,block in enumerate(s.split('<div class="single-product-classes">')[1:],1):
    title=clean(re.search(r'<h3>(.*?)</h3>',block,re.S)[1]);path=re.search(r'<img[^>]+src="([^"]+)"',block)[1]
    src=copy_relative('hr-management-consulting',path,f'consulting-{i}.webp')
    items=[clean(x) for x in re.findall(r'<span class="author[^>]*>(.*?)</span>',block.split('</div>\n                                        </div>')[0],re.S)]
    # Each source block includes later layout; take the first service's list only.
    blocklist=re.search(r'<div class="d-flex flex-column">(.*?)</div>',block,re.S)
    items=[clean(x) for x in re.findall(r'<span[^>]*>(.*?)</span>',blocklist[1],re.S)]
    interest=['HR Technology','Compensation & Benefits','Performance Management System','Recruitment & Selection','Organization Structure','Industrial Relations'][i-1]
    body+=f'<article class="consulting-card"><img src="{src}" alt="{e(title)}" loading="lazy"><p class="eyebrow muted">0{i} / HR Consulting</p><h2>{e(title)}</h2><ul>'+''.join('<li>'+e(x)+'</li>' for x in items)+f'</ul><a class="text-link" href="/contact/?interest={quote(interest)}">Discuss your requirements {arrow}</a></article>'
body+='</section>'+service_contact()
write('hr-management-consulting','HR Management & Consulting',body,description,'Services')

# Professional Development: six original categories and all programme lists.
s=source('professional-development')
rawintro=re.search(r'<div class="title-section">.*?<p>(.*?)</p>',s,re.S)[1]
introparas=[clean(x) for x in re.split(r'<br\s*/?>\s*<br\s*/?>',rawintro) if clean(x)]
body=intro('Our services','Professional','Development.',f'<p>{e(introparas[0])}</p>')
body+='<section class="wrap development-intro"><p>'+e(introparas[1])+'</p></section>'
categories=['Leadership','Fleet','Motivation','Diversity','Technical','University']
body+='<section class="section wrap development-programmes"><div class="programme-filters" role="group" aria-label="Filter programmes">'+''.join(f'<button class="filter-button" data-filter="{name.lower()}" aria-pressed="{str(name=="All").lower()}">{name}</button>' for name in ['All']+categories)+'</div><p class="filter-count" aria-live="polite">6 programme categories</p><div class="development-list">'
for i,(category,block) in enumerate(zip(categories,s.split('<div class="single-classes-area">')[1:]),1):
    title=clean(re.search(r'<h2>(.*?)</h2>',block,re.S)[1]);path=re.search(r'<img[^>]+src="([^"]+)"',block)[1]
    src=copy_relative('professional-development',path,f'development-{i}.webp')
    paragraph=clean(re.search(r'<p[^>]*>(.*?)</p>',block,re.S)[1])
    lst=re.search(r'<div class="content-list professional">(.*?)</div>',block,re.S)
    items=[clean(x) for x in re.findall(r'<p[^>]*>(.*?)</p>',lst[1],re.S)] if lst else []
    # Categories without a programme list must not inherit the following category's list.
    if category not in ['Leadership','Technical','University']:items=[]
    body+=f'<article class="development-card" data-category="{category.lower()}"><div class="development-image"><img src="{src}" alt="{e(title)}" loading="lazy"><span class="eyebrow muted">0{i} / {category}</span></div><div><h2>{e(title)}</h2><p>{e(paragraph)}</p>'
    if items:body+='<details class="programme-details" open><summary>List of programs <span aria-hidden="true">+</span></summary><ul>'+''.join('<li>'+e(x)+'</li>' for x in items)+'</ul></details>'
    body+=f'<a class="text-link" href="/contact/?interest=Professional%20Development">Discuss this programme {arrow}</a></div></article>'
body+='</div></section>'+service_contact()
write('professional-development','Professional Development',body,introparas[0],'Services')

# Awards and galleries: every original image, in original page order.
media_pages=[('award/hr-voty-2022','Awards','HR Vendors of the Year','2022.','HR Vendors of the Year 2022','awards-2022'),('award/vehicle-care-outcome-change-program-2025','Awards','Vehicle Care & Outcome','Change Program 2025.','Vehicle Care & Outcome Change Program 2025','awards-2025'),('gallery/genset-operators-awareness','Gallery','Genset Operators','Awareness.','Genset Operators Awareness','gallery-genset'),('gallery/internal-combustion-engine','Gallery','Internal Combustion','Engine.','ICE (Internal Combustion Engine) Exam Preparation & Coaching','gallery-ice')]
for route,group,line1,line2,title,slug in media_pages:
    s=source(route).split('<div class="logo-showcase-area')[0]
    paths=[x for x in re.findall(r'<img[^>]+src="([^"]+)"',s) if '/images/award/' in x or '/images/gallery/' in x]
    body=intro(group,line1,line2,f'<p>{e(title)}</p><p class="eyebrow muted media-total">{len(paths):02} '+('photographs' if group=='Gallery' else 'images')+'</p>')
    single=len(paths)==1
    body+=f'<section class="section wrap media-collection"><div class="collection-caption"><p class="eyebrow muted">{e(title)}</p><span>Click an image to explore</span></div><div class="media-grid {"award-grid" if group=="Awards" else "photo-grid"}{" single-media" if single else ""}">'
    for i,path in enumerate(paths,1):
        src=copy_relative(route,path,f'{slug}/{i:02}.webp');caption=f'{title} · {i:02} / {len(paths):02}'
        body+=f'<figure><button class="media-button" data-lightbox="{slug}" data-caption="{e(caption)}" aria-label="Open {e(title)} image {i} of {len(paths)}"><img src="{src}" alt="{e(title)} — image {i}" loading="{ "eager" if i==1 else "lazy" }"><span class="media-open" aria-hidden="true">↗</span></button><figcaption><span>{i:02} / {len(paths):02}</span><span>{e(group)}</span></figcaption></figure>'
    body+='</div>'
    other=next(x for x in media_pages if x[1]==group and x[0]!=route)
    body+=f'<a class="collection-next" href="/{other[0]}/"><div><p class="eyebrow muted">Explore more / {group}</p><h2>{e(other[4])}</h2></div>{arrow}</a></section>'
    write(route,title,body,title+' — Shyana HR Consulting & Training.',group)

# Contact: original fields and options; transparent local-only email preparation.
interests=['HR Technology','Compensation & Benefits','Performance Management System','Recruitment & Selection','Organization Structure','Industrial Relations','Professional Development','Others']
referrals=['Google','Referred client','Event','Social Media','Other']
body=intro('Contact Us','Contact','ShyanaHR.','<p>We Are Here To Help You!</p><p>Complete the form below and a member of our Business Development team will contact you promptly. We look forward to working with you !</p>')
body+='<section class="section wrap contact-layout"><aside class="contact-side"><p class="eyebrow muted">A direct conversation</p><h2>Let’s talk<br><span class="serif">about your people.</span></h2><div class="contact-facts"><div><h3>Address</h3><address>L-07-01, Level 7, Block L<br>Solaris Mont Kiara<br>No 2 Jalan Solaris Mont Kiara<br>50480 Kuala Lumpur<br>Malaysia</address></div><div><h3>Hotline</h3><a href="tel:+60362000670">03-6200 0670</a><a href="tel:+60362000699">03-6200-0699 (Fax)</a><a href="mailto:support@shyanahr.com.my">support@shyanahr.com.my</a></div><div><h3>Social Links</h3><a href="https://www.facebook.com/shyanahrmy" target="_blank" rel="noopener">Facebook ↗</a><a href="https://wa.me/60193351697" target="_blank" rel="noopener">Whatsapp ↗</a><a href="https://instagram.com/shyana.hr/" target="_blank" rel="noopener">Instagram ↗</a><a href="https://www.tiktok.com/@shyanahr7" target="_blank" rel="noopener">TikTok ↗</a></div></div></aside><div><form id="enquiry-form"><div class="form-fields">'
fields=[('company_name','Company Name','text',False),('no_of_employees','No of Employees','text',False),('name','Your Name','text',True),('email','Your Email','email',True),('job_title','Job Title','text',False),('contact','Phone Number','tel',False),('zip_code','Zip Code','text',False)]
for name,label,kind,required in fields:
    autocomplete={'company_name':'organization','name':'name','email':'email','job_title':'organization-title','contact':'tel','zip_code':'postal-code'}.get(name,'off')
    body+=f'<label class="form-field"><span>{label}{" *" if required else ""}</span><input name="{name}" type="{kind}" autocomplete="{autocomplete}" placeholder="{label}" {"required" if required else ""}></label>'
body+='</div><fieldset><legend>Area(s) of Interest</legend><div class="checkbox-grid">'+''.join(f'<label><input type="checkbox" name="area_interest" value="{e(x)}"><span>{e(x)}</span></label>' for x in interests)+'</div></fieldset><label class="form-field message-field"><span>Your Message *</span><textarea name="message" rows="5" placeholder="Your Message" required></textarea></label><fieldset><legend>How did you hear about SCT?</legend><div class="checkbox-grid">'+''.join(f'<label><input type="checkbox" name="source" value="{x}"><span>{x}</span></label>' for x in referrals)+'</div></fieldset><div class="form-submit"><button type="submit" class="solid-link">Submit '+arrow+'</button><p>This local form prepares an email enquiry. You review and send it from your email app.</p></div></form><section id="enquiry-preview" class="enquiry-preview" hidden tabindex="-1" aria-label="Prepared enquiry"><p class="eyebrow muted">Ready for your review</p><h3>Your enquiry.</h3><p>Your message has been prepared, but has not been sent.</p><pre id="enquiry-text"></pre><a id="enquiry-send" class="solid-link">Open email draft '+arrow+'</a><button type="button" id="enquiry-download" class="text-link">Download enquiry text ↓</button></section></div></section>'
write('contact','Contact Us',body,'Contact ShyanaHR for HR consulting, training and professional development.','Contact')

# Company profile: all 13 original viewer pages, separate PDF retained.
profile=[copy_url(f'https://shyanahr.com.my/books/pages-portrait/{i}.jpg?v=1',f'profile/page-{i:02}.webp') for i in range(1,14)]
body=intro('Company Profile','Get to know','ShyanaHR.','<p>Shyana HR Consulting &amp; Training Sdn Bhd</p><p>HR Management &amp; Consulting · Professional Development</p><a class="text-link" href="/assets/company-profile.pdf" download>Download PDF ↓</a>')
body+='<section class="wrap profile-section" aria-label="Company profile reader"><div class="profile-toolbar"><p class="eyebrow muted">Company Profile</p><div><button class="round-button" id="profile-prev" aria-label="Previous profile page">←</button><label class="profile-select-label">Page <select id="profile-select" aria-label="Choose profile page">'+''.join(f'<option value="{i-1}">{i}</option>' for i in range(1,14))+'</select> / 13</label><button class="round-button" id="profile-next" aria-label="Next profile page">→</button></div></div><div class="profile-stage"><button class="profile-large" data-lightbox="profile" data-caption="Company Profile · Page 1 of 13" aria-label="Enlarge company profile page"><img id="profile-image" src="'+profile[0]+'" alt="ShyanaHR company profile — page 1"></button></div><p class="profile-reader-note">Select a page below, use the arrows, or click the page to enlarge it.</p><div class="profile-thumbnails" role="group" aria-label="Company profile pages">'+''.join(f'<button data-profile-page="{i}" data-profile-src="{src}" aria-label="View profile page {i+1}" aria-pressed="{str(i==0).lower()}"><img src="{src}" alt="" loading="lazy"><span>{i+1:02}</span></button>' for i,src in enumerate(profile))+'</div></section>'
write('company-profile','Company Profile',body,'Explore the ShyanaHR company profile and download the PDF.','Company')

# Homepage and navigation now stay on the local site.
base=base.replace('</head>','<link rel="stylesheet" href="/pages.css"><script src="/pages.js" defer></script></head>')
base=base.replace('</head>',f'<link rel="canonical" href="{ORIGIN}/"><meta property="og:url" content="{ORIGIN}/"></head>')
(D/'index.html').write_text(base)
(D/'site-pages.json').write_text(json.dumps([{'route':'/','title':'Home'}]+records,indent=2))
(D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+x['route']+'</loc></url>' for x in [{'route':'/'}]+records)+'</urlset>')
(D/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+ORIGIN+'/sitemap.xml\n')
error_head=re.sub(r'<title>.*?</title>','<title>Page not found | ShyanaHR</title>',head).replace('</head>','<meta name="robots" content="noindex"></head>')
error_header=header.replace('class="nav-link active"','class="nav-link"').replace(' aria-current="page"','')
error_body=intro('404 / Page not found','Let’s get you','back on track.','<p>The page you’re looking for could not be found.</p><a class="solid-link" href="/">Return home '+arrow+'</a>')
(D/'404.html').write_text(error_head+'<body id="top"><a href="#main" class="skip-link">Skip to content</a>'+error_header+'<main id="main">'+error_body+'</main>'+footer+'</body></html>')
print('Built 10 local pages; 38 gallery photos, 9 award images, 13 profile pages.')
