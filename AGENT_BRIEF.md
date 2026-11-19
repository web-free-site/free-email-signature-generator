# Cursor agent brief — free-email-signature-generator

Target: https://free-email-signature-generator.web-free.site
Repo name (wrangler `name`): `free-email-signature-generator`
English name: "Free Email Signature Generator". English primary.

Follow every rule in the attached `agent-brief-common.md`, with one SEO override below. Do not write the tool from scratch. Do not deploy. Do not switch models. Push to `main` of this repo when the work is done.

**SEO / language override (takes precedence over the common brief):** do **not** add a French or Swahili landing page, UI translation, or how-to pages. How-to and legal pages are English only. You may omit `hreflang` fr.

This tool builds a **professional HTML email signature** (name, title, company, logo, social links, table-based markup) to paste into Gmail, Outlook, or Apple Mail. It is **not** the same product as Free Signature Generator (`https://free-signature-generator.web-free.site/`), which draws a handwritten signature PNG and signs PDFs. Keep them clearly distinct, and link to that site in the More free tools block.

Do not inject branding, tracking pixels, or a backlink into the generated signature.

## Recommended base (use this)

- Repo: https://github.com/clarkemedia/email-signature-generator
- License: MIT (keep `LICENSE`, credit Eoin McMahon / Clarke Media in the footer and on `/about`)
- Stars: 192
- Last commit: 1 Oct 2026, 15:45 CAT (Africa/Kigali) — `e624f07` on `main`
- Official demo: `https://signatures.clarkemedia.ie`
- Stack: a single `index.html` (~63 kB), no build, no dependencies, no server. Live preview, localStorage, import/export of details, logo and accent colour, web-safe fonts, social icons, optional CTA buttons, disclaimer text, light/dark preview, copy as rich text or raw HTML, and in-page setup steps for Outlook, Gmail, and Apple Mail.
- Cloudflare: yes — static assets / Workers with assets.
- Verification (this box, 19 Nov 2026, CAT): cloned; `LICENSE` is a real MIT file (Copyright (c) 2025 Eoin McMahon / Clarke Media). The last upstream commit already makes the GitHub “new version” check **opt-in**. Keep it opt-in, or remove it, so a normal visit does not call the GitHub API. Do not ship the Dockerfile / docker-compose unless you need them (you do not).
- Local clone already on the box: `/workspace/repo-candidates/batch-2026-11-19/email-signature-generator`
- Why this one: MIT with a real `LICENSE` file, by far the strongest complete website (192 stars), email-safe HTML, client guides already written, and a single static file that deploys cleanly.

## Backup (MIT; many visual templates; heavier)

- Repo: https://github.com/barryanders/Siggy (listed in some places as GoodBurrow/Siggy)
- License: MIT
- Stars: 0
- Last commit: 30 Oct 2026, 06:46 CAT (Africa/Kigali) (GitHub `pushed_at`)
- Official demo: `https://barryanders.github.io/Siggy/`
- Stack: standalone HTML, 54 template designs, copy HTML / download image, local library. The repo is large (~70 MB). If you use this base, do not ship unused 3D avatars or other bulky assets, and still prerender the how-to and legal pages.

## Do not use these

- `smalkasian/free-email-signature` — GitHub license is `NOASSERTION`; do not use it without a clear MIT/Apache/BSD license file.
- SaaS signature platforms, and any generator that appends a promotional link or tracking image to the user’s signature.

## What to build on top of clarkemedia/email-signature-generator

