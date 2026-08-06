/**
 * Type definitions matching backend API schemas
 */

export interface SentenceResult {
  text: string;
  start_char: number;
  end_char: number;
  score: number; // 0-100
  signals: {
    perplexity: number;
    burstiness: number;
    lexical: number;
    pattern: number;
  };
  evidence: string[];
}

export interface AnalyzeResponse {
  essay: string;
  overall_score: number; // 0-100
  verdict: 'HUMAN' | 'SUSPICIOUS' | 'AI_LIKELY';
  sentences: SentenceResult[];
  summary: {
    sentence_count: number;
    avg_score: number;
    min_score: number;
    max_score: number;
  };
}

export interface AnalyzeRequest {
  essay: string;
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';
