# 🎯 How to Use the Bug Reporter with AI Agents

## ✅ Your App is Ready!

### URLs:
- **React Frontend (NEW!):** http://localhost:3000
- **Python Backend:** http://localhost:5000
- **Legacy HTML:** http://localhost:5000 (original interface)

---

## 🚀 Quick Start - Using AI Agents

### 1. Report a Bug with AI Insights

1. **Open the App**
   - Go to: http://localhost:3000
   - Click **"Report Bug"** tab (should be selected by default)

2. **Select Project**
   - Choose **"Loyalty 2.0 Bug Reporting"** from the dropdown
   - (Other options show "Work In Progress")

3. **Fill in Bug Details**
   ```
   Title: Login fails on iOS app
   
   Description: Users are unable to login on the iOS app in production. 
   The app shows a timeout error after 10 seconds.
   
   Steps to Reproduce:
   1. Open HelloFresh app on iPhone
   2. Tap "Sign In"
   3. Enter valid email and password
   4. Tap "Login" button
   5. Wait 10 seconds
   
   Expected Behavior: User should be logged in successfully
   
   Actual Behavior: Error message appears: "Connection timeout. Please try again."
   
   Environment: Production
   Priority: High
   ```

4. **Get AI Insights** 🤖
   - Scroll down and click the **"Get AI Insights"** button
   - Wait 5-10 seconds for AI analysis
   
5. **Review AI Recommendations**
   - **Bug Quality Analysis:**
     - Completeness score
     - Missing information
     - Improvement suggestions
   
   - **Auto-Triage Recommendations:**
     - Suggested priority (Critical/High/Medium/Low)
     - Squad assignment (Loyalty Mission/Virality/Rewards)
     - Urgency score
     - Recommended labels (ios, authentication, production, etc.)

6. **Apply or Adjust**
   - Review AI suggestions
   - Adjust priority if needed
   - Add any missing details the AI identified

7. **Create Bug**
   - Click **"Create Bug Report"**
   - Bug will be created in Jira under REW-323
   - Slack notification sent automatically

---

## 🧪 Generate & Enhance Test Cases

### 1. Generate Test Cases from Jira Ticket

1. **Go to Test Cases Tab**
   - Click **"AI Test Cases"** tab

2. **Enter Ticket Information**
   ```
   Input: REW-444
   or
   Input: https://hellofresh.atlassian.net/browse/REW-444
   ```

3. **Generate**
   - Click **"Generate AI Test Cases"**
   - Wait 10-15 seconds
   - AI will:
     - Fetch the Jira ticket
     - Read Acceptance Criteria & User Stories
     - Generate comprehensive Gherkin test cases

4. **Review Generated Tests**
   - Happy path scenarios
   - Critical path tests
   - Edge cases
   - Acceptance criteria coverage

### 2. Enhance Test Cases with AI 🌟

1. **After generating tests, click "Enhance with AI"**

2. **Choose Quick Action or Custom Request**
   
   **Quick Actions:**
   - **Add Edge Cases** - Boundary conditions, special scenarios
   - **Add Negative Tests** - Error handling, invalid inputs
   - **More Detail** - Specific test data, assertions
   - **Platform Tests** - iOS, Android, Web specific tests

3. **Or Write Custom Request**
   ```
   Examples:
   - "Add tests for authentication error scenarios"
   - "Include boundary condition tests for point values"
   - "Add tests for slow network conditions"
   - "Include accessibility test scenarios"
   ```

4. **Click "Enhance Test Cases"**
   - Wait 8-12 seconds
   - AI will add new scenarios
   - Original tests remain, new ones added

5. **Iterate**
   - You can enhance multiple times!
   - Each enhancement builds on previous ones
   - Refine until you have complete coverage

6. **Copy to Clipboard**
   - Click **"Copy to Clipboard"**
   - Paste into your test files

---

## 📊 View Dashboard Metrics

1. **Go to Dashboard Tab**
   - Click **"Dashboard"** tab

2. **Select Project**
   - Choose **"Loyalty 2.0 Bug Reporting"**

3. **View Metrics**
   - Total bugs (Open/Resolved/On Hold)
   - Priority × Status matrix
   - 10-day creation trend chart
   - Platform breakdown (iOS/Android/Web)
   - Resolution metrics

4. **Click Any Metric**
   - Opens Jira with filtered search results
   - Example: Click "High Priority" → See all high priority bugs

