#!/usr/bin/env python3
import os
import json
import glob
from datetime import datetime

def get_session_workspaces():
    """Reads history.jsonl and maps session IDs to their workspaces."""
    history_file = os.path.expanduser("~/.gemini/antigravity-cli/history.jsonl")
    session_map = {}
    
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                        cid = data.get('conversationId')
                        workspace = data.get('workspace')
                        if cid and workspace:
                            session_map[cid] = workspace
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass
    return session_map

def list_sessions():
    brain_dir = os.path.expanduser("~/.gemini/antigravity-cli/brain/")
    if not os.path.exists(brain_dir):
        print(f"[ERROR] Brain directory not found at {brain_dir}")
        return

    session_map = get_session_workspaces()
    sessions = []
    
    # Iterate through all conversation folders in the brain
    for session_id in os.listdir(brain_dir):
        transcript_path = os.path.join(brain_dir, session_id, ".system_generated", "logs", "transcript.jsonl")
        
        # Check for transcript_full.jsonl as a fallback
        if not os.path.exists(transcript_path):
            transcript_path = os.path.join(brain_dir, session_id, ".system_generated", "logs", "transcript_full.jsonl")
            
        if os.path.exists(transcript_path):
            # Get last modified time
            mtime = os.path.getmtime(transcript_path)
            
            # Count how many turns roughly to show activity level
            try:
                with open(transcript_path, 'r') as f:
                    turns = sum(1 for line in f if line.strip())
            except Exception:
                turns = "?"
                
            workspace = session_map.get(session_id, "Unknown Workspace")
            
            sessions.append({
                "id": session_id,
                "timestamp": mtime,
                "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "workspace": workspace,
                "turns": turns
            })

    if not sessions:
        print("[*] No flight records found in the brain directory.")
        return

    # Sort descending by timestamp
    sessions.sort(key=lambda x: x["timestamp"], reverse=True)

    print(f"\n{'='*90}")
    print(f"{'DATE & TIME':<22} | {'SESSION ID (UUID)':<38} | {'TURNS':<6} | {'WORKSPACE'}")
    print(f"{'='*90}")
    
    for s in sessions:
        print(f"{s['date']:<22} | {s['id']:<38} | {str(s['turns']):<6} | {s['workspace']}")
    
    print(f"{'='*90}")
    print("\n[!] Tip: Copy a Session ID from above and pass it to the flight recorder:")
    print("    python3 scripts/flight_recorder.py --session-id <UUID> --mode cleaned\n")

if __name__ == "__main__":
    list_sessions()
