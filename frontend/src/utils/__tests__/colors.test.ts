import { describe, it, expect } from 'vitest';
import {
  getScoreLevel,
  getScoreColor,
  getScoreLabel,
  getVerdictColor,
} from '../colors';

describe('colors utils', () => {
  describe('getScoreLevel', () => {
    it('returns human for score < 40', () => {
      expect(getScoreLevel(0)).toBe('human');
      expect(getScoreLevel(39)).toBe('human');
    });

    it('returns suspicious for score 40-69', () => {
      expect(getScoreLevel(40)).toBe('suspicious');
      expect(getScoreLevel(69)).toBe('suspicious');
    });

    it('returns ai for score >= 70', () => {
      expect(getScoreLevel(70)).toBe('ai');
      expect(getScoreLevel(100)).toBe('ai');
    });
  });

  describe('getScoreColor', () => {
    it('returns green for human-like scores', () => {
      expect(getScoreColor(20)).toBe('#10b981');
    });

    it('returns orange for suspicious scores', () => {
      expect(getScoreColor(50)).toBe('#f59e0b');
    });

    it('returns red for AI-like scores', () => {
      expect(getScoreColor(80)).toBe('#ef4444');
    });
  });

  describe('getScoreLabel', () => {
    it('returns correct labels', () => {
      expect(getScoreLabel(20)).toBe('Human-like');
      expect(getScoreLabel(50)).toBe('Suspicious');
      expect(getScoreLabel(80)).toBe('AI-likely');
    });
  });

  describe('getVerdictColor', () => {
    it('returns correct colors for verdicts', () => {
      expect(getVerdictColor('HUMAN')).toBe('#10b981');
      expect(getVerdictColor('SUSPICIOUS')).toBe('#f59e0b');
      expect(getVerdictColor('AI_LIKELY')).toBe('#ef4444');
    });

    it('returns gray for unknown verdict', () => {
      expect(getVerdictColor('UNKNOWN')).toBe('#6b7280');
    });
  });
});
