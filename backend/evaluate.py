"""
Evaluation script for AI essay detector.

Loads test dataset, runs detector, calculates metrics, identifies failure cases.

Usage:
    python evaluate.py
    
Requires:
    - data/test_essays.json with exactly 10 human + 10 AI essays
    - All backend dependencies installed
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
from pipeline import DetectionPipeline


class EvaluationError(Exception):
    """Raised when evaluation cannot proceed due to data issues."""
    pass


def load_test_dataset(path: str = "../data/test_essays.json") -> List[Dict[str, Any]]:
    """
    Load and validate test dataset.
    
    Returns:
        List of essay dictionaries with id, text, label, source
        
    Raises:
        EvaluationError: If dataset is invalid or incomplete
    """
    dataset_path = Path(__file__).parent / path
    
    if not dataset_path.exists():
        raise EvaluationError(f"Test dataset not found: {dataset_path}")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    essays = data.get('essays', [])
    
    if len(essays) == 0:
        raise EvaluationError("Test dataset is empty")
    
    # Count human and AI essays
    human_count = sum(1 for e in essays if e.get('label') == 'human')
    ai_count = sum(1 for e in essays if e.get('label') == 'ai')
    
    print(f"Dataset composition: {human_count} human, {ai_count} AI")
    
    # Validate dataset completeness
    if human_count != 10 or ai_count != 10:
        raise EvaluationError(
            f"Dataset incomplete: Found {human_count} human and {ai_count} AI essays. "
            f"Required: exactly 10 human + 10 AI essays."
        )
    
    # Validate required fields
    for essay in essays:
        required_fields = ['id', 'text', 'label', 'source']
        missing = [f for f in required_fields if f not in essay]
        if missing:
            raise EvaluationError(
                f"Essay {essay.get('id', '?')} missing required fields: {missing}"
            )
        
        if essay['label'] not in ['human', 'ai']:
            raise EvaluationError(
                f"Essay {essay['id']} has invalid label: {essay['label']} "
                f"(must be 'human' or 'ai')"
            )
    
    return essays


def classify_verdict(overall_score: float, threshold: float = 70.0) -> str:
    """
    Convert overall score to classification label.
    
    Args:
        overall_score: 0-100 score from detector
        threshold: Score above which essay is classified as AI
        
    Returns:
        'ai' or 'human'
    """
    return 'ai' if overall_score >= threshold else 'human'


def run_evaluation(
    essays: List[Dict[str, Any]], 
    pipeline: DetectionPipeline
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Run detector on all essays and calculate metrics.
    
    Args:
        essays: List of test essays with labels
        pipeline: Initialized detection pipeline
        
    Returns:
        Tuple of (predictions, metrics)
        - predictions: List of dicts with essay_id, actual, predicted, score, etc.
        - metrics: Dict with accuracy, precision, recall, f1, confusion_matrix
    """
    predictions = []
    
    print(f"\nRunning detector on {len(essays)} essays...")
    
    for essay in essays:
        essay_id = essay['id']
        text = essay['text']
        actual_label = essay['label']
        
        # Run detector
        result = pipeline.analyze(text)
        predicted_score = result['overall_score']
        predicted_label = classify_verdict(predicted_score)
        
        predictions.append({
            'essay_id': essay_id,
            'actual': actual_label,
            'predicted': predicted_label,
            'score': predicted_score,
            'verdict': result['verdict'],
            'sentence_count': len(result['sentences']),
            'analyzer_scores': {
                'perplexity': result.get('perplexity_score', 0),
                'burstiness': result.get('burstiness_score', 0),
                'lexical': result.get('lexical_score', 0),
                'pattern': result.get('pattern_score', 0),
            },
            'source': essay['source']
        })
        
        print(f"  Essay {essay_id}: actual={actual_label}, "
              f"predicted={predicted_label}, score={predicted_score:.1f}")
    
    # Calculate confusion matrix
    tp = sum(1 for p in predictions if p['actual'] == 'ai' and p['predicted'] == 'ai')
    tn = sum(1 for p in predictions if p['actual'] == 'human' and p['predicted'] == 'human')
    fp = sum(1 for p in predictions if p['actual'] == 'human' and p['predicted'] == 'ai')
    fn = sum(1 for p in predictions if p['actual'] == 'ai' and p['predicted'] == 'human')
    
    # Calculate metrics
    accuracy = (tp + tn) / len(predictions) if predictions else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    metrics = {
        'test_set_size': len(predictions),
        'accuracy': round(accuracy, 4),
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1': round(f1, 4),
        'confusion_matrix': {
            'true_positives': tp,
            'true_negatives': tn,
            'false_positives': fp,
            'false_negatives': fn
        }
    }
    
    print(f"\nMetrics:")
    print(f"  Accuracy:  {metrics['accuracy']:.2%}")
    print(f"  Precision: {metrics['precision']:.2%}")
    print(f"  Recall:    {metrics['recall']:.2%}")
    print(f"  F1 Score:  {metrics['f1']:.2%}")
    print(f"\nConfusion Matrix:")
    print(f"  TP={tp}, TN={tn}, FP={fp}, FN={fn}")
    
    return predictions, metrics


