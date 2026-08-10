# 🛫 A.I.M. Flight Recorder

**A forensic skill for AGY/Antigravity and Grok CLI (dual vessel).**

Parses native session logs and writes clean Markdown **Flight Records**:

| Vessel | Logs |
|--------|------|
| **AGY** | `~/.gemini/antigravity-cli/brain/…/transcript.jsonl` |
| **Grok** | `~/.grok/sessions/<cwd>/<session_id>/updates.jsonl` |

## Features

- **Chronological indexing** — `list_sessions.py` lists **AGY and Grok** sessions.
- **Auto-detection** — latest Grok `updates.jsonl` and/or AGY `history.jsonl` for the current workspace.
- **Format auto-detect** — AGY transcript vs Grok `updates.jsonl` (or pass `--input`).
- **Modes:** `full` · `cleaned` *(default)* · `hybrid` · `chat_only`.

Dual-vessel policy: [docs/VESSEL_DUAL_COMPAT.md](docs/VESSEL_DUAL_COMPAT.md).

## Installation

```bash
git clone https://github.com/BrianV1981/aim-flight-recorder.git
cd aim-flight-recorder
```

### Grok CLI

```bash
mkdir -p ~/.grok/skills
ln -sfn "$(pwd)" ~/.grok/skills/aim-flight-recorder
# or project-local:
# mkdir -p .grok/skills && ln -sfn "$(pwd)" .grok/skills/aim-flight-recorder
```

### AGY / Antigravity (preserved)

```bash
mkdir -p ~/.gemini/antigravity-cli/skills
ln -sfn "$(pwd)" ~/.gemini/antigravity-cli/skills/aim-flight-recorder
```

Then: *"Pull a flight record of my last session."*

## Manual usage

### 1. Find a session ID
```bash
python3 scripts/list_sessions.py
```

### 2. Extract the record
```bash
python3 scripts/flight_recorder.py --session-id <ID> --mode cleaned --output record.md
# or explicit file (AGY or Grok):
python3 scripts/flight_recorder.py --input path/to/updates.jsonl --mode cleaned -o record.md
```
*(If `--session-id` is omitted, auto-detects the latest known session.)*

## Tests

```bash
python3 -m unittest tests.test_flight_recorder -v
```

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
- **[aim-flight-recorder](https://github.com/BrianV1981/aim-flight-recorder)** — Forensic Markdown session extractor.
- **[aim-boardroom](https://github.com/BrianV1981/aim-boardroom)** — Multi-agent orchestration room (OS multiplexing + artifacts).
- **[aim-skills](https://github.com/BrianV1981/aim-skills)** — **Skills index / multi-CLI install registry** (agy, grok, opencode, codex).

**DNA, comms & lore:**
- **[aim-coagents](https://github.com/BrianV1981/aim-coagents)** — DNA bank for sovereign co-agent blueprints.
- **[aim-knowledge](https://github.com/BrianV1981/aim-knowledge)** — Public Obsidian vault / deep-lore archive.
- **[aim-chalkboard](https://github.com/BrianV1981/aim-chalkboard)** — Optional cross-host async git mailbox (PoC; default same-host comms = **aim-communicate** skill).

**Deprecated / not maintained:**
- **[aim](https://github.com/BrianV1981/aim)** — Original **Gemini CLI** framework. Deprecated after loss of practical subscription access; **Great Migration → aim-agy**.
- **[aim-swarm](https://github.com/BrianV1981/aim-swarm)** — Legacy Python swarm factory → use **aim-coagents** + aim-agy spawn.
- **aim-claude / Anthropic-line vessels** — **Done.** Operator does not develop against Anthropic. Use **aim-agy / aim-grok / aim-opencode / aim-codex**.

Full map: see **aim-skills** `docs/AIM_ECOSYSTEM_MAP.md` or Operator artifact `AIM_ECOSYSTEM_MAP.md`.
<!-- AIM_ECOSYSTEM_END -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)