# GitHub PR QA Analysis Feature

AI-powered QA analysis for GitHub Pull Requests to identify test coverage gaps, risk areas, and testing recommendations.

## Overview

This feature uses Claude AI to analyze GitHub pull requests from a quality assurance perspective, helping teams identify:

- **Test Coverage Gaps**: Areas lacking sufficient test coverage
- **Risk Assessment**: High/Medium/Low risk classification for changes
- **Testing Recommendations**: Prioritized, actionable testing suggestions
- **Missing Tests**: Specific test files and scenarios that should be added
- **Quality Concerns**: Potential bugs, edge cases, and security issues

## Setup

### 1. GitHub Personal Access Token

You need a GitHub Personal Access Token to access PR data:

1. Go to: https://github.com/settings/tokens/new
2. Set token description: "Bug Reporter QA Analysis"
3. Select expiration (recommend: 90 days)
4. Select scopes:
   - ✅ **repo** (Full control of private repositories)
     - This includes repo:status, repo_deployment, public_repo, repo:invite, security_events
5. Click "Generate token"
6. Copy the token (starts with `ghp_`)

**Security Best Practices:**
- Never commit your token to git
- Store it in `.env` file (which is gitignored)
- Rotate tokens periodically
- Use fine-grained tokens if possible for better security

### 2. Add to Environment

Add your token to `.env`:

```bash
GITHUB_TOKEN=ghp_your_actual_token_here
```

### 3. Verify Setup

The backend will check for the token on startup. You'll see:

```
[INFO] GitHub token configured for QA Analysis
```

If missing:

```
[WARNING] GitHub token not configured - QA Analysis feature unavailable
```

## Usage

### Via Web UI

1. Navigate to "QA Analysis" tab
2. Enter GitHub PR URL:
   ```
   https://github.com/owner/repo/pull/123
   ```
3. Click "Analyze PR"
4. Wait 30-60 seconds for AI analysis
5. Review results:
   - Test Coverage Score (0-100%)
   - Risk Level (High/Medium/Low)
   - Risk Areas with specific concerns
   - Prioritized Testing Recommendations
   - Missing Tests list
   - Suggested Test Cases

### Supported URLs

- ✅ Pull Request: `https://github.com/owner/repo/pull/123`
- ❌ Repository: Not yet supported (coming soon)

### Example Analysis Output

```json
{
  "coverage_score": 65,
  "coverage_assessment": "Moderate - some tests present but gaps exist",
  "risk_level": "High",
  "risk_areas": [
    {
      "file": "src/auth.py",
      "risk": "High",
      "reason": "Security-critical authentication changes with no tests",
      "concern": "Potential vulnerability if edge cases not handled"
    }
  ],
  "test_recommendations": [
    {
      "priority": "Critical",
      "area": "Authentication",
      "recommendation": "Add unit tests for token validation edge cases",
      "test_scenarios": [
        "Expired token handling",
        "Invalid token format",
        "Missing token header"
      ]
    }
  ],
  "missing_tests": [
    "Unit tests for auth.py",
    "Integration tests for login flow"
  ]
}
```

## Architecture

### Backend

**File**: `app.py`

**Endpoint**: `POST /api/analyze-github`

**Request**:
```json
{
  "url": "https://github.com/owner/repo/pull/123",
  "type": "pr"
}
```

**Flow**:
1. Parse GitHub URL
2. Fetch PR data via PyGithub (files, diffs, metadata)
3. Get QA Analyzer agent from Agent Manager
4. Send PR data to Claude AI with specialized QA prompt
5. Parse AI response (JSON format)
6. Return structured analysis

### AI Agent

**File**: `agents/qa_analyzer.py`

**Class**: `QAAnalyzerAgent`

**Responsibilities**:
- Analyze PR changes for test coverage
- Classify risk levels (High/Medium/Low)
- Generate actionable testing recommendations
- Identify missing tests and edge cases
- Assess code quality concerns

**System Prompt Highlights**:
- Senior QA Engineer persona
- Risk classification framework (Security, Payments, DB changes = High)
- Test coverage assessment criteria
- Structured JSON output format

