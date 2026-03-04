/**
 * AI Agent Service
 * 
 * Client for Multi-Agent AI System
 */

import axios from 'axios';

const API_BASE = '/api';

export interface AgentInfo {
  name: string;
  description: string;
  class: string;
}

export interface BugAnalysisResult {
  success: boolean;
  agent: string;
  response: string;
  usage?: {
    input_tokens: number;
    output_tokens: number;
  };
  model: string;
  error?: string;
}

export interface TriageResult {
  success: boolean;
  agent: string;
  response: string;
  usage?: any;
  model: string;
  error?: string;
}

export interface SmartWorkflowResult {
  workflow: string;
  steps: Array<{
    step: string;
    agent: string;
    result: any;
  }>;
  recommendations?: {
    priority: string;
    squad: string;
    labels: string[];
    quality_score: number;
    improvements: string[];
  };
}

export const agentApi = {
  /**
   * List all available AI agents
   */
  listAgents: async (): Promise<{ agents: AgentInfo[]; count: number }> => {
    const response = await axios.get(`${API_BASE}/agents`);
    return response.data;
  },

  /**
   * Analyze a bug using AI
   */
  analyzeBug: async (bugData: {
    title: string;
    description: string;
    steps?: string;
    expected?: string;
    actual?: string;
    environment?: string;
    priority?: string;
  }): Promise<BugAnalysisResult> => {
    const response = await axios.post(`${API_BASE}/agents/analyze-bug`, bugData);
    return response.data;
  },

  /**
   * Auto-triage a bug using AI
   */
  triageBug: async (bugData: {
    title: string;
    description: string;
    steps?: string;
    expected?: string;
    actual?: string;
    environment?: string;
  }): Promise<TriageResult> => {
    const response = await axios.post(`${API_BASE}/agents/triage-bug`, bugData);
    return response.data;
  },

  /**
   * Check for semantic duplicates using AI
   */
  checkSemanticDuplicates: async (bugData: {
    title: string;
    description: string;
    steps?: string;
    environment?: string;
  }): Promise<any> => {
    const response = await axios.post(`${API_BASE}/agents/check-semantic-duplicates`, bugData);
    return response.data;
  },

  /**
   * Enhance test cases using AI
   */
  enhanceTestCases: async (data: {
    test_cases: string;
    enhancement_request: string;
    ticket_context?: any;
  }): Promise<any> => {
    const response = await axios.post(`${API_BASE}/agents/enhance-test-cases`, data);
    return response.data;
  },

  /**
   * Run complete smart workflow
   */
  runSmartWorkflow: async (bugData: {
    title: string;
    description: string;
    steps?: string;
    expected?: string;
    actual?: string;
    environment?: string;
  }): Promise<SmartWorkflowResult> => {
    const response = await axios.post(`${API_BASE}/agents/smart-workflow`, bugData);
    return response.data;
  },
};
