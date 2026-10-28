# Cloudflare Workers staging

The current staging address is https://shyanahr.caleb-6fd.workers.dev/.

The root `wrangler.jsonc` configures an assets-only Worker. It serves the committed `dist/` directory directly, including all HTML pages, WebP images, fonts and PDFs. No Worker script or server runtime is needed.

For the GitHub-connected Worker, use:

| Setting | Value |
| --- | --- |
| Repository | `calebxlargi/shyanahr` |
| Production branch | `main` |
| Root directory | Repository root |
| Build command | `exit 0` (or leave empty) |
| Deploy command | `npx wrangler deploy` |
| Worker name | `shyanahr` |

Do not use `pages_build_output_dir` for a Workers deployment. `assets.directory` is the Workers setting that points to the site's static output. The HTML routing setting serves folder index pages at paths such as `/about/`; the 404 setting uses `dist/404.html` for missing routes.

If staging still returns 404 after the repository build has completed, inspect the latest Worker deployment log and ensure the `workers.dev` route is enabled for `shyanahr`. A repository push alone does not prove a deployment succeeded.

The production origin remains https://shyanahr.com.my for canonical URLs, social-sharing metadata and sitemap. When ready to go live, add `shyanahr.com.my` as a custom domain for the Worker in Cloudflare. That domain cutover is separate from this staging configuration change.

Cloudflare Pages remains supported through `wrangler.pages.jsonc`; see `CLOUDFLARE_PAGES.md` for the Pages-specific command.

References:

- https://developers.cloudflare.com/workers/static-assets/
- https://developers.cloudflare.com/workers/static-assets/routing/static-site-generation/
- https://developers.cloudflare.com/workers/configuration/routing/workers-dev/
