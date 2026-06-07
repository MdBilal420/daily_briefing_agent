def truncate(text: str, max_chars: int) -> str:
    return text[:max_chars] + "..." if len(text) > max_chars else text


def build_context(notes: list[dict], articles: list[dict], config: dict) -> str:
    max_note_chars = config.get("max_note_chars", 1000)
    max_summary_chars = config.get("max_summary_chars", 500)
    lines = []
    lines.append("=== NOTES ===\n")
    for i, note in enumerate(notes, start=1):
        lines.append(f"[NOTE-{i}] {note['source']}")
        lines.append("---")
        lines.append(truncate(note["content"], max_note_chars))
        lines.append("---\n")
    lines.append("=== ARTICLES ===\n")
    for i, article in enumerate(articles, start=1):
        lines.append(f"[ARTICLE-{i}] {article['source_name']}")
        lines.append(f"Title: {article['title']}")
        lines.append(f"Link: {article['link']}")
        lines.append("---")
        lines.append(truncate(article["summary"], max_summary_chars))
        lines.append("---\n")
    return "\n".join(lines)