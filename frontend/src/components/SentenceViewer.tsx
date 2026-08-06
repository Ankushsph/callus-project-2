/**
 * Sentence viewer component - displays essay with color-coded highlighting
 */
import { SentenceResult } from '../types';
import { getScoreBackgroundColor, getScoreColor } from '../utils/colors';

interface SentenceViewerProps {
  sentences: SentenceResult[];
  selectedSentenceIndex: number | null;
  onSentenceClick: (index: number) => void;
}

export function SentenceViewer({
  sentences,
  selectedSentenceIndex,
  onSentenceClick,
}: SentenceViewerProps) {
  if (sentences.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        marginBottom: '1.5rem',
        padding: '1.5rem',
        backgroundColor: 'white',
        border: '1px solid #e5e7eb',
        borderRadius: '0.5rem',
      }}
    >
      <h3
        style={{
          fontSize: '1.125rem',
          fontWeight: '600',
          marginBottom: '1rem',
          color: '#1f2937',
        }}
      >
        Essay Analysis
      </h3>
      <div
        style={{
          lineHeight: '1.8',
          fontSize: '1rem',
        }}
      >
        {sentences.map((sentence, index) => (
          <span
            key={index}
            onClick={() => onSentenceClick(index)}
            style={{
              backgroundColor: getScoreBackgroundColor(sentence.score),
              borderLeft: `3px solid ${getScoreColor(sentence.score)}`,
              paddingLeft: '0.25rem',
              paddingRight: '0.25rem',
              marginRight: '0.25rem',
              cursor: 'pointer',
              display: 'inline',
              transition: 'opacity 0.2s',
              opacity: selectedSentenceIndex === index ? 1 : 0.85,
              fontWeight: selectedSentenceIndex === index ? '500' : 'normal',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.opacity = '1';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.opacity =
                selectedSentenceIndex === index ? '1' : '0.85';
            }}
            title={`Click to see details (Score: ${sentence.score.toFixed(0)})`}
          >
            {sentence.text}
          </span>
        ))}
      </div>
      <div
        style={{
          marginTop: '1rem',
          paddingTop: '1rem',
          borderTop: '1px solid #e5e7eb',
          display: 'flex',
          gap: '1.5rem',
          fontSize: '0.875rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div
            style={{
              width: '1rem',
              height: '1rem',
              backgroundColor: '#d1fae5',
              border: '2px solid #10b981',
              borderRadius: '0.25rem',
            }}
          />
          <span style={{ color: '#6b7280' }}>Human-like (0-39)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div
            style={{
              width: '1rem',
              height: '1rem',
              backgroundColor: '#fef3c7',
              border: '2px solid #f59e0b',
              borderRadius: '0.25rem',
            }}
          />
          <span style={{ color: '#6b7280' }}>Suspicious (40-69)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div
            style={{
              width: '1rem',
              height: '1rem',
              backgroundColor: '#fee2e2',
              border: '2px solid #ef4444',
              borderRadius: '0.25rem',
            }}
          />
          <span style={{ color: '#6b7280' }}>AI-likely (70-100)</span>
        </div>
      </div>
    </div>
  );
}
