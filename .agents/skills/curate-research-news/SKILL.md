---
name: curate-research-news
description: Collect, evaluate, review, and publish research-news links into this Obsidian vault. Use when asked in Japanese or English to collect news/articles, organize candidate links, score relevance or attention, apply approved inbox items, create weekly reviews, import bookmark Markdown, or create important-article notes.
---

# Curate Research News

Keep the human's selection and commentary central. Use scripts for repeatable parsing,
normalization, deduplication, and file updates; use Codex for web search, factual
summaries, theme judgment, and proposed commentary.

Run commands from the vault root. Resolve Python with `python`; if unavailable, use the
workspace bundled Python runtime.

## Choose the workflow

- For "今週の候補記事を収集して": follow **Collect candidates**.
- For "候補を整理して": inspect and enrich the current inbox without changing approval marks.
- For "承認済み記事を反映して": follow **Apply approvals**.
- For "今週のレビューを作成して": follow **Create a weekly review**.
- For importing `materials/bookmarks-*.md`: follow **Import legacy bookmarks**.

Read [references/format.md](references/format.md) before manually editing generated
Markdown or producing candidate JSON.

## Collect candidates

1. Read `config/topics.yaml` and `config/sources.yaml`.
2. Search the web using every enabled `search_queries` entry. Prefer primary sources and
   current publication dates. Do not automate Google Discover.
3. Treat `inbox/manual-urls.md` as user-supplied discoveries from X, Google Discover, or
   elsewhere. Never require X engagement metrics.
   When `sources.yaml` enables Workflowy, also read URLs under its Inbox through the
   official API using the `WORKFLOWY_API_KEY` environment variable. This source is
   read-only; do not complete, move, edit, or delete Workflowy nodes.
4. For each web result, prepare a JSON object matching `references/format.md`. Keep
   `factual_summary` separate from `commentary`. State when full text could not be read.
5. Save the JSON array to a temporary file, then run:

```powershell
python .agents/skills/curate-research-news/scripts/research_news.py collect `
  --web-results <temporary-json>
```

The command also loads configured RSS feeds and manual URLs. Network failures are
reported but do not abort other sources. It canonicalizes URLs, merges repeated
mentions, scores candidates, removes already accepted URLs, and writes
`inbox/YYYY-MM-DD.md`.

Do not bypass robots.txt or access controls. Do not save full article bodies.

## Organize candidates

Open the latest `inbox/YYYY-MM-DD.md`. Verify title, URL, publication date, topics,
score explanation, factual summary, and commentary. Correct weak model judgments while
preserving the machine-readable metadata comment. Leave approval checkboxes unchanged.

Recommend `#important` only for scores at or above the configured important threshold,
or when there is a clear strategic reason stated in the commentary.

## Apply approvals

The user approves an item by changing `- [ ]` to `- [x]`. Every approved item is treated
as important and receives an article note automatically.

Run:

```powershell
python .agents/skills/curate-research-news/scripts/research_news.py apply
```

This updates monthly indexes using the date the item was collected rather than its
publication date, creates or updates important article notes, records the accepted item,
and marks the inbox item as applied. Never edit text below
`## 人間用メモ` in an existing article note.

## Create a weekly review

Run:

```powershell
python .agents/skills/curate-research-news/scripts/research_news.py review
```

Then add a concise `## Codexの所見` section to the generated review using only accepted
items from that ISO week. Describe themes and meaningful connections; do not fabricate
engagement or popularity.

## Import legacy bookmarks

Run once for each source file:

```powershell
python .agents/skills/curate-research-news/scripts/research_news.py import-materials `
  materials/bookmarks-202605.md materials/bookmarks-202606.md
```

The importer keeps source files unchanged, carries nested notes into the monthly index,
and is idempotent by canonical URL.

## Scoring policy

Use the configured 100-point model:

- theme alignment: 40
- source trust: 20
- repeated independent mentions: 15
- novelty: 15
- freshness: 10

The script computes a conservative baseline. Codex may supply component scores when it
has inspected the source, but each component must stay within its maximum. Include only
candidates meeting the configured candidate threshold. Treat social metrics as optional
evidence, never as a required input.
