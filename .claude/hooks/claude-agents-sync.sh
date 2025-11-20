#!/bin/bash
#
# Claude/Agents Files Synchronization Hook Wrapper
#
# This script serves as a wrapper for the Python synchronization hook.
# It can be called directly or used as a Git hook.
#
# Usage:
#   ./claude-agents-sync.sh <file_path>
#   Or as a Git hook with FILE_PATH environment variable
#

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/claude-agents-sync.py"

# Check if Python script exists
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "Error: Python synchronization script not found at $PYTHON_SCRIPT" >&2
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not available" >&2
    exit 1
fi

# Get the file path (from argument or environment variable)
SYNC_FILE_PATH=""
if [[ $# -eq 1 ]]; then
    SYNC_FILE_PATH="$1"
elif [[ -n "$FILE_PATH" ]]; then
    SYNC_FILE_PATH="$FILE_PATH"
else
    echo "Error: No file path provided" >&2
    echo "Usage: $0 <file_path>" >&2
    echo "   or set FILE_PATH environment variable" >&2
    exit 1
fi

# Convert to absolute path if it's relative
if [[ "$SYNC_FILE_PATH" != /* ]]; then
    SYNC_FILE_PATH="$(cd "$(dirname "$SYNC_FILE_PATH")" && pwd)/$(basename "$SYNC_FILE_PATH")"
fi

# Export the file path for the Python script
export FILE_PATH="$SYNC_FILE_PATH"

# Run the Python script
python3 "$PYTHON_SCRIPT"

# Capture the exit code
EXIT_CODE=$?

# Exit with the same code as the Python script
exit $EXIT_CODE