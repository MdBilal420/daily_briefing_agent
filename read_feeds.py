import feedparser
import re
import html as html_module

def strip_html(text: str) -> str:
    text = html_module.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_articles(feeds: list[dict], max_articles: int) -> list[dict]:
    articles = []
    for feed in feeds:
        try:
            parsed_feed = feedparser.parse(feed['url'])
            entries = sorted(
                parsed_feed.entries,
                key=lambda e: e.get("published_parsed") or (0,) * 9,
                reverse=True
            )[:max_articles]

            for entry in entries:
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": strip_html(entry.get("summary", entry.get("description", ""))),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source_url": feed['url'],
                    "source_name": feed['name'],
                })
        except Exception as e:
            print(f"Warning: failed to fetch {feed['url']}: {e}")
    return articles