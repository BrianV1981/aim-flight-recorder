# 🗺️ Roadmap: A.I.M. Flight Recorder

The Flight Recorder is currently in `v1.0.0`. It successfully bridges the gap between raw, highly technical JSONL Antigravity logs and human-readable markdown summaries.

Here is the planned roadmap for future development:

## Phase 1: Core Scripting (Current)
- [x] Basic `jsonl` extraction engine (`flight_recorder.py`)
- [x] Multiple formatting modes (`full`, `cleaned`, `hybrid`, `chat_only`)
- [x] Global history parsing and session auto-detection
- [x] Session cataloging and sorting (`list_sessions.py`)
- [x] Formal Antigravity CLI Skill scaffolding (`SKILL.md`)

## Phase 2: Interactive TUI & Quality of Life
- [ ] **Interactive Menu**: Merge `list_sessions.py` and `flight_recorder.py` into a single Text User Interface (TUI) using `curses` or `rich`. Allow the operator to scroll through sessions with the arrow keys and hit `Enter` to generate a report.
- [ ] **Custom Mode Checkboxes**: Allow operators to explicitly toggle what gets included (e.g., `[x] Tool Payloads`, `[ ] Tool Outputs`, `[x] Agent Thoughts`).
- [ ] **Artifact Integration**: Add a dedicated parsing logic to render generated Markdown artifacts as collapsible blocks.

## Phase 3: Analytics & Auditing
- [ ] **Token Usage & Time Metrics**: Parse the timestamps inside the logs to calculate exact session duration, idle time, and estimated token usage.
- [ ] **Error Spotlighting**: Automatically highlight or flag tools that returned `[ERROR]` or non-zero exit codes to make debugging failed agent trajectories easier.
- [ ] **Ghost Hunting**: Identify and label sessions that were "killed" or abruptly terminated without a clean exit.

## Phase 4: Ecosystem Integrations
- [ ] **A.I.M. Reincarnation Hook**: Seamlessly hook the Flight Recorder into the A.I.M. `session_summarizer.py` daemon so that every time an agent reincarnates, a cleaned flight record is automatically archived into the `memory-wiki`.
- [ ] **Automated Pastebin/Gist**: Add a `--share` flag that automatically pushes the generated Markdown to a GitHub Gist (or similar service) and returns a shortlink for easy sharing with other developers.
