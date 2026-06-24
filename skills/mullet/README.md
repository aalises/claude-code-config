<p align="center">
  <img src="mullet.png" alt="Mullet" width="240">
</p>

<h1 align="center">Mullet</h1>

<p align="center"><em>business up front · party in the back</em></p>

**An agent skill for writing the least code that's actually correct.**

Mullet is a coding philosophy in one skill: think hard about what the task
*actually* needs, then write the smallest thing that does it. Two modes, one
haircut — **business up front** (reason before you type) and **party in the
back** (cut everything speculative). It runs on every code change so the
agent never quietly drifts back to over-building.

> The best code is the code never written. But the thinking that decides what
> to write is never skipped.

---

## Why

LLMs over-engineer by default. Ask for a date input and you get a custom
picker component, a config object, three abstraction layers, and a factory
"for later." Mullet is the senior dev sitting next to the agent who has been
paged at 3am for exactly that code and says: *no — one line, ship it.*

It's lazy on purpose, never lazy by accident. Validation, security,
accessibility, and error handling that prevents data loss are non-negotiable
and always survive the cut.

---

## The two sides

### Business up front — how it reasons

- **Think before coding** — state assumptions, surface tradeoffs, ask when
  genuinely unclear instead of guessing.
- **Simplicity first** — minimum code that solves the problem; nothing
  speculative. 200 lines that could be 50 get rewritten.
- **Surgical changes** — touch only what the request needs; don't "improve"
  adjacent code or refactor things that aren't broken.
- **Goal-driven** — turn "fix the bug" into "write a test that reproduces it,
  then make it pass," and loop until verified.

### Party in the back — how it cuts

The ladder. Stop at the first rung that holds:

```
1. Does this need to exist at all?      → speculative? skip it (YAGNI)
2. Stdlib does it?                       → use it
3. Native platform feature covers it?    → CSS over JS, DB constraint over app code
4. Already-installed dependency?         → use it; never add one for a few lines
5. Can it be one line?                   → one line
6. Only then                             → the minimum code that works
```

It's a reflex, not a research project. First lazy solution that works wins.

---

## Intensity

One dial — how hard it cuts. Default is **full**. Everything else stays the
same at every level; only the aggressiveness of the cutting changes.

| Level | How hard it cuts |
|---|---|
| **lite** | Lightest touch. Cuts only obvious over-engineering — speculative features, dead abstractions, unrequested config. Keeps structure and readability. |
| **full** | Default. The full ladder: stdlib/native/one-line before custom code, deletion over addition, shortest working diff. |
| **ultra** | Most aggressive. Fewest lines and files possible; one-liners and deletion even at some cost to readability. |
| **off** | Skill inert — back to default behavior. |

The safety floor never moves: validation, security, accessibility,
data-loss-preventing error handling, and the obvious in-scope parts survive
every level, ultra included.

---

## What makes it Mullet (and not just lazy)

Two deliberate rules keep the laziness honest:

- **No simplification-marker comments.** The code is never annotated as a
  shortcut. Simplicity reads as intent from the code itself; a known ceiling
  worth flagging is said in chat, not buried in a comment.
- **Don't defer the obvious.** YAGNI kills *speculative* and *unrequested*
  scope — not the parts clearly required for the thing to work. If it's
  in-scope and necessary, it's built now, not punted to "add when needed."

---

## Install (always-on mode)

Mullet ships three optional hooks that make it always-on, with a persistent
intensity level. A single flag file (`~/.claude/.mullet-active`) holds the
level (`off|lite|full|ultra`) and drives all three; default is **full**.

| Script | Hook | Does |
|---|---|---|
| `mullet-activate.sh` | `SessionStart` | Injects the skill each session, filtered to the active level (skips if off) |
| `mullet-tracker.sh` | `UserPromptSubmit` | Persists the level across turns |
| `mullet-statusline.sh` | statusline | Shows `[MULLET:<level>]` unless off |

Make them executable and wire them into `~/.claude/settings.json`:

```bash
chmod +x skills/mullet/*.sh
```

```json
{
  "statusLine": {
    "type": "command",
    "command": "<path-to-repo>/skills/mullet/mullet-statusline.sh"
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          { "type": "command", "command": "<path-to-repo>/skills/mullet/mullet-activate.sh", "timeout": 5 }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "<path-to-repo>/skills/mullet/mullet-tracker.sh", "timeout": 5 }
        ]
      }
    ]
  }
}
```

Skip the hooks entirely to use Mullet as a plain on-trigger skill instead.

---

## Toggle

| Say | Effect |
|---|---|
| `mullet lite` / `mullet full` / `mullet ultra` | Set how hard it cuts |
| `start mullet` / `mullet mode` | On at `full` |
| `stop mullet` / `normal mode` | Off — back to default behavior |

The level persists across turns and sessions until you change it.

---

## Files

```
skills/mullet/
├── SKILL.md               # the skill itself
├── mullet-activate.sh     # SessionStart injector
├── mullet-tracker.sh      # UserPromptSubmit on/off tracker
└── mullet-statusline.sh   # [MULLET] badge
```

---

## Credits

Mullet is a mix inspired by two ideas: Andrej Karpathy's coding discipline
(think before you type, simplicity first, surgical changes, goal-driven
verification) and [Ponytail](https://github.com/DietrichGebert/ponytail)'s
deliberate laziness (YAGNI, the decision ladder, shortest working diff). The
business up front comes from one, the party in the back from the other.
