"""Detection pipeline that orchestrates analysis."""

import spacy
from typing import List, Dict
from schemas import AnalyzeResponse, SentenceResult


class DetectionPipeline:
    """Orchestrates the detection workflow."""
    
    def __init__(self):
        """Initialize pipeline with NLP model."""
        print("Loading spaCy model...")
        self.nlp = spacy.load("en_core_web_sm")
        print("Pipeline ready.")
    
    def is_ready(self) -> bool:
        """Check if pipeline is ready."""
        return self.nlp is not None
    
    def _segment_sentences(self, text: str) -> List[Dict]:
        """
        Segment text into sentences, preserving character offsets.
        
        Returns list of dicts with: text, start_char, end_char
        """
        doc = self.nlp(text)
        sentences = []
        
        for sent in doc.sents:
            sentences.append({
                "text": sent.text.strip(),
                "start_char": sent.start_char,
                "end_char": sent.end_char,
            })
        
        return sentences
    
    def _compute_scores(self, sentences: List[Dict]) -> List[SentenceResult]:
        """
        Compute AI likelihood scores for each sentence.
        
        Currently returns placeholder scores. Will be implemented in Phase 2.
        """
        results = []
        
        for sent in sentences:
            # Placeholder: all sentences scored as 50 (neutral)
            score = 50.0
            signals = {
                "perplexity": 50.0,
                "burstiness": 50.0,
                "lexical": 50.0,
                "pattern": 50.0,
            }
            evidence = ["Analysis not yet implemented"]
            
            results.append(SentenceResult(
                text=sent["text"],
                start_char=sent["start_char"],
                end_char=sent["end_char"],
                score=score,
                signals=signals,
                evidence=evidence
            ))
        
        return results
    
    def _compute_verdict(self, sentences: List[SentenceResult]) -> tuple[float, str]:
        """
        Compute overall essay score and verdict.
        
        Returns (overall_score, verdict_string)
        """
        if not sentences:
            return 0.0, "UNKNOWN"
        
        # Average sentence scores
        overall_score = sum(s.score for s in sentences) / len(sentences)
        
        # Thresholds
        if overall_score < 40:
            verdict = "HUMAN"
        elif overall_score < 70:
            verdict = "SUSPICIOUS"
        else:
            verdict = "AI_LIKELY"
        
        return overall_score, verdict
    
    def analyze(self, essay: str) -> AnalyzeResponse:
        """
        Main analysis pipeline.
        
        1. Segment into sentences
        2. Compute scores per sentence
        3. Aggregate to essay-level verdict
        """
        # Segment
        sentences = self._segment_sentences(essay)
        
        if not sentences:
            raise ValueError("No sentences found in essay")
        
        # Score each sentence
        sentence_results = self._compute_scores(sentences)
        
        # Aggregate
        overall_score, verdict = self._compute_verdict(sentence_results)
        
        # Summary statistics
        summary = {
            "sentence_count": len(sentence_results),
            "avg_score": overall_score,
            "min_score": min(s.score for s in sentence_results),
            "max_score": max(s.score for s in sentence_results),
        }
        
        return AnalyzeResponse(
            essay=essay,
            overall_score=overall_score,
            verdict=verdict,
            sentences=sentence_results,
            summary=summary
        )
