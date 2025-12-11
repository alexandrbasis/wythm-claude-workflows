---
name: gemini-cli
description: Wield Google's Gemini CLI as a powerful auxiliary tool for code generation, review, analysis, and web research. Use when tasks benefit from a second AI perspective, current web information via Google Search, codebase architecture analysis, or parallel code generation. Also use when user explicitly requests Gemini operations.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
---

# Gemini CLI Integration Skill

This skill enables Claude Code to effectively orchestrate Gemini CLI (v0.16.0+) with Gemini 3 Pro for code generation, review, analysis, and specialized tasks.

## When to Use This Skill

### Ideal Use Cases

1. **Second Opinion / Cross-Validation**
   - Code review after writing code (different AI perspective)
   - Security audit with alternative analysis
   - Finding bugs Claude might have missed

2. **Google Search Grounding**
   - Questions requiring current internet information
   - Latest library versions, API changes, documentation updates
   - Current events or recent releases

3. **Codebase Architecture Analysis**
   - Use Gemini's `codebase_investigator` tool
   - Understanding unfamiliar codebases
   - Mapping cross-file dependencies

4. **Parallel Processing**
   - Offload tasks while continuing other work
   - Run multiple code generations simultaneously
   - Background documentation generation

5. **Specialized Generation**
   - Test suite generation
   - JSDoc/documentation generation
   - Code translation between languages

### When NOT to Use

- Simple, quick tasks (overhead not worth it)
- Tasks requiring immediate response (rate limits cause delays)
- When context is already loaded and understood
- Interactive refinement requiring conversation

## Core Instructions

### 1. Verify Installation

```bash
command -v gemini || which gemini
```

### 2. Basic Command Pattern

```bash
gemini "[prompt]" --yolo -o text 2>&1
```

Key flags:
- `--yolo` or `-y`: Auto-approve all tool calls
- `-o text`: Human-readable output
- `-o json`: Structured output with stats
- `-m gemini-2.5-flash`: Use faster model for simple tasks

### 3. Critical Behavioral Notes

**YOLO Mode Behavior**: Auto-approves tool calls but does NOT prevent planning prompts. Gemini may still present plans and ask "Does this plan look good?" Use forceful language:
- "Apply now"
- "Start immediately"
- "Do this without asking for confirmation"

**Rate Limits**: Free tier has 60 requests/min, 1000/day. CLI auto-retries with backoff. Expect messages like "quota will reset after Xs".

### 4. Output Processing

For JSON output (`-o json`), parse:
```json
{
  "response": "actual content",
  "stats": {
    "models": { "tokens": {...} },
    "tools": { "byName": {...} }
  }
}
```

## Quick Reference Commands

### Code Generation
```bash
gemini "Create [description] with [features]. Output complete file content." --yolo -o text
```

### Code Review
```bash
gemini "Review [file] for: 1) features, 2) bugs/security issues, 3) improvements" -o text
```

### Bug Fixing
```bash
gemini "Fix these bugs in [file]: [list]. Apply fixes now." --yolo -o text
```

### Test Generation
```bash
gemini "Generate [Jest/pytest] tests for [file]. Focus on [areas]." --yolo -o text
```

### Documentation
```bash
gemini "Generate JSDoc for all functions in [file]. Output as markdown." --yolo -o text
```

### Architecture Analysis
```bash
gemini "Use codebase_investigator to analyze this project" -o text
```

### Web Research
```bash
gemini "What are the latest [topic]? Use Google Search." -o text
```

### Faster Model (Simple Tasks)
```bash
gemini "[prompt]" -m gemini-2.5-flash -o text
```

## Error Handling

### Rate Limit Exceeded
- CLI auto-retries with backoff
- Use `-m gemini-2.5-flash` for lower priority tasks
- Run in background for long operations

### Command Failures
- Check JSON output for detailed error stats
- Verify Gemini is authenticated: `gemini --version`
- Check `~/.gemini/settings.json` for config issues

### Validation After Generation
Always verify Gemini's output:
- Check for security vulnerabilities (XSS, injection)
- Test functionality matches requirements
- Review code style consistency
- Verify dependencies are appropriate

## Integration Workflow

### Standard Generate-Review-Fix Cycle

```bash
# 1. Generate
gemini "Create [code]" --yolo -o text

# 2. Review (Gemini reviews its own work)
gemini "Review [file] for bugs and security issues" -o text

# 3. Fix identified issues
gemini "Fix [issues] in [file]. Apply now." --yolo -o text
```

### Background Execution

For long tasks, run in background and monitor:
```bash
gemini "[long task]" --yolo -o text 2>&1 &
# Monitor with BashOutput tool
```

## Gemini's Unique Capabilities

These tools are available only through Gemini:

1. **google_web_search** - Real-time internet search via Google
2. **codebase_investigator** - Deep architectural analysis
3. **save_memory** - Cross-session persistent memory
4. **generate_image** - AI image generation via nanobanana extension

## Image Generation

Gemini CLI supports image generation through the **nanobanana** extension.

### Prerequisites

The API key must be set in environment (already configured in `~/.zshrc`):
```bash
export NANOBANANA_GEMINI_API_KEY="your-key-here"
```

To get a key: [Google AI Studio](https://aistudio.google.com/app/apikey)

### Generate Image Command

```bash
gemini "Generate an image of [description]. Save it to /tmp/image-name.png" --yolo -o text 2>&1
```

### Model Selection (Optional)

```bash
# Default: gemini-2.5-flash-image (faster)
# For higher quality:
export NANOBANANA_MODEL="gemini-3-pro-image-preview"
```

### Rate Limits for Image Generation

**Important**: Image generation requires a paid tier or has very limited free quota.
- Free tier: ~0 requests (quota resets periodically)
- Paid Tier 1: 500 RPM for flash, 20 RPM for pro
- If quota exceeded, wait ~50 seconds and retry

### Example Prompts

```bash
# Product mockup
gemini "Generate an image of a mobile app interface for vocabulary learning with dark mode. Save to /tmp/app-mockup.png" --yolo -o text

# Illustration
gemini "Generate a cute robot mascot reading books in a cozy library. Save to /tmp/mascot.png" --yolo -o text

# Icon/Logo
gemini "Generate a minimalist logo for a language learning app, blue and white colors. Save to /tmp/logo.png" --yolo -o text
```

## Configuration

### Project Context (Optional)

Create `.gemini/GEMINI.md` in project root for persistent context that Gemini will automatically read.

### Session Management

List sessions: `gemini --list-sessions`
Resume session: `echo "follow-up" | gemini -r [index] -o text`

## See Also

- `reference.md` - Complete command and flag reference
- `templates.md` - Prompt templates for common operations
- `patterns.md` - Advanced integration patterns
- `tools.md` - Gemini's built-in tools documentation
