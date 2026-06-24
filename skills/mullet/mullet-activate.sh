#!/bin/bash
# Mullet SessionStart hook — injects the skill every session so it's always-on.
# The flag file holds the intensity level: off|lite|full|ultra (default full).
# Mode-keyed table rows and worked-example bullets in SKILL.md are filtered down
# to the active level before injection. Wire it in settings.json — see README.
flag="$HOME/.claude/.mullet-active"
level="full"
[ -f "$flag" ] && level="$(tr -d '[:space:]' <"$flag" | tr '[:upper:]' '[:lower:]')"
case "$level" in
  lite|full|ultra) ;;
  off) exit 0 ;;
  *) level="full" ;;
esac

awk -v mode="$level" '
  /^\|[[:space:]]*\*\*(lite|full|ultra)\*\*[[:space:]]*\|/ {
    row=$0; sub(/^\|[[:space:]]*\*\*/,"",row); sub(/\*\*.*/,"",row)
    if (row==mode) print; next
  }
  /^-[[:space:]]*(lite|full|ultra):/ {
    b=$0; sub(/^-[[:space:]]*/,"",b); sub(/:.*/,"",b)
    if (b==mode) print; next
  }
  { print }
' "$(dirname "$0")/SKILL.md"
