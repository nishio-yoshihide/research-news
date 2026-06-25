import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).parents[1]
    / ".agents"
    / "skills"
    / "curate-research-news"
    / "scripts"
    / "research_news.py"
)
SPEC = importlib.util.spec_from_file_location("research_news", SCRIPT)
rn = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rn)


class ResearchNewsTests(unittest.TestCase):
    def test_canonical_url_removes_tracking_and_fragment(self):
        value = rn.canonical_url(
            "HTTPS://Example.COM:443/a/?utm_source=x&b=2&fbclid=z&a=1#part"
        )
        self.assertEqual(value, "https://example.com/a?a=1&b=2")

    def test_parse_rss_and_atom(self):
        rss = b"""<rss><channel><item><title>A</title><link>https://e.test/a</link>
        <pubDate>Wed, 24 Jun 2026 10:00:00 GMT</pubDate><description>Hello</description>
        </item></channel></rss>"""
        atom = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>B</title>
        <link href="https://e.test/b"/><updated>2026-06-23T00:00:00Z</updated>
        <summary>World</summary></entry></feed>"""
        self.assertEqual(rn.parse_feed(rss)[0]["published"], "2026-06-24")
        self.assertEqual(rn.parse_feed(atom)[0]["url"], "https://e.test/b")

    def test_dedupes_url_variants_and_titles(self):
        items = [
            {"title": "Same Story", "url": "https://x.test/a?utm_source=rss", "source": "rss"},
            {"title": "Same Story", "url": "https://x.test/a#x", "source": "search"},
        ]
        merged = rn.merge_candidates(items)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["_occurrences"], 2)
        self.assertEqual(set(merged[0]["_sources"]), {"rss", "search"})

    def test_single_generic_keyword_does_not_clear_threshold(self):
        score, topics = rn.topic_score(
            {"title": "AI news", "factual_summary": "", "commentary": ""},
            [{"id": "ai", "include": ["AI"], "exclude": []}],
        )
        self.assertEqual(score, 8)
        self.assertEqual(topics, ["ai"])

    def test_workflowy_nodes_extract_urls_from_name_and_note(self):
        nodes = [
            {
                "name": "[Article title](https://example.com/a?utm_source=workflowy)",
                "note": "",
                "priority": 200,
            },
            {
                "name": "Read later",
                "note": "Useful context https://example.com/b",
                "priority": 100,
            },
        ]
        items = rn.workflowy_urls(nodes)
        self.assertEqual([item["url"] for item in items], [
            "https://example.com/b",
            "https://example.com/a?utm_source=workflowy",
        ])
        self.assertEqual(items[1]["title"], "Article title")

    def test_workflowy_urls_strip_trailing_quotes_and_punctuation(self):
        nodes = [
            {
                "name": 'Quoted https://example.com/quoted"',
                "note": "Japanese https://example.com/japanese」。",
                "priority": 100,
            },
        ]
        items = rn.workflowy_urls(nodes)
        self.assertEqual([item["url"] for item in items], [
            "https://example.com/quoted",
            "https://example.com/japanese",
        ])

    def make_root(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "config").mkdir()
        (root / "inbox").mkdir()
        (root / "config" / "topics.yaml").write_text(
            json.dumps({"topics": [{"id": "agents", "include": ["agent"], "exclude": []}]}),
            encoding="utf-8",
        )
        (root / "config" / "sources.yaml").write_text(
            json.dumps({
                "thresholds": {"candidate": 55, "important": 75},
                "rss": [],
                "trusted_domains": ["example.com"],
                "manual_urls": "inbox/manual-urls.md",
            }),
            encoding="utf-8",
        )
        (root / "inbox" / "manual-urls.md").write_text("", encoding="utf-8")
        return temp, root

    def test_collect_apply_review_and_preserve_human_note(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        web = root / "web.json"
        web.write_text(json.dumps([{
            "title": "Agent workflow",
            "url": "https://example.com/a?utm_source=test",
            "published": "2026-06-24",
            "source": "search",
            "topics": ["agents"],
            "factual_summary": "Facts.",
            "commentary": "Useful.",
            "full_text_read": True,
            "scores": {"theme": 40, "trust": 20, "mentions": 0, "novelty": 15, "freshness": 10},
        }]), encoding="utf-8")
        args = rn.build_parser().parse_args([
            "--root", str(root), "collect", "--no-rss", "--date", "2026-06-25",
            "--web-results", str(web),
        ])
        self.assertEqual(args.func(args), 0)
        inbox = root / "inbox" / "2026-06-25.md"
        text = inbox.read_text(encoding="utf-8").replace(
            "- [ ] [Agent workflow]", "- [x] [Agent workflow]"
        )
        inbox.write_text(text, encoding="utf-8")
        apply_args = rn.build_parser().parse_args([
            "--root", str(root), "apply", "--date", "2026-06-25",
        ])
        self.assertEqual(apply_args.func(apply_args), 0)
        articles = list(root.glob("articles/**/*.md"))
        self.assertEqual(len(articles), 1)
        article = articles[0]
        article.write_text(
            article.read_text(encoding="utf-8") + "\n手書きメモ\n", encoding="utf-8"
        )
        # Rewriting an article must preserve the protected human section.
        item = next(iter(rn.load_accepted(root).values()))
        rn.write_article(root, item, rn.dt.date(2026, 6, 25))
        self.assertIn("手書きメモ", article.read_text(encoding="utf-8"))
        self.assertEqual(apply_args.func(apply_args), 0)
        self.assertEqual(len(list(root.glob("indexes/**/*.md"))), 1)
        review_args = rn.build_parser().parse_args([
            "--root", str(root), "review", "--date", "2026-06-25",
        ])
        self.assertEqual(review_args.func(review_args), 0)
        self.assertTrue((root / "reviews" / "2026" / "2026-W26.md").exists())

    def test_collect_appends_without_overwriting_existing_approval(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        first = root / "first.json"
        second = root / "second.json"
        base = {
            "published": "2026-06-24",
            "source": "search",
            "topics": ["agents"],
            "factual_summary": "Facts.",
            "commentary": "Useful.",
            "full_text_read": True,
            "scores": {"theme": 40, "trust": 20, "mentions": 0, "novelty": 15, "freshness": 10},
        }
        first.write_text(json.dumps([{**base, "title": "First agent", "url": "https://example.com/first"}]), encoding="utf-8")
        second.write_text(json.dumps([{**base, "title": "Second agent", "url": "https://example.com/second"}]), encoding="utf-8")
        parser = rn.build_parser()
        args = parser.parse_args([
            "--root", str(root), "collect", "--no-rss", "--date", "2026-06-25",
            "--web-results", str(first),
        ])
        self.assertEqual(args.func(args), 0)
        inbox = root / "inbox" / "2026-06-25.md"
        inbox.write_text(
            inbox.read_text(encoding="utf-8").replace("- [ ] [First agent]", "- [x] [First agent]"),
            encoding="utf-8",
        )
        args = parser.parse_args([
            "--root", str(root), "collect", "--no-rss", "--date", "2026-06-25",
            "--web-results", str(second),
        ])
        self.assertEqual(args.func(args), 0)
        text = inbox.read_text(encoding="utf-8")
        self.assertIn("- [x] [First agent]", text)
        self.assertIn("- [ ] [Second agent]", text)
        self.assertEqual(sum(line.startswith("# ") for line in text.splitlines()), 1)

    def test_index_sections_are_sorted_newest_first(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for published in ("2026-06-07", "2026-06-25", "2026-06-17"):
            rn.append_index(root, {
                "title": published,
                "url": f"https://example.com/{published}",
                "published": published,
                "collected": published,
                "score": 80,
            }, rn.dt.date(2026, 6, 25))
        index = (root / "indexes" / "2026" / "2026-06.md").read_text(encoding="utf-8")
        self.assertLess(index.index("## 2026-06-25"), index.index("## 2026-06-17"))
        self.assertLess(index.index("## 2026-06-17"), index.index("## 2026-06-07"))

    def test_index_entry_is_inserted_into_existing_date_section(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for title, published in (
            ("first", "2026-06-12"),
            ("later date", "2026-06-25"),
            ("second", "2026-06-12"),
        ):
            rn.append_index(root, {
                "title": title,
                "url": f"https://example.com/{title.replace(' ', '-')}",
                "published": published,
                "collected": published,
                "score": 80,
            }, rn.dt.date(2026, 6, 25))
        index = (root / "indexes" / "2026" / "2026-06.md").read_text(encoding="utf-8")
        section = index.split("## 2026-06-12", 1)[1]
        self.assertIn("[first]", section)
        self.assertIn("[second]", section)

    def test_index_uses_collection_date_not_publication_date(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        rn.append_index(root, {
            "title": "Older publication",
            "url": "https://example.com/older",
            "published": "2026-05-13",
            "collected": "2026-06-25",
            "score": 80,
        }, rn.dt.date(2026, 6, 25))
        june = root / "indexes" / "2026" / "2026-06.md"
        self.assertTrue(june.exists())
        self.assertIn("## 2026-06-25", june.read_text(encoding="utf-8"))
        self.assertFalse((root / "indexes" / "2026" / "2026-05.md").exists())

    def test_unapproved_is_not_applied(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        item = {
            "title": "No",
            "url": "https://example.com/no",
            "score": 80,
            "scores": {k: 0 for k in rn.SCORE_MAX},
        }
        rn.write_text(
            root / "inbox" / "2026-06-25.md",
            rn.inbox_text([item], rn.dt.date(2026, 6, 25), 75),
        )
        args = rn.build_parser().parse_args([
            "--root", str(root), "apply", "--date", "2026-06-25",
        ])
        args.func(args)
        self.assertEqual(rn.load_accepted(root), {})

    def test_import_material_keeps_notes_and_is_idempotent(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        material = root / "legacy.md"
        material.write_text(
            "# bookmarks\n## 2026.6.20\n"
            "- [Title](https://example.com/a?utm_source=x)\n"
            "  - 大事な人間のメモ\n",
            encoding="utf-8",
        )
        args = rn.build_parser().parse_args([
            "--root", str(root), "import-materials", str(material),
        ])
        args.func(args)
        args.func(args)
        index = (root / "indexes" / "2026" / "2026-06.md").read_text(encoding="utf-8")
        self.assertEqual(index.count("https://example.com/a"), 2)  # link plus marker
        self.assertIn("大事な人間のメモ", index)
        self.assertEqual(len(rn.load_accepted(root)), 1)


if __name__ == "__main__":
    unittest.main()
