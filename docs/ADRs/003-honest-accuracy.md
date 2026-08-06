# ADR-003: Honest Accuracy Reporting

**Date**: 2026-08-06

**Status**: Accepted

## Context

The assignment brief requires:

> "Report honest accuracy: results on your own test set, three essays the detector gets confidently wrong, and your explanation of why. That demonstrates you understand your own system; a bare accuracy claim does not."

Many AI detectors claim 95%+ accuracy without showing their test data or failure modes. This is misleading.

## Decision

**We include a dedicated "Accuracy Report" in both documentation and UI that shows:**

1. Test set composition (number of human/AI essays, sources)
2. Confusion matrix (TP, FP, TN, FN)
3. Metrics: Accuracy, Precision, Recall, F1
4. **Three specific essays the detector gets confidently wrong**
5. **Our analysis of why each failure occurred**

## Rationale

1. **Assignment requirement**: Explicitly requested in the brief

2. **Intellectual honesty**: Shows we understand the system's limitations

3. **Builds trust**: Users see we're not hiding failures

4. **Educational value**: Failure analysis teaches more than success rate

5. **Distinguishes submission**: Most hackathon projects hide limitations

## Consequences

### Positive
- Demonstrates understanding of the system
- Shows engineering maturity (acknowledging limitations)
- Helps users understand when to trust/distrust results
- Valuable feedback for future improvements

### Negative
- Lower claimed accuracy than competitors (who hide failures)
- Requires honest test set evaluation (takes time)
- Exposes weaknesses

### Mitigation
- Frame as "scientific rigor" not "admitting defeat"
- Use failures to demonstrate understanding: "This essay was flagged because it uses formal academic vocabulary, but it's actually a non-native speaker trying to sound professional"
- Show we can debug our own system

## Implementation

### Test Set (data/test_essays.json)
```json
{
  "essays": [
    {
      "id": 1,
      "text": "...",
      "label": "human",
      "source": "Reddit r/ApplyingToCollege"
    },
    {
      "id": 2,
      "text": "...",
      "label": "ai",
      "source": "GPT-4, prompt: 'Write a college essay about overcoming challenges'"
    }
  ]
}
```

### Results (data/results.json)
```json
{
  "test_set_size": 20,
  "accuracy": 0.75,
  "precision": 0.80,
  "recall": 0.70,
  "f1": 0.75,
  "confusion_matrix": {
    "true_positives": 7,
    "false_positives": 2,
    "true_negatives": 8,
    "false_negatives": 3
  },
  "failure_cases": [
    {
      "essay_id": 5,
      "predicted": "AI_LIKELY",
      "actual": "human",
      "confidence": 0.85,
      "analysis": "This essay was written by a non-native English speaker who used a thesaurus heavily, resulting in formal vocabulary (high lexical score) and awkward phrasing that appeared AI-like. Limitation: detector doesn't distinguish ESL patterns from AI patterns."
    }
  ]
}
```

### UI Component
Dedicated "Accuracy" tab showing:
- Metrics table
- Three failure cases with side-by-side comparison
- Explanation of each failure
- Disclaimer: "This detector is a tool, not proof. Use as one signal among many."

## References

- Scientific method: Report negative results
- Software engineering: "Make it easy to debug"
- Assignment: "A report that says 'here is my accuracy, here are three essays it gets confidently wrong, and here is my theory about why' is worth far more than a 97% claim we don't believe."
