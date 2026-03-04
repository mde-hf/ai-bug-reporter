# 🚀 Multi-Agent AI System - Quick Start Guide

## What You Just Built

A complete **Multi-Agent AI System** with 4 specialized agents for intelligent bug management:

1. **Bug Analyzer** - Quality analysis and suggestions
2. **Duplicate Detective** - Semantic duplicate detection
3. **Test Case Enhancer** - AI-powered test improvement
4. **Bug Triage** - Automatic priority and routing

## ✅ What's Ready

### Backend (Python/Flask)
- ✅ 4 AI agents implemented
- ✅ Agent Manager for orchestration
- ✅ 6 new REST API endpoints
- ✅ AWS Bedrock integration (Claude 3.5 Sonnet)
- ✅ Full error handling and logging

### Frontend (React/TypeScript)
- ✅ AI Insights component
- ✅ Test Enhancement UI
- ✅ TypeScript API client
- ✅ Professional styling

### Documentation
- ✅ Comprehensive agent README
- ✅ API reference
- ✅ Test suite
- ✅ Usage examples

## 🏃 Try It Now

### 1. Start the Application

**Python Backend:**
```bash
cd "/Users/mde/bug creation"
source venv/bin/activate
python app.py
```

**React Frontend (separate terminal):**
```bash
cd "/Users/mde/bug creation/frontend"
npm run dev
```

The app will be available at:
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:5173`

### 2. Test the Agents

**Option A: Use the Test Script**
```bash
cd "/Users/mde/bug creation"
source venv/bin/activate
python agents/test_agents.py
```

This will test all 4 agents and show you exactly how they work.

**Option B: Use the UI**

1. Open `http://localhost:5173` (React frontend)
2. Go to "Report Bug" tab
3. Fill in bug details:
   - Title: "Login fails on iOS"
   - Description: "Users can't login on production"
   - Steps: "1. Open app\n2. Enter credentials\n3. Tap login"
   - Expected: "User should be logged in"
   - Actual: "Error: Connection timeout"
4. Click **"Get AI Insights"** button
5. Watch the AI analyze your bug in real-time!

**Option C: Test via API**

```bash
# Test Bug Analyzer
curl -X POST http://localhost:5000/api/agents/analyze-bug \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Login fails on iOS",
    "description": "Users cannot login on the iOS app",
    "steps": "1. Open app\n2. Enter credentials",
    "expected": "User should be logged in",
    "actual": "Error message appears"
  }'

# Test Bug Triage
curl -X POST http://localhost:5000/api/agents/triage-bug \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Rewards redemption fails at checkout",
    "description": "Production issue: users cannot redeem points"
  }'
```

## 📊 What to Expect

### Bug Analyzer Response
```json
{
  "success": true,
  "agent": "BugAnalyzerAgent",
  "response": "{
    \"quality_score\": {
      \"score\": \"Good\",
      \"rating\": 7
    },
    \"priority_recommendation\": {
      \"suggested_priority\": \"High\",
      \"reasoning\": \"Affects user authentication in production\"
    },
    \"summary\": \"Bug is well-documented but could include iOS version\"
  }",
  "usage": {
    "input_tokens": 245,
    "output_tokens": 412
  }
}
```

### Bug Triage Response
```json
{
  "success": true,
  "agent": "BugTriageAgent",
  "response": "{
    \"triage\": {
      \"priority\": \"High\",
      \"urgency_score\": 8.5
    },
    \"assignment\": {
      \"suggested_squad\": \"Loyalty Mission Squad\",
      \"suggested_component\": \"Rewards Redemption\"
    },
    \"classification\": {
      \"labels\": [\"ios\", \"checkout\", \"rewards\", \"production\"]
    }
  }"
}
```

## 🎮 Frontend Features

### AI Insights on Bug Report Page

1. Fill in bug form
2. Click **"Get AI Insights"**
3. See real-time analysis:
   - Quality score (1-10)
   - Completeness check
   - Priority recommendation
   - Squad assignment
   - Labels and tags

### Test Enhancement on Test Cases Page

1. Generate test cases from a Jira ticket
2. Click **"Enhance with AI"**
3. Choose quick action or custom request:
   - **Add Edge Cases** - Boundary and special conditions
   - **Add Negative Tests** - Error scenarios
   - **More Detail** - Specific steps and data
   - **Platform Tests** - iOS/Android/Web specific
