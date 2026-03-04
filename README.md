# Bug Reporter

A simple, user-friendly bug reporting tool that automatically checks for duplicate tickets before creating new ones in Jira. Built for the Loyalty & Virality tribe at HelloFresh.

## ✨ Features

- 🎯 **Simple Interface** - Clean, intuitive form for reporting bugs
- 🔍 **Automatic Duplicate Detection** - AI-powered search to find similar bugs before creating
- ✅ **Direct Jira Integration** - Creates bugs under Epic REW-323 automatically
- 🤖 **Multi-Agent AI System** ⭐ NEW - Advanced AI agents for intelligent bug management:
  - **Bug Analyzer** - Quality analysis and improvement suggestions
  - **Duplicate Detective** - Semantic duplicate detection beyond keywords
  - **Test Enhancer** - Iterative test case improvement
  - **Bug Triage** - Automatic priority and squad assignment
- 🧪 **AI Test Case Generator** - Claude AI generates comprehensive Cucumber/Gherkin test cases from JIRA tickets or Google Docs
- 📊 **Dashboard** - View bug statistics, trends, and metrics
- 📈 **Charts** - 10-day creation trend visualization
- 🚀 **Easy Setup** - One command to get started
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🌓 **Dark Mode** - Automatic theme switching
- 💬 **Slack Integration** - Automatic notifications to team channels

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
# Required: Jira Configuration
JIRA_EMAIL=your.email@hellofresh.com
JIRA_API_TOKEN=your_token_here

# AI Configuration (Agento-Compatible)
# Option 1: Claude CLI (Recommended - Uses Company AWS)
#   - Automatically detected if installed (no config needed!)
#   - Check: which claude
#   - Uses your company's AWS Bedrock via SSO
# Option 2: Personal Anthropic API
#   - Set ANTHROPIC_API_KEY below
# Priority: Claude CLI > Anthropic API > Rule-based fallback
#ANTHROPIC_API_KEY=sk-ant-api...

# Optional: Slack Integration
SLACK_WEBHOOK_URL=your_webhook_url
```

### Start the Application

**Option 1: Normal Start**

```bash
./start.sh
```

**Option 2: Auto-Restart Monitor (Recommended for Development)**

```bash
./monitor.sh
```

The monitor script will:
- ✅ Start the Flask server
- ✅ Check every 5 seconds if server is running
- ✅ Automatically restart if it crashes
- ✅ Show restart count and status

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

## 🤖 AI Test Case Generator (AWS Bedrock + Claude)

The tool includes an AI-powered test case generator that creates comprehensive Cucumber/Gherkin test scenarios from JIRA tickets or Google Drive documents.

### Setup AWS Bedrock

To enable AI test case generation, configure AWS Bedrock in your `.env`:

```bash
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1  # or your preferred region
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
```

### Getting AWS Credentials

**Option 1: HelloFresh Enterprise (Recommended)**
- Contact your DevOps/Platform team to get AWS credentials with Bedrock access
- HelloFresh likely has an enterprise AWS account with Bedrock enabled
- This ensures compliance and cost tracking

**Option 2: AWS IAM User**
1. Log into AWS Console
2. Go to IAM → Users → Create User
3. Attach policy: `AmazonBedrockFullAccess`
4. Create access keys
5. Copy the Access Key ID and Secret Access Key

### Enable Claude Model in Bedrock

1. Go to AWS Console → Amazon Bedrock
2. Navigate to **Model access** (in left sidebar)
3. Click **Manage model access**
4. Enable **Anthropic Claude** models:
   - `Claude 3.5 Sonnet` (recommended - best quality)
   - `Claude 3 Sonnet` (alternative)
5. Submit request (usually instant approval)

### Supported Input Sources

The AI generator accepts:

1. **JIRA Tickets**
   - Full URL: `https://hellofresh.atlassian.net/browse/REW-123`
   - Ticket key: `REW-123`

2. **Google Drive Documents**
   - Google Docs URL: `https://docs.google.com/document/d/...`
   - Document must be shared with "Anyone with the link"

### What the AI Generates

Claude AI analyzes the ticket/document and creates:

