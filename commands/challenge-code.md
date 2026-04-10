---
description: Challenge your code changes using an external AI agent debate loop
argument-hint: <challenger-cli-command> (e.g. "codex -q", "claude -p", "aider --message")
allowed-tools: Bash, Read, Write, Glob, Grep
---

You are running a multi-agent debate loop on your **implementation**, not a plan.
Your role is the **orchestrator**: you keep your full session context while an
external challenger agent independently reviews your actual code changes.

## Step 1 — Capture the diff

Run `git diff` (staged + unstaged) and write it to `changes-for-review.md` in
the repo root. Include a brief summary at the top listing which files changed
and why. If there are no changes, tell the user and stop.

Also write the base branch name (e.g. `main`, `master`) so the challenger has
context on what the diff is against. If unsure, use the output of
`git rev-parse --abbrev-ref HEAD` and `git merge-base HEAD main 2>/dev/null || git merge-base HEAD master`.

## Step 2 — Challenge loop (up to 5 rounds)

For each round:

### 2a. Invoke the challenger

Run via Bash:

```
$ARGUMENTS "Read changes-for-review.md in the repo root — it contains a code diff with a summary. Then independently explore this codebase to understand the context around the changes. Review the diff critically: find bugs, edge cases, security issues, missing error handling, incorrect assumptions, or things that will break. Write your critique to critique.md in the repo root."
```

### 2b. Read the critique

Read `critique.md` and evaluate each concern.

### 2c. Verify and fix

For each concern raised by the challenger:
- **If valid and actionable**: fix the code directly, then note what you
  changed.
- **If valid but out of scope**: acknowledge it and note it as a follow-up.
- **If invalid**: explain why, citing evidence from the codebase.

After making fixes, regenerate `changes-for-review.md` with the updated diff.

### 2d. Check for convergence

If all substantive concerns from this round were either fixed, acknowledged,
or refuted with evidence, the review has converged — stop the loop early.

## Step 3 — Present the result

- Present a summary: how many rounds, what was fixed, what was deferred
- List every code change made during the review (file + what changed)
- Delete `changes-for-review.md` and `critique.md` (cleanup)
