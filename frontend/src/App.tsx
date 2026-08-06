/**
 * Main App component - orchestrates the entire application
 */

import { useState } from 'react';
import { EssayInput } from './components/EssayInput';
import { AnalyzeButton } from './components/AnalyzeButton';
import { ResultsSummary } from './components/ResultsSummary';
import { SentenceViewer } from './components/SentenceViewer';
import { EvidencePanel } from './components/EvidencePanel';
import { analyzeEssay, ApiError } from './services/api';
import { AnalyzeResponse, LoadingState } from './types';

function App() {
  const [essay, setEssay] = useState('');
  const [loadingState, setLoadingState] = useState<LoadingState>('idle');
  const [results, setResults] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedSentenceIndex, setSelectedSentenceIndex] = useState<number | null>(null);

  const handleAnalyze = async () => {
    if (!essay.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoadingState('loading');
    setError(null);
    setResults(null);
    setSelectedSentenceIndex(null);

    try {
      const response = await analyzeEssay(essay);
      setResults(response);
      setLoadingState('success');
    } catch (err) {
      setLoadingState('error');
      
      if (err instanceof ApiError) {
        setError(`Analysis failed: ${err.message}`);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    }
  };

  const handleSentenceClick = (index: number) => {
    setSelectedSentenceIndex(index === selectedSentenceIndex ? null : index);
  };

  const selectedSentence = 
    selectedSentenceIndex !== null && results
      ? results.sentences[selectedSentenceIndex]
      : null;

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#f3f4f6',
        padding: '2rem 1rem',
      }}
    >
      <div
        style={{
          maxWidth: '900px',
          margin: '0 auto',
        }}
      >
        {/* Header */}
        <header style={{ marginBottom: '2rem', textAlign: 'center' }}>
          <h1
            style={{
              fontSize: '2.25rem',
              fontWeight: '700',
              color: '#1f2937',
              marginBottom: '0.5rem',
            }}
          >
            AI Essay Detector
          </h1>
          <p
            style={{
              fontSize: '1rem',
              color: '#6b7280',
            }}
          >
            Analyze essays for AI-generated content using measurable linguistic signals
          </p>
        </header>

        {/* Input Section */}
        <div
          style={{
            padding: '1.5rem',
            backgroundColor: 'white',
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)',
            marginBottom: '1.5rem',
          }}
        >
          <EssayInput
            value={essay}
            onChange={setEssay}
            disabled={loadingState === 'loading'}
          />
          <AnalyzeButton
            onClick={handleAnalyze}
            disabled={!essay.trim() || loadingState === 'loading'}
            loading={loadingState === 'loading'}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div
            style={{
              padding: '1rem',
              backgroundColor: '#fee2e2',
              border: '1px solid #ef4444',
              borderRadius: '0.375rem',
              marginBottom: '1.5rem',
              color: '#991b1b',
              fontSize: '0.95rem',
            }}
          >
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Results */}
        {results && (
          <>
            <ResultsSummary results={results} />
            
            {selectedSentence && (
              <EvidencePanel
                sentence={selectedSentence}
                onClose={() => setSelectedSentenceIndex(null)}
              />
            )}
            
            <SentenceViewer
              sentences={results.sentences}
              selectedSentenceIndex={selectedSentenceIndex}
              onSentenceClick={handleSentenceClick}
            />
          </>
        )}

        {/* Empty State */}
        {loadingState === 'idle' && !results && (
          <div
            style={{
              padding: '3rem 1.5rem',
              backgroundColor: 'white',
              borderRadius: '0.5rem',
              textAlign: 'center',
              color: '#9ca3af',
            }}
          >
            <p style={{ fontSize: '1.125rem', marginBottom: '0.5rem' }}>
              Paste an essay above and click "Analyze Essay" to get started
            </p>
            <p style={{ fontSize: '0.875rem' }}>
              The detector will highlight sentences and explain why they were flagged
            </p>
          </div>
        )}

        {/* Footer */}
        <footer
          style={{
            marginTop: '3rem',
            paddingTop: '1.5rem',
            borderTop: '1px solid #e5e7eb',
            textAlign: 'center',
            color: '#9ca3af',
            fontSize: '0.875rem',
          }}
        >
          <p>
            Callus Project 2 - Built with measurable linguistic signals, not LLM judgments
          </p>
          <p style={{ marginTop: '0.5rem' }}>
            Uses: Perplexity • Burstiness • Lexical Diversity • Pattern Matching
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