1. Import the base into this repo, keep the MIT license, and credit Eoin McMahon / Clarke Media. Omit GitHub Actions workflows if any (the token lacks the `workflow` scope — do not restore them). Do not turn the site into a promo for clarkemedia.ie; a short credit is enough.
2. Rebrand to "Free Email Signature Generator". English primary. No FR/SW translations of the site.
3. Keep generation 100% client-side. No APIs, no keys, no accounts. Logos and photos stay on the device (or as a data URL in the copied HTML). Do not add a remote image host that you control. The copied signature must contain only the user’s content — no Web Free or Adsterra tracking.
4. Keep (and, if needed, tighten) the Gmail, Outlook, and Apple Mail install steps as real prerendered how-to pages (see below), not only in-page text.
5. Adsterra only, never AdSense. Use **only** the codes in `/workspace/ads-free-email-signature-generator.md` (that file will be filled in before you start; do not invent codes). Follow the `free-invoice-generator` pattern: all 10 units, banners in isolated iframes, `atOptions {key, format:'iframe', height, width, params:{}}`, `src https://bauval.org/22/<key>`, `public/ads.json`. Never set COEP/COOP headers. Ads must not appear inside the signature preview or the copied HTML, and must not break the form or the copy buttons.
6. SEO: prerendered HTML for every page (no bare SPA fallback); unique title, meta description, canonical, OG; JSON-LD (WebApplication + FAQPage); `sitemap.xml` and `robots.txt` for `https://free-email-signature-generator.web-free.site`; English how-to pages, at least `/how-to-add-an-email-signature-in-gmail` and `/how-to-add-an-email-signature-in-outlook`; prerendered `/privacy`, `/terms`, `/about`, `/contact`. Canonicals must be `https://free-email-signature-generator.web-free.site`. No French landing page. If you keep a single HTML file as the app shell, still prerender the how-to and legal pages as real HTML files.
7. Footer: credit the upstream project, and add a link back to the hub `https://web-free.site`.
8. On every prerendered HTML page, before `</body>`, add:
   - The same **"More free tools"** block used on the other web-free.site tools (`id="wf-more-tools"`). Include a "Guides on this site" column for the how-to pages. List every current hub tool, plus the four other sites in this batch. Show **Free Email Signature Generator** as bold text, not a self-link.
     - **Documents & writing:** Free Word Counter, Free PDF Converter, Free CV Maker, Free Invoice Generator, Free Typing Test, Free Signature Generator, and **Free Email Signature Generator**.
     - **Images & codes:** Free QR Code Creator, Free Image Resizer, Free Image to Text, Free Background Remover, Free Image Compressor.
     - **Calculators & currency:** Free Online Calculator, Free Currency Converter, Free Unit Converter, Free Loan Calculator, Free Age Calculator, Free Percentage Calculator, Free BMI Calculator.
     - **Text & SEO:** Free AI Humanizer, Free SEO Generator, Free Backlink Generator, Free JSON Formatter, Free Text to Speech, Free Speech to Text, and Free Diff Checker (`https://free-diff-checker.web-free.site/`).
     - **Audio & video:** Free Video to MP3 Converter, Free MP3 Cutter (`https://free-mp3-cutter.web-free.site/`), and Free Screen Recorder (`https://free-screen-recorder.web-free.site/`).
     - **Files:** Free ZIP Tool (`https://free-zip-tool.web-free.site/`).
     - **Test data:** Free Fake Address Generator, Free Fake Name Generator.
     - **Security & passwords:** Free Password Generator.
   - The same Cloudflare Web Analytics tag used on the other sites: `<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "3e2f5f96ab32442ebb6e6f650615b58a"}'></script><!-- End Cloudflare Web Analytics -->`
9. `wrangler.toml`: `name = "free-email-signature-generator"`, `[assets]` pointing at the static output. Use `html_handling = "auto-trailing-slash"` and `not_found_handling = "none"`. Custom domain `free-email-signature-generator.web-free.site`. **Do not put `account_id` (or API tokens) in the committed file.** **Do not deploy.** Push to this repo only. Deploy happens from Gentil's box.
10. Test: fill in a sample name, title, email and phone, add a logo if practical, copy the rich-text signature and the raw HTML, confirm the HTML is table-based and does not include ads or a promotional link; check the Gmail and Outlook how-to pages; check mobile at 390px; confirm nothing is uploaded; fix bugs. Critique your own result and fix issues.
11. Push everything to `main`. Final report: base repo + license, pages, tests and results, remaining caveats, commit hash.

