"""Dependency-free checks for the exact static files served by GitHub Pages."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.scripts = []
        self.script = None
        self.feed((ROOT / "index.html").read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "script":
            self.script = [attrs.get("type", ""), ""]

    def handle_data(self, data):
        if self.script is not None:
            self.script[1] += data

    def handle_endtag(self, tag):
        if tag == "script" and self.script is not None:
            self.scripts.append(self.script)
            self.script = None


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.document = Document()
        self.host = (ROOT / "CNAME").read_text().strip()

    def test_metadata_matches_the_published_domain(self):
        tags = self.document.tags
        canonical = [a["href"] for t, a in tags if t == "link" and a.get("rel") == "canonical"]
        self.assertEqual(canonical, [f"https://{self.host}/"])
        self.assertTrue(any(t == "title" for t, _ in tags))
        self.assertTrue(any(t == "h1" for t, _ in tags))
        self.assertTrue(any(t == "meta" and a.get("name") == "description"
                            and a.get("content") for t, a in tags))
        structured = [json.loads(source) for kind, source in self.document.scripts
                      if kind == "application/ld+json"]
        self.assertTrue(structured, "structured metadata must be valid JSON")
        self.assertTrue(any(item.get("url") == f"https://{self.host}/"
                            for graph in structured for item in graph.get("@graph", [graph])))

    def test_assets_and_navigation_targets_exist(self):
        ids = [a["id"] for _, a in self.document.tags if a.get("id")]
        self.assertEqual(len(ids), len(set(ids)), "duplicate element IDs")
        for _, attrs in self.document.tags:
            for key in ("href", "src"):
                url = attrs.get(key, "")
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc:
                    continue
                with self.subTest(url=url):
                    if parsed.path:
                        self.assertTrue((ROOT / unquote(parsed.path).lstrip("/")).is_file())
                    if parsed.fragment:
                        self.assertIn(unquote(parsed.fragment), ids)
        for kind, source in self.document.scripts:
            if kind == "application/ld+json":
                continue
            for target in re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", source):
                with self.subTest(target=target):
                    self.assertIn(target, ids)

    def test_inline_javascript_parses(self):
        scripts = [source for kind, source in self.document.scripts if kind != "application/ld+json"]
        self.assertTrue(scripts)
        for source in scripts:
            result = subprocess.run(["node", "--check"], input=source, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_crawlers_can_discover_the_homepage(self):
        locs = [node.text for node in ET.parse(ROOT / "sitemap.xml").findall(".//{*}loc")]
        self.assertIn(f"https://{self.host}/", locs)
        self.assertIn(f"Sitemap: https://{self.host}/sitemap.xml", (ROOT / "robots.txt").read_text())
        self.assertIn("Allow: /", (ROOT / "robots.txt").read_text())


if __name__ == "__main__":
    unittest.main()
