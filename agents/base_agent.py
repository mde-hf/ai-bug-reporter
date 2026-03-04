"""
Multi-Agent AI System for Bug Reporter

This module provides specialized AI agents for intelligent bug management.
Each agent is powered by Anthropic API (Claude 3.5 Sonnet) - like Agento.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, anthropic_client, model_id: str, claude_cli_path=None):
        """
        Initialize the agent with Anthropic client and optional Claude CLI.
        
        Args:
            anthropic_client: anthropic.Anthropic client
            model_id: Claude model ID
            claude_cli_path: Path to Claude CLI executable (priority over API)
        """
        self.anthropic_client = anthropic_client
        self.model_id = model_id
        self.agent_name = self.__class__.__name__
        self.claude_cli_path = claude_cli_path
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    @abstractmethod
    def get_agent_description(self) -> str:
        """Return a description of what this agent does"""
        pass
    
    def invoke(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Invoke the agent with a prompt.
        Priority: Claude CLI > Anthropic API
        
        Args:
            prompt: User prompt/question
            context: Optional context data
            
        Returns:
            Dict containing response and metadata
        """
        try:
            system_prompt = self.get_system_prompt()
            
            # Build the full prompt with context
            full_prompt = self._build_prompt(prompt, context)
            
            logger.info(f"Invoking {self.agent_name}", extra={
                'agent': self.agent_name,
                'prompt_length': len(full_prompt)
            })
            
            # Priority 1: Try Claude CLI (company AWS)
            if self.claude_cli_path:
                try:
                    import subprocess
                    logger.info(f"{self.agent_name}: Trying Claude CLI...")
                    
                    result = subprocess.run(
                        [self.claude_cli_path, '--model', 'sonnet', '--message', full_prompt],
                        capture_output=True,
                        text=True,
                        timeout=120,
                        check=True
                    )
                    
                    if result.stdout:
                        response_text = result.stdout.strip()
                        logger.info(f"{self.agent_name} completed successfully via CLI")
                        return {
                            'success': True,
                            'agent': self.agent_name,
                            'response': response_text,
                            'provider': 'claude_cli',
                            'model': 'claude-3-5-sonnet'
                        }
                except Exception as cli_error:
                    logger.warning(f"Claude CLI failed: {cli_error}, trying API...")
            
            # Priority 2: Try Anthropic API (personal)
            if self.anthropic_client:
                logger.info(f"{self.agent_name}: Trying Anthropic API...")
                message = self.anthropic_client.messages.create(
                    model=self.model_id,
                    max_tokens=4096,
                    system=system_prompt,
                    messages=[{
                        "role": "user",
                        "content": full_prompt
                    }]
                )
                
                # Extract the response text
                response_text = message.content[0].text if message.content else ""
                
                logger.info(f"{self.agent_name} completed successfully via API")
                
                return {
                    'success': True,
                    'agent': self.agent_name,
                    'response': response_text,
                    'usage': {
                        'input_tokens': message.usage.input_tokens,
                        'output_tokens': message.usage.output_tokens
                    },
                    'provider': 'anthropic_api',
                    'model': self.model_id
                }
            
            # No provider available
            raise Exception("No AI provider available (neither CLI nor API)")
            
        except Exception as e:
            logger.error(f"{self.agent_name} error: {e}")
            return {
                'success': False,
                'agent': self.agent_name,
                'error': str(e)
            }
    
    def _build_prompt(self, prompt: str, context: Optional[Dict[str, Any]]) -> str:
        """Build the full prompt with context"""
        if not context:
            return prompt
        
        # Format context as a structured string
        context_str = "\n\n**Context:**\n"
        for key, value in context.items():
            if value:
                context_str += f"\n**{key.replace('_', ' ').title()}:**\n{value}\n"
        
        return f"{context_str}\n\n**Task:**\n{prompt}"
