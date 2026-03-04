import React, { useState } from 'react';
import { agentApi, BugAnalysisResult, TriageResult } from '../services/agentApi';
import './AIInsights.css';

interface AIInsightsProps {
  bugData: {
    title: string;
    description: string;
    steps: string;
    expected: string;
    actual: string;
    environment: string;
    priority: string;
  };
  onApplyRecommendations?: (recommendations: any) => void;
}

export const AIInsights: React.FC<AIInsightsProps> = ({ bugData, onApplyRecommendations }) => {
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<BugAnalysisResult | null>(null);
  const [triageResult, setTriageResult] = useState<TriageResult | null>(null);
  const [showInsights, setShowInsights] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runAnalysis = async () => {
    if (!bugData.title || !bugData.description) {
      setError('Please fill in at least the title and description');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Run analysis and triage in parallel
      const [analysis, triage] = await Promise.all([
        agentApi.analyzeBug(bugData),
        agentApi.triageBug(bugData),
      ]);

      setAnalysisResult(analysis);
      setTriageResult(triage);
      setShowInsights(true);
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'AI analysis failed');
      console.error('AI analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const parseJSONResponse = (response: string): any => {
    try {
      // Try to extract JSON from markdown code blocks
      const jsonMatch = response.match(/```json\n([\s\S]*?)\n```/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[1]);
      }
      // Try parsing directly
      return JSON.parse(response);
    } catch {
      return null;
    }
  };

  const renderAnalysisInsights = () => {
    if (!analysisResult || !analysisResult.success) return null;

    const parsed = parseJSONResponse(analysisResult.response);

    if (parsed) {
      return (
        <div className="insight-card">
          <h4>Bug Quality Analysis</h4>

          {parsed.quality_score && (
            <div className="quality-score">
              <span className="score-label">Quality Score:</span>
              <span className={`score-value score-${parsed.quality_score.score?.toLowerCase().replace(' ', '-')}`}>
                {parsed.quality_score.score} ({parsed.quality_score.rating}/10)
              </span>
            </div>
          )}

          {parsed.completeness && (
            <div className="analysis-section">
              <h5>Completeness</h5>
              <p><strong>Score:</strong> {parsed.completeness.score}</p>
              {parsed.completeness.suggestions && parsed.completeness.suggestions.length > 0 && (
                <>
                  <strong>Suggestions:</strong>
                  <ul>
                    {parsed.completeness.suggestions.map((s: string, i: number) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          )}

          {parsed.priority_recommendation && (
            <div className="analysis-section">
              <h5>Priority Recommendation</h5>
              <p>
                <strong>Suggested Priority:</strong>{' '}
                <span className={`priority-badge priority-${parsed.priority_recommendation.suggested_priority?.toLowerCase()}`}>
                  {parsed.priority_recommendation.suggested_priority}
                </span>
              </p>
              <p><strong>Reasoning:</strong> {parsed.priority_recommendation.reasoning}</p>
            </div>
          )}

          {parsed.summary && (
            <div className="analysis-section">
              <h5>Summary</h5>
              <p>{parsed.summary}</p>
            </div>
          )}
        </div>
      );
    }

    // Fallback: display raw response
    return (
      <div className="insight-card">
        <h4>Bug Quality Analysis</h4>
        <pre className="raw-response">{analysisResult.response}</pre>
      </div>
    );
  };

  const renderTriageInsights = () => {
    if (!triageResult || !triageResult.success) return null;

    const parsed = parseJSONResponse(triageResult.response);

    if (parsed) {
      return (
        <div className="insight-card">
          <h4>Auto-Triage Recommendations</h4>

          {parsed.triage && (
            <div className="analysis-section">
              <h5>Priority & Urgency</h5>
              <p>
                <strong>Priority:</strong>{' '}
                <span className={`priority-badge priority-${parsed.triage.priority?.toLowerCase()}`}>
                  {parsed.triage.priority}
                </span>
              </p>
              <p><strong>Urgency Score:</strong> {parsed.triage.urgency_score}/10</p>
              <p><strong>Reasoning:</strong> {parsed.triage.priority_reasoning}</p>
            </div>
          )}

          {parsed.assignment && (
            <div className="analysis-section">
              <h5>Squad Assignment</h5>
              <p><strong>Suggested Squad:</strong> {parsed.assignment.suggested_squad}</p>
              <p><strong>Component:</strong> {parsed.assignment.suggested_component}</p>
              <p><strong>Confidence:</strong> {parsed.assignment.confidence}</p>
              <p><strong>Reasoning:</strong> {parsed.assignment.reasoning}</p>
            </div>
          )}

          {parsed.classification && parsed.classification.labels && (
            <div className="analysis-section">
              <h5>Labels</h5>
              <div className="labels-container">
                {parsed.classification.labels.map((label: string, i: number) => (
                  <span key={i} className="label-badge">{label}</span>
                ))}
              </div>
            </div>
          )}

          {parsed.recommendations && parsed.recommendations.immediate_actions && (
            <div className="analysis-section">
              <h5>Immediate Actions</h5>
              <ul>
                {parsed.recommendations.immediate_actions.map((action: string, i: number) => (
                  <li key={i}>{action}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      );
    }

    // Fallback: display raw response
    return (
      <div className="insight-card">
        <h4>Auto-Triage Recommendations</h4>
        <pre className="raw-response">{triageResult.response}</pre>
      </div>
    );
  };

  return (
    <div className="ai-insights-container">
      <div className="ai-insights-header">
        <h3>AI Insights</h3>
        <button
          className="btn-analyze"
          onClick={runAnalysis}
          disabled={loading || !bugData.title || !bugData.description}
        >
          {loading ? 'Analyzing...' : 'Get AI Insights'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {showInsights && (
        <div className="insights-content">
          {renderAnalysisInsights()}
          {renderTriageInsights()}
        </div>
      )}
    </div>
  );
};
