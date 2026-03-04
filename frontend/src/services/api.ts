import axios from 'axios';
import type {
  DuplicateBug,
  DuplicateCheckResponse,
  BugRequest,
  BugResponse,
  EpicStats,
  TestCaseRequest,
  TestCaseResponse,
} from '@/types/api';

// Create axios instance
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Service
export const bugApi = {
  // Check for duplicate bugs
  async checkDuplicates(title: string, description: string): Promise<DuplicateBug[]> {
    const response = await api.post<DuplicateCheckResponse>('/check-duplicates', {
      title,
      description,
    });
    return response.data.duplicates;
  },

  // Create a new bug
  async createBug(bug: BugRequest, attachments?: File[]): Promise<BugResponse> {
    const formData = new FormData();
    formData.append('title', bug.title);
    formData.append('description', bug.description);
    formData.append('steps_to_reproduce', bug.steps_to_reproduce);
    formData.append('expected_behavior', bug.expected_behavior);
    formData.append('actual_behavior', bug.actual_behavior);
    formData.append('priority', bug.priority);
    formData.append('environment', bug.environment);
    formData.append('project', bug.project);

    if (attachments) {
      attachments.forEach((file) => {
        formData.append('attachments', file);
      });
    }

    const response = await api.post<BugResponse>('/create-bug', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get epic statistics
  async getEpicStats(): Promise<EpicStats> {
    const response = await api.get<EpicStats>('/epic-stats');
    return response.data;
  },

  // Generate test cases
  async generateTestCases(request: TestCaseRequest): Promise<TestCaseResponse> {
    const response = await api.post<TestCaseResponse>('/generate-test-cases', {
      ticket: request.ticket_link, // Backend expects 'ticket' not 'ticket_link'
    });
    return response.data;
  },
};

export default api;
