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

### 🧬 The A.I.M. Ecosystem

This project is a dedicated skill plugin operating within the broader A.I.M. Ecosystem. 

- **[aim-agy](https://github.com/BrianV1981/aim-agy):** The Core Engine (Built for Antigravity CLI). *This is the flagship repository.*
- **[aim-opencode](https://github.com/BrianV1981/aim-opencode):** Core adaptation for the OpenCode ecosystem.
- **[aim](https://github.com/BrianV1981/aim):** The original framework built for Google's Gemini CLI.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)