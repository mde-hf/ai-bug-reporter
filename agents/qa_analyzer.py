"""
QA Analyzer Agent

Analyzes GitHub repositories and pull requests from a QA perspective.
Identifies test coverage gaps, risk areas, and recommends testing focus.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class QAAnalyzerAgent(BaseAgent):
    """
    QA Analysis agent for GitHub code review.
    
    Analyzes code changes, identifies risks, and recommends test strategies.
    """
    
    def get_agent_description(self) -> str:
        return """QA Analyzer Agent reviews code changes from a quality assurance 
        perspective, identifying test coverage gaps, risk areas, and providing 
        actionable testing recommendations."""
    
    def get_system_prompt(self) -> str:
        return """You are a Senior QA Engineer with expertise in test strategy, risk assessment, and code quality.

Your role is to analyze code changes from a QA perspective and provide actionable insights.

**Analysis Framework:**

1. **Test Coverage Assessment:**
   - Do tests exist for the changes?
   - Are edge cases covered?
   - Error handling tested?
   - Integration points tested?
   
2. **Risk Classification:**
   - **🔴 High Risk:**
     * Authentication/Security changes
     * Payment/Financial logic
     * Data migration/Database changes
     * API breaking changes
     * Critical user flows
   
   - **🟡 Medium Risk:**
     * Business logic modifications
     * External API integrations
     * State management changes
     * New features
   
   - **🟢 Low Risk:**
     * UI styling only
     * Copy/text changes
     * Documentation updates
     * Code formatting

3. **Testing Recommendations:**
   - Prioritize what to test first
   - Suggest specific test scenarios
   - Identify missing test types (unit/integration/e2e)
   - Recommend automation opportunities

4. **Quality Concerns:**
   - Code complexity issues
   - Potential bugs or edge cases
   - Performance implications
   - Security vulnerabilities

**Output Format:**

```json
{
  "coverage_score": 65,
  "coverage_assessment": "Moderate - some tests present but gaps exist",
  "risk_level": "High",
  "test_breakdown": {
    "unit_tests": {
      "count": 12,
      "coverage_percentage": 70,
      "status": "Good"
    },
    "integration_tests": {
      "count": 5,
      "coverage_percentage": 40,
      "status": "Needs Improvement"
    },
    "ui_tests": {
      "count": 2,
      "coverage_percentage": 20,
      "status": "Poor"
    },
    "e2e_tests": {
      "count": 1,
      "coverage_percentage": 10,
      "status": "Poor"
    }
  },
  "risk_areas": [
    {
      "file": "auth.py",
      "risk": "High",
      "reason": "Security-critical authentication changes with no corresponding tests",
      "concern": "Potential security vulnerability if edge cases not handled"
    }
  ],
  "test_recommendations": [
    {
      "priority": "Critical",
      "area": "Authentication",
      "test_type": "Unit",
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
    "Integration tests for login flow",
    "Error handling tests"
  ],
  "suggested_test_cases": [
    "Test expired token returns 401",
    "Test malformed token returns 400",
    "Test successful authentication flow"
  ]
}
```

**Test Type Analysis:**
- Count existing tests by type (unit/integration/UI/E2E)
- Estimate coverage percentage per type
- Status: Good (70%+), Needs Improvement (40-69%), Poor (<40%)

Be specific, actionable, and prioritize by risk."""
    
    def analyze_pr(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a pull request for QA concerns.
        
        Args:
            pr_data: Pull request information including files, diff, description
            
        Returns:
            QA analysis with risks, coverage, and recommendations
        """
        changed_files = pr_data.get('changed_files', [])
        pr_title = pr_data.get('title', 'N/A')
        pr_description = pr_data.get('description', 'N/A')
        
        files_summary = "\n".join([
            f"- {f['filename']} (+{f['additions']} -{f['deletions']})"
            for f in changed_files[:10]  # Limit to 10 files for context
        ])
        
        prompt = f"""Analyze this pull request from a QA perspective:

**PR Title:** {pr_title}

**PR Description:**
{pr_description[:1000]}

**Changed Files:**
{files_summary}

Provide a COMPREHENSIVE analysis with ALL sections:

1. **Test Coverage Analysis**:
   - Overall coverage score (0-100)
   - Coverage assessment
   - Test breakdown by type (unit, integration, UI, E2E)

2. **Risk Assessment**:
   - Overall risk level (High/Medium/Low)
   - Specific risk areas with file names

3. **Testing Recommendations**:
   - Prioritized test recommendations
   - Specific test scenarios

4. **Developer Recommendations** (REQUIRED - at least 3):
   - Code quality improvements
   - Refactoring suggestions
   - Error handling enhancements
   - Testability improvements
   - Each with: priority, area, recommendation, action, benefit

5. **QA Recommendations** (REQUIRED - at least 3):
   - Testing focus areas
   - Security vulnerabilities to check
   - Test coverage gaps
   - Each with: priority, area, focus, vulnerabilities[], test_coverage_needed[]

6. **Missing Tests & Suggested Test Cases**

**CRITICAL**: Include complete developer_recommendations and qa_recommendations arrays in your JSON response. These are NOT optional.

Format as JSON matching the structure in your system prompt."""

        return self.invoke(prompt)
    
    def analyze_code_changes(self, changes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze specific code changes for test gaps.
        
        Args:
            changes: Dictionary with file changes and diffs
            
        Returns:
            Detailed analysis of test coverage gaps
        """
        files_info = ""
        for file_path, file_data in changes.items():
            additions = file_data.get('additions', 0)
            deletions = file_data.get('deletions', 0)
            patch = file_data.get('patch', '')[:500]  # First 500 chars
            
            files_info += f"""
File: {file_path}
Changes: +{additions} -{deletions}
Sample diff:
{patch}
---
"""
        
        prompt = f"""Analyze these code changes for test coverage:

{files_info}

Identify:
1. What functionality changed?
2. Are there corresponding test files?
3. What tests are missing?
4. What edge cases should be tested?
5. Risk level for each changed file

Be specific about what tests are needed."""

        return self.invoke(prompt)
