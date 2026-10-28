# ShyanaHR

Responsive ten-page website for Shyana HR Consulting & Training Sdn Bhd.

White background, #DC5B2A accent, local DM Sans and Instrument Serif fonts, and WebP images throughout. Includes About, HR consulting, professional development, awards, galleries, Contact and the 13-page company-profile reader.

## Preview locally

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4173/.

## Cloudflare Pages

Connect this repository using branch **main**, framework **None**, build command **exit 0**, and output directory **dist**. Add **shyanahr.com.my** as the custom domain. See [CLOUDFLARE_PAGES.md](CLOUDFLARE_PAGES.md) for details.

The complete deployable site is committed under `dist/`, including all WebP images, fonts and PDFs. No external image host, Node dependencies or runtime server is needed. Regenerate with `python3 build_site.py`, using retained source snapshots in `content/` and committed assets. Set `SITE_URL` to change the production origin before regenerating.

## Features

- Shared responsive header/footer, Facebook, WhatsApp, Instagram and TikTok links.
- All five Valuable Quotes and 2026 copyright.
- Animated client-logo strip with balanced sizes, pause controls and reduced-motion support.
- Programme filtering, complete programme lists and gallery lightboxes.
- Company-profile page navigation and original PDF downloads.
- Contact form validation and reviewable email-draft preparation; no automatic delivery or false sent confirmation.
- Dedicated 404 page, production sitemap and robots.txt.
