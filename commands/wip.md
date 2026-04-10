---
description: Quick work-in-progress snapshot for fast context switches
allowed-tools: Bash, Read, Write
---

Capture a quick snapshot of the current work state. This is lighter than
`/handoff` — meant for fast context switches when you need to jump to
something else and come back later.

## What to capture

From the conversation context, write a short WIP note covering:

1. **Doing:** What you're in the middle of right now (1 sentence)
2. **Next:** What the immediate next step would be (1 sentence)
3. **Blocker:** Anything blocking or that needs a decision (optional, skip if none)

## Format

Append to `.wip` in the repo root (create if it doesn't exist). Each entry
is timestamped:

```
---
**<current date and time>** | branch: `<current branch>`
- Doing: <what's in progress>
- Next: <what comes after>
- Blocker: <if any>
---
```

Keep each entry to 3-4 lines max. This is a scratchpad, not a document.

## After writing

- Copy the latest entry to clipboard (`pbcopy` / `xclip`)
- Tell the user it's saved to `.wip` and copied
- Do NOT present a long summary — just confirm it's done
