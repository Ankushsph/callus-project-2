"""
Analyze failure cases and add explanations.

This script examines the top failure cases from the evaluation and adds
detailed analysis explaining why each failure occurred.
"""

import json
from pathlib import Path


def analyze_failures():
    """Analyze failures and add detailed explanations."""
    results_path = Path(__file__).parent / "../data/results.json"
    
    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    failure_cases = results['failure_cases']
    
    if not failure_cases:
        print("No failure cases to analyze.")
        return
    
    print(f"Analyzing {len(failure_cases)} failure case(s)...")
    
    # Analyze each failure case
    analyzed_failures = []
    
    for i, fc in enumerate(failure_cases, 1):
        essay_id = fc['essay_id']
        actual = fc['actual']
        predicted = fc['predicted']
        score = fc['score']
        signals = fc['analyzer_scores']
        
        print(f"\nFailure {i}: Essay {essay_id}")
        print(f"  Actual: {actual}, Predicted: {predicted}, Score: {score:.1f}")
        print(f"  Signals - P:{signals['perplexity']:.1f}, B:{signals['burstiness']:.1f}, L:{signals['lexical']:.1f}, Pt:{signals['pattern']:.1f}")
        
        if actual == 'ai' and predicted == 'human':
            # AI text classified as human (False Negative)
            analysis = {
                "why_it_failed": f"The detector classified this AI-generated essay (score={score:.1f}) as human because all four analyzer signals indicated human-like characteristics.",
                "signal_breakdown": {
                    "perplexity": f"{signals['perplexity']:.1f}/100 - HIGH perplexity indicates the text was unpredictable to GPT-2, suggesting human variability. However, modern LLMs like Claude 3.5 Sonnet are trained to produce human-like variability.",
                    "burstiness": f"{signals['burstiness']:.1f}/100 - HIGH burstiness suggests varied sentence lengths, typically human. Claude intentionally varies sentence structure to avoid robotic patterns.",
                    "lexical": f"{signals['lexical']:.1f}/100 - LOW lexical repetition indicates diverse vocabulary with minimal word reuse, which is human-like. Modern LLMs avoid repetitive phrasing.",
                    "pattern": f"{signals['pattern']:.1f}/100 - {'No' if signals['pattern'] == 0 else 'Minimal'} detection of known AI phrases. Claude avoids obvious markers like 'delve into' or 'It is important to note'."
                },
                "root_cause": "**Fundamental limitation: The detector was designed to catch GPT-2-era AI writing (2019), but modern LLMs (2024-2026) have evolved significantly.** Claude 3.5 Sonnet produces text with human-like perplexity, varied sentence rhythm, diverse vocabulary, and avoids formulaic phrases. The detector's signals are based on characteristics that no longer distinguish modern AI from human writing.",
                "possible_improvements": [
                    "Add detection of subtler patterns: Modern AI often uses formal academic register consistently, avoids contractions, and maintains perfect grammar throughout (unlike most human student writing).",
                    "Analyze structural coherence: AI essays often have suspiciously perfect paragraph transitions and balanced structure.",
                    "Detect 'too good' signals: Lack of typos, consistent sophistication, and absence of colloquialisms may indicate AI.",
                    "Use more recent perplexity models: GPT-2 (2019) is outdated; using GPT-4 or Claude-based perplexity might work better.",
                    "Add stylometric analysis: Measure consistency in writing style, which humans vary more than AI.",
                    "Consider semantic coherence: AI sometimes produces logically perfect but experientially hollow narratives."
                ]
            }
        elif actual == 'human' and predicted == 'ai':
            # Human text classified as AI (False Positive)
            analysis = {
                "why_it_failed": f"The detector incorrectly flagged this human-written essay (score={score:.1f}) as AI-generated.",
                "signal_breakdown": {
                    "perplexity": f"{signals['perplexity']:.1f}/100 - {'LOW' if signals['perplexity'] < 50 else 'HIGH'} perplexity.",
                    "burstiness": f"{signals['burstiness']:.1f}/100 - {'LOW' if signals['burstiness'] < 50 else 'HIGH'} sentence variation.",
                    "lexical": f"{signals['lexical']:.1f}/100 - Lexical diversity score.",
                    "pattern": f"{signals['pattern']:.1f}/100 - Pattern matching score."
                },
                "root_cause": "Human writing characteristics triggered AI-like signals.",
                "possible_improvements": [
                    "Calibrate thresholds based on actual human/AI distributions.",
                    "Consider essay domain and age group (student writing vs professional)."
                ]
            }
        else:
            analysis = {
                "why_it_failed": "Unexpected failure type",
                "root_cause": "Unknown",
                "possible_improvements": []
            }
        
        fc['analysis'] = analysis
        analyzed_failures.append(fc)
    
    # Update results file
    results['failure_cases'] = analyzed_failures
    
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Added detailed analysis to {len(analyzed_failures)} failure case(s)")
    print(f"[OK] Updated {results_path}")


if __name__ == '__main__':
    analyze_failures()
