import { useState } from 'react';
import type { DuplicateBug } from '@/types/api';
import './DuplicatesList.css';

interface Props {
  duplicates: DuplicateBug[];
}

export default function DuplicatesList({ duplicates }: Props) {
  const [collapsed, setCollapsed] = useState(duplicates.length > 1);

  if (duplicates.length === 0) return null;

  const highestSimilarity = duplicates[0].similarity;
  let severityClass = 'low';
  let heading = 'Possibly Related Bugs';

  if (highestSimilarity >= 80) {
    severityClass = 'high';
    heading = 'Very Similar Bugs Found!';
  } else if (highestSimilarity >= 60) {
    severityClass = 'medium';
    heading = 'Similar Bugs Found';
  }

  return (
    <div className={`duplicates-section ${severityClass}`}>
      <h2 onClick={() => duplicates.length > 1 && setCollapsed(!collapsed)}>
        {heading} ({duplicates.length})
        {duplicates.length > 1 && (
          <span className="toggle-icon">{collapsed ? '▼' : '▲'}</span>
        )}
      </h2>

      {!collapsed && (
        <>
          <p className="duplicates-intro">
            {highestSimilarity >= 80
              ? 'These bugs are very similar to yours. Please review them carefully before creating a new ticket:'
              : 'We found bugs that might be related to yours:'}
          </p>

          <div className="duplicates-list">
            {duplicates.map((dup) => (
              <div key={dup.key} className="duplicate-card">
                <div className="duplicate-header">
                  <a
                    href={dup.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="duplicate-key"
                  >
                    {dup.key}
                  </a>
                  <span className={`similarity-badge ${getSimilarityClass(dup.similarity)}`}>
                    {Math.round(dup.similarity)}% match
                  </span>
                </div>
                <div className="duplicate-summary">{dup.summary}</div>
                <div className="duplicate-meta">
                  <span>Status: {dup.status}</span>
                  <span>Created: {new Date(dup.created).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="duplicates-actions">
            <p>Does your bug look different? You can still create it.</p>
          </div>
        </>
      )}
    </div>
  );
}

function getSimilarityClass(similarity: number): string {
  if (similarity >= 80) return 'high';
  if (similarity >= 60) return 'medium';
  return 'low';
}
