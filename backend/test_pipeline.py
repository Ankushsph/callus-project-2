"""Integration test for the detection pipeline."""

import pytest
from pipeline import DetectionPipeline


@pytest.fixture
def pipeline():
    """Create pipeline instance."""
    return DetectionPipeline()


def test_pipeline_initialization(pipeline):
    """Test that pipeline initializes successfully."""
    assert pipeline.is_ready()
    assert pipeline.nlp is not None


def test_sentence_segmentation(pipeline):
    """Test sentence segmentation with character offsets."""
    essay = "This is the first sentence. Here is a second one. And a third."
    sentences = pipeline._segment_sentences(essay)
    
    assert len(sentences) == 3
    assert sentences[0]["text"] == "This is the first sentence."
    assert sentences[1]["text"] == "Here is a second one."
    assert sentences[2]["text"] == "And a third."
    
    # Check offsets
    assert sentences[0]["start_char"] == 0
    assert sentences[0]["end_char"] == 27


def test_analyze_simple_essay(pipeline):
    """Test full analysis pipeline."""
    essay = "College is important. Education shapes our future. I want to study computer science."
    
    result = pipeline.analyze(essay)
    
    assert result.essay == essay
    assert result.verdict in ["HUMAN", "SUSPICIOUS", "AI_LIKELY"]
    assert 0 <= result.overall_score <= 100
    assert len(result.sentences) == 3
    
    # Check first sentence structure
    sent = result.sentences[0]
    assert sent.text == "College is important."
    assert 0 <= sent.score <= 100
    assert "perplexity" in sent.signals
    assert "burstiness" in sent.signals
    assert "lexical" in sent.signals
    assert "pattern" in sent.signals
    assert isinstance(sent.evidence, list)


def test_analyze_empty_essay(pipeline):
    """Test error handling for empty input."""
    with pytest.raises(ValueError, match="No sentences found"):
        pipeline.analyze("")


def test_analyze_single_sentence(pipeline):
    """Test analysis with single sentence."""
    essay = "This is a single sentence essay."
    result = pipeline.analyze(essay)
    
    assert len(result.sentences) == 1
    assert result.summary["sentence_count"] == 1


def test_verdict_thresholds(pipeline):
    """Test verdict computation logic."""
    # Create mock sentence results
    from schemas import SentenceResult
    
    # Low scores -> HUMAN
    low_sentences = [SentenceResult(
        text="test",
        start_char=0,
        end_char=4,
        score=30.0,
        signals={},
        evidence=[]
    )]
    score, verdict = pipeline._compute_verdict(low_sentences)
    assert verdict == "HUMAN"
    
    # Mid scores -> SUSPICIOUS
    mid_sentences = [SentenceResult(
        text="test",
        start_char=0,
        end_char=4,
        score=55.0,
        signals={},
        evidence=[]
    )]
    score, verdict = pipeline._compute_verdict(mid_sentences)
    assert verdict == "SUSPICIOUS"
    
    # High scores -> AI_LIKELY
    high_sentences = [SentenceResult(
        text="test",
        start_char=0,
        end_char=4,
        score=85.0,
        signals={},
        evidence=[]
    )]
    score, verdict = pipeline._compute_verdict(high_sentences)
    assert verdict == "AI_LIKELY"
