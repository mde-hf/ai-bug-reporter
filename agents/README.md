# Multi-Agent AI System

**Powered by AWS Bedrock (Claude 3.5 Sonnet)**

An advanced AI agent system that provides intelligent bug management capabilities.

## Overview

The Multi-Agent AI System consists of four specialized agents, each designed for specific tasks in the bug management workflow:

1. **Bug Analyzer Agent** - Analyzes bug report quality and provides improvement suggestions
2. **Duplicate Detective Agent** - Semantic duplicate detection beyond keyword matching
3. **Test Case Enhancer Agent** - Iteratively improves test cases through AI conversation
4. **Bug Triage Agent** - Automatically triages bugs with priority and assignment recommendations

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent Manager                            │
│  Orchestrates all agents and provides unified interface     │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                   │                   │
┌───────▼──────┐   ┌────────▼────────┐   ┌────▼──────────┐
│ Bug Analyzer │   │ Duplicate       │   │ Test Enhancer │
│              │   │ Detective       │   │               │
└──────────────┘   └─────────────────┘   └───────────────┘
                            │
                   ┌────────▼──────────┐
                   │  Bug Triage       │
                   │                   │
                   └───────────────────┘
```

## Features

### 1. Bug Analyzer Agent

**Purpose:** Analyze bug reports for quality and completeness

**Capabilities:**
- Completeness check (missing fields, clarity)
- Priority assessment based on severity keywords
- Environment and platform detection
- Component/area identification
- Quality scoring with actionable feedback

**API Endpoint:** `POST /api/agents/analyze-bug`

**Request:**
```json
{
  "title": "Login fails on iOS",
  "description": "Users can't login",
  "steps": "1. Open app\n2. Enter credentials\n3. Tap login",
  "expected": "User should be logged in",
  "actual": "Error message appears",
  "environment": "Production",
  "priority": "High"
}
```

**Response:**
```json
{
  "success": true,
  "agent": "BugAnalyzerAgent",
  "response": "{...analysis JSON...}",
  "usage": { "input_tokens": 245, "output_tokens": 412 },
  "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
}
```

### 2. Duplicate Detective Agent

**Purpose:** Semantic duplicate detection using AI understanding

**Capabilities:**
- Understands meaning, not just keywords
- Semantic similarity scoring (0-100)
- Identifies duplicates with different wording
- Confidence levels: High/Medium/Low
- Detailed reasoning for matches

**API Endpoint:** `POST /api/agents/check-semantic-duplicates`

**Request:**
```json
{
  "title": "App crashes when opening profile",
  "description": "The application force closes...",
  "steps": "Go to profile page",
  "environment": "Production"
}
```

**Response:**
```json
{
  "success": true,
  "agent": "DuplicateDetectiveAgent",
  "response": "[{candidate_key: 'REW-123', similarity_score: 85, ...}]"
}
```

### 3. Test Case Enhancer Agent

**Purpose:** Iteratively improve test cases through conversation

**Capabilities:**
- Add edge cases and boundary conditions
- Enhance test coverage
- Add platform-specific scenarios
- Improve specificity and detail
- Multi-turn conversation support

**API Endpoint:** `POST /api/agents/enhance-test-cases`

**Request:**
```json
{
  "test_cases": "Feature: Login\n  Scenario: User logs in...",
  "enhancement_request": "Add edge cases for error handling",
  "ticket_context": {
    "acceptance_criteria": ["..."],
    "ticket_key": "REW-123"
  }
}
```

**Response:**
```json
{
  "success": true,
  "agent": "TestCaseEnhancerAgent",
  "response": "Enhanced Gherkin test cases..."
}
```

### 4. Bug Triage Agent

**Purpose:** Automatic bug triaging and routing

**Capabilities:**
- Priority assessment (Critical/High/Medium/Low)
- Squad assignment (Loyalty Mission/Virality/Rewards)
- Component detection
- Urgency scoring (0-10)
- Label/tag recommendations
- Immediate action suggestions

**API Endpoint:** `POST /api/agents/triage-bug`

**Request:**
```json
{
  "title": "Checkout fails with rewards points",
  "description": "Users can't complete checkout when redeeming points",
  "environment": "Production"
}
```

**Response:**
```json
{
  "success": true,
  "agent": "BugTriageAgent",
  "response": "{...triage recommendations JSON...}"
}
```

## Smart Workflow

The **Smart Workflow** orchestrates multiple agents for comprehensive bug analysis:

1. Analyze bug quality (Bug Analyzer)
2. Auto-triage (Bug Triage)
3. Extract recommendations for bug creation

**API Endpoint:** `POST /api/agents/smart-workflow`

**Request:**
```json
{
  "title": "Bug title",
  "description": "Bug description",
  "steps": "Steps to reproduce"
}
```

**Response:**
```json
{
  "workflow": "smart_bug_creation",
  "steps": [
    { "step": "analysis", "agent": "bug_analyzer", "result": {...} },
    { "step": "triage", "agent": "bug_triage", "result": {...} }
  ],
  "recommendations": {
    "priority": "High",
    "squad": "Loyalty Mission Squad",
    "labels": ["ios", "checkout", "rewards"],
    "quality_score": 8,
    "improvements": ["Add specific iOS version", "Include error logs"]
  }
}
```

## Frontend Integration

### AI Insights Component

The `AIInsights` component in the React frontend provides:

- Real-time bug analysis
- Auto-triage recommendations
- Visual quality scoring
- Priority suggestions
- Label recommendations
- One-click analysis

**Usage in BugForm:**
```tsx
<AIInsights
  bugData={{
    title,
    description,
    steps,
    expected,
    actual,
    environment,
    priority
  }}
  onApplyRecommendations={(recommendations) => {
    if (recommendations.priority) {
      setPriority(recommendations.priority);
    }
  }}
