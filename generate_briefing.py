import anthropic
from datetime import date
import os


SYSTEM_PROMPT = """You are a daily briefing assistant. Every morning you read personal notes and external news articles, then produce a clear, conversational briefing.

Rules:
- Every factual claim must cite its source immediately using [NOTE-n] or [ARTICLE-n].
- Do not state anything that cannot be traced to a provided source.
- If a source is thin (title only, no summary), say so honestly rather than inventing detail.
- Tone: conversational, like a smart friend summarising your morning, not a news anchor.

Output format (use exactly these four sections):

## Notes Summary
What your notes say that matters today.

## News Summary
What is happening in the world worth knowing.

## Connections
Explicit links between your notes and the news. Only include a connection if the evidence is in the sources — do not speculate.

## Action Items
Concrete things worth doing today, drawn directly from notes or news."""


def generate_briefing(context: str, config: dict) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    user_message = f"Here is today's context:\n\n{context}\n\nGenerate today's briefing for {date.today()}."

    message = client.messages.create(
        model=config["model"],
        max_tokens=config["max-tokens"],
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return message.content[0].text