# Google Drive Integration Setup

## Overview

This app can access Google Drive documents using your HelloFresh Google account credentials via OAuth2. This allows you to use org-restricted documents without making them public.

## Setup Steps

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your HelloFresh Google account
3. Create a new project (or use existing):
   - Click "Select a project" → "New Project"
   - Name: "Bug Reporter" (or similar)
   - Click "Create"

### 2. Enable Google Drive API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click "Enable"

### 3. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure consent screen:
   - User Type: **Internal** (HelloFresh users only)
   - App name: "Bug Reporter"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue" through all steps
4. Create OAuth client ID:
   - Application type: **Web application**
   - Name: "Bug Reporter Web"
   - Authorized redirect URIs: `http://localhost:5000/google/callback`
   - Click "Create"
5. **Download the JSON** or copy:
   - Client ID
   - Client Secret

### 4. Configure Your Application

Add to your `.env` file:

```bash
# Google Drive OAuth (Optional - for org-restricted docs)
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5000/google/callback
```

### 5. First-Time Authentication

1. Start the application: `./start.sh`
2. Visit: http://localhost:5000/google/auth
3. Sign in with your HelloFresh Google account
4. Click "Allow" to grant permissions
5. You'll be redirected back to the app
6. Credentials are saved for future use!

## How It Works

1. **First time:** You authenticate via Google OAuth
2. **Tokens saved:** Access token + refresh token stored securely
3. **Auto-refresh:** When access token expires, refresh token gets a new one
4. **Seamless access:** All Google Docs you can access work in the app

## Permissions Requested

- **Read-only access** to Google Drive
- **Scope:** `https://www.googleapis.com/auth/drive.readonly`
- **No writing:** App cannot modify your documents

## Security

- Tokens stored locally in `.env` (not in git)
- Only you can access your Google Drive
- HelloFresh org restrictions still apply
- Can revoke access anytime at: https://myaccount.google.com/permissions

## Troubleshooting

### "Access Denied" Error
- Check OAuth consent screen is set to "Internal"
- Verify you're using HelloFresh Google account

### "Redirect URI Mismatch"
- Ensure redirect URI in Google Cloud Console matches: `http://localhost:5000/google/callback`
- No trailing slash!

### Token Expired
- Visit: http://localhost:5000/google/auth to re-authenticate
- Or delete old tokens from `.env` and re-auth

## Usage

Once authenticated, simply paste any Google Docs URL in the Test Case Generator:
- Works with org-restricted docs ✅
- Works with "Anyone with link" docs ✅
- Works with your private docs ✅

No need to change sharing settings!
