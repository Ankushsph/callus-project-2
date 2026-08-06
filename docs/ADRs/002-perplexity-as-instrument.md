# ADR-002: Perplexity as Measurement Instrument

**Date**: 2026-08-06

**Status**: Accepted

## Context

The assignment brief states:

> "Using a language model as an instrument is fine. Running text through a small local model for token probabilities, then doing your own analysis on those numbers, is real work and it's how good detectors are actually built. One line is worth drawing carefully: the model must not make the judgement call while your app relays the verdict."

We need to clarify: using GPT-2 to **measure** perplexity is acceptable, but using it to **classify** is not.

## Decision

**We use GPT-2 small to compute perplexity scores, but the classification logic is our own.**

Perplexity is a statistical measure (average negative log-likelihood of tokens). We:
1. Pass text through GPT-2 small
2. Extract token probabilities
3. Compute perplexity = exp(mean(-log(probabilities)))
4. **We decide** if perplexity value indicates AI text (e.g., < 30 is suspicious)

GPT-2 provides the measurement. Our code makes the judgment.

## Rationale

1. **Assignment allows it**: Explicitly states "using a language model as an instrument is fine"

2. **Well-understood metric**: Perplexity has been used in NLP research for decades. It measures "how surprised the model is" by the text.

3. **Transparent**: Perplexity is a number we can show users. "Perplexity: 18.2 (expected: 40-80)" is actionable evidence.

4. **Local execution**: GPT-2 small (117M parameters) runs locally via `transformers`. No API calls.

5. **Discriminative**: AI text tends to have lower perplexity (more predictable) than human text.

## Consequences

### Positive
- Scientifically grounded signal
- Used by state-of-the-art detectors (GPTZero, DetectGPT)
- Users understand "text is suspiciously predictable"
- No API costs

### Negative
- GPT-2 is older model (2019); newer LLMs may not match its training distribution
- Perplexity alone is insufficient (hence multi-signal approach)
- Requires ~500MB model download

### Mitigation
- Combine with 3 other signals (burstiness, lexical, patterns)
- Use perplexity as one vote, not the only vote
- Document that perplexity measures predictability, not authorship

## Implementation

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def compute_perplexity(text: str) -> float:
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
    return torch.exp(loss).item()
```

Threshold: Perplexity < 30 → contributes to AI-likely score.

## References

- Perplexity definition: https://en.wikipedia.org/wiki/Perplexity
- DetectGPT paper: Uses perplexity perturbations for detection
- GPTZero methodology: Multi-signal including perplexity