- ✅ **Acceptance Criteria Tests** - One scenario per AC found (tagged @AC1, @AC2, etc.)
- ✅ **User Story Tests** - Validates user story fulfillment
- ✅ **Business Rule Tests** - Ensures rules are enforced
- ✅ **Happy Path** - Ideal user journey (@happy_path @smoke)
- ✅ **Critical Path** - Essential business flows (@critical_path)
- ✅ **Edge Cases** - Boundary conditions (@edge_case)
- ✅ **Sad Path** - Error handling and validation (@sad_path)
- ✅ **Regression** - Side effect prevention (@regression)
- ✅ **Scenario Outlines** - Data-driven test examples
- ✅ **Multi-platform scenarios** - iOS/Android/Web where relevant

### Intelligent Parsing

The AI automatically detects and extracts:
- Acceptance Criteria sections
- User Stories (As a/I want/So that format)
- Business Rules
- Google Drive links embedded in tickets
- Bullet points as potential criteria

### Fallback Mode

### Fallback Mode (No AI)

If Claude CLI and Anthropic API are not configured or unavailable, the system automatically falls back to rule-based test case generation. Your tool will still work, just with simpler test scenarios.

### Cost Estimation

AWS Bedrock pricing (approximate):
- Claude 3.5 Sonnet: ~$0.003-0.015 per test case generation
- Very affordable for enterprise use
- Much cheaper than manual test case writing

---

## 🤖 Multi-Agent AI System

**NEW!** Advanced AI agents powered by Claude (CLI or API) for intelligent bug management.

### Available Agents

#### 1. Bug Analyzer Agent
Analyzes bug report quality and provides improvement suggestions:
- Completeness check (missing fields, clarity)
- Priority assessment based on severity keywords
- Environment and platform detection
- Component/area identification  
- Quality scoring with actionable feedback

**Usage:** Click "Get AI Insights" button on the Report Bug page

#### 2. Duplicate Detective Agent
Semantic duplicate detection beyond keyword matching:
- Understands meaning, not just keywords
- Identifies duplicates with different wording
- Semantic similarity scoring (0-100)
- Confidence levels and detailed reasoning

**Usage:** Automatically runs during duplicate checking (enhanced results)

#### 3. Test Case Enhancer Agent
Iteratively improves test cases through AI conversation:
- Add edge cases and boundary conditions
- Enhance test coverage
- Add platform-specific scenarios
- Improve specificity and detail

**Usage:** Click "Enhance with AI" on the Test Case Generator page

#### 4. Bug Triage Agent
Automatic bug triaging and routing:
- Priority assessment (Critical/High/Medium/Low)
- Squad assignment (Loyalty Mission/Virality/Rewards)
- Component detection
- Urgency scoring (0-10)
- Label/tag recommendations

**Usage:** Part of "Get AI Insights" workflow

### API Endpoints

All agent features are exposed via REST API:

```bash
# List all agents
GET /api/agents

# Analyze bug quality
POST /api/agents/analyze-bug

# Auto-triage bug
POST /api/agents/triage-bug

# Semantic duplicate detection
POST /api/agents/check-semantic-duplicates

# Enhance test cases
POST /api/agents/enhance-test-cases

# Complete smart workflow
POST /api/agents/smart-workflow
```

### Testing Agents

Test the agent system:

```bash
cd agents
python test_agents.py
```

### Documentation

For detailed agent documentation, see [agents/README.md](agents/README.md)

---

## 📁 Project Structure

```
bug-reporter/
├── app.py                 # Flask backend
├── agents/                # Multi-Agent AI System ⭐
│   ├── base_agent.py     # Base agent class
│   ├── bug_analyzer.py   # Bug analysis agent
│   ├── duplicate_detective.py  # Semantic duplicates
│   ├── test_enhancer.py  # Test case improvement
│   ├── bug_triage.py     # Auto-triage agent
│   ├── agent_manager.py  # Agent orchestration
│   ├── test_agents.py    # Agent tests
│   └── README.md         # Agent documentation
├── frontend/              # React + TypeScript UI
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API clients
│   │   ├── types/        # TypeScript types
│   │   └── pages/        # Page components
│   └── package.json
├── templates/
│   └── index.html        # Legacy HTML UI
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
5. **NEW!** Click **Get AI Insights** for:
   - Bug quality analysis
   - Auto-triage recommendations
   - Priority suggestions
   - Squad assignment recommendations
6. Optionally attach screenshots/videos
7. Click **Create Bug Report**

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
