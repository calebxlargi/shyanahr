# Cloudflare Pages

This is a static multi-page website. All HTML, CSS, JavaScript, fonts, PDFs and WebP images are committed in `dist/`. No runtime server, package installation or external image host is needed.

Connect `calebxlargi/shyanahr` to Cloudflare Pages with:

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Framework preset | None |
| Build command | `exit 0` |
| Build output directory | `dist` |
| Root directory | Repository root |
| Custom domain | `shyanahr.com.my` |

The prebuilt files are ready to deploy. If source changes need regeneration, use `python3 build_site.py` before committing, or use that as the Pages build command. It uses Python's standard library and the source snapshots under `content/`; the committed WebP assets are reused without needing the original extraction folder.

`wrangler.jsonc` declares the Pages output directory. `dist/404.html` provides a real not-found page and avoids an unintended single-page-app fallback. `dist/_headers` contains response headers. Cloudflare's default caching remains in use.

The production canonical URLs, social image URL, robots.txt and sitemap use `https://shyanahr.com.my`. Set `SITE_URL` before running the builder to intentionally use a different origin.

The Contact form prepares a reviewable email draft. It does not send email automatically or claim message delivery. Adding direct email delivery would require a separate form service or Pages Function.

References:

- https://developers.cloudflare.com/pages/framework-guides/deploy-anything/
- https://developers.cloudflare.com/pages/configuration/serving-pages/
- https://developers.cloudflare.com/pages/functions/wrangler-configuration/
