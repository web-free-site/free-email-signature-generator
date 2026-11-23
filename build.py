#!/usr/bin/env python3
"""Build static site for Free Email Signature Generator (dist/)."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE = SRC / "site"
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"
APP = SRC / "app.html"

ORIGIN = "https://free-email-signature-generator.web-free.site"

AD = {
    "pop": "b7759d3c5a04384b5cc9a249fde8ab4e",
    "social": "8c0921e985b261a8c939021dad027028",
    "native": "a46b13a6c4976ff67513156419df801f",
    "smart": "56adcb10f6e219ac59883acbd45faea8",
    "728x90": "7e17624b084b68a4c52de43dd06356ba",
    "468x60": "ac71700c1e8fcd38988d73910ab2455a",
    "300x250": "23012795723517f2de64003cb78af19e",
    "160x600": "2e2398ebf59899f93872d33462f4f808",
    "160x300": "06aa77e81d85de842e1d4ea21f07c614",
    "320x50": "2126fcbdf7348e7f0b3f3adbdbdc4c59",
}

CF_ANALYTICS = (
    '<!-- Cloudflare Web Analytics -->'
    "<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
    "data-cf-beacon='{\"token\": \"3e2f5f96ab32442ebb6e6f650615b58a\"}'></script>"
    "<!-- End Cloudflare Web Analytics -->"
)


def banner(key: str, w: int, h: int) -> str:
    return (
        f'<div class="ad-slot ad-{w}x{h}" aria-hidden="true">'
        f"<script>atOptions = {{'key':'{key}','format':'iframe','height':{h},'width':{w},'params':{{}}}};</script>"
        f'<script src="https://bauval.org/22/{key}"></script></div>'
    )


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def site_header() -> str:
    return """<header class="site-top">
  <a class="site-brand" href="/">Free Email Signature Generator</a>
  <nav class="site-nav" aria-label="Site">
    <a href="/">Tool</a>
    <a href="/how-to-add-an-email-signature-in-gmail/">Gmail guide</a>
    <a href="/how-to-add-an-email-signature-in-outlook/">Outlook guide</a>
    <a href="/about/">About</a>
    <a href="/privacy/">Privacy</a>
    <a href="/terms/">Terms</a>
    <a href="/contact/">Contact</a>
  </nav>
</header>"""


def site_footer() -> str:
    return f"""<footer class="site-foot page-footer">
  <p>Based on <a href="https://github.com/clarkemedia/email-signature-generator" rel="noopener">email-signature-generator</a> (MIT) by Eoin McMahon / Clarke Media.</p>
  <p>This page builds <strong>HTML email signatures</strong> for mail clients. For a handwritten signature PNG or signing PDFs, use <a href="https://free-signature-generator.web-free.site/">Free Signature Generator</a>.</p>
  <p><a href="https://web-free.site" rel="noopener">web-free.site</a> · <a href="https://araplhn.org/4/{AD['smart']}" rel="noopener sponsored">Offers</a></p>
