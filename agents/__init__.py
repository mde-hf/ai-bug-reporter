"""
Multi-Agent AI System for Bug Reporter

This package provides specialized AI agents powered by AWS Bedrock (Claude 3.5 Sonnet).
"""

from .base_agent import BaseAgent
from .bug_analyzer import BugAnalyzerAgent
from .duplicate_detective import DuplicateDetectiveAgent
from .test_enhancer import TestCaseEnhancerAgent
from .bug_triage import BugTriageAgent
from .agent_manager import AgentManager

__all__ = [
    'BaseAgent',
    'BugAnalyzerAgent',
    'DuplicateDetectiveAgent',
    'TestCaseEnhancerAgent',
    'BugTriageAgent',
    'AgentManager'
]

__version__ = '1.0.0'
