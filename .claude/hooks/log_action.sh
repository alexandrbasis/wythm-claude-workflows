#!/bin/bash
# Log detailed tool usage
input_json=$(cat)
tool_name=$(echo "$input_json" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('tool_name', ''))")
tool_input=$(echo "$input_json" | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data.get('tool_input', {})))")

# Format action description
case "$tool_name" in
    "Edit"|"MultiEdit")
        file_path=$(echo "$tool_input" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('file_path', '').split('/')[-1])")
        action="✏️ Edited $file_path"
        ;;
    "Write")
        file_path=$(echo "$tool_input" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('file_path', '').split('/')[-1])")
        action="📝 Created $file_path"
        ;;
    "Bash")
        command=$(echo "$tool_input" | python3 -c "import sys, json; data=json.load(sys.stdin); cmd=data.get('command', ''); print(cmd[:50] + '...' if len(cmd) > 50 else cmd)")
        action="💻 Ran: $command"
        ;;
    *)
        action="🔧 Used $tool_name"
        ;;
esac

# Save last action
echo "$action" > /tmp/claude_last_action.txt