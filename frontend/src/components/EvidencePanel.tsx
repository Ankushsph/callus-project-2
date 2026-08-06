/**
 * Evidence panel component - shows detailed scores and evidence for a sentence
 */
import { SentenceResult } from '../types';
import { getScoreColor, getScoreLabel } from '../utils/colors';

interface EvidencePanelProps {
  sentence: SentenceResult | null;
  onClose: () => void;
}

export function EvidencePanel({ sentence, onClose }: EvidencePanelProps) {
  if (!sentence) {
    return null;
  }

  const { score, signals, evidence, text } = sentence;

  return (
    <div
      style={{
        padding: '1.5rem',
        backgroundColor: 'white',
        border: '1px solid #e5e7eb',
        borderRadius: '0.5rem',
        marginBottom: '1.5rem',
      }}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'start',
          marginBottom: '1rem',
        }}
      >
        <h3
          style={{
            fontSize: '1.125rem',
            fontWeight: '600',
            color: '#1f2937',
          }}
        >
          Sentence Details
        </h3>
        <button
          onClick={onClose}
          style={{
            padding: '0.25rem 0.5rem',
            backgroundColor: 'transparent',
            border: '1px solid #d1d5db',
            borderRadius: '0.25rem',
            cursor: 'pointer',
            fontSize: '0.875rem',
            color: '#6b7280',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = '#f3f4f6';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'transparent';
          }}
        >
          Close
        </button>
      </div>

      {/* Selected sentence */}
      <div
        style={{
          padding: '0.75rem',
          backgroundColor: '#f9fafb',
          borderRadius: '0.375rem',
          marginBottom: '1rem',
          fontSize: '0.95rem',
          fontStyle: 'italic',
          color: '#4b5563',
          borderLeft: `3px solid ${getScoreColor(score)}`,
        }}
      >
        "{text}"
      </div>

      {/* Overall score */}
      <div
        style={{
          marginBottom: '1rem',
          padding: '1rem',
          backgroundColor: '#f9fafb',
          borderRadius: '0.375rem',
        }}
      >
        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.25rem' }}>
          Overall Score
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div
            style={{
              fontSize: '1.5rem',
              fontWeight: '700',
              color: getScoreColor(score),
            }}
          >
            {score.toFixed(0)}
          </div>
          <div style={{ fontSize: '0.875rem', color: '#9ca3af' }}>/100</div>
          <div
            style={{
              marginLeft: '0.5rem',
              padding: '0.25rem 0.5rem',
              backgroundColor: 'white',
              borderRadius: '0.25rem',
              fontSize: '0.875rem',
              fontWeight: '500',
              color: getScoreColor(score),
              border: `1px solid ${getScoreColor(score)}`,
            }}
          >
            {getScoreLabel(score)}
          </div>
        </div>
      </div>

      {/* Individual signals */}
      <div style={{ marginBottom: '1rem' }}>
        <div
          style={{
            fontSize: '0.875rem',
            fontWeight: '600',
            color: '#374151',
            marginBottom: '0.5rem',
          }}
        >
          Detection Signals
        </div>
        <div style={{ display: 'grid', gap: '0.5rem' }}>
          {Object.entries(signals).map(([name, value]) => (
            <SignalBar key={name} name={name} value={value} />
          ))}
        </div>
      </div>

      {/* Evidence */}
      <div>
        <div
          style={{
            fontSize: '0.875rem',
            fontWeight: '600',
            color: '#374151',
            marginBottom: '0.5rem',
          }}
        >
          Evidence
        </div>
        <ul
          style={{
            margin: 0,
            paddingLeft: '1.5rem',
            listStyleType: 'disc',
          }}
        >
          {evidence.map((item, index) => (
            <li
              key={index}
              style={{
                fontSize: '0.875rem',
                color: '#4b5563',
                marginBottom: '0.5rem',
                lineHeight: '1.5',
              }}
            >
              {item}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

function SignalBar({ name, value }: { name: string; value: number }) {
  const displayName = name.charAt(0).toUpperCase() + name.slice(1);
  
  return (
    <div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          marginBottom: '0.25rem',
          fontSize: '0.875rem',
        }}
      >
        <span style={{ color: '#6b7280' }}>{displayName}</span>
        <span style={{ fontWeight: '600', color: '#374151' }}>
          {value.toFixed(0)}
        </span>
      </div>
      <div
        style={{
          width: '100%',
          height: '0.5rem',
          backgroundColor: '#e5e7eb',
          borderRadius: '0.25rem',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${value}%`,
            height: '100%',
            backgroundColor: getScoreColor(value),
            transition: 'width 0.3s ease',
          }}
        />
      </div>
    </div>
  );
}
