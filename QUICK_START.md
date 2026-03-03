# Quick Start Guide - Share with Your Team

## For the Person Setting This Up

### 1. Get Your Jira API Token
- Go to: https://id.atlassian.com/manage-profile/security/api-tokens
- Click "Create API token"
- Name it "Bug Reporter" and copy the token

### 2. Quick Setup (5 minutes)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create your config file
cp .env.example .env

# Edit .env and add your Jira email and API token
# (use any text editor: nano, vim, VSCode, etc.)
nano .env
```

### 3. Run It

```bash
python app.py
```

Visit: http://localhost:5000

## Sharing with Your Team

### Option A: Same Office/WiFi Network (Easiest - 2 minutes)

1. Find your computer's IP address:
   ```bash
   # Mac/Linux:
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Windows:
   ipconfig
   ```
   Look for something like `192.168.1.xxx` or `10.0.0.xxx`

2. Keep `python app.py` running on your computer

3. Share this URL with your team:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

**Pros**: Super fast, no deployment needed
**Cons**: Only works when your computer is on and on same network

### Option B: Deploy to Railway (Free & Easy - 10 minutes)

Railway is the easiest free deployment option. No credit card required for basic usage.

1. Push this code to GitHub (if not already):
   ```bash
   git init
   git add .
   git commit -m "Bug reporter tool"
   gh repo create bug-reporter --private --source=. --remote=origin --push
   ```

2. Go to [railway.app](https://railway.app) and sign up with GitHub

3. Click "New Project" → "Deploy from GitHub repo"

4. Select your `bug-reporter` repository

5. Add environment variables in Railway dashboard:
   - Click on your service
   - Go to "Variables" tab
   - Add these variables:
     ```
     JIRA_EMAIL = your.email@hellofresh.com
     JIRA_API_TOKEN = your_api_token
     EPIC_KEY = REW-323
     PROJECT_KEY = REW
     ```

6. Railway will automatically deploy and give you a URL like:
   ```
   https://bug-reporter-production-xxxx.up.railway.app
   ```

7. Share that URL with your whole team!

**Pros**: 
- Always available (24/7)
- Fast and free
- Easy updates (just push to GitHub)
- Professional URL

**Cons**: 
- Free tier has limited hours (500 hours/month - plenty for a team tool)

### Option C: Deploy to Render (Also Free - 10 minutes)

Similar to Railway but with unlimited free hours (just slower startup).

1. Push code to GitHub (same as above)

2. Go to [render.com](https://render.com) and sign up

3. Click "New +" → "Web Service"

4. Connect your GitHub and select the repository

5. Configure:
   - **Name**: bug-reporter
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

6. Add environment variables (same as Railway)

7. Click "Create Web Service"

8. Render gives you a URL like: `https://bug-reporter.onrender.com`

**Pros**: 
- Completely free
- Always available
- No credit card needed

**Cons**: 
- Slower startup (spins down after 15 min of inactivity)
- First load after inactivity takes 30-60 seconds

## What Your Teammates See

Once deployed, your teammates just:
1. Open the URL (bookmark it!)
2. Fill out the simple form
3. Click "Check for Duplicates" to see similar bugs
4. Click "Create Bug Report" if it's new
5. Done! They get a link to the Jira ticket

No Jira login needed. No training required. Just works.

## Updating the Tool

If you make changes:

**Local deployment**: Just restart `python app.py`

**Railway/Render**: 
```bash
git add .
git commit -m "Updated bug reporter"
git push
```
Auto-deploys in 1-2 minutes!

## Tips for Your Team

- Add the URL to your team's bookmarks
- Pin it in Slack/Teams
- Add it to your internal wiki
- Consider making it the homepage for QA team browsers

## Troubleshooting

### "Can't connect to Jira"
- Check your JIRA_API_TOKEN is correct
- Verify your JIRA_EMAIL matches your Jira account
- Make sure you have permission to create bugs in REW project

### Teammates can't access local deployment
- Verify they're on the same WiFi/network
- Check your firewall settings
- Try turning off VPN on your computer

### Free tier limits reached
- Railway: Upgrade for $5/month for unlimited
- Render: Always free but might be slow
- Alternative: Deploy to your company's internal server

## Need Help?

Check the full README.md for detailed documentation!
