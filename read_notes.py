from pathlib import Path


def load_notes(notes_dir: str) -> list[dict]:
    notes = []
    for path in Path(notes_dir).glob("*.md"):
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        notes.append({
            "source": path.name,
            "content": content,
        })
    return notes
