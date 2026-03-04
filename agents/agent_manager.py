"""
Agent Manager

Orchestrates multiple AI agents and manages their interactions.
Uses Anthropic API like Agento.
"""

import logging
from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class AgentManager:
    """
    Manages all AI agents and provides unified interface.
    
    Handles agent initialization, selection, and coordination.
    """
    
    def __init__(self, anthropic_client, model_id: str = "claude-3-5-sonnet-20241022", claude_cli_path=None):
        """
        Initialize the Agent Manager.
        
        Args:
            anthropic_client: Anthropic client instance
            model_id: Claude model ID to use
            claude_cli_path: Path to Claude CLI executable (like Agento)
        """
        self.anthropic_client = anthropic_client
        self.model_id = model_id
        self.claude_cli_path = claude_cli_path
        
        # Initialize all agents
        self.agents = self._initialize_agents()
        
        # Log configuration
        if claude_cli_path:
            logger.info(f"Agent Manager: Using Claude CLI at {claude_cli_path}")
        elif anthropic_client:
            logger.info(f"Agent Manager: Using Anthropic API with {model_id}")
        else:
            logger.warning("Agent Manager: No AI provider available!")
        
        logger.info(f"Agent Manager initialized with {len(self.agents)} agents")
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all available agents"""
        if not self.anthropic_client and not self.claude_cli_path:
            logger.warning("No AI provider available - agents will not function")
            return {}
        
        from .bug_analyzer import BugAnalyzerAgent
        from .duplicate_detective import DuplicateDetectiveAgent
        from .test_enhancer import TestCaseEnhancerAgent
        from .bug_triage import BugTriageAgent
        from .qa_analyzer import QAAnalyzerAgent
        
        return {
            'bug_analyzer': BugAnalyzerAgent(self.anthropic_client, self.model_id, self.claude_cli_path),
            'duplicate_detective': DuplicateDetectiveAgent(self.anthropic_client, self.model_id, self.claude_cli_path),
            'test_enhancer': TestCaseEnhancerAgent(self.anthropic_client, self.model_id, self.claude_cli_path),
            'bug_triage': BugTriageAgent(self.anthropic_client, self.model_id, self.claude_cli_path),
            'qa_analyzer': QAAnalyzerAgent(self.anthropic_client, self.model_id, self.claude_cli_path)
        }
    
    def get_agent(self, agent_name: str) -> Optional[Any]:
        """
        Get a specific agent by name.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[Dict[str, str]]:
        """
        List all available agents.
        
        Returns:
            List of agent information
        """
        return [
            {
                'name': name,
                'description': agent.get_agent_description(),
                'class': agent.__class__.__name__
            }
            for name, agent in self.agents.items()
        ]
    
    def get_agent(self, agent_name: str) -> Optional['BaseAgent']:
        """
        Get a specific agent by name.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[Dict[str, str]]:
        """
        List all available agents.
        
        Returns:
            List of agent information
        """
        return [
            {
                'name': name,
                'description': agent.get_agent_description(),
                'class': agent.__class__.__name__
            }
            for name, agent in self.agents.items()
        ]
    
    def analyze_bug(self, bug_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a bug using the Bug Analyzer agent.
        
        Args:
            bug_data: Bug information
            
        Returns:
            Analysis results
        """
        agent = self.get_agent('bug_analyzer')
        if not agent:
            return {'success': False, 'error': 'Bug Analyzer agent not available'}
        
        return agent.analyze_bug(bug_data)
    
    def check_duplicates_semantic(
        self, 
        bug_data: Dict[str, Any], 
        candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check for semantic duplicates using AI.
        
        Args:
            bug_data: New bug to check
            candidates: List of potential duplicates
            
        Returns:
            Duplicate analysis
        """
        agent = self.get_agent('duplicate_detective')
        if not agent:
            return {'success': False, 'error': 'Duplicate Detective agent not available'}
        
        return agent.find_semantic_duplicates(bug_data, candidates)
    
    def enhance_test_cases(
        self, 
        test_cases: str, 
        enhancement_request: str,
        ticket_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhance test cases using AI.
        
        Args:
            test_cases: Current test cases
            enhancement_request: What to improve
            ticket_context: Optional ticket information
            
        Returns:
            Enhanced test cases
        """
        agent = self.get_agent('test_enhancer')
        if not agent:
            return {'success': False, 'error': 'Test Enhancer agent not available'}
        
        return agent.enhance_test_cases(test_cases, enhancement_request, ticket_context)
    
    def triage_bug(self, bug_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Automatically triage a bug.
        
        Args:
            bug_data: Bug information
            
        Returns:
            Triage recommendations
        """
        agent = self.get_agent('bug_triage')
        if not agent:
            return {'success': False, 'error': 'Bug Triage agent not available'}
        
        return agent.triage_bug(bug_data)
    
    def smart_bug_workflow(self, bug_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a complete AI-powered bug workflow.
        
        This orchestrates multiple agents:
        1. Analyze bug quality
        2. Auto-triage (priority, squad)
        3. Check for semantic duplicates
        
        Args:
            bug_data: Bug information
            
        Returns:
            Complete workflow results
        """
        logger.info("Starting smart bug workflow")
        
        results = {
            'workflow': 'smart_bug_creation',
            'steps': []
        }
        
        # Step 1: Analyze bug quality
        logger.info("Step 1: Analyzing bug quality")
        analysis = self.analyze_bug(bug_data)
        results['steps'].append({
            'step': 'analysis',
            'agent': 'bug_analyzer',
            'result': analysis
        })
        
        # Step 2: Auto-triage
        logger.info("Step 2: Auto-triaging bug")
        triage = self.triage_bug(bug_data)
        results['steps'].append({
            'step': 'triage',
            'agent': 'bug_triage',
            'result': triage
        })
        
        # Extract recommendations for bug creation
        if triage.get('success') and analysis.get('success'):
            results['recommendations'] = {
                'priority': self._extract_priority(triage),
                'squad': self._extract_squad(triage),
                'labels': self._extract_labels(triage),
                'quality_score': self._extract_quality_score(analysis),
                'improvements': self._extract_improvements(analysis)
            }
        
        logger.info("Smart bug workflow completed")
        return results
    
    def _extract_priority(self, triage_result: Dict[str, Any]) -> str:
        """Extract priority from triage result"""
        try:
            response_text = triage_result.get('response', '')
            if 'priority' in response_text.lower():
                if 'critical' in response_text.lower():
                    return 'Critical'
                elif 'high' in response_text.lower():
                    return 'High'
                elif 'low' in response_text.lower():
                    return 'Low'
            return 'Medium'
        except:
            return 'Medium'
    
    def _extract_squad(self, triage_result: Dict[str, Any]) -> str:
        """Extract squad from triage result"""
        try:
            response_text = triage_result.get('response', '').lower()
            if 'virality' in response_text:
                return 'Virality Squad'
            elif 'rewards squad' in response_text:
                return 'Rewards Squad'
            elif 'loyalty mission' in response_text:
                return 'Loyalty Mission Squad'
            return 'Loyalty Mission Squad'
        except:
            return 'Loyalty Mission Squad'
    
    def _extract_labels(self, triage_result: Dict[str, Any]) -> List[str]:
        """Extract labels from triage result"""
        try:
            response_text = triage_result.get('response', '').lower()
            labels = []
            label_keywords = ['ios', 'android', 'web', 'backend', 'frontend', 'api', 'checkout', 'authentication']
            for keyword in label_keywords:
                if keyword in response_text:
                    labels.append(keyword)
            return labels
        except:
            return []
    
    def _extract_quality_score(self, analysis_result: Dict[str, Any]) -> int:
        """Extract quality score from analysis result"""
        try:
            response_text = analysis_result.get('response', '')
            if 'excellent' in response_text.lower():
                return 9
            elif 'good' in response_text.lower():
                return 7
            elif 'needs improvement' in response_text.lower():
                return 5
            else:
                return 6
        except:
            return 6
    
    def _extract_improvements(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Extract improvement suggestions from analysis result"""
        try:
            response_text = analysis_result.get('response', '')
            improvements = []
            if 'add' in response_text.lower():
                improvements.append('Add more details')
            if 'missing' in response_text.lower():
                improvements.append('Include missing information')
            return improvements
        except:
            return []
