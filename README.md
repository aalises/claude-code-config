# claude-code-config

My personal Claude Code setup — commands, hooks, and config I use daily for
AI-assisted development. The core idea: use multiple AI agents as
**adversarial collaborators**, not just code generators.

## Philosophy

These tools are built around a few patterns I keep coming back to:

- **Multi-agent debate** — One agent proposes, another challenges. Fresh eyes
  catch what the author misses. The orchestrator (Claude Code) keeps full
  session context while challengers come in cold each round.
- **Filesystem as communication layer** — Agents read and write to shared
  files (`plan.md`, `critique.md`) instead of passing giant strings through
  shell arguments. Inspectable, debuggable, version-controllable.
- **Session context is precious** — Claude Code remembers every file it read.
  Don't throw that away by spawning fresh instances when you don't have to.
- **Clipboard-first output** — Plans and handoffs go straight to clipboard
  for pasting into PRs, Linear, Notion, or Slack.

## Setup

```bash
# Clone
git clone git@github.com:aalises/claude-code-config.git
cd claude-code-config

# Symlink all commands globally
ln -s $(pwd)/commands/* ~/.claude/commands/

# Add the hooks to your ~/.claude/settings.json (see Hooks section below)
```

Commands in `~/.claude/commands/` are available in every repo.

## Commands

### `/challenge-plan` — Debate a plan with another AI agent

Multi-agent debate loop. Claude Code orchestrates while an external AI agent
(Codex, Claude, Aider, etc.) independently explores the codebase and
challenges your plan.

```
/challenge-plan codex -q         # Use OpenAI Codex as challenger
/challenge-plan claude -p        # Use another Claude Code instance
/challenge-plan aider --message  # Use Aider
```

**How it works:**
1. Writes your current plan to `plan.md`
2. Shells out to the challenger — they explore the repo and write `critique.md`
3. Claude Code verifies each concern against the codebase (keeping full context)
4. Revises the plan, repeats up to 5 rounds or until convergence
5. Presents the final plan with revision history

### `/challenge-code` — Debate your implementation with another AI agent

Same debate loop, but on your **actual code changes** instead of a plan.
The challenger reviews your git diff, explores the codebase for context,
and critiques the implementation.

```
/challenge-code codex -q
/challenge-code claude -p
```

**How it works:**
1. Captures your git diff into `changes-for-review.md`
2. Challenger explores the repo, reviews the diff, writes `critique.md`
3. Claude Code verifies concerns and **fixes code directly** if valid
4. Repeats up to 5 rounds or until convergence
5. Summarizes what was fixed vs. deferred

### `/handoff` — Export session context

Exports your current Claude Code session context to a structured markdown
document. Captures decisions made, files explored, what's done, what's not,
and gotchas that the next person should know.

```
/handoff
```

Auto-copies to clipboard. Useful for:
- Handing off to a teammate async
- Writing PR descriptions
- Resuming work in a future session

## Hooks

### `copy-plan-to-clipboard.sh`

PostToolUse hook on `ExitPlanMode`. Auto-copies the plan to clipboard when you
exit plan mode.

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "<path-to-repo>/hooks/copy-plan-to-clipboard.sh",
            "timeout": 5,
            "async": true
          }
        ]
      }
    ]
  }
}
```

## Structure

```
commands/       # Custom slash commands (.md files)
hooks/          # Hook scripts (referenced from settings.json)
fragments/      # Reusable CLAUDE.md snippets to symlink into projects
```

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- A challenger CLI for debate commands (any of: `codex`, `claude`, `aider`)
- macOS (`pbcopy`) or Linux (`xclip`) for clipboard features