4. Watch AI enhance your tests!

## 🔥 Cool Examples to Try

### Example 1: Bug Quality Analysis
**Bug:** "Login not working"

**AI will suggest:**
- "Add which platform (iOS/Android/Web)"
- "Specify environment (Production/Staging)"
- "Include error message"
- "Priority: High (authentication issue)"

### Example 2: Semantic Duplicate Detection
**New Bug:** "Can't sign in to app"
**Existing Bug:** "Login fails with timeout"

**AI will detect:** 95% similarity - Same issue, different wording

### Example 3: Test Enhancement
**Original Test:**
```gherkin
Scenario: User logs in
  When I enter credentials
  Then I should be logged in
```

**After AI Enhancement:**
```gherkin
Scenario: User logs in with valid credentials
  Given I am on the login page
  And I have valid credentials
  When I enter email "user@example.com"
  And I enter password "ValidPass123"
  And I click the login button
  Then I should see the home page
  And my session should be active
  
@edge_case
Scenario: Login fails with expired password
  Given I am on the login page
  And my password has expired
  When I attempt to login
  Then I should see "Password expired" message
```

## 💡 Tips for Best Results

### 1. Bug Analysis
- Provide complete information
- Include all fields
- Add context about environment

### 2. Duplicate Detection
- Write clear, descriptive titles
- Include key symptoms
- AI understands meaning, not just words

### 3. Test Enhancement
- Start with generated test cases
- Use quick actions for common improvements
- Try custom requests for specific needs
- Iterate multiple times

### 4. Triage
- Include production/staging context
- Mention user impact
- Add component clues (checkout, login, etc.)

## 📈 Performance Expectations

| Agent | Response Time | Token Usage | Cost per Request |
|-------|--------------|-------------|------------------|
| Bug Analyzer | 3-5 seconds | 200-800 | ~$0.01-0.02 |
| Bug Triage | 2-4 seconds | 150-600 | ~$0.01 |
| Duplicate Detective | 4-6 seconds | 300-900 | ~$0.02-0.03 |
| Test Enhancer | 5-8 seconds | 400-1200 | ~$0.02-0.04 |
| Smart Workflow | 8-12 seconds | 500-1500 | ~$0.03-0.05 |

## 🛠️ Troubleshooting

### "Multi-Agent system not initialized"
**Cause:** AWS Bedrock client failed to initialize

**Fix:**
```bash
# Check AWS credentials
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY

# Verify .env file
cat .env

# Restart the server
python app.py
```

### "AWS Bedrock error: Access Denied"
**Cause:** AWS credentials don't have Bedrock access

**Fix:**
- Ensure IAM user has `bedrock:InvokeModel` permission
- Verify model ID is correct for your region
- Check region availability

### Slow Responses
**Tips:**
- First request may be slower (cold start)
- Subsequent requests are faster
- Limit context length for faster processing
- Use parallel requests when possible

## 🎯 Next Steps

### Immediate Use Cases
1. **Bug Intake:** Use AI Insights on every new bug
2. **Quality Gate:** Check bug quality before submission
3. **Test Coverage:** Enhance existing test suites
4. **Duplicate Prevention:** Run semantic checks

### Advanced Usage
1. **Smart Workflow:** Call `/api/agents/smart-workflow` for complete analysis
2. **Batch Processing:** Process multiple bugs in parallel
3. **Custom Prompts:** Modify agent system prompts for your team
4. **Integration:** Add to CI/CD pipelines

## 📚 Learn More

- **Full Documentation:** [agents/README.md](agents/README.md)
- **API Reference:** See agents README for all endpoints
- **Architecture:** Review agent_manager.py for orchestration
- **Customization:** Modify system prompts in each agent file

## 🎉 You're Ready!

Your Multi-Agent AI System is **fully operational** and ready to revolutionize your bug management workflow!

Start with the test script to see all agents in action:
```bash
cd "/Users/mde/bug creation"
source venv/bin/activate
python agents/test_agents.py
```

---

**Questions or Issues?**
- Check agents/README.md for detailed docs
- Review test_agents.py for examples
- Test individual endpoints with curl

**Happy AI-Powered Bug Management!** 🚀
