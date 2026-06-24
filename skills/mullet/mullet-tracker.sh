#!/usr/bin/env bash
# Mullet UserPromptSubmit hook — persists the intensity level to a flag file so
# it survives across turns/sessions (statusline + activate hook read it).
# Levels: off|lite|full|ultra. "stop mullet"/"normal mode" -> off;
# "mullet lite|full|ultra" -> that level; "start mullet"/"mullet mode" -> full.
flag="$HOME/.claude/.mullet-active"
input=$(tr '[:upper:]' '[:lower:]')   # whole UserPromptSubmit JSON, lowercased
if grep -Eq 'stop mullet|normal mode' <<<"$input"; then
  echo off >"$flag"
elif grep -Eq 'mullet (lite|full|ultra)' <<<"$input"; then
  grep -Eo 'mullet (lite|full|ultra)' <<<"$input" | head -1 | awk '{print $2}' >"$flag"
elif grep -Eq '(lite|full|ultra) mullet' <<<"$input"; then
  grep -Eo '(lite|full|ultra) mullet' <<<"$input" | head -1 | awk '{print $1}' >"$flag"
elif grep -Eq 'start mullet|mullet mode|mullet on' <<<"$input"; then
  echo full >"$flag"
fi
exit 0