### Frontend

**Files**:
- `frontend/src/pages/QAAnalysis.tsx` - Main component
- `frontend/src/pages/QAAnalysis.css` - Styling

**Features**:
- PR URL input with validation
- Loading states with spinner
- Error handling with clear messages
- Structured results display:
  - PR metadata (title, files changed, additions/deletions)
  - Coverage score with color coding
  - Risk badge with appropriate colors
  - Expandable risk areas
  - Prioritized recommendations
  - Missing tests checklist

## Dependencies

### Python
- `PyGithub==2.1.1` - GitHub API client
- Existing: `anthropic`, `Flask`, `requests`

### Frontend
- Existing: `React`, `TypeScript`, `axios`, `react-router-dom`

## Error Handling

### Common Errors

**"GitHub token not configured"**
- Solution: Add `GITHUB_TOKEN` to `.env` file

**"Failed to fetch PR data: 401"**
- Solution: Token expired or invalid, generate new one
- Solution: Token lacks `repo` scope, recreate with correct permissions

**"Invalid GitHub URL"**
- Solution: Use format `https://github.com/owner/repo/pull/123`

**"Repository analysis not yet implemented"**
- This is expected - only PR analysis is supported in MVP

**"Multi-Agent system not initialized"**
- Solution: Ensure Claude CLI or Anthropic API is configured
- Check logs for AI provider status

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check Claude AI status:

```bash
which claude  # Should show path if CLI available
echo $ANTHROPIC_API_KEY  # Should show key if API configured
```

## Testing

### Manual Testing

1. Use a public GitHub PR (e.g., from an open-source project)
2. Analyze a PR with various characteristics:
   - High risk (auth/payment changes)
   - Good test coverage
   - Poor test coverage
   - Multiple files
   - Single file

### Expected Behavior

- Analysis takes 30-90 seconds (AI processing time)
- Coverage score should be reasonable (0-100)
- Risk level should match change type
- Recommendations should be specific and actionable

## Future Enhancements

### Planned Features

1. **Repository Analysis**
   - Overall test coverage for entire repo
   - Risk heat map of files
   - Test suite health metrics

2. **Batch Analysis**
   - Analyze multiple PRs at once
   - Compare PRs from same epic/feature

3. **Integration**
   - Auto-analyze PRs when creating bugs
   - Link JIRA tickets to PR analysis
   - Slack notifications for high-risk PRs

4. **Historical Data**
   - Track coverage trends over time
   - Store analysis results
   - Generate reports

5. **Enhanced Metrics**
   - Cyclomatic complexity
   - Code duplication detection
   - Performance impact prediction

## API Reference

### Analyze GitHub PR

**Endpoint**: `POST /api/analyze-github`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "url": "https://github.com/owner/repo/pull/123",
  "type": "pr"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "analysis": {
    "coverage_score": 75,
    "coverage_assessment": "Good",
    "risk_level": "Medium",
    "risk_areas": [...],
    "test_recommendations": [...],
    "missing_tests": [...],
    "suggested_test_cases": [...]
  },
  "pr_info": {
    "title": "Add user authentication",
    "files_changed": 5,
    "additions": 234,
    "deletions": 12,
    "url": "https://github.com/owner/repo/pull/123"
  },
  "method": "claude-cli"
}
```

**Error Response (503)**:
```json
{
  "success": false,
  "error": "GitHub token not configured. Add GITHUB_TOKEN to .env file."
}
```

**Error Response (400)**:
```json
{
  "success": false,
  "error": "Invalid GitHub URL. Expected format: https://github.com/owner/repo/pull/123"
}
```

## Contributing

When enhancing this feature:

1. Update `QAAnalyzerAgent` system prompt for better analysis
2. Add new risk categories in the agent's classification
3. Enhance frontend UI for better visualization
4. Add unit tests for new functionality
5. Update this documentation

## Support

For issues or questions:
1. Check logs for error messages
2. Verify GitHub token permissions
3. Test with a public PR first
4. Review Claude AI configuration

## License

Part of Bug Reporter application - internal HelloFresh tool.