---

## 🔥 Real-World Examples

### Example 1: Poorly Written Bug → AI Improves It

**Your Input:**
```
Title: Login broken
Description: can't login
```

**AI Analysis Says:**
```json
{
  "quality_score": "Poor (3/10)",
  "missing_info": [
    "Which platform? (iOS/Android/Web)",
    "Which environment? (Production/Staging)",
    "What error message appears?",
    "Steps to reproduce",
    "Expected vs actual behavior"
  ],
  "priority_recommendation": "Cannot determine - insufficient information",
  "suggestions": [
    "Add specific platform information",
    "Include exact error message",
    "Provide detailed steps",
    "Specify environment"
  ]
}
```

**You Update Based on AI:**
```
Title: Login fails with timeout error on iOS Production
Description: Users cannot login on iOS app in production. 
Error: "Connection timeout after 10s"
Platform: iOS 16.4+
Environment: Production
Steps: [detailed steps]
Expected: User logs in
Actual: Timeout error
```

**AI Re-Analysis:**
```json
{
  "quality_score": "Good (8/10)",
  "priority_recommendation": "High",
  "suggested_squad": "Loyalty Mission Squad",
  "reasoning": "Production issue affecting core authentication"
}
```

---

### Example 2: Semantic Duplicate Detection

**New Bug:**
```
Title: Can't sign in to the app
Description: The sign in button doesn't work
```

**Existing Bugs in System:**
```
REW-123: Login fails with timeout
REW-456: Profile page crash
REW-789: Unable to authenticate users
```

**AI Duplicate Detective Finds:**
```json
[
  {
    "ticket": "REW-789",
    "similarity": 92,
    "is_duplicate": "yes",
    "reasoning": "Both describe authentication failure, same underlying issue",
    "recommendation": "Mark as duplicate of REW-789"
  },
  {
    "ticket": "REW-123",
    "similarity": 78,
    "is_duplicate": "maybe",
    "reasoning": "Related to login but different symptom (timeout vs button)",
    "recommendation": "Link as related"
  },
  {
    "ticket": "REW-456",
    "similarity": 15,
    "is_duplicate": "no",
    "reasoning": "Different feature (profile vs login)",
    "recommendation": "Create as new bug"
  }
]
```

---

### Example 3: Test Enhancement Workflow

**Generated Tests (Basic):**
```gherkin
@smoke @happy_path
Scenario: User redeems points at checkout
  Given I am logged in
  When I add items to cart
  And I apply points
  Then I should see discount
```

**After "Add Edge Cases":**
```gherkin
@smoke @happy_path
Scenario: User redeems points at checkout
  Given I am logged in
  When I add items to cart
  And I apply 500 points
  Then I should see €5.00 discount
  And my points balance should be reduced by 500

@edge_case @boundary
Scenario: User redeems exact points balance
  Given I have exactly 1000 points
  When I apply all 1000 points
  Then I should see €10.00 discount
  And my points balance should be 0
  
@edge_case @insufficient_balance
Scenario: User tries to redeem more points than available
  Given I have 300 points
  When I try to apply 500 points
  Then I should see error "Insufficient points"
  And no discount should be applied
```

**After "Add Platform Tests":**
```gherkin
[...previous tests...]

@ios @platform_specific
Scenario: Points redemption on iOS with Face ID
  Given I am using iPhone with Face ID enabled
  When I apply points requiring authentication
  Then I should see Face ID prompt
  And points should be applied after authentication

@android @platform_specific  
Scenario: Points redemption on Android with app background
  Given I have 500 points in cart
  When I background the app
  And I return after 30 seconds
  Then my points selection should be preserved
```

---

## 🎮 API Testing (For Developers)

### Test Individual Agents via API

```bash
# 1. Bug Analyzer
curl -X POST http://localhost:5000/api/agents/analyze-bug \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Checkout fails",
    "description": "Users cannot complete checkout",
    "steps": "1. Add items\n2. Go to checkout\n3. Enter payment",
    "expected": "Order completes",
    "actual": "Error appears"
  }'

# 2. Bug Triage
curl -X POST http://localhost:5000/api/agents/triage-bug \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Rewards redemption fails at checkout on iOS",
    "description": "Production issue affecting all iOS users"
  }'

# 3. Semantic Duplicates
curl -X POST http://localhost:5000/api/agents/check-semantic-duplicates \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Can'\''t sign in",
    "description": "Login button not working"
  }'

# 4. Test Enhancement
curl -X POST http://localhost:5000/api/agents/enhance-test-cases \
  -H "Content-Type: application/json" \
  -d '{
    "test_cases": "Scenario: User logs in\n  When I enter credentials\n  Then I am logged in",
    "enhancement_request": "Add edge cases and negative tests"
  }'

# 5. Smart Workflow (All Agents)
curl -X POST http://localhost:5000/api/agents/smart-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bug title",
    "description": "Bug description"
  }'
```

