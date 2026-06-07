# Daily Briefing Agent

A Python agent that reads your personal notes and RSS feeds each morning, then uses Claude to produce a cited daily briefing with notes summary, news summary, connections, and action items.

## How it works

```
notes/*.md  ──┐
              ├──► build_context ──► Claude ──► briefings/YYYY-MM-DD.md
RSS feeds  ───┘
```

1. **Load notes** — Markdown files from the `notes/` directory.
2. **Fetch articles** — Latest entries from configured RSS feeds (via [feedparser](https://pypi.org/project/feedparser/)).
3. **Build context** — Numbered sources (`[NOTE-n]`, `[ARTICLE-n]`) with truncated content for the model.
4. **Generate briefing** — Claude synthesizes a conversational briefing with inline citations.
5. **Append sources** — A `## Sources` section is added with links for every article cited in the output.

## Project structure

```
daily_briefing_agent/
├── main.py              # Entry point — orchestrates the pipeline
├── read_notes.py        # Loads markdown notes
├── read_feeds.py        # Fetches and parses RSS feeds
├── build_context.py     # Formats notes + articles for the model
├── generate_briefing.py # Calls the Anthropic API
├── config.yaml          # Feeds, model, and output settings
├── notes/               # Your personal markdown notes
├── briefings/           # Generated daily briefings (YYYY-MM-DD.md)
└── logs/                # Optional runtime logs (e.g. launchd)
```

## Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

1. Clone the repository and enter the project directory.

2. Install dependencies:

   ```bash
   pip install anthropic feedparser python-dotenv pyyaml rich
   ```

3. Create a `.env` file in the project root:

   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```

4. Add markdown notes to `notes/` (any `*.md` files are picked up automatically).

5. Edit `config.yaml` to set your RSS feeds, model, and limits.

## Usage

Run the agent manually:

```bash
python main.py
```

The briefing is written to `briefings/<today's date>.md` and printed to the terminal.

## Configuration

All settings live in `config.yaml`:

| Key | Description |
|-----|-------------|
| `rss-feeds` | List of `{ name, url }` feed entries |
| `max-articles` | Max articles to fetch per feed |
| `max-note-chars` | Character limit per note in context |
| `max-summary-chars` | Character limit per article summary in context |
| `model` | Anthropic model ID (default: `claude-haiku-4-5-20251001`) |
| `max-tokens` | Max tokens for the model response |
| `output-dir` | Directory for generated briefings |

Example:

```yaml
rss-feeds:
  - name: "TechCrunch"
    url: "https://techcrunch.com/feed/"
max-articles: 5
model: "claude-haiku-4-5-20251001"
max-tokens: 2048
output-dir: "briefings"
```

## Output format

Each briefing includes four sections:

- **Notes Summary** — What your notes say that matters today
- **News Summary** — Relevant news from RSS feeds
- **Connections** — Links between your notes and the news (evidence-based only)
- **Action Items** — Concrete next steps drawn from notes or news

Every factual claim cites its source inline as `[NOTE-n]` or `[ARTICLE-n]`. A `## Sources` section at the end lists linked articles referenced in the briefing.

## Scheduling (optional)

You can run this on a schedule with macOS `launchd`, cron, or any task runner. Point stdout/stderr at `logs/` if you want to keep a record of each run.

Example cron entry (every day at 7:00 AM):

```cron
0 7 * * * cd /path/to/daily_briefing_agent && /usr/bin/python3 main.py >> logs/launchd.log 2>> logs/launchd.error.log
```

