# Data and Markdown formats

## Web-result JSON

Pass a JSON array or `{"items": [...]}` to `collect --web-results`.

```json
{
  "title": "Article title",
  "url": "https://example.com/article",
  "published": "2026-06-24",
  "source": "Example",
  "source_type": "web_search",
  "topics": ["agent-engineering"],
  "factual_summary": "A short factual summary.",
  "commentary": "Why this may matter to the configured themes.",
  "full_text_read": true,
  "mentions": 1,
  "scores": {
    "theme": 32,
    "trust": 15,
    "mentions": 0,
    "novelty": 15,
    "freshness": 10
  }
}
```

All fields except `title` and `url` are optional. Score maxima are 40, 20, 15, 15,
and 10. The script clamps out-of-range values.

## Inbox

Each candidate is one block beginning with an approval checkbox:

```markdown
- [ ] [Title](https://example.com) #important
  <!-- research-news:eyJ... -->
  - Score: **82/100**
  - ...
```

The HTML comment is URL-safe base64-encoded JSON. Keep it intact when editing visible
text. Change `[ ]` to `[x]` to approve. Every approved item automatically gets an
article note. Applied entries become `[x] ... #important #applied`.

## Generated locations

- `inbox/YYYY-MM-DD.md`: review queue
- `indexes/YYYY/YYYY-MM.md`: accepted monthly index, grouped by collection/discovery date
- `reviews/YYYY/YYYY-Www.md`: accepted weekly review
- `articles/YYYY/YYYY-MM-DD-slug-hash.md`: important article
- `.research-news/accepted.json`: idempotency ledger

Article notes are regenerated around a protected `## 人間用メモ` section. Content in
that section belongs to the human and must not be replaced.
