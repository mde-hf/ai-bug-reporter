# AI Bug Reporter

A simple, user-friendly bug reporting tool that automatically checks for duplicate tickets before creating new ones in Jira. Built as a simpler alternative to direct JIRA interaction.

## Features

- 🎯 **Simple Interface** - Clean, intuitive form for reporting bugs
- 🔍 **Automatic Duplicate Detection** - AI-powered search to find similar bugs before creating
- ✅ **Direct Jira Integration** - Creates bugs under Epic REW-323 automatically
- 🚀 **Easy to Share** - Web-based, accessible to your entire team
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A Jira account with API access
- Access to HelloFresh Jira workspace

### 1. Get Your Jira API Token

1. Go to [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a name (e.g., "Bug Reporter")
4. Copy the token (you won't see it again!)

### 2. Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your details
# Required:
JIRA_EMAIL=your.email@hellofresh.com
JIRA_API_TOKEN=your_token_from_step_1
```

### 4. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## Sharing with Your Team

### Option 1: Local Network (Quick & Easy)

1. Find your local IP address:
   ```bash
   # On Mac/Linux:
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # On Windows:
   ipconfig
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Share the URL with your team:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

**Note**: Your teammates must be on the same network (same WiFi/office network)

### Option 2: Deploy to Cloud (Permanent Solution)

#### Deploy to Heroku (Free Tier Available)

1. Install Heroku CLI: [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

2. Create a `Procfile`:
   ```
   web: python app.py
   ```

3. Deploy:
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-bug-reporter
   
   # Set environment variables
   heroku config:set JIRA_EMAIL=your.email@hellofresh.com
   heroku config:set JIRA_API_TOKEN=your_token
   heroku config:set EPIC_KEY=REW-323
   heroku config:set PROJECT_KEY=REW
   
   # Deploy
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

4. Share the URL: `https://your-bug-reporter.herokuapp.com`

#### Deploy to Railway (Recommended - Very Easy)

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub account
3. Push this code to a GitHub repo
4. Click "New Project" → "Deploy from GitHub"
5. Select your repo
6. Add environment variables in Railway dashboard:
   - `JIRA_EMAIL`
   - `JIRA_API_TOKEN`
   - `EPIC_KEY`
   - `PROJECT_KEY`
7. Railway will give you a URL to share

#### Deploy to Render (Free Option)

1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python app.py`
6. Add environment variables
7. Deploy and share the URL

### Option 3: Docker (For Tech-Savvy Teams)

```bash
# Build and run with Docker
docker build -t bug-reporter .
docker run -p 5000:5000 \
  -e JIRA_EMAIL=your.email@hellofresh.com \
  -e JIRA_API_TOKEN=your_token \
  bug-reporter
```

## Usage

### Reporting a Bug

1. Open the application in your browser
2. Fill out the bug report form:
   - **Title**: Brief description of the issue
   - **Description**: Detailed explanation
   - **Steps to Reproduce**: How to trigger the bug
   - **Expected Behavior**: What should happen
   - **Actual Behavior**: What actually happens
   - **Environment**: Device/browser/platform info
   - **Priority**: Low/Medium/High/Critical

3. Click "Check for Duplicates" to see if similar bugs exist
4. If no duplicates (or your bug is different), click "Create Bug Report"
5. You'll get a link to the created Jira ticket!

### For Team Members

Just give them the URL and they can start reporting bugs immediately. No Jira knowledge required!

## How Duplicate Detection Works

The tool automatically:
1. Extracts key terms from your bug title and description
2. Searches Jira for similar bugs under Epic REW-323
3. Calculates similarity scores using keyword matching
4. Shows you the most similar bugs (if any)
5. Lets you decide whether to create a new bug or add to an existing one

## Troubleshooting

### "Failed to create issue" Error

- Check that your JIRA_EMAIL and JIRA_API_TOKEN are correct
- Verify you have permission to create bugs in the REW project
- Make sure the Epic REW-323 exists and you have access

### Can't Connect from Another Device

- Make sure both devices are on the same network
- Check your firewall isn't blocking port 5000
- Try using `0.0.0.0` as the host: add this to app.py: `app.run(host='0.0.0.0', port=5000)`

### Duplicate Detection Not Working

- The tool searches bugs under Epic REW-323 only
- Make sure the Epic has some existing bugs to search
- If no bugs exist yet, it will show "no duplicates found"

## Security Notes

- **Never commit your `.env` file** to git (it contains your API token)
- **API tokens are like passwords** - keep them secret
- If deploying publicly, consider adding authentication
- For internal tools, consider running on internal network only

## Customization

### Change the Epic

Edit `.env`:
```
EPIC_KEY=YOUR-EPIC-KEY
PROJECT_KEY=YOUR-PROJECT
```

### Adjust Duplicate Threshold

In `app.py`, find the `check_duplicates` route and adjust:
```python
'has_duplicates': len(duplicates) > 0 and duplicates[0]['similarity'] > 60
```
Change `60` to be more or less strict.

### Customize UI Colors

Edit `static/css/styles.css` and modify the `:root` variables at the top.

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your Jira credentials
3. Make sure you have network access to `hellofresh.atlassian.net`

## Architecture

- **Backend**: Python Flask (handles Jira API calls and duplicate detection)
- **Frontend**: Vanilla JavaScript (no frameworks, easy to customize)
- **Styling**: Custom CSS (modern, responsive design)
- **API**: RESTful endpoints for checking duplicates and creating bugs

## License

MIT License - Feel free to modify and share!
