"""Manual test script to verify pipeline without pytest."""

# Test that imports work
try:
    from schemas import AnalyzeRequest, AnalyzeResponse, SentenceResult
    print("✓ Schemas imported successfully")
except Exception as e:
    print(f"✗ Schema import failed: {e}")
    exit(1)

# Test pipeline (will need spaCy model)
print("\nNote: Pipeline test requires spaCy model 'en_core_web_sm' to be installed")
print("Run: python -m spacy download en_core_web_sm")
print("\nSkipping pipeline test for now (requires dependencies).")
print("\n✓ Phase 1 structure verification complete")
print("\nNext: Install dependencies and run pytest")
