#!/usr/bin/env bash
# Mullet UserPromptSubmit hook — persists the off-switch to a flag file so it
# survives across turns/sessions (statusline + activate hook read it).
# "stop mullet"/"normal mode" -> off; "start mullet"/"mullet mode" -> on.
flag="$HOME/.claude/.mullet-active"
input=$(tr '[:upper:]' '[:lower:]')   # whole UserPromptSubmit JSON, lowercased
if grep -Eq 'stop mullet|normal mode' <<<"$input"; then
  echo off >"$flag"
elif grep -Eq 'start mullet|mullet mode|mullet on' <<<"$input"; then
  echo on >"$flag"
fi
exit 0
