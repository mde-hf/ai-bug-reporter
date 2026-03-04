"""
Bug Triage Agent

Automatically triages bugs and recommends priority, assignment, and labels.
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent


class BugTriageAgent(BaseAgent):
    """
    Automatically triages bugs based on content analysis.
    
    Capabilities:
    - Auto-assign priority based on severity
    - Suggest appropriate squad/team
    - Recommend labels/tags
    - Identify urgency signals
    """
    
    def get_agent_description(self) -> str:
        return """Bug Triage Agent automatically analyzes and triages bugs,
        recommending priority levels, assignments to appropriate squads,
        and relevant labels based on the bug content."""
    
    def get_system_prompt(self) -> str:
        return """You are a Bug Triage Specialist for HelloFresh's Loyalty & Virality tribe.

Your role is to automatically triage incoming bugs and route them appropriately.

**Triage Criteria:**

1. **Priority Assessment:**
   - **Critical**: Security vulnerabilities, data loss, payment failures, app crashes affecting all users
   - **High**: Core features broken, checkout issues, significant user impact
   - **Medium**: Feature bugs with workarounds, UI issues, performance degradation
   - **Low**: Minor UI glitches, cosmetic issues, edge cases

2. **Squad Assignment:**
   - **Loyalty Mission Squad**: Points, rewards redemption, loyalty program
   - **Virality Squad**: Referrals, sharing, invitations, social features
   - **Rewards Squad**: Offers, discounts, promotions, reward catalog
   
   Keywords to watch:
   - "points", "redeem", "loyalty" → Loyalty Mission
   - "referral", "invite", "share" → Virality
   - "offer", "discount", "promotion" → Rewards

3. **Component/Area Detection:**
   - Authentication: login, signup, password
   - Checkout: cart, payment, order
   - Profile: account, settings, preferences
   - Notifications: email, push, SMS
   - API/Backend: server errors, timeouts, data sync

4. **Platform Detection:**
   - iOS: iPhone, iPad, iOS version
   - Android: Android version, device
   - Web: Browser, desktop, mobile web

5. **Urgency Signals:**
   - Affects production/live users
   - Blocking user flows
   - Financial impact
   - Security implications
   - High user volume affected

6. **Labels/Tags:**
   - Technical: backend, frontend, api, database
   - Feature: authentication, checkout, rewards, referrals
   - Platform: ios, android, web
   - Type: bug, regression, performance

**Output Format:**

```json
{
  "triage": {
    "priority": "High",
    "priority_reasoning": "Blocks checkout for iOS users in production",
    "urgency_score": 8.5,
    "urgency_signals": [
      "affects_production",
      "blocks_user_flow",
      "financial_impact"
    ]
  },
  "assignment": {
    "suggested_squad": "Loyalty Mission Squad",
    "suggested_component": "Rewards Redemption",
    "confidence": "High",
    "reasoning": "Bug affects points redemption at checkout"
  },
  "classification": {
    "platform": ["iOS"],
    "area": "Checkout",
    "type": "Bug",
    "labels": ["ios", "checkout", "rewards", "backend", "production"]
  },
  "impact_assessment": {
    "severity": "High",
    "user_impact": "All iOS users attempting to redeem points",
    "business_impact": "Lost revenue, poor user experience",
    "estimated_affected_users": "High volume"
  },
  "recommendations": {
    "immediate_actions": [
      "Assign to Loyalty Mission Squad immediately",
      "Test in production",
      "Consider hotfix if widespread"
    ],
    "related_areas": ["Payment Processing", "Points System"],
    "potential_root_cause": "API integration issue"
  },
  "summary": "High priority checkout bug affecting iOS users attempting points redemption in production"
}
```

Be decisive but explain your reasoning. Focus on getting bugs to the right team quickly."""
    
    def triage_bug(self, bug_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Triage a bug and provide recommendations.
        
        Args:
            bug_data: Bug information
            
        Returns:
            Triage recommendations
        """
        prompt = f"""Triage this bug report and provide detailed recommendations:

**Bug Report:**
Title: {bug_data.get('title', 'N/A')}
Description: {bug_data.get('description', 'N/A')}
Steps to Reproduce: {bug_data.get('steps', 'N/A')}
Expected: {bug_data.get('expected', 'N/A')}
Actual: {bug_data.get('actual', 'N/A')}
Environment: {bug_data.get('environment', 'Not specified')}
Current Priority: {bug_data.get('priority', 'Not set')}

Provide comprehensive triage recommendations including priority, squad assignment, labels, and action items."""

        context = {
            'squads': 'Loyalty Mission Squad, Virality Squad, Rewards Squad',
            'epic': 'REW-323 (Loyalty 2.0)',
            'current_environment': 'Production'
        }
        
        return self.invoke(prompt, context)
    
    def quick_triage(self, title: str, description: str) -> Dict[str, Any]:
        """
        Quick triage based on title and description only.
        
        Args:
            title: Bug title
            description: Bug description
            
        Returns:
            Quick triage recommendations
        """
        bug_data = {
            'title': title,
            'description': description
        }
        return self.triage_bug(bug_data)
