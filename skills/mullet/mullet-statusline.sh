#!/usr/bin/env bash
# Mullet statusline badge. Shows [MULLET:<level>] unless off. Default full.
flag="$HOME/.claude/.mullet-active"
level="full"
[ -f "$flag" ] && level="$(tr -d '[:space:]' <"$flag" | tr '[:upper:]' '[:lower:]')"
[ "$level" = "off" ] && exit 0
case "$level" in lite|full|ultra) ;; *) level="full" ;; esac
printf '\033[38;5;173m[MULLET:%s]\033[0m' "$level"
