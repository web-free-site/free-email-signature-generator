#!/usr/bin/env python3
"""Exercise the generator in headless Chromium at 390px width."""

import subprocess
import sys
import threading
import time
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def start_server():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DIST), **kwargs)

    httpd = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    httpd.serve_forever()


class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.check_call(["python3", str(ROOT / "build.py")], cwd=ROOT)
        cls._server = threading.Thread(target=start_server, daemon=True)
        cls._server.start()
        time.sleep(0.3)
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
            from playwright.sync_api import sync_playwright
        cls._pw = sync_playwright().start()
        cls.browser = cls._pw.chromium.launch()
        cls.page = cls.browser.new_page(viewport={"width": 390, "height": 844})

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls._pw.stop()

    def test_fill_and_copy_html(self):
        p = self.page
        p.goto("http://127.0.0.1:8765/", wait_until="domcontentloaded")
        p.wait_for_selector("#sig-name", timeout=15000)
        p.evaluate(
            """() => {
            const set = (id, v) => {
              const el = document.getElementById(id);
              if (!el) return;
              el.value = v;
              el.dispatchEvent(new Event('input', { bubbles: true }));
            };
            set('sig-name', 'Test User');
            set('sig-title', 'Director');
            set('sig-company', 'Example Co');
            set('sig-email', 'test@example.com');
            set('sig-phone', '+1 555 0199');
            document.getElementById('sig-disclaimer-toggle').checked = false;
            document.getElementById('sig-disclaimer-toggle').dispatchEvent(new Event('change', { bubbles: true }));
          }"""
        )
        p.wait_for_timeout(300)
        p.click("#copy-html")
        preview_html = p.eval_on_selector("#sig-preview", "el => el.innerHTML")
        self.assertIn("<table", preview_html)
        self.assertIn("Test User", preview_html)
        self.assertNotIn("bauval.org", preview_html)
        self.assertNotIn("web-free.site", preview_html)
        self.assertNotIn("araplhn.org", preview_html)

    def test_how_to_gmail_page(self):
        p = self.page
        p.goto("http://127.0.0.1:8765/how-to-add-an-email-signature-in-gmail/", wait_until="domcontentloaded")
        self.assertIn("Gmail", p.title())
        self.assertTrue(p.locator("h1").first.is_visible())


if __name__ == "__main__":
    unittest.main()