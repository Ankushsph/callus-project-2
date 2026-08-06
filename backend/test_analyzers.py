"""Unit tests for individual analyzers."""

import pytest
from analyzers import (
    PerplexityAnalyzer,
    BurstinessAnalyzer,
    LexicalDiversityAnalyzer,
    PatternAnalyzer
)


class TestPerplexityAnalyzer:
    """Tests for perplexity analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return PerplexityAnalyzer()
    
    def test_basic_text(self, analyzer):
        """Test perplexity calculation on simple text."""
        text = "This is a simple sentence for testing."
        score, evidence = analyzer.analyze(text)
        
        assert 0 <= score <= 100
        assert "Perplexity:" in evidence or "unavailable" in evidence
    
    def test_empty_text(self, analyzer):
        """Test handling of empty text."""
        score, evidence = analyzer.analyze("")
        assert 0 <= score <= 100
    
    def test_very_long_text(self, analyzer):
        """Test handling of long text (should truncate)."""
        text = "This is a sentence. " * 200
        score, evidence = analyzer.analyze(text)
        assert 0 <= score <= 100


class TestBurstinessAnalyzer:
    """Tests for burstiness analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return BurstinessAnalyzer()
    
    def test_uniform_sentences(self, analyzer):
        """Uniform sentence lengths should score high (AI-like)."""
        sentences = [
            "This is a test sentence.",
            "This is a test sentence.",
            "This is a test sentence.",
        ]
        score, evidence = analyzer.analyze(sentences)
        
        assert 50 <= score <= 100  # Uniform = AI-like
        assert "variation" in evidence.lower()
    
    def test_varied_sentences(self, analyzer):
        """Varied sentence lengths should score low (human-like)."""
        sentences = [
            "Short.",
            "This is a much longer sentence with many words.",
            "Medium length here.",
            "X",
        ]
        score, evidence = analyzer.analyze(sentences)
        
        assert 0 <= score <= 60  # Varied = human-like
        assert "variation" in evidence.lower() and "CV" in evidence
    
    def test_single_sentence(self, analyzer):
        """Single sentence should return neutral score."""
        sentences = ["One sentence."]
        score, evidence = analyzer.analyze(sentences)
        
        assert score == 50.0
        assert "multiple sentences" in evidence.lower()
    
    def test_empty_sentences(self, analyzer):
        """Empty list should return neutral score."""
        score, evidence = analyzer.analyze([])
        assert score == 50.0


class TestLexicalDiversityAnalyzer:
    """Tests for lexical diversity analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return LexicalDiversityAnalyzer()
    
    def test_repetitive_text(self, analyzer):
        """Repetitive text should score high (AI-like)."""
        text = "the the the the the the the the the the"
        score, evidence = analyzer.analyze(text)
        
        assert 60 <= score <= 100  # Low diversity = AI-like
        assert "TTR" in evidence or "diversity" in evidence.lower()
    
    def test_diverse_text(self, analyzer):
        """Diverse vocabulary should score low (human-like)."""
        text = "Every single word here is completely different and unique from others"
        score, evidence = analyzer.analyze(text)
        
        assert 0 <= score <= 50  # High diversity = human-like
        assert "unique words" in evidence
    
    def test_short_text(self, analyzer):
        """Short text should return neutral score."""
        text = "Too short"
        score, evidence = analyzer.analyze(text)
        
        assert score == 50.0
        assert "too short" in evidence.lower()
    
    def test_empty_text(self, analyzer):
        """Empty text should return neutral score."""
        score, evidence = analyzer.analyze("")
        assert score == 50.0


class TestPatternAnalyzer:
    """Tests for AI pattern matcher."""
    
    @pytest.fixture
    def analyzer(self):
        return PatternAnalyzer()
    
    def test_no_patterns(self, analyzer):
        """Text without AI patterns should score 0."""
        text = "I really love programming and solving problems."
        score, evidence = analyzer.analyze(text)
        
        assert score == 0.0
        assert "No AI patterns" in evidence
    
    def test_with_patterns(self, analyzer):
        """Text with AI patterns should score high."""
        text = "In today's rapidly evolving world, it is important to note that education plays a crucial role."
        score, evidence = analyzer.analyze(text)
        
        assert score > 50
        assert "Found" in evidence
        assert "AI patterns" in evidence
    
    def test_multiple_patterns(self, analyzer):
        """Multiple patterns should increase score."""
        text = "Furthermore, it is essential to note that moreover, we must consider."
        score, evidence = analyzer.analyze(text)
        
        assert score > 30
    
    def test_empty_text(self, analyzer):
        """Empty text should return neutral score."""
        score, evidence = analyzer.analyze("")
        assert score == 50.0
        assert "Empty" in evidence


class TestIntegration:
    """Integration tests for analyzer coordination."""
    
    def test_all_analyzers_return_valid_scores(self):
        """All analyzers should return scores in 0-100 range."""
        text = "This is a test essay. It has multiple sentences. Each sentence is different."
        sentences = text.split(". ")
        
        perp = PerplexityAnalyzer()
        burst = BurstinessAnalyzer()
        lex = LexicalDiversityAnalyzer()
        pat = PatternAnalyzer()
        
        perp_score, perp_ev = perp.analyze(text)
        burst_score, burst_ev = burst.analyze(sentences)
        lex_score, lex_ev = lex.analyze(text)
        pat_score, pat_ev = pat.analyze(text)
        
        for score in [perp_score, burst_score, lex_score, pat_score]:
            assert 0 <= score <= 100
        
        for evidence in [perp_ev, burst_ev, lex_ev, pat_ev]:
            assert isinstance(evidence, str)
            assert len(evidence) > 0
