# ADR-001: No LLM-Based Classification

**Date**: 2026-08-06

**Status**: Accepted

## Context

The assignment brief explicitly states: "Not a wrapper: a detector that sends the essay to a chat model and asks for a verdict is unreliable, cannot explain its reasoning, and takes an afternoon to build. We will be able to tell."

We need to build a detector that computes its own verdict using measurable signals, not by delegating the judgment to an LLM.

## Decision

**The system must never ask an LLM "Is this AI-generated?"**

All detection is performed through:
1. Measurable linguistic features (perplexity, burstiness, lexical diversity)
2. Pattern matching against known AI phrases
3. Rule-based scoring with transparent thresholds

## Rationale

1. **Explainability**: Users must understand exactly why each sentence was flagged. "The LLM said so" is not an explanation.

2. **Reproducibility**: Same input must always produce the same output. LLM APIs are non-deterministic.

3. **Transparency**: Educational institutions require auditable decisions. Our scoring logic is in the code, not hidden in a model.

4. **Cost**: No ongoing API fees. System runs entirely locally.

5. **Assignment compliance**: This is the core requirement of the project.

## Consequences

### Positive
- Every score is traceable to specific measurements
- No API dependencies or costs
- Deterministic behavior (essential for fairness)
- Easy to debug and improve

### Negative
- Lower accuracy ceiling than trained classifiers
- Must manually identify discriminative signals
- Can't adapt to new AI models automatically

### Mitigation
- Focus on robust, well-understood signals
- Design for easy addition of new analyzers
- Document limitations honestly

## Implementation

Four independent analyzers:
1. **Perplexity**: Measures text predictability using GPT-2 small (see ADR-002)
2. **Burstiness**: Measures sentence rhythm variation (pure statistics)
3. **Lexical Diversity**: Measures vocabulary repetition (pure statistics)
4. **Pattern Matching**: Detects known AI phrases (regex/string matching)

Each returns a 0-100 score. Final score is the average. Threshold: >70 = AI-likely.

All logic visible in `backend/analyzers.py`.
