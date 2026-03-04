# Google Drive Integration - Quick Start

## ✅ What You Get

Access **HelloFresh org-restricted Google Docs** without making them public!

- ✅ Works with "Restricted to HelloFresh" documents
- ✅ Uses YOUR HelloFresh Google account (your permissions)
- ✅ No service account needed
- ✅ Automatic token refresh
- ✅ Falls back to public docs if not authenticated

## 🚀 Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
cd "/Users/mde/bug creation"
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with **your HelloFresh Google account**
3. Create project: "Bug Reporter"
4. Enable **Google Drive API**:
   - APIs & Services → Library
   - Search "Google Drive API" → Enable
5. Create OAuth credentials:
   - APIs & Services → Credentials → Create Credentials → OAuth client ID
   - Configure consent screen (if needed):
     - User Type: **Internal** (HelloFresh only)
     - App name: "Bug Reporter"
   - Application type: **Web application**
   - Authorized redirect URIs: `http://localhost:5000/google/callback`
   - Click **Create** and **Download JSON** or copy:
     - Client ID
     - Client Secret

### Step 3: Configure

Add to your `.env` file:

```bash
# Google Drive OAuth
GOOGLE_CLIENT_ID=123456-abc123.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcd1234efgh5678
GOOGLE_REDIRECT_URI=http://localhost:5000/google/callback
```

### Step 4: Authenticate (One Time)

```bash
#1. Start the app
./start.sh

# 2. Visit in browser:
open http://localhost:5000/google/auth

# 3. Sign in with HelloFresh Google account
# 4. Click "Allow"
# 5. You're done! ✅
```

## 🎯 How to Use

### In the Test Case Generator:

1. Paste any Google Docs URL (even org-restricted!)
2. Click "Generate Test Cases"
3. It works! 🎉

### What Works:

✅ **Org-restricted** ("Restricted to HelloFresh")
✅ **Team-restricted** ("Specific people")  
✅ **Public** ("Anyone with the link")
✅ **Your private docs**

All just work if YOU have access!

## 🔧 Troubleshooting

### "Not authenticated" Error

**Solution:** Visit http://localhost:5000/google/auth

### "Access Denied" from Google

**Check:**
- OAuth consent screen set to "Internal" (not External)
- You're signing in with HelloFresh Google account
- Redirect URI exactly matches: `http://localhost:5000/google/callback`

### Token Expired

**Solution:** Just visit `/google/auth` again to refresh

## 🔒 Security

- **Read-only access** - App cannot modify your docs
- **Tokens stored locally** in `.google_token.json` (not in git)
- **Auto-refresh** - Seamless re-authentication
- **Can revoke anytime** at https://myaccount.google.com/permissions

## 📝 Notes

- **First time only:** You need to authenticate
- **After that:** Tokens auto-refresh, no more auth needed
- **Fallback:** If not authenticated, tries public access
- **Works offline:** Cached tokens work without internet

## ✨ That's It!

You can now use org-restricted Google Docs in your Test Case Generator!

No more changing sharing settings 🎉
