#!/usr/bin/env python3
"""List AGY brain sessions and Grok vessel sessions for flight recording."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote


def get_session_workspaces() -> dict[str, str]:
    """Map AGY conversation IDs → workspace from history.jsonl."""
    history_file = os.path.expanduser("~/.gemini/antigravity-cli/history.jsonl")
    session_map: dict[str, str] = {}

    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        cid = data.get("conversationId")
                        workspace = data.get("workspace")
                        if cid and workspace:
                            session_map[cid] = workspace
                    except json.JSONDecodeError:
                        continue
        except OSError:
            pass
    return session_map


def collect_agy_sessions() -> list[dict]:
    brain_dir = os.path.expanduser("~/.gemini/antigravity-cli/brain/")
    sessions: list[dict] = []
    if not os.path.isdir(brain_dir):
        return sessions

    session_map = get_session_workspaces()
    for session_id in os.listdir(brain_dir):
        transcript_path = os.path.join(
            brain_dir,
            session_id,
            ".system_generated",
            "logs",
            "transcript.jsonl",
        )
        if not os.path.exists(transcript_path):
            transcript_path = os.path.join(
                brain_dir,
                session_id,
                ".system_generated",
                "logs",
                "transcript_full.jsonl",
            )
        if not os.path.exists(transcript_path):
            continue
        mtime = os.path.getmtime(transcript_path)
        try:
            with open(transcript_path, "r", encoding="utf-8") as f:
                turns = sum(1 for line in f if line.strip())
        except OSError:
            turns = "?"
        workspace = session_map.get(session_id, "Unknown Workspace")
        sessions.append(
            {
                "id": session_id,
                "timestamp": mtime,
                "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "workspace": workspace,
                "turns": turns,
                "vessel": "AGY",
            }
        )
    return sessions


def collect_grok_sessions() -> list[dict]:
    """Grok: ~/.grok/sessions/<urlencode(cwd)>/<session_id>/updates.jsonl"""
    grok_root = Path.home() / ".grok" / "sessions"
    sessions: list[dict] = []
    if not grok_root.is_dir():
        return sessions

    for updates in grok_root.glob("*/*/updates.jsonl"):
        session_id = updates.parent.name
        enc_cwd = updates.parent.parent.name
        try:
            workspace = unquote(enc_cwd)
        except Exception:
            workspace = enc_cwd
        try:
            mtime = updates.stat().st_mtime
        except OSError:
            continue
        try:
            with updates.open("r", encoding="utf-8") as f:
                turns = sum(1 for line in f if line.strip())
        except OSError:
            turns = "?"
        sessions.append(
            {
                "id": session_id,
                "timestamp": mtime,
                "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "workspace": workspace,
                "turns": turns,
                "vessel": "Grok",
            }
        )
    return sessions


def print_table(title: str, sessions: list[dict]) -> None:
    print(f"\n{'=' * 100}")
    print(title)
    print(f"{'=' * 100}")
    if not sessions:
        print("[*] No sessions found for this vessel.")
        return
    sessions = sorted(sessions, key=lambda x: x["timestamp"], reverse=True)
    print(
        f"{'DATE & TIME':<22} | {'VESSEL':<6} | {'SESSION ID':<38} | {'TURNS':<6} | WORKSPACE"
    )
    print(f"{'-' * 100}")
    for s in sessions:
        print(
            f"{s['date']:<22} | {s['vessel']:<6} | {s['id']:<38} | "
            f"{str(s['turns']):<6} | {s['workspace']}"
        )


def list_sessions() -> None:
    agy = collect_agy_sessions()
    grok = collect_grok_sessions()

    if not agy and not grok:
        print("[*] No flight records found.")
        print("    AGY brain:  ~/.gemini/antigravity-cli/brain/")
        print("    Grok logs:  ~/.grok/sessions/<cwd>/<session_id>/updates.jsonl")
        return

    # Combined, newest first
    combined = sorted(agy + grok, key=lambda x: x["timestamp"], reverse=True)
    print_table("ALL VESSELS (newest first)", combined)
    print_table("AGY / Antigravity only", agy)
    print_table("Grok only", grok)

    print(f"\n{'=' * 100}")
    print("[!] Tip: pass a Session ID to the flight recorder:")
    print("    python3 scripts/flight_recorder.py --session-id <ID> --mode cleaned")
    print("    python3 scripts/flight_recorder.py --input path/to/updates.jsonl")
    print()


if __name__ == "__main__":
    list_sessions()
