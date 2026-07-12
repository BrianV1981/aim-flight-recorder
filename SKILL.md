---
name: aim-flight-recorder
description: Generates clean, human-readable markdown summaries (Flight Records) of agent session transcripts from the Antigravity raw JSONL logs.
---

# 🛫 AIM-Flight-Recorder

You have access to the **A.I.M. Flight Recorder**, a forensic tool designed to parse the raw JSONL session logs in `~/.gemini/antigravity-cli/brain/` and extract human-readable Markdown summaries. 

Use this skill when the Operator asks you to "pull a flight record", "summarize the session", "clean up the log", or requests an audit of what happened in a past session or the current session.

## Usage Instructions

This skill provides two python scripts located in the `scripts/` directory.

### 1. Listing Available Sessions
To see a chronological list of all recorded sessions across all projects, use:
```bash
python3 /home/kingb/aim-flight-recorder/scripts/list_sessions.py
```
This will print a beautiful table showing the Date, Session UUID, Turn Count, and Workspace for every flight record in the Brain, making it easy to find the exact UUID you need.

### 2. Extracting a Flight Record
To generate the actual markdown summary, execute:
```bash
python3 /home/kingb/aim-flight-recorder/scripts/flight_recorder.py [OPTIONS]
```

### Arguments & Options

1. **`--session-id <UUID>`**: (Optional) The specific conversation UUID to extract. If omitted, the script will automatically parse the Operator's `history.jsonl` and detect the latest active session.
2. **`--output <FILE.md>`**: (Optional) Where to save the output markdown file. Defaults to `flight_record.md`.
3. **`--mode <MODE>`**: (Optional) Determines the verbosity of the extracted logs. Defaults to `cleaned`.
   - `full`: Extracts everything. Full agent responses, raw JSON payloads of tool calls, and complete terminal/tool output blocks (can be extremely long).
   - `cleaned`: (Recommended) Extracts agent responses and provides a concise one-line summary of each tool call (e.g., `- Executed run_command: Check git status`). Drops raw JSON and terminal outputs.
   - `chat_only`: Strips all tool calls completely. Only extracts the back-and-forth text messages between the Operator and the Agent.
   - `hybrid`: Extracts agent responses and the specific *target* of the tool call (e.g., the command line string or the targeted file path) but drops the raw outputs and JSON.

### Examples

**Example 1: Extracting a quick conversational chat log of the current session**
```bash
python3 /home/kingb/aim-flight-recorder/scripts/flight_recorder.py --mode chat_only --output chat_summary.md
```

**Example 2: Auditing a past session explicitly**
```bash
python3 /home/kingb/aim-flight-recorder/scripts/flight_recorder.py --session-id a1b2c3d4-5678-90ab-cdef-1234567890ab --mode hybrid --output audit_log.md
```

## Agentic Guidelines
- **Always confirm the mode**: If the Operator asks for a flight record but doesn't specify how detailed they want it, default to `--mode cleaned`, but remind them that `full`, `chat_only`, and `hybrid` are available if they need more or less granularity.
- **Do not read the full flight record blindly**: If you generate a `--mode full` flight record, DO NOT attempt to read the entire `.md` file back into your own context window via `view_file` unless explicitly asked, as it may overwhelm your memory. Simply tell the Operator where the file was saved.
