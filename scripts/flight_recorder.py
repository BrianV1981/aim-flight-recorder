#!/usr/bin/env python3
"""A.I.M. Flight Recorder — human-readable markdown from session transcripts.

Supports:
  - AGY brain: ~/.gemini/antigravity-cli/brain/<id>/.../transcript.jsonl
  - Grok vessel: ~/.grok/sessions/<encoded-cwd>/<id>/updates.jsonl
  - Explicit --input path to either format
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional


def get_transcript_path(session_id: str) -> Optional[str]:
    """Resolve AGY brain transcript, then Grok updates.jsonl."""
    path = os.path.expanduser(
        f"~/.gemini/antigravity-cli/brain/{session_id}/.system_generated/logs/transcript.jsonl"
    )
    if os.path.exists(path):
        return path

    full_path = os.path.expanduser(
        f"~/.gemini/antigravity-cli/brain/{session_id}/.system_generated/logs/transcript_full.jsonl"
    )
    if os.path.exists(full_path):
        return full_path

    # Grok: scan session dirs for matching id
    grok_root = Path.home() / ".grok" / "sessions"
    if grok_root.is_dir():
        for updates in grok_root.glob(f"*/{session_id}/updates.jsonl"):
            return str(updates)
        # also flat id under encoded cwd already covered by glob
    return None


def _looks_like_grok_updates(file_path: str) -> bool:
    base = os.path.basename(file_path)
    if base == "updates.jsonl":
        return True
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for _ in range(20):
                line = f.readline()
                if not line.strip():
                    continue
                msg = json.loads(line)
                if not isinstance(msg, dict):
                    continue
                if msg.get("method") == "session/update":
                    return True
                u = (msg.get("params") or {}).get("update") or {}
                if u.get("sessionUpdate"):
                    return True
    except (OSError, json.JSONDecodeError, TypeError):
        pass
    return False


def parse_transcript(file_path: str, mode: str = "cleaned") -> str:
    if _looks_like_grok_updates(file_path):
        return parse_grok_updates(file_path, mode=mode)
    return parse_agy_transcript(file_path, mode=mode)


def parse_agy_transcript(file_path: str, mode: str = "cleaned") -> str:
    markdown_lines = [f"# Flight Recorder: {mode.upper()}", ""]

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                turn = json.loads(line)
            except json.JSONDecodeError:
                continue

            step_type = turn.get("type", "")
            content = turn.get("content", "")

            if step_type == "USER_INPUT":
                markdown_lines.append("## 👤 Operator")
                markdown_lines.append(f"> {str(content).strip()}")
                markdown_lines.append("")

            elif step_type == "PLANNER_RESPONSE":
                if str(content).strip():
                    markdown_lines.append("## 🤖 Agent")
                    markdown_lines.append(str(content).strip())
                    markdown_lines.append("")

                tool_calls = turn.get("tool_calls", [])
                if tool_calls and mode != "chat_only":
                    markdown_lines.append("### 🛠️ Actions Taken")
                    for tc in tool_calls:
                        name = tc.get("function_name", "tool")
                        args = tc.get("args", {})

                        if mode == "full":
                            markdown_lines.append(f"**{name}**")
                            markdown_lines.append("```json")
                            markdown_lines.append(json.dumps(args, indent=2))
                            markdown_lines.append("```")
                        elif mode == "cleaned":
                            summary = args.get(
                                "toolSummary", args.get("toolAction", name)
                            )
                            markdown_lines.append(f"- Executed `{name}`: {summary}")
                        elif mode == "hybrid":
                            target = args.get(
                                "CommandLine",
                                args.get(
                                    "TargetFile",
                                    args.get(
                                        "AbsolutePath",
                                        args.get("DirectoryPath", ""),
                                    ),
                                ),
                            )
                            if not target:
                                target = args.get("toolSummary", name)
                            markdown_lines.append(f"- **{name}**: `{target}`")
                    markdown_lines.append("")

            elif step_type == "TOOL_RESPONSE":
                if mode == "full":
                    markdown_lines.append("### 📡 Tool Output")
                    markdown_lines.append("```text")
                    out = str(content).strip()
                    if len(out) > 5000:
                        out = out[:5000] + "\n... [TRUNCATED] ..."
                    markdown_lines.append(out)
                    markdown_lines.append("```")
                    markdown_lines.append("")

    return "\n".join(markdown_lines)


def _flatten_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        if content.get("type") == "text":
            return str(content.get("text") or "")
        return str(content.get("text") or content.get("message") or "")
    if isinstance(content, list):
        parts = []
        for item in content:
            parts.append(_flatten_text(item))
        return "".join(parts)
    return str(content)


def parse_grok_updates(file_path: str, mode: str = "cleaned") -> str:
    """Rebuild Operator/Agent turns from Grok session updates.jsonl."""
    session_id = "unknown"
    lines_out: list[str] = [
        f"# Flight Recorder: {mode.upper()}",
        "",
        f"**Source:** `{file_path}`",
        f"**Format:** Grok `updates.jsonl`",
        "",
    ]

    # Accumulate assistant text / tools between user turns
    agent_buf: list[str] = []
    tools: list[dict] = []
    tool_results: list[str] = []

    def flush_agent() -> None:
        nonlocal agent_buf, tools, tool_results
        if not agent_buf and not tools and not tool_results:
            return
        text = "".join(agent_buf).strip()
        if text or mode == "chat_only":
            if text:
                lines_out.append("## 🤖 Agent")
                lines_out.append(text)
                lines_out.append("")
        if tools and mode != "chat_only":
            lines_out.append("### 🛠️ Actions Taken")
            for tc in tools:
                name = tc.get("name") or tc.get("tool") or "tool"
                args = tc.get("args") or tc.get("input") or {}
                if mode == "full":
                    lines_out.append(f"**{name}**")
                    lines_out.append("```json")
                    try:
                        lines_out.append(json.dumps(args, indent=2)[:8000])
                    except TypeError:
                        lines_out.append(str(args)[:8000])
                    lines_out.append("```")
                elif mode == "cleaned":
                    summary = ""
                    if isinstance(args, dict):
                        summary = (
                            args.get("description")
                            or args.get("command")
                            or args.get("target_file")
                            or args.get("file_path")
                            or args.get("query")
                            or ""
                        )
                    if not summary:
                        summary = name
                    if isinstance(summary, str) and len(summary) > 200:
                        summary = summary[:200] + "…"
                    lines_out.append(f"- Executed `{name}`: {summary}")
                elif mode == "hybrid":
                    target = ""
                    if isinstance(args, dict):
                        target = (
                            args.get("command")
                            or args.get("target_file")
                            or args.get("file_path")
                            or args.get("path")
                            or args.get("url")
                            or args.get("query")
                            or ""
                        )
                    lines_out.append(f"- **{name}**: `{target or name}`")
            lines_out.append("")
        if tool_results and mode == "full":
            for out in tool_results:
                lines_out.append("### 📡 Tool Output")
                lines_out.append("```text")
                chunk = out.strip()
                if len(chunk) > 5000:
                    chunk = chunk[:5000] + "\n... [TRUNCATED] ..."
                lines_out.append(chunk)
                lines_out.append("```")
                lines_out.append("")
        agent_buf = []
        tools = []
        tool_results = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(msg, dict):
                continue
            params = msg.get("params") or {}
            if params.get("sessionId"):
                session_id = params["sessionId"]
            update = params.get("update") or {}
            kind = update.get("sessionUpdate") or ""

            if kind == "user_message_chunk":
                flush_agent()
                text = _flatten_text(update.get("content"))
                if text.strip():
                    lines_out.append("## 👤 Operator")
                    lines_out.append(f"> {text.strip()}")
                    lines_out.append("")
                continue

            if kind == "agent_message_chunk":
                agent_buf.append(_flatten_text(update.get("content")))
                continue

            if kind in ("tool_call", "agent_tool_call", "function_call"):
                name = (
                    update.get("name")
                    or update.get("toolName")
                    or update.get("tool")
                    or "tool"
                )
                args = (
                    update.get("arguments")
                    or update.get("args")
                    or update.get("input")
                    or {}
                )
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {"raw": args}
                tools.append({"name": name, "args": args})
                continue

            if kind in ("tool_call_update", "tool_result", "function_call_output"):
                if mode == "full":
                    content = update.get("content") or update.get("output") or update
                    tool_results.append(_flatten_text(content) or json.dumps(update)[:2000])
                continue

            # Some Grok builds put assistant text under different keys
            if kind in ("agent_thought_chunk",):
                if mode == "full":
                    t = _flatten_text(update.get("content"))
                    if t.strip():
                        agent_buf.append(f"\n_Thought:_ {t.strip()}\n")
                continue

    flush_agent()

    # Header session id
    if session_id != "unknown":
        lines_out.insert(2, f"**Session ID:** `{session_id}`")
        lines_out.insert(3, "")

    return "\n".join(lines_out)


def get_latest_session_id() -> Optional[str]:
    # Prefer latest Grok session under aim-grok cwd encoding
    grok_root = Path.home() / ".grok" / "sessions"
    candidates: list[tuple[float, str]] = []
    if grok_root.is_dir():
        for updates in grok_root.glob("*/**/updates.jsonl"):
            # path: sessions/<enc>/<session-id>/updates.jsonl
            sid = updates.parent.name
            try:
                mtime = updates.stat().st_mtime
            except OSError:
                continue
            candidates.append((mtime, sid))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    history_file = os.path.expanduser("~/.gemini/antigravity-cli/history.jsonl")
    current_dir = os.path.abspath(os.getcwd())
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    if data.get("workspace") == current_dir:
                        return data.get("conversationId")
                for line in reversed(lines):
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    if data.get("conversationId"):
                        return data.get("conversationId")
        except Exception:
            pass
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A.I.M. Flight Recorder: Extract session markdown from transcripts."
    )
    parser.add_argument(
        "--session-id",
        default=None,
        help="Session ID to extract. Defaults to latest Grok/AGY session.",
    )
    parser.add_argument(
        "--input",
        "-i",
        default=None,
        help="Explicit path to transcript.jsonl or Grok updates.jsonl",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "cleaned", "chat_only", "hybrid"],
        default="cleaned",
        help="full | cleaned | chat_only | hybrid",
    )
    parser.add_argument(
        "--output", "-o", default="flight_record.md", help="Output Markdown file."
    )
    args = parser.parse_args()

    if args.input:
        path = os.path.expanduser(args.input)
        if not os.path.isfile(path):
            print(f"[ERROR] Input not found: {path}")
            sys.exit(1)
        print(f"[*] Reading blackbox data from {path}...")
        md_content = parse_transcript(path, mode=args.mode)
    else:
        session_id = args.session_id
        if not session_id:
            print("[*] No session ID provided. Auto-detecting latest session...")
            session_id = get_latest_session_id()
            if not session_id:
                print(
                    "[ERROR] Could not auto-detect session ID. Provide --session-id or --input."
                )
                sys.exit(1)
            print(f"[*] Found Session ID: {session_id}")

        path = get_transcript_path(session_id)
        if not path:
            print(f"[ERROR] Could not find transcript for session {session_id}")
            sys.exit(1)

        print(f"[*] Reading blackbox data from {path}...")
        md_content = parse_transcript(path, mode=args.mode)

    out_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(
        f"[SUCCESS] Flight Record generated at {out_path} using mode '{args.mode}'."
    )


if __name__ == "__main__":
    main()
