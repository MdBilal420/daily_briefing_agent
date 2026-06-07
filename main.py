from dotenv import load_dotenv

load_dotenv()

import yaml
from pathlib import Path
from read_notes import load_notes
from read_feeds import load_articles
from rich import print
from build_context import build_context
from generate_briefing import generate_briefing


def load_config(path: str = "config.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def main():
    config = load_config()
    notes = load_notes('notes')
    articles = load_articles(config["rss-feeds"], config["max-articles"])
    context = build_context(notes, articles, config)
    briefing = generate_briefing(context)
    print(briefing)

if __name__ == "__main__":
    main()