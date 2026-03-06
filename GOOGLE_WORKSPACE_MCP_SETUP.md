# Google Workspace MCP Integration - Setup Guide

## ✅ Installation Complete!

The Google Workspace MCP server has been installed and configured in Cursor.

## 📋 Next Steps (Action Required)

To start using Google Workspace with AI, you need to authenticate:

### Step 1: Set Up OAuth Credentials

1. **Go to Google Cloud Console**: https://console.cloud.google.com/

2. **Create or select a project** (use existing HelloFresh project if available)

3. **Enable Required APIs**:
   - Visit: `https://console.cloud.google.com/apis/library?project=YOUR_PROJECT_ID`
   - Enable:
     - ✅ Google Drive API
     - ✅ Gmail API
     - ✅ Google Calendar API
     - ✅ Google Sheets API
     - ✅ Google Docs API

4. **Configure OAuth Consent Screen**:
   - Visit: `https://console.cloud.google.com/apis/credentials/consent?project=YOUR_PROJECT_ID`
   - Choose **External** (testing mode)
   - App name: "HelloFresh QA Tools" (or any name)
   - **IMPORTANT**: Add your @hellofresh.com email as a **Test User**

5. **Create OAuth Client**:
   - Visit: `https://console.cloud.google.com/apis/credentials?project=YOUR_PROJECT_ID`
   - Click **"Create Credentials"** → **"OAuth client ID"**
   - Application type: **Desktop app**
   - Name: "GWS CLI"
   - Click **"Create"**
   - **Download the JSON file**

6. **Save the Credentials**:
   ```bash
   # Move the downloaded file to the gws config directory:
   cp ~/Downloads/client_secret_*.json ~/.config/gws/client_secret.json
   ```

### Step 2: Authenticate

```bash
# Run this command to authenticate:
gws auth login -s drive,gmail,calendar,sheets,docs
```

- A browser window will open
- If you see "Google hasn't verified this app" → Click **"Advanced"** → **"Go to app (unsafe)"**
- Sign in with your @hellofresh.com Google account
- Grant the requested permissions
- Close the browser tab when you see "Authentication successful"

### Step 3: Test the Connection

```bash
# Test Drive access:
gws drive files list --params '{"pageSize": 5}'

# Test Gmail access:
gws gmail users messages list --params '{"userId": "me", "maxResults": 5}'
```

## 🎯 What You Can Do Now

Once authenticated, you can use AI to:

### 📁 **Google Drive**
- "List files in my Drive"
- "Upload this test report to Drive"
- "Create a folder called QA Reports"
- "Share this file with the team"

### 📧 **Gmail**
- "Show me recent emails from JIRA"
- "Send an email with the test results"
- "Search for emails about REW-323"

### 📅 **Calendar**
- "Show my calendar for today"
- "Create a meeting for QA review tomorrow at 2pm"
- "Find all sprint planning meetings"

### 📊 **Google Sheets**
- "Read test cases from this spreadsheet"
- "Update the test results in Sheet1"
- "Create a new spreadsheet for test tracking"

### 📝 **Google Docs**
- "Create a test plan document"
- "Read the content from this doc"
- "Update the QA documentation"

## 🔧 Configuration

MCP Server Location:
```
/Users/mde/.cursor/projects/Users-mde-bug-creation/mcps/google-workspace/
```

Configuration File:
```json
{
  "name": "google-workspace",
  "command": "gws",
  "args": ["mcp", "-s", "drive,gmail,calendar,sheets,docs"]
}
```

## 📚 Documentation

Full setup guide: `/Users/mde/.cursor/projects/Users-mde-bug-creation/mcps/google-workspace/README.md`

GitHub: https://github.com/googleworkspace/cli

## ⚠️ Common Issues

### "Access blocked" during login
→ You're not added as a test user. Go to OAuth consent screen and add your email.

### "Google hasn't verified this app"
→ Normal for testing mode. Click "Advanced" → "Go to app (unsafe)".

### "API not enabled"
→ Enable the API in Cloud Console using the URL provided in the error.

### Too many scopes error
→ Use: `gws auth login -s drive,gmail,calendar,sheets,docs` (specific services only)

## 🚀 Ready to Use

After authentication, simply ask the AI to interact with Google Workspace:
- "Upload my test report to Google Drive"
- "Create a spreadsheet from this test data"
- "Send an email summary of the test results"
- "Schedule a meeting for code review"

The AI will automatically use the Google Workspace MCP tools to complete your requests!
