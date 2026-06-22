#!/bin/bash
# Mullet SessionStart hook — injects the skill every session so it's always-on
# (like ponytail), instead of waiting for the skill to trigger on its own.
# Wire it in ~/.claude/settings.json — see repo README "Hooks".
cat "$(dirname "$0")/SKILL.md"
