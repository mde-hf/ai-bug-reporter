import { useState } from 'react';
import axios from 'axios';
import './QAAnalysis.css';

interface PRInfo {
  title: string;
  files_changed: number;
  additions: number;
  deletions: number;
  url: string;
}

interface RiskArea {
  file: string;
  risk: string;
  reason: string;
  concern?: string;
}

interface TestRecommendation {
  priority: string;
  area: string;
  recommendation: string;
  test_scenarios?: string[];
}

interface TestTypeBreakdown {
  count: number;
  coverage_percentage: number;
  status: string;
}

interface TestBreakdown {
  unit_tests?: TestTypeBreakdown;
  integration_tests?: TestTypeBreakdown;
  ui_tests?: TestTypeBreakdown;
  e2e_tests?: TestTypeBreakdown;
}

interface AnalysisData {
  coverage_score?: number | string;
  coverage_assessment?: string;
  risk_level?: string;
  test_breakdown?: TestBreakdown;
  risk_areas?: RiskArea[];
  test_recommendations?: TestRecommendation[];
  missing_tests?: string[];
  suggested_test_cases?: string[];
  raw_analysis?: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function QAAnalysis() {
  const [githubUrl, setGithubUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [progressStatus, setProgressStatus] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [prInfo, setPrInfo] = useState<PRInfo | null>(null);

  const simulateProgress = () => {
    setProgress(0);
    setProgressStatus('Validating GitHub URL...');
    
    // Stage 1: Fetching PR data (0-20%)
    setTimeout(() => {
      setProgress(10);
      setProgressStatus('Connecting to GitHub...');
    }, 500);
    
    setTimeout(() => {
      setProgress(20);
      setProgressStatus('Fetching PR data...');
    }, 1500);
    
    // Stage 2: Analyzing files (20-30%)
    setTimeout(() => {
      setProgress(25);
      setProgressStatus('Loading changed files...');
    }, 3000);
    
    setTimeout(() => {
      setProgress(30);
      setProgressStatus('Analyzing code changes...');
    }, 4500);
    
    // Stage 3: AI Analysis (30-90%) - slower progress
    setTimeout(() => {
      setProgress(40);
      setProgressStatus('Running AI analysis...');
    }, 6000);
    
    setTimeout(() => {
      setProgress(50);
      setProgressStatus('Evaluating test coverage...');
    }, 10000);
    
    setTimeout(() => {
      setProgress(60);
      setProgressStatus('Identifying risk areas...');
    }, 15000);
    
    setTimeout(() => {
      setProgress(70);
      setProgressStatus('Generating recommendations...');
    }, 22000);
    
    setTimeout(() => {
      setProgress(80);
      setProgressStatus('Analyzing test types...');
    }, 30000);
    
    setTimeout(() => {
      setProgress(90);
      setProgressStatus('Finalizing analysis...');
    }, 40000);
    
    // Stage 4: Completing (90-95%)
    setTimeout(() => {
      setProgress(95);
      setProgressStatus('Preparing results...');
    }, 50000);
  };

  const handleAnalyze = async () => {
    if (!githubUrl.trim()) {
      setError('Please enter a GitHub PR URL');
      return;
    }

    // Basic URL validation
    if (!githubUrl.includes('github.com') || !githubUrl.includes('/pull/')) {
      setError('Invalid GitHub PR URL. Format: https://github.com/owner/repo/pull/123');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysis(null);
    setPrInfo(null);
    
    // Start progress simulation
    simulateProgress();

    try {
      const response = await axios.post(`${API_BASE_URL}/api/analyze-github`, {
        url: githubUrl,
        type: 'pr',
      });

      if (response.data.success) {
        setProgress(100);
        setProgressStatus('Complete!');
        setTimeout(() => {
          setAnalysis(response.data.analysis);
          setPrInfo(response.data.pr_info);
        }, 500);
      } else {
        setError(response.data.error || 'Analysis failed');
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || err.message || 'Failed to analyze GitHub PR';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string): string => {
    const lowerRisk = risk.toLowerCase();
    if (lowerRisk === 'high' || lowerRisk.includes('critical')) return '#dc2626';
    if (lowerRisk === 'medium' || lowerRisk === 'moderate') return '#ea580c';
    return '#16a34a';
  };

  const getCoverageColor = (score: number | string): string => {
    if (typeof score === 'string') return '#6b7280';
    if (score >= 80) return '#16a34a';
    if (score >= 60) return '#ea580c';
    return '#dc2626';
  };

  return (
    <div className="qa-analysis-container">
      <div className="qa-analysis-header">
        <h1>GitHub PR QA Analysis</h1>
        <p className="qa-analysis-subtitle">
          AI-powered analysis to identify test coverage gaps, risk areas, and testing recommendations
        </p>
      </div>

      <div className="qa-input-section">
        <div className="qa-input-group">
          <label htmlFor="github-url">GitHub Pull Request URL</label>
          <input
            id="github-url"
            type="text"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            placeholder="https://github.com/owner/repo/pull/123"
            disabled={loading}
          />
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading || !githubUrl.trim()}
          className="qa-analyze-button"
        >
          {loading ? 'Analyzing...' : 'Analyze PR'}
        </button>
      </div>

      {error && (
        <div className="qa-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {loading && (
        <div className="qa-loading">
          <div className="qa-spinner"></div>
          <p>Analyzing pull request... This may take 30-60 seconds.</p>
        </div>
      )}

      {analysis && prInfo && (
        <div className="qa-results">
          <div className="qa-pr-info">
            <h2>Pull Request Information</h2>
            <div className="qa-pr-stats">
              <div className="qa-stat">
                <span className="qa-stat-label">Title:</span>
                <span className="qa-stat-value">{prInfo.title}</span>
              </div>
              <div className="qa-stat">
                <span className="qa-stat-label">Files Changed:</span>
                <span className="qa-stat-value">{prInfo.files_changed}</span>
              </div>
              <div className="qa-stat">
                <span className="qa-stat-label">Lines Added:</span>
                <span className="qa-stat-value" style={{ color: '#16a34a' }}>
                  +{prInfo.additions}
                </span>
              </div>
              <div className="qa-stat">
                <span className="qa-stat-label">Lines Deleted:</span>
                <span className="qa-stat-value" style={{ color: '#dc2626' }}>
                  -{prInfo.deletions}
                </span>
              </div>
            </div>
            <a href={prInfo.url} target="_blank" rel="noopener noreferrer" className="qa-pr-link">
              View on GitHub
            </a>
          </div>

          {analysis.raw_analysis ? (
            <div className="qa-raw-analysis">
              <h2>AI Analysis</h2>
              <pre className="qa-raw-text">{analysis.raw_analysis}</pre>
            </div>
          ) : (
            <>
              <div className="qa-overview">
                <div className="qa-overview-card">
                  <h3>Test Coverage</h3>
                  <div
                    className="qa-coverage-score"
                    style={{ color: getCoverageColor(analysis.coverage_score || 'N/A') }}
                  >
                    {typeof analysis.coverage_score === 'number'
                      ? `${analysis.coverage_score}%`
                      : analysis.coverage_score}
                  </div>
                  {analysis.coverage_assessment && (
                    <p className="qa-assessment">{analysis.coverage_assessment}</p>
                  )}
                </div>

                <div className="qa-overview-card">
                  <h3>Risk Level</h3>
                  <div
                    className="qa-risk-badge"
                    style={{
                      backgroundColor: getRiskColor(analysis.risk_level || 'Unknown'),
                    }}
                  >
                    {analysis.risk_level || 'Unknown'}
                  </div>
                </div>
              </div>

              {analysis.test_breakdown && (
                <div className="qa-section">
                  <h2>Test Coverage Breakdown</h2>
                  <div className="qa-test-breakdown">
                    {analysis.test_breakdown.unit_tests && (
                      <div className="qa-test-type-card">
                        <div className="qa-test-type-header">
                          <span className="qa-test-type-icon">🔬</span>
                          <span className="qa-test-type-name">Unit Tests</span>
                        </div>
                        <div className="qa-test-type-stats">
                          <div className="qa-test-count">{analysis.test_breakdown.unit_tests.count}</div>
                          <div className="qa-test-percentage">
                            {analysis.test_breakdown.unit_tests.coverage_percentage}% coverage
                          </div>
                          <div
                            className="qa-test-status"
                            style={{
                              color:
                                analysis.test_breakdown.unit_tests.coverage_percentage >= 70
                                  ? '#16a34a'
                                  : analysis.test_breakdown.unit_tests.coverage_percentage >= 40
                                  ? '#ea580c'
                                  : '#dc2626',
                            }}
                          >
                            {analysis.test_breakdown.unit_tests.status}
                          </div>
                        </div>
                      </div>
                    )}

                    {analysis.test_breakdown.integration_tests && (
                      <div className="qa-test-type-card">
                        <div className="qa-test-type-header">
                          <span className="qa-test-type-icon">🔗</span>
                          <span className="qa-test-type-name">Integration Tests</span>
                        </div>
                        <div className="qa-test-type-stats">
                          <div className="qa-test-count">
                            {analysis.test_breakdown.integration_tests.count}
                          </div>
                          <div className="qa-test-percentage">
                            {analysis.test_breakdown.integration_tests.coverage_percentage}% coverage
                          </div>
                          <div
                            className="qa-test-status"
                            style={{
                              color:
                                analysis.test_breakdown.integration_tests.coverage_percentage >= 70
                                  ? '#16a34a'
                                  : analysis.test_breakdown.integration_tests.coverage_percentage >= 40
                                  ? '#ea580c'
                                  : '#dc2626',
                            }}
                          >
                            {analysis.test_breakdown.integration_tests.status}
                          </div>
                        </div>
                      </div>
                    )}

                    {analysis.test_breakdown.ui_tests && (
                      <div className="qa-test-type-card">
                        <div className="qa-test-type-header">
                          <span className="qa-test-type-icon">🎨</span>
                          <span className="qa-test-type-name">UI Tests</span>
                        </div>
                        <div className="qa-test-type-stats">
                          <div className="qa-test-count">{analysis.test_breakdown.ui_tests.count}</div>
                          <div className="qa-test-percentage">
                            {analysis.test_breakdown.ui_tests.coverage_percentage}% coverage
                          </div>
                          <div
                            className="qa-test-status"
                            style={{
                              color:
                                analysis.test_breakdown.ui_tests.coverage_percentage >= 70
                                  ? '#16a34a'
                                  : analysis.test_breakdown.ui_tests.coverage_percentage >= 40
                                  ? '#ea580c'
                                  : '#dc2626',
                            }}
                          >
                            {analysis.test_breakdown.ui_tests.status}
                          </div>
                        </div>
                      </div>
                    )}

                    {analysis.test_breakdown.e2e_tests && (
                      <div className="qa-test-type-card">
                        <div className="qa-test-type-header">
                          <span className="qa-test-type-icon">🎯</span>
                          <span className="qa-test-type-name">End-to-End Tests</span>
                        </div>
                        <div className="qa-test-type-stats">
                          <div className="qa-test-count">{analysis.test_breakdown.e2e_tests.count}</div>
                          <div className="qa-test-percentage">
                            {analysis.test_breakdown.e2e_tests.coverage_percentage}% coverage
                          </div>
                          <div
                            className="qa-test-status"
                            style={{
                              color:
                                analysis.test_breakdown.e2e_tests.coverage_percentage >= 70
                                  ? '#16a34a'
                                  : analysis.test_breakdown.e2e_tests.coverage_percentage >= 40
                                  ? '#ea580c'
                                  : '#dc2626',
                            }}
                          >
                            {analysis.test_breakdown.e2e_tests.status}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {analysis.risk_areas && analysis.risk_areas.length > 0 && (
                <div className="qa-section">
                  <h2>Risk Areas</h2>
                  <div className="qa-risk-areas">
                    {analysis.risk_areas.map((area, index) => (
                      <div key={index} className="qa-risk-card">
                        <div className="qa-risk-header">
                          <span className="qa-risk-file">{area.file}</span>
                          <span
                            className="qa-risk-level"
                            style={{ color: getRiskColor(area.risk) }}
                          >
                            {area.risk}
                          </span>
                        </div>
                        <p className="qa-risk-reason">{area.reason}</p>
                        {area.concern && (
                          <p className="qa-risk-concern">
                            <strong>Concern:</strong> {area.concern}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {analysis.test_recommendations && analysis.test_recommendations.length > 0 && (
                <div className="qa-section">
                  <h2>Testing Recommendations</h2>
                  <div className="qa-recommendations">
                    {analysis.test_recommendations.map((rec, index) => (
                      <div key={index} className="qa-recommendation-card">
                        <div className="qa-rec-header">
                          <span className="qa-rec-priority">{rec.priority}</span>
                          <span className="qa-rec-area">{rec.area}</span>
                        </div>
                        <p className="qa-rec-text">{rec.recommendation}</p>
                        {rec.test_scenarios && rec.test_scenarios.length > 0 && (
                          <div className="qa-scenarios">
                            <strong>Test Scenarios:</strong>
                            <ul>
                              {rec.test_scenarios.map((scenario, idx) => (
                                <li key={idx}>{scenario}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {analysis.missing_tests && analysis.missing_tests.length > 0 && (
                <div className="qa-section">
                  <h2>Missing Tests</h2>
                  <ul className="qa-missing-tests">
                    {analysis.missing_tests.map((test, index) => (
                      <li key={index}>{test}</li>
                    ))}
                  </ul>
                </div>
              )}

              {analysis.suggested_test_cases && analysis.suggested_test_cases.length > 0 && (
                <div className="qa-section">
                  <h2>Suggested Test Cases</h2>
                  <ul className="qa-test-cases">
                    {analysis.suggested_test_cases.map((testCase, index) => (
                      <li key={index}>{testCase}</li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default QAAnalysis;
