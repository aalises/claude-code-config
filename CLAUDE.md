# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Claude Code configuration toolkit — custom slash commands, hooks, and reusable fragments for AI-assisted development. Commands are symlinked from `~/.claude/commands/` so they're available in every repo.

## Architecture

### Core patterns

- **Multi-agent debate**: One agent (Claude Code) orchestrates while an external challenger CLI (`codex`, `claude`, `aider`) independently critiques plans or code. The orchestrator keeps full session context; challengers come in cold each round.
- **Filesystem as communication layer**: Agents communicate through shared files (`plan.md`, `critique.md`, `changes-for-review.md`) rather than shell arguments. The debate commands create these files, run the challenger, then read back results.
- **Clipboard-first output**: Most commands auto-copy their output via `pbcopy` (macOS) or `xclip` (Linux).

### Command lifecycle

The commands form two workflows:

**Debate loop** (`/challenge-plan`, `/challenge-code`):
1. Write context to file → 2. Shell out to challenger → 3. Read critique → 4. Verify each concern against codebase → 5. Revise or refute → 6. Repeat (up to 5 rounds or convergence) → 7. Cleanup temp files

**Context lifecycle** (`/wip` → `/resume`, `/handoff` → `/resume`, `/diff-summary`):
- `/wip` appends to `.wip` file; `/handoff` writes `handoff.md`
- `/resume` reads both, briefs you, then deletes them (consumed into conversation)
- `/diff-summary` is standalone — clipboard-only, no file persisted

**Assessment** (`/assess`):
- Fetches from Notion MCP (`mcp__notion__notion-fetch`) or Linear MCP (`mcp__linear-server__get_issue`), then launches parallel Explore agents for codebase investigation. Analysis only, no code changes.

### Structure

```
commands/     # Slash command definitions (.md with YAML frontmatter)
hooks/        # Shell scripts referenced from ~/.claude/settings.json
fragments/    # Reusable CLAUDE.md snippets to symlink into projects
```

## Command file conventions

Each command file uses YAML frontmatter with:
- `description`: shown in command picker
- `argument-hint`: placeholder text for arguments
- `allowed-tools`: explicit tool allowlist (keeps commands scoped)

Commands that produce output for the user follow the pattern: generate content → write to file → copy to clipboard → confirm to user.

## Hook setup

Hooks are configured in `~/.claude/settings.json` under `hooks.PostToolUse` (or other lifecycle events). The hook scripts read from stdin (tool result JSON) and must be idempotent. See `hooks/copy-plan-to-clipboard.sh` for the pattern.