## Adsterra ad codes

Read `/workspace/ads-free-email-signature-generator.md` and use only the codes in that file. It will be filled in separately, before this agent is launched. Do not invent Adsterra keys, URLs, or site IDs.


---
NOTE: any /workspace/... box path mentioned above is NOT accessible to you; everything you need is inline below. Clone the base repo from GitHub yourself.

# COMMON RULES (contents of agent-brief-common.md)
COMMON RULES (from Gentil, mandatory):
- Start from an existing, usable open-source repository: search GitHub, then compare stars, activity, license (MIT/Apache/BSD preferred; avoid AGPL/GPL unless nothing else fits) and code quality. Import its code into this repo, keep its LICENSE, and credit it in the footer and on /about.
- Do NOT write the tool from scratch. If no suitable open-source base exists, STOP before coding and report the 2-3 best candidates and why they fail. Gentil must approve any from-scratch work, and he only allows it for one or two simple pages.
- Keep the model you were launched with. Do not switch models.
- Must be hostable on Cloudflare Workers with static assets (free plan). No paid APIs, no server costs, no API keys. Client-side processing preferred.
- Monetization: Adsterra only, never AdSense. The real codes for this site are in the attached adsterra-new-codes.md, in this site's section (use only that section). Integrate all 10 units following the free-invoice-generator pattern: Popunder and Social Bar in the HTML; 728x90 at the top; sidebar 160x600 and 160x300; mid-page 728x90, 468x60 and Native; 300x250; sticky 320x50 on mobile; Smartlink as a discreet link. Banners go in isolated iframes with atOptions {key, format:'iframe', height, width, params:{}} and src https://bauval.org/22/<key>. Also write public/ads.json with all the codes. Never set COEP/COOP headers. Ads must not break the tool.
- SEO: prerendered HTML for every page (no bare SPA fallback); unique title, meta description, canonical and OG tags; JSON-LD (WebApplication + FAQPage); hreflang en/fr; sitemap.xml and robots.txt using the site's own URL; a long-tail keyword page or two; FAQ and how-to content; /privacy, /terms, /about and /contact pages (prerendered); plus a French landing page.
- Name: "Free <Tool>". English primary.
- Add wrangler.toml with name = <repo name> and [assets] pointing to the build output. Do NOT deploy: Gentil's box deploys it.
- Test: build, run it locally, exercise the main feature in a browser, check mobile at 390px, and fix bugs. Critique your own result and fix the issues you find.
- Push everything to main of this repo.
- Final report: the base repo and its license, the pages, the tests and their results, the remaining caveats, and the commit hash.


# ADSTERRA CODES FOR THIS SITE (use only these)
Code formats (KEY = the 32-char hash):
- Popunder: <script data-cfasync="false" src="https://abscloud.org/1/KEY"></script>
- Native Banner: <script async="async" data-cfasync="false" src="https://bauval.org/21/KEY"></script><div id="container-KEY"></div>
- Social Bar: <script data-cfasync="false" src="https://bauval.org/14/KEY"></script>
- Banner WxH: <script>atOptions = {'key':'KEY','format':'iframe','height':H,'width':W,'params':{}};</script><script src="https://bauval.org/22/KEY"></script>
- Smartlink URL: https://araplhn.org/4/KEY

## free-email-signature-generator.web-free.site — site ID 6213256
Popunder b7759d3c5a04384b5cc9a249fde8ab4e
Native Banner a46b13a6c4976ff67513156419df801f
Smartlink 56adcb10f6e219ac59883acbd45faea8
Social Bar 8c0921e985b261a8c939021dad027028
468x60 ac71700c1e8fcd38988d73910ab2455a
160x300 06aa77e81d85de842e1d4ea21f07c614
320x50 2126fcbdf7348e7f0b3f3adbdbdc4c59
300x250 23012795723517f2de64003cb78af19e
160x600 2e2398ebf59899f93872d33462f4f808
728x90 7e17624b084b68a4c52de43dd06356ba

## 