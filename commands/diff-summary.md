---
description: Clipboard-ready summary of your changes for PRs, Linear, Slack, or Notion
allowed-tools: Bash, Read, Glob, Grep
---

Generate a concise, clipboard-ready summary of the current branch's changes.
This is NOT a code review — it's a clean summary for pasting into a PR
description, Linear update, Slack message, or Notion comment.

## Step 1 — Gather the diff

Determine the base branch (`main` or `master`) and run:
- `git diff <base>...HEAD --stat` — files changed
- `git log <base>...HEAD --oneline` — commits
- `git diff <base>...HEAD` — actual changes (read selectively for context)

If there are also uncommitted changes, include those too.

## Step 2 — Write the summary

Format:

```
## What changed

<1-3 sentences: the high-level what and why>

### Changes
- <file or area>: <what changed and why>
- <file or area>: <what changed and why>
- ...

### Things to watch
- <anything the reviewer should pay attention to, edge cases, trade-offs>
```

Rules:
- Keep it under 20 lines total
- Lead with *why*, not *what* — the diff shows the what
- Group by logical change, not by file
- No code blocks unless absolutely necessary
- Tone: direct, like you're briefing a colleague

## Step 3 — Clipboard

Copy the summary to clipboard (`pbcopy` on macOS, `xclip -selection clipboard`
on Linux). Tell the user it's been copied.
