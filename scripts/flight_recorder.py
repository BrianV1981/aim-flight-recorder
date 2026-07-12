#!/usr/bin/env python3
import os
import sys
import json
import argparse

def get_transcript_path(session_id):
    path = os.path.expanduser(f"~/.gemini/antigravity-cli/brain/{session_id}/.system_generated/logs/transcript.jsonl")
    if os.path.exists(path):
        return path
    
    # Check if full transcript exists
    full_path = os.path.expanduser(f"~/.gemini/antigravity-cli/brain/{session_id}/.system_generated/logs/transcript_full.jsonl")
    if os.path.exists(full_path):
        return full_path
    return None

def parse_transcript(file_path, mode="cleaned"):
    markdown_lines = [f"# Flight Recorder: {mode.upper()}", ""]
    
    with open(file_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            try:
                turn = json.loads(line)
            except json.JSONDecodeError:
                continue
                
            step_type = turn.get("type", "")
            source = turn.get("source", "")
            content = turn.get("content", "")
            
            # Formatting logic based on the 4 modes
            if step_type == "USER_INPUT":
                markdown_lines.append(f"## 👤 Operator")
                markdown_lines.append(f"> {content.strip()}")
                markdown_lines.append("")
            
            elif step_type == "PLANNER_RESPONSE":
                if content.strip():
                    markdown_lines.append(f"## 🤖 Agent")
                    markdown_lines.append(f"{content.strip()}")
                    markdown_lines.append("")
                
                tool_calls = turn.get("tool_calls", [])
                if tool_calls and mode != "chat_only":
                    markdown_lines.append(f"### 🛠️ Actions Taken")
                    for tc in tool_calls:
                        name = tc.get("function_name", "tool")
                        args = tc.get("args", {})
                        
                        if mode == "full":
                            markdown_lines.append(f"**{name}**")
                            markdown_lines.append("```json")
                            markdown_lines.append(json.dumps(args, indent=2))
                            markdown_lines.append("```")
                        elif mode == "cleaned":
                            # Show summary or brief arguments
                            summary = args.get("toolSummary", args.get("toolAction", name))
                            markdown_lines.append(f"- Executed `{name}`: {summary}")
                        elif mode == "hybrid":
                            # The 'in-between' mode: Show command/file targeted, but not giant payloads
                            target = args.get("CommandLine", args.get("TargetFile", args.get("AbsolutePath", args.get("DirectoryPath", ""))))
                            if not target:
                                target = args.get("toolSummary", name)
                            markdown_lines.append(f"- **{name}**: `{target}`")
                    markdown_lines.append("")
                    
            elif step_type == "TOOL_RESPONSE":
                if mode == "full":
                    markdown_lines.append(f"### 📡 Tool Output")
                    markdown_lines.append("```text")
                    # Truncate if too massive even in full mode, or print as is
                    out = content.strip()
                    if len(out) > 5000:
                        out = out[:5000] + "\n... [TRUNCATED] ..."
                    markdown_lines.append(out)
                    markdown_lines.append("```")
                    markdown_lines.append("")

    return "\n".join(markdown_lines)

def get_latest_session_id():
    history_file = os.path.expanduser("~/.gemini/antigravity-cli/history.jsonl")
    current_dir = os.path.abspath(os.getcwd())
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                lines = f.readlines()
                # Read backwards to find the most recent session for this directory
                for line in reversed(lines):
                    if not line.strip(): continue
                    data = json.loads(line)
                    if data.get('workspace') == current_dir:
                        return data.get('conversationId')
                
                # Fallback: just grab the very latest session if none matches the dir
                for line in reversed(lines):
                    if not line.strip(): continue
                    data = json.loads(line)
                    if data.get('conversationId'):
                        return data.get('conversationId')
        except Exception:
            pass
    return None

def main():
    parser = argparse.ArgumentParser(description="A.I.M. Flight Recorder: Extract beautiful session markdown from transcripts.")
    parser.add_argument("--session-id", default=None, help="The Session ID to extract. Defaults to the latest session.")
    parser.add_argument("--mode", choices=["full", "cleaned", "chat_only", "hybrid"], default="cleaned",
                        help="full: Everything including outputs.\n"
                             "cleaned: Summarized tool calls, no outputs.\n"
                             "chat_only: Only Operator and Agent chat.\n"
                             "hybrid: Tool arguments but no outputs.")
    parser.add_argument("--output", "-o", default="flight_record.md", help="Output Markdown file.")
    args = parser.parse_args()

    session_id = args.session_id
    if not session_id:
        print("[*] No session ID provided. Auto-detecting latest session...")
        session_id = get_latest_session_id()
        if not session_id:
            print("[ERROR] Could not auto-detect session ID. Please provide --session-id.")
            sys.exit(1)
        print(f"[*] Found Session ID: {session_id}")

    path = get_transcript_path(session_id)
    if not path:
        print(f"[ERROR] Could not find transcript for session {session_id}")
        sys.exit(1)
        
    print(f"[*] Reading blackbox data from {path}...")
    md_content = parse_transcript(path, mode=args.mode)
    
    with open(args.output, "w") as f:
        f.write(md_content)
        
    print(f"[SUCCESS] Flight Record generated at {os.path.abspath(args.output)} using mode '{args.mode}'.")

if __name__ == "__main__":
    main()
