import { useState, useEffect } from 'react';
import axios from 'axios';
import './UserJourney.css';

interface PlatformStatus {
  web: string;
  ios: string;
  android: string;
}

interface Scenario {
  id: string;
  given: string | null;
  when: string | null;
  then: string | null;
  platforms: PlatformStatus;
  jira_link: string | null;
  test_status: string;
}

interface JourneySection {
  title: string;
  scenarios: Scenario[];
}

interface Statistics {
  total: number;
  not_started: number;
  in_progress: number;
  passed: number;
  failed: number;
  blocked: number;
}

interface JourneyData {
  title: string;
  subtitle: string;
  sections: JourneySection[];
  statistics: Statistics;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function UserJourney() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<JourneyData | null>(null);
  const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set([0]));
  const [testStatuses, setTestStatuses] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    loadJourneyData();
  }, []);

  const loadJourneyData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/user-journey`);
      
      if (response.data.success) {
        setData(response.data.data);
      } else {
        setError(response.data.error || 'Failed to load user journey data');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'Failed to load user journey data');
    } finally {
      setLoading(false);
    }
  };

  const toggleSection = (index: number) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSections(newExpanded);
  };

  const expandAll = () => {
    if (data) {
      setExpandedSections(new Set(data.sections.map((_, i) => i)));
    }
  };

  const collapseAll = () => {
    setExpandedSections(new Set());
  };

  const updateTestStatus = (testId: string, status: string) => {
    setTestStatuses((prev) => ({
      ...prev,
      [testId]: status,
    }));
  };

  const getPlatformStatusClass = (status: string): string => {
    const lowerStatus = status.toLowerCase();
    if (lowerStatus.includes('pass')) return 'platform-pass';
    if (lowerStatus.includes('fail')) return 'platform-fail';
    if (lowerStatus.includes('block')) return 'platform-blocked';
    if (lowerStatus.includes('progress') || lowerStatus.includes('testing')) return 'platform-progress';
    return 'platform-not-tested';
  };

  const getTestStatusClass = (status: string): string => {
    const lowerStatus = status.toLowerCase();
    if (lowerStatus.includes('pass')) return 'status-passed';
    if (lowerStatus.includes('fail')) return 'status-failed';
    if (lowerStatus.includes('block')) return 'status-blocked';
    if (lowerStatus.includes('progress')) return 'status-in-progress';
    return 'status-not-started';
  };

  const calculateStatistics = (): Statistics => {
    if (!data) return { total: 0, not_started: 0, in_progress: 0, passed: 0, failed: 0, blocked: 0 };
    
    const stats = { total: 0, not_started: 0, in_progress: 0, passed: 0, failed: 0, blocked: 0 };
    
    data.sections.forEach((section) => {
      section.scenarios.forEach((scenario) => {
        stats.total++;
        const status = (testStatuses[scenario.id] || scenario.test_status).toLowerCase();
        
        if (status.includes('pass')) stats.passed++;
        else if (status.includes('fail')) stats.failed++;
        else if (status.includes('block')) stats.blocked++;
        else if (status.includes('progress')) stats.in_progress++;
        else stats.not_started++;
      });
    });
    
    return stats;
  };

  const statistics = calculateStatistics();

  if (loading) {
    return (
      <div className="user-journey-container">
        <div className="user-journey-loading">
          <div className="loading-spinner"></div>
          <p>Loading user journey data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="user-journey-container">
        <div className="user-journey-error">
          <strong>Error:</strong> {error}
        </div>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <div className="user-journey-container">
      <div className="user-journey-header">
        <h1>{data.title}</h1>
        <p className="user-journey-subtitle">{data.subtitle}</p>
        
        <div className="user-journey-controls">
          <button onClick={expandAll} className="control-button">
            Expand All
          </button>
          <button onClick={collapseAll} className="control-button">
            Collapse All
          </button>
        </div>
      </div>

      {/* Statistics Dashboard */}
      <div className="statistics-dashboard">
        <div className="stat-card stat-total">
          <div className="stat-number">{statistics.total}</div>
          <div className="stat-label">Total Test Cases</div>
        </div>
        <div className="stat-card stat-passed">
          <div className="stat-number">{statistics.passed}</div>
          <div className="stat-label">Passed</div>
          <div className="stat-percentage">
            {statistics.total > 0 ? Math.round((statistics.passed / statistics.total) * 100) : 0}%
          </div>
        </div>
        <div className="stat-card stat-failed">
          <div className="stat-number">{statistics.failed}</div>
          <div className="stat-label">Failed</div>
          <div className="stat-percentage">
            {statistics.total > 0 ? Math.round((statistics.failed / statistics.total) * 100) : 0}%
          </div>
        </div>
        <div className="stat-card stat-in-progress">
          <div className="stat-number">{statistics.in_progress}</div>
          <div className="stat-label">In Progress</div>
          <div className="stat-percentage">
            {statistics.total > 0 ? Math.round((statistics.in_progress / statistics.total) * 100) : 0}%
          </div>
        </div>
        <div className="stat-card stat-blocked">
          <div className="stat-number">{statistics.blocked}</div>
          <div className="stat-label">Blocked</div>
          <div className="stat-percentage">
            {statistics.total > 0 ? Math.round((statistics.blocked / statistics.total) * 100) : 0}%
          </div>
        </div>
        <div className="stat-card stat-not-started">
          <div className="stat-number">{statistics.not_started}</div>
          <div className="stat-label">Not Started</div>
          <div className="stat-percentage">
            {statistics.total > 0 ? Math.round((statistics.not_started / statistics.total) * 100) : 0}%
          </div>
        </div>
      </div>

      <div className="user-journey-sections">
        {data.sections.map((section, sectionIndex) => (
          <div key={sectionIndex} className="journey-section">
            <div
              className="journey-section-header"
              onClick={() => toggleSection(sectionIndex)}
            >
              <span className="section-number">{sectionIndex + 1}</span>
              <h2 className="section-title">{section.title}</h2>
              <span className="section-toggle">
                {expandedSections.has(sectionIndex) ? '▼' : '▶'}
              </span>
              <span className="section-count">
                {section.scenarios.length} test {section.scenarios.length === 1 ? 'case' : 'cases'}
              </span>
            </div>

            {expandedSections.has(sectionIndex) && (
              <div className="journey-scenarios">
                {section.scenarios.map((scenario, scenarioIndex) => (
                  <div key={scenarioIndex} className="scenario-card">
                    <div className="scenario-header-row">
                      <span className="test-case-id">{scenario.id}</span>
                      
                      {/* Platform Status Badges */}
                      <div className="platform-badges">
                        <span className={`platform-badge ${getPlatformStatusClass(scenario.platforms.web)}`}>
                          WEB: {scenario.platforms.web}
                        </span>
                        <span className={`platform-badge ${getPlatformStatusClass(scenario.platforms.ios)}`}>
                          iOS: {scenario.platforms.ios}
                        </span>
                        <span className={`platform-badge ${getPlatformStatusClass(scenario.platforms.android)}`}>
                          Android: {scenario.platforms.android}
                        </span>
                      </div>

                      {/* Test Status Dropdown */}
                      <select
                        className={`test-status-select ${getTestStatusClass(testStatuses[scenario.id] || scenario.test_status)}`}
                        value={testStatuses[scenario.id] || scenario.test_status}
                        onChange={(e) => updateTestStatus(scenario.id, e.target.value)}
                      >
                        <option value="Not Started">Not Started</option>
                        <option value="In Progress">In Progress</option>
                        <option value="Passed">Passed</option>
                        <option value="Failed">Failed</option>
                        <option value="Blocked">Blocked</option>
                      </select>
                    </div>

                    {scenario.given && (
                      <div className="scenario-block given-block">
                        <span className="scenario-label">GIVEN</span>
                        <p className="scenario-text">{scenario.given}</p>
                      </div>
                    )}
                    
                    {scenario.when && (
                      <div className="scenario-block when-block">
                        <span className="scenario-label">WHEN</span>
                        <p className="scenario-text">{scenario.when}</p>
                      </div>
                    )}
                    
                    {scenario.then && (
                      <div className="scenario-block then-block">
                        <span className="scenario-label">THEN</span>
                        <p className="scenario-text">{scenario.then}</p>
                      </div>
                    )}

                    {scenario.jira_link && scenario.jira_link !== 'null' && scenario.jira_link !== 'nan' && (
                      <div className="scenario-jira-link">
                        <a href={scenario.jira_link} target="_blank" rel="noopener noreferrer">
                          View Defect in JIRA
                        </a>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default UserJourney;
