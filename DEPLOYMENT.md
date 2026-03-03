# Bug Reporter - Vercel Deployment Guide

This application is deployed on Vercel.

## Environment Variables

Set these in your Vercel project settings:

```
JIRA_BASE_URL=https://hellofresh.atlassian.net
JIRA_EMAIL=your.email@hellofresh.com
JIRA_API_TOKEN=your_jira_api_token
EPIC_KEY=REW-323
PROJECT_KEY=REW
SLACK_WEBHOOK_URL=your_slack_webhook_url (optional)
```

## Deployment

### Initial Setup

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

### Subsequent Deployments

The app auto-deploys when you push to GitHub main branch.

Or manually deploy:
```bash
vercel --prod
```

## Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000
