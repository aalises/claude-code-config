---
description: Reconstruct context when resuming work on a project or branch
allowed-tools: Bash, Read, Glob, Grep
---

You are helping the user resume work on this project. They've context-switched
away and need to quickly understand where things left off. Gather all available
signals and present a concise briefing.

## What to check (in this order)

### 1. Handoff or WIP notes

Check for `handoff.md` and `.wip` in the repo root. If either exists, read it
— this is the most reliable context since it was written intentionally.

### 2. Git state

Run these and synthesize:
- `git status` — any uncommitted changes?
- `git log --oneline -10` — what was worked on recently?
- `git branch --show-current` — what branch are we on?
- `git diff --stat` — what files have been modified?

### 3. Plan files

Check for any `.claude/plans/*.md` files. If found, read the most recent one
— it captures the implementation plan and decisions.

Also check for `plan.md` in the repo root (left by challenge sessions).

### 4. Branch context

If the branch name looks like a Linear ticket (e.g. `aalises/pay-1234-...`),
note the ticket ID so the user can cross-reference.

## Output format

Present a concise briefing:

```
## Where you left off

**Branch:** <branch-name>
**Last commit:** <message> (<time ago>)

### Context
<1-3 sentences from handoff.md/.wip if available, or inferred from git log>

### Uncommitted changes
<file list with brief description, or "clean working tree">

### Active plan
<1-2 sentences summarizing the plan if one exists, or "no plan found">

### Suggested next step
<what seems like the logical next action>
```

Keep it scannable. The user wants to get oriented in 30 seconds, not read a report.

## Step 5 — Cleanup

After presenting the briefing, delete `.wip` and `handoff.md` if they existed
— they've been consumed. The context is now in this conversation.
