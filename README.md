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

## Test Results

**Status**: Evaluation pending (Phase 4)

Test dataset and evaluation will be completed with:
- 20 essays (10 human, 10 AI-generated)
- Accuracy, Precision, Recall, F1 metrics
- 3 documented failure cases with analysis

Results will be available in `data/results.json` after evaluation.

## Limitations

- **English only**: Non-English essays will produce unreliable results
- **ESL bias**: May flag non-native speakers more frequently
- **Creative writing**: Poetry and fiction may score as "AI" due to unusual patterns
- **Small test set**: 20 essays limits statistical confidence
- **Adversarial prompts**: Can be evaded by sophisticated prompt engineering

## Tech Stack

**Backend**: Python 3.11, FastAPI, spaCy, transformers (GPT-2 small)  
**Frontend**: React 18, TypeScript, Vite  
**Deployment**: Docker + docker-compose

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
