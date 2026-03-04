"""
Duplicate Detective Agent

Advanced semantic duplicate detection using AI-powered analysis.
Goes beyond keyword matching to understand semantic similarity.
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent


class DuplicateDetectiveAgent(BaseAgent):
    """
    Semantic duplicate detection agent.
    
    Uses Claude to analyze bug descriptions semantically and identify
    duplicates that keyword matching might miss.
    """
    
    def get_agent_description(self) -> str:
        return """Duplicate Detective Agent uses semantic analysis to find 
        duplicate bugs that traditional keyword matching might miss, understanding
        the meaning and context of bug reports."""
    
    def get_system_prompt(self) -> str:
        return """You are a Duplicate Detection Expert specializing in identifying semantically similar bug reports.

Your role is to analyze bug reports and identify true duplicates, even when they use different wording.

**Analysis Approach:**

1. **Semantic Understanding:**
   - Focus on the underlying issue, not just keywords
   - "Login fails" and "Can't sign in" are the same issue
   - "App crashes" and "Application force closes" are duplicates
   - "Slow loading" and "Performance issue" might be related

2. **Context Analysis:**
   - Same affected feature/component
   - Same user flow/scenario
   - Similar symptoms/behavior
   - Same root cause (if identifiable)

3. **Similarity Scoring:**
   - **Exact Duplicate (95-100%)**: Same issue, different wording
   - **Very Similar (80-94%)**: Same core issue, minor variations
   - **Related (60-79%)**: Similar area/component, possibly same root cause
   - **Somewhat Related (40-59%)**: Same feature area, different issues
   - **Different (0-39%)**: Unrelated issues

4. **Key Differences to Note:**
   - Different platforms (iOS vs Android vs Web)
   - Different environments (Production vs Staging)
   - Different user flows
   - Different error conditions

**Output Format:**

```json
{
  "is_duplicate": true/false,
  "confidence": "High/Medium/Low",
  "similarity_score": 85,
  "similarity_category": "Very Similar",
  "reasoning": "Detailed explanation of why these are/aren't duplicates",
  "key_similarities": [
    "Both affect login flow",
    "Same error symptom (timeout)",
    "Same affected component (authentication)"
  ],
  "key_differences": [
    "Bug A is iOS, Bug B is Web",
    "Different error messages"
  ],
  "recommendation": "Mark as duplicate / Not a duplicate / Needs investigation",
  "suggested_action": "Close as duplicate of [KEY] / Create as new bug / Link as related"
}
```

Be precise and explain your reasoning clearly."""
    
    def compare_bugs(self, bug1: Dict[str, Any], bug2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two bugs for semantic similarity.
        
        Args:
            bug1: First bug data
            bug2: Second bug data
            
        Returns:
            Similarity analysis
        """
        prompt = f"""Compare these two bug reports and determine if they are duplicates:

**Bug 1:**
Title: {bug1.get('title', 'N/A')}
Description: {bug1.get('description', 'N/A')}
Steps: {bug1.get('steps', 'N/A')}
Platform: {bug1.get('platform', 'Unknown')}

**Bug 2:**
Title: {bug2.get('title', 'N/A')}
Description: {bug2.get('description', 'N/A')}
Steps: {bug2.get('steps', 'N/A')}
Platform: {bug2.get('platform', 'Unknown')}

Analyze semantic similarity and determine if these are duplicates."""

        return self.invoke(prompt)
    
    def find_semantic_duplicates(
        self, 
        bug_data: Dict[str, Any], 
        candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Find semantic duplicates from a list of candidates.
        
        Args:
            bug_data: New bug to check
            candidates: List of potential duplicate bugs
            
        Returns:
            Analysis with ranked duplicates
        """
        if not candidates:
            return {
                'success': True,
                'duplicates_found': [],
                'message': 'No candidates to compare'
            }
        
        # Build comparison prompt
        candidates_text = ""
        for i, candidate in enumerate(candidates, 1):
            candidates_text += f"\n**Candidate {i} [{candidate.get('key', 'N/A')}]:**\n"
            candidates_text += f"Title: {candidate.get('title', 'N/A')}\n"
            candidates_text += f"Description: {candidate.get('description', 'N/A')[:200]}...\n"
            candidates_text += f"Status: {candidate.get('status', 'Unknown')}\n"
        
        prompt = f"""Analyze this new bug report against existing bugs to find semantic duplicates:

**New Bug:**
Title: {bug_data.get('title', 'N/A')}
Description: {bug_data.get('description', 'N/A')}
Steps to Reproduce: {bug_data.get('steps', 'N/A')}
Environment: {bug_data.get('environment', 'Unknown')}

**Existing Bugs to Compare:**
{candidates_text}

For each candidate, provide:
1. Similarity score (0-100)
2. Is it a duplicate? (yes/no/maybe)
3. Brief reasoning
4. Recommendation

Format as JSON array:
```json
[
  {{
    "candidate_key": "REW-123",
    "similarity_score": 85,
    "is_duplicate": "yes",
    "reasoning": "Same issue with login timeout",
    "recommendation": "Mark as duplicate"
  }}
]
```"""

        return self.invoke(prompt)