def identify_failure_cases(
    predictions: List[Dict[str, Any]], 
    essays: List[Dict[str, Any]],
    min_failures: int = 3
) -> List[Dict[str, Any]]:
    """
    Identify high-confidence incorrect predictions for analysis.
    
    Args:
        predictions: List of prediction results
        essays: Original essay data for text retrieval
        min_failures: Minimum number of failures to identify
        
    Returns:
        List of failure case dicts with essay_id, actual, predicted, 
        confidence, analyzer_scores, and text excerpt
    """
    # Find all incorrect predictions
    failures = [p for p in predictions if p['actual'] != p['predicted']]
    
    if not failures:
        print(f"\n⚠️  No misclassifications found. All {len(predictions)} essays classified correctly.")
        return []
    
    print(f"\nFound {len(failures)} misclassification(s)")
    
    # Sort by confidence (distance from 50.0 threshold)
    # High confidence failures are those far from the boundary
    for f in failures:
        f['confidence_distance'] = abs(f['score'] - 50.0)
    
    failures.sort(key=lambda x: x['confidence_distance'], reverse=True)
    
    # Take top failures (up to min_failures)
    top_failures = failures[:min_failures]
    
    # Enrich with essay text for analysis
    essay_lookup = {e['id']: e for e in essays}
    
    failure_cases = []
    for f in top_failures:
        essay = essay_lookup[f['essay_id']]
        
        failure_cases.append({
            'essay_id': f['essay_id'],
            'actual': f['actual'],
            'predicted': f['predicted'],
            'score': f['score'],
            'verdict': f['verdict'],
            'analyzer_scores': f['analyzer_scores'],
            'source': f['source'],
            'text_excerpt': essay['text'][:200] + ('...' if len(essay['text']) > 200 else ''),
            'analysis': "(Analysis pending - requires manual review)"
        })
    
    print(f"\nTop {len(failure_cases)} high-confidence failure(s) identified for analysis:")
    for fc in failure_cases:
        print(f"  Essay {fc['essay_id']}: {fc['actual']} → {fc['predicted']} "
              f"(score={fc['score']:.1f}, source={fc['source']})")
    
    return failure_cases


def save_results(
    metrics: Dict[str, Any],
    failure_cases: List[Dict[str, Any]],
    predictions: List[Dict[str, Any]],
    output_path: str = "../data/results.json"
) -> None:
    """
    Save evaluation results to JSON file.
    
    Args:
        metrics: Calculated metrics dict
        failure_cases: Identified failure cases for analysis
        predictions: Full prediction results
        output_path: Path to output JSON file
    """
    results_path = Path(__file__).parent / output_path
    
    results = {
        'description': 'Evaluation results on test set',
        'evaluated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'test_set_size': metrics['test_set_size'],
        'metrics': {
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'f1': metrics['f1']
        },
        'confusion_matrix': metrics['confusion_matrix'],
        'failure_cases': failure_cases,
        'all_predictions': predictions
    }
    
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Results saved to {results_path}")


def main():
    """Main evaluation workflow."""
    print("=" * 70)
    print("AI Essay Detector - Evaluation")
    print("=" * 70)
    
    try:
        # Load dataset with validation
        print("\n1. Loading test dataset...")
        essays = load_test_dataset()
        print(f"✅ Loaded {len(essays)} essays")
        
        # Initialize pipeline
        print("\n2. Initializing detection pipeline...")
        pipeline = DetectionPipeline()
        print("✅ Pipeline ready")
        
        # Run evaluation
        print("\n3. Running evaluation...")
        predictions, metrics = run_evaluation(essays, pipeline)
        
        # Identify failure cases
        print("\n4. Identifying failure cases...")
        failure_cases = identify_failure_cases(predictions, essays, min_failures=3)
        
        if failure_cases:
            print("\n⚠️  Manual analysis required:")
            print("   Review the failure cases and add 'analysis' field explaining why each failed.")
        
        # Save results
        print("\n5. Saving results...")
        save_results(metrics, failure_cases, predictions)
        
        print("\n" + "=" * 70)
        print("Evaluation complete!")
        print("=" * 70)
        
    except EvaluationError as e:
        print(f"\n❌ Evaluation failed: {e}")
        print("\nTo complete evaluation:")
        print("1. Add 10 human-written essays to data/test_essays.json")
        print("2. Ensure each has: id, text, label='human', source")
        print("3. Re-run: python evaluate.py")
        return 1
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
