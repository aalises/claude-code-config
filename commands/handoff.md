---
description: Export session context for async handoff or PR descriptions
allowed-tools: Bash, Read, Write, Glob, Grep
---

Generate a structured handoff document from this conversation. This captures
the context that would be lost between sessions — decisions made, things
explored, open questions — so a teammate or your future self can pick up
where you left off.

## What to include

### 1. Objective
What was the task or goal of this session? One paragraph.

### 2. Key decisions
List every significant decision made during this session with brief reasoning.
Format as:
- **Decision**: [what was decided]
- **Why**: [reasoning or trade-off]
- **Alternatives considered**: [what was rejected and why]

### 3. Files touched
List every file that was read, modified, or created, grouped by action:
- **Modified**: files with actual changes
- **Explored**: files that were read for context (only include the important ones)

### 4. What's done
Bullet list of completed work.

### 5. What's NOT done
Bullet list of remaining work, open questions, or known issues. Be specific
about what's blocking or what needs human input.

### 6. Gotchas
Anything surprising, counterintuitive, or easy to miss that the next person
should know. Things like "this function looks unused but is called dynamically"
or "don't rename this — it's referenced by string in config".

## Output

Write the handoff to `handoff.md` in the repo root and copy its contents to
the clipboard (use `pbcopy` on macOS or `xclip -selection clipboard` on Linux).

Tell the user the handoff is in `handoff.md` and has been copied to clipboard.
