---
name: aim-flight-recorder
description: >
  Generates clean, human-readable markdown summaries (Flight Records) of agent
  session transcripts from AGY/Antigravity brain JSONL and Grok CLI session
  logs (updates.jsonl). Use when the Operator asks to pull a flight record,
  summarize a session, clean up a log, or audit a past/current session.
  Slash: /aim-flight-recorder.
---

# AIM-Flight-Recorder

Forensic tool for **dual vessels**:

| Vessel | Session logs |
|--------|----------------|
| **AGY / Antigravity** | `~/.gemini/antigravity-cli/brain/<id>/.system_generated/logs/transcript.jsonl` |
| **Grok CLI** | `~/.grok/sessions/<urlencode(cwd)>/<session_id>/updates.jsonl` |

Use when the Operator asks to "pull a flight record", "summarize the session", "clean up the log", or audit a past/current session.

## Install roots (do not strip either)

| Vessel | Symlink target |
|--------|----------------|
| Grok | `~/.grok/skills/aim-flight-recorder` **or** `<project>/.grok/skills/aim-flight-recorder` |
| AGY | `~/.gemini/antigravity-cli/skills/aim-flight-recorder` **or** project `.gemini/skills/` |

Clone once; symlink the **repo root** (this `SKILL.md` + `scripts/`) into the vessel skills dir.

## Scripts

Resolve the skill install path (examples use `$SKILL_ROOT`):

```bash
# library checkout
SKILL_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
# after Grok install
# SKILL_ROOT="$HOME/.grok/skills/aim-flight-recorder"
# after AGY install
# SKILL_ROOT="$HOME/.gemini/antigravity-cli/skills/aim-flight-recorder"
```

### 1. List sessions (AGY + Grok)

```bash
python3 "$SKILL_ROOT/scripts/list_sessions.py"
```

Prints tables with vessel, date, session id, turn count, workspace.

### 2. Extract a flight record

```bash
python3 "$SKILL_ROOT/scripts/flight_recorder.py" [OPTIONS]
```

#### Options

1. **`--session-id <ID>`** — AGY conversation UUID or Grok session id. If omitted, auto-detects latest Grok `updates.jsonl` mtime, then AGY `history.jsonl` for the current workspace.
2. **`--input` / `-i <FILE>`** — Explicit path to AGY `transcript.jsonl` or Grok `updates.jsonl`.
3. **`--output` / `-o <FILE.md>`** — Defaults to `flight_record.md`.
4. **`--mode <MODE>`** — Default `cleaned`:
   - `full` — full agent text, tool payloads, tool outputs
   - `cleaned` — agent text + one-line tool summaries
   - `chat_only` — Operator/Agent text only
   - `hybrid` — agent text + tool targets (commands/paths), no raw outputs

### Examples

```bash
# Conversational only (current/latest session)
python3 "$SKILL_ROOT/scripts/flight_recorder.py" --mode chat_only --output chat_summary.md

# Explicit session
python3 "$SKILL_ROOT/scripts/flight_recorder.py" \
  --session-id a1b2c3d4-5678-90ab-cdef-1234567890ab \
  --mode hybrid --output audit_log.md

# Grok updates.jsonl by path
python3 "$SKILL_ROOT/scripts/flight_recorder.py" \
  --input "$HOME/.grok/sessions/<enc-cwd>/<session-id>/updates.jsonl" \
  --mode cleaned --output grok_record.md
```

## Agentic guidelines

- Default mode: **`cleaned`**. Mention `full` / `chat_only` / `hybrid` if the Operator wants more or less detail.
- **Do not** read a `--mode full` record entirely into context unless asked — report the output path instead.
- Prefer host-appropriate read tools when skimming a record:

  | Vessel | Prefer |
  |--------|--------|
  | Grok | `read_file` (limit/offset for large files) |
  | AGY | `view_file` / host read tools |

- Preserve **both** AGY and Grok paths when editing this skill — dual vessel policy.
