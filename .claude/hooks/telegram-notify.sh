#!/bin/bash

# Telegram notification hook script
# Sends notifications about Claude Code events

# Read hook input from stdin
input=$(cat)

# Extract environment variables
BOT_TOKEN="${CLAUDE_HOOK_BOT_TOKEN}"
CHAT_ID="${CLAUDE_HOOK_CHAT_ID}"

# Exit if required env vars are missing
if [[ -z "$BOT_TOKEN" || -z "$CHAT_ID" ]]; then
    echo "Missing CLAUDE_HOOK_BOT_TOKEN or CLAUDE_HOOK_CHAT_ID" >&2
    exit 1
fi

# Parse event type from input
event_name=$(echo "$input" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('hook_event_name', 'Unknown'))")

# Create message based on event type
case "$event_name" in
    "Stop")
        message="🤖 Claude Code session completed"
        ;;
    "SubagentStop")
        message="🔧 Claude Code subagent task finished"
        ;;
    "Notification")
        notification_msg=$(echo "$input" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('message', 'Notification'))")
        message="🔔 $notification_msg"
        ;;
    *)
        message="📝 Claude Code event: $event_name"
        ;;
esac

# Send Telegram message
curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\":\"$CHAT_ID\",\"text\":\"$message\",\"parse_mode\":\"Markdown\"}" \
    > /dev/null

exit 0