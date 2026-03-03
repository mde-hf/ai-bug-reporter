# Bug Reporter

A simple, user-friendly bug reporting tool that automatically checks for duplicate tickets before creating new ones in Jira. Built for the Loyalty & Virality tribe at HelloFresh.

## ✨ Features

- 🎯 **Simple Interface** - Clean, intuitive form for reporting bugs
- 🔍 **Automatic Duplicate Detection** - AI-powered search to find similar bugs before creating
- ✅ **Direct Jira Integration** - Creates bugs under Epic REW-323 automatically
- 📊 **Dashboard** - View bug statistics, trends, and metrics
- 📈 **Charts** - 10-day creation trend visualization
- 🚀 **Easy Setup** - One command to get started
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🌓 **Dark Mode** - Automatic theme switching

---

## 🚀 Quick Start (One Command!)

```bash
git clone https://github.com/mde-hf/ai-bug-reporter.git
cd ai-bug-reporter
./setup.sh
```

That's it! The setup script will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create .env file from template
- ✅ Set up necessary directories

### Get Your Jira API Token

1. Go to [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a name (e.g., "Bug Reporter")
4. Copy the token

### Configure Your .env

Edit `.env` and add your credentials:

```bash
JIRA_EMAIL=your.email@hellofresh.com
JIRA_API_TOKEN=your_token_here
```

### Start the Application

```bash
./start.sh
```

Visit: **http://localhost:5000**

---

## 📋 Manual Setup (Alternative)

If you prefer manual setup:

### Prerequisites

- Python 3.8 or higher
- pip3
- A Jira account with API access
- Access to HelloFresh Jira workspace

### 1. Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your details
nano .env
```

Required variables:
```
JIRA_EMAIL=your.email@hellofresh.com
JIRA_API_TOKEN=your_token_here
```

### 3. Run the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 📁 Project Structure

```
bug-reporter/
├── app.py                 # Flask backend
├── templates/
│   └── index.html        # Main UI
├── static/
│   ├── css/
│   │   └── styles.css    # Styling
│   └── js/
│       └── app.js        # Frontend logic
├── setup.sh              # One-command setup
├── start.sh              # Start application
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── README.md            # This file
```

---

## 🎮 Usage

### Reporting a Bug

1. Select your **Project** (currently only Loyalty 2.0 is active)
2. Enter **Bug Title**
3. Auto-duplicate detection runs as you type
4. Fill in:
   - Description
   - Steps to Reproduce
   - Expected vs Actual Behavior
   - Environment (Staging/Production/Local)
   - Priority (Low/Medium/High/Critical)
5. Optionally attach screenshots/videos
6. Click **Create Bug Report**

### Dashboard

1. Click the **📊 Dashboard** tab
2. Select **Loyalty 2.0 Bug Reporting** from dropdown
3. View:
   - Total bugs, open/resolved counts
   - Priority × Status matrix
   - 10-day creation trend chart
   - Platform breakdown (iOS/Android/Web)
   - Resolution metrics

---

## 🌐 Deployment

This app is ready for Vercel deployment. See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions.

Quick deploy:
```bash
npx vercel
```

---

## 🛠️ Troubleshooting

### 4. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

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
