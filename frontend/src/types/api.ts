// API Types
export interface Bug {
  id: string;
  key: string;
  title: string;
  description: string;
  steps: string;
  expected: string;
  actual: string;
  priority: string;
  environment: string;
  project: string;
  status: string;
  jira_url: string;
  created_at: string;
}

export interface DuplicateBug {
  key: string;
  summary: string;
  status: string;
  url: string;
  similarity: number;
  created: string;
}

export interface BugRequest {
  title: string;
  description: string;
  steps_to_reproduce: string;
  expected_behavior: string;
  actual_behavior: string;
  priority: string;
  environment: string;
  project: string;
}

export interface BugResponse {
  success: boolean;
  message: string;
  jira_url?: string;
  key?: string;
}

export interface EpicStats {
  total_count: number;
  open_count: number;
  in_progress_count: number;
  resolved_count: number;
  closed_count: number;
  by_status: Record<string, number>;
  by_priority: Record<string, number>;
  by_platform: Record<string, number>;
  priority_matrix: Record<string, Record<string, number>>;
  creation_trend: TrendData[];
  avg_resolution_days: string;
}

export interface TrendData {
  date: string;
  count: number;
}

export interface TestCaseRequest {
  ticket_link: string;
}

export interface TestCaseResponse {
  success: boolean;
  ticket_key?: string;
  ticket_url?: string;
  summary?: string;
  description?: string;
  test_cases?: string;
  issue_type?: string;
  status?: string;
  priority?: string;
  source_type?: string;
  document_url?: string;
  error?: string;
}

export type Project = 'loyalty-2.0' | 'loyalty-mission' | 'virality' | 'rewards';

export type Priority = 'Low' | 'Medium' | 'High' | 'Critical';

export type Environment = 'Local' | 'Staging' | 'Production';
