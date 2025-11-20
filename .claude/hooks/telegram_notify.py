#!/usr/bin/env python3
"""
Simple Telegram notification hook for Claude Code
Sends short messages about operations
"""

import json
import os
import subprocess
import sys


def send_telegram_message(message):
    """Send message to Telegram"""
    bot_token = os.environ.get("CLAUDE_HOOK_BOT_TOKEN")
    chat_id = os.environ.get("CLAUDE_HOOK_CHAT_ID")

    if not bot_token or not chat_id:
        print("⚠️ Telegram credentials not set", file=sys.stderr)
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    try:
        # Use proper URL encoding to avoid issues with special characters
        import urllib.parse

        encoded_message = urllib.parse.quote_plus(message)

        result = subprocess.run(
            [
                "curl",
                "-s",
                "-X",
                "POST",
                url,
                "-d",
                f"chat_id={chat_id}",
                "-d",
                f"text={encoded_message}",
                "-d",
                "parse_mode=HTML",
            ],
            capture_output=True,
            check=True,
            text=True,
        )
        print(f"✅ Sent: {message}", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to send Telegram message: {e.stderr}", file=sys.stderr)
        return False


def main():
    try:
        stdin_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)

    hook_event = stdin_data.get("hook_event_name", "")

    # Simple messages for each event type
    if hook_event == "Notification":
        notification_msg = stdin_data.get("message", "")
        if "permission" in notification_msg.lower():
            send_telegram_message("🔐 Permission needed")
        elif "waiting" in notification_msg.lower():
            send_telegram_message("⏳ Waiting for input")
        else:
            send_telegram_message(f"📢 {notification_msg[:50]}")

    elif hook_event == "Stop":
        send_telegram_message("✅ Task completed")

    elif hook_event == "SubagentStop":
        send_telegram_message("🎯 Subtask done")


if __name__ == "__main__":
    main()
    sys.exit(0)
