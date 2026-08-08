# Evaluation Dataset

This directory contains the test dataset and evaluation results for the AI essay detector.

## Files

### `test_essays.json`
Complete test dataset with 20 essays (10 human, 10 AI-generated).

**Structure:**
- `description`: Dataset description
- `dataset_status`: "COMPLETE"
- `methodology`: Detailed sourcing information
- `reproducibility`: Random seed and script references
- `essays`: Array of 20 essay objects

**Essay object fields:**
- `id`: Integer 1-20
- `text`: Full essay text
- `label`: "human" or "ai"
- `source`: Attribution/provenance
- `notes`: Additional context (optional)
- `generation_prompt`: For AI essays (optional)
- `dataset_info`: For human essays (optional)

### `results.json`
Complete evaluation results including metrics, confusion matrix, failure analysis, and all predictions.

**Structure:**
- `description`: Results description
- `evaluated`: Timestamp
- `test_set_size`: 20
- `metrics`: accuracy, precision, recall, f1
- `confusion_matrix`: TP, TN, FP, FN
- `failure_cases`: Top 3 high-confidence errors with detailed analysis
- `all_predictions`: Complete prediction data for all 20 essays

### `ai_patterns.json`
Database of known AI phrases used by the pattern matching analyzer.

**Structure:**
- Array of pattern objects with:
  - `pattern`: Regex or substring to match
  - `score_contribution`: How much this pattern increases AI likelihood
  - `description`: Why this pattern is AI-like

## Dataset Sources

### Human Essays (IDs 11-20)
**Source**: ASAP-AES (Automated Student Assessment Prize - Automated Essay Scoring)  
**Dataset URL**: https://huggingface.co/datasets/llm-aes/asap-8-original  
**Original Competition**: Kaggle / Hewlett Foundation (2012)  
**License**: Public domain  
**Authors**: Students grades 7-10  
**Prompt**: "Tell a true story in which laughter was one element or part"  
**Sampling**: Random with seed 42 for reproducibility  
**Essay Set**: ASAP set 8 (laughter prompt)  
**Original Corpus**: 723 student essays  
**Selection**: 10 essays with varied scores and lengths

**Provenance**: These essays were written by real students for a standardized writing assessment. They were publicly released as part of an automated essay scoring competition and are widely used in NLP research.

### AI Essays (IDs 1-10)
**Source**: Claude 3.5 Sonnet (Anthropic)  
**Generation Date**: 2026-08-08  
**Generator**: Kiro AI assistant  
**Prompts**: Varied college admissions essay prompts  
**Styles**: Generic, narrative, reflective, argumentative  

**Generation methodology**:
1. Brief, generic admissions essay
2. Robotics/challenges narrative
3. Values/community service emphasis
4. Conclusion paragraph
5. Environmental science achievement
6. Cultural identity reflection
7. Mathematics passion
8. Student government leadership
9. Medicine/technology interest
10. Art + computer science integration

**Intentional variation**: Essays span different topics, lengths, and structures to test detector across AI writing styles.

## Evaluation Methodology

### Dataset Preparation
```bash
cd backend
python prepare_dataset.py
```

This script:
1. Loads existing 10 AI essays from repository
2. Attempts to download ASAP dataset from HuggingFace
3. Falls back to manually curated ASAP essays if download unavailable
4. Randomly samples 10 diverse human essays (seed=42)
5. Combines into final test_essays.json with full metadata

### Evaluation Execution
```bash
cd backend
python evaluate.py
```

This script:
1. Validates dataset (requires exactly 10 human + 10 AI)
2. Initializes detection pipeline
3. Runs detector on all 20 essays
4. Computes confusion matrix and metrics
5. Identifies top 3 high-confidence failures
6. Saves results to results.json

### Failure Analysis
```bash
cd backend
python analyze_failures.py
```

This script:
1. Loads evaluation results
2. Analyzes each failure case
3. Explains why each misclassification occurred
4. Documents root causes and possible improvements
5. Updates results.json with detailed analysis

## Evaluation Results Summary

**Accuracy**: 50.0% (10/20 correct)  
**Precision**: 0.0% (no true positives)  
**Recall**: 0.0% (missed all 10 AI essays)  
**F1**: 0.0

**Confusion Matrix**:
```
                Predicted
                Human    AI
Actual  Human     10      0
        AI        10      0
```

**Critical Finding**: All 10 AI essays were misclassified as human (100% false negative rate).

**Root Cause**: Detector was designed based on GPT-2-era AI characteristics (2019) and cannot identify text from modern LLMs like Claude 3.5 Sonnet (2024-2026). Modern AI produces:
- Human-like perplexity (unpredictable to GPT-2)
- Natural sentence variation (high burstiness)
- Diverse vocabulary (low lexical repetition)
- No obvious AI phrases

See `results.json` for complete analysis.

## Data Integrity

### What This Dataset IS
- ✅ 10 genuine human essays from established public dataset
- ✅ 10 clearly labeled AI-generated essays
- ✅ Full provenance and sourcing documentation
- ✅ Reproducible via provided scripts
- ✅ Honest evaluation showing system limitations

### What This Dataset IS NOT
- ❌ NOT synthetic human essays labeled as human
- ❌ NOT fabricated or misattributed sources
- ❌ NOT cherry-picked to inflate accuracy
- ❌ NOT modified to make detection easier
- ❌ NOT claiming general-world accuracy from 20 essays

## Limitations

- **Small sample size**: 20 essays (statistical confidence limited)
- **Domain-specific**: College/student essays only
- **Temporal**: Human essays from 2012, AI from 2026
- **Prompt mismatch**: Human essays all used "laughter" prompt; AI essays varied
- **Single AI model**: Only tested Claude 3.5 Sonnet
- **No adversarial examples**: AI essays not optimized to evade detection

## Reproducibility Checklist

- [x] Dataset sources documented
- [x] Licenses verified (public domain)
- [x] Random seed specified (42)
- [x] Sampling methodology documented
- [x] Scripts provided (prepare_dataset.py, evaluate.py, analyze_failures.py)
- [x] Dependencies listed (requirements.txt)
- [x] Results include all predictions, not just aggregates
- [x] Failure cases analyzed in detail
- [x] Limitations explicitly stated

## Citation

If using this dataset or methodology:

```
AI Essay Detector Evaluation Dataset (2026)
- Human essays: ASAP-AES corpus (Kaggle/Hewlett Foundation, 2012)
  https://huggingface.co/datasets/llm-aes/asap-8-original
- AI essays: Claude 3.5 Sonnet generated essays
- Repository: https://github.com/Ankushsph/callus-project-2
```

## Contact

For questions about dataset methodology or reproduction issues, refer to the repository README and evaluation scripts.
