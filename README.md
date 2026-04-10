# claude-code-config

Personal Claude Code commands, hooks, and configuration fragments.

## Setup

Symlink the commands directory to make them available globally:

```bash
ln -s $(pwd)/commands/* ~/.claude/commands/
```

Or symlink individual commands:

```bash
ln -s $(pwd)/commands/challenge-plan.md ~/.claude/commands/challenge-plan.md
```

Commands in `~/.claude/commands/` are available in every repo.

## Commands

### `/challenge-plan`

Multi-agent debate loop. Claude Code orchestrates while an external AI agent
(Codex, Claude, Aider, etc.) independently challenges your plan.

```
/challenge-plan codex -q      # Use OpenAI Codex as challenger
/challenge-plan claude -p     # Use another Claude Code instance
/challenge-plan aider --message  # Use Aider
```

**How it works:**
1. Writes your current plan to `plan.md`
2. Shells out to the challenger — they explore the repo and write `critique.md`
3. Claude Code verifies each concern against the codebase (keeping full session context)
4. Revises the plan, repeats up to 5 rounds or until convergence
5. Presents the final plan

## Structure

```
commands/       # Custom slash commands (.md files)
hooks/          # Hook scripts (referenced from settings.json)
fragments/      # Reusable CLAUDE.md snippets to symlink into projects
```
