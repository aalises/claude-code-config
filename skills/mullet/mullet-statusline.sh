#!/usr/bin/env bash
# Mullet statusline badge. Shows [MULLET] unless the flag file says off.
flag="$HOME/.claude/.mullet-active"
[ -f "$flag" ] && [ "$(tr -d '[:space:]' <"$flag")" = "off" ] && exit 0
printf '\033[38;5;173m[MULLET]\033[0m'
