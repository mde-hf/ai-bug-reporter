"""
Bug Analyzer Agent

Analyzes bug reports and provides intelligent suggestions for improvement.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class BugAnalyzerAgent(BaseAgent):
    """
    Analyzes bug reports and suggests improvements.
    
    Capabilities:
    - Identifies missing information
    - Suggests priority based on severity keywords
    - Detects environment from description
    - Recommends assignees based on component/area
    - Validates bug quality
    """
    
    def get_agent_description(self) -> str:
        return """Bug Analyzer Agent analyzes bug reports and provides intelligent 
        suggestions to improve bug quality, including missing information, 
        priority recommendations, and assignee suggestions."""
    
    def get_system_prompt(self) -> str:
        return """You are a Bug Analysis Expert for HelloFresh's Loyalty & Virality tribe.

Your role is to analyze bug reports and provide actionable suggestions to improve their quality.

**Analysis Areas:**

1. **Completeness Check:**
   - Are all required fields filled? (title, description, steps, expected, actual)
   - Is the description clear and detailed?
   - Are steps to reproduce specific and reproducible?
   - Is there enough information to understand and fix the bug?

2. **Priority Assessment:**
   - Analyze severity keywords: crash, data loss, security, performance, UI glitch
   - Consider impact: affects all users vs specific scenario
   - Suggest priority: Low, Medium, High, or Critical
   - Explain reasoning

3. **Environment Detection:**
   - Detect platform: iOS, Android, Web
   - Identify environment: Production, Staging, Local
   - Look for version numbers, device info, browser details

4. **Component/Area Detection:**
   - Identify affected component: Authentication, Rewards, Checkout, Profile, etc.
   - Suggest which squad should handle: Loyalty Mission, Virality, Rewards
   - Recommend potential assignee if obvious

5. **Quality Score:**
   - Rate bug quality: Excellent, Good, Needs Improvement, Poor
   - Explain score reasoning
   - List specific improvements needed

**Output Format:**
Provide your analysis as a structured JSON object:

```json
{
  "completeness": {
    "score": "Good/Needs Improvement/Poor",
    "missing_fields": ["field1", "field2"],
    "suggestions": ["Add browser version", "Include error message"]
  },
  "priority_recommendation": {
    "suggested_priority": "High",
    "reasoning": "Affects checkout flow for all users",
    "severity_keywords": ["checkout", "payment", "all users"]
  },
  "environment_detection": {
    "platform": "iOS/Android/Web",
    "environment": "Production",
    "confidence": "High/Medium/Low"
  },
  "component_analysis": {
    "affected_component": "Checkout",
    "suggested_squad": "Loyalty Mission Squad",
    "potential_assignee": "Backend Team"
  },
  "quality_score": {
    "score": "Good",
    "rating": 8,
    "improvements": ["Add specific iOS version", "Include error logs"]
  },
  "summary": "Brief summary of analysis and key recommendations"
}
```

Be specific, actionable, and helpful. Focus on making the bug easier to understand and fix."""
    
    def analyze_bug(self, bug_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a bug report.
        
        Args:
            bug_data: Dict containing bug information
            
        Returns:
            Analysis results with suggestions
        """
        prompt = f"""Analyze this bug report and provide comprehensive feedback:

**Bug Title:** {bug_data.get('title', 'N/A')}
**Priority:** {bug_data.get('priority', 'Not set')}
**Environment:** {bug_data.get('environment', 'Not specified')}

**Description:**
{bug_data.get('description', 'No description provided')}

**Steps to Reproduce:**
{bug_data.get('steps', 'No steps provided')}

**Expected Behavior:**
{bug_data.get('expected', 'Not specified')}

**Actual Behavior:**
{bug_data.get('actual', 'Not specified')}

Provide a detailed analysis with actionable suggestions."""

        context = {
            'squad_context': 'HelloFresh Loyalty & Virality tribe',
            'available_squads': 'Loyalty Mission Squad, Virality Squad, Rewards Squad',
            'common_components': 'Authentication, Rewards, Checkout, Profile, Referrals, Points'
        }
        
        return self.invoke(prompt, context)