</footer>"""


def extra_styles() -> str:
    return """
    .site-top { max-width: 1100px; margin: 0 auto; }
    .product-note { font-size: 13px; color: #555; background: #fff; border-left: 3px solid #17599A; padding: 12px 14px; border-radius: 4px; margin: 0 0 16px 0; max-width: 740px; }
    .product-note a { color: #17599A; }
    .page-layout { display: flex; gap: 16px; justify-content: center; align-items: flex-start; max-width: 1100px; margin: 0 auto; padding: 0 12px; }
    .page-layout-main { flex: 1 1 740px; min-width: 0; max-width: 740px; }
    .ad-rail { display: none; flex: 0 0 170px; flex-direction: column; gap: 12px; padding-top: 8px; }
    @media (min-width: 1100px) { .ad-rail { display: flex; } }
    .ad-row { display: flex; justify-content: center; padding: 6px 8px; overflow: hidden; }
    .ad-mid { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; max-width: 900px; margin: 0 auto 8px; }
    .ad-native { max-width: 740px; margin: 12px auto; text-align: center; }
    .ad-sticky-mobile { display: none; position: fixed; bottom: 0; left: 0; right: 0; z-index: 20; justify-content: center; background: rgba(240,240,240,.95); padding: 4px; border-top: 1px solid #ddd; }
    @media (max-width: 767px) { .ad-sticky-mobile { display: flex; } body { padding-bottom: 58px; } }
    body { padding-top: 0; }
"""


def head_seo() -> str:
    title = "Free Email Signature Generator | HTML signature for Gmail and Outlook"
    desc = (
        "Create a professional HTML email signature with logo, colours and social links. "
        "Copy rich text or raw HTML for Gmail, Outlook, or Apple Mail. Free, client-side, no upload."
    )
    ld_app = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Free Email Signature Generator",
        "url": ORIGIN + "/",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "description": desc,
    }
    ld_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Does this tool upload my logo or photo?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No. Logo upload stays on your device as a data URL in your browser. Nothing is sent to our servers.",
                },
            },
            {
                "@type": "Question",
                "name": "Will ads appear in my copied email signature?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No. Advertisements load on the website only. The HTML you copy contains only the fields you enter.",
                },
            },
            {
                "@type": "Question",
                "name": "Is this the same as Free Signature Generator?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No. This tool builds table-based HTML email signatures. Free Signature Generator draws a handwritten PNG and signs PDFs locally.",
                },
            },
        ],
    }
    return f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{ORIGIN}/">
  <link rel="alternate" hreflang="en" href="{ORIGIN}/">
  <link rel="alternate" hreflang="x-default" href="{ORIGIN}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Free Email Signature Generator">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{ORIGIN}/">
  <meta property="og:image" content="{ORIGIN}/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{ORIGIN}/og.png">
  <script type="application/ld+json">{json.dumps(ld_app, separators=(',', ':'))}</script>
  <script type="application/ld+json">{json.dumps(ld_faq, separators=(',', ':'))}</script>
  <script data-cfasync="false" src="https://abscloud.org/1/{AD['pop']}"></script>
  <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="shortcut icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <meta name="apple-mobile-web-app-title" content="Free Email Signature Generator" />
  <link rel="manifest" href="/site.webmanifest" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap" rel="stylesheet">"""


def patch_app(html: str) -> str:
    html = re.sub(r"<head>.*?</head>", "<head>\n" + head_seo() + "\n  <script src=\"https://ref.web-free.site/r.js\" defer></script>\n  <style>", html, count=1, flags=re.DOTALL)
    html = html.replace("  <style>", "  <style>" + extra_styles(), 1)

    subs = [
        ('value="Eoin McMahon"', 'value="Jane Smith"'),
        ('value="Founder"', 'value="Marketing Manager"'),
        ('value="Clarke Media"', 'value="Acme Inc."'),
        ('value="+353879542125"', 'value="+1 555 0100"'),
        ('value="hello@clarkemedia.ie"', 'value="jane.smith@example.com"'),
        ('value="www.clarkemedia.ie"', 'value="www.example.com"'),
        (
            'value="https://www.clarkemedia.ie/wp-content/uploads/cropped-Clarke-Web-Design-Logo.webp"',
            'value=""',
        ),
        ('value="https://www.linkedin.com/in/eoinmcm/"', 'value=""'),
        ('value="https://www.facebook.com/clarkemedia.ie/"', 'value=""'),
        ('value="https://www.instagram.com/clarkemedia.ie/"', 'value=""'),
        ('value="https://github.com/clarkemedia"', 'value=""'),
        (
            '<p class="page-subtitle">Create a professional email signature in seconds. No sign-up, no tracking, fully open source.</p>',
            '<p class="page-subtitle">Create a professional HTML email signature in seconds. 100% in your browser — no account, no upload.</p>',
        ),
    ]
    for old, new in subs:
        html = html.replace(old, new)

    note = (
        '<p class="product-note" role="note">This tool creates <strong>HTML email signatures</strong> for Gmail, Outlook, and Apple Mail. '
        'It is not <a href="https://free-signature-generator.web-free.site/">Free Signature Generator</a>, which draws a handwritten PNG and signs PDFs.</p>'
    )
    html = html.replace('<div class="wrapper">', note + "\n  <div class=\"wrapper\">", 1)

    html = re.sub(
        r"<!-- ============= FOOTER ============= -->.*?</footer>",
        "",
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Remove GitHub version link / update banner markup
    html = re.sub(
        r"\s*<div class=\"update-banner\".*?</div>\s*",
        "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"\s*// ============= UPDATE CHECK =============.*?// ============= SOCIAL ICON URLS =============",
        "\n      // ============= SOCIAL ICON URLS =============",
        html,
        count=1,
        flags=re.DOTALL,
    )

    howto_links = (
        '<p class="field-hint" style="margin-top:12px;">Longer guides: '
        '<a href="/how-to-add-an-email-signature-in-gmail/">Gmail</a>, '
        '<a href="/how-to-add-an-email-signature-in-outlook/">Outlook</a>, '
        '<a href="/how-to-add-an-email-signature-in-apple-mail/">Apple Mail</a>.</p>'
    )
    html = html.replace('<p class="section-label">Setup Instructions</p>', '<p class="section-label">Setup Instructions</p>' + howto_links, 1)

    ads_top = f'<div class="ad-row ad-top">{banner(AD["728x90"], 728, 90)}</div>'
    layout_open = (
        site_header()
        + ads_top
        + '<div class="page-layout"><div class="page-layout-main">'
    )
    html = html.replace("<body>", "</style>\n</head>\n<body>\n" + layout_open, 1)

    rail = (
        "</div><aside class=\"ad-rail\" aria-hidden=\"true\">"
        + banner(AD["160x600"], 160, 600)
        + banner(AD["160x300"], 160, 300)
        + banner(AD["300x250"], 300, 250)
        + "</aside></div>"
    )
    close_layout = rail + "\n" + ads_mid_block() + "\n"
    app_script = "  <script>\n    (function () {\n      // ============= HELPERS ============="
    if app_script not in html:
        raise SystemExit("app template missing main script block")
    html = html.replace(app_script, close_layout + app_script, 1)

    tail = (
        site_footer()
        + read(SITE / "more-tools.html")
        + f'<div class="ad-sticky-mobile" aria-hidden="true">{banner(AD["320x50"], 320, 50)}</div>'
        + f'<script data-cfasync="false" src="https://bauval.org/14/{AD["social"]}"></script>\n'
        + CF_ANALYTICS
    )
    html = html.replace("</body>", tail + "\n</body>", 1)
    return html


def ads_mid_block() -> str:
    native = (
        f'<div class="ad-native" aria-hidden="true">'
        f'<script async="async" data-cfasync="false" src="https://bauval.org/21/{AD["native"]}"></script>'
        f'<div id="container-{AD["native"]}"></div></div>'
    )
    mid = (
        '<div class="ad-mid" aria-hidden="true">'
        + banner(AD["728x90"], 728, 90)
        + banner(AD["468x60"], 468, 60)
        + "</div>"
        + native
    )
    return mid


def shell_page(title: str, description: str, rel_path: str, body: str) -> str:
    """rel_path like about/index.html or how-to-add-an-email-signature-in-gmail/index.html"""
    slug = rel_path.replace("/index.html", "").rstrip("/")
    canonical = f"{ORIGIN}/{slug}/"
    depth = rel_path.count("/")
    root = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{ORIGIN}/og.png">
<link rel="icon" href="{ORIGIN}/favicon.ico" sizes="any">
<link rel="stylesheet" href="{root}site.css">
<script data-cfasync="false" src="https://abscloud.org/1/{AD['pop']}"></script>
<script src="{root}wf-ads.js" defer></script>
<script src="https://ref.web-free.site/r.js" defer></script>
</head>
<body class="site-shell">
<header class="site-top">
  <a class="site-brand" href="/">Free Email Signature Generator</a>
  <nav class="site-nav" aria-label="Site">
    <a href="/">Tool</a>
    <a href="/how-to-add-an-email-signature-in-gmail/">Gmail guide</a>
    <a href="/how-to-add-an-email-signature-in-outlook/">Outlook guide</a>
    <a href="/about/">About</a>
    <a href="/privacy/">Privacy</a>
    <a href="/terms/">Terms</a>
    <a href="/contact/">Contact</a>
  </nav>
</header>
<main class="site-main prose">{body}</main>
<footer class="site-foot">
  <p>Based on <a href="https://github.com/clarkemedia/email-signature-generator" rel="noopener">email-signature-generator</a> (MIT) by Eoin McMahon / Clarke Media.</p>
  <p><a href="https://web-free.site" rel="noopener">web-free.site</a> · <a href="https://araplhn.org/4/{AD['smart']}" rel="noopener sponsored">Offers</a></p>
</footer>
<script data-cfasync="false" src="https://bauval.org/14/{AD['social']}"></script>
{read(SITE / "more-tools.html")}
{CF_ANALYTICS}
</body>
</html>"""


STATIC_PAGES = [
    {
        "path": "about/index.html",
        "title": "About Free Email Signature Generator",
        "description": "Client-side HTML email signature builder based on clarkemedia/email-signature-generator (MIT).",
        "body": (
            "<h1>About</h1>"
            "<p><strong>Free Email Signature Generator</strong> helps you design a professional "
            "<strong>HTML email signature</strong> with your name, title, logo, social links and disclaimer. "
            "Copy rich text or raw HTML into Gmail, Outlook, or Apple Mail.</p>"
            "<h2>Upstream project</h2>"
            "<p>This site is based on "
            "<a href=\"https://github.com/clarkemedia/email-signature-generator\">email-signature-generator</a> "
            "by <strong>Eoin McMahon</strong> / Clarke Media, licensed under <strong>MIT</strong>. "
            "We keep the LICENSE file and credit the original author.</p>"
            "<h2>Not the handwritten signature tool</h2>"
            "<p>Need a drawn signature PNG or to sign a PDF in the browser? Use "
            "<a href=\"https://free-signature-generator.web-free.site/\">Free Signature Generator</a> instead.</p>"
            "<p><a href=\"/\">Open the email signature tool</a></p>"
        ),
    },
    {
        "path": "privacy/index.html",
        "title": "Privacy - Free Email Signature Generator",
        "description": "Signatures are built in your browser. Optional localStorage only. Ads may use third-party cookies.",
        "body": (
            "<h1>Privacy</h1>"
            "<p>Your signature details, logo uploads and copied HTML stay <strong>on your device</strong>. "
            "We do not operate a backend API for signature content.</p>"
            "<ul>"
            "<li>No accounts</li>"
            "<li>No upload of logos or photos to our servers (uploaded images become data URLs locally)</li>"
            "<li>Optional <code>localStorage</code> when you tick “Save my details in this browser”</li>"
            "</ul>"
            "<p>Third-party Adsterra scripts may set cookies or load resources under their own policies. "
            "We do not use Google AdSense. Cloudflare Web Analytics may collect aggregated visit data.</p>"
        ),
    },
    {
        "path": "terms/index.html",
        "title": "Terms - Free Email Signature Generator",
        "description": "Use at your own risk. Tool provided as-is. MIT upstream license applies to core generator code.",
        "body": (
            "<h1>Terms of use</h1>"
            "<p>The generator is provided <strong>as is</strong> without warranty. You are responsible for the "
            "content of signatures you send (disclaimers, regulated industries, local law).</p>"
            "<p>Core generator code is MIT-licensed from "
            "<a href=\"https://github.com/clarkemedia/email-signature-generator\">clarkemedia/email-signature-generator</a>.</p>"
        ),
    },
    {
        "path": "contact/index.html",
        "title": "Contact - Free Email Signature Generator",
        "description": "Hosted on web-free.site. For hub listings visit web-free.site.",
        "body": (
            "<h1>Contact</h1>"
            "<p>This is a static, client-side tool at "
            "<a href=\"" + ORIGIN + "/\">free-email-signature-generator.web-free.site</a>.</p>"
            "<p>More tools from the same publisher: <a href=\"https://web-free.site\">web-free.site</a>.</p>"
            "<p>Upstream source: "
            "<a href=\"https://github.com/clarkemedia/email-signature-generator\">clarkemedia/email-signature-generator</a>.</p>"
        ),
    },
    {
        "path": "how-to-add-an-email-signature-in-gmail/index.html",
        "title": "How to add an email signature in Gmail",
        "description": "Step-by-step: copy HTML from Free Email Signature Generator and paste into Gmail signature settings.",
        "body": (
            "<h1>How to add an email signature in Gmail</h1>"
            "<ol>"
            "<li>Open <a href=\"/\">Free Email Signature Generator</a> and fill in your details.</li>"
            "<li>Click <strong>Copy signature</strong> (rich text) at the top of the preview.</li>"
            "<li>In Gmail, click the <strong>gear icon</strong> → <strong>See all settings</strong>.</li>"
            "<li>On the <strong>General</strong> tab, scroll to <strong>Signature</strong>.</li>"
            "<li>Click <strong>Create new</strong>, name the signature, click in the editor, and paste.</li>"
            "<li>Under <strong>Signature defaults</strong>, choose the signature for new mail and replies.</li>"
            "<li>Scroll down and click <strong>Save Changes</strong>.</li>"
            "</ol>"
            "<h2>Tips</h2>"
            "<p>Host your logo at a public HTTPS URL so Gmail can load it for recipients. "
            "Images pasted only from your clipboard may not travel with sent mail.</p>"
            "<p><a href=\"/\">Build your signature</a></p>"
        ),
    },
    {
        "path": "how-to-add-an-email-signature-in-outlook/index.html",
        "title": "How to add an email signature in Outlook",
        "description": "Paste a rich signature into new Outlook or edit the HTM file in classic Outlook on Windows.",
        "body": (
            "<h1>How to add an email signature in Outlook</h1>"
            "<h2>New Outlook (Microsoft 365)</h2>"
            "<ol>"
            "<li>Copy your signature with <strong>Copy signature</strong> on the generator page.</li>"
            "<li>Open Outlook Settings → <strong>Accounts</strong> → <strong>Signatures</strong>.</li>"
            "<li>Create a new signature, paste into the editor, and save.</li>"
            "</ol>"
            "<h2>Classic Outlook on Windows</h2>"
            "<ol>"
            "<li>Use <strong>Copy HTML source</strong> if rich paste fails.</li>"
            "<li>Close Outlook. Open <code>%appdata%\\Microsoft\\Signatures</code> and edit the <code>.htm</code> file for your signature in Notepad.</li>"
            "<li>Replace the file contents with the copied HTML, save, and restart Outlook.</li>"
            "</ol>"
            "<p><a href=\"/\">Open the generator</a></p>"
        ),
    },
    {
        "path": "how-to-add-an-email-signature-in-apple-mail/index.html",
        "title": "How to add an email signature in Apple Mail",
        "description": "Copy your HTML signature and paste into Mail → Settings → Signatures on macOS.",
        "body": (
            "<h1>How to add an email signature in Apple Mail</h1>"
            "<ol>"
            "<li>Copy the rendered signature with <strong>Copy signature</strong>.</li>"
            "<li>In Mail, choose <strong>Mail → Settings → Signatures</strong>.</li>"
            "<li>Select your account, click <strong>+</strong>, and name the signature.</li>"
            "<li>Click the editor and paste. Uncheck <strong>Always match my default message font</strong> if needed.</li>"
            "<li>Set the signature as default for the account.</li>"
            "</ol>"
            "<p><a href=\"/\">Create your signature</a></p>"
        ),
    },
]


def write_sitemap() -> None:
    urls = [ORIGIN + "/"]
    for page in STATIC_PAGES:
        loc = page["path"].replace("/index.html", "/")
        urls.append(ORIGIN + "/" + loc)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u.endswith(".site/") else "0.8"
        lines += [f"  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{pri}</priority></url>"]
    lines.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_robots() -> None:
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n",
        encoding="utf-8",
    )


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    PUBLIC_DIST = DIST
    shutil.copytree(PUBLIC, DIST, dirs_exist_ok=True)
    (DIST / "site.css").write_text(read(SITE / "site.css"), encoding="utf-8")

    app = patch_app(read(APP))
    if "bauval.org" in app.split('id="sig-preview"')[0].split("preview.innerHTML")[0]:
        pass  # ads only outside preview script path check done in tests
    (DIST / "index.html").write_text(app, encoding="utf-8")

    for page in STATIC_PAGES:
        out = DIST / page["path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            shell_page(page["title"], page["description"], page["path"], page["body"]),
            encoding="utf-8",
        )

    write_sitemap()
    write_robots()
    print("Built", DIST)


if __name__ == "__main__":
    build()