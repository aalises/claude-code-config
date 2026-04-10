---
description: Assess a Notion page or Linear ticket/URL — classify, root-cause, and plan
argument-hint: <notion-url | linear-url | linear-ticket-id>
allowed-tools: Bash, Read, Write, Glob, Grep, Agent, WebFetch
---

You are performing a deep assessment of an issue or feature request from an
external tracker. Your goal: understand what's being asked, determine if it's
valid, trace it through the codebase, and produce a structured assessment with
an implementation plan.

## Step 1 — Fetch the source

Determine the source type from `$ARGUMENTS`:

- **Notion URL** (contains `notion.so` or `notion.site`): use the Notion MCP
  tool (`mcp__notion__notion-fetch`) to fetch the page. If the content is very
  large, extract the relevant portions (title, description, reproduction steps,
  screenshots, traces, comments).
- **Linear ticket** (matches `XXX-1234` pattern) or **Linear URL** (contains
  `linear.app`): extract the ticket ID (e.g. `N8N-1234` from the URL path)
  and use the Linear MCP tool (`mcp__linear-server__get_issue`) to fetch the
  issue. Also fetch comments with `mcp__linear-server__list_comments`.
- **URL**: use WebFetch as fallback.

Extract all available signal: title, description, reproduction steps,
screenshots, conversation traces, user expectations, error messages, any
attached data.

## Step 2 — Classify

Determine the type:

| Type | Signal |
|------|--------|
| **Bug** | Something worked before and doesn't now, or behaves differently than expected |
| **UX issue** | Functionality works but the experience is confusing, misleading, or surprising |
| **Feature request** | New capability that doesn't exist yet |
| **Improvement** | Existing feature works but could be better (performance, reliability, DX) |
| **Not actionable** | Insufficient information, can't reproduce, or working as designed |

## Step 3 — Deep codebase investigation

Launch 1-3 Explore agents in parallel to trace the issue through the codebase.
Tailor the exploration to what you learned in Steps 1-2:

- For **bugs/UX issues**: trace the specific code path described in the report.
  Find the exact functions, prompts, or logic responsible. Identify root cause.
- For **features**: find where the new behavior would plug in. Identify
  existing patterns to follow, adjacent code, and integration points.
- For **improvements**: find the current implementation and understand its
  limitations.

Be specific — find file paths, line numbers, function names, data flows.

## Step 4 — Produce the assessment

Write a structured assessment directly in the conversation (NOT to a file):

```markdown
## Assessment: <title>

**Source:** <link to original issue>
**Type:** Bug | UX Issue | Feature | Improvement | Not Actionable
**Severity:** Critical | High | Medium | Low
**Confidence:** High | Medium | Low (how certain you are about the diagnosis)

### What's happening

<2-3 sentences: the problem or request in plain language, from the user's
perspective>

### Root cause / Technical analysis

<For bugs: exact root cause with file paths and line numbers>
<For features: where this would plug in, what exists today>
<Trace the data/code flow that leads to the issue>

### Affected areas

- <file:line — what it does and why it's relevant>
- <file:line — ...>

### Proposed fix / Implementation plan

<Concrete steps to fix or implement. Reference specific files, functions,
and patterns. Keep it actionable — someone should be able to pick this up
and start coding.>

1. **<file>**: <what to change and why>
2. **<file>**: <what to change and why>
...

### Verification

<How to verify the fix works — specific test commands, manual steps, or
edge cases to check>

### Open questions

<Anything you're unsure about or that needs clarification from the reporter
or team. Omit this section if there are none.>
```

## Guidelines

- **Be opinionated.** Give your honest assessment — if the issue is invalid or
  low-priority, say so and explain why.
- **Be specific.** Every claim about the codebase must reference actual files
  and line numbers you found during exploration.
- **Be concise.** The assessment should be scannable in under 2 minutes.
- **Separate observation from speculation.** If you're guessing at something,
  flag it clearly.
- **Don't start implementing.** This command produces analysis only. The user
  will decide what to do next.
