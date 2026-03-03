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
