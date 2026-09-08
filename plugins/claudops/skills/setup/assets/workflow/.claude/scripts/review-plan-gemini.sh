#!/usr/bin/env bash
# Legacy ExitPlanMode hook name; delegates to the shared Antigravity adapter.
set -u

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
[ "$TOOL_NAME" = "ExitPlanMode" ] || exit 0
PLAN_CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_response.plan // empty' 2>/dev/null)
PLAN_FILE=$(printf '%s' "$INPUT" | jq -r '.tool_response.filePath // empty' 2>/dev/null)
[ -n "$PLAN_CONTENT" ] || exit 0
if [ -z "$PLAN_FILE" ] || [ ! -f "$PLAN_FILE" ]; then
  jq -n '{systemMessage: "Antigravity review unavailable: plan file not found"}'
  exit 0
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
RUNNER="$SCRIPT_DIR/../skills/antigravity-cli/scripts/review.py"
RUN_DIR=$(mktemp -d "${TMPDIR:-/tmp}/claudops-agy-plan.XXXXXX") || exit 1
PROMPT_FILE="$RUN_DIR/prompt.txt"
{
  printf 'Review the implementation plan below. Repository: %s\n' "$PWD"
  printf '%s\n' 'Use only the supplied material. Do not use tools, edit files, or run shell commands.'
  printf '%s\n' 'Check correctness, edge cases, security, compatibility, and testability. Return a concise final review with actionable findings and evidence gaps.'
  printf '\nPLAN:\n%s\n' "$PLAN_CONTENT"
} > "$PROMPT_FILE"

if ! python3 "$RUNNER" --prompt-file "$PROMPT_FILE" --timeout 240 --output-dir "$RUN_DIR/result" > /dev/null 2> "$RUN_DIR/adapter.stderr.log"; then
  jq -n --arg path "$RUN_DIR" '{systemMessage: ("Antigravity review incomplete; plan unchanged. Diagnostics: " + $path)}'
  exit 0
fi
REVIEW=$(cat "$RUN_DIR/result/response.txt")
if ! printf '\n---\n\n## Antigravity Review\n\n%s\n' "$REVIEW" >> "$PLAN_FILE"; then
  jq -n --arg path "$RUN_DIR" '{systemMessage: ("Antigravity review could not be appended. Result: " + $path)}'
  exit 0
fi
jq -n --arg review "$REVIEW" --arg file "$PLAN_FILE" --arg path "$RUN_DIR/result/receipt.json" \
  '{additionalContext: ("## Antigravity Plan Review\n\nReview added to: " + $file + "\nReceipt: " + $path + "\n\n" + $review)}'