/>
```

### Test Case Enhancement

The Test Case Generator includes AI enhancement:

**Quick Actions:**
- Add Edge Cases
- Add Negative Tests
- More Detail
- Platform Tests

**Custom Enhancement:**
Users can provide custom enhancement requests like:
- "Add tests for authentication edge cases"
- "Include boundary condition tests"
- "Add iOS-specific scenarios"

## Configuration

### Environment Variables

```bash
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
```

### Agent Manager Initialization

```python
from agents import AgentManager

# Initialize the agent system
agent_manager = AgentManager(
    aws_region='us-east-1',
    model_id='anthropic.claude-3-5-sonnet-20241022-v2:0'
)

# List available agents
agents = agent_manager.list_agents()

# Use specific agents
result = agent_manager.analyze_bug(bug_data)
result = agent_manager.triage_bug(bug_data)
result = agent_manager.enhance_test_cases(test_cases, request)
```

## API Reference

### List All Agents

```
GET /api/agents
```

**Response:**
```json
{
  "success": true,
  "agents": [
    {
      "name": "bug_analyzer",
      "description": "Analyzes bug reports...",
      "class": "BugAnalyzerAgent"
    }
  ],
  "count": 4
}
```

## Error Handling

All agent endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad request (missing required fields)
- `500` - Server error (AI invocation failed)
- `503` - Service unavailable (Agent system not initialized)

## Performance

**Average Response Times:**
- Bug Analysis: 3-5 seconds
- Bug Triage: 2-4 seconds
- Semantic Duplicate Check: 4-6 seconds
- Test Case Enhancement: 5-8 seconds
- Smart Workflow: 8-12 seconds (parallel execution)

**Token Usage:**
- Average input: 200-500 tokens
- Average output: 300-800 tokens
- Cost per request: ~$0.01-0.03 (Claude 3.5 Sonnet pricing)

## Best Practices

### 1. Bug Analysis
- Provide complete bug information for better analysis
- Include all required fields (title, description, steps)
- Add context about environment and platform

### 2. Duplicate Detection
- Run keyword search first (faster)
- Use semantic detection for borderline cases
- Review AI confidence levels

### 3. Test Enhancement
- Start with generated test cases
- Use quick actions for common improvements
- Iterate with specific requests
- Review AI suggestions before applying

### 4. Triage Automation
- Use for initial bug intake
- Review recommendations before applying
- Consider urgency signals for production issues

## Troubleshooting

### Agent System Not Initialized

**Error:** `Multi-Agent system not initialized`

**Solution:**
```bash
# Check AWS credentials
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY

# Verify Bedrock access
aws bedrock-runtime invoke-model --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 --body '{"messages":[{"role":"user","content":"test"}]}' --region us-east-1 output.json
```

### AWS Bedrock Errors

**Error:** `ClientError: Access Denied`

**Solution:**
- Ensure AWS credentials have `bedrock:InvokeModel` permission
- Verify model ID is correct for your region
- Check region availability for Claude models

### Slow Response Times

**Optimization:**
- Use parallel agent calls when possible
- Cache duplicate check results
- Limit context length for faster processing
- Consider using Claude 3 Haiku for faster (but less capable) responses

## Future Enhancements

- [ ] Agent conversation memory for context
- [ ] Fine-tuned models for specific bug patterns
- [ ] Batch processing for multiple bugs
- [ ] Agent-to-agent communication
- [ ] Custom agent creation via configuration
- [ ] Performance metrics dashboard
- [ ] Agent feedback loop for improvement

## Credits

Built with:
- **AWS Bedrock** - AI infrastructure
- **Claude 3.5 Sonnet** - Language model
- **Flask** - Python backend
- **React** - Frontend UI
- **TypeScript** - Type safety
