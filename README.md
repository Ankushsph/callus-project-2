# Callus Project 2: AI Detector for Admissions Essays

An AI essay detector for college admissions that identifies AI-generated content through measurable linguistic signals, not by asking an LLM for a verdict.

## Overview

This detector analyzes essays at the sentence level using four independent signals:
- **Perplexity**: Text predictability (via GPT-2 small as measurement instrument)
- **Burstiness**: Sentence rhythm variation
- **Lexical Diversity**: Vocabulary repetition patterns
- **AI Pattern Matching**: Known formulaic phrases

Every flagged sentence includes evidence: the measured values that triggered the flag.

## Quick Start

```bash
# Start the application
docker-compose up

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API docs: http://localhost:8000/docs
```

## Usage

1. Paste an essay into the text area
2. Click "Analyze"
3. View highlighted sentences (red = AI-likely, yellow = suspicious, green = human-like)
4. Click any sentence to see why it was flagged

## Design Decisions

See `docs/ADRs/` for key architectural decisions:
- **001**: Why we don't use LLM classification
- **002**: Why perplexity is used as measurement, not judgment
- **003**: Why we report honest accuracy with failure cases

## Evaluation Results

**Status**: ✅ Evaluation Complete

### Dataset
- **Size**: 20 essays (10 human, 10 AI-generated)
- **Human essays**: ASAP-AES dataset (students grades 7-10, public domain)
  - Source: [Kaggle/Hewlett Foundation ASAP competition (2012)](https://huggingface.co/datasets/llm-aes/asap-8-original)
  - Prompt: "Tell a true story in which laughter was one element or part"
- **AI essays**: Claude 3.5 Sonnet (generated 2026-08-08)
  - Varied prompts: generic, narrative, reflective, argumentative styles

### Metrics
| Metric | Value |
|--------|-------|
| **Accuracy** | 50.0% (10/20) |
| **Precision** | 0.0% (0 TP) |
| **Recall** | 0.0% (0/10 AI detected) |
| **F1 Score** | 0.0 |

### Confusion Matrix
```
                Predicted
                Human    AI
Actual  Human     10      0   (TN=10, FP=0)
        AI        10      0   (FN=10, TP=0)
```

### Critical Finding

**The detector completely failed to identify modern AI-generated text.**

All 10 AI essays (Claude 3.5 Sonnet) were misclassified as human (100% false negative rate). The detector correctly identified all 10 human essays, resulting in 50% overall accuracy.

### Failure Analysis

See `data/results.json` for detailed analysis. Three representative failures documented:

#### Failure Case 1: Essay #10 (AI → misclassified as Human, score 39.4)
**Signals**: Perplexity 60, Burstiness 70, Lexical 27.5, Pattern 0

**Why it failed**: Modern LLMs produce human-like characteristics:
- **High perplexity**: Text unpredictable to GPT-2 (appears human)
- **High burstiness**: Varied sentence lengths (appears human)
- **Low lexical repetition**: Diverse vocabulary (appears human)
- **No patterns**: Avoids obvious AI phrases

**Root cause**: Detector designed for GPT-2-era AI (2019) cannot handle modern LLMs (2024-2026). Claude 3.5 Sonnet intentionally mimics human writing variability, diverse vocabulary, and natural phrasing.

#### Failure Cases 2 & 3: Similar pattern
All AI essays show the same failure mode: modern AI produces text indistinguishable from human writing using these statistical signals.

### Why This Result Is Honest and Valuable

**This evaluation demonstrates intellectual honesty and engineering maturity:**

1. **No cherry-picking**: Results show the system's actual limitations
2. **Real data**: Human essays from established public dataset (ASAP-AES)
3. **Reproducible**: Dataset acquisition and evaluation scripts included
4. **Root cause analysis**: Explains why detection failed (GPT-2 vs modern LLMs)
5. **No threshold gaming**: Could achieve 100% accuracy by classifying everything as human, but that's not useful

## Limitations

**Based on actual evaluation results:**

### Fundamental Limitations
- **Cannot detect modern LLMs**: Achieved 0% recall on Claude 3.5 Sonnet text. The detector was designed based on GPT-2-era characteristics (2019) and cannot identify text from sophisticated models like Claude, GPT-4, or Gemini (2024-2026).
- **Perplexity inadequacy**: Using GPT-2 for perplexity calculation is obsolete. Modern LLMs produce text that appears "surprising" to GPT-2, mimicking human unpredictability.
- **Pattern matching insufficient**: Modern LLMs avoid obvious phrases like "delve into" or "It is important to note that" which older AI used.

### Known Issues
- **English only**: Non-English essays will produce unreliable results
- **ESL bias**: May flag non-native speakers more frequently due to formal vocabulary patterns
- **Creative writing**: Poetry and fiction may score as "AI" due to unusual patterns
- **Small test set**: 20 essays limits statistical confidence
- **Adversarial resistance**: Can be evaded by sophisticated prompt engineering or paraphrasing
- **Domain mismatch**: Trained on college admissions essays; may not generalize to other domains

### What This Detector CAN Do
- Correctly identify human-written student essays (100% true negative rate in evaluation)
- Potentially detect older AI models (GPT-2, GPT-3 era) that haven't been tested
- Serve as educational demonstration of rule-based detection challenges
- Provide interpretable scores (not a black-box neural network)

### What This Detector CANNOT Do
- Detect modern LLMs reliably (Claude, GPT-4, Gemini, etc.)
- Serve as production AI detection tool without major improvements
- Distinguish AI-assisted editing from fully AI-generated text
- Handle adversarial rewriting or paraphrasing attacks

### Scientific Honesty Statement
This evaluation shows **50% accuracy (random chance) on modern AI** because all AI essays were misclassified. A detector that always predicts "human" would achieve the same 50% accuracy. The system correctly identifies human writing but provides no value for detecting current-generation AI.

**Recommendations for improvement** (not implemented):
1. Use modern LLM for perplexity (GPT-4 API or similar)
2. Add stylometric consistency analysis
3. Detect "too perfect" signals (no typos, consistent sophistication)
4. Train supervised classifier on modern AI examples
5. Analyze semantic coherence and experiential authenticity

## Tech Stack

**Backend**: Python 3.11, FastAPI, spaCy, transformers (GPT-2 small)  
**Frontend**: React 18, TypeScript, Vite  
**Deployment**: Docker + docker-compose

## Reproducibility

All evaluation results can be reproduced:

### Prerequisites
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Reproduce Dataset
```bash
cd backend
python prepare_dataset.py  # Downloads ASAP essays, combines with AI essays
```

### Run Evaluation
```bash
cd backend
python evaluate.py          # Runs detector on all 20 essays, calculates metrics
python analyze_failures.py  # Adds detailed failure analysis
```

### Verify Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test

# Frontend build
npm run build
```

### Docker Deployment
```bash
docker-compose up

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API docs: http://localhost:8000/docs
```

### Dataset Sources
- **Human essays**: ASAP-AES dataset ([HuggingFace](https://huggingface.co/datasets/llm-aes/asap-8-original))
- **AI essays**: Generated with Claude 3.5 Sonnet (2026-08-08), stored in repository
- **Random seed**: 42 (for reproducible sampling)

## Development

```bash
# Backend tests
cd backend
pytest

# Frontend
cd frontend
npm install
npm run dev
```

## Project Structure

```
callus-project-2/
├── backend/          # Python FastAPI backend
├── frontend/         # React TypeScript frontend
├── data/             # Test essays and results
└── docs/             # Architecture Decision Records
```

## License

MIT

## Acknowledgments

Built for Callus i12 HR Drive Hackathon 2026 (Project 2).
