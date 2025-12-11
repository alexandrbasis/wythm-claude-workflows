#!/usr/bin/env python3
"""
Claude/Agents Files Auto-Synchronization Hook

This hook automatically synchronizes claude.md and agents.md files whenever they are modified.
It works as a PostToolUse hook that triggers after file modifications.

The hook monitors:
1. Root level: claude.md ↔ agents.md
2. Backend level: backend/claude.md ↔ backend/AGENTS.md

Triggered when:
- Edit tool modifies any claude.md or agents.md file
- Write tool creates/modifies any claude.md or agents.md file
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def log_message(message: str, level: str = "INFO") -> None:
    """Log messages with timestamp"""
    import datetime

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        debug_log = Path(".claude/hooks/hook-debug.log")
        with open(debug_log, "a") as f:
            f.write(f"[AUTO-SYNC] {timestamp} {level}: {message}\n")
    except Exception:
        pass
    print(f"[{timestamp}] {level}: {message}")


def should_sync_file(file_path: str) -> bool:
    """Check if file should trigger synchronization"""
    file_path = Path(file_path).resolve()

    # Define files that should be synchronized
    sync_files = ["CLAUDE.md", "AGENTS.md"]

    return file_path.name in sync_files


def run_sync_hook(file_path: str) -> bool:
    """Run the synchronization hook for a given file"""
    try:
        script_path = Path(".claude/hooks/claude-agents-sync.sh")
        if not script_path.exists():
            log_message(f"Sync script not found: {script_path}", "ERROR")
            return False

        # Run the sync script
        result = subprocess.run(
            [script_path, file_path], capture_output=True, text=True, timeout=30
        )

        if result.returncode == 0:
            log_message(f"Successfully synced {file_path}")
            return True
        else:
            log_message(f"Sync failed for {file_path}: {result.stderr}", "ERROR")
            return False

    except subprocess.TimeoutExpired:
        log_message(f"Sync timeout for {file_path}", "ERROR")
        return False
    except Exception as e:
        log_message(f"Error running sync for {file_path}: {e}", "ERROR")
        return False


def extract_files_from_tool_input(tool_name: str, tool_input: dict) -> List[str]:
    """Extract file paths from different tool inputs"""
    files = []

    if tool_name == "Edit":
        file_path = tool_input.get("file_path", "")
        if file_path and should_sync_file(file_path):
            files.append(file_path)

    elif tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        if file_path and should_sync_file(file_path):
            files.append(file_path)

    elif tool_name == "Read":
        # Read operations don't need sync, but we log for debugging
        file_path = tool_input.get("file_path", "")
        if file_path and should_sync_file(file_path):
            log_message(f"Read operation on sync file: {file_path}", "DEBUG")

    return files


def main() -> None:
    """Main hook function"""
    try:
        # Read input from Claude
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Only process Edit and Write operations
        if tool_name not in ["Edit", "Write"]:
            sys.exit(0)

        # Extract files that need synchronization
        files_to_sync = extract_files_from_tool_input(tool_name, tool_input)

        if not files_to_sync:
            sys.exit(0)

        log_message(f"Detected modification of sync files: {files_to_sync}")

        # Run synchronization for each file
        success_count = 0
        for file_path in files_to_sync:
            if run_sync_hook(file_path):
                success_count += 1

        if success_count > 0:
            log_message(
                f"Auto-sync completed: {success_count}/{len(files_to_sync)} files synchronized"
            )
        else:
            log_message("Auto-sync failed for all files", "ERROR")

        sys.exit(0)

    except json.JSONDecodeError as e:
        log_message(f"JSON decode error: {e}", "ERROR")
        sys.exit(1)
    except Exception as e:
        log_message(f"Unexpected error: {e}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
