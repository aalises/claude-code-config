---
name: analyse-thumbs-down-feedback-langsmith
description: >-
  Fetches thumbs-down traces from a LangSmith annotation queue over a recent
  time window and produces a per-trace assessment table (trace ID, URL,
  assessment). Use when the user asks to analyse/review/audit thumbs-down,
  negative feedback, or down-voted traces in LangSmith over the past N days
  (or "past week", "past 2 days", etc.).
---

# Analyse thumbs-down traces (LangSmith)

Pulls items from a LangSmith annotation queue within a time window, fetches
each trace's context (user input, final status, tool calls, LLM messages,
feedback comments), and produces a short assessment per trace.

## Prerequisites

Configure these via env vars (preferred) or CLI flags:

| Env var | CLI flag | Required | Purpose |
|---|---|---|---|
| `LANGSMITH_API_KEY` | `--api-key-env VAR` | yes | API key with read access to the workspace. Override the env var name with `--api-key-env` if you store it elsewhere (e.g. `LANGSMITH_API_KEY_PROD`). |
| `LANGSMITH_QUEUE_ID` | `--queue-id` | yes | Annotation queue UUID to pull from. |
| `LANGSMITH_PROJECT_ID` | `--project-id` | optional | Filter queue items to a single project (matches the run's `session_id`). |
| `LANGSMITH_TENANT_ID` | `--tenant-id` | optional | Used to build browser URLs for each trace. |

Where to find the IDs in LangSmith:
- **Queue ID** — Annotation Queues → open queue → URL contains `/queues/<QUEUE_ID>`.
- **Project ID** — Projects → open project → URL contains `/projects/p/<PROJECT_ID>`.
- **Tenant ID** — any page → `smith.langchain.com/o/<TENANT_ID>/...`.

Runtime: Python 3 (stdlib only — no pip installs).

## Workflow

1. **Parse the window** from the user's request. Default to **7 days** if unspecified.
   - "past week" / "last week" → 7
   - "past 2 days" → 2
   - "past N days" / "last N days" → N
2. **Run the fetch script** (it writes a markdown report to stdout). The script
   lives at `scripts/fetch_thumbs_down.py` relative to this skill's directory:
   ```bash
   python3 <this-skill-dir>/scripts/fetch_thumbs_down.py --days N
   ```
   If the env vars aren't set, pass the IDs explicitly:
   ```bash
   python3 <this-skill-dir>/scripts/fetch_thumbs_down.py \
     --days N \
     --queue-id <QUEUE_ID> \
     --project-id <PROJECT_ID> \
     --tenant-id <TENANT_ID>
   ```
3. **Assess each trace thoroughly.** For every `## Trace …` block in the
   report, produce a detailed assessment with three sub-sections:
   - **What happened** — walk the trace: user request → agent/orchestrator
     response → tool calls → any subagent result → final state. Cite concrete
     signals (timings, tool names, error messages, cancelled reasons).
   - **Likely causes** — why the user was dissatisfied. Multiple causes are
     often compounding. Consider: silent LLM turns (tool calls with no
     assistant text), failed tool results, overconfident openers vs. broken
     delivery, long HITL waits, subagents that commit known-broken state,
     mismatch between user intent and agent action, feedback comments when
     present.
   - **Suggested fixes** — concrete, actionable. Prompt/tool/agent changes,
     pre-flight checks, placeholder behaviour, UX changes, better assistant
     messages. Prefer specifics over platitudes.
4. **Render the output** in the format below. The table is a scannable index;
   the detailed sections are where the real assessment lives.

## Output format

Start with a one-line summary and a scannable index table (one-line gist per
trace), then a detailed section per trace.

```
**3 thumbs-down traces in the past 7 days.**

| Trace | URL | Gist |
|---|---|---|
| `019dafb4…05e1b1f65da0` | [view](https://smith.langchain.com/o/…/r/019dafb4-0518-…) | <one-line gist of what went wrong> |

---

### `019dafb4-0518-7000-8000-05e1b1f65da0`
[LangSmith](https://smith.langchain.com/o/…/r/019dafb4-0518-…)

**What happened.** <walk the trace with concrete signals — timings, tool names, error messages>

**Likely causes.**
- <cause 1, tied to a concrete signal in the trace>
- <cause 2>

**Suggested fixes.**
- <specific, actionable fix 1>
- <specific, actionable fix 2>
```

- Use the full run ID as the `Trace` column (backticked) and a short link label for the URL.
- If there are zero traces in the window, say so in one sentence and offer to widen the range.

## Notes

- The script fetches root + direct descendants only (LLM/tool calls). If an
  assessment is unclear for a specific trace, dig deeper via the LangSmith API
  using the run ID — don't guess.
- Thumbs-down queue items often have **no comments** (`Feedback records: none`).
  That is normal. When a reviewer processes the queue entry, comments appear
  in `/feedback?run=<id>` and in the queue item's `last_reviewed_time` /
  `completed_by` fields; the script surfaces both.
- The script caps at 40 tool/LLM call entries per trace. Very long traces may
  have more detail in LangSmith.
