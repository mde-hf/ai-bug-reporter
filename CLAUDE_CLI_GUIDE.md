# Claude CLI Integration Guide

## Overview

This project now supports **Claude Code CLI** (just like Agento!), which allows you to use your company's AWS Bedrock access through a simple command-line interface. This means:

- ✅ **No personal Anthropic API key needed**
- ✅ **Uses your company's AWS Bedrock via SSO**
- ✅ **Automatic fallback to Anthropic API if available**
- ✅ **Works seamlessly in your web UI**

## How It Works

The system tries AI providers in this priority order:

```
1. Claude CLI (company AWS Bedrock via SSO)
   ↓ if fails
2. Anthropic API (personal account)
   ↓ if not configured
3. Rule-based generation (no AI)
```

## Setup

### Check if Claude CLI is Installed

```bash
which claude
```

**If you see a path** (e.g., `/opt/homebrew/bin/claude`):
- ✅ You're all set! The app will automatically detect and use it
- ✅ No configuration needed in `.env`
- ✅ AI features will use your company's AWS

**If you see nothing**:
- Install Claude CLI (ask your DevOps team or check internal docs)
- Or set up Anthropic API as backup (see below)

### Option 2: Anthropic API (Backup)

If Claude CLI isn't available, add to `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-api...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

Get your API key from: https://console.anthropic.com/

## Features Using AI

All these features will automatically use Claude CLI if available:

### 1. Test Case Generator
- Navigate to the "Test Case Generator" tab
- Enter a JIRA ticket link
- Click "Enhance with AI" to generate comprehensive test cases
- Uses Claude CLI → Anthropic API → Rule-based fallback

### 2. Multi-Agent System (Advanced)
- **Bug Analyzer**: Quality analysis and improvement suggestions
- **Duplicate Detective**: Semantic duplicate detection
- **Test Case Enhancer**: Iterative test case improvement
- **Bug Triage**: Auto-prioritization and squad assignment

All agents use the same fallback priority.

## Verification

### Check Startup Logs

When you start the app (`./start.sh`), look for:

```
✅ Claude CLI detected at: /opt/homebrew/bin/claude (using company AWS)
```

Or:

```
✅ Anthropic API available (personal account)
```

Or:

```
ℹ️  AI features will use fallback mode
```

### Test AI Features

1. Go to Test Case Generator tab
2. Enter a JIRA ticket: `https://hellofresh.atlassian.net/browse/REW-289`
3. Click "Generate Test Cases"
4. Check terminal logs to see which provider was used:
   - `[TestCaseGenerator] Trying Claude CLI...` → Using company AWS
   - `[TestCaseGenerator] Trying Anthropic API...` → Using personal API
   - `AI unavailable, using rule-based generation` → No AI provider

## How This Is Like Agento

Agento uses Claude Code CLI by calling it via `subprocess` from the backend. We do exactly the same:

```python
# In app.py and agents/base_agent.py
result = subprocess.run(
    [CLAUDE_CLI_PATH, '--model', 'sonnet', '--message', prompt],
    capture_output=True,
    text=True,
    timeout=120
)
```

This allows your web UI to leverage Claude via your company's AWS authentication, just like Agento does!

## Troubleshooting

### "Claude CLI not found"
- Run `which claude` to verify installation
- Check your PATH environment variable
- Contact DevOps for Claude CLI setup instructions

### "Claude CLI timeout"
- The timeout is set to 120 seconds
- For long test case generation, this is normal
- System will automatically fall back to Anthropic API

### "Empty response from Claude CLI"
- Check your AWS SSO authentication: `aws sso login`
- Verify your company's AWS Bedrock access
- Fall back to Anthropic API by setting `ANTHROPIC_API_KEY`

## Benefits

### Using Claude CLI (Company AWS)
- ✅ No personal API costs
- ✅ Company-level usage limits (higher)
- ✅ Centralized authentication (AWS SSO)
- ✅ Same experience as Agento

### Using Anthropic API (Personal)
- ✅ Works anywhere (no company VPN needed)
- ✅ Simple setup (just API key)
- ✅ Immediate availability

## Architecture

```
Web UI (React)
    ↓ HTTP Request
Flask Backend
    ↓
call_ai() function
    ↓
[Priority 1] → Claude CLI → subprocess call
    ↓ (if fails)
[Priority 2] → Anthropic API → direct API call
    ↓ (if not configured)
[Priority 3] → Rule-based generation
    ↓
Response to Web UI
```

All AI features (test case generator, multi-agent system) use this same architecture.

## Questions?

- Check Agento's implementation: `@agento` - we use the same pattern!
- See logs in terminal when running `./start.sh`
- Verify your setup: run `which claude` and check `.env` file
