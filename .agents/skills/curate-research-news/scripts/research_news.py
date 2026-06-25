#!/usr/bin/env python3
"""Deterministic helpers for the curate-research-news Codex skill."""

from __future__ import annotations

import argparse
import base64
import calendar
import datetime as dt
import email.utils
import hashlib
import html
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable


TRACKING_KEYS = {
    "fbclid", "gclid", "dclid", "mc_cid", "mc_eid", "ref", "ref_src",
    "shem", "share", "sharefoc", "agadiscoversdl",
}
SCORE_MAX = {"theme": 40, "trust": 20, "mentions": 15, "novelty": 15, "freshness": 10}
META_RE = re.compile(r"<!--\s*research-news:([A-Za-z0-9_-]+)\s*-->")
CHECKBOX_RE = re.compile(r"^- \[([ xX])\] \[(.+?)\]\((https?://[^)]+)\)(.*)$")
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
URL_RE = re.compile(r"""https?://[^\s<>)\]"']+""")


def vault_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def canonical_url(url: str) -> str:
    url = html.unescape(url.strip().strip("<>"))
    parts = urllib.parse.urlsplit(url)
    scheme = parts.scheme.lower() or "https"
    host = (parts.hostname or "").lower()
    port = parts.port
    netloc = host
    if port and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
        netloc = f"{host}:{port}"
    path = re.sub(r"/+", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query = []
    for key, value in urllib.parse.parse_qsl(parts.query, keep_blank_values=True):
        low = key.lower()
        if low.startswith("utm_") or low in TRACKING_KEYS:
            continue
        query.append((key, value))
    return urllib.parse.urlunsplit((scheme, netloc, path, urllib.parse.urlencode(sorted(query)), ""))


def clean_extracted_url(url: str) -> str:
    return html.unescape(url).rstrip(".,;:!?\"'、。，．…）】」』〉》")


def title_key(title: str) -> str:
    value = unicodedata.normalize("NFKC", title).lower()
    return re.sub(r"[\W_]+", "", value, flags=re.UNICODE)


def parse_date(value: Any) -> dt.date | None:
    if not value:
        return None
    text = str(value).strip()
    try:
        return dt.date.fromisoformat(text[:10])
    except ValueError:
        pass
    try:
        parsed = email.utils.parsedate_to_datetime(text)
        return parsed.date()
    except (TypeError, ValueError, OverflowError):
        return None


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def child_text(element: ET.Element, names: Iterable[str]) -> str:
    wanted = set(names)
    for child in element.iter():
        local = child.tag.rsplit("}", 1)[-1].lower()
        if local in wanted and child.text:
            return child.text.strip()
    return ""


def parse_feed(data: bytes, source_name: str = "RSS") -> list[dict[str, Any]]:
    root = ET.fromstring(data)
    entries = [
        node for node in root.iter()
        if node.tag.rsplit("}", 1)[-1].lower() in {"item", "entry"}
    ]
    results: list[dict[str, Any]] = []
    for entry in entries:
        title = clean_text(child_text(entry, {"title"}))
        url = child_text(entry, {"link"})
        if not url:
            for child in entry:
                if child.tag.rsplit("}", 1)[-1].lower() == "link":
                    url = child.attrib.get("href", "")
                    if url:
                        break
        summary = clean_text(child_text(entry, {"description", "summary", "content"}))
        published = child_text(entry, {"pubdate", "published", "updated", "date"})
        if title and url:
            results.append({
                "title": title,
                "url": url,
                "published": parse_date(published).isoformat() if parse_date(published) else "",
                "source": source_name,
                "source_type": "rss",
                "factual_summary": summary[:500],
                "commentary": "",
                "full_text_read": False,
            })
    return results


def fetch_feed(url: str, source_name: str) -> list[dict[str, Any]]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "research-news-curator/1.0 (+local personal feed reader)"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return parse_feed(response.read(), source_name)


def load_manual_urls(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8-sig"), flags=re.S)
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line in text.splitlines():
        markdown = LINK_RE.search(line)
        if markdown:
            title, url = markdown.groups()
        else:
            match = URL_RE.search(line)
            if not match:
                continue
            url = clean_extracted_url(match.group(0))
            title = urllib.parse.urlsplit(url).hostname or url
        key = canonical_url(url)
        if key not in seen:
            seen.add(key)
            results.append({
                "title": title.strip(),
                "url": url,
                "source": "手動URL",
                "source_type": "manual",
                "factual_summary": "本文未確認。Codexで内容を確認してから採否を判断する。",
                "commentary": "XまたはGoogle Discover等で人が発見した候補。",
                "full_text_read": False,
            })
    return results


def workflowy_request(path: str, api_key: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    url = f"https://workflowy.com/api/v1/{path.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "research-news-curator/1.0 (+local personal feed reader)",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def workflowy_text(node: dict[str, Any]) -> str:
    return clean_text(" ".join([
        str(node.get("name") or ""),
        str(node.get("note") or ""),
    ]))


def workflowy_urls(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for node in sorted(nodes, key=lambda value: int(value.get("priority", 0))):
        raw_name = str(node.get("name") or "")
        raw_note = str(node.get("note") or "")
        text = workflowy_text(node)
        markdown = LINK_RE.search(raw_name) or LINK_RE.search(raw_note)
        urls = URL_RE.findall(" ".join([raw_name, raw_note]))
        if markdown and markdown.group(2) not in urls:
            urls.insert(0, markdown.group(2))
        for url in urls:
            url = clean_extracted_url(url)
            key = canonical_url(url)
            if key in seen:
                continue
            seen.add(key)
            title = clean_text(markdown.group(1)) if markdown and canonical_url(markdown.group(2)) == key else ""
            results.append({
                "title": title or text.replace(url, "").strip(" -:") or urllib.parse.urlsplit(url).hostname or url,
                "url": url,
                "source": "Workflowy Inbox",
                "source_type": "manual",
                "factual_summary": "本文未確認。Codexで内容を確認してから採否を判断する。",
                "commentary": "WorkflowyのInboxへ「後で見る」として保存された候補。",
                "full_text_read": False,
            })
    return results


def load_workflowy_inbox(config: dict[str, Any]) -> list[dict[str, Any]]:
    if not config.get("enabled", False):
        return []
    env_name = str(config.get("api_key_env") or "WORKFLOWY_API_KEY")
    api_key = os.environ.get(env_name, "").strip()
    if not api_key:
        raise RuntimeError(f"{env_name} is not set")
    parent_id = str(config.get("parent_id") or "inbox")
    recursive = bool(config.get("recursive", True))
    pending = [parent_id]
    visited: set[str] = set()
    nodes: list[dict[str, Any]] = []
    while pending:
        current = pending.pop(0)
        if current in visited:
            continue
        visited.add(current)
        payload = workflowy_request("nodes", api_key, {"parent_id": current})
        children = payload.get("nodes") or []
        nodes.extend(children)
        if recursive:
            pending.extend(str(node["id"]) for node in children if node.get("id"))
    return workflowy_urls(nodes)


def accepted_path(root: Path) -> Path:
    return root / ".research-news" / "accepted.json"


def load_accepted(root: Path) -> dict[str, dict[str, Any]]:
    data = read_json(accepted_path(root), {})
    return data if isinstance(data, dict) else {}


def save_accepted(root: Path, data: dict[str, dict[str, Any]]) -> None:
    path = accepted_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def domain_trust(url: str, trusted: list[str]) -> int:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return 20 if any(host == d or host.endswith("." + d) for d in trusted) else 8


def topic_score(item: dict[str, Any], topics: list[dict[str, Any]]) -> tuple[int, list[str]]:
    supplied = item.get("topics") or []
    if supplied:
        valid = [str(x) for x in supplied]
        return min(40, 24 + max(0, len(valid) - 1) * 8), valid
    haystack = " ".join([
        str(item.get("title", "")),
        str(item.get("factual_summary", "")),
        str(item.get("commentary", "")),
    ]).lower()
    matched_topics: list[str] = []
    hits = 0
    exclusions = 0
    for topic in topics:
        topic_hits = sum(1 for word in topic.get("include", []) if str(word).lower() in haystack)
        topic_exclusions = sum(1 for word in topic.get("exclude", []) if str(word).lower() in haystack)
        if topic_hits:
            matched_topics.append(str(topic.get("id", topic.get("name", "topic"))))
            hits += topic_hits
        exclusions += topic_exclusions
    # A single generic hit such as "AI" must not make an item relevant by itself.
    score = min(40, 8 if hits == 1 else 10 + hits * 6) if hits else 0
    score = max(0, score - exclusions * 15)
    return score, matched_topics


def freshness_score(published: dt.date | None, today: dt.date) -> int:
    if not published:
        return 2
    age = (today - published).days
    if age < 0:
        return 5
    if age <= 7:
        return 10
    if age <= 30:
        return 8
    if age <= 90:
        return 5
    return 1


def clamp_scores(scores: dict[str, Any]) -> dict[str, int]:
    result = {}
    for key, maximum in SCORE_MAX.items():
        try:
            value = int(scores.get(key, 0))
        except (TypeError, ValueError):
            value = 0
        result[key] = max(0, min(maximum, value))
    return result


def merge_candidates(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    titles: dict[str, str] = {}
    for raw in items:
        if not raw.get("url") or not raw.get("title"):
            continue
        item = dict(raw)
        key = canonical_url(str(item["url"]))
        tkey = title_key(str(item["title"]))
        merge_key = key
        if key not in merged and tkey in titles:
            merge_key = titles[tkey]
        if merge_key not in merged:
            item["url"] = key
            item["_sources"] = [str(item.get("source", "unknown"))]
            item["_occurrences"] = max(1, int(item.get("mentions", 1) or 1))
            merged[merge_key] = item
            titles[tkey] = merge_key
            continue
        target = merged[merge_key]
        source = str(item.get("source", "unknown"))
        if source not in target["_sources"]:
            target["_sources"].append(source)
        target["_occurrences"] += max(1, int(item.get("mentions", 1) or 1))
        for field in ("factual_summary", "commentary", "published"):
            if len(str(item.get(field, ""))) > len(str(target.get(field, ""))):
                target[field] = item[field]
        target["full_text_read"] = bool(target.get("full_text_read") or item.get("full_text_read"))
    return list(merged.values())


def score_candidates(
    items: list[dict[str, Any]],
    topics: list[dict[str, Any]],
    sources: dict[str, Any],
    accepted: dict[str, Any],
    today: dt.date,
) -> list[dict[str, Any]]:
    trusted = [str(x).lower() for x in sources.get("trusted_domains", [])]
    scored = []
    for item in merge_candidates(items):
        canonical = canonical_url(str(item["url"]))
        baseline_theme, matched_topics = topic_score(item, topics)
        occurrences = int(item.get("_occurrences", 1))
        baseline = {
            "theme": baseline_theme,
            "trust": domain_trust(canonical, trusted),
            "mentions": min(15, max(0, occurrences - 1) * 8),
            "novelty": 0 if canonical in accepted else 15,
            "freshness": freshness_score(parse_date(item.get("published")), today),
        }
        supplied = item.get("scores")
        if isinstance(supplied, dict):
            for key, value in clamp_scores(supplied).items():
                if key in supplied:
                    baseline[key] = value
        item["scores"] = clamp_scores(baseline)
        item["score"] = sum(item["scores"].values())
        item["topics"] = item.get("topics") or matched_topics
        item["mentions"] = occurrences
        item["sources"] = item.pop("_sources", [])
        item.pop("_occurrences", None)
        item["url"] = canonical
        item["published"] = parse_date(item.get("published")).isoformat() if parse_date(item.get("published")) else ""
        scored.append(item)
    return sorted(scored, key=lambda x: (-int(x["score"]), str(x.get("published", "")), str(x["title"])))


def encode_meta(item: dict[str, Any]) -> str:
    raw = json.dumps(item, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_meta(value: str) -> dict[str, Any]:
    padded = value + "=" * (-len(value) % 4)
    return json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))


def inbox_text(items: list[dict[str, Any]], date: dt.date, important_threshold: int) -> str:
    lines = [
        f"# 記事候補 {date.isoformat()}",
        "",
        "採用する記事は `[ ]` を `[x]` に変更する。採用記事は自動的に個別ノート化される。",
        "",
    ]
    for item in items:
        recommendation = " #important-recommended" if int(item["score"]) >= important_threshold else ""
        lines.extend([
            f"- [ ] [{item['title']}]({item['url']}){recommendation}",
            f"  <!-- research-news:{encode_meta(item)} -->",
            f"  - Score: **{item['score']}/100** "
            f"(theme {item['scores']['theme']}, trust {item['scores']['trust']}, "
            f"mentions {item['scores']['mentions']}, novelty {item['scores']['novelty']}, "
            f"freshness {item['scores']['freshness']})",
            f"  - 公開日: {item.get('published') or '不明'}",
            f"  - 情報源: {', '.join(item.get('sources') or [str(item.get('source', '不明'))])}",
            f"  - テーマ: {', '.join(item.get('topics') or []) or '未分類'}",
            f"  - 事実要約: {item.get('factual_summary') or '本文未確認。'}",
            f"  - Codexコメント案: {item.get('commentary') or '未作成。'}",
            f"  - 本文確認: {'済' if item.get('full_text_read') else '未確認またはメタデータのみ'}",
            "",
        ])
    if not items:
        lines.append("候補はありません。RSS取得エラーや検索結果の投入状況を確認してください。")
    return "\n".join(lines)


def append_inbox_candidates(
    path: Path,
    candidates: list[dict[str, Any]],
    date: dt.date,
    important_threshold: int,
) -> int:
    if not path.exists():
        write_text(path, inbox_text(candidates, date, important_threshold))
        return len(candidates)
    existing_urls = {canonical_url(str(item["url"])) for item in parse_inbox(path)}
    additions = [
        item for item in candidates
        if canonical_url(str(item["url"])) not in existing_urls
    ]
    if not additions:
        return 0
    rendered = inbox_text(additions, date, important_threshold).splitlines()
    blocks = "\n".join(rendered[4:])
    current = path.read_text(encoding="utf-8-sig").rstrip()
    write_text(path, current + "\n" + blocks)
    return len(additions)


def parse_inbox(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    items = []
    for index, line in enumerate(lines):
        match = CHECKBOX_RE.match(line)
        if not match:
            continue
        checked, title, url, suffix = match.groups()
        meta = None
        for nearby in lines[index + 1:index + 5]:
            meta_match = META_RE.search(nearby)
            if meta_match:
                meta = decode_meta(meta_match.group(1))
                break
        if meta is None:
            continue
        meta.update({
            "title": title,
            "url": canonical_url(url),
            "approved": checked.lower() == "x",
            "important": "#important" in suffix and "#important-recommended" not in suffix.replace("#important-recommended", ""),
            "applied": "#applied" in suffix,
            "_line": index,
        })
        # Explicit #important and recommendation may coexist.
        tokens = suffix.split()
        meta["important"] = "#important" in tokens
        items.append(meta)
    return items


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")
    return (slug[:60] or "article").strip("-")


def article_path(root: Path, item: dict[str, Any], accepted_date: dt.date) -> Path:
    published = parse_date(item.get("published")) or accepted_date
    digest = hashlib.sha1(canonical_url(str(item["url"])).encode("utf-8")).hexdigest()[:8]
    return root / "articles" / str(published.year) / f"{published.isoformat()}-{slugify(str(item['title']))}-{digest}.md"


def protected_human_note(existing: str) -> str:
    marker = "## 人間用メモ"
    if marker not in existing:
        return ""
    return existing.split(marker, 1)[1].strip()


def write_article(root: Path, item: dict[str, Any], accepted_date: dt.date) -> Path:
    path = article_path(root, item, accepted_date)
    human = protected_human_note(path.read_text(encoding="utf-8-sig")) if path.exists() else ""
    published = item.get("published") or "不明"
    topics = item.get("topics") or []
    body = f"""---
title: {json.dumps(str(item['title']), ensure_ascii=False)}
url: {json.dumps(canonical_url(str(item['url'])), ensure_ascii=False)}
published: {json.dumps(str(published), ensure_ascii=False)}
collected: {json.dumps(str(item.get('collected') or accepted_date.isoformat()), ensure_ascii=False)}
source: {json.dumps(', '.join(item.get('sources') or [str(item.get('source', '不明'))]), ensure_ascii=False)}
topics: {json.dumps(topics, ensure_ascii=False)}
score: {int(item.get('score', 0))}
---

# {item['title']}

## 基本情報

- URL: {item['url']}
- 公開日: {published}
- 取得日: {item.get('collected') or accepted_date.isoformat()}
- 情報源: {', '.join(item.get('sources') or [str(item.get('source', '不明'))])}
- テーマ: {', '.join(topics) or '未分類'}
- スコア: {item.get('score', 0)}/100

## 事実要約

{item.get('factual_summary') or '本文未確認。'}

## Codexのコメント案

{item.get('commentary') or '未作成。'}

## 人間用メモ

{human}
"""
    write_text(path, body)
    return path


def index_path(root: Path, date: dt.date) -> Path:
    return root / "indexes" / str(date.year) / f"{date.year}-{date.month:02d}.md"


def index_date(item: dict[str, Any], accepted_date: dt.date) -> dt.date:
    return (
        parse_date(item.get("collected"))
        or parse_date(item.get("accepted_at"))
        or accepted_date
    )


def sort_index_sections(text: str) -> str:
    lines = text.strip().splitlines()
    if not lines:
        return ""
    header: list[str] = []
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        match = re.match(r"^## (\d{4}-\d{2}-\d{2})$", line)
        if match:
            current = match.group(1)
            sections.setdefault(current, [])
        elif current is None:
            header.append(line)
        else:
            sections[current].append(line)
    output = header
    for date in sorted(sections, reverse=True):
        output.extend(["", f"## {date}"])
        body = sections[date]
        while body and not body[0].strip():
            body = body[1:]
        while body and not body[-1].strip():
            body = body[:-1]
        if body:
            output.extend(["", *body])
    return "\n".join(output)


def add_article_link(existing: str, canonical: str, article: Path, root: Path) -> str:
    marker = f"<!-- research-news:url={canonical} -->"
    lines = existing.splitlines()
    try:
        marker_index = next(i for i, line in enumerate(lines) if marker in line)
    except StopIteration:
        return existing
    relative = article.relative_to(root).with_suffix("").as_posix()
    suffix = f" → [[{relative}|個別ノート]]"
    for index in range(marker_index - 1, -1, -1):
        if lines[index].startswith("- ["):
            if "個別ノート]]" not in lines[index]:
                lines[index] += suffix
            break
        if lines[index].startswith("## "):
            break
    return "\n".join(lines)


def remove_index_entry(existing: str, marker: str) -> str:
    lines = existing.splitlines()
    try:
        marker_index = next(i for i, line in enumerate(lines) if marker in line)
    except StopIteration:
        return existing
    start = marker_index
    while start >= 0 and not lines[start].startswith("- ["):
        start -= 1
    if start < 0:
        return existing
    end = marker_index + 1
    while end < len(lines) and not lines[end].strip():
        end += 1
    return "\n".join(lines[:start] + lines[end:])


def insert_index_entry(existing: str, section: str, entry: list[str]) -> str:
    lines = existing.rstrip().splitlines()
    try:
        section_index = lines.index(section)
    except ValueError:
        return "\n".join([*lines, "", section, "", *entry, ""])
    insert_at = len(lines)
    for index in range(section_index + 1, len(lines)):
        if lines[index].startswith("## "):
            insert_at = index
            break
    while insert_at > section_index + 1 and not lines[insert_at - 1].strip():
        insert_at -= 1
    return "\n".join([*lines[:insert_at], "", *entry, "", *lines[insert_at:]])


def append_index(root: Path, item: dict[str, Any], accepted_date: dt.date, article: Path | None = None) -> bool:
    date = index_date(item, accepted_date)
    path = index_path(root, date)
    canonical = canonical_url(str(item["url"]))
    marker = f"<!-- research-news:url={canonical} -->"
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else f"# リサーチニュース {date.year}-{date.month:02d}\n"
    existed = marker in existing
    if existed:
        existing = remove_index_entry(existing, marker)
    section = f"## {date.isoformat()}"
    suffix = ""
    if article:
        relative = article.relative_to(root).with_suffix("").as_posix()
        suffix = f" → [[{relative}|個別ノート]]"
    entry = [
        f"- [{item['title']}]({canonical}){suffix}",
        f"  - テーマ: {', '.join(item.get('topics') or []) or '未分類'}",
        f"  - スコア: {item.get('score', 0)}/100",
    ]
    if item.get("factual_summary"):
        entry.append(f"  - 要約: {item['factual_summary']}")
    if item.get("human_note"):
        for note_line in str(item["human_note"]).splitlines():
            if note_line.strip():
                entry.append(f"  - {note_line.strip().lstrip('*- ').strip()}")
    entry.append(f"  {marker}")
    updated = insert_index_entry(existing, section, entry)
    write_text(path, sort_index_sections(updated))
    return not existed


def command_collect(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    topics_config = read_json(root / "config" / "topics.yaml", {"topics": []})
    sources = read_json(root / "config" / "sources.yaml", {})
    today = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    items: list[dict[str, Any]] = []
    if args.web_results:
        payload = read_json(Path(args.web_results), [])
        items.extend(payload.get("items", []) if isinstance(payload, dict) else payload)
    if not args.no_rss:
        collection = sources.get("collection", {})
        lookback_days = int(collection.get("rss_lookback_days", 60))
        max_items = int(collection.get("max_items_per_feed", 50))
        for feed in sources.get("rss", []):
            if not feed.get("enabled", True):
                continue
            try:
                feed_items = fetch_feed(str(feed["url"]), str(feed.get("name", "RSS")))
                recent_items = []
                for item in feed_items:
                    published = parse_date(item.get("published"))
                    if published and (today - published).days > lookback_days:
                        continue
                    recent_items.append(item)
                    if len(recent_items) >= max_items:
                        break
                items.extend(recent_items)
            except (OSError, ET.ParseError, urllib.error.URLError) as exc:
                print(f"RSS warning: {feed.get('name')}: {exc}", file=sys.stderr)
    manual_path = root / str(sources.get("manual_urls", "inbox/manual-urls.md"))
    items.extend(load_manual_urls(manual_path))
    try:
        items.extend(load_workflowy_inbox(sources.get("workflowy", {})))
    except (OSError, RuntimeError, ValueError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"Workflowy warning: {exc}", file=sys.stderr)
    accepted = load_accepted(root)
    scored = score_candidates(items, topics_config.get("topics", []), sources, accepted, today)
    threshold = int(sources.get("thresholds", {}).get("candidate", 55))
    candidates = [item for item in scored if item["score"] >= threshold and item["url"] not in accepted]
    for item in candidates:
        item["collected"] = today.isoformat()
    output = root / "inbox" / f"{today.isoformat()}.md"
    important = int(sources.get("thresholds", {}).get("important", 75))
    added = append_inbox_candidates(output, candidates, today, important)
    print(f"Added {added} candidates to {output}")
    return 0


def latest_inbox(root: Path) -> Path | None:
    paths = sorted(root.glob("inbox/????-??-??.md"))
    return paths[-1] if paths else None


def command_apply(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    path = Path(args.inbox).resolve() if args.inbox else latest_inbox(root)
    if not path or not path.exists():
        print("No dated inbox file found.", file=sys.stderr)
        return 2
    accepted = load_accepted(root)
    today = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    applied = 0
    article_count = 0
    changed = False
    for item in parse_inbox(path):
        if not item["approved"]:
            continue
        canonical = canonical_url(str(item["url"]))
        if item["applied"]:
            existing_item = accepted.get(canonical)
            if existing_item and not existing_item.get("article_path"):
                promoted = {**existing_item, **{k: v for k, v in item.items() if not k.startswith("_")}}
                article = write_article(root, promoted, today)
                append_index(root, promoted, today, article)
                existing_item["article_path"] = article.relative_to(root).as_posix()
                article_count += 1
                changed = True
            continue
        item["accepted_at"] = today.isoformat()
        item["collected"] = item.get("collected") or today.isoformat()
        article = write_article(root, item, today)
        append_index(root, item, today, article)
        item["article_path"] = article.relative_to(root).as_posix()
        article_count += 1
        item.pop("_line", None)
        item.pop("approved", None)
        item.pop("important", None)
        item.pop("applied", None)
        accepted[canonical] = item
        applied += 1
        changed = True
    if applied or changed:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        for item in parse_inbox(path):
            if item["approved"]:
                index = item["_line"]
                tokens = lines[index].split()
                if "#important" not in tokens:
                    lines[index] += " #important"
                if "#applied" not in tokens:
                    lines[index] += " #applied"
        write_text(path, "\n".join(lines))
        save_accepted(root, accepted)
    print(f"Applied {applied} items; created/updated {article_count} article notes.")
    return 0


def iso_week(value: str | None) -> tuple[int, int]:
    date = dt.date.fromisoformat(value) if value else dt.date.today()
    iso = date.isocalendar()
    return iso.year, iso.week


def command_review(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    year, week = iso_week(args.date)
    accepted = load_accepted(root)
    items = []
    for item in accepted.values():
        date = parse_date(item.get("accepted_at"))
        if date and date.isocalendar().year == year and date.isocalendar().week == week:
            items.append(item)
    items.sort(key=lambda x: (-int(x.get("score", 0)), str(x.get("title", ""))))
    by_topic: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        for topic in item.get("topics") or ["未分類"]:
            by_topic.setdefault(str(topic), []).append(item)
    lines = [f"# 週次レビュー {year}-W{week:02d}", "", f"- 採用記事: {len(items)}件", ""]
    for topic, topic_items in sorted(by_topic.items()):
        lines.extend([f"## {topic}", ""])
        for item in topic_items:
            important = " #important" if item.get("article_path") else ""
            lines.append(f"- [{item['title']}]({item['url']}) — {item.get('score', 0)}/100{important}")
        lines.append("")
    lines.extend(["## Codexの所見", "", "（Codexが採用記事間の傾向と関連を追記する）"])
    output = root / "reviews" / str(year) / f"{year}-W{week:02d}.md"
    write_text(output, "\n".join(lines))
    print(f"Wrote review for {len(items)} accepted items to {output}")
    return 0


def heading_date(line: str) -> dt.date | None:
    match = re.match(r"^##\s+(\d{4})[.-](\d{1,2})[.-](\d{1,2})\s*$", line)
    if not match:
        return None
    year, month, day = map(int, match.groups())
    try:
        return dt.date(year, month, day)
    except ValueError:
        return None


def parse_material(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    items: list[dict[str, Any]] = []
    current_date: dt.date | None = None
    current: dict[str, Any] | None = None
    notes: list[str] = []

    def finish() -> None:
        nonlocal current, notes
        if current:
            current["human_note"] = "\n".join(notes).strip()
            items.append(current)
        current = None
        notes = []

    for line in lines:
        date = heading_date(line)
        if date:
            finish()
            current_date = date
            continue
        match = LINK_RE.search(line)
        if match and current_date:
            finish()
            title, url = match.groups()
            current = {
                "title": title.strip(),
                "url": canonical_url(url),
                "published": current_date.isoformat(),
                "source": path.name,
                "source_type": "legacy",
                "topics": [],
                "score": 100,
                "scores": {"theme": 40, "trust": 20, "mentions": 15, "novelty": 15, "freshness": 10},
                "factual_summary": "",
                "commentary": "",
                "full_text_read": False,
                "collected": current_date.isoformat(),
                "accepted_at": current_date.isoformat(),
            }
        elif current and line.strip():
            notes.append(line.strip())
    finish()
    return items


def command_import(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    accepted = load_accepted(root)
    imported = 0
    for filename in args.files:
        for item in parse_material(Path(filename)):
            key = canonical_url(str(item["url"]))
            date = parse_date(item["published"]) or dt.date.today()
            append_index(root, item, date)
            if key not in accepted:
                accepted[key] = item
                imported += 1
    save_accepted(root, accepted)
    print(f"Imported {imported} new links; ledger now contains {len(accepted)} links.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(vault_root()), help="Obsidian vault root")
    sub = parser.add_subparsers(dest="command", required=True)

    collect = sub.add_parser("collect", help="collect and score candidates")
    collect.add_argument("--web-results")
    collect.add_argument("--date")
    collect.add_argument("--no-rss", action="store_true")
    collect.set_defaults(func=command_collect)

    apply = sub.add_parser("apply", help="apply approved inbox entries")
    apply.add_argument("--inbox")
    apply.add_argument("--date")
    apply.set_defaults(func=command_apply)

    review = sub.add_parser("review", help="create an ISO-week review")
    review.add_argument("--date")
    review.set_defaults(func=command_review)

    importer = sub.add_parser("import-materials", help="import legacy bookmark Markdown")
    importer.add_argument("files", nargs="+")
    importer.set_defaults(func=command_import)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
