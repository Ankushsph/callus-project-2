/**
 * Results summary component - shows overall verdict and summary stats
 */
import { AnalyzeResponse } from '../types';
import { getVerdictColor } from '../utils/colors';

interface ResultsSummaryProps {
  results: AnalyzeResponse;
}

export function ResultsSummary({ results }: ResultsSummaryProps) {
  const { overall_score, verdict, summary } = results;

  const verdictDisplay = verdict.replace('_', ' ');

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
      <h2
        style={{
          fontSize: '1.25rem',
          fontWeight: '600',
          marginBottom: '1rem',
          color: '#1f2937',
        }}
      >
        Overall Verdict
      </h2>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          marginBottom: '1.5rem',
        }}
      >
        <div
          style={{
            fontSize: '3rem',
            fontWeight: '700',
            color: getVerdictColor(verdict),
          }}
        >
          {overall_score.toFixed(0)}
        </div>
        <div>
          <div
            style={{
              fontSize: '1.5rem',
              fontWeight: '600',
              color: getVerdictColor(verdict),
            }}
          >
            {verdictDisplay}
          </div>
          <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            AI Likelihood Score
          </div>
        </div>
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '1rem',
          paddingTop: '1rem',
          borderTop: '1px solid #e5e7eb',
        }}
      >
        <StatItem
          label="Sentences"
          value={summary.sentence_count.toString()}
        />
        <StatItem
          label="Average Score"
          value={summary.avg_score.toFixed(0)}
        />
        <StatItem
          label="Min Score"
          value={summary.min_score.toFixed(0)}
        />
        <StatItem
          label="Max Score"
          value={summary.max_score.toFixed(0)}
        />
      </div>
    </div>
  );
}

function StatItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div
        style={{
          fontSize: '0.75rem',
          color: '#9ca3af',
          marginBottom: '0.25rem',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          fontWeight: '600',
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: '1.5rem',
          fontWeight: '600',
          color: '#1f2937',
        }}
      >
        {value}
      </div>
    </div>
  );
}
