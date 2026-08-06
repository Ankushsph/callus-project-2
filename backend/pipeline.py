"""Detection pipeline that orchestrates analysis."""

import spacy
from typing import List, Dict
from schemas import AnalyzeResponse, SentenceResult
from analyzers import PerplexityAnalyzer, BurstinessAnalyzer, LexicalDiversityAnalyzer, PatternAnalyzer


class DetectionPipeline:
    """Orchestrates the detection workflow."""
    
    def __init__(self):
        """Initialize pipeline with NLP model and analyzers."""
        print("Loading spaCy model...")
        self.nlp = spacy.load("en_core_web_sm")
        
        print("Initializing analyzers...")
        self.perplexity_analyzer = PerplexityAnalyzer()
        self.burstiness_analyzer = BurstinessAnalyzer()
        self.lexical_analyzer = LexicalDiversityAnalyzer()
        self.pattern_analyzer = PatternAnalyzer()
        
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
        
        Runs all 4 analyzers and combines scores.
        """
        results = []
        
        # Extract sentence texts for burstiness (needs all sentences)
        sentence_texts = [s["text"] for s in sentences]
        burstiness_score, burstiness_evidence = self.burstiness_analyzer.analyze(sentence_texts)
        
        for sent in sentences:
            text = sent["text"]
            
            # Run analyzers
            perplexity_score, perplexity_evidence = self.perplexity_analyzer.analyze(text)
            lexical_score, lexical_evidence = self.lexical_analyzer.analyze(text)
            pattern_score, pattern_evidence = self.pattern_analyzer.analyze(text)
            
            # Combine scores (simple average)
            signals = {
                "perplexity": perplexity_score,
                "burstiness": burstiness_score,
                "lexical": lexical_score,
                "pattern": pattern_score,
            }
            
            overall_score = sum(signals.values()) / len(signals)
            
            # Collect evidence
            evidence = [
                perplexity_evidence,
                burstiness_evidence,
                lexical_evidence,
                pattern_evidence,
            ]
            
            results.append(SentenceResult(
                text=text,
                start_char=sent["start_char"],
                end_char=sent["end_char"],
                score=overall_score,
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
