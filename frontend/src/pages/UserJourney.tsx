import { useState, useEffect } from 'react';
import axios from 'axios';
import './UserJourney.css';

interface Scenario {
  given: string | null;
  when: string | null;
  then: string | null;
  status: string | null;
}

interface JourneySection {
  title: string;
  scenarios: Scenario[];
}

interface JourneyData {
  title: string;
  subtitle: string;
  sections: JourneySection[];
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function UserJourney() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<JourneyData | null>(null);
  const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set([0]));

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
                    
                    {scenario.status && scenario.status !== 'null' && scenario.status !== 'nan' && (
                      <div className="scenario-status">
                        <span className="status-badge">{scenario.status}</span>
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
