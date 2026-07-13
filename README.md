# 🛫 A.I.M. Flight Recorder

**A forensic skill and plugin for Google Antigravity (AGY) and the A.I.M. Exoskeleton.**

The `aim-flight-recorder` skill taps directly into the Antigravity local brain to parse native `.jsonl` session logs. It extracts, formats, and generates clean, human-readable Markdown summaries of any agent's conversational trajectory.

## Features

- **Chronological Indexing**: Easily parse and list all historical agent sessions grouped by workspace and date using `list_sessions.py`.
- **Intelligent Auto-Detection**: The skill natively hooks into `history.jsonl` to auto-detect the latest active session in your current directory.
- **Granular Formatting Modes**:
  - `full`: Extracts raw tool payloads, giant terminal outputs, and conversational context.
  - `cleaned` *(default)*: Generates a concise action-oriented summary without giant JSON blobs.
  - `hybrid`: Shows specific tool arguments (like targeted files or command line execution strings) without rendering the final tool outputs.
  - `chat_only`: Produces a pure back-and-forth conversational log, completely stripping all tool execution traces.

## Installation (Antigravity CLI)

To securely integrate this into your Antigravity environment, clone this repository and create a symlink to your `skills` directory:

```bash
git clone https://github.com/BrianV1981/aim-flight-recorder.git
cd aim-flight-recorder
ln -s $(pwd) ~/.gemini/antigravity-cli/skills/aim-flight-recorder
```

Once linked, any Antigravity agent will understand how to use the flight recorder natively. You can simply command your agent: *"Pull a flight record of my last session."*

## Manual Usage

### 1. Find a Session ID
```bash
python3 scripts/list_sessions.py
```

### 2. Extract the Record
```bash
python3 scripts/flight_recorder.py --session-id <UUID> --mode cleaned --output record.md
```
*(If `--session-id` is omitted, the script will automatically detect the last session run in the current directory).*

---

<!-- AIM_ECOSYSTEM_START -->
### 🧬 The A.I.M. Ecosystem

Modular A.I.M. (Actual Intelligent Memory) repositories. **Flagship engine: [aim-agy](https://github.com/BrianV1981/aim-agy).**

**Active vessels (CLI hosts):**
- **[aim-agy](https://github.com/BrianV1981/aim-agy)** — Core engine (Antigravity / post–Gemini-CLI line). *Flagship.*
- **[aim-grok](https://github.com/BrianV1981/aim-grok)** — Grok CLI vessel (hybrid memory, GitOps, wiki).
- **[aim-opencode](https://github.com/BrianV1981/aim-opencode)** — OpenCode CLI vessel.
- **[aim-codex](https://github.com/BrianV1981/aim-codex)** — Codex-native vessel (**on the horizon** — not deprecated).

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
- **aim-claude / Anthropic-line vessels** — **Done.** Operator does not develop against Anthropic. Use aim-agy / aim-grok / aim-opencode (or aim-codex when ready).

Full map: see **aim-skills** `docs/AIM_ECOSYSTEM_MAP.md` or Operator artifact `AIM_ECOSYSTEM_MAP.md`.
<!-- AIM_ECOSYSTEM_END -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)