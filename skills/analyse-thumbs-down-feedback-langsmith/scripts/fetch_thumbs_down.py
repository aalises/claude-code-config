#!/usr/bin/env python3
"""Fetch thumbs-down traces from a LangSmith annotation queue.

Pulls items from an annotation queue within a recent time window, then for
each trace fetches the root run, direct descendants (LLM/tool calls), and any
feedback records. Emits a markdown-formatted report on stdout; the caller
(Claude) is expected to read it and write a per-trace assessment.

Configuration (env vars, overridable via CLI flags):
    LANGSMITH_API_KEY       API key with read access to the workspace
    LANGSMITH_QUEUE_ID      Annotation queue UUID  (required)
    LANGSMITH_PROJECT_ID    Restrict queue items to this project UUID (optional)
    LANGSMITH_TENANT_ID     Tenant/workspace UUID — used for browser URLs (optional)

Usage:
    python3 fetch_thumbs_down.py --days 7
    python3 fetch_thumbs_down.py --queue-id <UUID> --project-id <UUID> --tenant-id <UUID>
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = "https://api.smith.langchain.com/api/v1"


def resolve_key(env_name: str) -> str:
    key = os.environ.get(env_name)
    if key:
        return key
    zshrc = Path.home() / ".zshrc"
    if zshrc.exists():
        for line in zshrc.read_text().splitlines():
            m = re.match(rf"^\s*export\s+{re.escape(env_name)}=(.+)$", line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    sys.exit(f"ERROR: {env_name} not set and not found in ~/.zshrc")


def api(path: str, key: str, method: str = "GET", body: dict | None = None):
    url = BASE + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"X-API-Key": key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err_body = e.read()[:300].decode(errors="replace")
        return {"_error": f"HTTP {e.code}", "_body": err_body}
    except Exception as e:
        return {"_error": str(e)}


def parse_ts(s: str | None):
    if not s:
        return None
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d


def truncate(s, n: int = 400) -> str:
    if s is None:
        return ""
    s = str(s)
    return s if len(s) <= n else s[: n - 1] + "…"


def fetch_run(run_id: str, key: str) -> dict:
    return api(f"/runs/{run_id}", key)


def fetch_feedback(run_id: str, key: str) -> list:
    r = api(f"/feedback?run={run_id}&limit=20", key)
    if isinstance(r, list):
        return r
    if isinstance(r, dict) and "feedback" in r:
        return r["feedback"]
    return []


def summarise_trace(root_id: str, key: str) -> dict:
    root = fetch_run(root_id, key)
    if root.get("_error"):
        return {"root_id": root_id, "error": root}
    child_ids = root.get("child_run_ids") or []
    with ThreadPoolExecutor(max_workers=8) as ex:
        children = list(ex.map(lambda cid: fetch_run(cid, key), child_ids))
    children = [c for c in children if isinstance(c, dict) and not c.get("_error")]
    children.sort(key=lambda c: c.get("dotted_order") or c.get("start_time") or "")
    return {"root": root, "children": children}


def run_url(tenant_id: str | None, project_id: str | None, run_id: str) -> str:
    if tenant_id and project_id:
        return f"https://smith.langchain.com/o/{tenant_id}/projects/p/{project_id}/r/{run_id}"
    if tenant_id:
        return f"https://smith.langchain.com/o/{tenant_id}/r/{run_id}"
    return f"https://smith.langchain.com/r/{run_id}"


def render_trace(
    data: dict,
    queue_item: dict,
    key: str,
    tenant_id: str | None,
    project_id: str | None,
) -> str:
    if "error" in data:
        return f"\n---\n## Trace `{data['root_id']}`\nERROR: {data['error']}\n"

    root = data["root"]
    children = data["children"]
    run_id = root["id"]
    meta = (root.get("extra") or {}).get("metadata") or {}
    effective_project = project_id or root.get("session_id")
    url = run_url(tenant_id, effective_project, run_id)

    st = parse_ts(root.get("start_time"))
    et = parse_ts(root.get("end_time"))
    dur = f"{(et - st).total_seconds():.1f}s" if st and et else "?"
    added = parse_ts(queue_item.get("added_at"))

    lines = [
        f"\n---",
        f"## Trace `{run_id}`",
        f"- **URL:** {url}",
        f"- **Queued (thumbs-down):** {added.isoformat() if added else '?'}",
        f"- **Run start:** {root.get('start_time')}  **Duration:** {dur}",
        f"- **Status:** {root.get('status')}  **Final:** {meta.get('final_status') or '-'}",
        f"- **Model:** {(meta.get('model_id') or {}).get('modelId', 'unknown')}",
        f"- **Thread:** {meta.get('thread_id') or meta.get('conversation_id') or '-'}",
        f"- **Agent role:** {meta.get('agent_role') or '-'}",
        f"- **Queue reviewed:** {queue_item.get('last_reviewed_time') or 'no'}",
    ]

    user_input = root.get("inputs") or {}
    msg = user_input.get("message") if isinstance(user_input, dict) else user_input
    lines.append(f"\n### User / input\n```\n{truncate(msg, 1500)}\n```")

    outputs = root.get("outputs") or {}
    lines.append(
        f"\n### Output\n```json\n{truncate(json.dumps(outputs, default=str, indent=2), 600)}\n```"
    )

    fb_items = fetch_feedback(run_id, key)
    if fb_items:
        lines.append(f"\n### Feedback records ({len(fb_items)})")
        for f in fb_items:
            lines.append(
                f"- key=`{f.get('key')}` score=`{f.get('score')}` "
                f"comment=`{f.get('comment') or ''}` by=`{f.get('created_by') or ''}`"
            )
    else:
        lines.append("\n### Feedback records: none")

    interesting = [c for c in children if c.get("run_type") in ("llm", "tool")]
    lines.append(
        f"\n### Tool calls & LLM outputs ({len(interesting)} of {len(children)} descendants)"
    )
    MAX = 40
    for c in interesting[:MAX]:
        cst_raw = c.get("start_time", "")
        cst = cst_raw[11:19] if cst_raw else "?"
        cstd = parse_ts(cst_raw)
        cet = parse_ts(c.get("end_time"))
        cdur = f"{(cet - cstd).total_seconds():.1f}s" if cstd and cet else "?"
        rt = c.get("run_type")
        name = c.get("name")
        cmeta = (c.get("extra") or {}).get("metadata") or {}
        err = " **ERR**" if c.get("error") else ""
        if rt == "tool":
            ins = c.get("inputs") or {}
            if isinstance(ins, dict) and "input" in ins:
                ins = ins["input"]
            outs = c.get("outputs")
            tool_label = cmeta.get("tool_name") or name
            lines.append(f"- [{cst}] {cdur} `tool:{tool_label}`{err}")
            lines.append(f"  - in: `{truncate(json.dumps(ins, default=str), 250)}`")
            lines.append(f"  - out: `{truncate(json.dumps(outs, default=str), 400)}`")
        elif rt == "llm":
            outs = c.get("outputs") or {}
            msgs = outs.get("messages") or []
            text = ""
            if msgs:
                last = msgs[-1]
                text = last.get("content") if isinstance(last, dict) else str(last)
            req = outs.get("requested_tools") or []
            calls = [t.get("toolName") for t in req]
            lines.append(f"- [{cst}] {cdur} `llm`{err}")
            bare = f"[Calling tools: {', '.join(calls)}]"
            if text and str(text).strip() not in ("", bare):
                lines.append(f"  - text: `{truncate(text, 400)}`")
            if calls:
                lines.append(f"  - calls: `{calls}`")
    if len(interesting) > MAX:
        lines.append(f"- … ({len(interesting) - MAX} more truncated)")

    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=7, help="How many days back (default 7)")
    p.add_argument("--limit", type=int, default=100, help="Max queue items to scan")
    p.add_argument(
        "--queue-id",
        default=os.environ.get("LANGSMITH_QUEUE_ID"),
        help="Annotation queue UUID (or env LANGSMITH_QUEUE_ID)",
    )
    p.add_argument(
        "--project-id",
        default=os.environ.get("LANGSMITH_PROJECT_ID"),
        help="Only include queue items for this project UUID (or env LANGSMITH_PROJECT_ID)",
    )
    p.add_argument(
        "--tenant-id",
        default=os.environ.get("LANGSMITH_TENANT_ID"),
        help="Tenant/workspace UUID — used to build browser URLs (or env LANGSMITH_TENANT_ID)",
    )
    p.add_argument(
        "--api-key-env",
        default="LANGSMITH_API_KEY",
        help="Env var holding the LangSmith API key (default LANGSMITH_API_KEY)",
    )
    args = p.parse_args()

    if not args.queue_id:
        sys.exit("ERROR: --queue-id (or env LANGSMITH_QUEUE_ID) is required")

    key = resolve_key(args.api_key_env)
    now = datetime.now(tz=timezone.utc)
    cutoff = now - timedelta(days=args.days)

    items = api(f"/annotation-queues/{args.queue_id}/runs?limit={args.limit}", key)
    if isinstance(items, dict) and items.get("_error"):
        sys.exit(f"ERROR: failed to fetch queue: {items}")

    in_window = []
    for it in items or []:
        if args.project_id and it.get("session_id") != args.project_id:
            continue
        added = parse_ts(it.get("added_at"))
        if not added or added < cutoff:
            continue
        in_window.append((added, it))
    in_window.sort(key=lambda x: x[0], reverse=True)

    print("# Thumbs-down traces")
    print(f"**Queue:** `{args.queue_id}`")
    if args.project_id:
        print(f"**Project:** `{args.project_id}`")
    print(f"**Window:** past {args.days} days (since {cutoff.isoformat()})")
    print(f"**Found:** {len(in_window)} trace(s)")

    if not in_window:
        print("\n_No thumbs-down traces in this window._")
        return 0

    for _added, item in in_window:
        data = summarise_trace(item["id"], key)
        print(render_trace(data, item, key, args.tenant_id, args.project_id))

    return 0


if __name__ == "__main__":
    sys.exit(main())
