# AI Agent Usage - Current Implementation

## Where AI Agents Are Used NOW

### ✅ ACTIVE: Test Case Generator (Web UI)

**Location**: Test Case Generator page (3rd tab in app)

**Feature**: "Enhance with AI" button

**What it does**:
1. User generates test cases from a JIRA ticket
2. User clicks "Enhance with AI" button
3. AI agent (`TestCaseEnhancer`) improves the test cases
4. Shows enhanced version with improvements

**Frontend**: `frontend/src/components/TestCaseGenerator.tsx`
```typescript
agentApi.enhanceTestCases({
  test_cases: generateMutation.data.test_cases,
  enhancement_request: enhancementRequest,
  ticket_context: {...}
})
```

**Backend**: `/api/agents/enhance-test-cases` (app.py line 1576)
```python
result = agent_manager.enhance_test_cases(
    test_cases=data['test_cases'],
    enhancement_request=data['enhancement_request'],
    ticket_context=data.get('ticket_context')
)
```

---

## 🔧 AVAILABLE BUT NOT USED IN UI: Other AI Agents

These agents exist and work, but have **no UI integration** yet:

### 1. Bug Analyzer Agent
**Endpoint**: `/api/agents/analyze-bug`
**What it does**: Analyzes bug quality and suggests improvements
**Status**: ❌ Not called from UI

### 2. Bug Triage Agent
**Endpoint**: `/api/agents/triage-bug`
**What it does**: Auto-suggests priority, squad, and labels
**Status**: ❌ Not called from UI

### 3. Duplicate Detective Agent
**Endpoint**: `/api/agents/check-semantic-duplicates`
**What it does**: Finds semantic duplicates (beyond keyword matching)
**Status**: ❌ Not called from UI

### 4. Smart Workflow
**Endpoint**: `/api/agents/smart-workflow`
**What it does**: Runs all agents together (analyze + triage + duplicates)
**Status**: ❌ Not called from UI

---

## All Available Endpoints (Backend)

```python
# WORKING ENDPOINTS:
GET  /api/agents                        # List all agents
POST /api/agents/analyze-bug            # Bug quality analysis
POST /api/agents/triage-bug             # Auto-triage (priority/squad)
POST /api/agents/check-semantic-duplicates  # AI duplicate detection
POST /api/agents/enhance-test-cases     # ✅ USED IN UI
POST /api/agents/smart-workflow         # Run all agents together
```

---

## Summary

### Currently Active in Web UI:
- ✅ **Test Case Enhancer** (Test Case Generator page)
  - User clicks "Enhance with AI"
  - Uses Claude CLI or Anthropic API
  - Improves generated test cases

### Available but Not in UI:
- ❌ Bug Analyzer (no UI button)
- ❌ Bug Triage (no UI button)
- ❌ Duplicate Detective (not integrated into duplicate check)
- ❌ Smart Workflow (no UI button)

---

## How to Enable More Agents in UI

If you want to use the other agents, you would need to:

### Option 1: Add to Bug Report Form
Add buttons to the bug form to:
- Analyze bug quality before submission
- Auto-suggest priority/squad
- Show AI-powered duplicate detection

### Option 2: Add to Dashboard
Show AI insights on the dashboard:
- Quality score for recent bugs
- Suggested improvements
- Auto-triage recommendations

### Option 3: Create New "AI Assistant" Tab
Add a 4th tab with:
- Bug analysis
- Triage suggestions
- Advanced duplicate detection

---

## Testing the Active Feature

### Test Case Enhancement (Currently Working)

1. Start the app:
   ```bash
   ./start.sh
   ```

2. Go to "Test Case Generator" tab

3. Enter a JIRA ticket:
   ```
   https://hellofresh.atlassian.net/browse/REW-289
   ```

4. Click "Generate Test Cases"

5. Click "Enhance with AI"

6. Check terminal logs:
   ```
   [TestCaseEnhancer] Trying Claude CLI...
   [TestCaseEnhancer] Claude CLI successful
   ```

---

## Testing the Inactive Features (API Only)

You can test the other agents via curl:

```bash
# List all agents
curl http://localhost:5000/api/agents

# Analyze a bug
curl -X POST http://localhost:5000/api/agents/analyze-bug \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Login page crashes on iOS",
    "description": "Steps: 1. Open app 2. Tap login",
    "environment": "Production"
  }'

# Triage a bug
curl -X POST http://localhost:5000/api/agents/triage-bug \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Checkout flow broken",
    "description": "Users cannot complete purchases",
    "environment": "Production"
  }'
```

---

## Conclusion

**Right now**: Only the **Test Case Enhancer** agent is actively used in the web UI.

**Available**: 3 more agents (Bug Analyzer, Bug Triage, Duplicate Detective) work via API but have no UI integration.

**All agents**: Use Claude CLI → Anthropic API → Fallback (like Agento).
