/**
 * Utility functions for score-based color mapping
 */

export type ScoreLevel = 'human' | 'suspicious' | 'ai';

export function getScoreLevel(score: number): ScoreLevel {
  if (score < 40) return 'human';
  if (score < 70) return 'suspicious';
  return 'ai';
}

export function getScoreColor(score: number): string {
  const level = getScoreLevel(score);
  
  switch (level) {
    case 'human':
      return '#10b981'; // green
    case 'suspicious':
      return '#f59e0b'; // yellow/orange
    case 'ai':
      return '#ef4444'; // red
  }
}

export function getScoreBackgroundColor(score: number): string {
  const level = getScoreLevel(score);
  
  switch (level) {
    case 'human':
      return '#d1fae5'; // light green
    case 'suspicious':
      return '#fef3c7'; // light yellow
    case 'ai':
      return '#fee2e2'; // light red
  }
}

export function getScoreLabel(score: number): string {
  const level = getScoreLevel(score);
  
  switch (level) {
    case 'human':
      return 'Human-like';
    case 'suspicious':
      return 'Suspicious';
    case 'ai':
      return 'AI-likely';
  }
}

export function getVerdictColor(verdict: string): string {
  switch (verdict) {
    case 'HUMAN':
      return '#10b981';
    case 'SUSPICIOUS':
      return '#f59e0b';
    case 'AI_LIKELY':
      return '#ef4444';
    default:
      return '#6b7280';
  }
}
