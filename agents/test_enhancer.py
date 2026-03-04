"""
Test Case Enhancer Agent

Iteratively improves test cases through conversation and refinement.
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent


class TestCaseEnhancerAgent(BaseAgent):
    """
    Enhances and refines test cases through iterative feedback.
    
    Supports multi-turn conversations for test case refinement.
    """
    
    def __init__(self, anthropic_client, model_id: str, claude_cli_path=None):
        super().__init__(anthropic_client, model_id, claude_cli_path)
        self.conversation_history = []
    
    def get_agent_description(self) -> str:
        return """Test Case Enhancer Agent refines and improves test cases 
        through iterative feedback, adding edge cases, improving coverage, 
        and ensuring comprehensive testing."""
    
    def get_system_prompt(self) -> str:
        return """You are a Test Case Enhancement Expert specializing in Cucumber Gherkin test scenarios.

Your role is to refine and improve test cases based on user feedback and requirements.

**Capabilities:**

1. **Add More Coverage:**
   - Generate additional edge cases
   - Add boundary condition tests
   - Include negative scenarios
   - Add integration test cases

2. **Improve Specificity:**
   - Make steps more detailed
   - Add specific test data
   - Include exact expected outcomes
   - Add assertions for verification

3. **Focus on Specific Areas:**
   - Authentication flows
   - Payment processing
   - Data validation
   - Error handling
   - Platform-specific behaviors

4. **Test Case Quality:**
   - Follow Gherkin best practices
   - Use clear Given-When-Then format
   - Include appropriate tags (@smoke, @regression, @edge_case)
   - Make scenarios independent and repeatable

**Interaction Style:**
- Ask clarifying questions when needed
- Explain changes you're making
- Provide options when multiple approaches exist
- Reference Acceptance Criteria from the ticket

**Output Format:**
Return enhanced test cases in Gherkin format with clear section headers.

Be conversational, helpful, and focused on test quality."""
    
    def enhance_test_cases(
        self, 
        test_cases: str, 
        enhancement_request: str,
        ticket_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhance existing test cases based on feedback.
        
        Args:
            test_cases: Current test cases (Gherkin format)
            enhancement_request: What to improve/add
            ticket_context: Optional ticket information
            
        Returns:
            Enhanced test cases
        """
        prompt = f"""Current Test Cases:

```gherkin
{test_cases}
```

**Enhancement Request:**
{enhancement_request}

Please enhance these test cases according to the request. Provide the improved version."""

        context = ticket_context or {}
        result = self.invoke(prompt, context)
        
        # Store in conversation history
        self.conversation_history.append({
            'request': enhancement_request,
            'response': result.get('response', '')
        })
        
        return result
    
    def add_edge_cases(self, test_cases: str, focus_area: str = None) -> Dict[str, Any]:
        """Quick method to add edge cases"""
        request = f"Add comprehensive edge cases"
        if focus_area:
            request += f" focusing on {focus_area}"
        return self.enhance_test_cases(test_cases, request)
    
    def improve_coverage(self, test_cases: str, acceptance_criteria: List[str]) -> Dict[str, Any]:
        """Improve test coverage for specific acceptance criteria"""
        ac_text = "\n".join(f"- {ac}" for ac in acceptance_criteria)
        request = f"""Improve test coverage to ensure all acceptance criteria are tested:

{ac_text}

Add missing test scenarios and ensure each criterion has dedicated tests."""
        
        return self.enhance_test_cases(test_cases, request)
    
    def add_platform_tests(self, test_cases: str, platforms: List[str]) -> Dict[str, Any]:
        """Add platform-specific test scenarios"""
        platforms_text = ", ".join(platforms)
        request = f"Add platform-specific test scenarios for: {platforms_text}"
        return self.enhance_test_cases(test_cases, request)
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
