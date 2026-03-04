/**
 * AI Agent Service
 * 
 * Client for Multi-Agent AI System - Test Case Enhancement only
 */

import axios from 'axios';

const API_BASE = '/api';

export const agentApi = {
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
};
