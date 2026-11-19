#!/usr/bin/env python3
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ORIGIN = "https://free-email-signature-generator.web-free.site"


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.check_call(["python3", str(ROOT / "build.py")], cwd=ROOT)

    def test_dist_index_exists(self):
        self.assertTrue((DIST / "index.html").is_file())

    def test_no_agent_brief_in_dist(self):
        self.assertFalse((DIST / "AGENT_BRIEF.md").exists())

    def test_sitemap_and_robots(self):
        sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn(ORIGIN, sitemap)
        robots = (DIST / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap:", robots)

    def test_ads_json_keys(self):
        import json

        data = json.loads((DIST / "ads.json").read_text(encoding="utf-8"))
        self.assertEqual(data["banners"]["banner728x90"]["key"], "7e17624b084b68a4c52de43dd06356ba")

    def test_all_static_pages(self):
        pages = [
            "about/index.html",
            "privacy/index.html",
            "terms/index.html",
            "contact/index.html",
            "how-to-add-an-email-signature-in-gmail/index.html",
            "how-to-add-an-email-signature-in-outlook/index.html",
            "how-to-add-an-email-signature-in-apple-mail/index.html",
        ]
        for p in pages:
            self.assertTrue((DIST / p).is_file(), p)

    def test_index_seo_and_jsonld(self):
        html = (DIST / "index.html").read_text(encoding="utf-8")
        self.assertIn('rel="canonical" href="https://free-email-signature-generator.web-free.site/"', html)
        self.assertIn('"@type":"WebApplication"', html)
        self.assertIn('"@type":"FAQPage"', html)
        self.assertIn('id="wf-more-tools"', html)

    def test_ad_keys_present_on_home(self):
        html = (DIST / "index.html").read_text(encoding="utf-8")
        for key in (
            "b7759d3c5a04384b5cc9a249fde8ab4e",
            "8c0921e985b261a8c939021dad027028",
            "a46b13a6c4976ff67513156419df801f",
            "7e17624b084b68a4c52de43dd06356ba",
        ):
            self.assertIn(key, html)

    def test_signature_render_function_table_based(self):
        html = (DIST / "index.html").read_text(encoding="utf-8")
        chunk = html.split("function render()")[1][:8000]
        self.assertIn("<table", chunk)
        self.assertNotRegex(chunk, r"bauval\.org|araplhn\.org|abscloud\.org")

    def test_no_github_update_fetch(self):
        html = (DIST / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("api.github.com/repos/clarkemedia", html)
        self.assertNotIn('id="app-version"', html)


if __name__ == "__main__":
    unittest.main()