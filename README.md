# A.I.M. Flight Recorder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support%20solo%20dev-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/BrianV1981)

**Forensic skill for AGY/Antigravity and Grok CLI (dual vessel).**  
Parses native session logs and writes clean Markdown **Flight Records**.

| Vessel | Session logs |
|--------|----------------|
| **AGY / Antigravity** | `~/.gemini/antigravity-cli/brain/<id>/.system_generated/logs/transcript.jsonl` |
| **Grok CLI** | `~/.grok/sessions/<urlencode(cwd)>/<session_id>/updates.jsonl` |

No machine-local absolute homes and no operator usernames in docs or install examples — use `$HOME`, `~`, `$(pwd)`, or `$SKILL_ROOT`.

---

## Features

- **Dual vessel** — AGY brain transcripts **and** Grok `updates.jsonl` (auto-detect or `--input`).
- **Chronological index** — `list_sessions.py` lists **both** vessels (combined + per-vessel tables).
- **Auto-detect session** — latest Grok `updates.jsonl` by mtime, then AGY `history.jsonl` for the current workspace.
- **Modes:** `full` · `cleaned` *(default)* · `hybrid` · `chat_only`.
- **Portable skill body** — `SKILL.md` + `scripts/` at repo root; symlink the repo into any vessel skills dir.

Dual-vessel policy: [`docs/VESSEL_DUAL_COMPAT.md`](docs/VESSEL_DUAL_COMPAT.md).

---

## Installation

```bash
git clone https://github.com/BrianV1981/aim-flight-recorder.git
cd aim-flight-recorder
```

### Grok CLI

```bash
# user-global
mkdir -p "${HOME}/.grok/skills"
ln -sfn "$(pwd)" "${HOME}/.grok/skills/aim-flight-recorder"

# or project-local
# mkdir -p .grok/skills && ln -sfn "$(pwd)" .grok/skills/aim-flight-recorder
```

### AGY / Antigravity (preserved)

```bash
mkdir -p "${HOME}/.gemini/antigravity-cli/skills"
ln -sfn "$(pwd)" "${HOME}/.gemini/antigravity-cli/skills/aim-flight-recorder"
```

Then ask the agent: *"Pull a flight record of my last session."*

---

## Manual usage

Resolve the skill root after install (checkout or symlink target):

```bash
SKILL_ROOT="$(pwd)"   # from this clone
# or: SKILL_ROOT="${HOME}/.grok/skills/aim-flight-recorder"
```

### 1. List sessions (AGY + Grok)

```bash
python3 "${SKILL_ROOT}/scripts/list_sessions.py"
```

### 2. Extract a flight record

```bash
python3 "${SKILL_ROOT}/scripts/flight_recorder.py" \
  --session-id <ID> \
  --mode cleaned \
  --output record.md

# Explicit file (either vessel format):
python3 "${SKILL_ROOT}/scripts/flight_recorder.py" \
  --input path/to/updates.jsonl \
  --mode cleaned \
  -o record.md
```

If `--session-id` is omitted, the script auto-detects the latest known session.

### Modes

| Mode | Behavior |
|------|----------|
| `cleaned` | Agent text + one-line tool summaries (default) |
| `full` | Full agent text, tool payloads, tool outputs |
| `hybrid` | Agent text + tool targets (commands/paths), no raw outputs |
| `chat_only` | Operator / Agent text only |

---

## Layout

```text
SKILL.md                 # Grok/AGY skill playbook (frontmatter + instructions)
scripts/
  flight_recorder.py     # AGY + Grok parsers, --input / --session-id
  list_sessions.py       # dual vessel index
docs/VESSEL_DUAL_COMPAT.md
tests/
  fixtures/              # AGY + Grok sample logs (no machine paths)
  test_flight_recorder.py
```

---

## Design rules

1. **No absolute home paths** and **no machine usernames** in `SKILL.md`, README, or install docs.  
2. **Dual vessel** — Grok support must not remove AGY brain paths or install instructions.  
3. Prefer `$SKILL_ROOT`, `$HOME`, `~`, and relative `scripts/…` in examples.  
4. Flight record `Source:` lines prefer cwd-relative or `~/…` display paths.

---

## Tests

```bash
python3 -m unittest tests.test_flight_recorder -v
```

---

## Support

**[Buy Me a Coffee →](https://www.buymeacoffee.com/BrianV1981)**

MIT — fork it, keep it, walk away with the files.

---

<!-- AIM_ECOSYSTEM_START -->
### 🧬 The A.I.M. Ecosystem

Modular A.I.M. (Actual Intelligent Memory) repositories. **Flagship engine: [aim-agy](https://github.com/BrianV1981/aim-agy).**

**Active vessels (CLI hosts):**
- **[aim-agy](https://github.com/BrianV1981/aim-agy)** — Core engine / *soul* (Antigravity CLI). *Flagship.* Shared nested `aim-agy_os/` ships here first.
- **[aim-grok](https://github.com/BrianV1981/aim-grok)** — Grok CLI vessel (hybrid memory, GitOps, wiki, fleet orchestration tooling).
- **[aim-opencode](https://github.com/BrianV1981/aim-opencode)** — OpenCode CLI vessel.
- **[aim-codex](https://github.com/BrianV1981/aim-codex)** — OpenAI Codex CLI vessel (greenfield nested soul + Codex overlays; primary `main`).

**Tools & workspaces:**
- **[aim-connect](https://github.com/BrianV1981/aim-connect)** — Self-hosted remote workspace web UI.
- **[aim-tmux-dashboard](https://github.com/BrianV1981/aim-tmux-dashboard)** — Terminal multi-session monitor.
- **[aim-browser](https://github.com/BrianV1981/aim-browser)** — Headed Chromium CDP engine + browser **skill suite**.
- **[aim-google](https://github.com/BrianV1981/aim-google)** — Google Workspace CLI (Gmail, Drive, Calendar, …).
- **[aim-flight-recorder](https://github.com/BrianV1981/aim-flight-recorder)** — **This repo** — forensic Markdown session extractor (AGY + Grok).
- **[aim-boardroom](https://github.com/BrianV1981/aim-boardroom)** — Multi-agent orchestration room (OS multiplexing + artifacts).
- **[aim-skill-library](https://github.com/BrianV1981/aim-skill-library)** — Shareable **tool skills** (communicate, calc, memory, …) + companion index.

**DNA, comms & lore:**
- **[aim-coagents](https://github.com/BrianV1981/aim-coagents)** — DNA bank for sovereign co-agent blueprints.
- **[aim-knowledge](https://github.com/BrianV1981/aim-knowledge)** — Public Obsidian vault / deep-lore archive.
- **[aim-chalkboard](https://github.com/BrianV1981/aim-chalkboard)** — Optional cross-host async git mailbox (PoC; default same-host comms = **aim-communicate** skill).

**Deprecated / not maintained:**
- **[aim](https://github.com/BrianV1981/aim)** — Original **Gemini CLI** framework. Deprecated after loss of practical subscription access; **Great Migration → aim-agy**.
- **[aim-swarm](https://github.com/BrianV1981/aim-swarm)** — Legacy Python swarm factory → use **aim-coagents** + aim-agy spawn.
- **aim-claude / Anthropic-line vessels** — **Done.** Operator does not develop against Anthropic. Use **aim-agy / aim-grok / aim-opencode / aim-codex**.
<!-- AIM_ECOSYSTEM_END -->
