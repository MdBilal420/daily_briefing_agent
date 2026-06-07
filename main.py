from dotenv import load_dotenv

load_dotenv()

import yaml
from pathlib import Path
from datetime import date
from read_notes import load_notes
from read_feeds import load_articles
from rich import print
from build_context import build_context
from generate_briefing import generate_briefing


def load_config(path: str = "config.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

import re


def append_sources(briefing: str, articles: list[dict]) -> str:
    ids_found = sorted(set(int(n) for n in re.findall(r'\[ARTICLE-(\d+)\]', briefing)))

    lines = ["\n\n## Sources"]
    for n in ids_found:
        article = articles[n - 1]
        lines.append(f"- [ARTICLE-{n}] [{article['title']}]({article['link']})")

    return briefing + "\n".join(lines)

def main():
    config = load_config()
    notes = load_notes('notes')
    articles = load_articles(config["rss-feeds"], config["max-articles"])
    context = build_context(notes, articles, config)
    briefing = generate_briefing(context, config)
    briefing = append_sources(briefing, articles)
    
    output_dir = Path(config["output-dir"])
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{date.today()}.md"
    output_path.write_text(briefing, encoding="utf-8")
    print(f"Briefing written to {output_path}")

    print(briefing)

if __name__ == "__main__":
    main()