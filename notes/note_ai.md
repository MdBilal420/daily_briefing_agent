# AI — scratch notes

## 2026-06-02 — LLM evals
- Set up a small golden set (20 prompts) for the briefing summarizer; track faithfulness + citation rate.
- Try `gpt-4.1-mini` vs local model for cost; latency budget is ~8s per run.
- TODO: log token usage per section (news vs calendar vs notes).

## 2026-06-03 — Agents & tools
- Daily briefing agent should be **read-mostly**: fetch calendar, weather, RSS, then synthesize — no writes without confirm.
- MCP pattern works well for GitHub + docs; keep tool list under ~12 to avoid context bloat.
- Reminder: idempotent runs — same inputs → same outline, even if prose varies.

## 2026-06-04 — RAG over personal notes
- Chunk notes at ~400 tokens with 50-token overlap; embed with `text-embedding-3-small`.
- Store metadata: `source`, `date`, `tags` (e.g. `ai`, `work`, `health`).
- When retrieving for briefing, boost recency (last 7 days) and cap at 5 chunks.
- **Idea:** tag this file `ai` so morning brief can surface “what you were thinking about ML lately.”