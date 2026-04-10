#!/bin/bash
# PostToolUse hook for ExitPlanMode
# Copies the plan file to clipboard automatically

# Read the tool result from stdin to extract the plan file path
INPUT=$(cat)
PLAN_DIR=".claude/plans"

# Find the most recently modified plan file
PLAN_FILE=$(ls -t "$PLAN_DIR"/*.md 2>/dev/null | head -1)

if [ -n "$PLAN_FILE" ] && [ -f "$PLAN_FILE" ]; then
  if command -v pbcopy &>/dev/null; then
    cat "$PLAN_FILE" | pbcopy
  elif command -v xclip &>/dev/null; then
    cat "$PLAN_FILE" | xclip -selection clipboard
  fi
fi
