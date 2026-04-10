---
description: Challenge a plan using an external AI agent debate loop
argument-hint: <challenger-cli-command> (e.g. "codex -q", "claude -p", "aider --message")
allowed-tools: Bash, Read, Write, Glob, Grep
---

You are running a multi-agent debate loop. Your role is the **orchestrator**: you
keep your full session context (all files read, all exploration done) while an
external challenger agent independently explores the codebase and critiques
your plan.

## Step 1 — Capture the plan

Take the implementation plan from this conversation and write it to `plan.md`
in the repo root. If no plan exists yet, tell the user and stop.

## Step 2 — Challenge loop (up to 5 rounds)

For each round:

### 2a. Invoke the challenger

Run via Bash:

```
$ARGUMENTS "Read plan.md in the repo root. Then independently explore this codebase and challenge the plan. Be specific — reference actual files, functions, and edge cases you find. What assumptions are wrong? What's missing? What will break? Write your critique to critique.md in the repo root."
```

### 2b. Read the critique

Read `critique.md` and evaluate each concern.

### 2c. Verify and revise

For each concern raised by the challenger:
- **If valid**: verify it against the codebase yourself (you already have
  context), then update the plan to address it.
- **If invalid**: note why it's wrong, citing evidence from the codebase.

Update `plan.md` with the revised plan. Append a "## Revision history" section
at the bottom tracking what changed in each round and why.

### 2d. Check for convergence

If all substantive concerns from this round were either addressed or refuted
with evidence, the plan has converged — stop the loop early.

## Step 3 — Present the result

- Present the final converged plan in the conversation
- Delete `critique.md` (cleanup)
- Keep `plan.md` in place for reference
- Summarize: how many rounds it took, what the major revisions were
