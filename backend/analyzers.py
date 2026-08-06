"""Four independent analyzers for AI detection signals."""

import json
import re
from pathlib import Path
from typing import List, Tuple
import numpy as np


class PerplexityAnalyzer:
    """
    Measures text predictability using GPT-2 small.
    
    Lower perplexity = more predictable = more AI-like.
    """
    
    def __init__(self):
        """Initialize GPT-2 model (lazy loading)."""
        self._model = None
        self._tokenizer = None
    
    def _load_model(self):
        """Load model on first use."""
        if self._model is None:
            try:
                from transformers import GPT2LMHeadModel, GPT2Tokenizer
                import torch
                
                print("Loading GPT-2 model for perplexity calculation...")
                self._model = GPT2LMHeadModel.from_pretrained("gpt2")
                self._tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
                self._model.eval()  # Set to evaluation mode
                print("GPT-2 model loaded.")
            except Exception as e:
                print(f"Warning: Could not load GPT-2 model: {e}")
                self._model = "failed"
                self._tokenizer = "failed"
    
    def analyze(self, text: str) -> Tuple[float, str]:
        """
        Compute perplexity score for text.
        
        Returns:
            (score, evidence) where score is 0-100 (higher = more AI-like)
        """
        self._load_model()
        
        # If model failed to load, return neutral score
        if self._model == "failed":
            return 50.0, "Perplexity analysis unavailable (model not loaded)"
        
        try:
            import torch
            
            # Tokenize
            inputs = self._tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            # Compute loss (negative log-likelihood)
            with torch.no_grad():
                outputs = self._model(**inputs, labels=inputs["input_ids"])
                loss = outputs.loss
            
            # Perplexity = exp(loss)
            perplexity = torch.exp(loss).item()
            
            # Convert to 0-100 score
            # Typical ranges: Human ~50-150, AI ~20-60
            # Lower perplexity → higher score (more AI-like)
            if perplexity < 20:
                score = 100.0
            elif perplexity < 40:
                score = 80.0
            elif perplexity < 60:
                score = 60.0
            elif perplexity < 100:
                score = 40.0
            else:
                score = 20.0
            
            evidence = f"Perplexity: {perplexity:.1f} (expected human range: 50-150)"
            return score, evidence
            
        except Exception as e:
            return 50.0, f"Perplexity calculation failed: {str(e)}"


class BurstinessAnalyzer:
    """
    Measures sentence rhythm variation.
    
    Human writing has variable sentence lengths (bursty).
    AI writing tends to be more uniform.
    """
    
    def analyze(self, sentences: List[str]) -> Tuple[float, str]:
        """
        Compute burstiness score across all sentences.
        
        Args:
            sentences: List of sentence texts
        
        Returns:
            (score, evidence) where score is 0-100 (higher = more AI-like)
        """
        if len(sentences) < 2:
            return 50.0, "Need multiple sentences to compute burstiness"
        
        # Compute sentence lengths (in words)
        lengths = [len(s.split()) for s in sentences]
        
        # Burstiness = coefficient of variation (std / mean)
        mean_length = np.mean(lengths)
        std_length = np.std(lengths)
        
        if mean_length == 0:
            return 50.0, "Cannot compute burstiness (zero mean length)"
        
        cv = std_length / mean_length
        
        # Typical ranges: Human CV ~0.4-0.8, AI CV ~0.2-0.4
        # Lower CV (uniform) → higher score (more AI-like)
        if cv < 0.2:
            score = 90.0
        elif cv < 0.4:
            score = 70.0
        elif cv < 0.6:
            score = 50.0
        elif cv < 0.8:
            score = 30.0
        else:
            score = 10.0
        
        evidence = f"Sentence length variation (CV): {cv:.2f} (expected human: 0.4-0.8, AI: 0.2-0.4)"
        return score, evidence


class LexicalDiversityAnalyzer:
    """
    Measures vocabulary repetition.
    
    Type-Token Ratio (TTR) = unique words / total words.
    AI tends to repeat safe vocabulary more.
    """
    
    def analyze(self, text: str) -> Tuple[float, str]:
        """
        Compute lexical diversity score.
        
        Returns:
            (score, evidence) where score is 0-100 (higher = more AI-like)
        """
        # Tokenize (simple whitespace split, lowercase)
        words = text.lower().split()
        
        if len(words) < 10:
            return 50.0, "Text too short for lexical analysis"
        
        # Count unique words
        unique_words = set(words)
        ttr = len(unique_words) / len(words)
        
        # Typical ranges: Human TTR ~0.5-0.7, AI TTR ~0.6-0.8
        # Higher TTR can indicate AI trying to be "sophisticated"
        # Lower TTR can indicate AI repeating safe words
        # We focus on LOW TTR (repetitive) as AI signal
        if ttr < 0.4:
            score = 80.0
        elif ttr < 0.5:
            score = 60.0
        elif ttr < 0.6:
            score = 40.0
        elif ttr < 0.75:
            score = 30.0
        else:
            score = 20.0
        
        evidence = f"Lexical diversity (TTR): {ttr:.2f}, {len(unique_words)} unique words in {len(words)} total (expected: 0.5-0.7)"
        return score, evidence


class PatternAnalyzer:
    """
    Detects known AI formulaic phrases.
    
    Matches against curated list of common AI patterns.
    """
    
    def __init__(self):
        """Load AI patterns from JSON file."""
        self.patterns = {}
        try:
            pattern_file = Path(__file__).parent.parent / "data" / "ai_patterns.json"
            with open(pattern_file, 'r') as f:
                self.patterns = json.load(f)
            print(f"Loaded {sum(len(v) for v in self.patterns.values())} AI patterns")
        except Exception as e:
            print(f"Warning: Could not load AI patterns: {e}")
    
    def analyze(self, text: str) -> Tuple[float, str]:
        """
        Detect AI patterns in text.
        
        Returns:
            (score, evidence) where score is 0-100 (higher = more AI-like)
        """
        if not self.patterns:
            return 50.0, "AI patterns not loaded"
        
        text_lower = text.lower()
        matches = []
        
        # Check each pattern category
        for category, phrases in self.patterns.items():
            for phrase in phrases:
                if phrase.lower() in text_lower:
                    matches.append((category, phrase))
        
        # Compute density: matches per 100 words
        word_count = len(text.split())
        if word_count == 0:
            return 50.0, "Empty text"
        
        density = (len(matches) / word_count) * 100
        
        # Score based on density
        # 0 matches → 0 score (not AI-like)
        # 1+ match per 100 words → high score
        if density == 0:
            score = 0.0
        elif density < 1:
            score = 30.0
        elif density < 2:
            score = 60.0
        elif density < 3:
            score = 80.0
        else:
            score = 95.0
        
        if matches:
            match_list = ", ".join(f'"{m[1]}"' for m in matches[:3])
            if len(matches) > 3:
                match_list += f" (+{len(matches)-3} more)"
            evidence = f"Found {len(matches)} AI patterns: {match_list} (density: {density:.1f} per 100 words)"
        else:
            evidence = "No AI patterns detected"
        
        return score, evidence
