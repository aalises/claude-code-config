---
description: Challenge a plan using an external AI agent debate loop
argument-hint: <challenger-cli-command> (e.g. "codex -q", "claude -p", "aider --message")
allowed-tools: Bash, Read, Write, Glob, Grep
---

You are running a multi-agent debate loop. Your role is the **orchestrator**: you
keep your full session context (all files read, all exploration done) while an
external challenger agent independently explores the codebase and critiques
your proposal.

## Step 1 — Capture the proposal

Look at the most recent substantial output in this conversation — it could be
an implementation plan, an assessment, a triage, a design, an architecture
proposal, or any other structured analysis. Extract it and write it to
`plan.md` in the repo root.

At the top of `plan.md`, add a one-line label: `# <Type>: <Title>` (e.g.
`# Plan: Add file parser`, `# Assessment: Auth middleware risk analysis`,
`# Triage: N8N-1234 investigation`). This tells the challenger what kind of
document they're reviewing.

If the conversation has no substantial structured output to challenge, tell the
user and stop.

## Step 2 — Challenge loop (up to 5 rounds)

For each round:

### 2a. Invoke the challenger

Run via Bash:

```
$ARGUMENTS "Read plan.md in the repo root — it contains a proposal (plan, assessment, triage, or design). Then independently explore this codebase and challenge it. Be specific — reference actual files, functions, and edge cases you find. What assumptions are wrong? What's missing? What will break? Write your critique to critique.md in the repo root."
```

### 2b. Read the critique

Read `critique.md` and evaluate each concern.

### 2c. Verify and revise

For each concern raised by the challenger:
- **If valid**: verify it against the codebase yourself (you already have
  context), then update the proposal to address it.
- **If invalid**: note why it's wrong, citing evidence from the codebase.

Update `plan.md` with the revised proposal. Append a "## Revision history"
section at the bottom tracking what changed in each round and why.

### 2d. Check for convergence

If all substantive concerns from this round were either addressed or refuted
with evidence, the proposal has converged — stop the loop early.

## Step 3 — Present the result

- Present the final converged proposal in the conversation
- Delete `critique.md` (cleanup)
- Keep `plan.md` in place for reference
- Summarize: how many rounds it took, what the major revisions were
