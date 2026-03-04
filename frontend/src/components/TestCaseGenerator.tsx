import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { bugApi } from '@/services/api';
import { agentApi } from '@/services/agentApi';
import './TestCaseGenerator.css';

export default function TestCaseGenerator() {
  const [ticketLink, setTicketLink] = useState('');
  const [enhancementRequest, setEnhancementRequest] = useState('');
  const [showEnhancement, setShowEnhancement] = useState(false);

  const generateMutation = useMutation({
    mutationFn: () => bugApi.generateTestCases({ ticket_link: ticketLink }),
  });

  const enhanceMutation = useMutation({
    mutationFn: () => {
      if (!generateMutation.data?.test_cases) {
        throw new Error('No test cases to enhance');
      }
      return agentApi.enhanceTestCases({
        test_cases: generateMutation.data.test_cases,
        enhancement_request: enhancementRequest,
        ticket_context: {
          ticket_key: generateMutation.data.ticket_key,
          summary: generateMutation.data.summary,
        }
      });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticketLink.trim()) {
      alert('Please enter a JIRA ticket or Google Drive link');
      return;
    }
    setShowEnhancement(false);
    generateMutation.mutate();
  };

  const handleEnhance = () => {
    if (!enhancementRequest.trim()) {
      alert('Please describe what you want to improve');
      return;
    }
    enhanceMutation.mutate();
  };

  const handleCopy = () => {
    const textToCopy = enhanceMutation.isSuccess && enhanceMutation.data?.response
      ? enhanceMutation.data.response
      : generateMutation.data?.test_cases;
    
    if (textToCopy) {
      navigator.clipboard.writeText(textToCopy);
      alert('Copied to clipboard!');
    }
  };

  return (
    <div className="test-case-generator">
      <div className="generator-header">
        <h2>AI-Powered Test Case Generator</h2>
        <p>Generate comprehensive test cases using Claude AI from JIRA tickets or Google Drive documents</p>
      </div>

      <form onSubmit={handleSubmit} className="generator-form">
        <div className="form-group">
          <label htmlFor="ticketLink">JIRA Ticket or Google Drive Link</label>
          <input
            type="text"
            id="ticketLink"
            value={ticketLink}
            onChange={(e) => setTicketLink(e.target.value)}
            placeholder="JIRA: REW-123 or https://... | Google Drive: https://docs.google.com/..."
          />
          <div className="help-text">
            <strong>Accepted formats:</strong><br />
            • JIRA ticket key (e.g., REW-123)<br />
            • JIRA ticket URL (e.g., https://hellofresh.atlassian.net/browse/REW-123)<br />
            • Google Docs link (e.g., https://docs.google.com/document/d/...)<br />
            <em style={{ display: 'block', marginTop: '0.5rem' }}>
              Powered by Claude AI via AWS Bedrock for intelligent test scenario generation
            </em>
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={generateMutation.isPending}
        >
          {generateMutation.isPending ? (
            <>
              <span className="spinner"></span>
              Generating...
            </>
          ) : (
            'Generate AI Test Cases'
          )}
        </button>
      </form>

      {generateMutation.isError && (
        <div className="result-error">
          <h3>Error</h3>
          <p>{(generateMutation.error as any)?.response?.data?.error || 'Failed to generate test cases'}</p>
        </div>
      )}

      {generateMutation.isSuccess && generateMutation.data && (
        <div className="result-success">
          <div className="result-header">
            <h3>AI-Generated Test Cases</h3>
            {generateMutation.data.source_type && (
              <span className="source-badge">
                {generateMutation.data.source_type === 'jira' ? 'JIRA' : 'Google Drive'}
              </span>
            )}
          </div>

          <div className="ticket-info">
            <div className="ticket-key">
              <a
                href={generateMutation.data.ticket_url || generateMutation.data.document_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {generateMutation.data.ticket_key || 'GDOC'}
              </a>
            </div>
            {generateMutation.data.summary && (
              <p><strong>Summary:</strong> {generateMutation.data.summary}</p>
            )}
            {generateMutation.data.status && (
              <div className="ticket-meta">
                <span className="badge">{generateMutation.data.issue_type}</span>
                <span className="badge">{generateMutation.data.status}</span>
                <span className="badge">{generateMutation.data.priority}</span>
              </div>
            )}
          </div>

          <div className="test-cases-content">
            <pre>
              {enhanceMutation.isSuccess && enhanceMutation.data?.response
                ? enhanceMutation.data.response
                : generateMutation.data.test_cases}
            </pre>
          </div>

          <div className="button-group">
            <button type="button" className="btn btn-secondary" onClick={handleCopy}>
              Copy to Clipboard
            </button>
            <button
              type="button"
              className="btn btn-outline"
              onClick={() => setShowEnhancement(!showEnhancement)}
            >
              {showEnhancement ? 'Hide' : 'Enhance with AI'}
            </button>
          </div>

          {showEnhancement && (
            <div className="enhancement-section">
              <h4>Enhance Test Cases with AI</h4>
              <p>Tell Claude AI how you want to improve these test cases:</p>
              <div className="quick-actions">
                <button
                  type="button"
                  className="btn btn-small"
                  onClick={() => setEnhancementRequest('Add more edge cases')}
                >
                  Add Edge Cases
                </button>
                <button
                  type="button"
                  className="btn btn-small"
                  onClick={() => setEnhancementRequest('Add negative test scenarios')}
                >
                  Add Negative Tests
                </button>
                <button
                  type="button"
                  className="btn btn-small"
                  onClick={() => setEnhancementRequest('Make test steps more detailed and specific')}
                >
                  More Detail
                </button>
                <button
                  type="button"
                  className="btn btn-small"
                  onClick={() => setEnhancementRequest('Add platform-specific tests for iOS, Android, and Web')}
                >
                  Platform Tests
                </button>
              </div>
              <textarea
                value={enhancementRequest}
                onChange={(e) => setEnhancementRequest(e.target.value)}
                rows={3}
                placeholder="E.g., 'Add more edge cases for error handling' or 'Include tests for mobile platforms'"
                className="enhancement-input"
              />
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleEnhance}
                disabled={enhanceMutation.isPending}
              >
                {enhanceMutation.isPending ? (
                  <>
                    <span className="spinner"></span>
                    Enhancing...
                  </>
                ) : (
                  'Enhance Test Cases'
                )}
              </button>

              {enhanceMutation.isError && (
                <div className="error-message">
                  Error enhancing test cases: {(enhanceMutation.error as any)?.response?.data?.error || 'Unknown error'}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