---

## 💡 Pro Tips

### For Bug Reports:
1. **Fill all fields** before clicking "Get AI Insights" for best results
2. **Be specific** - AI works better with detailed information
3. **Include error messages** - Helps AI assess severity
4. **Mention platform** - iOS, Android, Web
5. **State environment** - Production issues get higher priority

### For Duplicate Detection:
1. **Write clear titles** - AI understands meaning
2. **Don't worry about exact wording** - "Login fails" = "Can't sign in"
3. **Review AI confidence** - High/Medium/Low
4. **Check recommendations** - AI suggests whether to create or duplicate

### For Test Enhancement:
1. **Start with basic tests** - Let AI add complexity
2. **Use quick actions first** - Fast and effective
3. **Iterate multiple times** - Each enhancement adds more
4. **Custom requests** - Be specific about what you need
5. **Review before copying** - AI is smart but verify scenarios

### For Dashboard:
1. **Click any metric** - Opens filtered Jira search
2. **Use trends** - Identify spike patterns
3. **Platform breakdown** - See which platforms need attention
4. **Priority matrix** - Quick overview of workload

---

## 🛠️ Troubleshooting

### "Get AI Insights" Button Not Working
- Check console (F12) for errors
- Verify AWS credentials in `.env`
- Ensure Python backend is running

### "Multi-Agent system not initialized"
```bash
# Check backend logs
# Should see: "Multi-Agent AI System initialized successfully"

# If not, check .env file:
cat .env | grep AWS
```

### Slow AI Responses
- First request is slower (cold start)
- Subsequent requests are faster
- Expected: 5-15 seconds per agent
- Check your AWS region (us-east-1 is fastest)

### Frontend Not Loading
```bash
# Check if running:
lsof -ti:3000

# Restart if needed:
cd "/Users/mde/bug creation/frontend"
npm run dev
```

---

## 📈 What to Expect

### Response Times
| Feature | Time | What's Happening |
|---------|------|-----------------|
| Bug Analysis | 5-8s | Analyzing quality, priority, completeness |
| Bug Triage | 3-5s | Assessing urgency, squad, labels |
| Duplicate Check | 6-10s | Semantic comparison with existing bugs |
| Test Generation | 10-15s | Reading ticket, generating scenarios |
| Test Enhancement | 8-12s | Adding new test cases |
| Smart Workflow | 12-18s | Running multiple agents in sequence |

### Costs (AWS Bedrock)
- Bug Analysis: ~$0.01-0.02
- Bug Triage: ~$0.01
- Duplicate Check: ~$0.02-0.03
- Test Enhancement: ~$0.02-0.04
- **Total per bug (with AI):** ~$0.03-0.05
- **ROI:** Saves 30-60 minutes of manual work

---

## 🎯 Best Practices

### Daily Workflow
1. **Morning:** Check dashboard for overnight bugs
2. **New Bugs:** Always use "Get AI Insights" first
3. **Test Cases:** Generate for each feature ticket
4. **Enhancement:** Enhance tests before sprint planning
5. **Review:** Check AI suggestions but trust your judgment

### Team Usage
1. **Share with team:** Everyone can use the same URL
2. **Consistency:** AI ensures consistent bug quality
3. **Training:** New members learn bug standards from AI
4. **Review process:** AI pre-triages before manual review

---

## 🎉 You're Ready!

**Start using the AI agents now:**
1. Open http://localhost:3000
2. Report a bug
3. Click "Get AI Insights"
4. Watch the magic happen! ✨

**Need help?** Check the documentation:
- [QUICK_START_AGENTS.md](QUICK_START_AGENTS.md) - This guide
- [agents/README.md](agents/README.md) - Technical docs
- [README.md](README.md) - Main documentation

---

**Questions?** The AI agents are self-documenting - just try them and see what they suggest!
